@echo off
chcp 65001 >nul
title DASHBOARD — Kha Son Green Home CRM
cd /d D:\QuanLyBKD2
python3.13 -m streamlit run dashboard.py --server.headless false --browser.gatherUsageStats false
pause
