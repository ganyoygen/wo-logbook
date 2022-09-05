import tkinter as tk
import os
import csv # untuk write ke Excel
import time
from threading import Thread
from datetime import date,datetime
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
from sys_mysql import getdata_one,getdata_all,insert_data
from sys_mssql import mssql_one
from sys_date import GetDuration,PopupDateTime,CustomDateEntry,store_date,get_date
from sys_progbar import SetProgBar
from sys_pullwo import PullWoTable

judul_kolom = ("WO","IFCA","Tanggal","UNIT","Work Request","Staff","Work Action","Tanggal Done","Jam Done","Received")
header_csv = ["Index","No WO","No IFCA","Tanggal Buat","Jam Buat","Unit",\
            "Work Request","Staff","Work Action","Tanggal Selesai","Jam Selesai",\
            "Status WO","Diterima","Penerima","Tanggal Diterima","auth_login"]

class PageMain(tk.Frame):
    def __init__(self,parent,user,dept):
        ttk.Frame.__init__(self,parent)
        self.parent = parent
        self.user = user
        self.dept = dept
        self.online = datetime.now()
        imgdateset = tk.PhotoImage(file = str(os.getcwd()+"\\"+"icon"+"\\"+"date.png"))
        self.imgdateget = imgdateset.subsample(2, 2) # Resizing image by.subsample to fit on button
        icosearch2 = tk.PhotoImage(file = str(os.getcwd()+"\\"+"icon"+"\\"+"search2.png"))
        self.icosearch2 = icosearch2.subsample(2, 2) # Resizing image by.subsample to fit on button
        self.btnselect = StringVar(parent,value="TN")

        self.komponenMain()
        self.komponenAtas()
        self.komponenTengah()
        self.komponenBawah()

        self.parent.bind('<ButtonPress-1>', self.ceksesi)
        self.topFrame.bind('<ButtonPress-1>', self.ceksesi)
        self.midFrame.bind('<ButtonPress-1>', self.ceksesi)
        self.botFrame.bind('<ButtonPress-1>', self.ceksesi)

    def ceksesi(self,event=None):
        # # debug True (bypass ceksesi)
        # return True
        # # end debug
        from main import checksession
        online = (str(self.online)[:-7])
        if checksession(self.user,online) == False: # komparasi lastlogin db = program
            self.parent.destroy() # Matikan program karena sesi berakhir
            return False

    def komponenMain(self):
        self.topFrame = ttk.Frame(self)
        self.topFrame.pack(side=TOP,fill=X)
        self.midFrame = ttk.Frame(self)
        self.midFrame.pack(side=TOP, fill=X)
        self.botFrame = ttk.Frame(self)
        self.botFrame.pack(side=TOP, fill=X)
        footer = ttk.Frame(self)
        footer.pack(side=BOTTOM, fill=X)
        
        ttk.Label(self.topFrame, text='').grid(row=0, column=0)
        ttk.Label(self.midFrame, text='').grid(row=0, column=0)
        ttk.Label(self.botFrame, text='').grid(row=0, column=0)
        ttk.Label(footer, text='').grid(row=0, column=0)

    def komponenAtas(self):
        #samping kiri
        topleft = ttk.Frame(self.topFrame)
        topleft.grid(row=1,column=1,sticky=W)
        ttk.Label(topleft, text='No WO').grid(row=0, column=0, sticky=W,padx=20)
        ttk.Label(topleft, text=':').grid(row=0, column=1, sticky=W,pady=5,padx=10)
        self.entWo = ttk.Entry(topleft, width=12)
        self.entWo.grid(row=0, column=2,sticky=W)

        ttk.Label(topleft, text="IFCA").grid(row=1, column=0, sticky=W,padx=20)
        ttk.Label(topleft, text=':').grid(row=1, column=1, sticky=W,pady=5,padx=10)
        self.entIfca = ttk.Entry(topleft, width=12)
        self.entIfca.grid(row=1, column=2,sticky=W)
        radiobtn = ttk.Frame(topleft)
        radiobtn.grid(row=1,column=2)

        self.rbtnTN = ttk.Radiobutton(radiobtn, text="TN", variable=self.btnselect, value="TN", command=self.auto_ifca)
        self.rbtnTN.grid(row=0, column=0,sticky=W)
        self.rbtnBM = ttk.Radiobutton(radiobtn, text="BM", variable=self.btnselect, value="BM", command=self.auto_ifca)
        ttk.Label(radiobtn, text="  /  ").grid(row=0,column=1,sticky=E)
        self.rbtnBM.grid(row=0, column=2,sticky=W)
        self.btnSearchIfcaServ = Button(radiobtn,image=self.icosearch2,command=self.getDataIFCAServer)
        self.btnSearchIfcaServ.grid(row=0, column=3,pady=10,padx=5)

        #tglbuat
        ttk.Label(topleft, text="Tanggal - Jam").grid(row=2, column=0, sticky=W,padx=20)
        ttk.Label(topleft, text=':').grid(row=2, column=1, sticky=W,pady=5,padx=10)
        tglbuat = ttk.Frame(topleft)
        tglbuat.grid(row=2,column=2,sticky=W)
        self.entTglbuat = ttk.Entry(tglbuat, width=10)
        self.entTglbuat.grid(row=1, column=0,sticky=W)
        self.entJambuat = ttk.Entry(tglbuat,width=7)
        self.entJambuat.grid(row=1, column=1,sticky=W)
        self.btnDateCreate = Button(tglbuat,image=self.imgdateget,command=self.onDateCreate)
        self.btnDateCreate.grid(row=1, column=2,pady=10,padx=5)

        ttk.Label(topleft, text="Unit").grid(row=3, column=0, sticky=W,padx=20)
        ttk.Label(topleft, text=':').grid(row=3, column=1, sticky=W,pady=5,padx=10)             
        self.entUnit = ttk.Entry(topleft, width=15)
        self.entUnit.grid(row=3, column=2,sticky=W)

        ttk.Label(topleft, text="Work Request").grid(row=4, column=0, sticky=NW,padx=20)
        ttk.Label(topleft, text=':').grid(row=4, column=1, sticky=NW,padx=10,pady=6)
        self.entWorkReq = ScrolledText(topleft,height=4,width=35)
        self.entWorkReq.grid(row=4, column=2,sticky=W)

        ttk.Label(topleft, text="Staff").grid(row=5, column=0, sticky=W,padx=20)
        ttk.Label(topleft, text=':').grid(row=5, column=1, sticky=W,pady=5,padx=10)
        self.entStaff = ttk.Entry(topleft, width=20)
        self.entStaff.grid(row=5, column=2,sticky=W)

        #samping kanan
        topright = ttk.Frame(self.topFrame)
        topright.grid(row=1,column=2,sticky=W)
        ttk.Label(topright, text="").grid(row=0, column=0, sticky=W,pady=5,padx=20)
        ttk.Label(topright, text="").grid(row=1, column=0, sticky=W,pady=5,padx=20)
        ttk.Label(topright, text="Status").grid(row=2, column=0, sticky=W,pady=5,padx=20)
        ttk.Label(topright, text=':').grid(row=2, column=1, sticky=W,pady=5,padx=10)

        self.opsiStatus = ttk.Combobox(topright, \
            values = ["","DONE","CANCEL","PENDING"],\
            state="readonly", width=10)
        self.opsiStatus.current(0)
        self.opsiStatus.grid(row=2, column=2,sticky=W)

        ttk.Label(topright, text="Tanggal - Jam").grid(row=3, column=0, sticky=W,padx=20)
        ttk.Label(topright, text=':').grid(row=3, column=1, sticky=W,pady=5,padx=10)             
        tgldone = ttk.Frame(topright)
        tgldone.grid(row=3,column=2,sticky=W)
        self.entTgldone = ttk.Entry(tgldone, width=10)
        self.entTgldone.grid(row=0, column=0,sticky=W)
        self.entJamdone = ttk.Entry(tgldone, width=7)
        self.entJamdone.grid(row=0, column=1,sticky=W)
        self.btnDateDone = Button(tgldone,image=self.imgdateget,command=self.onDateDone)
        self.btnDateDone.grid(row=0, column=2,pady=10,padx=5)

        ttk.Label(topright, text="Work Action").grid(row=4, column=0, sticky=NW,padx=20)
        ttk.Label(topright, text=':').grid(row=4, column=1, sticky=NW,padx=10,pady=6)
        self.entWorkAct = ScrolledText(topright,height=4,width=35)
        self.entWorkAct.grid(row=4, column=2,sticky=W)
                
        ttk.Label(topright, text="Received").grid(row=5, column=0, sticky=W,padx=20)
        ttk.Label(topright, text=':').grid(row=5, column=1, sticky=W,pady=5,padx=10)
        recentry = ttk.Frame(topright)
        recentry.grid(row=5,column=2,sticky=W)
        self.entRecDate = ttk.Entry(recentry, width=20)
        self.entRecDate.grid(row=0, column=0,sticky=W)
        self.entRecBy = ttk.Entry(recentry, width=25)
        self.entRecBy.grid(row=0, column=1,sticky=W)
        self.varRec=IntVar()
        self.btnCekRec = ttk.Checkbutton(recentry,variable=self.varRec)
        self.btnCekRec.grid(row=0, column=2)

    def komponenTengah(self):
        #panel button
        self.btnClear = Button(self.midFrame, text='New',\
            command=self.onClear, width=10,\
            relief=RAISED, bd=2, bg="#666", fg="white",\
            activebackground="#444",activeforeground="white")
        self.btnClear.grid(row=1, column=1,pady=0,padx=5)

        self.btnSave = Button(self.midFrame, text='Save',\
            command=self.onSave, width=10,\
            relief=RAISED, bd=2, bg="#666", fg="white",\
            activebackground="#444",activeforeground="white" )
        self.btnSave.grid(row=1,column=2,pady=0,padx=5)

        self.btnUpdate = Button(self.midFrame, text='Update',\
            command=self.onUpdate,state="disable", width=10,\
            relief=RAISED, bd=2, bg="#666", fg="white",\
            activebackground="#444",activeforeground="white")
        self.btnUpdate.grid(row=1,column=3,pady=0,padx=5)

        self.btnDelete = Button(self.midFrame, text='Delete',\
            command=self.onDelete,state="disable", width=10,\
            relief=RAISED, bd=2, bg="#FC6042", fg="white",\
            activebackground="#444",activeforeground="white")
        self.btnDelete.grid(row=1,column=4,pady=0,padx=5)

        self.btnReceived = Button(self.midFrame, text='Received',\
            command=self.onReceived,state="disable", width=10,\
            relief=RAISED, bd=2, bg="#667", fg="white",\
            activebackground="#444",activeforeground="white")
        self.btnReceived.grid(row=1,column=5,pady=0,padx=5)

        self.btnPull = Button(self.midFrame, text='PULL',\
            command=self.getpull,\
            state="normal", width=10,\
            relief=RAISED, bd=2, \
            bg="#558", fg="white", \
            activebackground="#444",activeforeground="white")
        self.btnPull.grid(row=1,column=6,pady=10,padx=5)

    def komponenBawah(self):
        # search and export
        row1 = ttk.Frame(self.botFrame)
        row1.grid(row=0,column=1,sticky=W,padx=10)
        self.opsicari = ttk.Combobox(row1, \
            values = ["IFCA","Tanggal", "Unit", "Work Req."], \
            state="readonly", width=10)
        self.opsicari.current(1)
        self.opsicari.grid(row=2, column=1,sticky=W)
        self.opsicari.bind('<<ComboboxSelected>>',self.boxsearchsel)

        self.entCari = ttk.Entry(row1, width=20)
        self.entCari.grid(row=2, column=2)
        self.dateStart = CustomDateEntry(row1,width=10,locale='en_UK')
        self.dateEnd = CustomDateEntry(row1,width=10,locale='en_UK')
        ttk.Label(row1, text='~').grid(row=2,column=3)
        self.entCari.bind('<Return>',self.onSearch)
        self.dateStart.bind('<Return>',self.onSearch)
        self.dateEnd.bind('<Return>',self.onSearch)

        # self.entCari.bind('<KeyRelease>',self.onSearch) #cari saat input apapun
        
        self.btnSearch = Button(row1, text='Search',\
            command=self.onSearch,\
            state="normal", width=10,\
            relief=RAISED, bd=2, bg="#667", fg="white",\
            activebackground="#444",activeforeground="white")
        self.btnSearch.grid(row=2,column=6,pady=10,padx=5)

        self.btnMainExp = Button(row1, text='Export',\
            command=self.onMainExport,\
            state="normal", width=10,\
            relief=RAISED, bd=2, \
            bg="#558", fg="white", \
            activebackground="#444",activeforeground="white")
        self.btnMainExp.grid(row=2,column=7,pady=10,padx=5)

        self.btnImportCsv = Button(row1, text='Import',\
            command=self.onImport_csv,\
            state="normal", width=10,\
            relief=RAISED, bd=2, \
            bg="#558", fg="white", \
            activebackground="#444",activeforeground="white")
        self.btnImportCsv.grid(row=2,column=8,pady=10,padx=5)

        #tabel
        listifca = ttk.Frame(self.botFrame)
        listifca.grid(row=2,column=1,sticky=W,padx=10)
        self.tabelIfca = ttk.Treeview(listifca, columns=judul_kolom,show='headings')
        self.tabelIfca.bind("<Double-1>", self.mainlog_detail)
        sbVer = ttk.Scrollbar(listifca, orient='vertical',command=self.tabelIfca.yview)
        sbVer.pack(side=RIGHT, fill=Y)
        sbHor = ttk.Scrollbar(listifca, orient='horizontal',command=self.tabelIfca.xview)
        sbHor.pack(side=BOTTOM, fill=X)

        self.tabelIfca.pack(side=TOP, fill=BOTH)
        self.tabelIfca.configure(yscrollcommand=sbVer.set)
        self.tabelIfca.configure(xscrollcommand=sbHor.set)

        self.onClear()

    def getpull(self,event=None):
        self.gopopup=PullWoTable(self.parent,self.user,self.dept)
        self.btnPull["state"] = "disabled"
        self.parent.wait_window(self.gopopup.top)
        self.btnPull["state"] = "normal"

    def entrySet(self,opsi):
        # 1 on doubleclick main entry, normal
        if opsi == "mainclear":
            self.entWo.config(state="normal")
            self.entIfca.config(state="normal")
            self.entTglbuat.config(state="normal")
            self.entJambuat.config(state="normal")
            self.entUnit.config(state="normal")
            self.entTgldone.config(state="normal")
            self.entJamdone.config(state="normal")
            self.entRecBy.config(state="normal")
            self.entRecDate.config(state="normal")
            self.entWo.delete(0, END)
            self.entIfca.delete(0, END)
            self.entTglbuat.delete(0, END)
            self.entJambuat.delete(0, END)
            self.entUnit.delete(0, END)
            self.entWorkReq.delete('1.0', 'end')
            self.entStaff.delete(0, END)
            self.entTgldone.delete(0, END)
            self.entJamdone.delete(0, END)
            self.entWorkAct.delete('1.0', 'end')
            self.entRecBy.delete(0, END)
            self.entRecDate.delete(0, END)
            self.entRecBy.config(state="normal")
            self.entRecDate.config(state="normal")
            self.btnDelete.config(state="disable")
            self.btnReceived.config(state="disable")
            self.btnUpdate.config(state="disable")
            self.rbtnTN.grid(row=0, column=0,sticky=W)
            self.rbtnBM.grid(row=0, column=2,sticky=W)
            # A. readonly aja, input pake popup
            self.entTglbuat.config(state="readonly")
            self.entJambuat.config(state="readonly")
            self.entTgldone.config(state="readonly")
            self.entJamdone.config(state="readonly")
            # A #
            self.varRec.set(0)
        # mainentry readonly panel kiri kecuali work req dan staff
        elif opsi == "enablebtn":
            self.btnDateCreate.config(state="normal")
            self.btnDateDone.config(state="normal")
            self.btnSave.config(state="normal")
            self.rbtnBM.config(state="normal")
            self.rbtnTN.config(state="normal")
            self.btnCekRec.config(state="normal")
            self.btnSearchIfcaServ.config(state="normal")
        elif opsi == "disablebtn":
            self.btnDateCreate.config(state="disable")
            self.btnDateDone.config(state="disable")
            self.btnSave.config(state="disable")
            self.rbtnBM.config(state="disable")
            self.rbtnTN.config(state="disable")
            self.btnCekRec.config(state="disable")
            self.btnSearchIfcaServ.config(state="disable")
        elif opsi == "mainreadifca":
            self.entWo.config(state="readonly")
            self.entIfca.config(state="readonly")
            self.entTglbuat.config(state="readonly")
            self.entJambuat.config(state="readonly")
            self.entUnit.config(state="readonly")
            self.entTgldone.config(state="readonly")
            self.entJamdone.config(state="readonly")
            self.entRecBy.config(state="readonly")
            self.entRecDate.config(state="readonly")
            self.rbtnTN.grid_forget()
            self.rbtnBM.grid_forget()
        # 1 #
        else : pass

    def checkwo(self,data):
        if (len(data) < 1): # Jika wo kosong
            # print("Diterima, len data",len(data),"wo bisa kosong")
            return data
        elif (len(data) >= 1 and data.isdigit() == False):
            # print("Ditolak, digit",data.isdigit())
            return False
        else:
            # print("no awal",data)
            while 0 < len(data): # jika ada "0" didepan hapus aja
                if data[0] == '0':
                    data = data[1:]
                    continue
                break
            # print("no akhir",data)
            sql = ("SELECT * FROM logbook where no_wo LIKE %s")
            val = (data,)
            hasil = getdata_one(sql,val)
            if (hasil == None): # Jika wo no. baru
                # print("diterima,",data,"!-",hasil)
                return data
            if (data == hasil[1]):
                # print("ditolak,",data,"=",hasil[1])
                return False

    def checkifca(self,data):
        if ((data[:2] != "BM") and (data[:2] != "TN")):
            # print("bukan TIPE yang benar,",data[:2])
            return False
        elif (len(data) != 10):
            # print("panjang =",len(data))
            return False
        elif (data[2:].isdigit() == False):
            # print("8 char digit?",data[2:].isdigit())
            return False
        else:
            sql = ("SELECT * FROM logbook where no_ifca LIKE %s")
            val = (data,)
            hasil = getdata_one(sql,val)
            if hasil == None:
                # print("diterima,",data,"!-",hasil)
                return True
            if (data == hasil[2]):
                # print("ditolak,",data,"=",hasil[2])
                return False

    def boxsearchsel(self,event):
        if self.opsicari.get() == "Tanggal":
            self.entCari.delete(0, END)
            self.entCari.grid_forget()
            self.dateStart.grid(row=2,column=2)
            self.dateEnd.grid(row=2,column=4)
        else:
            self.entCari.delete(0, END)
            self.dateStart.grid_forget()
            self.dateEnd.grid_forget()
            self.entCari.grid(row=2, column=2,sticky=W)

    def onSearch(self,event=None):
        if self.ceksesi() == False: return # lakukan cek sesi
        self.entrySet("mainclear")
        self.opsiStatus.current(0)
        self.querySearch() # set dulu variabel self.sql dan self.val
        results = getdata_all(self.sql,self.val)
        self.showtable(results)

    def querySearch(self):
        opsi = self.opsicari.get()
        cari = self.entCari.get()
        if opsi == "Tanggal":
            if self.dateStart.get() == self.dateEnd.get():
                cari = store_date(self.dateStart.get())
                self.sql = "SELECT * FROM logbook WHERE date_create LIKE %s ORDER BY time_create DESC"
                self.val = ("%{}%".format(cari),)
            else: #part jika search between date
                sdate = store_date(self.dateStart.get())
                edate = store_date(self.dateEnd.get())
                self.sql = "SELECT * FROM logbook WHERE (date_create BETWEEN %s AND %s) ORDER BY no_ifca DESC"
                self.val = ('{}'.format(sdate),'{}'.format(edate))
        elif opsi == "IFCA":
            self.sql = "SELECT * FROM logbook WHERE no_ifca LIKE %s ORDER BY no_ifca DESC"
            self.val = ("%{}%".format(cari),)
        elif opsi == "Unit":
            self.sql = "SELECT * FROM logbook WHERE unit LIKE %s ORDER BY date_create DESC"
            self.val = ("%{}%".format(cari),)
        elif opsi == "Work Req.":
            self.sql = "SELECT * FROM logbook WHERE work_req LIKE %s ORDER BY date_create DESC"
            self.val = ("%{}%".format(cari),)
        else: pass

    def auto_wo(self):
        lasttn = self.get_last_ifca("TN")
        lastbm = self.get_last_ifca("BM")
        sql = ("SELECT no_wo FROM logbook where no_ifca LIKE %s")
        val = (lasttn,)
        wotn = getdata_one(sql,val)
        sql = ("SELECT no_wo FROM logbook where no_ifca LIKE %s")
        val = (lastbm,)
        wobm = getdata_one(sql,val)
        maxwo = max(wotn[0],wobm[0])
        if maxwo == "": newo = 1 #jika no wo kosong dari TN dan BM, set 1
        else: newo = int(maxwo)+1 #setelah max dari TN dan BM, + 1
        if len(str(newo)) <= 6:
            self.entWo.insert(0, newo)
            self.entIfca.focus_set()
        else:
            messagebox.showwarning(title="Peringatan", \
                    message="maaf lebar data untuk no WO hanya sampai 6 digit")

    def get_last_ifca(self,data):
        sql = "SELECT MAX(no_ifca) FROM logbook WHERE no_ifca LIKE %s"
        val = ("%{}%".format(data),)
        hasil = getdata_all(sql,val) # max IFCA dalam tupple
        return hasil[len(hasil)-1][0] # Max num ifca terakhir

    def auto_ifca(self):
        tipe = str(self.btnselect.get())
        lastifca = self.get_last_ifca(tipe)
        if lastifca == None: # prevent error jika belum ada data
            lastifca = "XX10000000"
        # print("Last Ifca",lastifca)
        newIfcaNum = (int(lastifca[2:])+1) # cari lastifca, hapus tipe(BM/TN) + 1
        getNewIfca = tipe+str(newIfcaNum) # Ifca baru siap dipakai
        # print("Get new ifca:",getNewIfca) 
        self.entIfca.delete(0, END)
        self.entIfca.insert(0,getNewIfca)
        self.getDataIFCAServer()

    def getDataIFCAServer(self,Event=None):
        # sql = "SELECT * FROM [property_live].[mgr].[sv_entry_hd] where report_no = 'TN10029737'"
        # sql = "SELECT * FROM [property_live].[mgr].[sv_entry_hd] where report_no = " + "'" +str(data) + "'"
        sql = "SELECT * FROM [property_live].[mgr].[sv_entry_hd] where report_no = " + "'" +str(self.entIfca.get()) + "'"
        data = mssql_one(sql)
        if data != None: 
            # print(data)
            getdate, gettime = str(data[5]).split() #pisah tanggal dan jam
            # print("Unit:",data[2])
            # print("FullDate:",data[5])
            # print("WorkReq:",data[9])
            # print("Tanggal:",get_date(getdate))
            # print("Jam:",gettime[:5]) # [:5] = hh:mm

            self.entrySet("mainclear")
            self.entIfca.insert(END, data[3])
            self.entTglbuat.config(state="normal")
            self.entJambuat.config(state="normal")
            self.entTglbuat.insert(END, get_date(getdate))
            self.entJambuat.insert(END, gettime[:5]) # [:5] = hh:mm
            self.entTglbuat.config(state="readonly")
            self.entJambuat.config(state="readonly")
            self.entUnit.insert(END, data[2])
            self.entWorkReq.insert(END, data[9])
            self.auto_wo()

    def showtable(self,data):
        self.tabelIfca.delete(*self.tabelIfca.get_children()) #refresh, hapus dulu tabel lama
        for kolom in judul_kolom:
            self.tabelIfca.heading(kolom,text=kolom)
        # self.tabelIfca.column("No", width=10,anchor="w")
        self.tabelIfca.column("WO", width=50,anchor="w")
        self.tabelIfca.column("IFCA", width=80,anchor="w")
        self.tabelIfca.column("Tanggal", width=80,anchor="w")
        self.tabelIfca.column("UNIT", width=80,anchor="w")
        self.tabelIfca.column("Work Request", width=150,anchor="w")
        self.tabelIfca.column("Staff", width=70,anchor="w")
        self.tabelIfca.column("Work Action", width=150,anchor="w")
        self.tabelIfca.column("Tanggal Done", width=80,anchor="w")
        self.tabelIfca.column("Jam Done", width=40,anchor="w")
        self.tabelIfca.column("Received", width=40,anchor="w")
    
        i=0
        for dat in data: 
            if(i%2):
                baris="genap"
            else:
                baris="ganjil"
            #hilangkan nomor mulai dari kolom wo dat[1:]
            self.tabelIfca.insert('', 'end', values=dat[1:], tags=baris)
            i+=1
        self.tabelIfca.tag_configure("ganjil", background="gainsboro")
        self.tabelIfca.tag_configure("genap", background="floral white")                              

    def onImport_csv(self):
        Thread(target=self.proses_import).start()

    def proses_import(self):
        # section return (abort)
        if (self.dept != "ROOT"):
            messagebox.showerror(title="Prohibited", \
                message="This command is reserved for Administrator")
            self.btnImportCsv.grid_forget()
            return
        fnames = filedialog.askopenfilename(filetypes=[("Excel CSV", "*.csv")])
        if not fnames:
            print("open file canceled")
            return
        with open(fnames) as cek_header:
            reader = csv.reader(cek_header)
            for row in reader:
                if row == header_csv:
                    break
                else: 
                    messagebox.showerror(title="Import File Error", \
                        message="The header file is invalid!")
                    return
        with open(fnames) as countrow:
            reader = csv.reader(countrow)
            next(reader) # skip the heading
            lines = len(list(reader)) # jumlah baris dalam file setelah header
            # lines = sum(1 for row in reader) # ini juga bisa hitung jumlah baris
            if lines > 5000:
                messagebox.showerror(title="Import File Error", \
                    message="Row count: {}. Maximum is 5000".format(lines))
                return
        # section processing
        start = time.perf_counter()
        progbar = SetProgBar(self.parent,lines)
        with open(fnames) as input_file:
            reader = csv.reader(input_file)
            next(reader) # skip the heading
            update = 0
            insert = 0
            for rowno, row in enumerate(reader):
                if (row[0].isdigit() == False): # abaikan selain index=digit
                    progbar.bytes = rowno + 1 # tambah digit karena jumlah lines menghitung apapun
                    continue
                if self.checkifca(row[2]) == False: #check IFCA, jika ada update aja
                    # print("IFCA",row[2],"Sudah terdaftar")
                    sql = "UPDATE logbook SET date_create=%s,time_create=%s,unit=%s,work_req=%s WHERE no_ifca =%s"
                    val = (store_date(row[3]),row[4],row[5],row[6],row[2])
                    if (insert_data(sql,val)) == True:
                        update += 1
                    else:
                        messagebox.showerror(title="Import File Error", \
                            message="Fail on Update {}".format(row[2]))
                else: # insert baru
                    sql = "INSERT INTO logbook (no_wo,no_ifca,date_create,time_create,unit,work_req,staff,\
                        work_act,date_done,time_done,status_ifca,received,wo_receiver,date_received,auth_login)"+\
                        "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    # val = (row)
                    val = (row[1],row[2],store_date(row[3]),row[4],row[5],row[6],row[7],row[8],\
                        store_date(row[9]),row[10],row[11],row[12],row[13],store_date(row[14]),row[15])
                    if (insert_data(sql,val)) == True:
                        insert += 1
                    else: 
                        messagebox.showerror(title="Import File Error", \
                            message="Fail on New Insert {}".format(row[2]))
                progbar.bytes = rowno + 1
            finish = time.perf_counter()
            usedsecs = finish-start
            if usedsecs > 60: usedsecs = GetDuration(usedsecs).value
            messagebox.showinfo(title="Import File Result", \
                message="Update IFCA: {0}\r\nNew Record: {1}\r\nTime Used: {2}"\
                    .format(update,insert,usedsecs))
        self.onSearch() #Refresh table by search

    def onMainExport(self): #export from database treeview
        results = self.tabelIfca.get_children() # dalam format [list]
        if len(results) > 0:
            #for testing export
            # i=1
            # for dat in results:
            #     value = self.tabelIfca.item(dat)['values']
            #     value.insert(0,i) # tambah nomor colom pertama
            #     print(value)
            #     value.insert(4,value.pop(13)) # pindahin jambuat ke kolom 4
            #     print(value)
            #     i+=1
            # end testing 

            directory = filedialog.asksaveasfilename(initialdir = os.getcwd(), \
                initialfile = self.entCari.get(), \
                defaultextension='.csv', \
                title="Save file Export", \
                filetypes=[("Excel CSV", "*.csv"),("All", "*.*")])
            if not directory:
                print("cancel export")
                return
            try:
                filename=open(directory,'w',newline='')
            except:
                messagebox.showerror(title="Export File Error", \
                    message="Permission denied: {}".format(directory))
                return
            cWrite=csv.writer(filename)
            cWrite.writerow(["Export time","",datetime.now()])
            cWrite.writerow([""])
            cWrite.writerow(header_csv)
            i=1
            for dat in results:
                value = self.tabelIfca.item(dat)['values']
                value.insert(0,i) # tambah nomor colom pertama
                value.insert(4,value.pop(13)) # pindahin jambuat ke kolom 4
                value.insert(11,value.pop(14)) # pindahin status ke kolom 11
                cWrite.writerow(value)
                i+=1
            cWrite.writerow([""])
            cWrite.writerow(["Save to",directory])
            cWrite.writerow(["Finish",len(results),"record(s)"])
            filename.close()
            messagebox.showinfo(title="Export File", \
                message="Sudah tersimpan di: {}".format(directory))
        else: print("result:",len(results))

    def onReceived(self):
        # try:
        ifca = self.entIfca.get()
        dept = self.entRecBy.get().split(".")
        if len(dept) <= 1: dept = [self.user,"ROOT"]
        if len(ifca.strip()) == 0:
            messagebox.showwarning(title="Peringatan",message="No IFCA Kosong.")
            self.entIfca.focus_set()
        elif (ifca[:2] == "TN"):
            if (self.dept == "CS") or (self.dept == "RCP"):
                if messagebox.askokcancel('Receive WO {}'.format(ifca),'WO sudah diterima?') == True: 
                    self.doReceive(self.idWO) # Update DATA berdasarkan ID wo
            else: messagebox.showerror(title="Receive WO {}".format(ifca), \
                                message="WO TN hanya bisa diterima oleh RCP/CS")
        elif (ifca[:2] == "BM"):
            if (self.dept == "DOCON") or (self.dept == "ENG"):
                # antisipasi duplikasi receive
                if (dept[1] == self.dept):
                    messagebox.showerror(title="Replacing !", \
                                message="WO Sudah diterima oleh {}".format(self.entRecBy.get()))
                elif messagebox.askokcancel('Receive WO {}'.format(ifca),'WO sudah diterima?') == True: 
                    self.doReceive(self.idWO) # Update DATA berdasarkan ID wo
            else: messagebox.showerror(title="Receive WO {}".format(ifca), \
                                message="WO BM hanya bisa diterima oleh DOCON/ENG")
        else: pass

    def doReceive(self,data):
        receiver = self.user + "." + self.dept
        tsekarang = datetime.now()
        sql = "UPDATE logbook SET date_received=%s,received=%s,wo_receiver=%s WHERE id =%s"
        val = (tsekarang,True,receiver,data)
        if (insert_data(sql,val)) == True:
            # messagebox.showinfo(title="Informasi", \
            # message="Wo {} sudah diterima.".format(data))
            self.onSearch() #update received sesuai tabel yg dicari

    def mainlog_detail(self, event):
        try:
            curItem = self.tabelIfca.item(self.tabelIfca.focus())
            ifca_value = curItem['values'][1]
            self.entrySet("mainclear")
            self.entrySet("disablebtn")
            self.entTglbuat.config(state="normal")
            self.entJambuat.config(state="normal")
            self.entTgldone.config(state="normal")
            self.entJamdone.config(state="normal")
            # sql = "SELECT * FROM logbook WHERE no_ifca = %s"
            # val = (ifca_value,)
            sql = "SELECT * FROM logbook WHERE (no_ifca = %s AND time_create = %s)"
            val = (ifca_value,curItem['values'][12]) # prevent ketika no IFCA sama sertakan JAM buat
            data = getdata_one(sql,val)
            self.idWO = data[0] # simpan data ID wo
            self.entIfca.insert(END, ifca_value)
            self.entWo.insert(END, data[1])
            self.entTglbuat.insert(END,get_date(str(data[3])))
            self.entJambuat.insert(END, data[13])
            self.entUnit.insert(END, data[4])
            self.entWorkReq.insert(END, data[5])
            self.entStaff.insert(END, data[6])
            self.entTgldone.insert(END,get_date(str(data[8])))
            self.entJamdone.insert(END, data[9])
            self.entWorkAct.insert(END, data[7])
            self.entRecDate.insert(END,get_date(str(data[12])))
            self.entRecBy.insert(END, data[11])
            if data[14] == "DONE":
                self.opsiStatus.current(1)
                self.btnReceived.config(state="normal")
                # ngapain diUpdate lagi wo sudah DONE
            elif data[14] == "CANCEL": 
                self.opsiStatus.current(2)
                self.btnReceived.config(state="normal")
            elif data[14] == "PENDING":
                self.opsiStatus.current(3)
            elif data[14] == "ONPROGRESS" or data[14] == "RETURNED" or data[14] == "TAKEN":
                self.opsiStatus.current(0)
            else:
                if self.dept == "ENG": # khusus class ENG
                    self.btnUpdate.config(state="normal")
                    self.btnDateDone.config(state="normal")
                self.opsiStatus.current(0)
            if data[10] == True:
                # self.btnCekRec.select() # .select()/.deselect() jika menggunakan Checkbutton()
                self.varRec.set(1) # ttk.Checkbutton
                # tidak dapat receive wo TN karena sudah direceive
                if ifca_value[:2] == "TN": self.btnReceived.config(state="disable")
            else: 
                # self.btnCekRec.deselect()
                self.varRec.set(0)
            if self.dept == "ROOT": # bisa edit untuk root
                self.entrySet("enablebtn")
                self.btnUpdate.config(state="normal")
                self.btnDelete.config(state="normal")
                self.btnSave.config(state="disable")
            else: self.entrySet("mainreadifca") # read only setelah entry terisi
        except:
            print('Tidak ada data di tabel')

    def onDelete(self):
        cIfca = self.entIfca.get()
        if messagebox.askokcancel('Delete Data','WO dengan no {0} #{1} akan dihapus?'.format(cIfca,self.idWO)) == True:
            sql = "DELETE FROM logbook WHERE id =%s" # lebih spesifik dengan id WO
            val = (self.idWO,)
            if (insert_data(sql,val)) == True:
                sql = "DELETE FROM onprogress WHERE no_ifca =%s"
                val = (cIfca,)
                if (insert_data(sql,val)) == True:
                    self.onSearch() #update received sesuai tabel yg dicari
                    messagebox.showinfo(title="Delete {0} #{1}".format(cIfca,self.idWO), \
                            message="Data sudah di hapus.")
        else: pass

    def onClear(self):
        if self.dept == "ENG": self.entrySet("enablebtn")# khusus class ENG
        else: self.entrySet("disablebtn")
        self.tabelIfca.delete(*self.tabelIfca.get_children())
        self.entCari.delete(0, END)
        self.dateStart.delete(0, END)
        self.dateEnd.delete(0, END)
        self.opsiStatus.current(0)
        # list wo hari ini
        self.opsicari.current(1)
        self.boxsearchsel(None)
        today = date.today()
        self.dateStart.insert(END,today.strftime("%d-%m-%Y"))
        self.dateEnd.insert(END,today.strftime("%d-%m-%Y"))
        self.onSearch()
        self.auto_wo()
        self.entUnit.focus_set()
        # os.system("cls")

    def onSave(self):
        cWo = self.checkwo(self.entWo.get()) # self.checkwo, jika salah return False
        cIfca = self.entIfca.get()
        cTglBuat = store_date(self.entTglbuat.get()) #check tgl dulu
        cJamBuat = self.entJambuat.get()
        cUnit = self.entUnit.get().upper().strip()
        cWorkReq = self.entWorkReq.get('1.0', 'end').upper().strip()
        cStaff = self.entStaff.get().upper().strip()
        cIfca = self.entIfca.get()
        if cWo == False: #check WO
            messagebox.showerror(title="Error", \
            message="WO sudah terdaftar atau Input WO salah")
        elif self.checkifca(cIfca) == False: #check IFCA
            messagebox.showerror(title="Error", \
            message="IFCA sudah terdaftar atau Input IFCA salah")
            self.entIfca.focus_set()
        elif len(cTglBuat) == 0 or len(cJamBuat.strip()) != 5: #check tgl jika kosong, batalkan save
            messagebox.showerror(title="Error",message="Format tanggal salah")
        elif len(cUnit) == 0:
            messagebox.showwarning(title="Peringatan",message="Unit harus diisi.")
            self.entUnit.focus_set()
            self.entUnit.delete(0, END)
        else:
            sql = "INSERT INTO logbook (no_wo,no_ifca,date_create,time_create,unit,work_req,staff,auth_login)"+\
                  "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (cWo,cIfca,cTglBuat,cJamBuat,cUnit,cWorkReq,cStaff,self.user)
            if (insert_data(sql,val)) == True:
                messagebox.showinfo(title="Informasi",message="Data sudah di tersimpan.")
                self.onClear()

    def onUpdate(self):
        #panel kiri
        cWo = self.entWo.get()
        cIfca = self.entIfca.get()
        cTglBuat = store_date(self.entTglbuat.get()) #check tgl dulu
        cJamBuat = self.entJambuat.get()
        cUnit = self.entUnit.get().upper().strip()
        cWorkReq = self.entWorkReq.get('1.0', 'end').upper().strip()
        cStaff = self.entStaff.get().upper().strip()
        cStatus = self.opsiStatus.get()
        cTimeAcc = datetime.now()
        curItem = self.tabelIfca.item(self.tabelIfca.focus())
        #panel kanan
        cWorkAct = self.entWorkAct.get('1.0', 'end').upper().strip()
        cTglDone = store_date(self.entTgldone.get()) #check tgl dulu
        jamdone = self.entJamdone.get()
        #eksekusi sql
        if len(cWorkReq) <= 0:
            messagebox.showwarning(title="Peringatan",message="Work Request harus diisi.")
            self.entWorkReq.focus_set()
            self.entWorkReq.delete('1.0', 'end')
            return # stop aja karena cWorkAct tidak diisi
        if cWorkReq == curItem['values'][4] and \
            cStaff == curItem['values'][5] and \
            cWorkAct == curItem['values'][6] and \
            self.dept == "ENG": # penegasan, agar root dapat edit parameter lain
            print("Tidak ada aktivitas perubahan")
        else:
            if cStatus == "DONE":
                if len(cStaff) <= 0: 
                    messagebox.showwarning(title="Peringatan",message="Staff ENG harus diisi.")
                    self.entStaff.focus_set()
                    self.entStaff.delete(0, END)
                    return # stop aja karena cStaff tidak diisi
                elif len(cWorkAct) <= 0:
                    messagebox.showwarning(title="Peringatan",message="Work Action harus diisi.")
                    self.entWorkAct.focus_set()
                    self.entWorkAct.delete('1.0', 'end')
                    return # stop aja karena cWorkAct tidak diisi
                elif len(cTglDone) == 0 or len(jamdone.strip()) != 5:
                    messagebox.showerror(title="Error",message="Format tanggal salah")
                    return # stop aja karena tanggal tidak diisi
                else : pass
            elif cStatus == "PENDING":
                cTglDone = ""
                jamdone = ""
                com_auth_by = cStaff+"@"+self.user
                if len(cStaff) <= 0: 
                    messagebox.showwarning(title="Peringatan",message="Staff ENG harus diisi.")
                    self.entStaff.focus_set()
                    self.entStaff.delete(0, END)
                    return # stop aja karena cStaff tidak diisi
                elif len(cWorkAct) <= 0: 
                    messagebox.showwarning(title="Peringatan",message="Work Action harus diisi.")
                    self.entWorkAct.focus_set()
                    self.entWorkAct.delete('1.0', 'end')
                    return # stop aja karena cWorkAct tidak diisi
                else: ### jgn eksekusi sekarang mungkin?
                    sql = "INSERT INTO onprogress (no_ifca,date_update,commit_update,auth_by,auth_login,auth_dept)"+\
                    "VALUES(%s,%s,%s,%s,%s,%s)"
                    val = (cIfca,cTimeAcc,cWorkAct,com_auth_by,self.user,self.dept)
                    print("Pending store data,",insert_data(sql,val))
            elif cStatus == "CANCEL":
                cTglDone = ""
                jamdone = ""
                if len(cWorkAct) <= 0: 
                    messagebox.showwarning(title="Peringatan",message="Work Action harus diisi.")
                    self.entWorkAct.focus_set()
                    self.entWorkAct.delete('1.0', 'end')
                    return # stop aja karena cWorkAct tidak diisi
            else : # UPDATE tidak perlu tanggal
                cTglDone = ""
                jamdone = ""

            sql = "UPDATE logbook SET no_wo=%s,no_ifca=%s,date_create=%s,time_create=%s,unit=%s,work_req=%s,staff=%s,\
                status_ifca=%s,date_done=%s,time_done=%s,work_act=%s,received=%s,wo_receiver=%s,auth_login=%s WHERE id =%s"
            val = (cWo,cIfca,cTglBuat,cJamBuat,cUnit,cWorkReq,cStaff,cStatus,cTglDone,jamdone,\
                cWorkAct,self.varRec.get(),self.entRecBy.get(),self.user,self.idWO)
            if (insert_data(sql,val)) == True:
                messagebox.showinfo(title="Informasi", \
                    message="Data sudah di terupdate.")
                self.onSearch()

    def onDateCreate(self):
        setdate = PopupDateTime(self.parent)
        setdate.parent.wait_window(setdate.top)
        if len(setdate.value.strip()) > 0: 
            # output <tanggal> <jam>, lanjutkan perintah
            getdate, gettime = setdate.value.split() #pisah tanggal dan jam
            self.entTglbuat.config(state="normal")
            self.entJambuat.config(state="normal")
            self.entTglbuat.delete(0, END)
            self.entJambuat.delete(0, END)
            self.entTglbuat.insert(END, getdate)
            self.entJambuat.insert(END, gettime)
            self.entTglbuat.config(state="readonly")
            self.entJambuat.config(state="readonly")
            self.entUnit.focus_set()
        else: 
            # output kosong, batalkan perintah
            pass

    def onDateDone(self):
        setdate = PopupDateTime(self.parent)
        setdate.parent.wait_window(setdate.top)
        if len(setdate.value.strip()) > 0: 
            # output <tanggal> <jam>, lanjutkan perintah
            getdate, gettime = setdate.value.split() #pisah tanggal dan jam
            self.entTgldone.config(state="normal")
            self.entJamdone.config(state="normal")
            self.entTgldone.delete(0, END)
            self.entJamdone.delete(0, END)
            self.entTgldone.insert(END, getdate)
            self.entJamdone.insert(END, gettime)
            self.entTgldone.config(state="readonly")
            self.entJamdone.config(state="readonly")
        else: 
            # output kosong, batalkan perintah
            pass

def testrun(user,dept):
    notebook = ttk.Notebook(root) # lihat, self.parent = root
    notebook.pack(fill="both", expand=True)
    notebook.add(PageMain(notebook,user,dept), text="Main")
    root.title("Project Logbook by GanyoyGen - Debug - Test Log: {0}.{1}".format(user,dept))
    root.iconbitmap(str(os.getcwd()+"\\"+"icon-icons.com_main.ico"))
    root.mainloop()

if __name__ == "__main__":
    # PASTIKAN ceksesi dalam mode DEBUG
    from ttkthemes import ThemedTk
    root = ThemedTk(theme='clearlooks')
    user = 'Owner'
    dept = 'ENG'
    testrun(user,dept)