import tkinter as tk
import mysql.connector
import time
import datetime
# from socket_mysql import *
from socket_mysql import read_db_config,getdata_all,getdata_one,insert_data
from popup_date import PopupDateTime # popup set tgl jam
from tkinter import *
from tkinter import ttk, messagebox


kolomUser = ("UID","Username","Class","Date Created","Activated","Locked","Last Login","Last Host","Last IP")
class UserMgmt(tk.Frame):
    def __init__(self,parent,user,dept):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.user = user
        self.dept = dept

        if dept == "ROOT":
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
        ttk.Label(self.topFrame, text='UID - Username').grid(row=1,column=1,sticky=W,padx=10,pady=5)
        ttk.Label(self.topFrame, text=':').grid(row=1,column=2,sticky=W,padx=10,pady=5)
        frEntUid = ttk.Frame(self.topFrame)
        frEntUid.grid(row=1,column=3,sticky=W)
        self.entUid = ttk.Entry(frEntUid,width=5)
        self.entUid.grid(row=1,column=1,sticky=W)
        self.entName = ttk.Entry(frEntUid,width=20)
        self.entName.grid(row=1,column=2,sticky=W)

        ttk.Label(self.topFrame, text='Class / Department').grid(row=2,column=1,sticky=W,padx=10,pady=5)
        ttk.Label(self.topFrame, text=':').grid(row=2,column=2,sticky=W,padx=10,pady=5)
        self.entDept = ttk.Combobox(self.topFrame, \
            values = ["","ROOT","ENG","DOCON","CS","RCP"],\
            state="readonly", width=10)
        self.entDept.current(0)
        self.entDept.grid(row=2, column=3,sticky=W)

        ttk.Label(self.topFrame, text='Email').grid(row=3,column=1,sticky=W,padx=10,pady=5)
        ttk.Label(self.topFrame, text=':').grid(row=3,column=2,sticky=W,padx=10,pady=5)

        ttk.Label(self.topFrame, text='Status').grid(row=4,column=1,sticky=W,padx=10,pady=5)
        ttk.Label(self.topFrame, text=':').grid(row=4,column=2,sticky=W,padx=10,pady=5)
        self.entSts = ttk.Entry(self.topFrame,width=10)
        self.entSts.grid(row=4,column=3,sticky=W)

        ttk.Label(self.topFrame, text='Last Login-Host-IP').grid(row=5,column=1,sticky=W,padx=10,pady=5)
        ttk.Label(self.topFrame, text=':').grid(row=5,column=2,sticky=W,padx=10,pady=5)
        frEntLast = ttk.Frame(self.topFrame)
        frEntLast.grid(row=5,column=3,sticky=W)
        self.entLastLog = ttk.Entry(frEntLast,width=20)
        self.entLastLog.grid(row=1,column=1,sticky=W)
        self.entLastPC = ttk.Entry(frEntLast,width=8)
        self.entLastPC.grid(row=1,column=2,sticky=W)
        self.entLastIP = ttk.Entry(frEntLast,width=12)
        self.entLastIP.grid(row=1,column=3,sticky=W)

        ttk.Label(self.topFrame, text='Reset Password').grid(row=6,column=1,sticky=W,padx=10,pady=5)
        ttk.Label(self.topFrame, text=':').grid(row=6,column=2,sticky=W,padx=10,pady=5)
        
    def komponenTengah(self):
        pass
    
    def komponenBawah(self):
        listuser = ttk.Frame(self.botFrame)
        listuser.grid(row=0,column=1,sticky=W,padx=10)
        
        self.tabelUser = ttk.Treeview(listuser,column=kolomUser,show='headings')
        self.tabelUser.bind('<Double-1>',self.user_detail)
        sbVer = ttk.Scrollbar(listuser, orient='vertical',command=self.tabelUser.yview)
        sbVer.pack(side=RIGHT, fill=Y)
        sbHor = ttk.Scrollbar(listuser, orient='horizontal',command=self.tabelUser.xview)
        sbHor.pack(side=BOTTOM, fill=X)

        self.tabelUser.pack(side=TOP, fill=BOTH)
        self.tabelUser.configure(yscrollcommand=sbVer.set)
        self.tabelUser.configure(xscrollcommand=sbHor.set)

        ttk.Label(self.botFrame,text="").grid(row=1,column=1,pady=50)

        self.refresh()

    def entryset(self,opsi):
        if opsi == "clear":
            self.entUid.delete(0,END)
            self.entName.delete(0,END)
            self.entSts.delete(0,END)
            self.entLastLog.delete(0,END)
            self.entLastPC.delete(0,END)
            self.entLastIP.delete(0,END)

    def user_detail(self,event=None):
        self.entryset("clear")
        curItem = self.tabelUser.item(self.tabelUser.focus())
        self.entUid.insert(END,curItem['values'][0])
        self.entName.insert(END,curItem['values'][1])

        if curItem['values'][2] == "ROOT": self.entDept.current(1)
        elif curItem['values'][2] == "ENG": self.entDept.current(2)
        elif curItem['values'][2] == "DOCON": self.entDept.current(3)
        elif curItem['values'][2] == "CS": self.entDept.current(4)
        elif curItem['values'][2] == "RCP": self.entDept.current(5)
        else: self.entDept.current(0)

        if curItem['values'][5] == True: self.entSts.insert(END,"Locked")
        self.entLastLog.insert(END,curItem['values'][6])
        self.entLastPC.insert(END,curItem['values'][7])
        self.entLastIP.insert(END,curItem['values'][8])

    def refresh(self):
        # sql = "SELECT * FROM acct"
        sql = "SELECT `index`,`username`,`dept`,`date_create`,`activated`,`lock`,\
            `date_lock`,`last_login`,`last_host`,`last_ip` FROM `acct`"
        val = ()
        results = getdata_all(sql,val)
        self.tabelUser.delete(*self.tabelUser.get_children()) #refresh, hapus dulu tabel lama
        for kolom in kolomUser:
            self.tabelUser.heading(kolom,text=kolom)
        self.tabelUser.column("UID", width=30,anchor="w")
        self.tabelUser.column("Username", width=100,anchor="w")
        self.tabelUser.column("Class", width=50,anchor="w")
        self.tabelUser.column("Date Created", width=120,anchor="w")
        self.tabelUser.column("Activated", width=30,anchor="w")
        self.tabelUser.column("Locked", width=30,anchor="w")
        self.tabelUser.column("Last Login", width=120,anchor="w")
        self.tabelUser.column("Last Host", width=80,anchor="w")
        self.tabelUser.column("Last IP", width=80,anchor="w")
        
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
