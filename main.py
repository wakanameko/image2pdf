# coding: utf-8
import os
import platform
import customtkinter as ctk
import PIL

##########
# functions
def openSettingFile():
    try:    
        with open(path_setting_ini, "r", encoding="UTF-8") as file_setting:
            global settings, size_window_x, size_window_y, appearance, theme, language, history_dir_img, history_path_pdf
            settings = file_setting.read().splitlines()
            print(settings)
            if (len(settings) != 7):
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
    except FileNotFoundError:
        print("setting.ini が見つかりません。")
        writeSettingFile()
        openSettingFile()

def writeSettingFile(mode="default"):
    if mode == "default":
        with open(path_setting_ini, "w", encoding="UTF-8") as file_setting:
            file_setting.write("410\n310\nsystem\nblue\njapanese\n\n\n")
        print("setting.ini を初期化しました。")
    if mode == "save":
        with open(path_setting_ini, "w", encoding="UTF-8") as file_setting:
            global settings, size_window_x, size_window_y, appearance, theme, language, history_dir_img, history_path_pdf
            size_window_x = app.winfo_width()
            size_window_y = app.winfo_height()
            history_dir_img = textbox_dir_img_input.get()
            history_path_pdf = textbox_path_pdf_input.get()
            file_setting.write(f"{size_window_x}\n{size_window_y}\n{appearance}\n{theme}\n{language}\n{history_dir_img}\n{history_path_pdf}\n")

def choose_dir_img():
    global history_dir_img
    open_dir_img = ctk.filedialog.askdirectory(title="PDF形式に変換する画像が入ったフォルダを選択してください。", initialdir=currentDir)
    if open_dir_img:
        textbox_dir_img_input.delete(0, ctk.END)
        textbox_dir_img_input.insert(0, open_dir_img)
        writeSettingFile(mode="save")

def choose_path_pdf():
    array_filetypes = [("PDFファイル", ".pdf"), ("その他のフォーマット", ".*") ]
    save_path_pdf = ctk.filedialog.asksaveasfilename(title="PDFファイルの保存先を指定してください。", initialdir=currentDir, filetypes=array_filetypes, defaultextension=".pdf")
    if save_path_pdf:
        textbox_path_pdf_input.delete(0, ctk.END)
        textbox_path_pdf_input.insert(0, save_path_pdf)
        writeSettingFile(mode="save")

def run_image_pdf():
    writeSettingFile(mode="save")
    try:
        array_file_all = os.listdir(history_dir_img)    # 昇順になるしDSstoreも出てくる
        array_file_image = [i for i in array_file_all if i.endswith(".png")]
    except FileNotFoundError:
        print("画像が見つかりませんでした。")
        return
    
    image_objs = []
    for j, i in enumerate(array_file_image):
        path_images = os.path.join(history_dir_img, i)
        print(path_images, j)
        with PIL.Image.open(path_images) as convert_image:
            image_objs.append(convert_image.convert('RGB'))
        print("successfully converting {} files!".format(j+1))
    image_objs[0].save(history_path_pdf, "PDF" ,resolution=100.0, save_all=True, append_images=image_objs[1:])

def quit_thisAPP():
    writeSettingFile(mode="save")
    app.destroy
    quit()

##########
# initialize
APPNAME = "image2pdf"
VERSION = 1.0
DEVELOPER = "wakanameko"
currentDir = os.path.dirname(__file__)
env_OS = platform.system()
if env_OS == "Darwin":
    path_setting_ini = "{}/setting.ini".format(currentDir)
    name_filer = "Finder"
elif env_OS == "win32" or "Windows":
    path_setting_ini = "{}\\setting.ini".format(currentDir)
    name_filer = "Explorer"
print("####################\n",APPNAME, "version:", VERSION, "by", DEVELOPER, "\nOS:", env_OS,"\n####################")

openSettingFile()

##########
# initialize main window
ctk.set_appearance_mode(appearance)  # options: "Light", "Dark", "System"
ctk.set_default_color_theme(theme)  # options: "blue", "green", "dark-blue"
app = ctk.CTk()
app.title("{} | version: {}".format(APPNAME, VERSION))
app.geometry("{}x{}".format(size_window_x, size_window_y))
# メインフレームの作成（スクロール可）
frame_main = ctk.CTkScrollableFrame(app)
frame_main.pack(fill="both", expand=True, padx=10, pady=10)

##########
# Place Widgets
# section1
label_appname = ctk.CTkLabel(master=frame_main, text=APPNAME, font=("system-ui", 16, "bold"))
label_appname.pack(pady=(10, 5))
separator1 = ctk.CTkFrame(master=frame_main, height=2, fg_color="gray")
separator1.pack(fill="x", pady=(5, 10))
# section2
label_dir_img = ctk.CTkLabel(master=frame_main, text="PDFにする画像フォルダ", font=("system-ui", 14, "bold"))
label_dir_img.pack(pady=(5, 2))
frame_dir_img = ctk.CTkFrame(master=frame_main)
frame_dir_img.pack(fill="x", expand=True, pady=(5, 10))
button_dir_img_open = ctk.CTkButton(master=frame_dir_img, text="フォルダを選択", command=lambda:choose_dir_img())
button_dir_img_open.pack(side="left", padx=(0, 5))
textbox_dir_img_input = ctk.CTkEntry(master=frame_dir_img, placeholder_text="画像ファイルが入ったフォルダを選択")
textbox_dir_img_input.pack(side="left", fill="x", expand=True)
if history_dir_img:
    textbox_dir_img_input.insert(0, history_dir_img)
label_path_pdf = ctk.CTkLabel(master=frame_main, text="PDFの保存先", font=("system-ui", 14, "bold"))
label_path_pdf.pack(pady=(5, 2))
frame_path_pdf = ctk.CTkFrame(master=frame_main)
frame_path_pdf.pack(fill="x", expand=True, pady=(5, 10))
button_path_pdf_open = ctk.CTkButton(master=frame_path_pdf, text="ファイルを指定", command=lambda:choose_path_pdf())
button_path_pdf_open.pack(side="left", padx=(0, 5))
textbox_path_pdf_input = ctk.CTkEntry(master=frame_path_pdf, placeholder_text="PDFファイルの保存先を指定")
textbox_path_pdf_input.pack(side="left", fill="x", expand=True)
if history_path_pdf:
    textbox_path_pdf_input.insert(0, history_path_pdf)
separator2 = ctk.CTkFrame(master=frame_main, height=2, fg_color="gray")
separator2.pack(fill="x", pady=(5, 10))
# section3
button_convert_img_pdf = ctk.CTkButton(master=frame_main, text="実行", command=lambda:run_image_pdf())
button_convert_img_pdf.pack(pady=(5, 2))


# ウィンドウが消されたときの処理
#app.protocol("WM_DELETE_WINDOW", quit_thisAPP())
app.mainloop()