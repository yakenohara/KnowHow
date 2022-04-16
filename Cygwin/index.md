## chere

Windows Explorer 上で右クリックしたディレクトリをカレントディレクトリして Cygwin を起動する

### Install

1. Cygwin を 管理者権限で起動する
2. 以下コマンドを実行する
```
chere -i -cm2 -s bash -t mintty -e 'Cygwin Prompt Here'
```
※ `-e` オプションはお好みで。
  キーボードショートカットを設定する場合は、`Cygwin Prompt Here(&W)` のように  
  `&?` でキー名を指定する。

### Uninstall

1. Cygwin を 管理者権限で起動する
2. 以下コマンドを実行する
```
$ chere -u
```
