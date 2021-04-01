const {Builder, Browser, By, Capabilities, until} = require('selenium-webdriver');

(async function(){

    var str_navigateTo = 'http://localhost:8000/';

    var str_browserName = Browser.CHROME;
    
    // Create WebDriver object
    var obj_webDriver = await new Builder()
        .withCapabilities(
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

    // Navigate
    await obj_webDriver.get(str_navigateTo);

    // Get <textarea> object
    var obj_element = await obj_webDriver.wait(until.elementLocated(By.id('txtx')), 3000);

    // Read initial content
    var str_textContent = await obj_element.getText();
    console.log(`[1]<.getText()> str_textContent:"${str_textContent}"`);
    console.log(`[2]<.getAttribute('value')> str_textContent:"${str_textContent}"`);

    // Clear and Read
    await obj_element.clear();
    var str_textContent = await obj_element.getText();
    console.log(`[2]<.clear()> str_textContent:"${str_textContent}"`);
    var str_textContent = await obj_element.getAttribute('value');
    console.log(`[2]<.getAttribute('value')> str_textContent:"${str_textContent}"`);

    // Input text and Read
    await obj_element.sendKeys("updated text");
    var str_textContent = await obj_element.getText();
    console.log(`[3]<.sendKeys("updated text")> str_textContent:"${str_textContent}"`);
    var str_textContent = await obj_element.getAttribute('value');
    console.log(`[2]<.getAttribute('value')> str_textContent:"${str_textContent}"`);

})();
