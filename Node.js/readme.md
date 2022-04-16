# install

インストーラーをたたくだけ  
[https://nodejs.org/ja/download/](https://nodejs.org/ja/download/)  

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

# Commands

## nodes.js のバージョン確認
```
node --version
```

## Package (Module) をインストール  
```
npm install <packeage name>
```

※Package と Module の違いは以下参照  
npm とは何か / Package と module の違い – １日ひとつ、強くなる。  
[http://better-than-i-was-yesterday.com/what-is-npm/](http://better-than-i-was-yesterday.com/what-is-npm/)  

ローカルからインストールする場合は、対象 Package (Module) の `package.json` が配置されたディレクトリを指定すればいい。

↓ 添付の `install-from-local\removeNPMAbsolutePaths-2.0.0.zip` を `C:\` 直下に解凍したものを install する例 ↓  
```
npm install C:\removeNPMAbsolutePaths-2.0.0
```

project の 定義ファイル package.json があって、
この中(このファイルはテキストファイル。エディタで開ける。)にパッケージ依存関係が定義してある場合は、以下だけでいい
```
npm install
```

あとは パッケージを使いたくなったときに、`require()` すればいい

## Release Project with `node_modules`

`node_modules` 配下も含めて、 PJ をまるごと別 PC にもってくれば、 `npm install` せずに実行できる。  
*** ただし、 *** `node_modules` の各 Package (Module) 配下の package.json 内には、`npm install` した時の PC 内のインストールパス(絶対パス)が "_where" プロパティとして記録されている。  
絶対パスなので、ユーザー名など個人情報が含まれる可能性があるので、消しておくのが無難。(消しても動作に影響はない)  
これを消してくれるのが [`removeNPMAbsolutePaths`](https://www.npmjs.com/package/removeNPMAbsolutePaths) という Package (Module) 。  
`npm install -g removeNPMAbsolutePaths` して使えるようにしておくといい。  
添付の `install-from-local\removeNPMAbsolutePaths-2.0.0.zip` からインストールしてもいい。  


## npm init

パッケージ依存関係を定義しておきたいときは `npm init` で package.json を作成しておいたほうがいい。  
以下ページがわかりやすい  

https://blog.katsubemakito.net/nodejs/publish_npm_package_for_beginners  


## Install した package の一覧

```
npm ls
```

# Examples

## hello world

以下内容のJavaScriptファイル `hello.js` を作成  

```
console.log("hello world");
```

コマンドプロンプトで `node hello.js` で実行

```
node hello.js
hello world
```

## パッケージの追加(`npm install`)と読み込み(`require()`)

esprima(JavaScriptソースコードのパーサー) を使用した例

```
npm install esprima
```
