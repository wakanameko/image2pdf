@echo off
echo. Welcome to builder!
SET APPNAME=image2pdf
SET VERSION=
SET /P VERSION="ビルドする対象のバージョンを入力:"
echo. venvを作成します。既存のvenvは削除します。
if exist venv rmdir /s /q venv
"C:\Python38\python.exe" -m venv "./venv"
call venv\Scripts\activate.bat
echo. 必要なモジュールをインストールします。
pip install customtkinter
pip install tkinterdnd2
pip install pillow
pip install pyinstaller
echo. 既存のビルドファイルがあれば削除します。
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist %APPNAME%.spec del /q %APPNAME%.spec
echo. PyInstallerを実行します。
"C:\Python38\python.exe" -m PyInstaller --noconfirm --onedir --windowed --name %APPNAME% --add-data "C:\Python38\Lib\site-packages/customtkinter;customtkinter/" --add-data "%VERSION%\translation;translation/" "%VERSION%\main.py"
echo. ディレクトリを掃除します。
call venv\Scripts\deactivate.bat
rmdir /s /q venv
rmdir /s /q build
del /q %APPNAME%.spec
echo. 正常に処理を完了しました。
pause