import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys

# Program to generate a Window for the size of the screen 
# where the programm is beeing run


filename = sys.argv[0]
pathname = os.path.dirname(filename)        
full_path = os.path.abspath(pathname)

index_module = full_path.find('module')
cache_folder = full_path[:index_module]+'cache'
image_frubana = cache_folder+'/frubana.png'

root = tk.Tk()
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
#print(root.winfo_screenheight(), root.winfo_screenwidth())
root.geometry("%dx%d" % (width, height))
image = Image.open(image_frubana)

if image.size != (width, height):
    image = image.resize((width, height), Image.ANTIALIAS)
    #print("DONE RESIZING")
    # image.save("background.jpg")
#print(image.size)
image = ImageTk.PhotoImage(image)
bg_label = tk.Label(root, image = image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
bg_label.image = image
your_button = ttk.Button(root, text='This is a button')
your_button.grid()
root.mainloop()