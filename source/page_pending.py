import tkinter as tk
import mysql.connector
from mysqlcon import read_db_config
from tkinter import *
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

kolomPending = ("WO","IFCA","Tanggal","UNIT","Work Request")

class Pending(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # label = tk.Label(self, text="This is page 2")
        # label.pack(fill ="both", expand=True, padx=20, pady=10)
        self.setKomponen()
        
    def setKomponen(self):
        # tab pending
        topFrame = Frame(self)
        topFrame.pack(side=TOP,fill=X)
        midFrame = Frame(self)
        midFrame.pack(side=TOP, fill=X)
        botFrame = Frame(self)
        botFrame.pack(expand=YES, side=TOP,fill=Y)
        Label(topFrame, text='').grid(row=0, column=0)
        Label(midFrame, text='').grid(row=1, column=0)
        entOne = Frame(topFrame)
        entOne.grid(row=1,column=1,sticky=W)
        self.pendWo = Entry(entOne, width=10)
        self.pendWo.grid(row=1, column=0,sticky=W)
        # Label(entOne, text=' ').grid(row=1, column=1, sticky=W,pady=5,padx=10)
        self.pendIfca = Entry(entOne, width=15)
        self.pendIfca.grid(row=1, column=2,sticky=W)               
        Label(entOne, text=' ').grid(row=1, column=3, sticky=W,pady=5,padx=10)
        self.pendUnit = Entry(entOne, width=12)
        self.pendUnit.grid(row=1, column=4,sticky=W)
        entTwo = Frame(topFrame)
        entTwo.grid(row=2,column=1,sticky=W)
        self.pendTgl = Entry(entTwo, width=15)
        self.pendTgl.grid(row=2, column=0,sticky=W)
        # Label(entTwo, text=' ').grid(row=2, column=1, sticky=W,pady=5,padx=10)
        self.pendJam = Entry(entTwo, width=10)
        self.pendJam.grid(row=2, column=1,sticky=W)               
        Label(entTwo, text=' ').grid(row=2, column=2, sticky=W,pady=5,padx=10)
        self.pendStaff = Entry(entTwo, width=12)
        self.pendStaff.grid(row=2, column=3,sticky=W)
        self.pendWorkReq = ScrolledText(topFrame,height=8,width=40)
        self.pendWorkReq.grid(row=3, column=1,sticky=W)
        entLeft = Frame(topFrame)
        entLeft.grid(row=2,column=5,sticky=W)
        Label(entLeft, text='By :').grid(row=2, column=0, sticky=W,pady=5,padx=10)
        self.accpStaff = Entry(entLeft, width=20)
        self.accpStaff.grid(row=2, column=1,sticky=W) 
        self.btnAccept = Button(entLeft, text='Accept',\
                                command=self.onAccPending, width=10,\
                                relief=RAISED, bd=2, bg="#FC6042", fg="white",activebackground="#444",activeforeground="white" )
        self.btnAccept.grid(row=2, column=2,pady=10,padx=5)
        Label(topFrame, text='                  ').grid(row=2, column=2, sticky=W,pady=5,padx=10)
        self.pendWorkAct = ScrolledText(topFrame,height=8,width=40)
        self.pendWorkAct.grid(row=3, column=5,sticky=W)
        self.btnRefresh = Button(midFrame, text='Refresh',\
                                command=self.pending_refresh, width=10,\
                                relief=RAISED, bd=2, bg="#667", fg="white",activebackground="#444",activeforeground="white" )
        self.btnRefresh.grid(row=1, column=0,pady=10,padx=5)
        #tabel
        self.pend_data = Frame(botFrame, bd=10)
        self.pend_data.pack(fill=BOTH, expand=YES)
        self.tabelPend = ttk.Treeview(self.pend_data, columns=kolomPending,show='headings')
        self.tabelPend.bind("<Double-1>",self.pending_detail)
        sbVer = Scrollbar(self.pend_data, orient='vertical',command=self.tabelPend.yview)
        sbVer.pack(side=RIGHT, fill=Y)
        sbHor = Scrollbar(self.pend_data, orient='horizontal',command=self.tabelPend.xview)
        sbHor.pack(side=BOTTOM, fill=X)
        self.tabelPend.pack(side=TOP, fill=BOTH)
        self.tabelPend.configure(yscrollcommand=sbVer.set)
        self.tabelPend.configure(xscrollcommand=sbHor.set)
        #showtable
        self.pending_refresh()
    
    def entrySet(self,opsi):
        # 2 tabpending, clear
        if opsi == "pendclear":
                self.pendWo.config(state="normal")
                self.pendIfca.config(state="normal")
                self.pendUnit.config(state="normal")
                self.pendTgl.config(state="normal")
                self.pendJam.config(state="normal")
                self.pendStaff.config(state="normal")
                self.pendWorkReq.config(state="normal")
                self.pendWorkAct.config(state="normal")
                self.pendWo.delete(0, END)
                self.pendIfca.delete(0, END)
                self.pendUnit.delete(0, END)
                self.pendTgl.delete(0, END)
                self.pendJam.delete(0, END)
                self.pendStaff.delete(0, END)
                # self.accpStaff.delete(0, END)
                self.pendWorkAct.delete('1.0', 'end')
                self.pendWorkReq.delete('1.0', 'end')
        # tabpending readonly
        if opsi == "pendread":
                self.pendWo.config(state="readonly")
                self.pendIfca.config(state="readonly")
                self.pendUnit.config(state="readonly")
                self.pendTgl.config(state="readonly")
                self.pendJam.config(state="readonly")
                self.pendStaff.config(state="readonly")
                self.pendWorkReq.config(state="disable")
                self.pendWorkAct.config(state="disable")
        # 2 #
 
    def pending_table(self):
        try:
            db_config = read_db_config()
            con = mysql.connector.connect(**db_config)
            cur = con.cursor()
            sql = "SELECT * FROM logbook WHERE status_ifca LIKE %s"
            data = "PENDING"
            val = ("%{}%".format(data),)
        #     data = "%PENDING%"
            cur.execute(sql, val)
            results = cur.fetchall()
            self.tabelPend.delete(*self.tabelPend.get_children()) #refresh, hapus dulu tabel lama
            for kolom in kolomPending:
                self.tabelPend.heading(kolom,text=kolom)
            # self.tabelPend.column("No", width=10,anchor="w")
            self.tabelPend.column("WO", width=50,anchor="w")
            self.tabelPend.column("IFCA", width=80,anchor="w")
            self.tabelPend.column("Tanggal", width=80,anchor="w")
            self.tabelPend.column("UNIT", width=80,anchor="w")
            self.tabelPend.column("Work Request", width=200,anchor="w")
        
            i=0
            for dat in results: 
                if(i%2):
                    baris="genap"
                else:
                    baris="ganjil"
                #hilangkan nomor mulai dari kolom wo dat[1:]
                self.tabelPend.insert('', 'end', values=dat[1:], tags=baris)
                i+=1

            self.tabelPend.tag_configure("ganjil", background="gainsboro")
            self.tabelPend.tag_configure("genap", background="floral white")
            cur.close()
            con.close()
            
        except mysql.connector.Error as err:
            messagebox.showerror(title="Error", \
                message="SQL Log: {}".format(err))                           

    def pending_detail(self, event):
        try:
            curItem = self.tabelPend.item(self.tabelPend.focus())
            ifca_value = curItem['values'][1]
            self.entrySet("pendclear")
            self.pendIfca.insert(END, ifca_value)
            
            db_config = read_db_config()
            con = mysql.connector.connect(**db_config)
            cur = con.cursor()
            # sql = "SELECT no_wo, no_ifca, date_create, time_create, unit, work_req, staff, work_act, FROM logbook WHERE no_ifca = %s"
            sql = "SELECT no_wo, no_ifca, date_create, unit, work_req, staff, work_act, time_create FROM logbook WHERE no_ifca = %s"
            cur.execute(sql,(ifca_value,))
            data = cur.fetchone()
            self.pendWo.insert(END, data[0])
            #TGL buat
            self.pendTgl.insert(END, data[2])
            getTgl = self.pendTgl.get() #dari mysql YYYY-MM-DD
            #balikin menjadi DD-MM-YYYY
            showtgl = str(getTgl)[8:] + '-' + str(getTgl)[5:7] +'-' + str(getTgl)[:4]
            self.pendTgl.delete(0, END)
            self.pendTgl.insert(END, showtgl)
            self.pendJam.insert(END, data[7])
            self.pendUnit.insert(END, data[3])
            self.pendWorkReq.insert(END, data[4])
            self.pendStaff.insert(END, data[5])
            self.pendWorkAct.insert(END, data[6])

            self.entrySet("pendread")
            self.btnAccept.config(state="normal")
            cur.close()
            con.close()
            # self.pending_table()
        except:
            print('Tidak ada data di tabel')

    def onAccPending(self):
        try:
            db_config = read_db_config()
            con = mysql.connector.connect(**db_config)
            cur = con.cursor()
            getIfca = self.pendIfca.get()
            getAccBy = self.accpStaff.get()
            from datetime import datetime
            getTimeAcc = datetime.now()
            firstcom = "WO Sudah diterima oleh"
            setStatus = "ONPROGRESS"
            if len(getAccBy.strip()) == 0:
                messagebox.showwarning(title="Peringatan",message="Siapa yang menerima WO?")
                self.accpStaff.focus_set()
            else:
                sql1 = "INSERT INTO onprogress (no_ifca,date_update,commit_update,auth_by,auth_login)"+\
                "VALUES(%s,%s,%s,%s,%s)"
                cur.execute(sql1,(getIfca,getTimeAcc,firstcom,getAccBy.upper(),""))
                sql2 = "UPDATE logbook SET status_ifca=%s WHERE no_ifca =%s"
                cur.execute(sql2,(setStatus,getIfca))
                con.commit()
                cur.close()
                con.close()
                messagebox.showinfo(title="Informasi",message="WO sudah diterima oleh {}.".format(getAccBy))
                self.pending_refresh()
        except mysql.connector.Error as err:
            messagebox.showerror(title="Error", \
                message="SQL Log: {}".format(err)) 

    def pending_refresh(self):
            self.btnAccept.config(state="disable")
            self.entrySet("pendclear")
            self.pending_table()
