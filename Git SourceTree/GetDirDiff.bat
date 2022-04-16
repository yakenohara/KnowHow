set param1=%3

if "%2" == "-1" (
  set param2=
) else (
  set param2=%2
)

cd /d "%~1"
git difftool --dir-diff %param1% %param2%
