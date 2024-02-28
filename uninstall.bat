@echo off

rem Virtual environment activate
call .venv\Scripts\activate

rem Packages list
pip list

rem 
echo y | pip uninstall task-manager

rem Virtual environment deactivate
deactivate