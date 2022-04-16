# 文字列の表現


| `'` で括った文字列内                | `"` で括った文字列内                |
| ----------------------------------- | ----------------------------------- |
| `"` はエスケープ無しで記述できる    | `"` はエスケープ無しで記述できる    |
| `'` を表現するには、`''` と記述する | `"` を表現するには、`""` と記述する |
| 変数は展開されない                  | 変数は展開される                    |
| エスケプシーケンスは使えない        | エスケプシーケンスが使える          |
| 部分演算子は使えない                | 部分文字列が使える                  |

## エスケープシーケンス

| 表示させる文字       | 表記            |
| -------------------- | --------------- |
| 改行(CR)             | `` `r``         |
| 改行(LF)             | `` `n``         |
| 改行(CRLF)           | `` `r`n``       |
| `` ` `` | ``` `` ``` |
| 変数                 | `` `$(変数名)`` |

## 部分演算子

`"` で括った文字列内で式を展開して表示したい場合は `$()` を使う。

↓↓ 例 ↓↓  
```powershell
> $a = 100
> $str = "`$a + 10 = $($a + 10)"
> Write-Host $str
$a + 10 = 110
```

## ヒアドキュメント

変数を展開させる場合は `@"` ~ `"@` で括る。  
変数を展開させない場合は `@'` ~ `'@` で括る。  

# 配列

`@( )` ( `,` 区切り) で表記する。入れ子にすることもできるので、以下のように2次元配列を作る事ができる。

```powershell
# 3行2列の 2次元配列を `ForEach-Object` で巡回する例
$t2arr = @(
    ("1-1", "1-2"),
    ("2-1", "2-2"),
    ("3-1", "3-2")
)
$t2arr | ForEach-Object {
    $_ | ForEach-Object {
        Write-Host $_
    }
}
```

# スコープ

## ブロックスコープ

 `{` ~ `}` で囲まれた部分 (=ブロック) はそのブロック内で定義された変数はブロック内でのみ有効となる。以下はブロックスコープ内でのみ有効となるもの。
 
 - 変数
 - 関数
 - エイリアス //todo なにこれ
 - ドライブ //todo なにこれ

↓↓ 例 ↓↓  
```powershell
function Outer {
    Write-Host 'Outer function started.'
    function Inner {
        Write-Host 'Inner function started.'
    }
    Inner
}
Outer
Inner # <- ここでエラーとなる。
```

しかし、以下はスコープを形成しない。

 - `if` や `for` といった制御構文
 - `try` - `catch` - `finally`
 - `begin` - `process` - `end`
 - `ForEach-Object`
 - `.ForEach` method

↓↓ 例 ↓↓  
```powershell
# 定義されていない変数を参照したときにエラーが出るようにする
# (デフォルトは `Set-StrictMode -Off` (エラーは出ない))
Set-StrictMode -Version Latest

# `if` ブロックがブロックスコープを形成しない例
    if ($true) {
        [int] $i_f = 10
    }
    Write-Host "`$i_f = $i_f" # <- エラーとはならない

# `for` ブロックがブロックスコープを形成しない例
    for ($i = 1; $i -le 3; ++$i) {
        $fr = $i
    }
    Write-Host "`$fr = $fr" # <- エラーとはならない

# `ForEach-Object` ブロックがブロックスコープを形成しない例
    1..3 | ForEach-Object {
        $fe = $_
    }
    Write-Host "`$fe = $fe" # <- エラーとはならない

# `.ForEach` method がブロックスコープを形成しない例
    (1..3).ForEach({
        $fem = $_
    })
    Write-Host "`$fem = $fem" # <- エラーとはならない

```

## スクリプトブロック、Call operator `&` (実行演算子) とダイナミックスコープ

↓↓ 呼び出される .ps1 スクリプトファイル ↓↓  
```powershell
$scriptblock = { # <- このブロックが読み込まれた時点では実行されない。
    Write-Host 'Scriptblock started.'
    Write-Host $s
}
function func1 {
    $s = 10
    & $scriptblock
}
function func2 {
    $s = 20
    & $scriptblock
}
func1
func2
```
↓↓ 実行結果 ↓↓  
```PowerShell terminal
> .\Pshell.ps1
Scriptblock started.
10
Scriptblock started.
20
```

 - `{ }` 内に記述されたスクリプトを変数に代入しておくことで、Call operator `&` を使って実行できる。Call operator `&` は別の .ps1 ファイルを実行する際の演算子としても記述できる。(PowerShell スクリプト内で、`& .\(ファイル名).ps1` のように記述する。以降に例を記述)
 - `func1`, `func2` で定義されたブロック内で定義された、同名だが別のスコープを持つ `$s` が、`$scriptblock` というスクリプトブロックから参照されている。それぞれのスコープ毎に `$s` を参照するので、上のような結果になる。このような動作の事を 'ダイナミックスコープ' という。

### .ps1 ファイルから 別の .ps1 ファイルを実行する。

↓↓ 呼び出される .ps1 スクリプトファイル (`Pshell.ps1`) ↓↓  
```powershell
# 引数を巡回してすべて表示する
for ($idx = 0 ; $idx -lt $Args.count ; $idx++){
    Write-Host "No $idx : `"$($Args[$idx])`""
}
```
↓↓ 呼び出す .ps1 スクリプトファイル (`A.ps1`) ↓↓  
```powershell
# 同じディレクトリに配置された `Pshell.ps1` に引数文字列 `argA`, `argB includes space` を渡す例
& .\Pshell.ps1 'argA' 'argB includes space'
```
↓↓ 実行結果 ↓↓  
```PowerShell terminal
> .\A.ps1
No 0 : "argA"
No 1 : "argB includes space
```

### コマンドプロンプト、バッチファイルで実行する例

```Batchfile

@echo off
::
:: 同じディレクトリに配置された `Pshell.ps1` に引数文字列 `argA`, `argB includes space` を渡す例
::

::定数
set ps1FileName=Pshell.ps1
::初期化
set ps1FileFullPath=%~dp0%ps1FileName%
::Call powershell
powershell -ExecutionPolicy Unrestricted "& \"%ps1FileFullPath%\" argA ""argB includes space"""
```
PowerShell  
```powershell
# 引数を巡回してすべて表示する
for ($idx = 0 ; $idx -lt $Args.count ; $idx++){
    Write-Host "No $idx : `"$($Args[$idx])`""
}
```
↓↓ 実行例 ↓↓  
```terminal
>t.bat
No 0 : "argA"
No 1 : "argB includes space"
```

### VBScript で実行する例

コマンドプロンプトから実行する場合は、指定した .ps1 ファイルを叩くだけであるので、標準出力、標準エラー出力を得たい場合は、VBScript で実行する。
もしくは、後述の PowerShell の `Set-Clipboard` コマンドレットを使う。

VBScript  
```VBScript
'
' 同じディレクトリに配置された `Pshell.ps1` に引数文字列 `argA`, `argB includes space` を渡す例
'

' ライブラリからオブジェクト生成
Set WSObj = WScript.CreateObject("WScript.Shell")
Set FSObj = createObject("Scripting.FileSystemObject")

'
' ps1 スクリプトの実行コマンド (文字列) の生成
' Powershell の実行ポリシーを気にしたくないので、
' `powershell -ExecutionPolicy Unrestricted ` を付与している。
'
cmdStr = "powershell -ExecutionPolicy Unrestricted " & _
         """& \""" & FSObj.getParentFolderName(WScript.ScriptFullName) & "\" & "Pshell.ps1" & "\""" & _
         " argA ""argB includes space""" & paramStr & """"

'
' ps1 スクリプトの実行。
' 標準出力、標準エラー出力を得えられる反面、OS 画面 に PowerShell ウィンドウが表示される。
' 標準出力、標準エラー出力が不要で、OS 画面 に PowerShell ウィンドウが表示したくない場合は、
' `WSObj.Run cmdStr` と実行すればいい。
'
Set outExec = WSObj.Exec(cmdStr)

' 標準出力、標準エラー出力を得る
Set StdOut = outExec.StdOut ' 標準出力の取得
Set StdErr = outExec.StdErr ' 標準エラー出力の取得

' 標準出力の整形
szStr = "<STDOUT>" & vbCrLf
Do While Not StdOut.AtEndOfStream
    szStr = szStr & StdOut.ReadLine() &vbCrLf
Loop
szStr = szStr & "</STDOUT>"

' 標準エラー出力の整形
seStr = "<STDERR>" & vbCrLf
Do While Not StdErr.AtEndOfStream
    seStr = seStr & StdErr.ReadLine() &vbCrLf
Loop
seStr = seStr & "</STDERR>"

' 標準出力、標準エラー出力をあわせて表示
msg = "<COMMAND>" & vbCrLf & cmdStr & vbCrLf & "</COMMAND>" & vbCrLf & szStr & vbCrLf & seStr
WScript.Echo msg

' クリップボードにコピー
WSObj.Exec("clip").StdIn.Write msg
```
PowerShell  
```powershell
# 引数を巡回してすべて表示する
for ($idx = 0 ; $idx -lt $Args.count ; $idx++){
    Write-Host "No $idx : `"$($Args[$idx])`""
}
```
↓↓ クリップボードに出力される例 ↓↓  
```
<COMMAND>
powershell -ExecutionPolicy Unrestricted "& \"D:\Pshell.ps1\" argA "argB includes space""
</COMMAND>
<STDOUT>
No 0 : "argA"
No 1 : "argB"
No 2 : "includes"
No 3 : "space"
</STDOUT>
<STDERR>
</STDERR>
```

# dot sourcing [ドットソース]

呼び出したスクリプトブロック内の変数に呼び出し側がアクセスしたい場合に使う。

**例えば、以下はエラーになるが、**

↓↓ 呼び出される .ps1 スクリプトファイル (Pshell.ps1) ↓↓  
```powershell
$varXinPshell = "brabrabra"
```
↓↓ 呼び出す .ps1 スクリプトファイル (A.ps1) ↓↓  
```powershell
# 定義されていない変数を参照したときにエラーが出るようにする
# (デフォルトは `Set-StrictMode -Off` (エラーは出ない))
Set-StrictMode -Version Latest

& .\Pshell.ps1
Write-Host $varXinPshell # <- ここでエラーになる
```
↓↓ 実行結果 ↓↓  
```PowerShell terminal
> .\A.ps1
変数 '$varXinPshell' は、設定されていないために取得できません。
```

**以下はエラーにならない。**

↓↓ 呼び出される .ps1 スクリプトファイル (Pshell.ps1) ↓↓  
```powershell
$varXinPshell = "brabrabra"
```
↓↓ 呼び出す .ps1 スクリプトファイル (A.ps1) ↓↓  
```powershell
# 定義されていない変数を参照したときにエラーが出るようにする
# (デフォルトは `Set-StrictMode -Off` (エラーは出ない))
Set-StrictMode -Version Latest

. .\Pshell.ps1
Write-Host $varXinPshell # <- ここでエラーになる
```
↓↓ 実行結果 ↓↓  
```PowerShell terminal
> .\A.ps1
brabrabra
```

# TIPS

## クリップボード操作

PowerShell 内でクリップボードに出力したい場合は、以下の様にすれば良いが、PowerShell のバージョンが v5.0 以上である必要がある。
```powershell
Set-Clipboard $(変数名)
```
