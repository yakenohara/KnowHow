# Django から Postgresql にアクセスする

## Install psycopg2

作成した仮想環境で `pip install psycopg2-binary==2.8.6` する。(2.9.x 系だと `python manage.py migrate` で失敗するので注意。`2.8.6` をインストールする。)  

```
***-no-MacBook-Pro:bin ***$ source ~/pyvenv/bin/activate
(pyvenv) ***-no-MacBook-Pro:bin ***$ pip install psycopg2-binary==2.8.6
Collecting psycopg2-binary==2.8.6
  Downloading psycopg2_binary-2.8.6-cp37-cp37m-macosx_10_6_intel.macosx_10_9_intel.macosx_10_9_x86_64.macosx_10_10_intel.macosx_10_10_x86_64.whl (1.5 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.5/1.5 MB 1.6 MB/s eta 0:00:00
Installing collected packages: psycopg2-binary
Successfully installed psycopg2-binary-2.8.6
(pyvenv) ***-no-MacBook-Pro:bin ***$ deactivate
***-no-MacBook-Pro:bin ***$ 
```

## PostgreSQL DB の作成

`command` + `space` で `SQL Shell` と入力して SQL Shell (psql).app を起動  

```
Last login: Sun Mar 20 14:45:11 on ttys003
/Library/PostgreSQL/14/scripts/runpsql.sh; exit

The default interactive shell is now zsh.
To update your account to use zsh, please run `chsh -s /bin/zsh`.
For more details, please visit https://support.apple.com/kb/HT208050.
***noMBP:~ ***$ /Library/PostgreSQL/14/scripts/runpsql.sh; exit
Server [localhost]: 
Database [postgres]: 
Port [5432]: 
Username [postgres]: 
Password for user postgres: # <- PostgreSQL インストール時に設定したパスワード
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

postgres=# CREATE DATABASE my_django_db;
CREATE DATABASE
postgres=# CREATE USER my_django_user WITH PASSWORD 'my_django_pass';
CREATE ROLE
postgres=# ALTER ROLE my_django_user SET client_encoding TO 'utf8';
ALTER ROLE
postgres=# ALTER ROLE my_django_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE
postgres=# ALTER ROLE my_django_user SET timezone TO 'UTC';
ALTER ROLE
postgres=# GRANT ALL PRIVILEGES ON DATABASE my_django_db TO my_django_user;
GRANT
postgres=# \l
                                  List of databases
     Name     |  Owner   | Encoding  | Collate | Ctype |      Access privileges      
--------------+----------+-----------+---------+-------+-----------------------------
 my_django_db | postgres | SQL_ASCII | C       | C     | =Tc/postgres               +
              |          |           |         |       | postgres=CTc/postgres      +
              |          |           |         |       | my_django_user=CTc/postgres
 postgres     | postgres | SQL_ASCII | C       | C     | 
 template0    | postgres | SQL_ASCII | C       | C     | =c/postgres                +
              |          |           |         |       | postgres=CTc/postgres
 template1    | postgres | SQL_ASCII | C       | C     | =c/postgres                +
              |          |           |         |       | postgres=CTc/postgres
(4 rows)

postgres=# \q
logout
Saving session...
...copying shared history...
...saving history...truncating history files...
...completed.
```

## settings.py の編集

 - 変更前  
```
# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
 - 変更後  
```
# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'my_django_db', #  SQL Shell で `CREATE DATABASE ***;` で設定した DB 名
        'USER': 'my_django_user', # SQL Shell で `CREATE USER ***` で設定したユーザー名を指定
        'PASSWORD': 'my_django_pass', # SQL Shell で `CREATE USER ***  WITH PASSWORD '***';` で設定したパスワード
        'HOST': '',
        'PORT': '',
    }
}
```