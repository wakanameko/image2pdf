#!/bin/bash

set -e

# 定義
PYTHON_BIN="/usr/local/bin/python3.8"
VENV_DIR="./venv"
read -p "main.pyが格納されているフォルダ名を入力してください: " TARGET_FOLDER
if [ ! -d "$TARGET_FOLDER" ]; then
    echo "エラー: フォルダ '$TARGET_FOLDER' が存在しません。"
    exit 1
fi
TARGET_SCRIPT="$TARGET_FOLDER/main.py"
if [ ! -f "$TARGET_SCRIPT" ]; then
    echo "エラー: $TARGET_SCRIPT が存在しません。"
    deactivate
    exit 1
fi

# 仮想環境(カレントに作成)
# 既存の仮想環境があれば削除
if [ -d "$VENV_DIR" ]; then
    echo "既存の仮想環境を削除中..."
    rm -rf "$VENV_DIR"
fi
echo "Creating virtual environment in $VENV_DIR..."
$PYTHON_BIN -m venv "$VENV_DIR"

source "$VENV_DIR/bin/activate"

# pipとモジュールのインストール・更新
echo "Upgrading pip..."
pip install --upgrade pip
echo "Installing required modules..."
pip install customtkinter
pip install tkinterdnd2
pip install pillow
pip install pyinstaller

# PyInstaller を使ってビルド
# 既存の関連ファイルがあれば消す
if [ -d "./build" ]; then
    echo "既存のビルドファイルを削除中..."
    rm -rf "./build"
    rm -rf "./dist"
    rm -rf "./main.spec"
fi
echo "PyInstallerを実行中..."
pyinstaller --clean --noconfirm --onedir --windowed --name "image2pdf" --add-data="${TARGET_FOLDER}/translation:translation" --add-data="/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/customtkinter:customtkinter/" "$TARGET_SCRIPT"

# 仮想環境をディアクティベート
deactivate

echo "ビルド完了。dist/ ディレクトリに実行ファイルが生成されました。"
