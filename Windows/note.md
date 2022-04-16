# よく探しがちなディレクトリ

## スタートアップの保存場所

### 場所その1

```
C:\Users\[ユーザー名]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
```

### 場所その2

```
C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup
```

## Explorerの「送る」

```
C:\Users\<username>\AppData\Roaming\Microsoft\Windows\SendTo
```
または、「ファイル名を指定して実行」で`shell:sendto`

# レジストリ関係

## レジストリ ルートキーの関係

http://nonsubject.arinco.org/p/hkcr-hkcu-hklm.html

## 「プログラムから開く」のリストから削除 

http://www5f.biglobe.ne.jp/ayum/sample/fromp.html

## アプリで開くを右クリックに追加するコマンド

https://qiita.com/bugtrap/items/f2096bfb6dbd83b60fb0

## 101英語キーボードの導入

以下を設定後 Windows を再起動  

HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\i8042prt\Parameters  

| KEY                        | 日本語キーボード | USキーボード |
| -------------------------- | ---------------- | ------------ |
| LayerDriver JPN            | kbd106.dll       | kbd101.dll   |
| OverrideKeyBoardIdentifier | PCAT_106KEY      | PCAT_101KEY  |


## インストーラ不要のアプリを削除→似た名前のアプリをインストールすると、右クリックメニューの`ファイルをプログラムから開く`が効かない場合

例えば、Nicoplayer113をアンインストール後、新バージョンのNicoplayer117をインストールしたら、レジストリエディタから、
```
HKEY_CLASSES_ROOT\Applications\NicoPlayer.exe\sell\\open\command
```
内の、"規定"ファイルを
```
"C:\Program Files\nicoplayer113\NicoPlayer.exe" "%1"
```

から、以下のように修正。
```
"C:\Program Files\nicoplayer117\NicoPlayer.exe" "%1"
```
