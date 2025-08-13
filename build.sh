#!/bin/bash

# 入力
read -p "バージョンを入力: " VERSION
VERSION_INT=$(echo "$VERSION * 10" | bc | cut -d. -f1)

# define App Name
APP_NAME=image2pdf

# path
ROOT_PATH="/Users/haruno/Documents/My Softwares/$APP_NAME"
PYTHON_PATH="/Library/Frameworks/Python.framework/Versions/3.8/bin/python3"
SCRIPT_PATH="$ROOT_PATH/$VERSION/main.py"
TRANSLATION_PATH="$ROOT_PATH/$VERSION/translation"
APP_PATH_OLD="$ROOT_PATH/dist/$APP_NAME v$VERSION.app"

# option
if [ $VERSION_INT -ge 15 ]; then
    PYINSTALLER_OPTS="--noconfirm --onedir --windowed \
    --add-data \"env/lib/python3.8/site-packages/customtkinter:customtkinter/\" \
    --add-data \"env/lib/python3.8/site-packages/tkinterdnd2:tkinterdnd2/\" \
    --add-data \"$TRANSLATION_PATH:translation/\" \
    --name \"$APP_NAME v$VERSION\" "
else
    PYINSTALLER_OPTS="--noconfirm --onedir --windowed \
    --add-data \"env/lib/python3.8/site-packages/customtkinter:customtkinter/\" \
    --add-data \"$TRANSLATION_PATH:translation/\" \
    --name \"$APP_NAME v$VERSION\" "
fi

#------------------------------------------------------------------------------------#

# make venv
$PYTHON_PATH -m venv env
source env/bin/activate

# install requirements
env/bin/python3 -m pip install pyinstaller
env/bin/python3 -m pip install --upgrade pip
env/bin/python3 -m pip install customtkinter
env/bin/python3 -m pip install pillow
if [ $VERSION_INT -ge 15 ]; then
    env/bin/python3 -m pip install tkinterdnd2
fi

# do PyInstaller
eval "env/bin/python3 -m PyInstaller $PYINSTALLER_OPTS \"$SCRIPT_PATH\""

# goodbye venv
deactivate

# copy to root from dist
cp -R "$APP_PATH_OLD" "$ROOT_PATH"

#------------------------------------------------------------------------------------#

# configure of signature
codesign --remove-signature "image2pdf v$VERSION.app"

#------------------------------------------------------------------------------------#

# zipping
ditto -c -k --sequesterRsrc --keepParent "${ROOT_PATH}/image2pdf v${VERSION}.app" "${ROOT_PATH}/Mac.x64.Intel.zip"

#------------------------------------------------------------------------------------#

# cleanup
rm -r "$ROOT_PATH/build"
rm -r "$ROOT_PATH/dist"
rm -r "$ROOT_PATH/image2pdf v$VERSION.spec"
rm -r "$ROOT_PATH/env"
