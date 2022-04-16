
// 
// note
// clipboard へアクセスする為に、内部的に clipboardData API を使っている
// この API は IE とそれ以外で実装が異なる
//  - IE11以外の場合
//     W3Cの仕様通り -> https://www.w3.org/TR/clipboard-apis/
//  - IE11の場合
//      独自タスク内でアクセス可能で、読み込み方法は以下の通り。
//      第1引数は 'text' 以外は指定不可。
//        - read
//           `str = window.clipboardData.getData('text');`
//        - write
//           `window.clipboardData.setData('text', "any string");`
//
var browserIsIE11 = (navigator.userAgent.toLowerCase().indexOf('trident/7') > -1);
var clipboardEvent = null;
var mousetrapInstance = null;

if(browserIsIE11){ // IE11の場合

    mousetrapInstance = new Mousetrap();

    //
    //note
    // IE11 の場合は、
    // `document.addEventListener('cut', function(e){ ~` で evet を拾おうとしても、拾えない事がある。
    // (少なくとも、`contenteditable="false"` な `div` 要素をクリック後に
    // `ctrl+x` or `ctrl+v` しても、 cut/paste event は拾えなかった。)
    // その為、IE11用の実装としては、
    // `mousetrapInstance.bind("ctrl+x", function(e, combo){ ~ ` のように実装した
    // 独自event 内で clipboard control を行い、
    // Browser の Clipboard event タスク内では `event.returnValue = false;` する
    // 

    document.addEventListener('cut', function(e){
        console.log("browser cut event");
        disablingKeyEvent(e);
    });
    mousetrapInstance.bindGlobal("ctrl+x", function(e, combo){
        console.log("Mousetrap cut event");
        cutEventProcess();
        disablingKeyEvent(e);
    });

    document.addEventListener('copy', function(e){
        console.log("browser copy event");
        disablingKeyEvent(e);
    });
    mousetrapInstance.bindGlobal("ctrl+c", function(e, combo){
        console.log("Mousetrap copy event");
        copyEventProcess();
        disablingKeyEvent(e);
    });

    document.addEventListener('paste', function(e){
        console.log("browser paste event");
        disablingKeyEvent(e);
    });
    mousetrapInstance.bindGlobal("ctrl+v", function(e, combo){
        console.log("Mousetrap paste event");
        pasteEventProcess();
        disablingKeyEvent(e);
    });
    
}else{ // IE11でない場合

    //
    //note
    // IE11以外の Browser では、W3Cの仕様通り、
    // Browser の Clipboard event を Overrideする方法(具体的には、
    // `document.addEventListener('copy', function(e){ ~ ` のように実装した event タスク内)
    // でないと clipboardData API を使って Clipboard にアクセスできない。
    // その為、 `mousetrapInstance.bind("alt+c", function(e, combo){ ~ ` のように実装した
    // 独自の key bind によって Clipboard を control することは不可能。
    // Clipboard control は Browser の Clipboard event を Override する。

    document.addEventListener('cut', function(e){
        console.log("browser cut event");
        
        clipboardEvent = e;
        cutEventProcess();
        disablingKeyEvent(e);
    });

    document.addEventListener('copy', function(e){
        console.log("browser copy event");

        clipboardEvent = e;
        copyEventProcess();
        disablingKeyEvent(e);
    });

    document.addEventListener('paste', function(e){
        console.log("browser paste event");

        clipboardEvent = e;
        pasteEventProcess();
        disablingKeyEvent(e);
    });

}

function cutEventProcess(){

    var txtCntnt = 'cut event overrided';

    copyStrToClipboard(txtCntnt);
}

function copyEventProcess(){

    var txtCntnt = 'copy event overrided';

    copyStrToClipboard(txtCntnt);
}

function pasteEventProcess(){
    
    var txtCntnt = getStrFromClipboard();

    console.log('text content:`' + txtCntnt + '`');
}

// 文字列を clipboard に格納する
function copyStrToClipboard(str){
    
    try{
        window.clipboardData.setData('text', str); //ie11 の場合
    
    }catch(e){
        clipboardEvent.clipboardData.setData('text/plain', str); //ie11 以外の場合
    }
    
}

// clipboard から文字列を取得する
function getStrFromClipboard(){
    var str = "";
    
    try{
        str = window.clipboardData.getData('text'); //ie11 の場合
    
    }catch(e){
        str = clipboardEvent.clipboardData.getData('text/plain');　//ie11 以外の場合
    }
    
    return str;
}

// preventDefault する
function disablingKeyEvent(e){
    if (e.preventDefault) {
        e.preventDefault();
    
    } else { //ブラウザによって `.preventDefault` が用意されていない場合
        e.returnValue = false;
    }
}
    