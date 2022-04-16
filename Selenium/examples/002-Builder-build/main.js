const {Builder, Browser} = require('selenium-webdriver');

(async () => {

    // https://www.selenium.dev/selenium/docs/api/javascript/module/selenium-webdriver/index_exports_Browser.html
    var str_browserName = Browser.CHROME;

    // https://www.selenium.dev/selenium/docs/api/javascript/module/selenium-webdriver/index_exports_ThenableWebDriver.html
    var obj_webDriver = await new Builder()
        .forBrowser(str_browserName)
        .build()
    ;

    // Set screen resolution as XGA size
    await obj_webDriver.manage().window().setRect({
        width:1024,
        height:768
    });

    // Navigate to
    await obj_webDriver.get('https://github.com/');

})();
