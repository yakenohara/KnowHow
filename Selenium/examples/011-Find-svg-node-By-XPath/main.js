const {Builder, Browser, By, Capabilities, logging} = require('selenium-webdriver');

(async () => {

    // https://www.selenium.dev/selenium/docs/api/javascript/module/selenium-webdriver/index_exports_Browser.html
    var str_browserName = Browser.CHROME;

    // https://www.selenium.dev/selenium/docs/api/javascript/module/selenium-webdriver/index_exports_ThenableWebDriver.html
    var obj_webDriver = await new Builder()
        .withCapabilities(

            // https://www.selenium.dev/selenium/docs/api/javascript/module/selenium-webdriver/index_exports_Capabilities.html
            new Capabilities()
                .setBrowserName(str_browserName)
        )
        .build()
    ;

    // Set screen resolution as XGA size
    await obj_webDriver.manage().window().setRect({
        width:1024,
        height:768
    });

    // Navigate to
    await obj_webDriver.get('http://localhost:8000/');

    var obj_elements = await obj_webDriver.findElements(

        // https://www.selenium.dev/selenium/docs/api/javascript/module/selenium-webdriver/lib/by_exports_By.html#By.xpath
        By.xpath(
            `/html` +
                `/body` +
                    `/*[name()="svg"]` +
                        `/*[name()="g"]` +
                            `/*[name()="text"]` +
                                `/*[name()="tspan"]`
            // note
            // The <svg> elements are not from the XHTML namespace but belongs to SVG namespace.
            // https://stackoverflow.com/questions/49024052/creating-xpath-for-svg-tag
        )
    );

    console.log(`obj_elements.length:${obj_elements.length}`);

    if(obj_elements.length == 1){

        // https://www.selenium.dev/selenium/docs/api/javascript/module/selenium-webdriver/lib/webdriver_exports_WebElement.html#getText
        let str_textContent = await obj_elements[0].getText();

        console.log(`str_textContent:${str_textContent}`);
    }

})();
