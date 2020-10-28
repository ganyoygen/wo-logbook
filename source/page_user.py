import tkinter as tk
import mysql.connector
import time
import datetime
# from socket_mysql import *
from socket_mysql import read_db_config,getdata_all,getdata_one,insert_data
from popup_date import PopupDateTime # popup set tgl jam
from tkinter import *
from tkinter import ttk, messagebox


kolomUser = ("UID","Username","Department","DateCreated","Activated","Locked","LastLogin","LastHost","LastIP")
class UserMgmt(tk.Frame):
    def __init__(self,parent,user,dept):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.user = user
        self.dept = dept

        self.komponenUtama()
        self.komponenAtas()
        self.komponenTengah()
        self.komponenBawah()
        
    def komponenUtama(self):
        self.topFrame = ttk.Frame(self)
        self.topFrame.pack(side=TOP,fill=X)
        self.midFrame = ttk.Frame(self)
        self.midFrame.pack(side=TOP, fill=X)
        self.botFrame = ttk.Frame(self)
        self.botFrame.pack(side=TOP, fill=X)
        
        ttk.Label(self.topFrame, text='').grid(row=0, column=0)
        ttk.Label(self.midFrame, text='').grid(row=0, column=0)
        ttk.Label(self.botFrame, text='').grid(row=0, column=0)

    def komponenAtas(self):
        entOne = ttk.Frame(self.topFrame)
        entOne.grid(row=1,column=1,sticky=W)
        ttk.Label(entOne,text="entone").grid(row=0,column=0,sticky=W)

        entTwo = ttk.Frame(self.topFrame)
        entTwo.grid(row=2,column=1,sticky=W)
        ttk.Label(entTwo,text="enttwo").grid(row=0,column=0,sticky=W)

    def komponenTengah(self):
        ttk.Label(self.midFrame,text="untuk tombol2").grid(row=0,column=0,sticky=W)
    
    def komponenBawah(self):
        listuser = ttk.Frame(self.botFrame).grid(row=0,column=1,sticky=W,padx=10)
        
        self.tabelUser = ttk.Treeview(listuser,column=kolomUser,show='headings')
        self.tabelUser.bind('<Double-1>',self.user_detail)
        sbVer = ttk.Scrollbar(listuser, orient='vertical',command=self.tabelUser.yview)
        sbVer.pack(side=RIGHT, fill=Y)
        sbHor = ttk.Scrollbar(listuser, orient='horizontal',command=self.tabelUser.xview)
        sbHor.pack(side=BOTTOM, fill=X)

        self.tabelUser.pack(side=TOP, fill=BOTH)
        self.tabelUser.configure(yscrollcommand=sbVer.set)
        self.tabelUser.configure(xscrollcommand=sbHor.set)

        self.refresh()

    def user_detail(self):
        print("detail user")

    def refresh(self):
        print("refresh clicked")
        # sql = "SELECT * FROM acct"
        sql = "SELECT `index`,`username`,`dept`,`date_create`,`activated`,`lock`,\
            `date_lock`,`last_login`,`last_host`,`last_ip` FROM `acct`"
        val = ()
        results = getdata_all(sql,val)
        self.tabelUser.delete(*self.tabelUser.get_children()) #refresh, hapus dulu tabel lama
        for kolom in kolomUser:
            self.tabelUser.heading(kolom,text=kolom)
        self.tabelUser.column("UID", width=50,anchor="w")
        self.tabelUser.column("Username", width=80,anchor="w")
        self.tabelUser.column("Department", width=80,anchor="w")
        self.tabelUser.column("DateCreated", width=80,anchor="w")
        self.tabelUser.column("Activated", width=80,anchor="w")
        self.tabelUser.column("Locked", width=80,anchor="w")
        self.tabelUser.column("LastLogin", width=80,anchor="w")
        self.tabelUser.column("LastHost", width=80,anchor="w")
        self.tabelUser.column("LastIP", width=80,anchor="w")
        
        i=0
        for dat in results: 
            if(i%2):
                baris="genap"
            else:
                baris="ganjil"
            self.tabelUser.insert('', 'end', values=dat, tags=baris)
            i+=1
        self.tabelUser.tag_configure("ganjil", background="gainsboro")
        self.tabelUser.tag_configure("genap", background="floral white")
