## OS 起動時の「PC のセットアップを完了しましょう」の無効化

システム > 通知
    「Windows を最大限に活用し、このデバイスの設定を完了する方法を提案する」
    「Windows を使用する際のヒントや提案を入手する」
    

## Windows メニューのインターネット連携させない

個人用設定 > タスクバー
    タスクバー項目
        検索: 「非表示」

PowerShell を管理者権限で以下実行  
```PowerShell
Get-AppxPackage *WebExperience* | Remove-AppxPackage
```
レジストリエディタで以下を設定
```
[HKEY_CURRENT_USER\Software\Policies\Microsoft\Windows\Explorer]
"DisableSearchBoxSuggestions"=dword:00000001
```

## Explorer の右クリックメニューをクラシック化

レジストリエディタで以下を設定
```
[HKEY_CURRENT_USER\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32]
@=""
```
