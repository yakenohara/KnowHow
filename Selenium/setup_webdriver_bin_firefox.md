# Install Driver for Firefox

[Mozilla の公式ドキュメント](https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Cross_browser_testing/Your_own_automation_environment) の以下を実施する。

```
1. Download the latest GeckoDriver (for Firefox) and ChromeDriver drivers.
2. Unpack them into somewhere fairly easy to navigate to, like the root of your home user directory.
3. Add the chromedriver and geckodriver driver's location to your system PATH variable. This should be an absolute path from the root of your hard disk, to the directory containing the drivers. 例えば、if we were using a Mac OS X machine, our user name was bob, and we put our drivers in the root of our home folder, the path would be /Users/bob.
```
## 1. Download the latest GeckoDriver~, 2. Unpack them ~

[ここ](https://github.com/mozilla/geckodriver/releases)から Driver をダウンロードする。  

※note  
 - Firefox が 32bit なのか 64bit なのかを確認するには、Firefox の `ヘルプ` -> `Firefox について` を開いて確認する。
 - Firefox だけを動作させたいなら、`ChromeDriver` のインストールは不要。  
  理由はわからない。インストールしなくても、Firefox 起動させられる事を確認した。

## 3. Add the chromedriver driver's location to your system PATH variable.

ダウンロードした実行ファイルをパスが通ったディレクトリに配置する。
