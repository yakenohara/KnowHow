# Install

PostgreSQL Database Download  
https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

![](assets/images/mac-install-01.svg)  
![](assets/images/mac-install-02.svg)  
![](assets/images/2022-03-19-19.49.00.png)  
![](assets/images/2022-03-19-19.50.15.png)  
![](assets/images/2022-03-19-19.50.52.png)  
![](assets/images/2022-03-19-19.51.29.png)  

スーパーユーザ postgres のパスワードを指定します。パスワードは確認のため、同じものを 2 回入力します。データベースへの接続時に必要になるので、忘れないように注意してください。  

![](assets/images/2022-03-19-19.52.15.png)  
![](assets/images/2022-03-19-19.52.51.png)  

デフォルトのロケールを選択します。ロケールは言語や国によって異なる文字の扱いや並び替え順を指定するものです。デフォルトの [Default locale] では OS の設定に基づくロケール、日本語の環境であれば Japanese_Japan.932 が選択されます。日本語ではロケールを使う必要があまりなく、ロケールを使うと文字の処理が遅くなり、インデックスの作成時にオプションを指定しないと、LIKE でインデックスも使えなくなるので、ロケールを使わないことを示す C を選択しておきましょう。  

![](assets/images/2022-03-19-19.53.36.png)  
![](assets/images/2022-03-19-19.54.02.png)  
![](assets/images/2022-03-19-19.54.31.png)  
![](assets/images/2022-03-19-19.54.58.png)  
![](assets/images/2022-03-19-19.56.07.png)  ´

# PostgreSQL サービスの起動と停止

`command` + `space` で `pgAdmin` と入力して pgAdmin 4.app を起動。  

![](assets/images/2022-03-19-20-12-38.png)  

インストール時に設定したパスワードを入力してログインします。  

![](assets/images/2022-03-19-20.15.28.png)  

PATHの設定をします。  
`~/.bash_profile` と `~/.zprofile` ファイルにパスを追加します。

```
***-no-MacBook-Pro:bin ***$ echo 'export PATH=$PATH:/Library/PostgreSQL/14/bin' >> ~/.bash_profile # <- インストール時に設定したディレクトリに一致させるように注意
***-no-MacBook-Pro:bin ***$ cat ~/.bash_profile
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
export PATH=$PATH:"/Applications/Selenium Driver"
eval "$(pyenv init -)"

# Setting PATH for Python 3.10
# The original version is saved in .bash_profile.pysave
PATH="/Library/Frameworks/Python.framework/Versions/3.10/bin:${PATH}"
export PATH
export PATH=$PATH:/Library/PostgreSQL/14/bin # <- パスが追加された
***-no-MacBook-Pro:bin ***$ echo 'export PATH=$PATH:/Library/PostgreSQL/14/bin' >> ~/.zprofile # <- インストール時に設定したディレクトリに一致させるように注意
***-no-MacBook-Pro:bin ***$ cat ~/.zprofile
export PATH=$PATH:/Library/PostgreSQL/14/bin # <- パスが追加された
***-no-MacBook-Pro:bin ***$ 
```

ターミナルを一度終了して再起動します。

バージョン確認をします。
postgres --version

```
***noMBP:~ ***$ postgres --version
postgres (PostgreSQL) 14.2
***noMBP:~ ***$ 
```

`command` + `space` で `SQL Shell` と入力して SQL Shell (psql).app を起動  
接続先のホスト名 Server、データベース名 Database、ポート番号 Port、ユーザ名 Username、クライアント側のエンコーディング Client Encoding、パスワードの入力を求めるプロンプトが順番に表示されます。角カッコ内がデフォルト値を表している。  
Server, Database, Port Username はデフォルト値のまま何も入力せず、Enter キーを押す。  
psql を終了するには `\q` を入力した後に何かキーを押す。  

```
Last login: Sun Mar 20 14:41:34 on ttys004
/Library/PostgreSQL/14/scripts/runpsql.sh; exit

The default interactive shell is now zsh.
To update your account to use zsh, please run `chsh -s /bin/zsh`.
For more details, please visit https://support.apple.com/kb/HT208050.
***noMBP:~ ***$ /Library/PostgreSQL/14/scripts/runpsql.sh; exit
Server [localhost]: 
Database [postgres]: 
Port [5432]: 
Username [postgres]: 
Password for user postgres: 
psql (14.2)
Type "help" for help.

postgres=# \l
                             List of databases
   Name    |  Owner   | Encoding  | Collate | Ctype |   Access privileges   
-----------+----------+-----------+---------+-------+-----------------------
 postgres  | postgres | SQL_ASCII | C       | C     | 
 template0 | postgres | SQL_ASCII | C       | C     | =c/postgres          +
           |          |           |         |       | postgres=CTc/postgres
 template1 | postgres | SQL_ASCII | C       | C     | =c/postgres          +
           |          |           |         |       | postgres=CTc/postgres
(3 rows)

postgres=# \q
logout
Saving session...
...copying shared history...
...saving history...truncating history files...
...completed.

[プロセスが完了しました]
```
