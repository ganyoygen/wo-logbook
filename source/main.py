import os
import tkinter
from tkinter import *
from tkinter import ttk,messagebox
from page_main import PageMain
from page_progress import PageProg
from page_user import UserMgmt
from page_about import About
from ttkthemes import ThemedTk # make sure to pip install ttkthemes
from login import Login

VERSION = "1.1-11.20"

class WindowDraggable():
    def __init__(self, label):
            self.label = label
            label.bind('<ButtonPress-1>', self.StartMove)
            label.bind('<ButtonRelease-1>', self.StopMove)
            label.bind('<B1-Motion>', self.OnMotion)

    def StartMove(self, event):
            self.x = event.x
            self.y = event.y

    def StopMove(self, event):
            self.x = None
            self.y = None

    def OnMotion(self,event):
            x = (event.x_root - self.x - self.label.winfo_rootx() + self.label.winfo_rootx())
            y = (event.y_root - self.y - self.label.winfo_rooty() + self.label.winfo_rooty())
            root.geometry("+%s+%s" % (x, y))

class MainLog:
    def __init__(self,parent):
        self.parent = parent
        self.user = ""
        self.dept = ""
        self.parent.protocol("WM_DELETE_WINDOW", self.keluar)
        lebar=950
        tinggi=680
        setTengahX = (self.parent.winfo_screenwidth()-lebar)//2
        setTengahY = (self.parent.winfo_screenheight()-tinggi)//2
        self.parent.geometry("%ix%i+%i+%i" %(lebar, tinggi,setTengahX, setTengahY-40)) # setTengahY-40 : Biar lebih keatas
        self.startlogin()

    def startlogin(self):
        self.login = Login(self.parent)
        self.login.parent.wait_window(self.login.top)
        self.user = self.login.user
        self.dept = self.login.dept
        if self.user == "" and self.dept == "":
            self.keluar()
        else:
            self.aturKomponen()
    
    def aturKomponen(self):
        frameWin = Frame(self.parent, bg="#898")
        frameWin.pack(fill=X,side=TOP)
        footer = Frame(self.parent)
        footer.pack(fill=X,side=BOTTOM)
        WindowDraggable(frameWin)
        # Label(frameWin, text='Work Order Logbook Record',bg="#898",fg="white").pack(side=LEFT,padx=20)
        Label(frameWin, text=("Login: {0}.{1}".format(self.user,self.dept)),bg="#898",fg="white").pack(side=LEFT,padx=20)
        Label(footer, text=("Work Order Manager Version: {0}".format(VERSION))).pack(side=LEFT,padx=10)
        Label(footer, text=("Copyright © 2020 prasetya.angga.pares@gmail.com")).pack(side=RIGHT,padx=10)
        '''
        # Menghilangkan Frame windows
        buttonx = Button(frameWin, text="X",fg="white", bg="#FA8072", width=6, height=2,bd=0,\
                         activebackground="#FB8072",activeforeground="white", command=self.keluar, relief=FLAT)
        self.parent.overrideredirect(1) 
        buttonx.pack(side=RIGHT)
        '''

        self.notebook = ttk.Notebook(self.parent) # lihat, self.parent = root
        self.notebook.pack(fill="both", expand=True)

        page0 = PageMain(self.notebook,self.user,self.dept)
        page1 = PageProg(self.notebook,self.user,self.dept)
        page2 = UserMgmt(self.notebook,self.user,self.dept)
        page3 = About(self.notebook,self.user,self.dept)
        self.notebook.add(page0, text="Main")
        self.notebook.add(page1, text="Progress")
        self.notebook.add(page2, text="User Mgmt")
        self.notebook.add(page3, text="About")
        if self.dept != "ROOT": self.notebook.tab(2, state = 'disabled')

    def keluar(self,event=None):
        # print("disable close on the main windows!")
        try: 
            self.login.parent.destroy()
            self.parent.destroy()
        except: pass
        # if (messagebox.askokcancel("Attention","Do you really want to exit the App?")):
            # self.parent.destroy()


if __name__ == "__main__":
    # os.system("cls")
    # root = Tk()
    root = ThemedTk(theme='scidblue')
    root.title("Work Order Manager")
    root.iconbitmap(str(os.getcwd()+"\\"+"icon-icons.com_main.ico"))
    MainLog(root)
    root.mainloop()