@echo off
title BSS Pro Macro - Installation

echo ====================================================
echo   BSS Pro Macro v1.0.0 - Windows Installation
echo   Advanced Bee Swarm Simulator Automation
echo ====================================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found! Starting installation...
echo.

python install.py

pause