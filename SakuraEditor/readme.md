# .ini の場所

`sakura.exe` を同じディレクトリに `sakura.exe.ini` があるので、そのファイル内で定義する。  
下記は通常インストール時の設定。  
`C:\Users\(ユーザー名)\AppData\Roaming\sakura` 配下に `sakura.ini` が配置される。

```
;	○設定例
;		設定ファイル（sakura.ini）をドキュメントフォルダ下のsakura_settingsサブフォルダに置く
;			MultiUser=1
;			UserRootFolder=2
;			UserSubFolder=sakura_settings
;		⇒ ex. C:\Documents and Settings\<username>\My Documents\sakura_settings\sakura.ini
UserSubFolder=sakura
```

# 設定

## grep結果をリアルタイム表示

設定(O)→共通設定(C)→検索タブ→Grep リアルタイムで表示する(R)にチェックを入れます。

## grep結果をダブルクリックでジャンプしない

設定(O)→共通設定(C)→検索タブ→ダブルクリックでタグジャンプのチェックを外します。

# マクロ

## ファイルの再読み込みを行いたい場合

以下マクロを登録・実行する  

[SakuraKeyMacro-ReFresh](https://github.com/yakenohara/SakuraKeyMacro-ReFresh)  
