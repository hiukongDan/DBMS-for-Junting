@echo off
python -m install pip install --upgrade pip
pip install eel
pip install openpyxl
pip install bcrypt
echo Install required modules successfully!
echo python main.py > junting.cmd
powershell -File shortcut.ps1