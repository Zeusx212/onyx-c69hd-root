@echo off
setlocal
title Onyx Boox C69HD Root Setup Tool
python "%~dp0c69hd_root_tool.py"
if %errorlevel% neq 0 pause
