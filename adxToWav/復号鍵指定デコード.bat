@echo off
if "%~2" == "" (
 "%~dp0adx.exe" %~1
 exit /b
)
set X_K=%~2
set X=-b %X_K%
"%~dp0adx.exe" %X% %~1
