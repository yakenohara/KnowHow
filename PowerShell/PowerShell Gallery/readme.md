# 使う側

## 環境セットアップ時のみ

`PSGallery` の `InstallationPolicy` を `Trusted` にする

現状確認
```powershell
> Get-PSRepository

Name                      InstallationPolicy   SourceLocation
----                      ------------------   --------------
PSGallery                 Untrusted            https://www.powershellgallery.com/api/v2
```
もし上記のように `Untrusted` となっている場合は、以下のように `Set-PSRepository -Name PSGallery -InstallationPolicy Trusted` で `Trusted` に変更する
```powershell
> Set-PSRepository -Name PSGallery -InstallationPolicy Trusted
> Get-PSRepository

Name                      InstallationPolicy   SourceLocation
----                      ------------------   --------------
PSGallery                 Trusted              https://www.powershellgallery.com/api/v2
```

## モジュールの追加

すべてのユーザーが使用できるようにインストールする (管理者権限が必要)  
([Az.Monitor](https://www.powershellgallery.com/packages/Az.Monitor/7.0.0) をインストールする例)  
```powershell
Install-Module -Name Az.Monitor
```
現在のユーザーが使用できるようにインストールする (管理者権限が不要)  
([powershell-yaml](https://www.powershellgallery.com/packages/powershell-yaml/0.4.12) をインストールする例)  
```powershell
Install-Module -Name powershell-yaml -Scope CurrentUser
```

### 追加済モジュール一覧の確認

`Get-Module -ListAvailable` で確認できる。  
筆者の環境だと、インストール先は以下のようになった。  
すべてのユーザー向けにインストールした場合は、 `C:\Program Files\WindowsPowerShell\Modules`  
現在のユーザー向けにインストールした場合は、 `C:\Users\***\Documents\WindowsPowerShell\Modules`  

```powershell
> Get-Module -ListAvailable


    ディレクトリ: C:\Users\***\Documents\WindowsPowerShell\Modules


ModuleType Version    Name                                ExportedCommands
---------- -------    ----                                ----------------
Script     0.4.12     powershell-yaml                     {ConvertTo-Yaml, ConvertFrom-Yaml, cfy, cty}


    ディレクトリ: C:\Program Files\WindowsPowerShell\Modules


ModuleType Version    Name                                ExportedCommands
---------- -------    ----                                ----------------
Script     5.3.2      Az.Accounts                         {Disable-AzDataCollection, Disable-AzContextAutosave, Enab...
Script     7.0.0      Az.Monitor                          {Add-AzLogProfile, Add-AzMetricAlertRule, Add-AzMetricAler...
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<Omitting>~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    ディレクトリ: C:\WINDOWS\system32\WindowsPowerShell\v1.0\Modules


ModuleType Version    Name                                ExportedCommands
---------- -------    ----                                ----------------
Manifest   1.0.0.0    AppBackgroundTask                   {Disable-AppBackgroundTaskDiagnosticLog, Enable-AppBackgro...
Manifest   2.0.0.0    AppLocker                           {Get-AppLockerFileInformation, Get-AppLockerPolicy, New-Ap...
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<Omitting>~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```
