@echo off
chcp 65001 >nul
cd /d "%~dp0"
"C:\Users\storm\AppData\Local\Programs\Python\Python314\python.exe" "%~dp0stop.py"