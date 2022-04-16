
# Point

`.build()` で帰ってくる WebDriver object は、  
毎回新しいプロファイルでブラウザを起動した事と同じになる。  
これは、ブラウジング履歴も、cache も、cookie もまっさらな状態で起動するという事。  
https://groups.google.com/forum/#!topic/selenium-users/UX1Znrrb98Q  

すくなくとも、確認環境(ChromeDriver 81.0.4044.69) では、  
ページのリロード時に cache, cookie を無視するオプションが存在しないので、  
代わりに WebDriver object を破棄して再び `.build()` するしかない。  
