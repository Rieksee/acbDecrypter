@echo off

rem ********************************************************************************
rem *           デフォルト値設定                                                   *
rem *                                                                              *
rem *                                                                              *
rem *   ビットモード (8、16、24、32、float、double のどれかを指定)                 *
set X_M=16
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
  echo ※このウィンドウを閉じて、デコードしたいファイルをドラッグ＆ドロップしてください。
  pause
  exit /b
)

echo:
set X_I=
echo 何も入力しない場合、デコード処理を行います。
set /P X_I="ヘッダ情報のみ表示しますか？(何か入力するとヘッダ情報のみ表示): "
if "%X_I%" neq "" (
  echo:
  for %%f in (%*) do "%~dp0adx.exe" -i %%f
  pause
  exit /b
)

echo:
echo ビットモードを入力しない場合、16bitPCMとして出力されます。
set /P X_M="ビットモード (8、16、24、32、float(f)、double(d) のどれかを指定): "
echo:
echo 暗号化されてない場合、キーワードは不要です。
set /P X_K="キーワード: "
set X_BB=
if "%X_K%" == "" (
  echo:
  echo 暗号化されてない場合、復号鍵は不要です。
  set /P X_BB="復号鍵 (16進数16桁で指定): "
)
if "%X_K%%X_BB%" == "" (
  echo:
  echo 暗号化されてない場合、特殊鍵は不要です。
  set /P X_A="特殊鍵 (16進数12桁で指定): "
)
if "%X_BB%" neq "" (
  set X_B=%X_BB%
)
echo:
if "%X_M:~0,1%" == "f" (set X_M=0)
if "%X_M:~0,1%" == "d" (set X_M=1)
set X=-m %X_M% -a %X_A% -b %X_B% -k "%X_K%"
for %%f in (%*) do "%~dp0adx.exe" %X% %%f
echo:
pause
