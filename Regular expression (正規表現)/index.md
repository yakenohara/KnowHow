# 指定文字列を含まない行
//note `VALUE` : 検索したい文字列

```
^(?!.*VALUE).+$
```
# 指定文字列（複数指定）を含まない行
//note `VALUE` : 検索したい文字列(条件を増やす場合は、`|VALUE?`を続けて指定)
```
^(?!.*(VALUE1|VALUE2)).+$
```
# 指定文字列から始まらない行
//note `VALUE` : 検索したい文字列
```
^(?!VALUE).+$
```
# 指定文字列で終わらない行
//note `VALUE` : を検索したい文字列
```
^(?!.*VALUE$).+$
```
# `指定文字列1`を含まないが、`指定文字列2`を含む行
//note  
`VALUE1`:含ませたくない文字列  
`VALUE2`:含ませたい文字列
```
^(?!.*VALUE1).*(?=VALUE2).*$
```

# Links
JavaScript正規表現 怒濤の100サンプル!!  
[http://testcording.com/?p=2013](http://testcording.com/?p=2013)  
