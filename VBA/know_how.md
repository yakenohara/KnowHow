# CVErr function

# Parameters

| Constant   | Number | Display | Desctiption                                                                              |
| ---------- | -----: | ------- | ---------------------------------------------------------------------------------------- |
| xlErrDiv0  |   2007 | #DIV/0! | 0割り                                                                                    |
| xlErrNA    |   2042 | #N/A    | 計算や処理の対象となるデータがない、または正当な結果が得られない                         |
| xlErrName  |   2029 | #NAME?  | Excelの関数では利用できない名前(存在しない関数名等)が使用されている                      |
| xlErrNull  |   2000 | #NULL!  | 半角空白文字の参照演算子で指定した2つのセル範囲に、共通部分がない(`=SUM(A1:A3 C1:C3)`等) |
| xlErrNum   |   2036 | #NUM!   | 使用できる範囲外の数値を指定したか、それが原因で関数の解が見つからない                   |
| xlErrRef   |   2023 | #REF!   | 数式内で無効なセルが参照されている                                                       |
| xlErrValue |   2015 | #VALUE! | 関数の引数の形式が間違っている(数値を指定すべきところに文字列を指定等)                   |


## Example

```
Public Function returnErr() As Variant
    returnErr = CVErr(xlErrNA) '#N/Aを返す
End Function
```

# Range.Find method

## Parameters

| Argment           | Constant    | Description                         |
| ----------------- | ----------- | ----------------------------------- |
| What              | -           | 検索するデータを指定(required)      |
| After             | -           | 検索を開始するセルを指定            |
| LookIn (!)        | xlFormulas  | 検索対象を数式に指定(default)       |
|                   | xlValues    | 検索対象を値に指定                  |
|                   | xlComments  | 検索対象をコメント文に指定          |
| LookAt (!)        | xlPart      | 一部が一致するセルを検索(default)   |
|                   | xlWhole     | 全部が一致するセルを検索            |
| SearchOrder (!)   | xlByColumns | 検索方向を行で指定(default)         |
|                   | xlByRows    | 検索方向を列で指定                  |
| SearchDirection   | xlNext      | 順方向で検索(default)               |
|                   | xlPrevious  | 逆方向で検索                        |
| MatchCase (!?)    | False       | 大文字と小文字を区別しない(default) |
|                   | True        | 大文字と小文字を区別する            |
| MatchByte (!)     | False       | 半角と全角を区別しない(default)     |
|                   | True        | 半角と全角を区別する                |
| SearchFormat (!?) | False       | 書式で検索しない(default)           |
|                   | True        | 書式で検索する                      |

(!)  
設定値を省略した場合は、前回設定した値が引き継がれる  
Range.Find method (Excel)  
[https://docs.microsoft.com/ja-jp/office/vba/api/excel.range.find](https://docs.microsoft.com/ja-jp/office/vba/api/excel.range.find)  

(!?)  
MSDN では明記していないが、この Argment も、設定値を省略した場合は、前回設定した値が引き継がれる。  
検索に失敗するとき（Findメソッドの引数省略時に起きる失敗）｜Excel VBA  
[https://www.moug.net/tech/exvba/0150111.html](https://www.moug.net/tech/exvba/0150111.html)  

## Example

```
' 全部が一致するセルを検索
Set foundobj = ThisWorkbook.Sheets(1).UsedRange.Find( _
    What:="findThis", _
    LookAt:=xlWhole _
)

If Not (foundobj Is Nothing) Then '見つかった場合
    Debug.print "found"
End If
```
