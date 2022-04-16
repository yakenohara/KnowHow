# Point

clipborad 操作の手段はいろいろ。  
知りうる限りで以下の通り。  

 - clipboard.v2.0.4.js  
 - document.execCommand  
 - window.clipboardData  
 - event.clipboardData(button click)  
 - event.clipboardData(browser event)  
 - Asynchronous Clipboard API  

各手段をブラウザ毎に実行してみたテスト結果は `\test\result.xlsx` を参照  
(※`Asynchronous Clipboard API` はやってないよ)  

# `ctrl+x`, `ctrl+c`, `ctrl+v` イベントを オーバーライドするには

以下がベストプラクティス  
実装例は `\example` 配下を参照

## ie11 の場合は、

1. ブラウザの `cut`, `copy`, `paste` イベントを無視する  
   ※このイベント内で `window.clipboardData.setData()` とやろうとしても、  
   イベント自体を取得できないことがある為。  
   (少なくとも、`contenteditable="false"` な `div` 要素をクリック後に  
    `ctrl+x` or `ctrl+v` しても、 cut/paste event は拾えなかった。)

↓ `cut` イベントを無視する実装例 ↓  
```javascript
document.addEventListener('cut', function(e){
    e.preventDefault();
});
```
2. `ctrl+x`, `ctrl+c`, `ctrl+v` キーボードイベント内で、  
   `window.clipboardData` の `.setData()`, `.getData()` をコールする  
   ※`ctrl+x` のようなコンボキーのイベント取得は 素の JavaScript だけではしんどいので、  
   [Mousetrap](https://github.com/ccampbell/mousetrap) 等の外部ライブラリを使うのがオススメ

↓ mousetrap v1.6.2 と mousetrap-global-bind.js を利用した `ctrl+x` イベントの実装例 ↓  
```javascript
var mousetrapInstance = new Mousetrap();
mousetrapInstance.bindGlobal("ctrl+x", function(e, combo){
    window.clipboardData.setData('text/plain', str);
    e.preventDefault();
});
```

## ie11 以外の場合は、

1. ブラウザの `cut`, `copy`, `paste` イベント内で、  
   `event.clipboardData` の `.setData()`, `.getData()` をコールしてから、  
   ブラウザデフォルト動作をキャンセルする  

↓ 実装例 ↓  
```javascript
document.addEventListener('cut', function(e){
    e.clipboardData.setData('text/plain', str);
    e.preventDefault();
});
```

# 参考リンク

## document.execCommand("Copy");

[クリック一つでクリップボードにコピーする機能（HTMLとJavaScriptのみで実現)](https://www.marorika.com/entry/copy-to-clipboard)

[JavaScriptでクリップボードに文字をコピーする(ブラウザ)](https://qiita.com/simiraaaa/items/2e7478d72f365aa48356)

[Clipboard API について](https://hakuhin.jp/js/clipboard.html)

[クリップボードへのアクセス](https://so-zou.jp/web-app/tech/programming/javascript/dom/node/document/clipboard.htm)

## clipboard API

[clipboardData.itemsでデータを引っ張ってくる](https://qiita.com/kwst/items/8d9cd40e181761085325)

[Chrome, Firefox, IEのCopy & Paste実装方法](https://qiita.com/saitoxu/items/b317ccde7e2af9797288)

## Async Clipboard API

[Async Clipboard APIでJavaScriptからクリップボードを操作する](https://sbfl.net/blog/2018/03/03/async-clipboard-api/)

[Asynchronous Clipboard API Sample](https://googlechrome.github.io/samples/async-clipboard/)
