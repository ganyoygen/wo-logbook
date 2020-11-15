import os
import tkinter as tk
from tkinter import *
from tkinter import ttk,Toplevel


class SetProgBar(object):
    def __init__(self,parent,data):
        top = self.top = Toplevel(parent)
        top.title("Progress Bar")
        top.iconbitmap(str(os.getcwd()+"\\"+"icon-icons.com_main.ico"))
        self.parent = parent
        self.top.protocol("WM_DELETE_WINDOW", self.keluar)
        topFr = ttk.Frame(top)
        topFr.grid(row=0,column=0)

        self.pbar = ttk.Progressbar(topFr,orient="horizontal",length=500,mode="determinate")
        self.pbar.grid(row=1,column=0)
        self.plabel = ttk.Label(topFr,text="")
        self.plabel.grid(row=2,column=0)
        self.bytes = 0
        self.pbar["value"] = 0
        self.maxbytes = data
        self.pbar["maximum"] = data
        self.read_data()

        # top.wait_visibility() # window needs to be visible for the grab (ga akan kerja kalo aktif pas import di page main)
        top.grab_set()
        top.bind("<FocusOut>", self.alarm)
        top.resizable(0,0)
        self._set_transient(parent)

    def read_data(self):
        '''simulate reading 500 bytes; update progress bar'''
        # self.bytes += 10
        self.pbar["value"] = self.bytes
        # self.plabel.config(text=str((self.bytes/self.maxbytes)*100)+"%")
        self.plabel.config(text=str(self.bytes)+"/"+str(self.maxbytes))
        if self.bytes < self.maxbytes:
            self.top.after(100, self.read_data)
        else:
            self.pbar.stop()
            self.pbar.grid_forget()
            self.top.destroy()
    
    def keluar(self,event=None):
        print("disable close the program when process still loading")
        # self.top.destroy()

    def _set_transient(self, master, relx=0.5, rely=0.3):
        # window proses ikut parent (without icon taskbar)
        widget = self.top
        widget.withdraw() # Remain invisible while we figure out the geometry
        widget.transient(master)
        widget.update_idletasks() # Actualize geometry information
        if master.winfo_ismapped():
            m_width = master.winfo_width()
            m_height = master.winfo_height()
            m_x = master.winfo_rootx()
            m_y = master.winfo_rooty()
        else:
            m_width = master.winfo_screenwidth()
            m_height = master.winfo_screenheight()
            m_x = m_y = 0
        w_width = widget.winfo_reqwidth()
        w_height = widget.winfo_reqheight()
        x = m_x + (m_width - w_width) * relx
        y = m_y + (m_height - w_height) * rely
        if x+w_width > master.winfo_screenwidth():
            x = master.winfo_screenwidth() - w_width
        elif x < 0:
            x = 0
        if y+w_height > master.winfo_screenheight():
            y = master.winfo_screenheight() - w_height
        elif y < 0:
            y = 0
        widget.geometry("+%d+%d" % (x, y))
        widget.deiconify() # Become visible at the desired location

    def alarm(self, event):
        self.top.bell()

class TestRun(object):
    def __init__(self,master):
        self.master=master
        self.setbtn=ttk.Button(master,text="Progress",command=self.popup)
        self.setbtn.pack()

    def popup(self):
        # os.system("cls")
        data = 100
        test=SetProgBar(self.master,data)
        self.setbtn["state"] = "disabled"
        for i in range(data):
            test.bytes = i+1 #update self.bytes hingga memenuhi data 
        self.master.wait_window(test.top)
        self.setbtn["state"] = "normal"

if __name__ == "__main__":
    root=tk.Tk()
    TestRun(root)
    root.mainloop()

