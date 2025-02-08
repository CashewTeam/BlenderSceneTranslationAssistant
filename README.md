# BlenderSceneTranslationAssistant

A small add-on for translating collection/object/material/texture filenames in Blender project files, developed using DeepSeek R1.

For node translation recommendations, please use the [Geometry Nodes Translation Add-on](https://www.bilibili.com/video/BV1An4y1979Q/) developed by [Xinyu Zhu](https://afdian.com/a/ycyxz).

## Usage Guide

The collection/object/material renaming panel is located in:`3D View` → `N Panel` → `Tools` → `Scene Translator`

1. Click `Extract & Copy Scene Texts` to extract and copy text. For small text volumes, you can directly paste into translation tools. Some translation tools may lose line breaks - try alternative tools if this occurs.
2. For large text volumes:

   - Paste text into Excel first
   - Batch translate according to translation tool's character limits
   - Recommended tool: [YandexTranslate](https://translate.yandex.com) (10k character limit, preserves line breaks)
3. After translating, paste text and click `Paste Scene Texts` to verify correspondence.
4. Click `Apply Scene Renaming` to complete translation.

Material renaming follows similar steps. The panel is located in:
`Node Editor` → `N Panel` → `Tools` → `Texture Translator`



# Blenderシーン翻訳アシスタント

Blenderプロジェクトファイル内のコレクション、オブジェクト、マテリアル、テクスチャマップのファイル名を翻訳するための小さなアドオンです。DeepSeek R1を使用して開発されました。

ノードの翻訳には、[異次元学者](https://afdian.com/a/ycyxz)が開発した[ジオメトリノード翻訳プラグイン](https://www.bilibili.com/video/BV1An4y1979Q/)の使用を推奨します。

## 使用方法

コレクション、オブジェクト、マテリアルの名前変更パネルは、  
`3Dビュー` → `Nパネル` → `ツール` → `Scene Translator` にあります。

1. `Extract & Copy Scene Texts`をクリックしてテキストを抽出し、コピーします。テキスト量が少ない場合は、直接翻訳ツールに貼り付けて翻訳できます。一部の翻訳ツールでは改行が失われる場合があるため、その場合は別のツールを試してください。

2. テキスト量が多い場合：  
   - まずテキストをExcelに貼り付けます  
   - 翻訳ツールの文字数制限に従ってバッチ翻訳します  
   - 推奨ツール: [YandexTranslate](https://translate.yandex.com)（1万字制限、改行を保持）

3. 翻訳後、テキストを貼り付けて`Paste Scene Texts`をクリックし、テキストが正しく対応しているか確認します。

4. `Apply Scene Renaming`をクリックして翻訳を完了します。

マテリアルの名前変更も同様の手順です。パネルは、  
`ノードエディター` → `Nパネル` → `ツール` → `Texture Translator` にあります。




# Blender场景翻译助手

一个用于翻译Blender工程文件中的集合、物品、材质、贴图文件名的小插件，使用DeepSeek R1编写。

如果需要使用节点翻译推荐使用[异次元学者](https://afdian.com/a/ycyxz)开发的[几何节点翻译插件](https://www.bilibili.com/video/BV1An4y1979Q/)

## 使用方法

集合、物品、材质重名名面板位于`3D视图`-`N面板`-`工具`-`Scence Translator`

点击`Extract & Copy Scene Texts`第一个按提取并复制文本，如果文本量较小可以直接粘贴到翻译工具中翻译，部分情况下翻译工具会导致换行丢失可以更换翻译工具。

如果文本量较大可以先将文本粘贴到Excel表格中，按照翻译工具字数限制分批次翻译，推荐使用[YandexTranslate](https://translate.yandex.com)，字数限制为1W字，且不会丢失换行符。

将翻译后的文本复制后，点击`Paste Scene Texts`，可以检查一下文本是否正确对应。

点击`Apply Scene Renaming`完成翻译。

材质重命名方法类似，面板位于`节点编辑器`-`N面板`-`工具`-`Texture Translator`
