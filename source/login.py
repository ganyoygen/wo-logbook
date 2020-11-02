import tkinter
import socket
import time
from tkinter import *
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk # make sure to pip install ttkthemes
from datetime import datetime
from sys_mysql import insert_data,getdata_one
from sys_account import RegisterAcct,RemoveAcct
from sys_pwhash import generate_hash,verify_password
from sys_date import GetSeconds,GetDuration

root = ThemedTk(theme='aquativo')

class Login:
    def __init__(self,parent,title):
        self.parent = parent
        self.parent.title(title)
        self.parent.protocol("WM_DELETE_WINDOW", self.keluar)
        lebar=250
        tinggi=100
        setTengahX = (self.parent.winfo_screenwidth()-lebar)//2
        setTengahY = (self.parent.winfo_screenheight()-tinggi)//2
        self.parent.geometry("%ix%i+%i+%i" %(lebar, tinggi,setTengahX, setTengahY))
        self.aturKomponen()
        
    def aturKomponen(self):
        ttk.Label(self.parent, text="Username").grid(row=0, column=0, sticky=W,padx=6)
        ttk.Label(self.parent, text="Password").grid(row=1, column=0, sticky=W,padx=6)

        self.entryUsername = ttk.Entry(self.parent,width=17)
        self.entryUsername.grid(row=0, column=1,sticky=W)
        self.entryUsername.bind('<Return>', self.letEntryPass)

        self.entryPassword = ttk.Entry(self.parent,show='*',width=17)
        self.entryPassword.grid(row=1, column=1,sticky=W)
        self.entryPassword.bind('<Return>', self.proses)

        self.buttonLogin = ttk.Button(self.parent, text="Login", command=self.proses,\
                             width=10)
        self.buttonLogin.grid(row=2, column=1)

        self.btnRegAcct = ttk.Button(self.parent, text="Register", command=self.regacct,\
                             width=10)
        self.btnRegAcct.grid(row=2, column=2)

        self.entryUsername.focus_set()

    def keluar(self,event=None):
        self.parent.destroy()

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
                sql = "UPDATE acct SET last_login=%s,last_host=%s,last_ip=%s WHERE uid=%s"
                val = (datetime.now(),host_name,host_ip,data[0])
                if (insert_data(sql,val)) == True:
                    root.destroy()
                    # import main
                    from main import start
                    start(user,dept)
                else: return
            elif (user==""):
                self.entryUsername.focus_set()
            elif (password==""):
                self.entryPassword.focus_set()
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

def main():
    Login(root, "Login Program")
    root.mainloop()
main()

