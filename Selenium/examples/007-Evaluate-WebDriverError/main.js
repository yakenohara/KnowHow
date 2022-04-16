const {Builder, Browser, Capabilities, logging} = require('selenium-webdriver');

(async () => {

    // https://www.selenium.dev/selenium/docs/api/javascript/module/selenium-webdriver/index_exports_Browser.html
    var str_browserName = Browser.CHROME;

    // https://www.selenium.dev/selenium/docs/api/javascript/module/selenium-webdriver/lib/logging_exports_Type.html
    var str_logType = logging.Type.BROWSER;

    // https://www.selenium.dev/selenium/docs/api/javascript/module/selenium-webdriver/lib/logging_exports_Level.html
    var obj_logLevel = logging.Level.ALL;
    
    // https://www.selenium.dev/selenium/docs/api/javascript/module/selenium-webdriver/index_exports_ThenableWebDriver.html
    var obj_webDriver = await new Builder()
        .withCapabilities(

            // https://www.selenium.dev/selenium/docs/api/javascript/module/selenium-webdriver/index_exports_Capabilities.html
            new Capabilities()
                .setBrowserName(str_browserName)
                .setLoggingPrefs(

                    // Use IIFE to make and get logging.Preferences object 
                    (function(){
                        // https://www.selenium.dev/selenium/docs/api/javascript/module/selenium-webdriver/lib/logging.html
                        var obj_logPrefs = new logging.Preferences();
                        obj_logPrefs.setLevel(str_logType, obj_logLevel);
                        return obj_logPrefs;
                    })()
                )
        )
        .build()
    ;

    // Set screen resolution as XGA size
    await obj_webDriver.manage().window().setRect({
        width:1024,
        height:768
    });

    // Navigate to
    await obj_webDriver.get('https://github.com/');

    // `console.log()`
    await obj_webDriver.executeScript('console.log(\'hello console\');');

    var str_expectedString = 'hello console';
    var int_waitMS = 3000;
    
    await obj_webDriver
        .wait(async () => {
            
            var bl_gotLog = false;

            await obj_webDriver
                .manage()
                .logs()
                .get(logging.Type.BROWSER)
                .then(entries => {
                    entries.forEach( entry => {

                        console.log(`[${entry.level.name}(Lv:${entry.level.value})] ${entry.message}`);

                        // note
                        // .message には、以下のように console.log() に渡した文字列以外も付加されている。
                        // `console-api 2:32 "hello console"`
                        if(entry.message.indexOf(str_expectedString) != (-1)){
                            console.log("OK");
                            bl_gotLog = true;
                        }
                    });
                })
            ;

            return bl_gotLog;

        },int_waitMS)
        .catch(function(e){

            // note 
            // https://www.selenium.dev/selenium/docs/api/javascript/module/selenium-webdriver/index_exports_ThenableWebDriver.html
            // ↑ Interface ThenableWebDriver の説明↑ では time out 時に TypeError が throw されるとあるが、
            // 実際は`Class TimeoutError`(<- `Class WebDriverError` の sub class)。
            // なのでこのエラーを判定を判定する方法は ↓↓ になる
            if( (typeof e) === 'object' && e.constructor.name === "TimeoutError"){
                console.log("NG");
            
            }else{
                throw e;
            }
        })
    ;

})();
