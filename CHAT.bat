@echo off
chcp 65001 >nul
title GGUF Runner Hub
cd /d "%~dp0"
set "GGUF_ROOT=%~dp0"
if "%GGUF_ROOT:~-1%"=="\" set "GGUF_ROOT=%GGUF_ROOT:~0,-1%"

call "%~dp0scripts\detect_windows.bat" 2>nul
if exist "%~dp0profiles\preferred_python.txt" (
  set /p GGUF_PREF_PY=<"%~dp0profiles\preferred_python.txt"
)
call "%~dp0scripts\env_python.bat" 2>nul

if not exist "models" mkdir models 2>nul
if not exist "sessions" mkdir sessions 2>nul
if not exist "workspace" mkdir workspace 2>nul

echo ============================================
echo  GGUF Runner — OS class: %GGUF_OS_CLASS%
if defined GGUF_WMIC_VER echo  Windows version: %GGUF_WMIC_VER%
if defined GGUF_REG_VER echo  Registry version: %GGUF_REG_VER%
echo ============================================

set "PY="
if /I "%GGUF_OS_CLASS%"=="legacy" (
  if exist "%~dp0python38\python.exe" (
    set "PY=%~dp0python38\python.exe"
    echo [OK] Legacy Windows — using Python 3.8
  ) else (
    echo [ERROR] ویندوز ۷/۸.۰ است ولی پوشه python38 وجود ندارد.
    echo.
    echo Setup فعلی فقط Python 3.11 ^(python\^) دارد که روی Win7 کار نمی‌کند.
    echo لطفاً بیلد جدید GitHub را نصب کنید که python38 را هم داشته باشد.
    echo.
    echo مسیر فعلی نصب:
    echo   %~dp0
    if exist "%~dp0python\python.exe" echo   [یافت شد] python\python.exe  ^(3.11 — ناسازگار با Win7^)
    if not exist "%~dp0python38\python.exe" echo   [نیست] python38\python.exe
    pause
    exit /b 1
  )
) else (
  if exist "%~dp0python\python.exe" (
    set "PY=%~dp0python\python.exe"
    echo [OK] Modern Windows — using Python 3.11
  ) else if exist "%~dp0python38\python.exe" (
    set "PY=%~dp0python38\python.exe"
    echo [OK] Fallback Python 3.8
  )
)

if not defined PY (
  where python >nul 2>&1 && for /f "delims=" %%P in ('where python') do (
    if not defined PY set "PY=%%P"
  )
)

if not defined PY (
  echo [ERROR] هیچ Python مناسبی پیدا نشد.
  pause
  exit /b 1
)

echo [OK] Using: %PY%

REM Refuse known-bad combination: legacy OS + path contains \python\ not \python38\
echo %PY% | findstr /I "\\python\\python.exe" >nul
if not errorlevel 1 (
  if /I "%GGUF_OS_CLASS%"=="legacy" (
    echo [ERROR] مسدود شد: Python 3.11 روی ویندوز Legacy اجرا نمی‌شود.
    echo api-ms-win-core-path-l1-1-0.dll روی Win7 موجود نیست.
    pause
    exit /b 1
  )
)

"%PY%" -c "import sys; print(sys.version)" 2>nul
if errorlevel 1 (
  echo [ERROR] اجرای python شکست خورد.
  pause
  exit /b 1
)

"%PY%" -c "import customtkinter" 2>nul
if errorlevel 1 (
  echo [ERROR] customtkinter/tkinter موجود نیست.
  pause
  exit /b 1
)

if exist "scripts\python\app_hub.py" (
  echo Starting GGUF Runner Hub...
  "%PY%" "%~dp0scripts\python\app_hub.py"
) else (
  "%PY%" "%~dp0scripts\python\desktop_chat.py"
)
set ERR=%ERRORLEVEL%
if not "%ERR%"=="0" pause
exit /b %ERR%
