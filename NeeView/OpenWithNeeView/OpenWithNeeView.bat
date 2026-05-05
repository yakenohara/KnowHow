:: <CAUTION!>
:: 管理者権限で実行すること
:: </CAUTION!>

@echo off
:: 定数
set ps1FileName=OpenWithNeeView.ps1

:: 初期化
set ps1FileFullPath=%~dp0%ps1FileName%


:: Call powershell
powershell -ExecutionPolicy Bypass "& \"%ps1FileFullPath%\""

:: errorlevel 判定
if %errorlevel% neq 0 (
    pause
    exit /b 1
)
