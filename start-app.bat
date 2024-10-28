@echo off
set "script_dir=%~dp0"
cd /d "%script_dir%"
call "%script_dir%env_manager\Scripts\activate.bat"
streamlit run taches.py