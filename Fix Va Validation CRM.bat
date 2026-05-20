@echo off
chcp 65001 > nul
cd /d "%~dp0"
echo.
echo =====================================================
echo  SUA DU LIEU + CAI DROPDOWN VALIDATION
echo  Kha Son Green Home
echo =====================================================
echo.
python fix_and_validate_crm.py
echo.
pause
