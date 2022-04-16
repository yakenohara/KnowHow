# <Check STA mode>-------------------------------------------------------------------------------------

# note
# 
# ShowDialog() ���\�b�h��\��������ɂ́APowerShell �� STA ���ŋN������K�v������B
# https://social.technet.microsoft.com/Forums/ja-JP/1b5e7670-9942-4c5c-9b92-e7a0f4c4fef4/windows-7-1997812398-powershell-12391-systemwindowsformsopenfiledialog?forum=powershellja
#
# ���R�͕s�������A���̎��́A 
# (Ookii.Dialogs -> VistaFolderBrowserDialog Class) �ł��A
# (System.Windows.Forms -> FolderBrowserDialog Class) �ł������U�镑��������̂ŁA
# STA ���̋N���łȂ���΁ASTA ���ŋN������ PowerShell �ɏ������ڂ�

$onStartUp = [Threading.Thread]::CurrentThread.GetApartmentState() # �N�����𕶎���Ŏ擾

if( $onStartUp -ne "STA"){ # STA ���̋N���łȂ����

    Write-Host "PowerShell started up as ``${onStartUp}`` mode. Re start as STA mode."

    $myScriptName = & {$MyInvocation.ScriptName} # ������ script �t�@�C���̃t���p�X���擾
    powershell -sta -File $myScriptName $Args
    exit
}

# ------------------------------------------------------------------------------------</Check STA mode>

$mxOfArgs = $Args.count
for ($idx = 0 ; $idx -lt $mxOfArgs ; $idx++){
    Write-Host $Args[$idx]
}

# Ookii.Dialogs.dll ���݃`�F�b�N
$fullPathOfOokiiDiaglogsDLL = (Split-Path $MyInvocation.MyCommand.Path -Parent) + "\Ookii.Dialogs.dll" # ���� ps1 script �Ɠ����f�B���N�g��������
if(!(Test-Path $fullPathOfOokiiDiaglogsDLL -PathType leaf)){ # ���݂��Ȃ��ꍇ
    Write-Error "``${fullPathOfOokiiDiaglogsDLL}`` not found."
    exit # �I��
}

# �֘A�I�u�W�F�N�g�̎�荞��
Add-Type -AssemblyName System.Windows.Forms
Add-Type -Path $fullPathOfOokiiDiaglogsDLL

# ���C���E�B���h�E�擾
$process = [Diagnostics.Process]::GetCurrentProcess()
$window = New-Object Windows.Forms.NativeWindow
$window.AssignHandle($process.MainWindowHandle)

$fd = New-Object Ookii.Dialogs.VistaFolderBrowserDialog

$fd.Description = $Description

if($CurrentDefault -eq $true){
    $fd.SelectedPath = (Get-Item $PWD).FullName # �J�����g�f�B���N�g���������t�H���_�Ƃ���
}

# �t�H���_�I���_�C�A���O�\��
$ret = $fd.ShowDialog($window)

Write-Host "Selected ``${ret}``"

if ($ret -eq "OK") {
    Write-Host ("Selected Directory:``" + $fd.SelectedPath + "``")
} else {
    Write-Host "Nothing selected"
}
