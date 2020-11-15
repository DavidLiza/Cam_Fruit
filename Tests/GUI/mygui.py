#!/usr/bin/env python
# -*- coding: latin-1-*-

#from    Tkinter import *
from    tkinter import *
import  tkinter.font as tkFont
import  tkinter.messagebox as tkMessageBox

import  serial
import  time
import  string
import  numpy
import  sys
import  os
#import TCS3200

#os.system("vncserver :1 -geometry 1280x800 -depth 16 -pixelformat rgb565")
#os.system("sudo pigpiod")
#RGB=commands.getoutput('/usr/bin/python TCS3200.py')


win = Tk()
screen_width  = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()
print ("Width {} & Height {}".format(screen_width,screen_height))

win.config(bg="WHITE")

imagenl=PhotoImage(file="../../cache/logo6GIF.gif")
imagen2=PhotoImage(file="../../cache/MECA.gif")

lblImagen=Label(win,image=imagenl).place(x=500,y=50)
lblImagen=Label(win,image=imagen2).place(x=500,y=250)


def tiimee():
    times = ment.get()
    lblpres    = Label(text=times ,font=Fontext,bg="WHITE").place(x=125,y=160)

def reboot():
    os.system("sudo reboot")

def turnoff():
    os.system("sudo poweroff")

def reboot():
    os.system("sudo reboot")

def update(): #funcion para los valores del sensor
    while 1:

        if __name__ == "__main__":
            RED=21
            GREEN=20
            BLUE=16

            def wait_for_return(str):
                if sys.hexversion < 0x03000000:
                 raw_input(str)
                else:
                 input(str)
            interval = 0.2
        
        total = 666

        readingaz.set(0)  #set
        readingro.set(0)
        readingve.set(0)
        readingam.set(0)
        readingto.set(total)
        try:
            win.update()
            time.sleep(1)
        except:
            print ("Break Update")
            break
        
            
def RELE():
    print ("Activacion de un RELE")

def exitProgram():
    print ("Saliendo del programa")
    win.destroy()
    print ("Fuera de tres primeros")


def envio():
    print("Este es el valor a 255")
    print("Funcion de envio")

def readColor():

    tkMessageBox.showinfo("Halo", "SAPOELQUE LEA!")
    print ("HELLO")

def set_window():
    win.title("PROCESO DE PESAJE") #TITULO DEL GUI
    win.geometry('800x480') #dimensiones
    
    #TITULO CENTRADO
    #lbltitulo= Label(win, text= "MAS TAPITAS ",fg = "blue",bg="WHITE",font=myFont).place(x=250,y=10)
    lbltitulo= Label(win, text= "MAS TAPITAS ",fg = "blue",bg="WHITE",font=myFont).place(relx=0.4,rely=0.01)

    #Labels
    lblsubt    = Label(text= "Variables ",fg = "blue",font=myFont,bg="WHITE").place(x=40,y=55)
    lbltemp    = Label(text= "Numero de tapas:",font=Fontext,bg="WHITE").place(x=75,y=100)
    lblazul    = Label(text= "Azul:",font=Fontext,bg="WHITE").place(x=75,y=130)
    lblrojo    = Label(text= "Rojo:",font=Fontext,bg="WHITE").place(x=75,y=160)
    lblverd    = Label(text= "Verde:",font=Fontext,bg="WHITE").place(x=75,y=190)
    lblamar    = Label(text= "Amarillo:",font=Fontext,bg="WHITE").place(x=75,y=220)
    lblpres    = Label(text= "Numero Total de tapas :",font=Fontext,bg="WHITE").place(x=75,y=260)

    lblazu    = Label(win,textvariable = readingaz,font =ALERTA,fg="blue",bg="WHITE").place(x=180,y=130)
    lblroj    = Label(win,textvariable = readingro,font =ALERTA,fg="red",bg="WHITE").place(x=180,y=160)
    lblver    = Label(win,textvariable = readingve,font =ALERTA,fg="green",bg="WHITE").place(x=180,y=190)
    lblama    = Label(win,textvariable = readingam,font =ALERTA,fg="yellow",bg="WHITE").place(x=180,y=220)
    lbltot    = Label(win,textvariable = readingto,font =ALERTA,fg="black",bg="WHITE").place(x=75,y=295)

    menubar = Menu(win)
    OPTIONSmenu = Menu(menubar, tearoff=0)

    OPTIONSmenu.add_command(label="Close", command=exitProgram)
    OPTIONSmenu.add_separator()
    OPTIONSmenu.add_command(label="Reboot", command=reboot)
    OPTIONSmenu.add_separator()
    OPTIONSmenu.add_command(label="Turn off", command=turnoff)
    menubar.add_cascade(label="System Options", menu=OPTIONSmenu)
    win.config(menu=menubar)

#LETRAS
myFont     = tkFont.Font(family = 'URW Chancery L', size = 26, weight = 'bold')
Fontext    = tkFont.Font(family = "Arial", size = 18)
vari       = tkFont.Font(family = "Times New Roman",size=22)
ALERTA     = tkFont.Font(family = "URW Gothic L",size=18)

readingaz  = StringVar()
readingro  = StringVar()
readingve  = StringVar()
readingam  = StringVar()
readingto  = StringVar()


#FRAME
bottomFrame = Frame (win)
bottomFrame.pack(side=BOTTOM)
bbottomFrame = Frame (bottomFrame)
bbottomFrame.pack(side=RIGHT)

#INTERACCIONES
exitButton= Button(text = "Start",fg="red",font =ALERTA,  command =readColor).place(x=200,y=365)
ReleButton = Button(text = "ON/OFF",fg="blue",font =ALERTA, command = RELE ).place(x=300,y=365)

#teclado = Button(win, text ="TECLADO" , command = teclado ).place(x=600,y=100)
#CHAO = Button(win, text ="APAGAR" , fg="red",command = turnoff ).place (x=100,y=365)
#LASSIGUIENTES 3 LIBEAS  DE CODIGOSEENCARGABANDE CREAR UNA BARRA  DESPLEGABLE
ment = StringVar()
spin = Spinbox(win,textvariable=ment, from_=0, to=10).place(x=600,y=50)
tiimee= Button(text = "Start",fg="red",  command = tiimee).place(x=600,y=100)

if __name__ == '__main__':
    print ("Run as Main")
    set_window()
    
    win.after(5,update)
    print ("OK OK")

    mainloop()
