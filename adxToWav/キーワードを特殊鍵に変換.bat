@echo off

echo:
echo キーワードは暗号化タイプ8で使用されます。
set /P X_K="キーワード: "

"%~dp0adx.exe" -y 1 -k "%X_K%" "@"
echo:
pause
