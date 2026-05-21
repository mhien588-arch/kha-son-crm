@echo off
chcp 65001 >nul
title BỘ CÔNG CỤ TƯ VẤN KHÁCH HÀNG — Kha Son Green Home
cd /d D:\QuanLyBKD2
set PYTHONIOENCODING=utf-8
python3.13 -m consultation.cli
if errorlevel 1 (
    python -m consultation.cli
)
pause
