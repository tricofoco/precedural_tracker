#!/bin/bash

echo "========================================"
echo "Building Topic Manager Executable"
echo "========================================"
echo

# Check if PyInstaller is installed
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "PyInstaller not found. Installing..."
    pip3 install pyinstaller
fi

echo
echo "Building application..."
echo

# Build the application
pyinstaller --onedir --windowed --name TopicManager topic_manager.py

if [ $? -eq 0 ]; then
    echo
    echo "========================================"
    echo "BUILD SUCCESSFUL!"
    echo "========================================"
    echo
    echo "The executable is located in: dist/TopicManager/"
    echo
    echo "IMPORTANT: Before deploying, remember to:"
    echo "1. Edit topic_manager.py and set the correct shared drive database path"
    echo "2. Rebuild using this script"
    echo "3. Copy the entire dist/TopicManager folder to your deployment location"
    echo
else
    echo
    echo "BUILD FAILED!"
    echo
    exit 1
fi
