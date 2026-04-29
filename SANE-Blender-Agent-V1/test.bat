@echo off
setlocal
cd /d "%~dp0"
if not exist venv (
  py -3 -m venv venv
  if errorlevel 1 python -m venv venv
)
call venv\Scripts\activate.bat
python -m pip install -r requirements.txt >nul
python tests\test_suite.py
