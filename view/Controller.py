from time import sleep
import tkinter as tk
from tkinter import font as tkfont
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from turtle import onclick
from PIL import Image
from PIL import ImageTk
import threading
from pathlib import Path
import os
import time

import globalData as globalData
from libs.Screen import center

background_color = "#121212"
text_color = "#F0F0F3"
transparent_color = "#915f07"
buttonbackground_color = "#003333"
buttonActivebackground_color = "#669999"

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
    background_label = tk.Label(parent, image=BackGroundImage, background=background_color)
    background_label.place(relx=0, y=0, relheight=1, relwidth=1)
    parent.img = BackGroundImage

def measureslog(string):
    log = open("log_measures.txt", "a")
    Day = time.strftime("%m-%d-%Y", time.localtime())
    Time = time.strftime("%I:%M:%S %p", time.localtime())
    log.write(Day+"\t\t"+Time+"\t\t"+string+"\n")
    log.close()

class TkThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
        
    def run(self):
        self.root = tk.Tk()
        window_height = 1080
        window_width = 1920
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))

        #self.root.attributes("-fullscreen", True)

        self.root.protocol("WM_DELETE_WINDOW", self.exit_callback)
        #self.root.overrideredirect(True)
        self.root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        #self.root.geometry("{0}x{1}+0+0".format(str(scr_w),str(scr_h)))

        self.frames = {}
        for F in (GUI001, GUI001, GUI002):
            page_name = F.__name__
            frame = F(parent=self.root, controller=self)
            frame.configure(background=background_color)

            self.frames[page_name] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

            # exitButton = tk.Button(self.frames[page_name], bg=buttonbackground_color, activebackground=buttonActivebackground_color, fg="white", font=("Helvetica", 20, "bold"), \
            # justify="center", text="X", command= self.exit_callback)
            # exitButton.place(relx=0.95, rely=0.05, anchor="center")

        # start page
        self.root.configure(background=background_color)
        self.show_frame("GUI001")
        self.select_page()
        self.root.mainloop()

    def select_page(self):
        page_name = globalData.tela_selecionada
        
        """
        EXEMPLO DE ATUALIZACAO EM TEMPO REAL DA PAGINA
        if page_name == "TELA":
            self.frames[page_name].METODO_DE_ATUALIZACAO()
        """
        self.show_frame(page_name)
        self.root.after(400, self.select_page)

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
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
        
    def simulation_click(self, event):
        print(event)
        globalData.tela_selecionada = "GUI002"

    def page_build(self):
        #Titulo Principal
        # title = tk.Label(self, text= "QUAL GUINDASTE VOCÊ DESEJA CONTROLAR?", foreground="#313B3F", bg=background_color, font=("Inter Regular", 28))
        # title.place(x=280, y=40, width=890, height=130)
        
        #Titulo Principal
        title = tk.Label(self, text= "Simulação", foreground=text_color, bg=background_color, font=("Inter Regular", 64))
        title.place(x=162, y=488, width=465, height=90)
        title.bind("<Button-1>", self.simulation_click)

        #Subtitulo
        subTitle = tk.Label(self, text= "Clique para começar com o Copelia", foreground=text_color, bg=background_color, font=("Inter Regular", 16))
        subTitle.place(x=162, y=598, width=465, height=24)
        
        #Titulo Principal
        title = tk.Label(self, text= "Físico", foreground=text_color, bg=background_color, font=("Inter Regular", 64))
        title.place(x=1293, y=488, width=465, height=90)

        #Subtitulo
        subTitle = tk.Label(self, text= "Clique para começar com o Arduino", foreground=text_color, bg=background_color, font=("Inter Regular", 16))
        subTitle.place(x=1293, y=598, width=465, height=24)
        
        #Divisor
        # divisor = tk.Label(self, text= "", foreground="#313B3F", bg=background_color, font=("Inter Regular", 1), borderwidth=0.5, relief="solid")
        # divisor.place(x=724, y=504, width=2, height=240)

class GUI002(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.page_build()
        
    def simulation_click(self, event):
        print(event)

    def page_build(self):     
        #Titulo Principal
        title = tk.Label(self, text= "Guindaste Simulado", foreground=text_color, bg=background_color, font=("Inter Regular", 20))
        title.place(x=918, y=14, width=260, height=24)
        title.bind("<Button-2>", self.simulation_click)        
        w1 = tk.Scale(self, from_=0, to=360, tickinterval=1)
        w1.place(x=918, y= 56)


if __name__ == "__main__":
    gui = TkThread()
    