@echo off
setlocal
title Onyx Boox C69HD Factory Stock Restore
python "%~dp0c69hd_restore_stock.py"
if %errorlevel% neq 0 pause
