import tkinter as tk
 
def print_something(event):
	print("You choose " + v.get())

root = tk.Tk()
v = tk.StringVar()
om = tk.OptionMenu(root, v, "Choose", "item 1", "item 2", "item 3")
v.set("item 3")
om.pack()
om.bind("<Return>", print_something)
om.focus()
om.config(width=40 )
menu_pal = root.nametowidget(om.menuname)
#menu_pal.config(width=40) # set the drop down menu font
 
root.mainloop()

