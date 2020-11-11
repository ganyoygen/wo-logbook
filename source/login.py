import os
import socket
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk,messagebox,Toplevel
from ttkthemes import ThemedTk # make sure to pip install ttkthemes
from datetime import datetime
from sys_mysql import insert_data,getdata_one
from sys_account import RegisterAcct,RemoveAcct
from sys_pwhash import verify_password
from sys_date import GetSeconds,GetDuration
from sys_config import SetConfig


class Login(object):
    def __init__(self,parent):
        top = self.top = Toplevel(parent)
        top.title("Login Program")
        top.iconbitmap(str(os.getcwd()+"\\"+"icon-icons.com_main.ico"))
        self.parent = parent
        self.top.protocol("WM_DELETE_WINDOW", self.keluar)

        self.user = ""
        self.dept = ""
        frame = ttk.Frame(top)
        frame.grid(row=0,column=0)

        ttk.Label(frame, text="Username").grid(row=0,column=0,sticky=W,padx=6,pady=6)
        ttk.Label(frame, text="Password").grid(row=1,column=0,sticky=W,padx=6,pady=6)

        self.entryUsername = ttk.Entry(frame,width=17)
        self.entryUsername.grid(row=0, column=1,sticky=W)
        self.entryUsername.bind('<Return>', self.letEntryPass)

        self.entryPassword = ttk.Entry(frame,show='*',width=17)
        self.entryPassword.grid(row=1, column=1,sticky=W)
        self.entryPassword.bind('<Return>', self.proses)

        ttk.Button(frame,text="ConfigDB",\
            command=self.config_db,width=10).grid(row=2, column=0,padx=6)
        ttk.Button(frame,text="Login",\
            command=self.proses,width=10).grid(row=2, column=1,padx=6)
        ttk.Button(frame,text="Register",\
            command=self.regacct,width=10).grid(row=2, column=2,padx=6)

        self.entryUsername.focus_set()
        # top.wait_visibility() 
        # top.grab_set()
        top.bind("<FocusOut>", self.alarm)
        top.resizable(0,0)
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

    def keluar(self,event=None):
        pass
        # close app by master windows

    def letEntryPass(self,event=None):
        self.entryPassword.focus_set()

    #proses cek user dan pass
    def proses(self,event=None):
        sql = "SELECT * FROM acct WHERE username = %s"
        val = (self.entryUsername.get(),)
        data = getdata_one(sql,val)
        if data != None :
            uid = data[0]
            user = data[1]
            password = data[2]
            dept = data[4]
            datecreate = GetSeconds(str(data[5]))
            matchpw = verify_password(self.entryPassword.get(),password)
            host_name = socket.gethostname() 
            host_ip = socket.gethostbyname(host_name)
            # login username samakan saja menjadi lower
            if (str(self.entryUsername.get()).lower().strip() == user.lower()) \
                and (matchpw == True):
                if data[6] != True: # bagian ceking aktivasi + remove acct
                    datetodrop = datecreate.value + 604800 # 86400*7 (7 hari). Lebih baik buat custom
                    duration = GetDuration(datetodrop - time.time())
                    messagebox.showerror(title="Belum Aktivasi", \
                    message="Tidak dapat menggunakan program.\r\nsilahkan hubungi Administrator\r\nuntuk Aktivasi Departement.\
                        \r\n \
                        \r\nSisa waktu: {}".format(duration.value))
                    # bagian remove account
                    if ((datetodrop - time.time()) <=0 and RemoveAcct(uid).result == True):
                            messagebox.showwarning(title="Account Info",message="Account Deleted successfully")
                    return
                if data[7] == True:
                    messagebox.showerror(title="Account dikunci", \
                    message="Tidak dapat menggunakan program.\r\nAccount anda telah dikunci.")
                    return
                if data[12] == None:
                    messagebox.showerror(title="Double Login Warning!", \
                    message="Tidak dapat login program.\r\nAccount anda sedang digunakan.")
                    return
                sql = "UPDATE acct SET last_login=%s,last_host=%s,last_ip=%s,last_logout=%s WHERE uid=%s"
                val = (datetime.now(),host_name,host_ip,"",data[0])
                if (insert_data(sql,val)) == True:
                    self.user = user
                    self.dept = dept
                    self.top.destroy()
                else: return
            else: #untuk salah password
                self.entryPassword.delete(0, END)
                self.entryPassword.focus_set()
        else:
            self.entryUsername.delete(0, END)
            self.entryPassword.delete(0, END)
            self.entryUsername.focus_set()

    def regacct(self):
        regacct = RegisterAcct(self.parent)
        regacct.parent.wait_window(regacct.top)
        if regacct.value != "":
            self.entryUsername.delete(0,END)
            self.entryUsername.insert(0,regacct.value)

    def config_db(self):
        setconfig = SetConfig(self.parent)
        setconfig.parent.wait_window(setconfig.top)


class TestRun(object):
    def __init__(self,master):
        self.master=master
        self.setbtn=ttk.Button(master,text="Login",command=self.popup)
        self.setbtn.pack()

    def popup(self):
        gopopup=Login(self.master)
        self.setbtn["state"] = "disabled"
        self.master.wait_window(gopopup.top)
        try: self.setbtn["state"] = "normal"
        except: pass

if __name__ == "__main__":
    # root=tk.Tk()
    root = ThemedTk(theme='aquativo')
    TestRun(root)
    # Login(root)
    root.mainloop()
