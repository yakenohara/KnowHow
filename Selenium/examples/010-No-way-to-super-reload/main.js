const {Builder, Browser, Capabilities, logging} = require('selenium-webdriver');

(async function(){

    var str_navigateTo = 'https://github.com/';
    var str_browserName = Browser.FIREFOX;

    var obj_webDriver;
    for(let int_idx = 0 ; int_idx < 2 ; int_idx++){

        console.log('Starting session...');

        // すでにブラウザを開いていたら、閉じる
        if((typeof obj_webDriver) === 'object' && obj_webDriver.constructor.name === 'Driver'){
            await obj_webDriver.quit();
            obj_webDriver = undefined;
        }

        // Create WebDriver object
        obj_webDriver = await new Builder()
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

        console.log(`Accessing Times:${int_idx+1}`)

        // Navigate
        await obj_webDriver.get(str_navigateTo);

        console.log(`Opened "${str_navigateTo}"`);

    }

    console.log('Done!');
    
})();
