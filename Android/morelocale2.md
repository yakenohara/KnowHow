## adb コマンドの実行

端末を USB デバッグ接続して、`adb shell pm grant jp.co.c_lis.ccl.morelocale android.permission.CHANGE_CONFIGURATION` をコマンドプロンプトで実行する。
以下の様に、コマンドに対する返事が何もない状態が、成功状態。  

```
>adb shell pm grant jp.co.c_lis.ccl.morelocale android.permission.CHANGE_CONFIGURATION

>
```

`<NOTE>`  

もし以下の様にダイアログが出てきたら、失敗している。環境変数を正しく設定できていないときや、端末のデバッグ接続が失敗している場合にこの様になるらしい。 USB を挿し直したり、端末を再起動したり、同じコマンドを何度か繰り返し実行すると、成功する。

```
>adb shell pm grant jp.co.c_lis.ccl.morelocale android.permission.CHANGE_CONFIGURATION
adb server version (39) doesn't match this client (41); killing...
* daemon started successfully

>adb shell pm grant jp.co.c_lis.ccl.morelocale android.permission.CHANGE_CONFIGURATION
* daemon not running; starting now at tcp:5037
* daemon started successfully
adb.exe: device unauthorized.
This adb server's $ADB_VENDOR_KEYS is not set
Try 'adb kill-server' if that seems wrong.
Otherwise check for a confirmation dialog on your device.

```

`</NOTE>`  

## MoreLocale 2 の設定

端末側で MoreLocale 2 インストール・起動して、`Custom Locale` を選択。
以下のように設定して `SET`

Language:`ja`  
Country:`JP`  
Variant:`` <- 空欄のままでいい。

表示言語が日本語になったはずだ。  
