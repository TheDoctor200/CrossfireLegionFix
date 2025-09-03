@echo off
echo Installing Flet if not already installed...
pip install -r requirements.txt

echo Starting Regional Format Changer...
python regional_format_changer.py

pause
