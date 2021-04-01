# Install

## Download 
https://github.com/UB-Mannheim/tesseract/wiki  
![](assets/images/download.svg)  

`Additionalscript data` と `Additional language data` ので日本語データを追加する  
![](assets/images/2020-07-23-17-13-00.png)  

`Additionalscript data` を開いて `Japanese` と `Japanese(vertical)` (<- 縦書き用) にチェック  
![](assets/images/2020-07-23-17-13-29.png)  

`Additional language data` を開いて `Japanese` と `Japanese(vertical)` (<- 縦書き用) にチェック  
![](assets/images/2020-07-23-17-13-35.png)  

あとはすべて OK でいい。

## 環境変数設定

`PATH` に以下を追加(Tesseract のインストールディレクトリ)
![](assets/images/PATH.svg)  

`TESSDATA_PREFIX` を以下のように追加定義( `~\Tesseract-OCR\` は Tesseract のインストールディレクトリ)  
(※この環境変数は コマンドプロンプト上での -l オプションで言語を指定する時に必要。この環境変数がないと `-l` を入力ファイルパスと解釈してしまう)  
![](assets/images/TESSDATA_PREFIX.svg)  

