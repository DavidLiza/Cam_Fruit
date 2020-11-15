

#from    tkinter import * 
import  tkinter as tk               
from    tkinter import font as tkfont  
import  tkinter.messagebox as tkMessageBox

import  serial
import  time
import  string
import  numpy
import  sys
import  os


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
                
        # Elimiunbar esto
        tk.Tk.__init__(self, *args, **kwargs)

        self.root = tk.Tk()
        
        screen_width  = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        print ("Width {} & Height {}".format(screen_width,screen_height))

        self.root.geometry("1920x1080")
        self.root.title("Frubana")
        self.root.configure(bg="WHITE")
        self.root.grid()

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")


        
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others

        container = tk.Frame(self.root,height=500,width=300,bg="black")
        container.grid_propagate(1)
        
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        print ("Frames Declaration")
        for F in (StartPage, AdminEstibas, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        print ("Frames Declared")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        menubar = frame.menubar(self.root)
        self.root.configure(menu=menubar)
        
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        #frame = tk.Frame(parent)
        
        mylogo=tk.PhotoImage(file="../../cache/logo6GIF.gif")
        #imagen2=tk.PhotoImage(file="../../cache/MECA.gif")
        
        w = tk.Canvas(self,width = 300, height = 300)
        w.pack()
        w.create_image(20,20, image=mylogo)
        #lblImagen=tk.Label(frame,image=mylogo)
        #lblImagen.place(x=0,y=0)

        label = tk.Label(self, text="Welcome to frubana", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        
        button1 = tk.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame("AdminEstibas"))
        button2 = tk.Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame("PageTwo"))
        button1.pack()
        button2.pack()

    def menubar(self, root):
        menubar = tk.Menu(root)
        pageMenu = tk.Menu(menubar)
        pageMenu.add_command(label="Close")
        menubar.add_cascade(label="Options", menu=pageMenu)
        return menubar

class AdminEstibas(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Select the table", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

    def menubar(self, root):
        menubar = tk.Menu(root)
        pageMenu = tk.Menu(menubar)
        pageMenu.add_command(label="Close")
        menubar.add_cascade(label="Options", menu=pageMenu)
        return menubar

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

    def menubar(self, root):
        menubar = tk.Menu(root)
        pageMenu = tk.Menu(menubar)
        pageMenu.add_command(label="Close")
        menubar.add_cascade(label="Options", menu=pageMenu)
        return menubar


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()

"""	
*********** TKINTER *******
https://www.youtube.com/watch?v=jBUpjijYtCk
https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
https://pythonprogramming.net/search/?q=gui
https://www.geeksforgeeks.org/python-gui-tkinter/
"""
	
