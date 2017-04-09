@echo off

echo:
echo 復号鍵は暗号化タイプ9で使用されます。
set /P X_B="復号鍵 (16進数16桁で指定): "

"%~dp0adx.exe" -y 2 -b %X_B% "@"
echo:
pause
