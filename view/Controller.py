from time import sleep
import tkinter as tk
from tkinter import font as tkfont
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, IntVar, StringVar
from tracemalloc import start
import customtkinter
from tkinter.messagebox import showinfo
from turtle import onclick, width
from PIL import Image
from PIL import ImageTk
import threading
from pathlib import Path
import os
import time

from pygments import highlight

import globalData as globalData
from libs.Screen import center

background_color = "#121212"
control_background_color = "#262626"
text_color = "#F0F0F3"
transparent_color = "#915f07"
buttonbackground_color = "#003333"
buttonActivebackground_color = "#669999"

evt = threading.Event()

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def setBackgroundLabel(parent, BackGroundType=None):
    """Place background image on a label"""

    mySelfParent = parent

    if BackGroundType is not None:
        print(BackGroundType)
    BackGroundImage = Image.open(relative_to_assets("backgrond.png"))

    BackGroundImage = ImageTk.PhotoImage(BackGroundImage)
    background_label = tk.Label(
        parent, image=BackGroundImage, background=background_color)
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

        self.root.protocol("WM_DELETE_WINDOW", self.exit_callback)
        # self.root.overrideredirect(True)
        self.root.geometry("{}x{}+{}+{}".format(window_width,
                           window_height, x_cordinate, y_cordinate))
        # self.root.attributes("-fullscreen", True)

        # self.root.geometry("{0}x{1}+0+0".format(str(scr_w),str(scr_h)))

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
        # Titulo Principal
        # title = tk.Label(self, text= "QUAL GUINDASTE VOCÊ DESEJA CONTROLAR?", foreground="#313B3F", bg=background_color, font=("Inter Regular", 28))
        # title.place(x=280, y=40, width=890, height=130)

        # Titulo Principal
        title = tk.Label(self, text="Simulação", foreground=text_color,
                         bg=background_color, font=("Inter Regular", 64))
        title.place(x=162, y=488, width=465, height=90)
        title.bind("<Button-1>", self.simulation_click)

        # Subtitulo
        subTitle = tk.Label(self, text="Clique para começar com o Copelia",
                            foreground=text_color, bg=background_color, font=("Inter Regular", 16))
        subTitle.place(x=162, y=598, width=465, height=24)

        # Titulo Principal
        title = tk.Label(self, text="Físico", foreground=text_color,
                         bg=background_color, font=("Inter Regular", 64))
        title.place(x=1293, y=488, width=465, height=90)

        # Subtitulo
        subTitle = tk.Label(self, text="Clique para começar com o Arduino",
                            foreground=text_color, bg=background_color, font=("Inter Regular", 16))
        subTitle.place(x=1293, y=598, width=465, height=24)

        # Divisor
        # divisor = tk.Label(self, text= "", foreground="#313B3F", bg=background_color, font=("Inter Regular", 1), borderwidth=0.5, relief="solid")
        # divisor.place(x=724, y=504, width=2, height=240)


class GUI002(tk.Frame):
    # l1 = None
    # l2 = None
    rotation_variable = None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.page_build()
        self.rotation_variable = IntVar()

    def simulation_click(self, event):
        print(event)

    def popup_showinfo(self):
        showinfo("Window", "Hello World!")

    def rotation_command(self, event):
        print(event)

    def rotation_entry_callback(self):
        print(self.rotation_variable.get())
        return True

    def page_build(self):
        # Titulo Principal
        title = tk.Label(
            self,
            text="Guindaste Simulado",
            foreground=text_color,
            bg=background_color,
            font=("Inter Regular", 20))

        title.place(x=830, y=16, width=260, height=24)

        # Ellipse da telemetria
        ellipse_telemetry_image = Image.open(
            relative_to_assets("images/Ellipse 15.png"))
        ellipse_telemetry_image = ImageTk.PhotoImage(ellipse_telemetry_image)
        ellipse_telemetry_base = tk.Label(
            self,
            image=ellipse_telemetry_image,
            bg=background_color)
        ellipse_telemetry_base.image = ellipse_telemetry_image
        ellipse_telemetry_base.place(x=682, y=104)

        # Espaço da imagem
        component_1_image = Image.open(
            relative_to_assets("images/Component 1.png"))
        component_1_image = ImageTk.PhotoImage(component_1_image)
        component_1 = tk.Label(
            self,
            width=510,
            height=510,
            background=background_color,
            foreground=background_color,
            activebackground=background_color,
            image=component_1_image,
            bg=background_color)
        component_1.image = component_1_image
        component_1.place(x=701, y=123)

        # Retângulo dos controles
        rectangle_7_image = Image.open(
            relative_to_assets("images/Rectangle 7.png"))
        rectangle_7_image = ImageTk.PhotoImage(rectangle_7_image)
        rectangle_7 = tk.Label(
            self,
            image=rectangle_7_image,
            bg=background_color)
        rectangle_7.image = rectangle_7_image
        rectangle_7.place(x=254, y=758)

        # Retângulo da telemetria - altura
        height_telemetry_image = Image.open(
            relative_to_assets("images/Group 5.png"))
        height_telemetry_image = ImageTk.PhotoImage(height_telemetry_image)
        height_telemetry_base = tk.Label(
            self,
            image=height_telemetry_image,
            bg=background_color)
        height_telemetry_base.image = height_telemetry_image
        height_telemetry_base.place(x=1212, y=286)

        # Label do controle de rotação
        rotation_1_label = tk.Label(
            self,
            text="Rotação",
            foreground=text_color,
            bg=control_background_color,
            font=("Inter Regular", 16))
        rotation_1_label.place(x=1336, y=808, width=90, height=32)

        # Input do controle de rotação
        rotation_canva = customtkinter.CTkFrame(
            master=self,
            height=60,
            width=67,
            bg_color=control_background_color,
            fg_color=control_background_color,
            border_width=0,
            border_color=control_background_color)
        # frame_1.pack()
        rotation_canva.place(x=1246, y=817)

        rotation_entry = customtkinter.CTkEntry(
            master=rotation_canva,
            placeholder_text="0",
            height=30,
            width=67,
            border_width=0,
            border_color=control_background_color,
            text_font=("Inter Regular", 16),
            justify="center",
            fg_color=control_background_color,
            text_color=text_color,
            textvariable=self.rotation_variable,
            validate="focusout",
            validatecommand=self.rotation_entry_callback
        )

        rotation_entry.pack()

        rotation_metrics_label = tk.Label(
            self,
            text="graus",
            foreground=text_color,
            bg=control_background_color,
            font=("Inter Regular", 16))

        rotation_metrics_label.place(x=1246, y=842, width=67, height=30)
        # Slider da rotação
        rotation_slider = customtkinter.CTkSlider(
            master=self,
            from_=0,
            to=360,
            command=self.rotation_command,
            width=240,
            height=8,
            fg_color="#666666",
            progress_color="#E5E5E5",
            button_color="#E5E5E5",
            border_width=4,
            button_hover_color="#E5E5E5",
            bg_color="#262626",
            border_color="#262626",
            button_corner_radius=100,
            highlightthickness=0,
            corner_radius=0,
            bd=0
        )

        rotation_slider.set(0)
        rotation_slider.border_color = "#262626"
        rotation_slider.place(x=1338, y=846)

        # Label do controle de distância entre a ferramenta e o objeto
        tool_1_label = tk.Label(self, text="Distância", foreground=text_color,
                                bg=control_background_color, font=("Inter Regular", 16))
        tool_1_label.place(x=436, y=808, width=90, height=32)

        # Slider da distância
        distance_slider = customtkinter.CTkSlider(
            master=self,
            from_=0,
            to=1,
            command=None,
            width=240,
            height=8,
            fg_color="#666666",
            progress_color="#E5E5E5",
            button_color="#E5E5E5",
            border_width=4,
            button_hover_color="#E5E5E5",
            bg_color="#262626",
            border_color="#262626",
            button_corner_radius=100,
            highlightthickness=0,
            corner_radius=0,
            bd=0
        )

        distance_slider.set(0)
        distance_slider.border_color = "#262626"
        distance_slider.place(x=436, y=846)

        distance_canva = customtkinter.CTkFrame(
            master=self,
            height=60,
            width=67,
            bg_color=control_background_color,
            fg_color=control_background_color,
            border_width=0,
            border_color=control_background_color)
        # frame_1.pack()
        distance_canva.place(x=345, y=817)

        distance_entry = customtkinter.CTkEntry(
            master=distance_canva,
            placeholder_text="0",
            height=30,
            width=67,
            border_width=0,
            border_color=control_background_color,
            text_font=("Inter Regular", 16),
            justify="center",
            fg_color=control_background_color,
            text_color=text_color)

        distance_entry.pack()

        rotation_metrics_label = tk.Label(
            self,
            text="cm",
            foreground=text_color,
            bg=control_background_color,
            font=("Inter Regular", 16))

        rotation_metrics_label.place(x=345, y=842, width=67, height=30)

        # Botão liga e desliga o ímã
        magnet_image = Image.open(
            relative_to_assets("images/Group 15.png"))
        magnet_image = ImageTk.PhotoImage(magnet_image)
        magnet_button = tk.Button(
            self,
            image=magnet_image,
            bg=control_background_color,
            highlightthickness=0,
            bd=0,
            activebackground=control_background_color,
            activeforeground=control_background_color,
            borderwidth=0,
            justify="center",
            highlightbackground=control_background_color
        )

        magnet_button.image = magnet_image
        magnet_button.place(x=893, y=782)


if __name__ == "__main__":
    gui = TkThread()
