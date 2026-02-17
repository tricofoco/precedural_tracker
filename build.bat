@echo off
echo ========================================
echo Building Topic Manager Executable
echo ========================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
)

echo.
echo Building application...
echo.

REM Build the application
REM pyinstaller --onedir --windowed --name TopicManager topic_manager.py
pyinstaller --onedir --windowed --name ProceduralTracker --icon=app_icon.ico topic_manager.py

if errorlevel 1 (
    echo.
    echo BUILD FAILED!
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo BUILD SUCCESSFUL!
echo ========================================
echo.
echo The executable is located in: dist\ProceduralTracker\
echo.
echo IMPORTANT: Before deploying, remember to:
echo 1. Edit topic_manager.py and set the correct shared drive database path
echo 2. Rebuild using this script
echo 3. Copy the entire dist\TopicManager folder to your deployment location
echo.
pause
