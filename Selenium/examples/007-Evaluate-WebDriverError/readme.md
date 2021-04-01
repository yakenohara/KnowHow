# Point

https://www.selenium.dev/selenium/docs/api/javascript/module/selenium-webdriver/index_exports_ThenableWebDriver.html  
↑ Interface ThenableWebDriver の説明↑ では time out 時に TypeError が throw されるとあるが、  
実際は`Class TimeoutError`(<- `Class WebDriverError` の sub class)。  
なのでこのエラーを判定を判定する方法は ↓↓ になる  

```
if( (typeof e) === 'object' && e.constructor.name === "TimeoutError")
```
