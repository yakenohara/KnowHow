'<!Caution!>
'
'ディレクトリは無視します
'
'</!Caution!>

'設定
str_mpcPath = "C:\Program Files\MPC-BE x64\mpc-be64.exe"

'ライブラリからオブジェクト生成
Set ShellObj = CreateObject("WScript.Shell")
Set FSObj = createObject("Scripting.FileSystemObject")
Set fileArrayList = CreateObject("System.Collections.ArrayList")

'ArrayList作成ループ
For Each arg In WScript.Arguments
    If Not(FSObj.FolderExists(arg)) Then 'ファイルの場合
        Call fileArrayList.Add(FSObj.GetAbsolutePathName(arg))
    End If
Next

'件数チェック
If fileArrayList.Count = 0 Then 'ファイル指定が0件の場合
    WScript.Quit '終了する
End If

'名前順で並べ替え
Call fileArrayList.Sort

'結合して配列を取得
names = fileArrayList.ToArray

'ItemListの作成
cmdStr = """" & str_mpcPath & """ /add"
itrMx = UBound(names)
For itr = 0 To itrMx
    cmdStr = cmdStr & " """ & names(itr) & """"
Next    

'クリップボードにコピー
'ShellObj.Exec("clip").StdIn.Write cmdStr

ShellObj.Run cmdStr
