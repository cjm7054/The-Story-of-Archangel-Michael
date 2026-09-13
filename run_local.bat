@echo off
title Catholic Video Generator

cd /d "%~dp0"

echo ========================================================
echo   Catholic Video Generator - Typecast Piljae
echo ========================================================
echo.

echo [1/3] Checking Python installation...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org or Microsoft Store.
    pause
    exit /b 1
)

echo [2/3] Installing Python dependencies...
python -m pip install requests pillow edge-tts python-dotenv

echo.
echo [3/3] Downloading high resolution Catholic assets and font...
python src\download_assets.py

echo.
echo ========================================================
echo   Generating Episode 1 Video...
echo ========================================================
python src\main.py --script episodes\ep01_altar_kiss.json --output output

if exist "output\ep01_altar_kiss_final.mp4" (
    echo.
    echo ========================================================
    echo   Video generation completed successfully!
    echo   File: output\ep01_altar_kiss_final.mp4
    echo ========================================================
    start "" "output\ep01_altar_kiss_final.mp4"
) else (
    echo.
    echo [Check] Video file not found. Please review log above.
)

pause
