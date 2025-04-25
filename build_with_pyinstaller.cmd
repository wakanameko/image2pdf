@echo off
echo. Welcome to builder!
SET APPNAME=image2pdf
SET VERSION=
SET /P VERSION="�r���h����Ώۂ̃o�[�W���������:"
echo. venv���쐬���܂��B������venv�͍폜���܂��B
if exist venv rmdir /s /q venv
"C:\Python38\python.exe" -m venv "./venv"
call venv\Scripts\activate.bat
echo. �K�v�ȃ��W���[�����C���X�g�[�����܂��B
pip install customtkinter
pip install tkinterdnd2
pip install pillow
pip install pyinstaller
echo. �����̃r���h�t�@�C��������΍폜���܂��B
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist %APPNAME%.spec del /q %APPNAME%.spec
echo. PyInstaller�����s���܂��B
"C:\Python38\python.exe" -m PyInstaller --noconfirm --onedir --windowed --name %APPNAME% --add-data "C:\Python38\Lib\site-packages/customtkinter;customtkinter/" --add-data "%VERSION%\translation;translation/" "%VERSION%\main.py"
echo. �f�B���N�g����|�����܂��B
call venv\Scripts\deactivate.bat
rmdir /s /q venv
rmdir /s /q build
del /q %APPNAME%.spec
echo. ����ɏ������������܂����B
pause