@echo off
echo Virtual environment activate
call .venv\Scripts\activate

echo Install packages global
pip install -e .

echo Package start
manager

echo 
pause