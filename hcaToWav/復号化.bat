@echo off

rem ********************************************************************************
rem *           デフォルト値設定                                                   *
rem *                                                                              *
rem *   復号鍵 (16進数16桁で指定)                                                  *
rem set X_K=CF222F1FE0748978
rem *                                                                              *
rem *                                                                              *
rem ********************************************************************************

rem if "%~1" == "" (
rem   echo ※このウィンドウを閉じて、復号化したいファイルをドラッグ＆ドロップしてください。
rem   pause
rem   exit /b
rem )

rem echo:
rem echo 復号鍵を入力しない場合、デフォルト鍵を使用します。
rem set /P X_K="復号鍵 (16進数16桁で指定): "
set X_K=%~1
rem echo:
set X=-c -a %X_K:~8,8% -b %X_K:~0,8%
rem for %%f in (%*) do "%~dp0hca.exe" %X% %%f
for %%f in (%~2) do "%~dp0hca.exe" %X% %%f
rem echo:
rem pause
