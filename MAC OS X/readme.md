# キーボードショットカット

| Windows                                                 | Mac OS X                                                                          |
| ------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Ctrl + C                                                | `command` + `c`                                                                   |
| Ctrl + V                                                | `command` + `v`                                                                   |
| Ctrl + Z                                                | `command` + `z`                                                                   |
| Ctrl + Y                                                | `command` + `shift` + `z`                                                         |
| Ctrl + A                                                | `command` + `a`                                                                   |
| Ctrl + S                                                | `command` + `s`                                                                   |
| Ctrl + Shift + F                                        | `command` + `shift` + `f`                                                         |
| Ctrl + Shift + E                                        | `command` + `shift` + `e`                                                         |
| Backspace                                               | `delete`                                                                          |
| Del                                                     | `fn` + `delete`                                                                   |
| Home                                                    | (`fn` + `←`) or (`command` + `←`)                                                 |
| End                                                     | (`fn` + `→`) or (`command` + `→`)                                                 |
| Ctrl + Home                                             | `command` + `↑`                                                                   |
| Ctrl + End                                              | `command` + `↓`                                                                   |
| Ctrl + `←`                                              | `option` + `←`                                                                    |
| Ctrl + `→`                                              | `option` + `→`                                                                    |
| PageUp                                                  | `fn` + `↑`                                                                        |
| PageDown                                                | `fn` + `↓`                                                                        |
| Ctrl + PageUp                                           | `option` + `command` + `←`                                                        |
| Ctrl + PageDown                                         | `option` + `command` + `→`                                                        |
| Ctrl + MouseWheelUp                                     | `command` + `+`                                                                   |
| Ctrl + MouseWheelDown                                   | `command` + `-`                                                                   |
| Alt + Tab                                               | `command` + `tab` (アプリ間切り替えのみ。ウィンドウの切り替えは `command` + `F1`) |
| Win + D                                                 | F11                                                                               |
| Win + `↓`                                               | `command` + `h`                                                                   |
| Win + Home                                              | `option` + `command` + `h`                                                        |
| F12                                                     | `control` + `command` + `f`                                                       |
| Win + PrintScreen (ピクチャに保存される)                | `command` + `shift` + `3` (デスクトップに保存される)                              |
| Win + Alt + PrintScreen (ビデオ\キャプチャに保存される) | `command` + `shift` + `4` + `space` → `return` (デスクトップに保存される)         |
| Win + Shift + F (クリップボードに保存される)            | `command` + `shift` + `4` (デスクトップに保存される)                              |
| Ctrl + Shift + ESC                                      | `option` + `command` + `esc`                                                      |

## Finder

| Action                                     | Windows                                                    | Mac OS X                                                                         |
| ------------------------------------------ | ---------------------------------------------------------- | -------------------------------------------------------------------------------- |
| リネーム                                   | F2                                                         | `Enter`                                                                          |
| 選択したディレクトリを開く                 | (ダブルクリック) or (Enter)                                | (ダブルクリック) or (`command` + `↓`)                                            |
| 選択したディレクトリの親ディレクトリへ移動 | Alt + `↑`                                                  | `command` + `↑`                                                                  |
| 指定したディレクトリに移動                 | Ctrl + L                                                   | `command` + `shift` + `g`                                                        |
| ファイル/ディレクトリのパス取得            | ファイルを選択して Shit + 右クリック → `パスのコピー(A)`   | ファイルを選択して右クリック → `情報を見る` → `場所:` に表示される文字列をコピー |
| 隠しファイルの表示/非表示             I    | フォルダーオプションでファイルとフォルダーの表示設定を変更 | `command` + `shift` + `.`                                                        |

## バーチャルデスクトップ

| Action                     | Windows          | Mac OS X                                 |
| -------------------------- | ---------------- | ---------------------------------------- |
| 1 つ右のデスクトップに移動 | Win + Ctrl + `→` | (3 本指で左にスワイプ) or (`ctrl` + `→`) |
| 1 つ左のデスクトップに移動 | Win + Ctrl + `←` | (3 本指で右にスワイプ) or (`ctrl` + `←`) |

## Terminal

| Action                                         | Command |
| ---------------------------------------------- | ------- |
| ホームディレクトリ ( `/Users/***` ) に移動する | `cd ~`  |

## VS Code

| Windows          | Mac OS X                    |
| ---------------- | --------------------------- |
| Ctrl + F         | `command` + `f`             |
| Ctrl + H         | `option` + `command`  + `f` |
| Ctrl + Shift + E | `command` + `shift` + `e`   |
| Ctrl + Shift + F | `command` + `shift` + `f`   |
| Ctrl + Alt + `↑` | `command` + `option` + `↑`  |
| Ctrl + Alt + `↓` | `command` + `option` + `↓`  |

# 設定

mail.app -> `メール` -> `環境設定` -> `一般` タブ -> `デフォルトメールソフト` -> firefox

# HomeBrew

## Install

[https://brew.sh/index_ja](https://brew.sh/index_ja) にアクセスして "インストール" の項目にあるように、以下コマンドをコピー  

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

コピーしたコマンドを terminal で実行する

```terminal
***@***noMBP ~ % /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
==> Checking for `sudo` access (which may request your password)...
Password:
==> This script will install:
/usr/local/bin/brew
/usr/local/share/doc/homebrew
/usr/local/share/man/man1/brew.1
/usr/local/share/zsh/site-functions/_brew
/usr/local/etc/bash_completion.d/brew
/usr/local/Homebrew
==> The following existing directories will be made group writable:
/usr/local/bin
==> The following existing directories will have their owner set to ***:
/usr/local/bin
==> The following existing directories will have their group set to admin:
/usr/local/bin
==> The following new directories will be created:
/usr/local/etc
/usr/local/include
/usr/local/lib
/usr/local/sbin
/usr/local/share
/usr/local/var
/usr/local/opt
/usr/local/share/zsh
/usr/local/share/zsh/site-functions
/usr/local/var/homebrew
/usr/local/var/homebrew/linked
/usr/local/Cellar
/usr/local/Caskroom
/usr/local/Frameworks
==> The Xcode Command Line Tools will be installed.

Press RETURN/ENTER to continue or any other key to abort:
==> /usr/bin/sudo /bin/chmod u+rwx /usr/local/bin
==> /usr/bin/sudo /bin/chmod g+rwx /usr/local/bin
==> /usr/bin/sudo /usr/sbin/chown *** /usr/local/bin
==> /usr/bin/sudo /usr/bin/chgrp admin /usr/local/bin
==> /usr/bin/sudo /bin/mkdir -p /usr/local/etc /usr/local/include /usr/local/lib /usr/local/sbin /usr/local/share /usr/local/var /usr/local/opt /usr/local/share/zsh /usr/local/share/zsh/site-functions /usr/local/var/homebrew /usr/local/var/homebrew/linked /usr/local/Cellar /usr/local/Caskroom /usr/local/Frameworks
==> /usr/bin/sudo /bin/chmod ug=rwx /usr/local/etc /usr/local/include /usr/local/lib /usr/local/sbin /usr/local/share /usr/local/var /usr/local/opt /usr/local/share/zsh /usr/local/share/zsh/site-functions /usr/local/var/homebrew /usr/local/var/homebrew/linked /usr/local/Cellar /usr/local/Caskroom /usr/local/Frameworks
==> /usr/bin/sudo /bin/chmod go-w /usr/local/share/zsh /usr/local/share/zsh/site-functions
==> /usr/bin/sudo /usr/sbin/chown *** /usr/local/etc /usr/local/include /usr/local/lib /usr/local/sbin /usr/local/share /usr/local/var /usr/local/opt /usr/local/share/zsh /usr/local/share/zsh/site-functions /usr/local/var/homebrew /usr/local/var/homebrew/linked /usr/local/Cellar /usr/local/Caskroom /usr/local/Frameworks
==> /usr/bin/sudo /usr/bin/chgrp admin /usr/local/etc /usr/local/include /usr/local/lib /usr/local/sbin /usr/local/share /usr/local/var /usr/local/opt /usr/local/share/zsh /usr/local/share/zsh/site-functions /usr/local/var/homebrew /usr/local/var/homebrew/linked /usr/local/Cellar /usr/local/Caskroom /usr/local/Frameworks
==> /usr/bin/sudo /bin/mkdir -p /usr/local/Homebrew
==> /usr/bin/sudo /usr/sbin/chown -R ***:admin /usr/local/Homebrew
==> /usr/bin/sudo /bin/mkdir -p /Users/***/Library/Caches/Homebrew
==> /usr/bin/sudo /bin/chmod g+rwx /Users/***/Library/Caches/Homebrew
==> /usr/bin/sudo /usr/sbin/chown -R *** /Users/***/Library/Caches/Homebrew
==> Searching online for the Command Line Tools
==> /usr/bin/sudo /usr/bin/touch /tmp/.com.apple.dt.CommandLineTools.installondemand.in-progress
==> Installing Command Line Tools for Xcode-13.2
==> /usr/bin/sudo /usr/sbin/softwareupdate -i Command\ Line\ Tools\ for\ Xcode-13.2
Software Update Tool

Finding available software

Downloading Command Line Tools for Xcode
Downloaded Command Line Tools for Xcode
Installing Command Line Tools for Xcode
Done with Command Line Tools for Xcode
Done.
==> /usr/bin/sudo /usr/bin/xcode-select --switch /Library/Developer/CommandLineTools
==> /usr/bin/sudo /bin/rm -f /tmp/.com.apple.dt.CommandLineTools.installondemand.in-progress
==> Downloading and installing Homebrew...
remote: Enumerating objects: 205735, done.
remote: Counting objects: 100% (44/44), done.
remote: Compressing objects: 100% (44/44), done.
remote: Total 205735 (delta 0), reused 44 (delta 0), pack-reused 205691
Receiving objects: 100% (205735/205735), 57.00 MiB | 5.37 MiB/s, done.
Resolving deltas: 100% (151444/151444), done.
From https://github.com/Homebrew/brew
 * [new branch]          dependabot/bundler/Library/Homebrew/msgpack-1.5.1 -> origin/dependabot/bundler/Library/Homebrew/msgpack-1.5.1
 * [new branch]          master                                            -> origin/master
 * [new tag]             0.1                                               -> 0.1
 * [new tag]             0.2                                               -> 0.2
 * [new tag]             0.3                                               -> 0.3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Omittting~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 * [new tag]             3.4.3                                             -> 3.4.3
 * [new tag]             3.4.4                                             -> 3.4.4
 * [new tag]             3.4.5                                             -> 3.4.5
HEAD is now at 56415326b Merge pull request #13113 from Homebrew/update-man-completions
==> Tapping homebrew/core
remote: Enumerating objects: 1172698, done.
remote: Counting objects: 100% (21/21), done.
remote: Compressing objects: 100% (15/15), done.
remote: Total 1172698 (delta 10), reused 16 (delta 6), pack-reused 1172677
Receiving objects: 100% (1172698/1172698), 461.43 MiB | 6.13 MiB/s, done.
Resolving deltas: 100% (812259/812259), done.
From https://github.com/Homebrew/homebrew-core
 * [new branch]              master     -> origin/master
Updating files: 100% (6358/6358), done.
HEAD is now at eaa36582452 checkov: update 2.0.1035 bottle.
==> Downloading https://ghcr.io/v2/homebrew/portable-ruby/portable-ruby/blobs/sha256:0cb1cc7af109437fe0e020c9f3b7b95c3c709b140bde9f991ad2c1433496dd42
############################################################################################################################################## 100.0%
==> Pouring portable-ruby-2.6.8.yosemite.bottle.tar.gz
==> Installation successful!

==> Homebrew has enabled anonymous aggregate formulae and cask analytics.
Read the analytics documentation (and how to opt-out) here:
  https://docs.brew.sh/Analytics
No analytics data has been sent yet (nor will any be during this install run).

==> Homebrew is run entirely by unpaid volunteers. Please consider donating:
  https://github.com/Homebrew/brew#donations

==> Next steps:
- Run brew help to get started
- Further documentation:
    https://docs.brew.sh

***@***noMBP ~ % 
```