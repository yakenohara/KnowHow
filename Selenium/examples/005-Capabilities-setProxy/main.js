const {Builder, Browser, Capabilities} = require('selenium-webdriver');
const proxy = require('selenium-webdriver/proxy');

(async () => {

    // https://www.selenium.dev/selenium/docs/api/javascript/module/selenium-webdriver/index_exports_Browser.html
    var str_browserName = Browser.CHROME;

    // note
    // プロキシを通してアクセスする場合は、インターネットオプションと同様の設定を行う。
    // https://www.selenium.dev/selenium/docs/api/javascript/module/selenium-webdriver/proxy.html
    //
    // <caution!>
    // この時、socksプロトコル以外のプロトコルを使ったプロキシの場合は、ユーザ名・パスワードは設定できない。
    // ブラウザに表示された Auth dialog に自分で入力する。
    // <reference>
    // ↓ Chrome の `onAuthRequired` イベントを取得して、                                 ↓
    // ↓ USERNAME, PASSWORD を設定させる Chrome extension を実装してしまうトリッキーな例 ↓
    // https://stackoverflow.com/questions/55582136/how-to-set-proxy-with-authentication-in-selenium-chromedriver-python
    // </reference>
    //
    // </caution!>
    //
    // ↓ http, https proxy ↓
    // ```
    // var obj_proxySettings = new proxy.manual({
    //     http: '<proxyserver.domain>:<port>',
    //     https: '<proxyserver.domain>:<port>'
    // });
    // ```
    //
    // ↓ 自動構成スクリプト(pac file)  ↓
    // ```
    var obj_proxySettings = new proxy.pac('<proxyserver.domain>/<pacfile>');
    // ```

    // Create a driver instance
    // https://www.selenium.dev/selenium/docs/api/javascript/module/selenium-webdriver/index_exports_ThenableWebDriver.html
    var obj_webDriver = await new Builder()
        .withCapabilities(

            // https://www.selenium.dev/selenium/docs/api/javascript/module/selenium-webdriver/index_exports_Capabilities.html
            new Capabilities()
                .setBrowserName(str_browserName)
                .setProxy(obj_proxySettings)
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
    
    
    // // <Chrome の Auth dialog を取得しようとトライする例>-------------------------------------------
    // // Ex.1, Ex.2 でそれぞれトライしたけど、取得はできなかった。
    // // 確認環境は以下の通り
    // // - Windows10 (64bit)  
    // // - Node.js v10.16.2
    // // - selenium-webdriver 4.0.0-alpha.7
    // // - Chrome 80.0.3987.163
    // // - ChromeDriver 80.0.3987.106
    // await obj_webDriver
    //     .wait(async () => {

    //         let bl_gotAlert = false;

    //         // Ex.1
    //         // window.alert(), window.confirm(), window.prompt() のいづれかを取得する。
    //         // しかし、Chrome の Auth dialog がこれらに該当するわけではないらしく、
    //         // NoSuchAlertError が Throw される。
    //         await obj_webDriver
    //             .switchTo()
    //             .alert()
    //             .then(function(obj_alert){
    //                 console.log('got alert');

    //             }).catch(function(e){

    //                 if( (typeof e) === 'object' && e.constructor.name === "NoSuchAlertError"){
    //                     console.log('NoSuchAlertError');
        
    //                 }else{
    //                     throw e;
    //                 }

    //             });
    //         ;

    //         // Ex.2
    //         // activeElement を取得する.
    //         // しかし、Chrome の Auth dialog が取得できるわけではなく、
    //         // document.body が取得される。
    //         await obj_webDriver
    //             .switchTo()
    //             .activeElement()
    //             .then(async function(obj_WebElementPromise){

    //                 await obj_WebElementPromise
    //                     .getTagName()
    //                     .then(function(str){
    //                         console.log(str); //<- `body` が出力される

    //                     })
    //                 ;

    //             })
    //         ;

    //         return bl_gotAlert;

    //     },3000)
    //     .catch(function(e){

    //         console.error('<exception caught!>----------------------------');

    //         if( (typeof e) === 'object' && e.constructor.name === "TimeoutError"){
    //             console.log("Cannot get Auth dialog");

    //         }else{
    //             throw e;
    //         }
    //     })
    // ;
    // // -------------------------------------------</Chrome の Auth dialog を取得しようとトライする例>

})();
