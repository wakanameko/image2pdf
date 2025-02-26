# image2pdf
## 概要
Python3と[諸々のライブラリ](https://github.com/wakanameko/image2pdf/blob/main/requirements.txt)を用いて、画像ファイル群を1つのPDFファイルにします。  

## 動作確認環境
以下の環境にて動作確認済み。
|Windows       |MacOS (OSX)        |Linux|
|:------------:|:-----------------:|:---:|
|Windows10     |MacOS Catalina     |     |
|Windows7      |MacOS High Sierra  |     |　　

100枚程度のpng画像からの変換を動作確認として行いました。  
Macについては、iMac 21.5 late 2009にて動作確認しています。MacBook Air 2011, 2012では動作しませんでした。  


## その他  
メモリをかなり消費するので、フリーのメモリが1GB以上あるときに実行すると安定します。

---
# Change Log
## 1.4
その他
- 例外処理を強化
## 1.3
GUI
- 「対象の画像形式」テキストを追加
- 翻訳ファイルの追加と、それに対応するためラベルの変更

その他
- ウィンドウが閉じれない問題を修正
- 例外処理を強化
## 1.2
GUI
- ステータス表示を追加
- 対象ファイルの拡張子選択ボックスを追加
- フォントをOSのデフォルトに強制指定

その他
- Windows7での動作を保証
- ウィンドウを閉じた際に自動で設定を保存
- ソフトを終了するショートカットキーを追加
- 例外処理を強化
## 1.1
プログレスバーの追加と諸々。
## 1.0
リリースしました。現段階では、pngからの変換しかできません。  
変換は、名前の昇順で実行されていきます。
