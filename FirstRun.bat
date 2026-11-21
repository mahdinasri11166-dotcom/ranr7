@echo off
chcp 65001 >nul
title GGUF Runner — First Run
cd /d "%~dp0"
call "%~dp0scripts\detect_windows.bat" 2>nul
call "%~dp0scripts\install_detect_windows.bat" 2>nul
echo GGUF_OS_CLASS=%GGUF_OS_CLASS%> "%~dp0profiles\os_class.txt" 2>nul

echo OS class: %GGUF_OS_CLASS%
if /I "%GGUF_OS_CLASS%"=="legacy" (
  if not exist "%~dp0python38\python.exe" (
    echo [ERROR] Win7/8.0 نیاز به python38 دارد — در این نصب نیست.
    echo دوباره از GitHub Actions فایل Setup کامل را بگیرید.
    pause
    exit /b 1
  )
  echo [OK] python38 present
) else (
  if exist "%~dp0python\python.exe" echo [OK] python 3.11 present
)

if not exist "models\*.gguf" (
  if not exist models mkdir models
  explorer "%~dp0models"
)
call "%~dp0CHAT.bat"
