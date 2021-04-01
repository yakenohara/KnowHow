# How to Run

1. index.html にローカルでアクセスできるように、`py -m http.server` しておく
2. 別窓でこのディレクトリ配下をカレントディレクトリにして、`node main.js` する
   
# Point

(Class WebElement).getText() では、`<textarea>` 内の文字列は取得できない。  
(Class WebElement).getAttribute('value') を使う。  
