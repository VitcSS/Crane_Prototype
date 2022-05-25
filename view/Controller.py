from time import sleep
import tkinter as tk
from tkinter import font as tkfont
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from PIL import Image
from PIL import ImageTk
import threading
from pathlib import Path
import os
import time

import globalData as globalData

scr_w = 1280
scr_h = 720

backGroundColor = '#F0DCAB'
transparentColor = '#915f07'
buttonBackGroundColor = '#003333'
buttonActiveBackGroundColor = '#669999'

evt = threading.Event()

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def setBackgroundLabel(parent, BackGroundType = None):
    """Place background image on a label"""

    mySelfParent = parent

    if BackGroundType is not None:
        print(BackGroundType)
    BackGroundImage = Image.open(relative_to_assets("backgrond.png"))

    BackGroundImage = ImageTk.PhotoImage(BackGroundImage)
    background_label = tk.Label(parent, image=BackGroundImage, background=backGroundColor)
    background_label.place(relx=0, y=0, relheight=1, relwidth=1)
    parent.img = BackGroundImage

def measureslog(string):
    log = open("log_measures.txt", "a")
    Day = time.strftime("%m-%d-%Y", time.localtime())
    Time = time.strftime("%I:%M:%S %p", time.localtime())
    log.write(Day+'\t\t'+Time+'\t\t'+string+'\n')
    log.close()

class TkThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        self.root = tk.Tk()
        #self.root.attributes("-fullscreen", True)

        self.root.protocol("WM_DELETE_WINDOW", self.exit_callback)
        #self.root.overrideredirect(True)
        self.root.geometry(str(scr_w)+"x"+str(scr_h))
        #self.root.geometry("{0}x{1}+0+0".format(str(scr_w),str(scr_h)))

        self.frames = {}
        for F in (GUI001, GUI002):
            page_name = F.__name__
            frame = F(parent=self.root, controller=self)

            self.frames[page_name] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

            exitButton = tk.Button(self.frames[page_name], bg=buttonBackGroundColor, activebackground=buttonActiveBackGroundColor, fg='white', font=('Helvetica', 20, 'bold'), \
            justify='center', text="X", command= self.exit_callback)
            exitButton.place(relx=0.95, rely=0.05, anchor="center")

        # start page

        self.show_frame("GUI001")

        self.select_page()
        self.root.config(background=backGroundColor)
        self.root.mainloop()

    def select_page(self):
        page_name = globalData.setCurrentScreen
        
        """
        EXEMPLO DE ATUALIZACAO EM TEMPO REAL DA PAGINA
        if page_name == "TELA":
            self.frames[page_name].METODO_DE_ATUALIZACAO()
        """
        self.show_frame(page_name)
        self.root.after(400, self.select_page)

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def rebuild_page(self, page_name):
        for widget in self.frames[page_name].winfo_children():
            widget.destroy()
        self.frames[page_name].page_build()

    def exit_callback(self):
        os._exit(0)

class GUI001(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.page_build()

    def page_build(self):
        setBackgroundLabel(self)
        
        #Titulo Principal
        title = tk.Label(self, text= "Guindaste", bg=backGroundColor, font=('Helvetica', 35, 'bold'))
        title.place(relx=0.5, rely=0.15, anchor="center")

        #Subtitulo
        subTitle = tk.Label(self, text= "Inicialização...", bg=backGroundColor, font=('Helvetica', 20))
        subTitle.place(relx=0.5, rely=0.30, anchor="center")

        #Id da tela
        subTitle = tk.Label(self, text= "GUI001", bg=backGroundColor, font=('Helvetica', 11))
        subTitle.place(relx=0.88, rely=0.95)

class GUI002(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.page_build()

    def page_build(self):
        setBackgroundLabel(self)

        #Titulo Principal
        title = tk.Label(self, text= "Guindaste", bg=backGroundColor, font=('Helvetica', 35, 'bold'))
        title.place(relx=0.5, rely=0.15, anchor="center")

        #Subtitulo
        subTitle = tk.Label(self, text= "FALHA DE INICIALIZAÇÃO.", foreground="red", bg=backGroundColor, font=('Helvetica', 20, 'bold'))
        subTitle.place(relx=0.5, rely=0.30, anchor="center")

        #Id da tela
        subTitle = tk.Label(self, text= "GUI002", bg=backGroundColor, font=('Helvetica', 11))
        subTitle.place(relx=0.88, rely=0.95)

if __name__ == "__main__":
    gui = TkThread()
    