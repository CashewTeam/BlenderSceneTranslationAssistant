import bpy
import os
from bpy.types import Operator, Panel, UIList, PropertyGroup
from bpy.props import StringProperty, CollectionProperty, IntProperty

bl_info = {
    "name": "Scene Translation Assistant 场景翻译助手",
    "blender": (2, 80, 0),
    "category": "Tool",
    "author": "Con11 & DeepSeek R1",
    "version": (1, 0),
    "description": "Combined material and scene translation tools",
}

# 公共工具函数 ===========================================
def copy_to_clipboard(text: str):
    bpy.context.window_manager.clipboard = text

def read_clipboard() -> str:
    return bpy.context.window_manager.clipboard

# ========================================================
# 材质翻译插件部分
# ========================================================
class MaterialTextItem(PropertyGroup):
    original_text: StringProperty()
    translated_text: StringProperty()
    filepath: StringProperty()

class MATERIAL_UL_TranslationList(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.prop(item, "original_text", text="", emboss=False)
            row.prop(item, "translated_text", text="", emboss=True)
        else:
            layout.label(text="")

class MATERIAL_OT_ExtractTexts(Operator):
    bl_idname = "material.extract_texts"
    bl_label = "Extract & Copy Texture Texts"
    
    def execute(self, context):
        scene = context.scene
        scene.material_text_items.clear()
        
        for img in bpy.data.images:
            if img.source == 'FILE' and not img.packed_file:
                filepath = bpy.path.abspath(img.filepath)
                filename = os.path.basename(filepath)
                name, ext = os.path.splitext(filename)
                
                item = scene.material_text_items.add()
                item.original_text = name
                item.translated_text = name
                item.filepath = filepath
        
        text = '\n'.join([item.original_text for item in scene.material_text_items])
        copy_to_clipboard(text)
        return {'FINISHED'}

class MATERIAL_OT_PasteTexts(Operator):
    bl_idname = "material.paste_texts"
    bl_label = "Paste Texture Texts"
    
    def execute(self, context):
        text = read_clipboard()
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        items = context.scene.material_text_items
        for i in range(min(len(lines), len(items))):
            items[i].translated_text = lines[i]
        return {'FINISHED'}

class MATERIAL_OT_ReplaceTexts(Operator):
    bl_idname = "material.replace_texts"
    bl_label = "Apply Texture Renaming"
    
    def execute(self, context):
        for item in context.scene.material_text_items:
            if item.translated_text and item.original_text != item.translated_text:
                old_abs_path = item.filepath
                dirname = os.path.dirname(old_abs_path)
                ext = os.path.splitext(old_abs_path)[1]
                new_abs_path = os.path.join(dirname, f"{item.translated_text}{ext}")
                
                try:
                    if os.path.exists(old_abs_path):
                        os.rename(old_abs_path, new_abs_path)
                        new_rel_path = bpy.path.relpath(new_abs_path)
                        
                        for img in bpy.data.images:
                            if bpy.path.abspath(img.filepath) == old_abs_path:
                                img.filepath = new_rel_path
                                img.name = item.translated_text
                                img.reload()
                        
                        item.filepath = new_abs_path
                        item.original_text = item.translated_text
                except Exception as e:
                    self.report({'ERROR'}, f"Error: {str(e)}")
        return {'FINISHED'}

class NODE_PT_MaterialTranslation(Panel):
    bl_label = "Texture Translator"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Tool"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.operator(MATERIAL_OT_ExtractTexts.bl_idname, icon='COPYDOWN')
        layout.operator(MATERIAL_OT_PasteTexts.bl_idname, icon='PASTEDOWN')
        layout.template_list(
            "MATERIAL_UL_TranslationList", 
            "", 
            scene, 
            "material_text_items", 
            scene, 
            "material_text_items_index"
        )
        layout.operator(MATERIAL_OT_ReplaceTexts.bl_idname, icon='FILE_REFRESH')

# ========================================================
# 场景翻译插件部分
# ========================================================
class SceneTranslationItem(PropertyGroup):
    original: StringProperty()
    translated: StringProperty()

class SCENE_UL_TranslationList(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.label(text=item.original)
            row.prop(item, "translated", text="", emboss=True)
        else:
            layout.label(text="")

class SCENE_OT_ExtractTexts(Operator):
    bl_idname = "scene.extract_texts"
    bl_label = "Extract & Copy Scene Texts"
    
    def execute(self, context):
        wm = context.window_manager
        wm.scene_translation_items.clear()
        
        names = []
        names.extend(obj.name for obj in bpy.data.objects)
        names.extend(mat.name for mat in bpy.data.materials)
        names.extend(col.name for col in bpy.data.collections)
        
        seen = set()
        for name in sorted(list(set(names)), key=names.index):
            if name not in seen:
                seen.add(name)
                item = wm.scene_translation_items.add()
                item.original = name
        
        text = "\n".join([item.original for item in wm.scene_translation_items])
        copy_to_clipboard(text)
        return {'FINISHED'}

class SCENE_OT_PasteTexts(Operator):
    bl_idname = "scene.paste_texts"
    bl_label = "Paste Scene Texts"
    
    def execute(self, context):
        text = read_clipboard()
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        items = context.window_manager.scene_translation_items
        for i in range(min(len(lines), len(items))):
            items[i].translated = lines[i]
        return {'FINISHED'}

class SCENE_OT_ReplaceTexts(Operator):
    bl_idname = "scene.replace_texts"
    bl_label = "Apply Scene Renaming"
    
    def execute(self, context):
        wm = context.window_manager
        name_map = {item.original: item.translated for item in wm.scene_translation_items if item.translated.strip()}
        
        for obj in bpy.data.objects:
            if obj.name in name_map:
                obj.name = name_map[obj.name]
        
        for mat in bpy.data.materials:
            if mat.name in name_map:
                mat.name = name_map[mat.name]
        
        for col in bpy.data.collections:
            if col.name in name_map:
                col.name = name_map[col.name]
        
        return {'FINISHED'}

class VIEW3D_PT_SceneTranslation(Panel):
    bl_label = "Scene Translator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"
    
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        
        layout.operator(SCENE_OT_ExtractTexts.bl_idname, icon='COPYDOWN')
        layout.operator(SCENE_OT_PasteTexts.bl_idname, icon='PASTEDOWN')
        layout.template_list(
            "SCENE_UL_TranslationList",
            "",
            wm,
            "scene_translation_items",
            wm,
            "scene_translation_index"
        )
        layout.operator(SCENE_OT_ReplaceTexts.bl_idname, icon='FILE_REFRESH')

# ========================================================
# 注册和注销
# ========================================================
classes = (
    # 材质翻译插件
    MaterialTextItem,
    MATERIAL_UL_TranslationList,
    MATERIAL_OT_ExtractTexts,
    MATERIAL_OT_PasteTexts,
    MATERIAL_OT_ReplaceTexts,
    NODE_PT_MaterialTranslation,
    
    # 场景翻译插件
    SceneTranslationItem,
    SCENE_UL_TranslationList,
    SCENE_OT_ExtractTexts,
    SCENE_OT_PasteTexts,
    SCENE_OT_ReplaceTexts,
    VIEW3D_PT_SceneTranslation
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # 材质翻译数据存储在Scene
    bpy.types.Scene.material_text_items = CollectionProperty(type=MaterialTextItem)
    bpy.types.Scene.material_text_items_index = IntProperty()
    
    # 场景翻译数据存储在WindowManager
    bpy.types.WindowManager.scene_translation_items = CollectionProperty(type=SceneTranslationItem)
    bpy.types.WindowManager.scene_translation_index = IntProperty()

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.material_text_items
    del bpy.types.Scene.material_text_items_index
    del bpy.types.WindowManager.scene_translation_items
    del bpy.types.WindowManager.scene_translation_index

if __name__ == "__main__":
    register()