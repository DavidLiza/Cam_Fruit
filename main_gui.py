#!/usr/bin/env python3
# -*- coding: utf-8 -*-
_author_ = 'David Lizarazo'
__copyright__  = "Copyright 2020"
__credits__    = [" David Lizarazo"]
__version__    = "1.0.2"
__maintainer__ = "David Lizarazo"
__email__      = "davidlizarazovesga@hotmail.com"
__status__     = "Production"


# TODOS
# - Implementar el modulo de inicial 
# - Crear pop up para cuando se guarda la configiuracion 
# - Redireccionar Pantalla despues del Wifi 
# - Cada que se entra a pagina inicial , chequear conectividad


import os
import sys
import Cython
import math
import multiprocessing 
import py_compile                           #To enable wich file must be compile
import threading                            #To create threads
import signals  
import signal                               #Used to enable the key interrupt.


import barcode
import urllib.request   as url
import tkinter          as tk
from   tkinter          import ttk
from   time             import sleep
from   multiprocessing  import Value
from   datetime         import datetime      #To get the moment when QR is scanned
from   PIL              import Image, ImageTk
from   io               import BytesIO

import module.constants as CONS
import module.decodeModule      as decM    #To desencipt the QR information 
import module.gpioModule        as LEDS    #To enable and play GPIOS connected
import module.my_requests       as API    #To make the request to the servers
import module.databaseConsume   as SQL     #To consum the database 

#Salidas del Rapsberry :
# - Salida para los Sensores
# - Entrada para los sensores 
# - Usb de la camara 
# - Serial para la Bascula 
# - Entrada de Voltaje 

# Variables GLobales
State_config     = False
State_connection = False
screen_height    = 0
screen_width     = 0

canas_exists     = False
estibas_exists   = False

"""
State_Configuration = Value('i',-1)
State_Changed       = Value('b',False)
dead                = Value('b',False)
screen_dead         = Value('b',False)

sudo apt install matchbox-keyboard
matchbox-keyboard


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
Title_font   = ("Aharoni", 50 , "bold")
Subtitle_font= ("Aharoni", 30 , "bold")
Text_font    = ("Aharoni", 20 )

Pop_Up_Font_T = ("Aharoni", 30 , "bold")
Pop_Up_Font_R = ("Aharoni", 20 )

Button_font  = ("Aharoni", 25 , "bold")

NORM_FONT    = ("Verdana", 20)
SMALL_FONT   = ("Verdana", 18)


# File Importan Path
filename = sys.argv[0]
pathname = os.path.dirname(filename)        
full_path = os.path.abspath(pathname)

index_module = full_path.find('module')
if index_module != -1 :
    cache_folder = full_path[:index_module]+'cache'
else :
    cache_folder = full_path + '/cache'

def call_keyboard (event) :
    print ("Call To Keyboiard")
    #os.system("matchbox-keyboard")

def popupmsg(title="Hey!" , msg= "Holi"):
    global screen_height
    global screen_width

    popup = tk.Tk()

    popup.wm_title(title )
    popup.geometry("{}x{}+{}+{}".format (int(screen_width*0.35) ,
                                           int(screen_height*0.25),
                                           int(screen_width*0.37),
                                           int(screen_height*0.37) ))

    label = ttk.Label(popup, text=msg, font=Subtitle_font)
    label.pack(side="top",expand =True , pady=10)

    B1 = tk.Button(popup ,text="Okay", font=Subtitle_font , command = popup.destroy )
    B1.config( width=25 , foreground="#F8AC18"  )
    B1.pack(ipady=30 , pady=30 ,  padx=18)
    popup.mainloop()

def Testing():
    pass
    #config_bluetooth()

class Connection_Conf():
    def __init__(self):
        print (CONS.bcolors.HEADER+"Connection Started"+CONS.bcolors.ENDC)

    def internal__check_connection(self):
        global State_connection
        try:   url.urlopen("http://google.com")
        except url.URLError :  
            State_connection = False
            return State_connection
        else: # Conectado a Internet 
            State_connection = True
            return State_connection

    def check_connection(self):
        print ("Conectado?")
        if self.internal__check_connection():
            popupmsg(title="Estado de conexion" ,msg ="Conectado")
        else :
            popupmsg(title="Estado de conexion" ,msg = "Desconecatdo")

    def check_API(self):
        print ("API?")
        popupmsg(title="Estado de conexion" ,msg ="AYIOH")


# *********************************************************
# ************************ MAIN ***************************
# *********************************************************

class GUI(tk.Tk):
    def __init__(self, *args , **kwargs):
        global screen_height
        global screen_width
        global cache_folder

        icon = cache_folder+'/frubana_logo.png'
        image_frubana = cache_folder+'/frubana.png'

        tk.Tk.__init__(self)
        
        self.class_connection = Connection_Conf()
        print ("State connection {}".format(self.class_connection.internal__check_connection()))
        
        screen_height = self.winfo_screenheight()
        screen_width  = self.winfo_screenwidth()

        print ("W {} , H {} ".format(screen_width, screen_height))
        self.iconphoto(False ,tk.PhotoImage(file=icon))
        self.wm_title("Frubana Peso")
        self.geometry("%dx%d" % (screen_width, screen_height))

        image = Image.open(image_frubana)
        image = ImageTk.PhotoImage(image)
        self.bg_label = tk.Label(self, image = image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_label.image = image

        # -- Initialize styles --
        style = ttk.Style()
        style.configure('TFrame', background='white')

        style.configure("Principal.TButton" , relief="raised" , borderwidth=3 , foreground="#F8AC18" , 
                        width = 30 , padding=12 , pady=100 ,
                        background="white" ,  font = Button_font , highlightbackground = "#F8AC18")
        
        style.configure("Secundary.TButton" , relief="raised" , borderwidth=3 , foreground="#F8AC18" , 
                        width = 20 , padding=8 , pady=100 ,
                        background="white" ,  font = Button_font , highlightbackground = "#F8AC18")

        style.configure("Tittle.TLabel" , background="white" , font=Title_font , foreground="#F8AC18" )
        style.configure("SubTittle.TLabel" , background="white" , font=Subtitle_font , foreground="#F8AC18" )
        style.configure("BlackSubTittle.TLabel" , background="white" , font=Subtitle_font , foreground="black" )
        style.configure("RedSubTittle.TLabel"   , background="white" , font=Subtitle_font , foreground="red" )
        style.configure("GreenSubTittle.TLabel" , background="white" , font=Subtitle_font , foreground="green" )


        container = tk.Frame(self)
        container.pack(side="top" , fill="both" , expand= True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # -- Frames --
        self.__frames = {}
        for my_frames in (  StartPage, 
                            Add_WIFI, 
                            Admin_wifis,
                            Admin_Data, 
                            Config_Canas, 
                            Config_Estibas, 
                            Weigh_Initial,
                            Weigh_Result ):

            frame = my_frames(container, self)
            self.__frames[my_frames] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)


        # -- Main Menu Bar --
        menubar = tk.Menu(container)
        menubar.config(font=Text_font)
        
        menubar.add_command(label="\u0020", activebackground=menubar.cget("background"))
        filemenu = tk.Menu(menubar, tearoff =0 )
        filemenu.add_separator()
        filemenu.add_command(label="Test",          font=Text_font,  command= lambda: self.show_frame(Admin_wifis) )
        filemenu.add_separator()
        filemenu.add_command(label="Exit",          font=Text_font,  command=quit)
        filemenu.add_separator()
        menubar.add_cascade (label="System",   menu=filemenu)

        menubar.add_command(label="\u0020", activebackground=menubar.cget("background"))
        menubar.add_command(label="\u22EE", activebackground=menubar.cget("background"))
        menubar.add_command(label="\u0020", activebackground=menubar.cget("background"))

        exchangeChoice = tk.Menu(menubar, tearoff=1)
        exchangeChoice.add_command(label="Mostrar Redes WIFI",    font= Text_font, command=lambda: self.show_frame(Admin_wifis))
        exchangeChoice.add_separator()
        exchangeChoice.add_command(label="Admin Contenedores",font= Text_font, command=lambda: self.show_frame(Admin_Data))
        exchangeChoice.add_separator()
        exchangeChoice.add_command(label="Verifica Conexión",font= Text_font, command=lambda: self.class_connection.check_connection())
        exchangeChoice.add_separator()
        exchangeChoice.add_command(label="Verifica API",     font= Text_font, command=lambda: self.class_connection.check_API() )
        exchangeChoice.add_separator()
        exchangeChoice.add_command(label="Admin Bluetooths",        font= Text_font, command=lambda: config_bluetooth() )
        menubar.add_cascade(label="Conexiónes", menu=exchangeChoice)

        tk.Tk.config(self, menu=menubar)

    def show_frame(self, cont):
        frame = self.__frames[cont]
        try:
            frame.update_frame()
        except Exception as e:
            print ("Este Frame no tiene la funcion UPDATE {}".format(cont))
            print ("Error {}".format(e))
        frame.tkraise()

# *********************************************************
# *********************** FRAMES **************************
# *********************************************************

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        global State_config
        ttk.Frame.__init__(self,parent)
        self.__controller = controller

        # --  Get Images --
        image_limonsin = Image.open(cache_folder+'/limonsin.png')
        image_limonsin = image_limonsin.resize((150,150), Image.ANTIALIAS)
        image_limonsin = ImageTk.PhotoImage(image_limonsin)

        image_conf = Image.open(cache_folder+'/config.png')
        image_conf = image_conf.resize((80,80), Image.ANTIALIAS)
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

        button1 = ttk.Button(self, text="Administra Complementos",  style="Principal.TButton" ,
                            command=lambda: self.define_configuration_page())
        button1.place(relx=0.12,rely=0.8 ,  height=120 )
        
        self.__butt_pesaje = ttk.Button(self, text="Proceso de Pesaje", style="Principal.TButton",
                            command=lambda: self.__controller.show_frame(Weigh_Initial))
        self.__butt_pesaje.place(relx=0.52,rely=0.8 ,  height=120 )
       
        # -- Labels --
        labeltitle  = ttk.Label(self, text="Recibo", style="Tittle.TLabel" )
        labeltitle.place(relx =0.1 , rely=0.015)
        labeltitle2 = ttk.Label(self, text="en bodega", style="SubTittle.TLabel")
        labeltitle2.place(relx=0.1 , rely=0.085)
        labeltitle2 = ttk.Label(self, text="Seleccione que poroceso iniciar : ", style="BlackSubTittle.TLabel")
        labeltitle2.place(relx=0.1 , rely=0.155)

        label_limonsin = tk.Label(self, image = image_limonsin, borderwidth=0)
        label_limonsin.place(relx= 0.012 , rely= 0.018)
        label_limonsin.image = image_limonsin

        label_im_admin = tk.Label(self, image = image_admin,    borderwidth=0)
        label_im_admin.place(relx= 0.20 , rely= 0.23)
        label_im_admin.image = image_admin
 
        label_im_start = tk.Label(self, image = image_start ,   borderwidth=0)
        label_im_start.place(relx= 0.60 , rely= 0.23)
        label_im_start.image = image_start

    def define_configuration_page(self):
        global State_connection

        if not State_connection : 
            print (CONS.bcolors.FAIL+"No esta configurado"+CONS.bcolors.ENDC)
            
            action = """SELECT * FROM wifis ;"""
            __localdb = SQL.LocalDBConsumption(databasename="device.db")
            __location_info = __localdb.consult(action,modification=True)
            __localdb.close_connection()

            if not __location_info: self.__controller.show_frame(Add_WIFI)
            else :                  self.__controller.show_frame(Admin_wifis)

        else:
            print (CONS.bcolors.FAIL+"Configurado"+CONS.bcolors.ENDC)
            self.__controller.show_frame(Admin_Data)

    def update_frame(self):
        global canas_exists
        global estibas_exists

        self.define_configuration_page()  

        if canas_exists and estibas_exists:     self.__butt_pesaje.state(["!disabled"])
        else :                                  self.__butt_pesaje.state(["disabled"])
        
class Add_WIFI(tk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self,parent)
        print ("Conf Wifi ")
        self.__controller = controller
        self.__val_data  = "disabled"
        self.__change_button = False

        # --  Get Images --
        image_limonsin = Image.open(cache_folder+'/limonsin.png')
        image_limonsin = image_limonsin.resize((150,150), Image.ANTIALIAS)
        image_limonsin = ImageTk.PhotoImage(image_limonsin)

        image_home = Image.open(cache_folder+'/carbon_home.png')
        image_home = image_home.resize((100,100), Image.ANTIALIAS)
        image_home = ImageTk.PhotoImage(image_home)

        image_wifi = Image.open(cache_folder+'/wifi.png')
        image_wifi = image_wifi.resize((75,75), Image.ANTIALIAS)
        image_wifi = ImageTk.PhotoImage(image_wifi)

        # -- Buttons --
        button_home = ttk.Button(self, image=image_home  , style="Principal.TButton" , # background="white" ,
                            command=lambda:  self.__controller.show_frame(StartPage))
        button_home.image = image_home
        button_home.place(relx= 0.90 , rely= 0.018)
        

        self.save = ttk.Button( self, text="Guardar Configuracion", style="Principal.TButton",
                                command=lambda: self.save_ssid_data() )
        self.save.state([self.__val_data])
        self.save.place(relx=0.312,rely=0.75 , height=120)

        # -- Labels --
        labeltitle  = ttk.Label(self, text="Configuracion WIFI ", style="Tittle.TLabel" )
        labeltitle.place(relx =0.1 , rely=0.015)

        labeltitle2 = ttk.Label(self, text="Inserte nombre de red y contraseña : ", style="BlackSubTittle.TLabel")
        labeltitle2.place(relx=0.1 , rely=0.085)

        label_limonsin = tk.Label(self, image = image_limonsin, borderwidth=0)
        label_limonsin.place(relx= 0.012 , rely= 0.018)
        label_limonsin.image = image_limonsin
 
        label_im_wifi = tk.Label(self, image = image_wifi , borderwidth=0 , background="white")
        label_im_wifi.place(relx= 0.300 , rely= 0.25)
        label_im_wifi.image = image_wifi

        # -- INPUTS --
        reg = controller.register(self.callback)
        labeltitle_name = ttk.Label(self, text="Nombre (SSID) : ", style="BlackSubTittle.TLabel")
        labeltitle_name.place(relx=0.4 , rely=0.25)

        self.name_ssid = tk.Entry(self , font="Aharoni 20")
        self.name_ssid.place(relx=0.4 , rely=0.32 ,  width=400, height=60)
        self.name_ssid.config(width = 50 , validate="key" )

        labeltitle_pass = ttk.Label(self, text="Contraseña : ", style="BlackSubTittle.TLabel")
        labeltitle_pass.place(relx=0.4 , rely=0.39)

        self.password = tk.Entry(self , font="Aharoni 20" )
        self.password.place(relx=0.4 , rely=0.46 , width=400, height=60)        
        self.password.config(show="*" , width = 50 , validate="key" , validatecommand=( reg ,'%P' ))

        self.name_ssid.bind("<1>", call_keyboard)
        self.password.bind("<1>", call_keyboard)

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

    def wifi_error(self,error):
        print (CONS.bcolors.FAIL + "Error {}".format(error) + CONS.bcolors.ENDC)
        popupmsg(title="Error Wifi" , msg="Verifique la informacion")

    def save_ssid_data(self):
        global State_connection 

        __wpa_config = False
        name     = self.name_ssid.get()
        password = self.password.get()

        try:
            action = """INSERT INTO wifis (ssid , password) 
                        VALUES ( '{}' , '{}' ) ;""".format(name,password)
            self.__localdb = SQL.LocalDBConsumption(databasename="device.db")
            self.__location_info = self.__localdb.consult(action,modification=True)
            self.__localdb.close_connection()

            if not self.__location_info:
                __wpa_config = False
                self.wifi_error(error= "Wifi already exists")
                return 
            __wpa_config = True

        except Exception as e:
            self.wifi_error(error= "Wifi already exists")
            return 

        if __wpa_config : 
            try:
                os.system('sudo chmod 666 /etc/wpa_supplicant/wpa_supplicant.conf')
                with open("/etc/wpa_supplicant/wpa_supplicant.conf", "a+") as supplicant:
                    supplicant.write("\nnetwork={ \n    ssid='%s' \n    psk='%s' \n} \n " %(name,password))
                State_connection = True
            except Exception as e:
                self.wifi_error(error="WPA supplicant Error")
                return

            try:
                os.system('sudo chmod 644 /etc/wpa_supplicant/wpa_supplicant.conf')
                __wpa_config = True
            except Exception as e:
                self.wifi_error(error="WPA back error")
                return


        self.__controller.show_frame(StartPage)
        popupmsg(title="Wifi" , msg="Red Wifi Guardada")
        #Reload WPA services
        os.system('sudo systemctl daemon-reload')
        os.system('sudo systemctl restart dhcpcd')

    def update_frame(self):
        self.name_ssid.delete(0, 'end')
        self.password.delete(0, 'end')

class Admin_wifis(tk.Frame):

    def __init__(self, parent, controller):
        
        ttk.Frame.__init__(self, parent)
        self.__controller = controller 
        self.__wpa_file   = "/etc/wpa_supplicant/wpa_supplicant.conf"
        # --  Get Images --
        image_limonsin = Image.open(cache_folder+'/limonsin.png')
        image_limonsin = image_limonsin.resize((150,150), Image.ANTIALIAS)
        image_limonsin = ImageTk.PhotoImage(image_limonsin)

        image_home = Image.open(cache_folder+'/carbon_home.png')
        image_home = image_home.resize((90,90), Image.ANTIALIAS)
        image_home = ImageTk.PhotoImage(image_home)

        image_wifi = Image.open(cache_folder+'/wifi.png')
        image_wifi = image_wifi.resize((75,75), Image.ANTIALIAS)
        image_wifi = ImageTk.PhotoImage(image_wifi)
        
        # -- Labels Tittles --
         
        label_limonsin = tk.Label(self, image = image_limonsin, borderwidth=0)
        label_limonsin.place(relx= 0.010 , rely= 0.055)
        label_limonsin.image = image_limonsin

        label_im_wifi = tk.Label(self, image = image_wifi , borderwidth=0 , background="white")
        label_im_wifi.place(relx= 0.05 , rely= 0.225)
        label_im_wifi.image = image_wifi

        label_title = ttk.Label(self, text="Administrar Redes ", style="Tittle.TLabel")
        label_title.place(relx=0.08 , rely=0.055)
        label_subtitle = ttk.Label(self, text="WIFIS ", style="BlackSubTittle.TLabel")
        label_subtitle.place(relx=0.08 , rely=0.135)

        label_redes = ttk.Label(self, text="Redes Guardadas: ", style="BlackSubTittle.TLabel")
        label_redes.place(relx=0.08 , rely=0.25)

        label_canastillas = ttk.Label(self, text="Seleccionada: ", style="BlackSubTittle.TLabel")
        label_canastillas.place(relx=0.5 , rely=0.25)

        self.__counter_can = 0
        self.__counter_pal = 0

        num_canastillas = ttk.Label(self, text="Cantidad: ", style="BlackSubTittle.TLabel")
        num_canastillas.place(relx=0.08 , rely=0.75)


        # -- Entryes Cantidad --
        self.__entry_can = tk.Entry(self ,font="Aharoni 20" )
        self.__entry_can.insert(0," ")
        self.__entry_can.config(state="disabled")
        self.__entry_can.place(height= 60, width= 400 , relx=0.5 , rely=0.35)

        # -- Lista Box --
        self.lista_box = tk.Listbox( self , 
                                highlightcolor="#F8AC18" , 
                                highlightbackground="#ffffff",
                                selectborderwidth=5 , 
                                font=Pop_Up_Font_R)
        self.lista_box.place(height= 300, width= 600 , relx =0.08 , rely = 0.35 )
        self.lista_box.bind('<<ListboxSelect>>', self.onselect)
        #self.get_redes()

        # -- Buttons --
        button_home = ttk.Button(self, image=image_home  , style="Principal.TButton" , # background="white" ,
                            command=lambda: self.__controller.show_frame(StartPage))
        button_home.image = image_home
        button_home.place(relx= 0.88 , rely= 0.055)


        button_start = ttk.Button(self, text="Eliminar Red",  style="Secundary.TButton" ,
                            command=lambda: self.__delete_red() )
        button_start.place(relx=0.50 , rely=0.45 , height=100)

        button_start = ttk.Button(self, text="Nueva red",  style="Secundary.TButton" ,
                            command=lambda: self.__controller.show_frame(Add_WIFI))
        button_start.place(relx=0.08 , rely=0.75 , height=100) 

    def onselect(self,evt):
        w = evt.widget
        index_value = int(w.curselection()[0])
        print ('You selected item %d: "%s"' % (index_value,  w.get(index_value) ))

        self.__entry_can.config(state='normal')
        self.__entry_can.delete(0,tk.END)
        self.__entry_can.insert(0,str(w.get(index_value)))
        self.__entry_can.config(state='disabled')

    def wifi_error(self,error):
        print (CONS.bcolors.FAIL + "Error {}".format(error) + CONS.bcolors.ENDC)
        popupmsg(title="Error Wifi" , msg=error)

    def __delete_red(self):
        index_value   = int(self.lista_box.curselection()[0])
        ssid_name     = self.lista_box.get(index_value)

        accion = """DELETE FROM wifis WHERE ssid='{}' """.format(ssid_name)
        __localdb = SQL.LocalDBConsumption(databasename= "device.db")
        __redes   = __localdb.consult(lite_consult=accion , modification=True)
        __localdb.close_connection()
        print ("Done {}".format(__redes))

        try:
            os.system('sudo chmod 666 {}'.format(self.__wpa_file))
            with open(self.__wpa_file) as supplicant:
                lines=supplicant.readlines()
                cont = 0 
                for word in lines:
                    if "{}".format(ssid_name) in word:
                        break
                    cont += 1
                supplicant.close()

            cont = cont-1
            print (lines[cont])
            print (lines[cont+1])


            for x in range(4):
                lines.pop(cont)
                
            with open(self.__wpa_file , "w") as supplicant:
                new_file_contents = "".join(lines)
                supplicant.write(new_file_contents)
                supplicant.close()

        except Exception as e:
            print (CONS.bcolors.OKBLUE+e+CONS.bcolors.ENDC)
            self.wifi_error(error="WPA supplicant Error")
            return

        try:
            os.system('sudo chmod 644 {}'.format(self.__wpa_file))
            __wpa_config = True
        except Exception as e:
            self.wifi_error(error="WPA back error")
            return
        print ("Se elimino ")
        self.__controller.show_frame(Admin_wifis)

    def get_redes (self):
            
        accion = """SELECT ssid FROM wifis;"""
        __localdb = SQL.LocalDBConsumption(databasename= "device.db")
        __redes   = __localdb.consult(lite_consult=accion , modification=False)
        __localdb.close_connection()

        if not __redes:
            self.__controller.show_frame(Add_WIFI)
            self.wifi_error(error="No hay redes guardadas")
        else:
            for wifis in __redes:
                print (wifis)
                self.lista_box.insert(tk.END,wifis[0])

    def update_frame(self):
        self.get_redes()
        print ("Actualizacion del Frame Admin Wifi ")


# ************************************************************
# ******************** CONFIGURATION *************************
# ************************************************************

class Admin_Data(tk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        
        # -- Labels Tittles --
         
        labeltitle = ttk.Label(self, text="Configuracion de contenedores ", style="Tittle.TLabel")
        labeltitle.place(relx=0.1 , rely=0.055)
        labeltitle2 = ttk.Label(self, text="Tipologías : ", style="BlackSubTittle.TLabel")
        labeltitle2.place(relx=0.1 , rely=0.135)

        labeltitle_canas = ttk.Label(self, text="Canastilla ", style="BlackSubTittle.TLabel")
        labeltitle_canas.place(relx=0.12 , rely=0.25)
        
        labeltitle_canas = ttk.Label(self, text="Estibas ", style="BlackSubTittle.TLabel")
        labeltitle_canas.place(relx=0.42 , rely=0.25)
        
        labeltitle_canas = ttk.Label(self, text="Gato ", style="BlackSubTittle.TLabel")
        labeltitle_canas.place(relx=0.72 , rely=0.25)


        # --  Get Images --
        image_home = Image.open(cache_folder+'/carbon_home.png')
        image_home = image_home.resize((90,90), Image.ANTIALIAS)
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

        image_wifi = Image.open(cache_folder+'/wifi.png')
        image_wifi = image_wifi.resize((300,300), Image.ANTIALIAS)
        image_wifi = ImageTk.PhotoImage(image_wifi)
        
        # -- Buttons --
        button_home = ttk.Button(self, image=image_home  , style="Principal.TButton" , # background="white" ,
                            command=lambda: controller.show_frame(StartPage))
        button_home.image = image_home
        button_home.place(relx=0.012,rely= 0.055)
        

        button_canas = ttk.Button(self, text="Seleccionar",  style="Secundary.TButton" ,
                            command=lambda: controller.show_frame(Config_Canas))
        button_canas.place(relx=0.05,rely=0.75 ,    height=100)

        button_estibas = ttk.Button(self, text="Seleccionar", style="Secundary.TButton",
                            command=lambda: controller.show_frame(Config_Estibas))
        button_estibas.place(relx=0.35,rely=0.75 ,  height=100)
        
        button_gato = ttk.Button(self, text="Seleccionar", style="Secundary.TButton",
                            command=lambda: controller.show_frame(Config_Estibas))
        button_gato.place(relx=0.64,rely=0.75 ,     height=100)

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

    def update_frame(self):
        # No es necesari actualizar nada en este Frame
        print ("Actualizacion del Frame Admin Data ")

class Config_Canas(tk.Frame):

    def __init__(self, parent, controller):
        
        ttk.Frame.__init__(self, parent)
        self.__controller = controller
        self.__pinted = False
        self.__get_canastillas()
        
        # --  Get Images --
        image_home = Image.open(cache_folder+'/back_row.png')
        image_home = image_home.resize((90,90), Image.ANTIALIAS)
        image_home = ImageTk.PhotoImage(image_home)

        # -- Labels Tittles --
        labeltitle = ttk.Label(self, text="Configuracion de canastillas ", style="Tittle.TLabel")
        labeltitle.place(relx=0.1 , rely=0.055)
        labeltitle2 = ttk.Label(self, text="Tipologías : ", style="SubTittle.TLabel")
        labeltitle2.place(relx=0.1 , rely=0.135)


        labeltitle_canas = ttk.Label(self, text="Canastilla ", style="BlackSubTittle.TLabel")
        labeltitle_canas.place(relx=0.12 , rely=0.25)

        # -- Buttons --

        button_canas = ttk.Button(self, text="Añadir ",  style="Principal.TButton" ,
                            command=lambda: self.__add_canas() )
        button_canas.place(relx=0.08,rely=0.75)
 
        button_home = ttk.Button(self, image=image_home  , style="Principal.TButton" , # background="white" ,
                            command=lambda: self.__controller.show_frame(Admin_Data))
        button_home.image = image_home
        button_home.place(relx= 0.012 , rely= 0.055)

    def show_cont (self ):
        
        if  canas_exists and not self.__pinted : 

            self.label_canastillas = ttk.Label(self, text="Canastillas Guardadas: ", style="BlackSubTittle.TLabel")
            self.label_canastillas.place(relx=0.08 , rely=0.25)

            self.label_selecc = ttk.Label(self, text="Seleccionada: ", style="BlackSubTittle.TLabel")
            self.label_selecc.place(relx=0.5 , rely=0.25)


            # -- Entryes Cantidad --
            self.__entry_can = tk.Entry(self ,font="Aharoni 20" )
            self.__entry_can.insert(0," ")
            self.__entry_can.config(state="disabled")
            self.__entry_can.place(height= 60, width= 400 , relx=0.5 , rely=0.35)

            # -- Lista Box --
            
            self.lista_box = tk.Listbox( self , 
                                    highlightcolor="#F8AC18" , 
                                    highlightbackground="#ffffff",
                                    selectborderwidth=5 , 
                                    font=Pop_Up_Font_R)
            self.lista_box.place(height= 300, width= 600 , relx =0.08 , rely = 0.35 )
            self.lista_box.bind('<<ListboxSelect>>', self.onselect)

            self.button_delete = ttk.Button(self, text="Eliminar Red",  style="Secundary.TButton" ,
                                command=lambda: self.__delete_cont() )
            self.button_delete.place(relx=0.50 , rely=0.45 , height=100)
        
            self.__pinted = True 

        if self.__pinted:
            self.lista_box.delete(0, tk.END)
            for canastillas in self.__canastillas : 
                print (canastillas)
                self.lista_box.insert(tk.END,canastillas[1])

    def onselect(self,evt):
        w = evt.widget
        index_value = int(w.curselection()[0])
        print ('You selected item %d: "%s"' % (index_value,  w.get(index_value) ))

        self.__entry_can.config(state='normal')
        self.__entry_can.delete(0,tk.END)
        self.__entry_can.insert(0,str(w.get(index_value)))
        self.__entry_can.config(state='disabled')

    def __delete_cont(self):
        index_value   = int(self.lista_box.curselection()[0])
        ssid_id     = self.lista_box.get(index_value)


        for canastillas in self.__canastillas:
            if ssid_id == canastillas[1]:
                ssid_id = canastillas[0]
                break

        accion = """DELETE FROM canastillas WHERE code_id= {} """.format(ssid_id)
        __localdb = SQL.LocalDBConsumption(databasename= "contenedores.db")
        __redes   = __localdb.consult(lite_consult=accion , modification=True)
        __localdb.close_connection()

        print (accion)
        self.__controller.show_frame(Config_Canas)

    def __add_canas (self):
        config_popup(title="Configurar Canastillas", tipo="canastillas" , frames_controller=self.__controller)

    def __get_canastillas(self):
        global canas_exists
        accion = """SELECT * FROM canastillas"""
        __localdb = SQL.LocalDBConsumption(databasename= "contenedores.db")
        self.__canastillas = __localdb.consult(lite_consult=accion , modification=False)
        __localdb.close_connection()

        if not self.__canastillas:
            canas_exists = False
        else:
            canas_exists = True

    def update_frame(self):

        self.__get_canastillas()
        if not self.__canastillas :
            label_db = ttk.Label(self, text="Sin Canastillas", style="BlackSubTittle.TLabel")
            label_db.place(relx=0.15 , rely=0.4)
            
            if self.__pinted : 
                
                self.label_canastillas.destroy()
                self.label_selecc.destroy()
                self.__entry_can.destroy()
                self.lista_box.destroy()
                self.button_delete.destroy()

                self.__pinted =  False
                print (CONS.bcolors.FAIL + "Eliminar el resto de contenedores " +CONS.bcolors.ENDC)

        else : 
            try:
                self.lista_box.select_clear()
            except :
                print ("Seleccione este ")
            self.show_cont()

class Config_Estibas(tk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        
        self.__controller = controller
        self.__pinted     = False
        self.__get_estibas()
        # --  Get Images --
        image_home = Image.open(cache_folder+'/back_row.png')
        image_home = image_home.resize((90,90), Image.ANTIALIAS)
        image_home = ImageTk.PhotoImage(image_home)
 
        # -- Labels Tittles --
        labeltitle = ttk.Label(self, text="Configuracion de estibas ", style="Tittle.TLabel")
        labeltitle.place(relx=0.1 , rely=0.055)
        labeltitle2 = ttk.Label(self, text="Tipologías : ", style="SubTittle.TLabel")
        labeltitle2.place(relx=0.1 , rely=0.135)

        
        labeltitle_canas = ttk.Label(self, text="Estibas ", style="BlackSubTittle.TLabel")
        labeltitle_canas.place(relx=0.12 , rely=0.25)
        
        if not self.__get_estibas():
            label_db = ttk.Label(self, text="Sin Estibas", style="BlackSubTittle.TLabel")
            label_db.place(relx=0.15 , rely=0.4)

        # -- Buttons --
        button_home = ttk.Button(self, image=image_home  , style="Principal.TButton" , # background="white" ,
                            command=lambda: controller.show_frame(Admin_Data)  )
        button_home.image = image_home
        button_home.place(relx= 0.012 , rely= 0.055)
        

        button_add = ttk.Button(self, text="Agregar",  style="Principal.TButton" ,
                            command=lambda: self.__add_estibas() )
        button_add.place(relx=0.08,rely=0.75)


    def show_cont (self ):

        if  estibas_exists and not self.__pinted : 
            self.label_estibas = ttk.Label(self, text="Estibas Guardadas: ", style="BlackSubTittle.TLabel")
            self.label_estibas.place(relx=0.08 , rely=0.25)

            self.label_selecc = ttk.Label(self, text="Seleccionada: ", style="BlackSubTittle.TLabel")
            self.label_selecc.place(relx=0.5 , rely=0.25)


            # -- Entryes Cantidad --
            self.__entry_can = tk.Entry(self ,font="Aharoni 20" )
            self.__entry_can.insert(0," ")
            self.__entry_can.config(state="disabled")
            self.__entry_can.place(height= 60, width= 400 , relx=0.5 , rely=0.35)

            # -- Lista Box --
            
            self.lista_box = tk.Listbox( self , 
                                    highlightcolor="#F8AC18" , 
                                    highlightbackground="#ffffff",
                                    selectborderwidth=5 , 
                                    font=Pop_Up_Font_R)
            self.lista_box.place(height= 300, width= 600 , relx =0.08 , rely = 0.35 )
            self.lista_box.bind('<<ListboxSelect>>', self.onselect)

            self.button_delete = ttk.Button(self, text="Eliminar Red",  style="Secundary.TButton" ,
                                command=lambda: self.__delete_cont() )
            self.button_delete.place(relx=0.50 , rely=0.45 , height=100)
            self.__pinted = True 

        if self.__pinted:
            self.lista_box.delete(0, tk.END)
            for canastillas in self.__estibas : 
                print (canastillas)
                self.lista_box.insert(tk.END,canastillas[1])

    def onselect(self,evt):
        w = evt.widget
        index_value = int(w.curselection()[0])
        print ('You selected item %d: "%s"' % (index_value,  w.get(index_value) ))

        self.__entry_can.config(state='normal')
        self.__entry_can.delete(0,tk.END)
        self.__entry_can.insert(0,str(w.get(index_value)))
        self.__entry_can.config(state='disabled')

    def __delete_cont(self):
        index_value   = int(self.lista_box.curselection()[0])
        cont_id     = self.lista_box.get(index_value)


        for estibas in self.__estibas:
            if cont_id == estibas[1]:
                cont_id = estibas[0]
                break

        accion = """DELETE FROM estibas WHERE code_id= {} """.format(cont_id)
        __localdb = SQL.LocalDBConsumption(databasename= "contenedores.db")
        __redes   = __localdb.consult(lite_consult=accion , modification=True)
        __localdb.close_connection()

        self.__controller.show_frame(Config_Estibas)

    def __add_estibas(self):
        config_popup(title="Configurar Estibas", tipo="estibas" , frames_controller=self.__controller)

    def __get_estibas(self):
        global estibas_exists
        accion = """SELECT * FROM estibas"""
        __localdb = SQL.LocalDBConsumption(databasename= "contenedores.db")
        self.__estibas = __localdb.consult(lite_consult=accion , modification=False)
        __localdb.close_connection()

        if not self.__estibas:
            estibas_exists = False
        else:
            estibas_exists = True
    
    def update_frame(self):
        self.__get_estibas()
        if not self.__estibas :
            label_db = ttk.Label(self, text="Sin Estibas", style="BlackSubTittle.TLabel")
            label_db.place(relx=0.15 , rely=0.4)
            
            if self.__pinted : 
                
                self.label_estibas.destroy()
                self.label_selecc.destroy()
                self.__entry_can.destroy()
                self.lista_box.destroy()
                self.button_delete.destroy()

                self.__pinted =  False
        else : 
            
            try:
                self.lista_box.select_clear()
            except:
                print ("Doone")
            self.show_cont()

class Weigh_Initial(tk.Frame):

    def __init__(self, parent, controller):
        
        ttk.Frame.__init__(self, parent)
        self.__controller = controller 
        # --  Get Images --
        image_limonsin = Image.open(cache_folder+'/limonsin.png')
        image_limonsin = image_limonsin.resize((150,150), Image.ANTIALIAS)
        image_limonsin = ImageTk.PhotoImage(image_limonsin)

        image_home = Image.open(cache_folder+'/carbon_home.png')
        image_home = image_home.resize((90,90), Image.ANTIALIAS)
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
         
        label_limonsin = tk.Label(self, image = image_limonsin, borderwidth=0)
        label_limonsin.place(relx= 0.010 , rely= 0.055)
        label_limonsin.image = image_limonsin

        label_title = ttk.Label(self, text="Proceso de Pesaje ", style="Tittle.TLabel")
        label_title.place(relx=0.08 , rely=0.055)
        label_subtitle = ttk.Label(self, text="Seleccione los contenedores: ", style="BlackSubTittle.TLabel")
        label_subtitle.place(relx=0.08 , rely=0.135)

    
        label_canastillas = ttk.Label(self, text="Tipo de canastilla: ", style="BlackSubTittle.TLabel")
        label_canastillas.place(relx=0.08 , rely=0.25)

        label_palets = ttk.Label(self, text="Tipo de Estibas: ", style="BlackSubTittle.TLabel")
        label_palets.place(relx=0.50 , rely=0.25)

        self.__counter_can = 0
        self.__counter_pal = 0

        num_canastillas = ttk.Label(self, text="Cantidad: ", style="BlackSubTittle.TLabel")
        num_canastillas.place(relx=0.08 , rely=0.75)

        num_palets      = ttk.Label(self, text="Cantidad: ", style="BlackSubTittle.TLabel")
        num_palets.place(relx=0.50 , rely=0.75)

        # -- Entryes Cantidad --
        self.__entry_can = tk.Entry(self ,font="Aharoni 20" )
        self.__entry_can.insert(0," ")
        self.__entry_can.config(state="disabled")
        self.__entry_can.place(height= 60, width= 200 , relx=0.205 , rely=0.75)

        self.__entry_pal = tk.Entry(self ,font="Aharoni 20")
        self.__entry_pal.insert(0," ")
        self.__entry_pal.config(state="disabled")
        self.__entry_pal.place(height= 60, width= 200 , relx=0.625 , rely=0.75)

        # -- Botoncitos -- (+ / -)
        mas_can = tk.Button(self, text="+", fg="dark green", bg = "white" ,  font = Subtitle_font ,
                            command=lambda : self.onClick_can())
        mas_can.place(height= 90, width= 90 ,  relx=0.35 , rely=0.745)
        
        men_can = tk.Button(self, text="-", fg="dark green", bg = "white" ,  font = Subtitle_font ,
                            command=lambda : self.onClick_can(action=False))
        men_can.place(height= 90, width= 90 ,  relx=0.40 , rely=0.745)

        mas_pal = tk.Button(self, text="+", fg="dark green", bg = "white" , font = Subtitle_font , 
                            command=lambda : self.onClick_pal())
        mas_pal.place(height= 90, width= 90 ,  relx=0.75 , rely=0.745)
        
        men_pal = tk.Button(self, text="-", fg="dark green", bg = "white" , font = Subtitle_font , 
                            command=lambda : self.onClick_pal(action=False))
        men_pal.place(height= 90, width= 90 ,  relx=0.80 , rely=0.745)


        # -- Option Menu --
        self.__canas_list  = ["TTEST1" ] 
        self.__pal_list    = ["Test1" ] 

        self.get_canastillas()
        self.get_palets()
        
        variable_can = tk.StringVar(self)
        variable_can.set(self.__canas_list[0])

        variable_pal = tk.StringVar(self)
        variable_pal.set(self.__pal_list[0])

        opt_canastillas = tk.OptionMenu(self, variable_can, *self.__canas_list)
        opt_canastillas.config(width=40, font=Text_font) # ---
        menu_can = self.nametowidget(opt_canastillas.menuname)
        menu_can.config( font=Text_font) # set the drop down menu font
        opt_canastillas.place(relx=0.08 , rely=0.3 )

        opt_palets = tk.OptionMenu(self, variable_pal, *self.__pal_list)
        opt_palets.config(width=40, font=Text_font)
        menu_pal = self.nametowidget(opt_palets.menuname)
        menu_pal.config(font=Text_font) # set the drop down menu font
        opt_palets.place(relx=0.5 , rely=0.3)

        # -- Buttons --
        button_home = ttk.Button(self, image=image_home  , style="Principal.TButton" , # background="white" ,
                            command=lambda: self.__controller.show_frame(StartPage))
        button_home.image = image_home
        button_home.place(relx= 0.88 , rely= 0.055)


        button_start = ttk.Button(self, text="Iniciar",  style="Secundary.TButton" ,
                            command=lambda: self.__controller.show_frame(Weigh_Result))
        button_start.place(relx=0.15,rely=0.85 ,    height=100)

    def onClick_can(self, action=True):
        if action:
            self.__counter_can = self.__counter_can+ 1
        else:
            self.__counter_can = self.__counter_can - 1
        if self.__counter_can < 0 :  self.__counter_can = 0
        self.__entry_can.config(state='normal')
        self.__entry_can.delete(0,tk.END)
        self.__entry_can.insert(0,str(self.__counter_can))
        self.__entry_can.config(state='disabled')
     
    def onClick_pal(self, action=True ):
        if action:
            self.__counter_pal = self.__counter_pal + 1
        else:
            self.__counter_pal = self.__counter_pal - 1
        if self.__counter_pal < 0 : self.__counter_pal = 0
        self.__entry_pal.config(state='normal')
        self.__entry_pal.delete(0,tk.END)
        self.__entry_pal.insert(0,str(self.__counter_pal))
        self.__entry_pal.config(state='disabled')

    def get_canastillas (self):
            
        accion = """SELECT * FROM canastillas"""
        __localdb = SQL.LocalDBConsumption(databasename= "contenedores.db")
        __canastillas = __localdb.consult(lite_consult=accion , modification=False)
        __localdb.close_connection()
        if not __canastillas:
            self.__controller.show_frame(StartPage)
        else:
            for canas in __canastillas:
                print (canas)
                self.__canas_list.append("Canastilla1")
                self.__canas_list.append("Canastilla2")

    def get_palets (self):
                   
        accion = """SELECT * FROM estibas """
        __localdb = SQL.LocalDBConsumption(databasename= "contenedores.db")
        __palets = __localdb.consult(lite_consult=accion , modification=False)
        __localdb.close_connection()
        if not __palets:
            self.__controller.show_frame(StartPage)
        else:
            for pal in __palets:
                print (pal)
                self.__pal_list.append("Palet1")
                self.__pal_list.append("Palet2")

    def update_frame(self):
        print ("Actualizacion del frame Weight INital  ")

class Weigh_Result(tk.Frame):

    def __init__(self, parent, controller):
        
        ttk.Frame.__init__(self, parent)
        self.__controller = controller
        self.__pinted     = False
        print ("INit Weigh Result")
        
        # --  Get Images --
        image_home = Image.open(cache_folder+'/back_row.png')
        image_home = image_home.resize((90,90), Image.ANTIALIAS)
        image_home = ImageTk.PhotoImage(image_home)


        # -- Labels Tittles --
        labeltitle = ttk.Label(self, text="Proceso de pesaje ", style="Tittle.TLabel")
        labeltitle.place(relx=0.1 , rely=0.055)
        labeltitle2 = ttk.Label(self, text="Resultados : ", style="SubTittle.TLabel")
        labeltitle2.place(relx=0.1 , rely=0.135)

 
        # -- Buttons --
        button_home = ttk.Button(self, image=image_home  , style="Principal.TButton" , # background="white" ,
                            command=lambda: self.__controller.show_frame(Weigh_Initial))
        button_home.image = image_home
        button_home.place(relx= 0.012 , rely= 0.055)
        
        button_again = ttk.Button(self, text="Pesar de nuevo ",  style="Principal.TButton" ,
                            command=lambda: self.__same() )
        button_again.place(relx=0.14,rely=0.8)
        
        button_nuevo = ttk.Button(self, text="Nuevo pesaje ",  style="Principal.TButton" ,
                            command=lambda: self.__new() )
        button_nuevo.place(relx=0.54,rely=0.8)
            
    def __new (self):
        self.__controller.show_frame(Weigh_Initial)

    def __same (self):
        self.__controller.show_frame(Weigh_Initial)

    def __gen_barcode(self):
        
        # Make sure to pass the number as string 
        number = '5901234123457'

        rv = BytesIO()
        my_code  = barcode.EAN13(number , writer=barcode.writer.ImageWriter()).write(rv)
        
        my_code2 = barcode.EAN13(number , writer=barcode.writer.ImageWriter())
        my_code2.save("new_code")
        
        image_home = Image.open('new_code.png')
        width, height = image_home.size
        print ("Size of image {} {} ".format(width,height))
        image_home = image_home.resize((600,360), Image.ANTIALIAS)
        image_home = ImageTk.PhotoImage(image_home)

        self.label_code = tk.Label(self, image = image_home, borderwidth=0)
        self.label_code.place(relx= 0.34 , rely= 0.41)
        self.label_code.image = image_home

    def __get_weights(self):
        return None
        return 123

    def __final_cam (self):
        with open('cache/limonsin.png', 'rb') as file:
            image = file.read()
            image = base64.b64encode(image)  
            print (image)

            API.request_Frubana(basekts     = 66 , 
                                product     ="product2", 
                                state       = "state2", 
                                num_pallets = 67 , 
                                pallets_id  = "palet2",
                                abs_weight  = 42 ,
                                final_weight= 36 , 
                                image=image)


    def update_frame(self):
        print ("Actualizacion del frame Weight Result  ")
        
        self.__weight = self.__get_weights()
        if self.__weight :
            self.__final_cam()
            try:
                self.labeltitle_res.destroy()
                self.label_peso_total.destroy()
            except :
                print (CONS.bcolors.FAIL+"ERRRRRDA"+CONS.bcolors.ENDC)

            self.labeltitle_res = ttk.Label(self, text="¡Proceso Exitoso!", style="GreenSubTittle.TLabel")
            self.labeltitle_res.place(relx=0.4 , rely=0.25)

            self.label_peso_total = ttk.Label(self, text="Peso Final del producto:", style="BlackSubTittle.TLabel")
            self.label_peso_total.place(relx=0.445 , rely=0.3)

            self.label_peso_total_val = ttk.Label(self, text="{} Kg".format(self.__weight), style="BlackSubTittle.TLabel")
            self.label_peso_total_val.place(relx=0.46 , rely=0.35)
            self.__pinted = True if self.__gen_barcode() else False
                 

        else : 
            if self.__pinted:
                self.labeltitle_res.destroy()
                self.label_peso_total.destroy()
                self.label_peso_total_val.destroy()
                self.label_code.destroy()
            
            self.labeltitle_err = ttk.Label(self, text="¡Proceso No Completado!", style="RedSubTittle.TLabel")
            self.labeltitle_err.place(relx=0.4 , rely=0.25)

            self.label_error = ttk.Label(self, text="Error En proceso \n Retire elementos ajenos al proceso de pesado", style="BlackSubTittle.TLabel")
            self.label_error.place(relx=0.445 , rely=0.3)

        #self.__gen_barcode()

# ------ POP UPS ------

def config_bluetooth( ):

    def onselect(evt):
        w = evt.widget
        index_value = int(w.curselection()[0])
        print ('You selected item %d: "%s"' % (index_value,  w.get(index_value) ))
        blue_name.config(state='normal')
        blue_name.delete(0,tk.END)
        blue_name.insert(0,str(w.get(index_value)))
        blue_name.config(state='disabled')

    def pair():
        conn_b.config(state = "normal")
        index_value = int(lista_box.curselection()[0])
        print ("Seleccionado {}".format(index_value))
        print ("Got {}".format(lista_box.get(index_value)))
            
    def connect (  ):
        # echo -e "connect AA:BB:CC:DD:EE \nquit" | bluetoothctl
        
        index_value = int(lista_box.curselection()[0])
        print ("Connectando {} ".format(lista_box.curselection()[0]))
        print ("Got {}".format(lista_box.get(index_value)))
        blue_name.config(state='normal')
        blue_name.delete(0,tk.END)
        blue_name.insert(0,"Conectado")
        blue_name.config(state='disabled')

    def list_blue():
        pair_b.config(state = "normal")
        lista_box.insert(tk.END,"ALo")
        lista_box.insert(tk.END,"LL")
        lista_box.insert(tk.END,"Adios")

    popup_blue = tk.Tk()

    popup_blue.wm_title("Configuracion de Bluetooth")
    popup_blue.geometry("{}x{}+{}+{}".format (int(screen_width*0.45) ,
                                        int(screen_height*0.55),
                                        int(screen_width*0.33),
                                        int(screen_height*0.18) ))

    label = tk.Label(popup_blue, text="Dispositivos Bluetooth", font=Pop_Up_Font_T , fg='#F8AC18' )
    label.grid(row = 0,column = 0)


    tk.Label(popup_blue ,text = "Actualziar dispositivos" , font=Pop_Up_Font_R).grid(row = 2,column = 0)
   
    lista_box = tk.Listbox( popup_blue , 
                            highlightcolor="#F8AC18" , 
                            highlightbackground="#ffffff",
                            selectborderwidth=5 , 
                            font=Pop_Up_Font_R)
    lista_box.place(height= 200, width= 550 , relx =0.01 , rely = 0.22 )
    lista_box.bind('<<ListboxSelect>>', onselect)

    blue_name = tk.Entry(popup_blue , font=Pop_Up_Font_R , state='disabled')
    blue_name.place(height= 100, width= 450 , relx =0.01 , rely = 0.65 )

    listar = tk.Button(popup_blue,text="Escanea", command = lambda: list_blue() )
    listar.config( font=Pop_Up_Font_R , height=2 , width=10  )
    listar.place(height= 92, width= 200 , relx =0.73 , rely = 0.22 )


    # INVOCAR UNA FUNCION QUE SE ENCUENTRE EN EL MODULO DE LA BASE DE DATOS
    pair_b = tk.Button(popup_blue ,text="Pair", command = lambda: pair()  ) #or popup.destroy()
    pair_b.config( font=Pop_Up_Font_R , height=2 , width=10   )
    pair_b.config(state="disabled")
    pair_b.place(height= 92, width= 200 , relx =0.73 , rely = 0.65 )

    conn_b = tk.Button(popup_blue ,text="Conectar", command = lambda: connect()  ) #or popup.destroy()
    conn_b.config( font=Pop_Up_Font_R , height=2 , width=10   )
    conn_b.config(state="disabled")
    conn_b.place(height= 92, width= 200 , relx =0.73 , rely = 0.82 )

    popup_blue.mainloop()

def config_popup( frames_controller , title="Configurar __" , tipo="CanPalTo" ):
    def save_in_db( ):
        done =  False
        try:
            if id_cont.get() and name_c.get() and weight.get() :
                            
                accion = """INSERT INTO {} (code_id , name , peso ) 
                            VALUES         ({},'{}',{})""".format(tipo,id_cont.get(),name_c.get(),weight.get())
                __localdb = SQL.LocalDBConsumption(databasename= "contenedores.db")
                __location_new1 = __localdb.consult(lite_consult=accion , modification=True)
                __localdb.close_connection()

                if __location_new1:
                    done =  True 

        except Exception as e :
            print (e)

        finally:
            if done:   
                popup.destroy()

                if tipo == "canastillas" : frames_controller.show_frame(Config_Canas)
                if tipo == "estibas" : frames_controller.show_frame(Config_Estibas)

                popupmsg(title="Exito" , msg = "Guardado")

            else :      
                popupmsg(title="ERROR" , msg = "Error en datos")

    def get_cont_weight ( the_entry ):
        the_entry.config(state='normal')
        the_entry.delete(0,tk.END)
        the_entry.insert(0,"666")
        the_entry.config(state='disabled')

    popup = tk.Tk()
    
    popup.wm_title(title)
    popup.geometry("{}x{}+{}+{}".format (int(screen_width*0.55) ,
                                        int(screen_height*0.5),
                                        int(screen_width*0.25),
                                        int(screen_height*0.2) ))

    label = tk.Label(popup, text="Nueva {}".format(tipo), font=Pop_Up_Font_T , fg='#F8AC18' )
    label.grid(row = 0,column = 0)


    tk.Label(popup ,text = "ID Contenedor" , font=Pop_Up_Font_R).grid(row = 2,column = 0)
    tk.Label(popup ,text = "Nombre "       , font=Pop_Up_Font_R).grid(row = 4,column = 0)
    tk.Label(popup ,text = "Peso Contenedor",font=Pop_Up_Font_R).grid(row = 6,column = 0)

    id_cont = tk.Entry(popup , font=Pop_Up_Font_R)
    id_cont.grid(row=2 , column=1 , padx=10 , pady=10 , ipady=30)
    name_c = tk.Entry(popup , font=Pop_Up_Font_R)
    name_c.grid(row=4 , column=1 , padx=10 , pady=10 , ipady=30)
    weight = tk.Entry(popup , font=Pop_Up_Font_R , state='disabled')
    weight.grid(row=6 , column=1 , padx=10 , pady=10 , ipady=30)

    pesar = tk.Button(popup,text="Pesar", command = lambda: get_cont_weight(weight) )
    pesar.config( font=Pop_Up_Font_R , height=2 , width=10  )
    pesar.grid(row = 6,column = 2 , padx=18 )

    # INVOCAR UNA FUNCION QUE SE ENCUENTRE EN EL MODULO DE LA BASE DE DATOS
    save = tk.Button(popup ,text="Okay", command = lambda: save_in_db()  ) #or popup.destroy()
    save.config( font=Pop_Up_Font_R , height=2 , width=10   )
    save.grid(row = 14,column = 0 , padx=18)
    popup.mainloop()

# ------  Inicial ------

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

# Last tutorial I saw
#https://pythonprogramming.net/object-oriented-programming-crash-course-tkinter/?completed=/tkinter-depth-tutorial-making-actual-program/