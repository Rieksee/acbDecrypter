@echo off

if "%~1" == "" (
  echo ※このウィンドウを閉じて、解析したいファイルをドラッグ＆ドロップしてください。
  pause
  exit /b
)

echo:
set X_Z=
echo 何も入力しない場合、素数を使って解析します。
set /P X_Z="全ての値で解析しますか？(何か入力すると全ての値で解析): "
echo:
if "%X_Z%" neq "" (set X_Z=-z)
"%~dp0adx.exe" -x %X_Z% %1
echo:
pause
