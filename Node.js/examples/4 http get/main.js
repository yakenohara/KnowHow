const https = require('https');
const fs = require('fs');

// <Setting>---------------------------
var int_msTimeForTimeOut = 10000;
// --------------------------</Setting>

// <example implimentation>-----------------------------------------------------------------------------------

var str_url;

// 200 OK な場合
str_url = 'https://images-assets.nasa.gov/image/PIA15416/PIA15416~orig.jpg';
var str_toSaveFileName = 'orig.jpg';

// URL 文字列が無効な場合
// str_url = 'efjiwef';

// サーバーとの接続確立前に発生したエラー
// str_url = 'https://feiowe.net/';

// 404 Not Found になる
// str_url = 'https://github.com/aaaaaaaaaa/aaaaaaaaaaa/aaaaaaaaa/aaaaaa';


var bool_downloading = false;

var obj_1 = new httpsGet(
    str_url,
    str_toSaveFileName,
    function(obj_result){ // When process end
        bool_downloading = false;
        console.log('');
        console.log('---------------------<RESULT>------------------------')
        console.log(JSON.stringify(obj_result, undefined, 4));
    },
    function(int_stage, str_message){ // When process satage moved

        if(int_stage == 4){ // ダウンロードが完了した時

            // ダウンロード最終状態を standard out する
            var obj_status = obj_1.getStatus();
            process.stdout.write('\r');
            process.stdout.write(func_makeProgressString(obj_status.downloadedByteSize, obj_status.toDownloadByteSize));
            process.stdout.write('\n');
        }

        console.log(`Stage:${int_stage}, ${str_message}`);

        if(int_stage == 3){ // ファイルダウンロードが開始された時

            // 定周期によるダウンロード観測結果表示を開始する
            bool_downloading = true; //ダウンロード中フラグ ON
            func_dlCheck();
        }else{
            bool_downloading = false; //ダウンロード中フラグ OFF
        }
        
    }
    // dlProgressListener は登録しない()
);

// 定周期によるダウンロード状態の観測結果表示
// 定周期でダウンロード状態を観測して、結果を standard out する
var int_msDlCheckFreq = 100;
function func_dlCheck(){
    if(bool_downloading){ // ダウンロード中フラグ ON の場合
        var obj_status = obj_1.getStatus();
        process.stdout.write('\r');
        process.stdout.write(func_makeProgressString(obj_status.downloadedByteSize, obj_status.toDownloadByteSize));
        setTimeout(func_dlCheck, int_msDlCheckFreq);
    }

}

// パーセンテージ, 分子(3桁区切り), 分母(3桁区切り)を文字列化して返す
function func_makeProgressString(numerator, denominator){

    var str_toRet;
    var int_digitsOfFlac = 1; // パーセンテージ表示の内の小数点以下の桁数

    var int_parsedDenominator = parseInt(denominator);
    
    var str_toShowNumerator = numerator.toLocaleString();
    var str_toShowDenominator;

    if(isNaN(int_parsedDenominator)){ // 分母が数値として無効な場合(= When 'content-size' property of http response is invalid)
        str_toShowDenominator = 'Unkown';
        str_toShowPercentage = '???.' + '?'.repeat(int_digitsOfFlac);
        
    }else{ // 分母が数値として有効な場合
        str_toShowDenominator = int_parsedDenominator.toLocaleString();
        str_toShowNumerator = ' '.repeat(str_toShowDenominator.length - str_toShowNumerator.length) + str_toShowNumerator; // space padding
        int_progressPercentage = numerator/int_parsedDenominator * 100;
        str_toShowPercentage = int_progressPercentage.toFixed(int_digitsOfFlac);
        str_toShowPercentage = ' '.repeat((4+int_digitsOfFlac) - str_toShowPercentage.length) + str_toShowPercentage;
    }

    str_toRet = `Progress:${str_toShowPercentage}[%] (${str_toShowNumerator}[bytes]/${str_toShowDenominator}[bytes])`;

    return str_toRet;
}

// ----------------------------------------------------------------------------------</example implimentation>

//
//  Access to the specified URL and save as file
//
//  Parameters
//  ----------
//  url : String
//      URL to download
//  fileName : String
//      Filepath to save file
//  resultListener : function
//      Callback function that will be fired with 1 argument(see following) when process is ended.  
//      Note. This will be fired whether process ends in scceeded or not.
//          1st Argment : Object
//              Each property means following
//                  isOK : boolean
//                      true if all process ends in scceeded, otherwise false
//                  message : String
//                      Overview of all processes
//                  lastStageNumber : Number
//                      Which process number reached in the download processes that is divided into the following 4 processes
//                          1: 'Wait for http response'
//                          2: 'Got http response'
//                          3: 'Wait for downloading complete
//                          4: 'Completed'
//                  lastStageMessage : Number
//                      Meaning of lastStageNumber above
//                  incomingMsg : Object
//                      Note. This property will be added only if there is responce from the server
//                      Following property of the http response
//                          statusCode : Number
//                              Status code of the http response. Same as message.statusCode of http.IncomingMessage class. To know details, See following.
//                              https://nodejs.org/api/http.html#http_message_statuscode
//                          statusMessage : String
//                              Status message of the http response. Same as message.statusMessage of http.IncomingMessage class. To know details, See following.
//                              https://nodejs.org/api/http.html#http_message_statusmessage
//                          headers : Object
//                              Response header of the http response. Same as message.headers of http.IncomingMessage class. To know details, See following.
//                              https://nodejs.org/api/http.html#http_message_headers
//                          complete
//                              True if download successfully ended otherwise false. Same as message.complete of http.IncomingMessage class. To know details, See following.
//                              https://nodejs.org/api/http.html#http_message_complete
//                  toDownloadByteSize : Number
//                      Note. This property will be added only if there is a valid 'content-size' property in the http response from the server
//                      Total byte size of content.
//                  downloadedByteSize : Number
//                      Note. This property will be added only if downloading process is started
//                      How many bytes downloaded when process ended
//  stageListener : function
//      Callback function that will be fired with 2 argument(see following) when process stage is moved.  
//          1st Argument : Number
//              Which process number reached in the download processes that is divided into the following 4 processes
//                  1: 'Wait for http response'
//                  2: 'Got http response'
//                  3: 'Wait for downloading complete
//                  4: 'Completed'
//          2nd Argument : Number
//              Meaning of 1st argument above
//  dlProgressListener : function
//      Callback function that will be fired with 2 argument(see following) when every 'data' event of download stream.
//          1st Argument : Number
//              Total amount byte size of downloaded completely
//          2nd Argument : Number
//              Content byte size of file
//              Note. This argument will be specified only if there is a valid 'content-size' property in the http response from the server
// 
function httpsGet(url, fileName, resultListener, stageListener, dlProgressListener){

    var int_stage = 0;
    var obj_stageDef = {
        '0': 'Generate http request',
        '1': 'Wait for http response',
        '2': 'Got http response',
        '3': 'Wait for downloading complete',
        '4': 'Completed'
    }

    var bool_haveDone = false;
    var str_reportedMessage;

    var obj_res;
    var int_toDownloadByteSize;
    var int_downloadedByteSize;

    this.getStatus = function(){

        var str_msg = bool_haveDone ? str_reportedMessage : 'Now in progress' ;

        return func_reportStatus(undefined, str_msg, obj_res);
    }

    try{

        // 
        // http.get(url[, options][, callback])  
        // https://nodejs.org/api/http.html#http_http_get_url_options_callback
        // 
        var req = https.get(url, function(obj_incomingMsg){
            // 
            // argument `obj_incomingMsg` is an instance of http.IncomingMessage  
            // https://nodejs.org/api/http.html#http_class_http_incomingmessage
            //
    
            obj_res = {
                'statusCode':obj_incomingMsg.statusCode,
                'statusMessage':obj_incomingMsg.statusMessage,
                'headers':obj_incomingMsg.headers,
                'complete':obj_incomingMsg.complete
            };
    
            // 1: Wait for http response
            //  | | | |
            //  v v v v
            // 2: Got http response
            func_nextStage(); // Goto next stage
            
            if (obj_incomingMsg.statusCode !== 200) {
                //
                // pattern.3 with IncomingMessage
                // HTTP response status code が 200(OK) ではない場合はここにくる
                //
    
                //
                // http.get(url[, options][, callback]) して生成される http.ClientRequest class のドキュメントで、
                // `the data from the response object must be consumed` とのことなので、
                // HTTP response status code が 200(OK) ではない場合は、 `.resume()` して終了する  
                // https://nodejs.org/api/http.html#http_class_http_clientrequest
                //
                obj_incomingMsg.on('end', function(){
                    func_reportResult( // 失敗として終了
                        false,
                        'Bad response. Cannot start downloading.',
                        obj_res)
                    ;
                });
                obj_incomingMsg.resume(); // Consume response data to free up memory
                return;
            }
    
            var obj_writeStream = fs.createWriteStream(fileName);
            obj_incomingMsg.pipe(obj_writeStream);
            
            var int_parsedToDownloadByteSize = parseInt(obj_incomingMsg.headers['content-length']);

            // incomingMsg.headers['content-length'] が整数値として無効な場合は undefined のままとする
            // incl. incomingMsg.headers['content-length'] が存在しない場合
            if(!isNaN(int_parsedToDownloadByteSize)){
                int_toDownloadByteSize = int_parsedToDownloadByteSize;
            }

            int_downloadedByteSize = 0;
            obj_incomingMsg.on('data',function(chunk){
                int_downloadedByteSize += chunk.length;

                if(typeof dlProgressListener == 'function'){
                    dlProgressListener(int_downloadedByteSize, int_toDownloadByteSize);
                }
                
            });
            obj_incomingMsg.on('end', function(){
                
                obj_writeStream.close();
                
                obj_res['complete'] = obj_incomingMsg.complete;
                
                if(!obj_incomingMsg.complete){ // 中断された場合
                    // pattern.4 with IncomingMessage
                    func_reportResult( // 失敗として終了
                        false,
                        'The connection was terminated while the message was still being sent',
                        obj_res)
                    ;
                }else{ //中断されなかった場合

                    // pattern.5 with IncomingMessage

                    // 3: Wait for downloading complete
                    //  | | | |
                    //  v v v v
                    // 4: Completed
                    func_nextStage(); // Goto next stage

                    func_reportResult( // 成功として終了
                        true,
                        'OK',
                        obj_res)
                    ;
                }
            });

            // 2: Got http response
            //  | | | |
            //  v v v v
            // 3: Wait for downloading complete
            func_nextStage(); // Goto next stage
            
        });
    
        req.setTimeout(int_msTimeForTimeOut, function(){
            // 
            // pattern.4 with IncomingMessage
            // Download 中に接続がタイムアウトした場合はここにくる
            // ただし、サーバーとの接続要求でタイムアウトが発生した場合は、
            // `req.on('error', function(e){` がコールされ、
            // この callback はコールされない(note: 設定したタイムアウト用待ち時間は発生する)
            // e.g.
            //  - Download 中のサーバダウン
            //  - Download 中の LAN cable / Wi-Fi 切断
            // 
    
            req.abort(); // Goto -> `obj_incomingMsg.on('end', function(){`
        });
    
        req.on('error', function(e){
            //
            // pattern.2 no IncomingMessage
            // サーバーとの接続確立前に発生したエラーはここにくる
            // e.g. 
            //  - DNS エラー
            //  - http response 取得前に req.abort() or req.destroy() がたたかれた
            //  - https.get した時点でネットワーク接続がない( LAN cable / Wi-Fi 切断等)
            //
            func_reportResult(false, String(e)); // 失敗として終了
            return;
        });
    
    }catch(e){
        //
        // pattern.1 no IncomingMessage
        // URL 文字列が無効な場合に発生したエラーはここにくる
        // e.g.
        //  - URL が `https://` (note: not `http://`) で始まらない  
        //
        func_reportResult(false, String(e)); // 失敗として終了
        return;
    }

    // 0: Generate http request
    //  | | | |
    //  v v v v
    // 1: Wait for http response
    func_nextStage(); // Goto next stage

    function func_nextStage(){
        int_stage++;

        if(typeof stageListener == 'function'){
            stageListener(int_stage, obj_stageDef[int_stage]);
        }
    }

    function func_reportStatus(bool_isOK, str_message, obj_incomingMsg){
        var obj_result = {};

        obj_result['haveDone'] = bool_haveDone;
        if(typeof bool_isOK != 'undefined'){
            obj_result['isOK'] = bool_isOK;
        }
        obj_result['message'] = str_message;
        obj_result['url'] = url;
        obj_result['fileName'] = fileName;
        obj_result['lastStageNumber'] = int_stage;
        obj_result['lastStageMessage'] = obj_stageDef[int_stage];

        if(typeof obj_incomingMsg == 'object'){
            obj_result['incomingMsg'] = {...obj_incomingMsg};
        }
        if(typeof int_toDownloadByteSize == 'number'){
            obj_result['toDownloadByteSize'] = int_toDownloadByteSize;
        }
        if(typeof int_downloadedByteSize == 'number'){
            obj_result['downloadedByteSize'] = int_downloadedByteSize;
        }

        return obj_result;
    }

    function func_reportResult(bool_isOK, str_message, obj_incomingMsg){

        bool_haveDone = true;
        str_reportedMessage = str_message;
        var obj_result = func_reportStatus(bool_isOK, str_message, obj_incomingMsg);

        if(typeof resultListener == 'function'){ 
            resultListener(obj_result);
        }
    }
}
