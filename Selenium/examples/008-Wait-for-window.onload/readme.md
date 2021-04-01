# Point
(Class WebDriver).get(url) の完了は window.onload と同じ。  
なので このスクリプトのように独自に `window.addEventListener("load", ~` しても、  
onload イベントは取得できない  
