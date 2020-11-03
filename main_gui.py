#!/usr/bin/env python3
# -*- coding: utf-8 -*-
_author_ = 'David Lizarazo'
__copyright__  = "Copyright 2020"
__credits__    = [" David Lizarazo"]
__version__    = "1.0.2"
__maintainer__ = "David Lizarazo"
__email__      = "davidlizarazovesga@hotmail.com"
__status__     = "Production"


import os
import sys
import Cython
import math
import multiprocessing 
import py_compile                           #To enable wich file must be compile
import threading                            #To create threads
import signals  
import signal                               #Used to enable the key interrupt.


import urllib.request   as url
import tkinter          as tk
from   tkinter          import ttk
from   time             import sleep
from   multiprocessing  import Value
from   datetime         import datetime      #To get the moment when QR is scanned
from   PIL              import Image, ImageTk

import module.constants as CONS

#Salidas del Rapsberry :
# - Salida para los Sensores
# - Entrada para los sensores 
# - Usb de la camara 
# - Serial para la Bascula 
# - Entrada de Voltaje 

# Variables GLobales
State_config = False
State_connection = False

"""
State_Configuration = Value('i',-1)
State_Changed       = Value('b',False)
dead                = Value('b',False)
screen_dead         = Value('b',False)
"""
#stop_for_sc     = threading.Lock()

# Definicion de interrupciones para finalizr el programa 
def keyboardInterruptHandler(signal, frame):
    print('KeyboardInterrupt (ID: {})'.format(signal))
    print ("Preview Exit(0)")
    exit(0)


signal.signal(signal.SIGINT, keyboardInterruptHandler)
signal.signal(signal.SIGTERM, keyboardInterruptHandler)


#Fonts
Title_font   = ("Aharoni", 40 , "bold")
Subtitle_font= ("Aharoni", 20 , "bold")
Text_font    = ("Aharoni", 20 )

Button_font  = ("Aharoni", 15 , "bold")

NORM_FONT    = ("Verdana", 10)
SMALL_FONT   = ("Verdana", 8)


# File Importan Path
filename = sys.argv[0]
pathname = os.path.dirname(filename)        
full_path = os.path.abspath(pathname)

index_module = full_path.find('module')
if index_module != -1 :
    cache_folder = full_path[:index_module]+'cache'
else :
    cache_folder = full_path + '/cache'

def popupmsg(title="Hey!" , msg= "Holi"):
    popup = tk.Tk()
    popup.wm_title(title)
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)

    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()


"""
 ___
|   |        _     __  
|===|  |  | | \ | |  | 
|   |  |__| |_/ | |__|
"""
class ThreadForSounds(threading.Thread):
    def __init__(self,group=None,target=None,name=None,  action=None,nameID ='Unicornio'):
        super().__init__(group=group,target=target,name=name)
        self.__nameID   = nameID 
        self.__action   = action
        self.__isrunning= False

    def run(self):
        pass
        """
        self.__isrunning=True
        if self.__action == 'read':          # QR detected
            LEDS.gpio_read()
            self.__isrunning=False
            return
        if self.__action == 'val':          # HIT
            LEDS.gpio_accepted()
            self.__isrunning=False
            return
        if self.__action == 'init':         # INIT SOUND
            LEDS.salute_qr('Estóy listo!',conn_state)
            self.__isrunning=False
            return
        if self.__action =='noval':         # NO HIT
            LEDS.gpio_reject()
            self.__isrunning=False
            return
        if self.__action == 'speak' :       # Speak
            LEDS.salute_qr(self.__nameID,conn_state)
            self.__isrunning=False
        if self.__action == 'config':      # GPIO CONFIGURATION
            signals.Decoding.send(__name__)
            LEDS.gpio_conf(LOGIC_ON='LOW')
            LEDS.gpio_init()
        self.__isrunning=False
        """

    @property
    def is_running(self):
        return self.__isrunning


class Connection_Conf():
    def __init__(self):
        print (CONS.bcolors.HEADER+"Connection Started"+CONS.bcolors.ENDC)

    def __check_connection(self):
        try:   url.urlopen("http://google.com")
        except url.URLError :   return False
        else:                   return True

    def check_connection(self):
        print ("Conectado?")
        if self.__check_connection():
            self.__popupmsg("Conectado")
        else :
            self.__popupmsg("Desconecatdo")

    def check_API(self):
        print ("API?")
        self.__popupmsg("AYIOH")

            
    def __popupmsg(self,msg):
        popup = tk.Tk()
        popup.wm_title("Mensaje de Conexión")
        label = ttk.Label(popup, text=msg, font=NORM_FONT)
        label.pack(side="top", fill="x", pady=10)

        B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
        B1.pack()
        popup.mainloop()

class GUI(tk.Tk):
    def __init__(self, *args , **kwargs):
        global cache_folder
        icon = cache_folder+'/frubana_logo.png'
        image_frubana = cache_folder+'/frubana.png'

        tk.Tk.__init__(self)
        
        self.width = self.winfo_screenwidth()
        self.height= self.winfo_screenheight()
        self.iconphoto(False ,tk.PhotoImage(file=icon))
        self.wm_title("Frubana Peso")
        self.geometry("%dx%d" % (self.width, self.height))

        image = Image.open(image_frubana)
        image = ImageTk.PhotoImage(image)
        self.bg_label = tk.Label(self, image = image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_label.image = image

        # Initialize style
        style = ttk.Style()
        style.configure('TFrame', background='white')

        style.configure("Principal.TButton", padding=15, relief="raised" , borderwidth=3 , foreground="#F8AC18" , 
                        width = 30 , height = 20,
                        background="white" ,  font = Button_font , highlightbackground = "#F8AC18")
        # style.configure("TButton", padding=20, relief="raised" , borderwidth=3 , foreground="#F8AC18" , 
        #                 background="white" ,  font = Button_font , highlightbackground = "#F8AC18")

        style.configure("Tittle.TLabel" , background="white" , font=Title_font , foreground="#F8AC18" )
        style.configure("SubTittle.TLabel" , background="white" , font=Subtitle_font , foreground="#F8AC18" )
        style.configure("BlackSubTittle.TLabel" , background="white" , font=Subtitle_font , foreground="black" )
        # style.configure("TButton", padding=6, relief="sunken",background="#F8AC18")
        
        container = tk.Frame(self)
        container.pack(side="top" , fill="both" , expand= True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)




        self.__frames = {}

        for my_frames in (StartPage, Conf_WIFI , Admin_Data, Config_Canas, Weigh_Initial ):
            frame = my_frames(container, self)
            self.__frames[my_frames] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

        

        # Main Menu Bar 
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff =0 )
        filemenu.add_command(label="Save settings", command = lambda: popupmsg(title="Not supported" , msg="Not supported just yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        self.class_connection = Connection_Conf()

        
        exchangeChoice = tk.Menu(menubar, tearoff=1)
        
        exchangeChoice.add_command(label="Mostrar Redes",   command=lambda: self.class_connection.check_connection())
        exchangeChoice.add_command(label="Verifica Conexión",   command=lambda: self.class_connection.check_connection())
        exchangeChoice.add_command(label="Verifica API",        command=lambda: self.class_connection.check_API() )

        menubar.add_cascade(label="Conexión", menu=exchangeChoice)

        tk.Tk.config(self, menu=menubar)

    def show_frame(self, cont):
        frame = self.__frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self,parent)

        self.__controller = controller

        # --  Get Images --
        
        image_limonsin = Image.open(cache_folder+'/limonsin.png')
        image_limonsin = image_limonsin.resize((100,100), Image.ANTIALIAS)
        image_limonsin = ImageTk.PhotoImage(image_limonsin)

        image_conf = Image.open(cache_folder+'/config.png')
        image_conf = image_conf.resize((50,50), Image.ANTIALIAS)
        image_conf = ImageTk.PhotoImage(image_conf)

        image_admin = Image.open(cache_folder+'/principal_page/admin_db.png')
        image_admin = image_admin.resize((450,450), Image.ANTIALIAS)
        image_admin = ImageTk.PhotoImage(image_admin)

        image_start = Image.open(cache_folder+'/principal_page/star_process.png')
        image_start = image_start.resize((450,450), Image.ANTIALIAS)
        image_start = ImageTk.PhotoImage(image_start)
        

        # -- Buttons --

        button_conf = ttk.Button(self, image=image_conf  , style="Principal.TButton" , # background="white" ,
                            command=lambda: self.define_configuration_page())
        button_conf.image = image_conf
        button_conf.place(relx=0.88,rely=0.015)

        button1 = ttk.Button(self, text="Aministra Complementos",  style="Principal.TButton" ,
                            command=lambda: self.define_configuration_page())
        button1.place(relx=0.20,rely=0.75)
        
        button2 = ttk.Button(self, text="Proceso de Pesaje", style="Principal.TButton",
                            command=lambda: self.__controller.show_frame(Weigh_Initial))
        button2.state(["disabled"])
        button2.place(relx=0.6,rely=0.75)

        # -- Labels --
         
        labeltitle  = ttk.Label(self, text="Recibo", style="Tittle.TLabel" )
        labeltitle.place(relx =0.08 , rely=0.015)
        labeltitle2 = ttk.Label(self, text="en bodega", style="SubTittle.TLabel")
        labeltitle2.place(relx=0.08 , rely=0.085)
        labeltitle2 = ttk.Label(self, text="Seleccione que poroceso iniciar : ", style="BlackSubTittle.TLabel")
        labeltitle2.place(relx=0.08 , rely=0.155)


        label_limonsin = tk.Label(self, image = image_limonsin, borderwidth=0)
        label_limonsin.place(relx= 0.012 , rely= 0.018)
        label_limonsin.image = image_limonsin

        label_im_admin = tk.Label(self, image = image_admin,    borderwidth=0)
        label_im_admin.place(relx= 0.20 , rely= 0.2)
        label_im_admin.image = image_admin
 
        label_im_start = tk.Label(self, image = image_start ,   borderwidth=0)
        label_im_start.place(relx= 0.60 , rely= 0.2)
        label_im_start.image = image_start

    def define_configuration_page(self):
        global State_config
        if not State_config : 
            print (CONS.bcolors.FAIL+"No esta configuraro"+CONS.bcolors.ENDC)
            self.__controller.show_frame(Conf_WIFI)
        else:
            print (CONS.bcolors.FAIL+"Configuraro"+CONS.bcolors.ENDC)
            self.__controller.show_frame(Admin_Data)

class Conf_WIFI(tk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self,parent)

        self.__controller = controller
        self.__val_data  = "disabled"
        self.__change_button = False

        # --  Get Images --
        
        image_limonsin = Image.open(cache_folder+'/limonsin.png')
        image_limonsin = image_limonsin.resize((100,100), Image.ANTIALIAS)
        image_limonsin = ImageTk.PhotoImage(image_limonsin)

        image_home = Image.open(cache_folder+'/carbon_home.png')
        image_home = image_home.resize((50,50), Image.ANTIALIAS)
        image_home = ImageTk.PhotoImage(image_home)

        image_wifi = Image.open(cache_folder+'/wifi.png')
        image_wifi = image_wifi.resize((50,50), Image.ANTIALIAS)
        image_wifi = ImageTk.PhotoImage(image_wifi)

        # -- Buttons --

        button_home = ttk.Button(self, image=image_home  , style="Principal.TButton" , # background="white" ,
                            command=lambda: controller.show_frame(StartPage))
        button_home.image = image_home
        button_home.place(relx= 0.90 , rely= 0.018)
        

        self.save = ttk.Button(self, text="Guardar Configuracion", style="Principal.TButton",
                            command=lambda: self.save_ssid_data() )
        self.save.state([self.__val_data])
        self.save.place(relx=0.40,rely=0.75)

        # -- Labels --
         
        labeltitle  = ttk.Label(self, text="Configuracion WIFI ", style="Tittle.TLabel" )
        labeltitle.place(relx =0.08 , rely=0.015)

        labeltitle2 = ttk.Label(self, text="Inserte nombre de red y contraseña : ", style="BlackSubTittle.TLabel")
        labeltitle2.place(relx=0.08 , rely=0.085)


        label_limonsin = tk.Label(self, image = image_limonsin, borderwidth=0)
        label_limonsin.place(relx= 0.012 , rely= 0.018)
        label_limonsin.image = image_limonsin
 
        label_im_wifi = tk.Label(self, image = image_wifi , borderwidth=0 , background="white")
        label_im_wifi.place(relx= 0.350 , rely= 0.35)
        label_im_wifi.image = image_wifi

        # -- INPUTS --
        reg = controller.register(self.callback)

        labeltitle_name = ttk.Label(self, text="Nombre (SSID) : ", style="BlackSubTittle.TLabel")
        labeltitle_name.place(relx=0.4 , rely=0.35)

        self.name_ssid = tk.Entry(self)
        self.name_ssid.place(relx=0.4 , rely=0.4)
        self.name_ssid.config(width = 50 , validate="key" )

        labeltitle_pass = ttk.Label(self, text="Contraseña : ", style="BlackSubTittle.TLabel")
        labeltitle_pass.place(relx=0.4 , rely=0.5)

        self.password = tk.Entry(self)
        self.password.place(relx=0.4 , rely=0.55)        
        self.password.config(show="*" , width = 50 , validate="key" , validatecommand=( reg ,'%P' ))


    def callback(self, valor):
        if len(self.password.get()) > 3   and   len(self.name_ssid.get()) > 3 :
            if self.__change_button:
                return True  
            self.save.state(["!disabled"])
            self.__change_button = True

        else :
            if self.__change_button:
                self.save.state(["disabled"])
                self.__change_button = False
        return True 

    def save_ssid_data(self):
        global State_config 

        self.__wpa_config = False
        name     = self.name_ssid.get()
        password = self.password.get()

        try:
            os.system('sudo chmod 666 /etc/wpa_supplicant/wpa_supplicant.conf')
            with open("/etc/wpa_supplicant/wpa_supplicant.conf", "a+") as supplicant:
                supplicant.write("\n network={ \n    ssid='%s' \n    psk='%s' \n} \n " %(name,password))
                State_config = True

        except Exception as e:
            print(CONS.bcolors.FAIL+'Error_Ocurred seting the wpa_supplicant {}'.format(e)+CONS.bcolors.ENDC)

        try:
           os.system('sudo chmod 644 /etc/wpa_supplicant/wpa_supplicant.conf')
           self.__wpa_config = True
        except Exception as e:
           print (CONS.bcolors.FAIL+'Error reestoring permitions on wpa_supplicant'+CONS.bcolors.ENDC)

        if self.__wpa_config : 

           __local_con = """INSERT INTO info (ssid,password) VALUES ('{}' , '{}' ) """.format(CONS.IDevice)
           print (__local_con)
           #self.__localdb = SQL.LocalDBConsumption(databasename="device.db")
           #self.__location_info = self.__localdb.consult(__local_con)
           #self.__localdb.close_connection()

        popupmsg(title="Wifi" , msg="Red Wifi Guardada")



class Admin_Data(tk.Frame):

    def __init__(self, parent, controller):
        
        ttk.Frame.__init__(self, parent)
        
        # -- Labels Tittles --
         
        labeltitle2 = ttk.Label(self, text="Configuracion de contenedores ", style="Tittle.TLabel")
        labeltitle2.place(relx=0.08 , rely=0.055)
        labeltitle2 = ttk.Label(self, text="Tipologías : ", style="BlackSubTittle.TLabel")
        labeltitle2.place(relx=0.08 , rely=0.135)

        labeltitle_canas = ttk.Label(self, text="Canastilla ", style="BlackSubTittle.TLabel")
        labeltitle_canas.place(relx=0.12 , rely=0.25)
        
        labeltitle_canas = ttk.Label(self, text="Estibas ", style="BlackSubTittle.TLabel")
        labeltitle_canas.place(relx=0.42 , rely=0.25)
        
        labeltitle_canas = ttk.Label(self, text="Gato ", style="BlackSubTittle.TLabel")
        labeltitle_canas.place(relx=0.72 , rely=0.25)


        # --  Get Images --
        image_home = Image.open(cache_folder+'/b_house.png')
        image_home = Image.open(cache_folder+'/carbon_home.png')
        image_home = image_home.resize((50,50), Image.ANTIALIAS)
        image_home = ImageTk.PhotoImage(image_home)

        image_canastillas = Image.open(cache_folder+'/canastillas/base.png')
        image_canastillas = image_canastillas.resize((300,300), Image.ANTIALIAS)
        image_canastillas = ImageTk.PhotoImage(image_canastillas)

        image_estibas = Image.open(cache_folder+'/estibas/estibas.jpg')
        image_estibas = image_estibas.resize((300,300), Image.ANTIALIAS)
        image_estibas = ImageTk.PhotoImage(image_estibas)

        image_gato = Image.open(cache_folder+'/gatos/gato.jpg')
        image_gato = image_gato.resize((300,300), Image.ANTIALIAS)
        image_gato = ImageTk.PhotoImage(image_gato)
        
        # -- Buttons --
        button_home = ttk.Button(self, image=image_home  , style="Principal.TButton" , # background="white" ,
                            command=lambda: controller.show_frame(StartPage))
        button_home.image = image_home
        button_home.place(relx= 0.012 , rely= 0.055)
        

        button_canas = ttk.Button(self, text="Seleccionar",  style="Principal.TButton" ,
                            command=lambda: controller.show_frame(Admin_Data))
        button_canas.place(relx=0.08,rely=0.75)

        button_estibas = ttk.Button(self, text="Seleccionar", style="Principal.TButton",
                            command=lambda: controller.show_frame(Weigh_Initial))
        button_estibas.place(relx=0.38,rely=0.75)
        
        button_gato = ttk.Button(self, text="Seleccionar", style="Principal.TButton",
                            command=lambda: controller.show_frame(Weigh_Initial))
        button_gato.place(relx=0.68,rely=0.75)

        # -- Labels Images --
        
        label_im_canas = tk.Label(self, image = image_canastillas,    borderwidth=0)
        label_im_canas.place(relx= 0.10 , rely= 0.35)
        label_im_canas.image = image_canastillas
 
        label_im_estibas = tk.Label(self, image = image_estibas ,   borderwidth=0)
        label_im_estibas.place(relx= 0.40 , rely= 0.35)
        label_im_estibas.image = image_estibas

        label_im_gato = tk.Label(self, image = image_gato ,   borderwidth=0)
        label_im_gato.place(relx= 0.70 , rely= 0.35)
        label_im_gato.image = image_gato

class Config_Canas(tk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Page Two!!!", style="Tittle.TLabel" )
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(Admin_Data))
        button2.pack()
        
class Weigh_Initial(tk.Frame):

    def __init__(self, parent, controller):
        
        ttk.Frame.__init__(self, parent)

        
        # --  Get Images --
        image_home = Image.open(cache_folder+'/b_house.png')
        image_home = image_home.resize((50,50), Image.ANTIALIAS)
        image_home = ImageTk.PhotoImage(image_home)

        image_canastillas = Image.open(cache_folder+'/canastillas/base.png')
        image_canastillas = image_canastillas.resize((300,300), Image.ANTIALIAS)
        image_canastillas = ImageTk.PhotoImage(image_canastillas)

        image_estibas = Image.open(cache_folder+'/estibas/estibas.jpg')
        image_estibas = image_estibas.resize((300,300), Image.ANTIALIAS)
        image_estibas = ImageTk.PhotoImage(image_estibas)

        image_gato = Image.open(cache_folder+'/gatos/gato.jpg')
        image_gato = image_gato.resize((300,300), Image.ANTIALIAS)
        image_gato = ImageTk.PhotoImage(image_gato)
        
        # -- Labels Tittles --
         
        labeltitle2 = ttk.Label(self, text="Configuracion de contenedores ", style="Tittle.TLabel")
        labeltitle2.place(relx=0.08 , rely=0.055)
        labeltitle2 = ttk.Label(self, text="Tipologías : ", style="BlackSubTittle.TLabel")
        labeltitle2.place(relx=0.08 , rely=0.135)


        # -- Buttons --
        button_home = ttk.Button(self, image=image_home  , style="Principal.TButton" , # background="white" ,
                            command=lambda: controller.show_frame(StartPage))
        button_home.image = image_home
        button_home.place(relx= 0.012 , rely= 0.055)


        label = ttk.Label(self, text="Page Two!!!", style="Tittle.TLabel" )
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(Admin_Data))
        button2.pack()
        

def main():
    

    # CALL INTI CLASS
    app = GUI()
    app.mainloop()
    


if __name__ == "__main__":
    os.system('clear')
    print (CONS.IDevice)
    print ("*** FRUBANA BEGINS ***") 
    print (CONS.bcolors.CIAN+ "Folder {}".format(cache_folder)+ CONS.bcolors.ENDC)

    main()
    # Call the main configuraiton 



# ************  INPUTS ************

# e = ttk.Entry(midIQ)
# e.insert(0,10)
# e.pack()
# e.focus_set()

# Last tutorial I saw
#https://pythonprogramming.net/object-oriented-programming-crash-course-tkinter/?completed=/tkinter-depth-tutorial-making-actual-program/