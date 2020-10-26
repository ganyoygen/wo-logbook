import mysql.connector
import tkinter
from mysqlcon import read_db_config
from tkinter import *
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk # make sure to pip install ttkthemes
from regacct import RegisterAcct

root = ThemedTk(theme='aquativo')

class Login:
    def __init__(self,parent,title):
        self.parent = parent
        self.parent.title(title)
        self.parent.protocol("WM_DELETE_WINDOWS", self.keluar)
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

        self.entryPassword = ttk.Entry(self.parent,show='+',width=17)
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
        try:
            db_config = read_db_config()
            con = mysql.connector.connect(**db_config)
            cur = con.cursor()
            sql = "SELECT * FROM acct WHERE username = %s"
            cur.execute(sql,(self.entryUsername.get(),))
            data = cur.fetchone()
        except mysql.connector.Error as err:
            messagebox.showerror(title="Error",message="SQL Log: {}".format(err))
        print(data)
        if data != None : 
            user = data[1]
            password = data[2]
            dept = data[3]
            # login username samakan saja menjadi lower
            if (str(self.entryUsername.get()).lower().strip() == user.lower()) \
                and (str(self.entryPassword.get()) == password):
                root.destroy()
                # import main
                from main import start
                start(user,dept)
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

def main():
    Login(root, "Login Program")
    root.mainloop()
main()

