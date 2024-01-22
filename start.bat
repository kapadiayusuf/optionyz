@echo off

rem Navigate to the project directory
cd C:\django_projects\code\optionstrader

rem Activate the virtual environment
call C:\django_projects\code\venv\Scripts\activate.bat

rem Run the development server
python manage.py runserver --insecure

echo Press any key to exit...
pause >nul