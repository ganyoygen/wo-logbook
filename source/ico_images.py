import tkinter as tk
import os
from tkinter import ttk

class iconimage(object):
    def __init__(self,master):
        self.master=master
        style = ttk.Style(self.master)
        # style.map('TButton', foreground = [("active", "brown"),("!active", "black")])
        style.map('TButton', background = [('active','gainsboro')],\
                            foreground = [("active", "brown"), ("!active", "black")])
        iclogout = tk.PhotoImage(file = str(os.getcwd()+"\\"+"icon"+"\\"+"logout.png"))
        self.iclogout = iclogout.subsample(2, 2) 
        imgdateset = tk.PhotoImage(file = str(os.getcwd()+"\\"+"icon"+"\\"+"date.png"))
        self.imgdateget = imgdateset.subsample(2, 2) # Resizing image by.subsample to fit on button
        icosearch2 = tk.PhotoImage(file = str(os.getcwd()+"\\"+"icon"+"\\"+"search2.png"))
        self.icosearch2 = icosearch2.subsample(2, 2)
        icosrctab = tk.PhotoImage(file = str(os.getcwd()+"\\"+"icon"+"\\"+"search.png"))
        self.icosrctab = icosrctab.subsample(2, 2) 
        icoexpxl = tk.PhotoImage(file = str(os.getcwd()+"\\"+"icon"+"\\"+"expexl.png"))
        self.icoexpxl = icoexpxl.subsample(2, 2) 
        icoimport = tk.PhotoImage(file = str(os.getcwd()+"\\"+"icon"+"\\"+"import.png"))
        self.icoimport = icoimport.subsample(2, 2)
        icodbsyn = tk.PhotoImage(file = str(os.getcwd()+"\\"+"icon"+"\\"+"dbsync.png"))
        self.icodbsyn = icodbsyn.subsample(2, 2)

        iconew = tk.PhotoImage(file = str(os.getcwd()+"\\"+"icon"+"\\"+"newf.png"))
        self.iconew = iconew.subsample(2, 2)
        icosave = tk.PhotoImage(file = str(os.getcwd()+"\\"+"icon"+"\\"+"save.png"))
        self.icosave = icosave.subsample(2, 2)
        icoupdt = tk.PhotoImage(file = str(os.getcwd()+"\\"+"icon"+"\\"+"update.png"))
        self.icoupdt = icoupdt.subsample(2, 2)
        icodel = tk.PhotoImage(file = str(os.getcwd()+"\\"+"icon"+"\\"+"delete.png"))
        self.icodel = icodel.subsample(2, 2)
        icorcv = tk.PhotoImage(file = str(os.getcwd()+"\\"+"icon"+"\\"+"receive.png"))
        self.icorcv = icorcv.subsample(2, 2)
        icopull = tk.PhotoImage(file = str(os.getcwd()+"\\"+"icon"+"\\"+"collect.png"))
        self.icopull = icopull.subsample(2, 2)
