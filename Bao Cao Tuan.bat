@echo off
chcp 65001 > nul
title BAO CAO TUAN - KHA SON GREEN HOME
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
python weekly_report.py
pause
