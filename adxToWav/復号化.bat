@echo off

rem ********************************************************************************
rem *           デフォルト値設定                                                   *
rem *                                                                              *
rem *   キーワード                                                                 *
set X_K=
rem *                                                                              *
rem *   復号鍵 (16進数16桁で指定)                                                  *
set X_B=CF222F1FE0748978
rem *                                                                              *
rem *   特殊鍵 (16進数12桁で指定)                                                  *
set X_A=000000000000
rem *                                                                              *
rem *                                                                              *
rem ********************************************************************************

if "%~1" == "" (
  echo ※このウィンドウを閉じて、復号化したいファイルをドラッグ＆ドロップしてください。
  pause
  exit /b
)

echo:
echo キーワードは暗号化タイプ8で使用されます。
set /P X_K="キーワード: "
set X_BB=
if "%X_K%" == "" (
  echo:
  echo 復号鍵は暗号化タイプ9で使用されます。
  set /P X_BB="復号鍵 (16進数16桁で指定): "
)
if "%X_K%%X_BB%" == "" (
  echo:
  echo 特殊鍵は暗号化タイプに関係なく使用されます。
  set /P X_A="特殊鍵 (16進数12桁で指定): "
)
if "%X_BB%" neq "" (
  set X_B=%X_BB%
)
echo:
set X=-c -a %X_A% -b %X_B% -k "%X_K%"
for %%f in (%*) do "%~dp0adx.exe" %X% %%f
echo:
pause
