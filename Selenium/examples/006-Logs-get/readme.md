# Point

## 1

https://www.selenium.dev/selenium/docs/api/javascript/module/selenium-webdriver/lib/logging.html  
↑  
公式ドキュメントでは `remote logging API` と説明されている。  
執筆時点では、ページの説明にあるように、一部ブラウザ(chrome, firefox)のみ対応。  

## 2
entry.message には、以下のように console.log() に渡した文字列以外も付加されている。  
`console-api 2:32 "hello console"`  

なので `entry.message === 'hello console'` のように比較はできない。  

