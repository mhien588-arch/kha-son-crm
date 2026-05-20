@echo off
chcp 65001 > nul
title DON DEP BAO CAO - KHA SON GREEN HOME
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
python cleanup_reports.py
pause
