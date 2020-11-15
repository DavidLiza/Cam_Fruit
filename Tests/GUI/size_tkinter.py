import tkinter as tk
from   tkinter import ttk

from PIL import Image, ImageTk
import os
import sys

#Salidas del Rapsberry :
# - Salida para los Sensores
# - Entrada para los sensores 
# - Usb de la camara 
# - Serial para la Bascula 
# - Entrada de Voltaje 


#Fonts
Title_font   = ("Aharoni", 40 , "bold")
Subtitle_font= ("Aharoni", 20 , "bold")
Text_font    = ("Aharoni", 10 )

Button_font  = ("Aharoni", 15 , "bold")

NORM_FONT    = ("Verdana", 10)
SMALL_FONT   = ("Verdana", 8)


# File Importan Path
filename = sys.argv[0]
pathname = os.path.dirname(filename)        
full_path = os.path.abspath(pathname)

index_module = full_path.find('module')
cache_folder = full_path[:index_module]+'cache'

print ("Folder {}".format(cache_folder))

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("Hey!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)

    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()


exchange = "BTC-e"
DatCounter = 9000
programName = "btce"


def changeExchange(toWhat,pn):
    global exchange
    global DatCounter
    global programName

    exchange = toWhat
    programName = pn
    DatCounter = 9000
    


class SeaofBTCapp(tk.Tk):
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



        # Main Menu Bar 
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff =0 )
        filemenu.add_command(label="Save settings", command = lambda: popupmsg("Not supported just yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)


        exchangeChoice = tk.Menu(menubar, tearoff=1)
        exchangeChoice.add_command(label="BTC-e", command=lambda: changeExchange("BTC-e","btce"))
        exchangeChoice.add_command(label="Bitfinex",command=lambda: changeExchange("Bitfinex","bitfinex"))
        exchangeChoice.add_command(label="Bitstamp",command=lambda: changeExchange("Bitstamp","bitstamp"))
        exchangeChoice.add_command(label="Huobi",command=lambda: changeExchange("Huobi","huobi"))

        menubar.add_cascade(label="Exchange", menu=exchangeChoice)

        tk.Tk.config(self, menu=menubar)



        self.__frames = {}

        for my_frames in (StartPage, Admin_Data, Weigh_Initial):
            frame = my_frames(container, self)
            self.__frames[my_frames] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.__frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self,parent)

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
                            command=lambda: controller.show_frame(Admin_Data))
        button_conf.image = image_conf
        button_conf.place(relx=0.88,rely=0.015)

        button1 = ttk.Button(self, text="Aministra Complementos",  style="Principal.TButton" ,
                            command=lambda: controller.show_frame(Admin_Data))
        button1.place(relx=0.20,rely=0.75)
        
        button2 = ttk.Button(self, text="Proceso de Pesaje", style="Principal.TButton",
                            command=lambda: controller.show_frame(Weigh_Initial))
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
        

if __name__ == "__main__":
    os.system('clear')
    print ("*** FRUBANA BEGINS ***")    
    app = SeaofBTCapp()
    app.mainloop()


# ************  INPUTS ************

# e = ttk.Entry(midIQ)
# e.insert(0,10)
# e.pack()
# e.focus_set()

# Last tutorial I saw
#https://pythonprogramming.net/object-oriented-programming-crash-course-tkinter/?completed=/tkinter-depth-tutorial-making-actual-program/