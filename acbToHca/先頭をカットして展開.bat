@echo off

if "%~1" == "" (
  echo ※このウィンドウを閉じて、アーカイブしたいファイルやフォルダをドラッグ＆ドロップしてください。
  pause
  exit /b
)

echo:
"%~dp0afs2.exe" -c %*
rem echo:
rem pause
