# Git の Commit Author と Commiter を変更する

Git のコミットには、Author と Commiter の2つが存在する

e.g.
```
$ git log -1 --pretty=full
commit 90b59c48c7ce2e0ec7229445b664f9872133c5a6
Author: hogehoge <aaaaaa@example.com>
Commit: fugafuga <bbbbbb@example.com>

    add xxx.txt
```

## Commiter の変更

リポジトリ直下の `.gitconfig` に以下設定を追加する  

```
git config --local user.name fixed_name
git config --local user.email fixed_email@example.com
```

更新したい情報を `.gitconfig` に設定した後、`--amend` で変更する  

```
git commit --amend
```

## Author の変更

Author も変更する場合は、下記のように `--author` 追加してコミットする。

```
$ git commit --amend --author="fixed_name <dummy_email_address@example.com>"
$ git rebase --continue
# 変更されたか確認
$ git log --pretty=full
# すでにプッシュしてしまっているなら、-f が必要になる
$ git push origin hoge
```

## 過去のコミットをすべて変更する

`<CAUTION!>`
push 済みの場合は force push が必要
`</CAUTION!>`

```
$ git filter-branch -f --env-filter "GIT_AUTHOR_NAME='fixed_name'; GIT_AUTHOR_EMAIL='fixed_email@example.com'; GIT_COMMITTER_NAME='fixed_name'; GIT_COMMITTER_EMAIL='fixed_email@example.com';" HEAD 
```
