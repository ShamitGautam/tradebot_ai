@echo off
REM Quick start guide for the Trading Bot (Windows)

echo ==========================================
echo Trading Bot - Quick Start Setup (Windows)
echo ==========================================
echo.

REM Check Python version
echo Checking Python version...
python --version

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Get API credentials from: https://testnet.binancefuture.com/
echo 2. Run: python cli.py init
echo 3. Place orders with: python cli.py order
echo.
echo Examples:
echo   python cli.py order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
echo   python cli.py order --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.5 --price 2500
echo   python cli.py balance
echo.
pause
