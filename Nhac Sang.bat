@echo off
chcp 65001 > nul
title NHAC NHO SANG - KHA SON GREEN HOME
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
python nhac_sang.py
