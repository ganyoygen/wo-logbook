import os
import tkinter
from tkinter import *
from tkinter import ttk
from page_main import PageMain
from page_pending import Pending
from page_progress import PageProg
from ttkthemes import ThemedTk # make sure to pip install ttkthemes

# root = Tk()
root = ThemedTk(theme='clearlooks')

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
    def __init__(self,parent,user,dept):
        self.parent = parent
        self.user = user
        self.dept = dept
        self.parent.protocol("WM_DELETE_WINDOWS", self.keluar)
        lebar=950
        tinggi=680
        setTengahX = (self.parent.winfo_screenwidth()-lebar)//2
        setTengahY = (self.parent.winfo_screenheight()-tinggi)//2
        self.parent.geometry("%ix%i+%i+%i" %(lebar, tinggi,setTengahX, setTengahY-40)) # setTengahY-40 : Biar lebih keatas
        
        self.aturKomponen()
    
    def aturKomponen(self):
        frameWin = Frame(self.parent, bg="#898")
        frameWin.pack(fill=X,side=TOP)
        WindowDraggable(frameWin)
        Label(frameWin, text='Work Order Logbook Record',bg="#898",fg="white").pack(side=LEFT,padx=20)
        # Label(frameWin, text=("Login:",self.user),bg="#898",fg="white").pack(side=RIGHT,padx=20)
        Label(frameWin, text=("Login: {0}.{1}".format(self.user,self.dept)),bg="#898",fg="white").pack(side=RIGHT,padx=20)
        '''
        # Menghilangkan Frame windows
        buttonx = Button(frameWin, text="X",fg="white", bg="#FA8072", width=6, height=2,bd=0,\
                         activebackground="#FB8072",activeforeground="white", command=self.keluar, relief=FLAT)
        self.parent.overrideredirect(1) 
        buttonx.pack(side=RIGHT)
        '''

        self.notebook = ttk.Notebook(self.parent) # lihat, self.parent = root
        self.notebook.pack(fill="both", expand=True)

        page1 = PageMain(self.notebook,self.user,self.dept)
        page2 = PageProg(self.notebook,self.user,self.dept)
        page3 = Pending(self.notebook)
        self.notebook.add(page1, text="Main")
        self.notebook.add(page2, text="Progress")
        self.notebook.add(page3, text="Pending")

    def keluar(self,event=None):
        self.parent.destroy()

def start(user,dept):
    os.system("cls")
    root.title("Project Logbook by GanyoyGen")
    root.iconbitmap(str(os.getcwd()+"\\"+"icon-icons.com_main.ico"))
    MainLog(root,user,dept)

if __name__ == "__main__":
    start("UkikLodom","ENG")
    root.mainloop()