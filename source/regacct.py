import os
import tkinter as tk
from tkinter import ttk, Toplevel
from tkcalendar import DateEntry
import sys

class RegisterAcct(object):
    def __init__(self,parent):
        top = self.top = Toplevel(parent)
        self.parent = parent
        topFrame = ttk.Frame(top)
        topFrame.grid(row=0,column=0)
        ttk.Label(topFrame,text="Username").grid(row=0,column=0)
        ttk.Label(topFrame,text="Password").grid(row=1,column=0)
        ttk.Label(topFrame,text="Confirm").grid(row=2,column=0)
        ttk.Label(topFrame,text="Email").grid(row=3,column=0)
        ttk.Label(topFrame,text=":").grid(row=0,column=1)
        ttk.Label(topFrame,text=":").grid(row=1,column=1)
        ttk.Label(topFrame,text=":").grid(row=2,column=1)
        ttk.Label(topFrame,text=":").grid(row=3,column=1)

        self.entUser = ttk.Entry(topFrame, width=20)
        self.entUser.grid(row=0, column=2)
        self.entPass = ttk.Entry(topFrame,show='*',width=20)
        self.entPass.grid(row=1, column=2)
        self.entConf = ttk.Entry(topFrame,show='*',width=20)
        self.entConf.grid(row=2, column=2)
        self.entEmail = ttk.Entry(topFrame, width=20)
        self.entEmail.grid(row=3, column=2)

        self.okbtn=ttk.Button(topFrame,text="OK",width=7,command=self.proses)
        self.okbtn.grid(row=4,column=1)
        # self.okbtn["state"] = "disabled"
        topFrame.wait_visibility() # window needs to be visible for the grab
        topFrame.grab_set()
        topFrame.bind("<FocusOut>", self.alarm)
        self._set_transient(parent)
    
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
    
    def proses(self):
        print(self.entUser.get())
        print(self.entPass.get())
        print(self.entEmail.get())
        self.top.destroy()

class TestRun(object):
    def __init__(self,master):
        self.master=master
        self.setbtn=ttk.Button(master,text="Register",command=self.popup)
        self.setbtn.pack()

    def popup(self):
        self.gopopup=RegisterAcct(self.master)
        self.setbtn["state"] = "disabled"
        self.master.wait_window(self.gopopup.top)
        self.setbtn["state"] = "normal"



if __name__ == "__main__":
    root=tk.Tk()
    m=TestRun(root)
    root.mainloop()