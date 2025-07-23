@echo off
echo ======================================================
echo         Daily News Reels - Video Quality Analyzer
echo ======================================================

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not in PATH. Please install Python 3.8+
    pause
    exit /b 1
)

REM Install required packages if needed
echo Installing/updating required packages...
python -m pip install opencv-python librosa moviepy numpy soundfile pillow tqdm colorama rich

REM Run the video analyzer
echo.
echo Starting Video Quality Analyzer...
echo.
python showcase_video_analyzer.py

pause
