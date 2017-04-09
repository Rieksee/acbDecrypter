@echo off

if "%~1" == "" (
  echo ※このウィンドウを閉じて、解析したいファイルをドラッグ＆ドロップしてください。
  pause
  exit /b
)

echo:
set X_X=1
echo 解析モード
echo 1. 通常解析(デフォルト)
echo 2. 素数解析
echo 3. 全値解析
set /P X_X="番号で指定してください。: "
echo:
"%~dp0adx.exe" -x %X_X% %1
echo:
pause
