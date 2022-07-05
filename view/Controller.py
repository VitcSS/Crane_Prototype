from math import ceil
from time import sleep
import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
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

background_color = '#121212'
control_background_color = '#262626'
text_color = '#F0F0F3'

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path('./assets')


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


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

        self.root.protocol('WM_DELETE_WINDOW', self.exit_callback)
        self.root.geometry('{}x{}+{}+{}'.format(window_width,
                           window_height, x_cordinate, y_cordinate))

        self.frames = {}

        for F in (GUI001, GUI001, GUI002):
            page_name = F.__name__
            frame = F(parent=self.root, controller=self)
            frame.configure(background=background_color)

            self.frames[page_name] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Página inicial
        self.root.configure(background=background_color)
        self.show_frame('GUI001')
        self.select_page()
        self.root.mainloop()

    def select_page(self):
        page_name = globalData.telaSelecionada

        '''
        EXEMPLO DE ATUALIZACAO EM TEMPO REAL DA PAGINA
        if page_name == 'TELA':
            self.frames[page_name].METODO_DE_ATUALIZACAO()
        '''

        if page_name == 'GUI002':
            self.frames[page_name].update_telemetry()

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

    def select_simulation_page(self, event):
        globalData.dataInput = 'copelia'
        globalData.eventos.set()
        # globalData.telaSelecionada = "GUI002"

    def select_physical_page(self, event):
        globalData.dataInput = 'arduino'
        globalData.eventos.set()
        # globalData.telaSelecionada = "GUI002"

    def page_build(self):
        # Titulo Principal
        title = tk.Label(self, text='Simulação', foreground=text_color,
                         bg=background_color, font=('Inter Regular', 64))
        title.place(x=162, y=488, width=465, height=90)
        title.bind('<Button-1>', self.select_simulation_page)

        # Subtitulo
        subTitle = tk.Label(self, text='Clique para começar com o Copelia',
                            foreground=text_color, bg=background_color, font=('Inter Regular', 16))
        subTitle.place(x=162, y=598, width=465, height=24)

        # Titulo Principal
        title = tk.Label(self, text='Físico', foreground=text_color,
                         bg=background_color, font=('Inter Regular', 64))
        title.place(x=1293, y=488, width=465, height=90)
        title.bind('<Button-1>', self.select_physical_page)

        # Subtitulo
        subTitle = tk.Label(self, text='Clique para começar com o Arduino',
                            foreground=text_color, bg=background_color, font=('Inter Regular', 16))
        subTitle.place(x=1293, y=598, width=465, height=24)


class GUI002(tk.Frame):
    # l1 = None
    # l2 = None
    rotation_variable = 0
    distance_variable = 0
    is_magnet_active = None
    rotation = 0
    toy_distance = -30

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.page_build()
        self.rotation_variable = 0
        self.distance_variable = 0
        self.is_magnet_active = False

    def popup_showinfo(self):
        showinfo('Window', 'Hello World!')

    def rotation_command(self, position):
        self.rotation_variable = int(round(position, 0))
        self.rotation_metric['text'] = str(
            int(round(position, 0)))
        self.rotation_metric.update()

    def distance_command(self, distance):
        if (distance):
            self.distance_variable = int(round(distance, 0))
            self.distance_vertical_metric['text'] = str(
                int(round(distance, 0)))
            self.distance_vertical_metric.update()

    def change_magnet_image(self):
        if self.is_magnet_active == False:
            self.magnet_button.configure(image=self.active_magnet_image)
            self.magnet_button.photo = self.active_magnet_image
            self.magnet_button.image = self.active_magnet_image
            self.is_magnet_active = True
        else:
            self.magnet_button.configure(image=self.off_magnet_image)
            self.magnet_button.photo = self.off_magnet_image
            self.magnet_button.image = self.off_magnet_image
            self.is_magnet_active = False

        globalData.dataInput = 'atuar_ferramenta'
        globalData.dataInput2 = self.is_magnet_active

    def send_rotation_command(self):
        print("CLICADO ROTACAO")
        self.rotation = int(round(self.rotation_variable, 0))
        # self.actual_position_value['text'] = str(self.rotation)
        # self.actual_position_value.update()
        globalData.dataInput = 'rotacionar_torre'
        globalData.dataInput2 = self.rotation

    def send_toy_distance_command(self):
        self.toy_distance = int(round(self.distance_variable, 0))
        # self.actual_position_toy_value['text'] = str(
        #     int(round(self.toy_distance, 0)))
        # self.actual_position_toy_value.update()
        globalData.dataInput = 'mover_ferramenta'
        globalData.dataInput2 = self.toy_distance

    def update_telemetry(self):
        self.ultrasson_meter_value['text'] = str(globalData.distanceTool)
        self.actual_position_value['text'] = str(globalData.towerPosition)
        self.actual_position_toy_value['text'] = str(globalData.toolPosition)
        self.title['text'] = f'Guindaste {"simulado" if globalData.guindasteSelecionado.lower() == "copelia" else "físico"}'

    def back_to_menu(self):
        self.ultrasson_meter_value['text'] = '0'
        self.actual_position_value['text'] = '0'
        self.actual_position_toy_value['text'] = '0'
        globalData.dataInput = 'voltar_menu'

    def page_build(self):
        # Titulo Principal
        self.title_background_image = Image.open(
            relative_to_assets('images/Rectangle 6.png'))
        self.title_background_image = ImageTk.PhotoImage(
            self.title_background_image)
        self.title_background = tk.Label(
            self,
            image=self.title_background_image,
            bg='#262626')
        self.title_background.image = self.title_background_image
        self.title_background.place(x=0, y=0)

        self.back_to_menu_image = Image.open(
            relative_to_assets('images/arrow-down.png'))
        self.back_to_menu_image = ImageTk.PhotoImage(
            self.back_to_menu_image)
        self.back_to_menu_button = tk.Label(
            self,
            image=self.back_to_menu_image,
            bg='#262626')
        self.back_to_menu_button.image = self.back_to_menu_image
        self.back_to_menu_button.place(x=73.19, y=17)
        self.back_to_menu_button.bind(
            '<Button-1>', lambda e: self.back_to_menu())

        self.title = tk.Label(
            self,
            text=f'Guindaste {"simulado" if globalData.guindasteSelecionado == "COPELIA" else "físico"}',
            foreground=text_color,
            bg='#262626',
            font=('Inter Regular', 20))

        self.title.place(x=830, y=16, width=260, height=24)

        # Seção 3
        # Ellipse da telemetria
        self.ellipse_telemetry_image = Image.open(
            relative_to_assets('images/Group 18.png'))
        self.ellipse_telemetry_image = ImageTk.PhotoImage(
            self.ellipse_telemetry_image)
        self.ellipse_telemetry_base = tk.Label(
            self,
            image=self.ellipse_telemetry_image,
            bg=background_color)
        self.ellipse_telemetry_base.image = self.ellipse_telemetry_image
        self.ellipse_telemetry_base.place(x=278, y=104)

        # Espaço da imagem
        self.component_1_image = Image.open(
            relative_to_assets('images/Component 1.png'))
        self.component_1_image = ImageTk.PhotoImage(self.component_1_image)
        self.component_1 = tk.Label(
            self,
            width=143,
            height=143,
            image=self.component_1_image,
            bg='#D9D9D9')

        self.component_1.image = self.component_1_image
        self.component_1.place(x=885, y=305)

        self.ultrasson_meter_label = tk.Label(
            self,
            text='Medida do\nUltrassom',
            foreground=text_color,
            bg='#4C6CFD',
            font=('Inter Regular', 20))

        self.ultrasson_meter_label.place(x=322, y=346, width=130, height=72)

        self.ultrasson_meter_value = tk.Label(
            self,
            text='0',
            foreground=text_color,
            bg='#4C6CFD',
            font=('Inter Regular', 30))

        self.ultrasson_meter_value.place(x=509, y=352, width=62, height=60)

        self.ultrasson_meter_unit_meter = tk.Label(
            self,
            text='cm',
            foreground=text_color,
            bg='#4C6CFD',
            font=('Inter Regular', 14))

        self.ultrasson_meter_unit_meter.place(
            x=577, y=352, width=50, height=60)

        self.actual_position = tk.Label(
            self,
            text='Posição\ndo guindaste',
            foreground=text_color,
            bg='#4C6CFD',
            font=('Inter Regular', 20))

        self.actual_position.place(x=1260, y=296, width=178, height=72)

        self.actual_position_value = tk.Label(
            self,
            text='0',
            foreground=text_color,
            bg='#4C6CFD',
            font=('Inter Regular', 30))

        self.actual_position_value.place(x=1447, y=302, width=80, height=60)

        self.actual_position_unit_meter = tk.Label(
            self,
            text='graus',
            foreground=text_color,
            bg='#4C6CFD',
            font=('Inter Regular', 14))

        self.actual_position_unit_meter.place(
            x=1530, y=302, width=50, height=60)

        self.actual_position_toy = tk.Label(
            self,
            text='Posição\nda ferramenta',
            foreground=text_color,
            bg='#4C6CFD',
            font=('Inter Regular', 20))

        self.actual_position_toy.place(x=1260, y=385, width=178, height=72)

        self.actual_position_toy_value = tk.Label(
            self,
            text='0',
            foreground=text_color,
            bg='#4C6CFD',
            font=('Inter Regular', 30))

        self.actual_position_toy_value.place(
            x=1447, y=385, width=80, height=60)

        self.actual_position_toy_unit_meter = tk.Label(
            self,
            text='cm',
            foreground=text_color,
            bg='#4C6CFD',
            font=('Inter Regular', 14))

        self.actual_position_toy_unit_meter.place(
            x=1530, y=385, width=50, height=60)

        # Seção 2
        # Retângulo dos controles
        self.rectangle_7_image = Image.open(
            relative_to_assets('images/Rectangle 7.png'))
        self.rectangle_7_image = ImageTk.PhotoImage(self.rectangle_7_image)
        self.rectangle_7 = tk.Label(
            self,
            image=self.rectangle_7_image,
            bg=background_color)
        self.rectangle_7.image = self.rectangle_7_image
        self.rectangle_7.place(x=254, y=758)

        # Botão de play
        self.send_rotation_image = Image.open(
            relative_to_assets('images/ButtonPlay.png'))
        self.send_rotation_image = ImageTk.PhotoImage(self.send_rotation_image)
        self.send_rotation_button = tk.Button(
            self,
            image=self.send_rotation_image,
            bg=control_background_color,
            highlightthickness=0,
            bd=0,
            activebackground=control_background_color,
            activeforeground=control_background_color,
            justify='center',
            highlightbackground=control_background_color,
            relief=SUNKEN,
            width=56,
            height=56,
            command=self.send_rotation_command
        )

        self.send_rotation_button.place(x=1550, y=820)

        # Label do controle de rotação
        self.rotation_1_label = tk.Label(
            self,
            text='Rotação',
            foreground=text_color,
            bg=control_background_color,
            font=('Inter Regular', 16))
        self.rotation_1_label.place(x=1280, y=808, width=90, height=32)

        self.rotation_metric = tk.Label(
            self,
            text=self.rotation_variable,
            foreground=text_color,
            bg=control_background_color,
            font=('Inter Regular', 16))

        self.rotation_metric.place(x=1175, y=812, width=90, height=32)

        self.rotation_metrics_label = tk.Label(
            self,
            text='graus',
            foreground=text_color,
            bg=control_background_color,
            font=('Inter Regular', 16))

        self.rotation_metrics_label.place(x=1188, y=842, width=67, height=30)

        # Slider da rotação
        self.rotation_slider = customtkinter.CTkSlider(
            master=self,
            from_=-180,
            to=180,
            command=self.rotation_command,
            width=240,
            height=8,
            fg_color='#666666',
            progress_color='#E5E5E5',
            button_color='#E5E5E5',
            border_width=4,
            button_hover_color='#E5E5E5',
            bg_color='#262626',
            border_color='#262626',
            button_corner_radius=100,
            highlightthickness=0,
            corner_radius=0,
            bd=0,
            borderwidth=0,
            relief=SUNKEN
        )

        self.rotation_slider.set(0)
        self.rotation_slider.border_color = '#262626'
        self.rotation_slider.place(x=1280, y=846)

        # Seção 1
        # Botão que envia a distância
        self.send_distance_image = Image.open(
            relative_to_assets('images/ButtonPlay.png'))
        self.send_distance_image = ImageTk.PhotoImage(self.send_distance_image)
        self.send_distance_button = tk.Button(
            self,
            image=self.send_distance_image,
            bg=control_background_color,
            highlightthickness=0,
            bd=0,
            activebackground=control_background_color,
            activeforeground=control_background_color,
            borderwidth=0,
            justify='center',
            highlightbackground=control_background_color,
            relief=SUNKEN,
            width=56,
            height=56,
            command=self.send_toy_distance_command
        )

        self.send_distance_button.place(x=325, y=820)

        # Label do controle de distância entre a ferramenta e o objeto
        self.tool_1_label = tk.Label(self, text='Distância', foreground=text_color,
                                     bg=control_background_color, font=('Inter Regular', 16))
        self.tool_1_label.place(x=400, y=808, width=90, height=32)

        # Slider da distância
        self.distance_slider = customtkinter.CTkSlider(
            master=self,
            from_=-27,
            to=27,
            command=self.distance_command,
            width=240,
            height=8,
            fg_color='#666666',
            progress_color='#E5E5E5',
            button_color='#E5E5E5',
            border_width=4,
            button_hover_color='#E5E5E5',
            bg_color='#262626',
            border_color='#262626',
            button_corner_radius=100,
            highlightthickness=0,
            corner_radius=0,
            bd=0
        )

        self.distance_slider.set(0)
        self.distance_slider.border_color = '#262626'
        self.distance_slider.place(x=400, y=846)

        # Valor da distância

        self.distance_vertical_metric = tk.Label(
            self,
            text=0,
            foreground=text_color,
            bg=control_background_color,
            font=('Inter Regular', 16))

        self.distance_vertical_metric.place(x=665, y=812, width=67, height=30)

        self.distance_metrics_label = tk.Label(
            self,
            text='cm',
            foreground=text_color,
            bg=control_background_color,
            font=('Inter Regular', 16))

        self.distance_metrics_label.place(x=665, y=842, width=67, height=30)

        # Botão liga e desliga o ímã
        self.off_magnet_image = Image.open(
            relative_to_assets('images/BotaoImaDesligado.png'))

        self.off_magnet_image = ImageTk.PhotoImage(self.off_magnet_image)

        self.active_magnet_image = Image.open(
            relative_to_assets('images/BotaoImaLigado.png'))

        self.active_magnet_image = ImageTk.PhotoImage(self.active_magnet_image)

        self.magnet_button = tk.Button(
            self,
            image=self.off_magnet_image,
            bg=control_background_color,
            highlightthickness=0,
            bd=0,
            activebackground=control_background_color,
            activeforeground=control_background_color,
            borderwidth=0,
            justify='center',
            highlightbackground=control_background_color,
            command=self.change_magnet_image,
            # relief=SUNKEN
        )

        self.magnet_button.image = self.off_magnet_image
        self.magnet_button.place(x=894, y=782)


if __name__ == '__main__':
    gui = TkThread()
