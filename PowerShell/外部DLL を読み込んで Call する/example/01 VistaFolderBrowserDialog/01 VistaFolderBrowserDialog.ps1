# <Check STA mode>-------------------------------------------------------------------------------------

# note
# 
# ShowDialog() メソッドを表示させるには、PowerShell を STA 環境で起動する必要がある。
# https://social.technet.microsoft.com/Forums/ja-JP/1b5e7670-9942-4c5c-9b92-e7a0f4c4fef4/windows-7-1997812398-powershell-12391-systemwindowsformsopenfiledialog?forum=powershellja
#
# 理由は不明だが、この事は、 
# (Ookii.Dialogs -> VistaFolderBrowserDialog Class) でも、
# (System.Windows.Forms -> FolderBrowserDialog Class) でも同じ振る舞いをするので、
# STA 環境の起動でなければ、STA 環境で起動した PowerShell に処理を移す

$onStartUp = [Threading.Thread]::CurrentThread.GetApartmentState() # 起動環境を文字列で取得

if( $onStartUp -ne "STA"){ # STA 環境の起動でなければ

    Write-Host "PowerShell started up as ``${onStartUp}`` mode. Re start as STA mode."

    $myScriptName = & {$MyInvocation.ScriptName} # 自分の script ファイルのフルパスを取得
    powershell -sta -File $myScriptName $Args
    exit
}

# ------------------------------------------------------------------------------------</Check STA mode>

$mxOfArgs = $Args.count
for ($idx = 0 ; $idx -lt $mxOfArgs ; $idx++){
    Write-Host $Args[$idx]
}

# Ookii.Dialogs.dll 存在チェック
$fullPathOfOokiiDiaglogsDLL = (Split-Path $MyInvocation.MyCommand.Path -Parent) + "\Ookii.Dialogs.dll" # この ps1 script と同じディレクトリを検索
if(!(Test-Path $fullPathOfOokiiDiaglogsDLL -PathType leaf)){ # 存在しない場合
    Write-Error "``${fullPathOfOokiiDiaglogsDLL}`` not found."
    exit # 終了
}

# 関連オブジェクトの取り込み
Add-Type -AssemblyName System.Windows.Forms
Add-Type -Path $fullPathOfOokiiDiaglogsDLL

# メインウィンドウ取得
$process = [Diagnostics.Process]::GetCurrentProcess()
$window = New-Object Windows.Forms.NativeWindow
$window.AssignHandle($process.MainWindowHandle)

$fd = New-Object Ookii.Dialogs.VistaFolderBrowserDialog

$fd.Description = $Description

if($CurrentDefault -eq $true){
    $fd.SelectedPath = (Get-Item $PWD).FullName # カレントディレクトリを初期フォルダとする
}

# フォルダ選択ダイアログ表示
$ret = $fd.ShowDialog($window)

Write-Host "Selected ``${ret}``"

if ($ret -eq "OK") {
    Write-Host ("Selected Directory:``" + $fd.SelectedPath + "``")
} else {
    Write-Host "Nothing selected"
}
