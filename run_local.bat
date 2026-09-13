@echo off
chcp 65001 > nul
title 미카엘이 전하는 가톨릭이야기 - 영상 자동 생성기

echo ========================================================
echo   미카엘이 전하는 가톨릭이야기 (신비한 가톨릭사전)
echo   타입캐스트 '필재' 목소리 로컬 영상 자동 생성기
echo ========================================================
echo.

cd /d "%~dp0"

:: 1. 파이썬 환경 확인
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [오류] Python이 설치되어 있지 않거나 PATH에 등록되지 않았습니다.
    echo https://www.python.org 에서 Python 3.10 이상을 설치해주세요.
    pause
    exit /b 1
)

:: 2. FFmpeg 확인
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [주의] FFmpeg가 설치되어 있지 않습니다.
    echo Windows 패키지 관리자(winget)로 FFmpeg 자동 설치를 시도합니다...
    winget install Gyan.FFmpeg --accept-source-agreements --accept-package-agreements
)

:: 3. 필요한 파이썬 라이브러리 자동 설치
echo [1/3] 파이썬 패키지 의존성을 확인하고 설치합니다...
pip install -r requirements.txt >nul 2>&1

:: 4. 고화질 성화 및 나눔명조 폰트 에셋 다운로드
echo [2/3] 나눔명조 폰트 및 고화질 가톨릭 성화 에셋을 점검합니다...
python src\download_assets.py

:: 5. 영상 생성 실행 (필재 목소리 + Ken Burns + 나눔명조 자막)
echo.
echo [3/3] 타입캐스트 '필재' 목소리로 제1화 영상을 생성합니다...
echo --------------------------------------------------------
python src\main.py --script episodes\ep01_altar_kiss.json --output output
echo --------------------------------------------------------

if exist "output\ep01_altar_kiss_final.mp4" (
    echo.
    echo ========================================================
    echo   🎉 영상 제작이 성공적으로 완료되었습니다!
    echo   위치: output\ep01_altar_kiss_final.mp4
    echo ========================================================
    echo.
    echo 완성된 영상을 미디어 플레이어로 즉시 재생합니다...
    start "" "output\ep01_altar_kiss_final.mp4"
) else (
    echo.
    echo [확인] 영상 생성 중 오류가 발생했습니다. 위 콘솔 로그를 확인해주세요.
)

pause
