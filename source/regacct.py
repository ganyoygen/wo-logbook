import os
import tkinter as tk
from tkinter import *
from tkinter import ttk,Toplevel,messagebox
from tkcalendar import DateEntry
from socket_mysql import insert_data,getdata_one
from custom_entry import LimitEntry
from datetime import datetime

class RegisterAcct(object):
    def __init__(self,parent):
        top = self.top = Toplevel(parent)
        top.title("Create your User Account")
        self.parent = parent
        self.value = ""
        topFrame = ttk.Frame(top)
        topFrame.grid(row=0,column=0)
        ttk.Label(topFrame,text="Username").grid(row=0,column=0,sticky=W)
        ttk.Label(topFrame,text="Password").grid(row=1,column=0,sticky=W)
        ttk.Label(topFrame,text="Confirm").grid(row=2,column=0,sticky=W)
        ttk.Label(topFrame,text="Email").grid(row=3,column=0,sticky=W)
        ttk.Label(topFrame,text="(max 10)").grid(row=0,column=1)
        ttk.Label(topFrame,text="(max 16)").grid(row=1,column=1)
        # ttk.Label(topFrame,text=":").grid(row=2,column=1)
        # ttk.Label(topFrame,text=":").grid(row=3,column=1)

        self.entUser = LimitEntry(topFrame,maxlen=10,width=20)
        self.entUser.grid(row=0, column=2)
        self.entPass = LimitEntry(topFrame,maxlen=16,show='*',width=20)
        self.entPass.grid(row=1, column=2)
        self.entConf = ttk.Entry(topFrame,show='*',width=20)
        self.entConf.grid(row=2, column=2)
        self.entEmail = LimitEntry(topFrame,maxlen=32,width=20)
        self.entEmail.grid(row=3, column=2)

        self.btnSignUp=ttk.Button(topFrame,text="Sign Up",width=7,command=self.proses)
        self.btnSignUp.grid(row=4,column=1)
        # self.btnSignUp["state"] = "disabled"
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
        getTime = datetime.now()
        sql = "SELECT * FROM acct WHERE username = %s"
        val = (self.entUser.get(),)
        data = getdata_one(sql,val)
        if (self.entUser.get()==""): self.entUser.focus_set()
        elif (self.entPass.get()==""): self.entPass.focus_set()
        elif (self.entConf.get()==""): self.entConf.focus_set()
        elif (self.entEmail.get()==""): self.entEmail.focus_set()
        elif data == None :
            if str(self.entPass.get()).lower() != str(self.entConf.get()).lower():
                # parent=self.top karena msgbox with toplevel
                messagebox.showerror(title="Error",parent=self.top,\
                    message="Konfirmasi Password tidak sesuai")
                self.entConf.focus_set()
            elif len(self.entUser.get()) < 3:
                messagebox.showerror(title="Error",parent=self.top,\
                    message="Username harus antara 3 - 10 karakter")
                self.entUser.focus_set()
            elif self.entUser.get().isalnum() == False:
                messagebox.showerror(title="Error",parent=self.top,\
                    message="Username yang diperbolehkan hanya kombinasi huruf dan angka")
                self.entUser.focus_set()
            else:
                sql = "INSERT INTO acct (username, passhash, dept, date_create)"+\
                      "VALUES(%s,%s,%s,%s)"
                val = (self.entUser.get().strip(),self.entPass.get().strip(),"USER",getTime)
                if (insert_data(sql,val)) == True:
                    messagebox.showinfo(title="Informasi", message="Data sudah di tersimpan.")
                    self.value = self.entUser.get()
                    self.top.destroy()
        else:
            user = data[1]
            password = data[2]
            dept = data[3]
            if str(self.entUser.get()).lower().strip() == user.lower():
                # parent=self.top karena msgbox with toplevel
                messagebox.showerror(title="Error",parent=self.top, \
                    message="User {} sudah terdaftar.\nSilahkan pilih yang lain".format(self.entUser.get()))
            self.entUser.focus_set()

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
    TestRun(root)
    root.mainloop()