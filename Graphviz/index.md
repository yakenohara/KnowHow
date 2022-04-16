# Install

以下からダウンロード。  

http://www.graphviz.org/download/  
または  
https://web.archive.org/web/20150402023342/http://www.graphviz.org/Download_windows.php  

インストーラーを実行するだけ。

# パスを通す

`\bin` ディレクトリを指定する。  
↓Windows10(64bit)の例。

```
C:\Program Files (x86)\Graphviz2.38\bin
```

# Example

同封の Dot ファイル `/example/ExampleDiagram.dot` を svg 画像に変換する例。  
以下 cmd Command で svg ファイルを得られる。

```
dot -Tsvg ".\example\ExampleDiagram.dot" -o ".\example\ExampleDiagram.svg"
```

## POINT

 - label に スペース, 改行 を含む場合は `"` で囲む
