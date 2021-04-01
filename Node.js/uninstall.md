# Uninstall

1. アンインストーラーをたたく。  

2. アンインストーラーで削除しきれないディレクトリ & ファイルを削除する。  
   ここらへんは環境により変わるかもしれない。  
   筆者の環境では、以下が残っていたので、手作業で消した。  

```
//directories
C:\Users\<USERNAME>\AppData\Roaming\npm
C:\Users\<USERNAME>\AppData\Roaming\npm-cache
C:\Users\<USERNAME>\node_modules
C:\Program Files\nodejs

//files
C:\Users\<USERNAME>\.node_repl_history
C:\Users\<USERNAME>\.npmrc //<- もしかしたら、ここかもしれない C:\Users\<USERNAME>\AppData\Roaming\npm\etc\npmrc
C:\Users\<USERNAME>\package-lock.json
```
