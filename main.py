# coding: utf-8
import os
import platform
import shutil
import customtkinter as ctk
from tkinterdnd2 import TkinterDnD, DND_ALL
import PIL

##########
# functions
def openSettingFile():
    try:
        with open(path_setting_ini, "r", encoding="UTF-8") as file_setting:
            global settings, size_window_x, size_window_y, appearance, theme, language, history_dir_img, history_path_pdf, history_format_img
            settings = file_setting.read().splitlines()
            print(settings)
            if (len(settings) != 8):
                print("setting.ini が破損しています。")
                writeSettingFile()
                openSettingFile()
            size_window_x = settings[0]
            size_window_y = settings[1]
            appearance = settings[2]
            theme = settings[3]
            language = settings[4]
            history_dir_img = settings[5]
            history_path_pdf = settings[6]
            history_format_img = settings[7]
    except FileNotFoundError:
        print("setting.ini が見つかりません。")
        writeSettingFile()
        openSettingFile()

def writeSettingFile(mode="default"):
    if mode == "default":
        with open(path_setting_ini, "w", encoding="UTF-8") as file_setting:
            file_setting.write("580\n370\nsystem\nblue\nJapanese\n\n\n\n")
        print("setting.ini を初期化しました。")
    if mode == "save":
        with open(path_setting_ini, "w", encoding="UTF-8") as file_setting:
            global settings, size_window_x, size_window_y, appearance, theme, language, history_dir_img, history_path_pdf, history_format_img
            size_window_x = app.winfo_width()
            size_window_y = app.winfo_height()
            history_dir_img = textbox_dir_img_input.get()
            history_path_pdf = textbox_path_pdf_input.get()
            history_format_img = combo_format.get()
            file_setting.write(f"{size_window_x}\n{size_window_y}\n{appearance}\n{theme}\n{language}\n{history_dir_img}\n{history_path_pdf}\n{history_format_img}\n")

def open_language_file(lang="Japanese"):
    try:
        with open("{}{}.txt".format(path_dir_translation, lang), "r", encoding="UTF-8") as file_language:
            global info_files_converting, success_files_convert, error_image_not_found, error_not_a_dir, error_file_dest_not_found, error_file_type_not_found, popup_title_choose_dir_img, popup_title_save_path_pdf
            translations = file_language.read().splitlines()
            print(translations)

            # GUI section 2
            label_dir_img.configure(text=translations[0])
            label_img_format.configure(text=translations[1])
            button_dir_img_open.configure(text=translations[2])
            textbox_dir_img_input.configure(placeholder_text=translations[3])
            label_path_pdf.configure(text=translations[4])
            button_path_pdf_open.configure(text=translations[5])
            textbox_path_pdf_input.configure(placeholder_text=translations[6])
            # GUI section 3
            button_convert_img_pdf.configure(text=translations[7])
            # infomation messages
            info_files_converting = translations[8]
            # success messages
            success_files_convert = translations[9]
            # error messages
            error_image_not_found = translations[10]
            error_not_a_dir = translations[11]
            error_file_dest_not_found = translations[12]
            error_file_type_not_found = translations[13]
            # popup window
            popup_title_choose_dir_img = translations[14]
            popup_title_save_path_pdf = translations[15]
    except FileNotFoundError:
        print("言語ファイル「{}{}.txt」が見つかりません。".format(path_dir_translation, lang))
        open_language_file()
    except UnicodeDecodeError:
        print("言語ファイル「{}{}.txt」が読み込めません。".format(path_dir_translation, lang))
        open_language_file()


def choose_dir_img():
    global history_dir_img
    if history_dir_img:
        initial_dir_img = history_dir_img
    else:
        initial_dir_img = currentDir
    open_dir_img = ctk.filedialog.askdirectory(title=popup_title_choose_dir_img, initialdir=initial_dir_img)
    if open_dir_img:
        textbox_dir_img_input.delete(0, ctk.END)
        textbox_dir_img_input.insert(0, open_dir_img)
        writeSettingFile(mode="save")

def choose_path_pdf():
    global history_path_pdf
    if history_path_pdf:
        initial_path_pdf = os.path.dirname(history_path_pdf)
    else:
        initial_path_pdf = currentDir
    array_filetypes = [("PDFファイル", ".pdf"), ("その他のフォーマット", ".*") ]
    save_path_pdf = ctk.filedialog.asksaveasfilename(title=popup_title_save_path_pdf, initialdir=initial_path_pdf, filetypes=array_filetypes, defaultextension=".pdf")
    if save_path_pdf:
        textbox_path_pdf_input.delete(0, ctk.END)
        textbox_path_pdf_input.insert(0, save_path_pdf)
        writeSettingFile(mode="save")

def choose_with_dnd(event):
    global history_dir_img, history_path_pdf
    # サンプルコードの受け売り
    dropped_file = event.data.replace("{","").replace("}", "")
    # 何かしらを受け取ったらテキストボックスを更新
    if dropped_file:
        if event.widget == frame_dir_img:
            textbox_dir_img_input.delete(0, ctk.END)
            textbox_dir_img_input.insert(0, dropped_file)
            writeSettingFile(mode="save")
        elif event.widget == frame_path_pdf:
            textbox_path_pdf_input.delete(0, ctk.END)
            textbox_path_pdf_input.insert(0, dropped_file)
            writeSettingFile(mode="save")


def run_image_pdf():
    global history_dir_img, history_path_pdf
    writeSettingFile(mode="save")
    try:
        array_file_all = os.listdir(history_dir_img)    # 昇順になるしDSstoreも出てくる
        array_file_image = [i for i in array_file_all if i.endswith(history_format_img)]
        if not array_file_image:
            raise FileNotFoundError
    except FileNotFoundError:
        label_convert_status.configure(text=error_image_not_found, text_color="red")
        return
    except NotADirectoryError:
        # 画像フォルダがzipファイルの場合
        tmp_pop_dir_img = []
        for i in range(-4, 0):
            tmp_pop_dir_img.append(history_dir_img[i])
        tmp_pop_dir_img_str = "".join(tmp_pop_dir_img)
        if tmp_pop_dir_img_str == ".zip":
            tmp_unzip_dir_img = os.path.dirname(history_dir_img)
            shutil.unpack_archive(history_dir_img, history_dir_img[:-4])
            history_dir_img = history_dir_img[:-4]  # 末尾の4文字（.zip）を取り除く
            textbox_dir_img_input.delete(0, ctk.END)
            textbox_dir_img_input.insert(0, history_dir_img)
            return run_image_pdf()
        
        label_convert_status.configure(text=error_not_a_dir, text_color="red")
        return

    # 出力先が空の場合
    if not history_path_pdf:
        label_convert_status.configure(text=error_file_dest_not_found, text_color="red")
        return
    
    # 出力ファイルの拡張子が未指定の場合
    tmp_pop_path_pdf = []
    for i in range(-4, 0):
        # nonlocal tmp_pop_path_pdf
        tmp_pop_path_pdf.append(history_path_pdf[i])
    tmp_pop_path_pdf_str = "".join(tmp_pop_path_pdf)
    if tmp_pop_path_pdf_str != ".pdf":
        label_convert_status.configure(text=error_file_type_not_found, text_color="red")
        print(tmp_pop_path_pdf_str)
        return

    # 変換
    image_objs = []
    for j, i in enumerate(array_file_image):
        path_images = os.path.join(history_dir_img, i)
        with PIL.Image.open(path_images) as convert_image:
            image_objs.append(convert_image.convert('RGB'))
        progressbar.set((j + 1) / len(array_file_image))
        label_convert_status.configure(text=info_files_converting.format(j+1, len(array_file_image)), text_color=("blue", "cyan"))  # タプルで色指定したら(Light, Dark)で適用されるらしい
        app.update_idletasks()
    image_objs[0].save(history_path_pdf, "PDF", resolution=100.0, save_all=True, append_images=image_objs[1:])

    label_convert_status.configure(text=success_files_convert, text_color="green")


def quit_thisAPP(event=None):
    writeSettingFile(mode="save")
    app.destroy()
    quit()

##########
# initialize
APPNAME = "image2pdf"
VERSION = 1.6
DEVELOPER = "wakanameko"
currentDir = os.path.dirname(__file__)
print("{}/setting.ini".format(currentDir))
env_OS = platform.system()
if env_OS == "Darwin":
    path_setting_ini = "{}/setting.ini".format(currentDir)
    path_dir_translation = "{}/translation/".format(currentDir)
    name_filer = "Finder"
elif env_OS == "win32" or "Windows":
    path_setting_ini = "{}\\setting.ini".format(currentDir)
    path_dir_translation = "{}\\translation\\".format(currentDir)
    name_filer = "Explorer"
print("####################\n" + APPNAME, "version:", VERSION, "by", DEVELOPER, "\nOS:", env_OS,"\n####################")
try:
    openSettingFile()
except UnicodeDecodeError:
    print("setting.iniの読み込み中にエラーが発生しました。例外: UnicodeDecodeError")
    writeSettingFile()
    openSettingFile()

##########
# initialize main window
# クラス定義
class CTk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)
class DnDFrame(ctk.CTkFrame, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)
ctk.set_appearance_mode(appearance)  # options: "Light", "Dark", "System"
ctk.set_default_color_theme(theme)  # options: "blue", "green", "dark-blue"
app = ctk.CTk()
app.title("{} | version: {}".format(APPNAME, VERSION))
try:
    app.geometry("{}x{}".format(size_window_x, size_window_y))
except TypeError:
    writeSettingFile()
    app.geometry("{}x{}".format(size_window_x, size_window_y))
# Tkinter のデフォルトフォントを強制変更
ctk.CTkFont._default_font = ctk.CTkFont("system-ui")
# メインフレームの作成（スクロール可）
frame_main = ctk.CTkScrollableFrame(app)
frame_main.pack(fill="both", expand=True, padx=10, pady=10)


##########
# Place Widgets
# section1
label_appname = ctk.CTkLabel(master=frame_main, text=APPNAME, font=("system-ui", 18, "bold"))
label_appname.pack(pady=(0, 5))
separator1 = ctk.CTkFrame(master=frame_main, height=2, fg_color="gray")
separator1.pack(fill="x", pady=(5, 10))
# section2
label_dir_img = ctk.CTkLabel(master=frame_main, text="", font=("system-ui", 14, "bold"))
label_dir_img.pack(pady=(5, 0))
frame_img_format = ctk.CTkFrame(master=frame_main) # D&Dするために、継承クラスを使用してフレーム作成
frame_img_format.pack(anchor="center", fill="x", expand=True, pady=(5, 0))
label_img_format_margin_L = ctk.CTkLabel(master=frame_img_format, text="", font=("system-ui", 0, "normal"))
label_img_format_margin_L.pack(side="left", expand=True, padx=(0, 5))
label_img_format = ctk.CTkLabel(master=frame_img_format, text="", font=("system-ui", 12, "normal"))
label_img_format.pack(side="left", padx=(0, 5))
combo_format = ctk.CTkComboBox(master=frame_img_format, font=("system-ui", 14, "normal"), values=["png", "bmp", "webp"])
combo_format.pack(side="left", padx=(0, 5))
label_img_format_margin_R = ctk.CTkLabel(master=frame_img_format, text="", font=("system-ui", 0, "normal"))
label_img_format_margin_R.pack(side="left", expand=True, padx=(0, 5))
if history_format_img:
    combo_format.set(history_format_img)

frame_dir_img = DnDFrame(master=frame_main)
frame_dir_img.pack(fill="x", expand=True, pady=(5, 10))
button_dir_img_open = ctk.CTkButton(master=frame_dir_img, text="", font=("system-ui", 14, "normal"), command=lambda:choose_dir_img())
button_dir_img_open.pack(side="left", padx=(0, 5))
textbox_dir_img_input = ctk.CTkEntry(master=frame_dir_img, font=("system-ui", 14, "normal"), placeholder_text="")
textbox_dir_img_input.pack(side="left", fill="x", expand=True)
if history_dir_img:
    textbox_dir_img_input.insert(0, history_dir_img)
frame_dir_img.drop_target_register(DND_ALL)
frame_dir_img.dnd_bind("<<Drop>>", choose_with_dnd)

label_path_pdf = ctk.CTkLabel(master=frame_main, text="", font=("system-ui", 14, "bold"))
label_path_pdf.pack(pady=(5, 2))
frame_path_pdf = DnDFrame(master=frame_main)
frame_path_pdf.pack(fill="x", expand=True, pady=(5, 10))
button_path_pdf_open = ctk.CTkButton(master=frame_path_pdf, text="", font=("system-ui", 14, "normal"), command=lambda:choose_path_pdf())
button_path_pdf_open.pack(side="left", padx=(0, 5))
textbox_path_pdf_input = ctk.CTkEntry(master=frame_path_pdf, font=("system-ui", 14, "normal"), placeholder_text="")
textbox_path_pdf_input.pack(side="left", fill="x", expand=True)
if history_path_pdf:
    textbox_path_pdf_input.insert(0, history_path_pdf)
frame_path_pdf.drop_target_register(DND_ALL)
frame_path_pdf.dnd_bind("<<Drop>>", choose_with_dnd)
separator2 = ctk.CTkFrame(master=frame_main, height=2, fg_color="gray")
separator2.pack(fill="x", pady=(5, 10))
# section3
button_convert_img_pdf = ctk.CTkButton(master=frame_main, text="", font=("system-ui", 14, "bold"), command=lambda:run_image_pdf())
button_convert_img_pdf.pack(pady=(5, 0))
label_convert_status = ctk.CTkLabel(master=frame_main, text="", font=("system-ui", 12, "normal"))
label_convert_status.pack(pady=(2, 0))
progressbar = ctk.CTkProgressBar(master=frame_main, width=200, height=8)
progressbar.pack(padx=(15, 15), pady=(2, 7), fill="x", expand=True)
progressbar.set(0)



# load translation file
open_language_file(lang=language)

# ウィンドウが消されたときの処理
app.protocol("WM_DELETE_WINDOW", quit_thisAPP)
# ショートカットキー
app.bind("<Control-w>", quit_thisAPP)
app.bind("<Control-q>", quit_thisAPP)

app.mainloop()
