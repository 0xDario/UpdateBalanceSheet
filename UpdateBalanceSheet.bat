@echo off

REM First Window
start "UpdateBalanceSheet Script" cmd /k "cd /d C:\Users\Lupin\source\repos\UpdateBalanceSheet\ && call venv\Scripts\activate && python main.py"

REM Second Window
start "Window 2" cmd /k "cd /d C:\Users\Lupin\source\repos\UpdateBalanceSheet\clientportal.gw && .\bin\run.bat .\root\conf.yaml"
