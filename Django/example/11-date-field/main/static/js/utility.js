const dict_utilities = {

    //
    // document.cookie から指定文字列の値を検索して返す
    // 存在しない場合は、null を返す
    // https://docs.djangoproject.com/en/4.0/ref/csrf/#acquiring-the-token-if-csrf-use-sessions-and-csrf-cookie-httponly-are-false
    //
    getValueFromCookie : function(str_name){

        var str_cookie = null;

        if (document.cookie && document.cookie != '') { // cookie が存在する場合
          
            var str_semicolonSplittedCookies = document.cookie.split(';');

          // Cookie の検索ループ
          for (var i = 0; i < str_semicolonSplittedCookies.length; i++) {

            // 前後の空白スペースを削除
            var str_subject = str_semicolonSplittedCookies[i].trim();

            // `<指定文字列>=` で始まる場合
            if (str_subject.substring(0, str_name.length + 1) === (str_name + '=')) {

                // `=` 以降を cookie と解釈
                str_cookie = decodeURIComponent(str_subject.substring(str_name.length + 1));
                break;
            }
          }
        }
        return str_cookie;
    },
}
