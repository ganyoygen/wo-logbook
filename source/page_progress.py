import tkinter as tk
import mysql.connector
import os
import csv # untuk write ke Excel
import time
import datetime

from mysqlcon import read_db_config
from popup_date import PopupDateTime # popup set tgl jam
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText

kolomProgIfca = ("WO","IFCA","UNIT")
kolomCommIfca = ("TANGGAL","UPDATE","OLEH","DEPT")

class PageProg(tk.Frame):
    def __init__(self,parent,user,dept):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.user = user
        self.dept = dept
        self.statwosel = StringVar(parent,value="PEND")

        self.komponenProgress()
        self.komponenAtas()
        self.komponenTengah()
        self.komponenBawah()

    def komponenProgress(self):
        self.topFrame = ttk.Frame(self)
        self.topFrame.pack(side=TOP,fill=X)
        self.midFrame = ttk.Frame(self)
        self.midFrame.pack(side=TOP, fill=X)
        self.botFrame = ttk.Frame(self)
        self.botFrame.pack(side=TOP, fill=X)
        footer = ttk.Frame(self)
        footer.pack(side=TOP, fill=X)
        
        ttk.Label(self.topFrame, text='').grid(row=0, column=0)
        ttk.Label(self.midFrame, text='').grid(row=0, column=0)
        ttk.Label(self.botFrame, text='').grid(row=0, column=0)
        ttk.Label(footer, text='').grid(row=0, column=0)
        
    def komponenAtas(self):
        entOne = ttk.Frame(self.topFrame)
        entOne.grid(row=1,column=1,sticky=W)
        self.progWo = ttk.Entry(entOne, width=10)
        self.progWo.grid(row=1, column=0,sticky=W)
        self.progIfca = ttk.Entry(entOne, width=15)
        self.progIfca.grid(row=1, column=1,sticky=W)               
        ttk.Label(entOne, text=' ').grid(row=1, column=2, sticky=W,pady=5,padx=10)
        self.progUnit = ttk.Entry(entOne, width=12)
        self.progUnit.grid(row=1, column=3,sticky=W)

        entTwo = ttk.Frame(self.topFrame)
        entTwo.grid(row=2,column=1,sticky=W)
        self.progTgl = ttk.Entry(entTwo, width=15)
        self.progTgl.grid(row=1, column=0,sticky=W)
        self.progJam = ttk.Entry(entTwo, width=10)
        self.progJam.grid(row=1, column=1,sticky=W)               
        ttk.Label(entTwo, text=' ').grid(row=1, column=2, sticky=W,pady=5,padx=10)
        self.progStaff = ttk.Entry(entTwo, width=12)
        self.progStaff.grid(row=1, column=3,sticky=W)

        self.progWorkReq = ScrolledText(self.topFrame,height=8,width=40)
        self.progWorkReq.grid(row=3, column=1,sticky=W)
        
        ttk.Label(self.topFrame, text='     ').grid(row=3,column=2,sticky=W,pady=5,padx=10)
        self.commitDetail = ScrolledText(self.topFrame,height=8,width=50)
        self.commitDetail.grid(row=3, column=3,sticky=W)

        entLeft = ttk.Frame(self.topFrame)
        entLeft.grid(row=2,column=3,sticky=W)
        self.commitdate = ttk.Entry(entLeft, width=20)
        self.commitdate.grid(row=1, column=0,sticky=W)
        ttk.Label(entLeft, text='By :').grid(row=1, column=1, sticky=W,pady=5,padx=5)
        self.commitby = ttk.Entry(entLeft, width=20)
        self.commitby.grid(row=1, column=2,sticky=W)

        self.btnPendAccp = Button(entLeft, text='Accept',\
            command=self.onAccPending, width=10,\
            relief=RAISED, bd=2, bg="#FC6042", fg="white",\
            activebackground="#444",activeforeground="white" )
        self.btnPendAccp.grid(row=1,column=3,sticky=N,pady=10,padx=5)
        
        entBtnRight = ttk.Frame(self.topFrame)
        entBtnRight.grid(row=3,column=4,sticky=W)
        
        self.btnCommUpdate = Button(entBtnRight, text='Update',\
            command=self.onProgCommUpd, width=10,\
            relief=RAISED, bd=2, bg="#FC6042", fg="white",\
            activebackground="#444",activeforeground="white" )
        self.btnCommUpdate.grid(row=1,column=0,sticky=N,pady=5,padx=5)
        self.btnCommReturn = Button(entBtnRight, text='Return',\
            command=self.onReturnWO, width=10,\
            relief=RAISED, bd=2, bg="#FC6042", fg="white",\
            activebackground="#444",activeforeground="white" )
        self.btnCommReturn.bind("<Button-3>",self.onReturnWO) # percobaan tooltips
        self.btnCommReturn.grid(row=2,column=0,sticky=N,pady=5,padx=5)
        self.btnCommTake = Button(entBtnRight, text='Take',\
            command=self.onTakeWO, width=10,\
            relief=RAISED, bd=2, bg="#FC6042", fg="white",\
            activebackground="#444",activeforeground="white" )
        self.btnCommTake.bind("<Button-3>",self.onTakeWO) # percobaan tooltips
        self.btnCommTake.grid(row=3,column=0,sticky=N,pady=5,padx=5)
        self.btnCommDone = Button(entBtnRight, text='Done',\
            command=self.onSetDoneWO, width=10,\
            relief=RAISED, bd=2, bg="#FC6042", fg="white",#
            activebackground="#444",activeforeground="white" )
        self.btnCommDone.bind("<Button-3>",self.onSetDoneWO) # percobaan tooltips
        self.btnCommDone.grid(row=4,column=0,sticky=N,pady=5,padx=5)
        
    def komponenTengah(self):
        btnselect = ttk.Frame(self.midFrame)
        btnselect.grid(row=1,column=1,sticky=W)
        self.rstswo = ttk.Radiobutton(btnselect,text="PENDING",variable=self.statwosel,value="PEND",command=self.progress_refresh)
        self.rstswo.grid(row=1, column=1,sticky=W)
        self.rstswo = ttk.Radiobutton(btnselect,text="PROGRESS",variable=self.statwosel,value="PROG",command=self.progress_refresh)
        ttk.Label(btnselect, text="     ").grid(row=1,column=2,sticky=E)
        self.rstswo.grid(row=1, column=3,sticky=W)
        self.rstswo = ttk.Radiobutton(btnselect,text="RETURN",variable=self.statwosel,value="RETU",command=self.progress_refresh)
        ttk.Label(btnselect, text="     ").grid(row=1,column=4,sticky=E)
        self.rstswo.grid(row=1, column=5,sticky=W)
        self.rstswo = ttk.Radiobutton(btnselect,text="TAKEN",variable=self.statwosel,value="TAKE",command=self.progress_refresh)
        ttk.Label(btnselect, text="     ").grid(row=1,column=6,sticky=E)
        self.rstswo.grid(row=1, column=7,sticky=W)
        ttk.Label(btnselect, text="     ").grid(row=1,column=8,sticky=E)

        frcaridata = ttk.Frame(self.midFrame)
        frcaridata.grid(row=1,column=2,sticky=E)

        self.entcaridata = ttk.Entry(frcaridata, width=15)
        self.entcaridata.grid(row=1, column=1,sticky=E)

        self.btnRefProg = Button(frcaridata, text='Search',\
            command='self.caridata', width=10,\
            relief=RAISED, bd=2, bg="#667", fg="white",#
            activebackground="#444",activeforeground="white")
        self.btnRefProg.grid(row=1,column=2,pady=5,padx=5)

    def komponenBawah(self):
        listprog = ttk.Frame(self.botFrame)
        listprog.grid(row=1,column=0,sticky=W)
        ttk.Label(self.botFrame, text='     ').grid(row=1,column=1)
        listcomm = ttk.Frame(self.botFrame)
        listcomm.grid(row=1,column=2,sticky=W)

        self.tabelProg = ttk.Treeview(listprog, columns=kolomProgIfca,show='headings')
        self.tabelProg.bind("<Double-1>",self.progress_detail)
        sbVer = ttk.Scrollbar(listprog, orient='vertical',command=self.tabelProg.yview)
        sbVer.pack(side=RIGHT, fill=Y)
        sbHor = ttk.Scrollbar(listprog, orient='horizontal',command=self.tabelProg.xview)
        sbHor.pack(side=BOTTOM, fill=X)
        self.tabelProg.pack(side=TOP, fill=BOTH)
        self.tabelProg.configure(yscrollcommand=sbVer.set)
        self.tabelProg.configure(xscrollcommand=sbHor.set)

        self.tabelcomm = ttk.Treeview(listcomm, columns=kolomCommIfca,show='headings')
        self.tabelcomm.bind("<Double-1>",self.prog_comm_detail)
        sbVer = ttk.Scrollbar(listcomm, orient='vertical',command=self.tabelcomm.yview)
        sbVer.pack(side=RIGHT, fill=Y)
        sbHor = ttk.Scrollbar(listcomm, orient='horizontal',command=self.tabelcomm.xview)
        sbHor.pack(side=BOTTOM, fill=X)
        self.tabelcomm.pack(side=TOP, fill=BOTH)
        self.tabelcomm.configure(yscrollcommand=sbVer.set)
        self.tabelcomm.configure(xscrollcommand=sbHor.set)
        
        self.progress_refresh()
    
    def entrySet(self,opsi):
        # 3 progress entry clear
        if opsi == "progclear":
            self.progWo.config(state="normal")
            self.progIfca.config(state="normal")
            self.progUnit.config(state="normal")
            self.progTgl.config(state="normal")
            self.progJam.config(state="normal")
            self.progStaff.config(state="normal")
            self.progWorkReq.config(state="normal")
            self.commitdate.config(state="normal")
            self.commitby.config(state="normal")
            self.commitDetail.config(state="normal")
            self.progWo.delete(0, END)
            self.progIfca.delete(0, END)
            self.progUnit.delete(0, END)
            self.progTgl.delete(0, END)
            self.progJam.delete(0, END)
            self.progStaff.delete(0, END)
            self.commitdate.delete(0, END)
            self.commitby.delete(0, END)
            self.commitDetail.delete('1.0', 'end')
            self.progWorkReq.delete('1.0', 'end')
        elif opsi == "progread":
            self.progWo.config(state="readonly")
            self.progIfca.config(state="readonly")
            self.progUnit.config(state="readonly")
            self.progTgl.config(state="readonly")
            self.progJam.config(state="readonly")
            self.progStaff.config(state="readonly")
            self.progWorkReq.config(state="disable")
            # self.commitDetail.config(state="disable")
        elif opsi == "disablebtn":
            self.btnPendAccp.config(state="disable")
            self.btnCommUpdate.config(state="disable")
            self.btnCommReturn.config(state="disable")
            self.btnCommTake.config(state="disable")
            self.btnCommDone.config(state="disable")
        else : pass
        # 3 #

    def progress_table(self,opsi):
        '''
        opsi = <status WO>
        '''
        try:
            db_config = read_db_config()
            con = mysql.connector.connect(**db_config)
            cur = con.cursor()
            # sql = "SELECT * FROM logbook WHERE status_ifca LIKE %s"
            # sql = "SELECT no_wo, no_ifca, unit FROM logbook WHERE status_ifca LIKE %s OR status_ifca LIKE %s OR status_ifca LIKE %s"
            sql = "SELECT no_wo, no_ifca, unit FROM logbook WHERE status_ifca LIKE %s"
            val = ("%{}%".format(opsi),)
            cur.execute(sql, val)
            results = cur.fetchall()
            self.tabelProg.delete(*self.tabelProg.get_children()) #refresh, hapus dulu tabel lama
            for kolom in kolomProgIfca:
                self.tabelProg.heading(kolom,text=kolom)
            # self.tabelProg.column("No", width=10,anchor="w")
            self.tabelProg.column("WO", width=50,anchor="w")
            self.tabelProg.column("IFCA", width=80,anchor="w")
            self.tabelProg.column("UNIT", width=80,anchor="w")
            
            i=0
            for dat in results: 
                if(i%2):
                    baris="genap"
                else:
                    baris="ganjil"
                #tampilkan hanya wo ifca unit 
                # self.tabelProg.insert('', 'end', values=dat[1]+" "+dat[2]+" "+dat[4], tags=baris)
                self.tabelProg.insert('', 'end', values=dat, tags=baris)
                i+=1
            self.tabelProg.tag_configure("ganjil", background="gainsboro")
            self.tabelProg.tag_configure("genap", background="floral white")
            cur.close()
            con.close()
        
        except mysql.connector.Error as err:
            messagebox.showerror(title="Error", \
                message="SQL Log: {}".format(err))                           

    def commited_table(self,data):
        # data = "no_ifca"
        try:
            db_config = read_db_config()
            con = mysql.connector.connect(**db_config)
            cur = con.cursor()
            # sql = "SELECT * FROM onprogress WHERE no_ifca LIKE %s"
            sql = "SELECT date_update,commit_update,auth_by,auth_dept \
                    FROM onprogress WHERE no_ifca LIKE %s"
            val = ("%{}%".format(data),)
            cur.execute(sql, val)
            results = cur.fetchall()
            self.tabelcomm.delete(*self.tabelcomm.get_children()) #refresh, hapus dulu tabel lama
            for kolom in kolomCommIfca:
                self.tabelcomm.heading(kolom,text=kolom)
            # self.tabelcomm.column("No", width=10,anchor="w")
            self.tabelcomm.column("TANGGAL", width=110,anchor="w")
            self.tabelcomm.column("UPDATE", width=300,anchor="w")
            self.tabelcomm.column("OLEH", width=110,anchor="w")
            self.tabelcomm.column("DEPT", width=60,anchor="w")
            
            i=0
            for dat in results: 
                if(i%2):
                    baris="genap"
                else:
                    baris="ganjil"
                self.tabelcomm.insert('', 'end', values=dat, tags=baris)
                i+=1
            self.tabelcomm.tag_configure("ganjil", background="gainsboro")
            self.tabelcomm.tag_configure("genap", background="floral white")
            cur.close()
            con.close()
        
        except mysql.connector.Error as err:
            messagebox.showerror(title="Error", \
                message="SQL Log: {}".format(err))                           

    def progress_detail(self, event):
        try:
            curItem = self.tabelProg.item(self.tabelProg.focus())
            ifca_value = curItem['values'][1]
            self.entrySet("progclear")
            self.commited_table(ifca_value)
            self.progIfca.insert(END, ifca_value)
            db_config = read_db_config()
            con = mysql.connector.connect(**db_config)
            cur = con.cursor()
            # sql = "SELECT no_wo, no_ifca, date_create, unit, work_req, staff, work_act, time_create, status_ifca FROM logbook WHERE no_ifca = %s"
            sql = "SELECT no_wo,no_ifca,date_create,time_create,unit,\
                work_req,staff,status_ifca FROM logbook WHERE no_ifca = %s"
            cur.execute(sql,(ifca_value,))
            data = cur.fetchone()
            self.progWo.insert(END, data[0])
            #TGL buat
            self.progTgl.insert(END, data[2])
            getTgl = self.progTgl.get() #dari mysql YYYY-MM-DD
            #balikin menjadi DD-MM-YYYY
            showtgl = str(getTgl)[8:] + '-' + str(getTgl)[5:7] +'-' + str(getTgl)[:4]
            self.progTgl.delete(0, END)
            self.progTgl.insert(END, showtgl)
            self.progJam.insert(END, data[3])
            self.progUnit.insert(END, data[4])
            self.progWorkReq.insert(END, data[5])
            self.progStaff.insert(END, data[6])
            self.entrySet("progread")
            self.commitdate.config(state="disable")
            if (self.dept == "ENG") or (self.dept == "CS"):
                if data[7] == "PENDING": 
                    self.btnCommUpdate.config(state="disable")
                    self.btnPendAccp.config(state="normal")
                elif data[7] == "ONPROGRESS": 
                    self.btnCommUpdate.config(state="normal")
                    self.btnCommReturn.config(state="normal")
                elif (data[7] == "RETURNED") and (self.dept == "ENG"): 
                    self.btnCommTake.config(state="normal")
                elif (data[7] == "TAKEN") and (self.dept == "ENG"): 
                    self.btnCommDone.config(state="normal")
                else : pass
            else : pass #fungsi diatas hanya untuk cs-eng
            self.commitby.focus_set()
            cur.close()
            con.close()            
        except:
            print('Tidak ada data di tabel')

    def prog_comm_detail(self, event):
        try:
            curItem = self.tabelcomm.item(self.tabelcomm.focus())
            comDate = curItem['values'][0]
            valIfca = self.progIfca.get()
        
            db_config = read_db_config()
            con = mysql.connector.connect(**db_config)
            cur = con.cursor()
            sql = "SELECT * FROM onprogress WHERE no_ifca LIKE %s AND date_update = %s"
            cur.execute(sql,(valIfca,comDate))
            data = cur.fetchone()
            self.commitdate.config(state="normal")
            self.commitby.config(state="normal")
            self.commitDetail.config(state="normal")
            self.commitdate.delete(0, END)
            self.commitby.delete(0, END)
            self.commitDetail.delete('1.0', 'end')
            showdate = str(data[2])[8:10] + '-' + str(data[2])[5:7] +'-' + str(data[2])[:4]+' '+str(data[2])[11:]
            self.commitdate.insert(END, showdate)
            self.commitby.insert(END, data[4])
            self.commitDetail.insert(END, data[3])
            self.commitdate.config(state="readonly")
            self.commitby.config(state="readonly")
            self.commitDetail.config(state="disable")
            self.entrySet("disablebtn")
            cur.close()
            con.close()
        except:
            print('Tidak ada data di tabel')

    def progress_refresh(self):
        self.entrySet("disablebtn")
        self.entrySet("progclear")
        self.tabelcomm.delete(*self.tabelcomm.get_children()) #refresh, hapus dulu tabel lama
        tipe = str(self.statwosel.get())
        if tipe == "PEND": self.progress_table("PENDING")
        elif tipe == "PROG": self.progress_table("ONPROGRESS")
        elif tipe == "RETU": self.progress_table("RETURNED")
        elif tipe == "TAKE": self.progress_table("TAKEN")
        else : pass
        #########

    def onProgCommUpd(self):
        try:
            db_config = read_db_config()
            con = mysql.connector.connect(**db_config)
            cur = con.cursor()
            getIfca = self.progIfca.get()
            getUsrUpd = self.commitby.get()
            getcommit = self.commitDetail.get(1.0,END) # ('1.0', 'end')
            accandusr = getUsrUpd.upper().strip()+"@"+self.user
            from datetime import datetime
            getTime = datetime.now()
            
            if len(getUsrUpd.strip()) == 0: # .strip memastikan space/tab termasuk len 0
                messagebox.showwarning(title="Peringatan",message="Siapa yang update commit?")
                self.commitby.focus_set()
                self.commitby.delete(0, END)
            elif len(getcommit.strip()) == 0: # .strip memastikan space/tab termasuk len 0
                messagebox.showwarning(title="Peringatan",message="Silahkan isi perubahan terlebih dahulu")
                self.commitDetail.focus_set()
                self.commitDetail.delete('1.0','end')
            else:
                sql = "INSERT INTO onprogress (no_ifca,date_update,commit_update,auth_by,auth_login,auth_dept)"+\
                "VALUES(%s,%s,%s,%s,%s,%s)"
                cur.execute(sql,(getIfca,getTime,getcommit.strip(),accandusr,self.user,self.dept))
                messagebox.showinfo(title="Informasi",message="Update telah tersimpan oleh {}.".format(getUsrUpd))
                self.progress_detail(self)
            con.commit()
            cur.close()
            con.close()
        except mysql.connector.Error as err:
            messagebox.showerror(title="Error", \
                message="SQL Log: {}".format(err))

    def onAccPending(self):
        try:
            db_config = read_db_config()
            con = mysql.connector.connect(**db_config)
            cur = con.cursor()
            getIfca = self.progIfca.get()
            getAccBy = self.commitby.get()
            accandusr = getAccBy.upper().strip()+"@"+self.user
            from datetime import datetime
            getTimeAcc = datetime.now()
            autocom = "[WO OnProgress] diterima oleh {}.".format(getAccBy.upper())
            setStatus = "ONPROGRESS"
            if len(getAccBy.strip()) == 0:
                messagebox.showwarning(title="Peringatan",message="Siapa yang menerima WO?")
                self.commitby.focus_set()
                self.commitby.delete(0, END)
            else:
                sql1 = "INSERT INTO onprogress (no_ifca,date_update,commit_update,auth_by,auth_login,auth_dept)"+\
                "VALUES(%s,%s,%s,%s,%s,%s)"
                cur.execute(sql1,(getIfca,getTimeAcc,autocom,accandusr,self.user,self.dept))
                sql2 = "UPDATE logbook SET status_ifca=%s WHERE no_ifca =%s"
                cur.execute(sql2,(setStatus,getIfca))
                messagebox.showinfo(title="Informasi",message="WO sudah diterima oleh {}.".format(getAccBy))
                self.progress_refresh()
            con.commit()
            cur.close()
            con.close()
        except mysql.connector.Error as err:
            messagebox.showerror(title="Error", \
                message="SQL Log: {}".format(err))

    def onReturnWO(self,event=None):
        if not event == None:
            print("event True =",Event) # percobaan tooltips
            return
        try:
            db_config = read_db_config()
            con = mysql.connector.connect(**db_config)
            cur = con.cursor()
            getIfca = self.progIfca.get()
            getAccBy = self.commitby.get()
            accandusr = getAccBy.upper().strip()+"@"+self.user
            from datetime import datetime
            getTimeAcc = datetime.now()
            autocom = "[WO Return] dikembalikan oleh {}.".format(getAccBy.upper())
            setStatus = "RETURNED"

            cekaccp = "SELECT auth_dept FROM onprogress \
                WHERE no_ifca = %s AND `commit_update` LIKE '%[WO OnProgress] diterima oleh%'"
            cur.execute(cekaccp,(getIfca,))
            data = cur.fetchone()

            if len(getAccBy.strip()) == 0:
                messagebox.showwarning(title="Peringatan",message="Siapa yang mengembalikan WO?")
                self.commitby.focus_set()
                self.commitby.delete(0, END)
            elif self.dept != data[0]:
                messagebox.showerror(title="Error",message="WO yang diterima oleh Dept. {0}, Tidak bisa dikembalikan oleh Dept. {1}.\r\n \
                    \r\nWO Hanya bisa dikembalikan oleh Dept. yang sama saat WO diterima.".format(data[0],self.dept))
            elif messagebox.askokcancel('Return WO','WO akan dikembalikan?') == True: 
                sql1 = "INSERT INTO onprogress (no_ifca,date_update,commit_update,auth_by,auth_login,auth_dept)"+\
                "VALUES(%s,%s,%s,%s,%s,%s)"
                cur.execute(sql1,(getIfca,getTimeAcc,autocom,accandusr,self.user,self.dept))
                sql2 = "UPDATE logbook SET status_ifca=%s WHERE no_ifca =%s"
                cur.execute(sql2,(setStatus,getIfca))
                messagebox.showinfo(title="Informasi",message="WO Sudah dikembalikan oleh {}.".format(getAccBy))
                self.progress_refresh()
            else: pass
            con.commit()
            cur.close()
            con.close()
        except mysql.connector.Error as err:
            messagebox.showerror(title="Error", \
                message="SQL Log: {}".format(err)) 

    def onTakeWO(self,event=None):
        if not event == None:
            print("event True =",Event) # percobaan tooltips
            return
        try:
            db_config = read_db_config()
            con = mysql.connector.connect(**db_config)
            cur = con.cursor()
            getIfca = self.progIfca.get()
            getAccBy = self.commitby.get()
            accandusr = getAccBy.upper().strip()+"@"+self.user
            from datetime import datetime
            getTimeAcc = datetime.now()
            autocom = "[WO Taken] diterima oleh {}.".format(getAccBy.upper())
            setStatus = "TAKEN"

            if len(getAccBy.strip()) == 0:
                messagebox.showwarning(title="Peringatan",message="Siapa yang menerima WO?")
                self.commitby.focus_set()
                self.commitby.delete(0, END)
            elif messagebox.askokcancel('Take WO','WO sudah diterima?') == True: 
                sql1 = "INSERT INTO onprogress (no_ifca,date_update,commit_update,auth_by,auth_login,auth_dept)"+\
                "VALUES(%s,%s,%s,%s,%s,%s)"
                cur.execute(sql1,(getIfca,getTimeAcc,autocom,accandusr,self.user,self.dept))
                sql2 = "UPDATE logbook SET status_ifca=%s WHERE no_ifca =%s"
                cur.execute(sql2,(setStatus,getIfca))
                messagebox.showinfo(title="Informasi",message="WO Sudah diterima oleh {}.".format(getAccBy))
                self.progress_refresh()
            else: pass
            con.commit()
            cur.close()
            con.close()
        except mysql.connector.Error as err:
            messagebox.showerror(title="Error", \
                message="SQL Log: {}".format(err)) 

    def onSetDoneWO(self,event=None):
        if not event == None:
            print("event True =",Event) # percobaan tooltips
            return
        try:
            db_config = read_db_config()
            con = mysql.connector.connect(**db_config)
            cur = con.cursor()
            getIfca = self.progIfca.get()
            getAccBy = self.commitby.get()
            accandusr = getAccBy.upper().strip()+"@"+self.user
            getcommit = self.commitDetail.get(1.0,END) # ('1.0', 'end')
            from datetime import datetime
            getRealTime = datetime.now()
            # autocom = "Status wo DONE oleh {}.".format(getAccBy)
            setStatus = "DONE"

            if len(getAccBy.strip()) == 0:
                messagebox.showwarning(title="Peringatan",message="Siapa staff yang handle WO?")
                self.commitby.focus_set()
                self.commitby.delete(0, END)
            elif len(getcommit.strip()) == 0: # .strip memastikan space/tab termasuk len 0
                    messagebox.showwarning(title="Peringatan",message="Silahkan isi perubahan terlebih dahulu")
                    self.commitDetail.focus_set()
                    self.commitDetail.delete('1.0','end')
            else: 
                setdate = PopupDateTime(self.parent)
                setdate.parent.wait_window(setdate.top)
                if len(setdate.value.strip()) > 0: 
                    getdate, gettime = setdate.value.split() #pisah tanggal dan jam

                    sqllastcom = "INSERT INTO onprogress (no_ifca,date_update,commit_update,auth_by,auth_login,auth_dept)"+\
                    "VALUES(%s,%s,%s,%s,%s,%s)"
                    cur.execute(sqllastcom,(getIfca,getRealTime,getcommit.strip(),accandusr,self.user,self.dept))

                    storedata = self.getDataComm(getIfca)

                    sqlmain = "UPDATE logbook SET staff=%s,status_ifca=%s,date_done=%s,time_done=%s,work_act=%s WHERE no_ifca =%s"
                    cur.execute(sqlmain,(getAccBy.upper(),setStatus,self.checktgl(getdate),gettime,storedata.strip(),getIfca))

                    messagebox.showinfo(title="Informasi",message="Update telah tersimpan oleh {}.".format(getAccBy))
                    self.progress_refresh()
                else: 
                    # output kosong, batalkan perintah DONE
                    print("batalkan done")
            con.commit()
            cur.close()
            con.close()
        except mysql.connector.Error as err:
            messagebox.showerror(title="Error", \
                message="SQL Log: {}".format(err)) 

    def getDataComm(self,data): #PR: RAMPINGKAN DATA
        try:
            db_config = read_db_config()
            con = mysql.connector.connect(**db_config)
            cur = con.cursor()
            sql = "SELECT date_update,commit_update,auth_by,auth_dept \
                    FROM onprogress WHERE no_ifca LIKE %s"
        #     data = "TN10020352"
            val = ("%{}%".format(data),)
            cur.execute(sql, val)
            results = cur.fetchall()
            
            self.commitDetail.delete('1.0', 'end')
            for dat in results: 
                #tampilkan mulai dari tanggal
                # nantinya kumpulkan dulu data progres selanjutnya store ke sql
                self.commitDetail.insert(END, dat)
                self.commitDetail.insert(END, "\r\n")

            getcom = self.commitDetail.get(1.0,END)
            self.commitDetail.delete('1.0', 'end')
            cur.close()
            con.close()
            return getcom
        
        except mysql.connector.Error as err:
            messagebox.showerror(title="Error", \
                message="SQL Log: {}".format(err))

    def checktgl(self,data):
        if len(str(data)) == 10:
            cHari = str(data)[0:2]
            cBulan = str(data)[3:5]
            cTahun = str(data)[6:]
            return datetime.date(int(cTahun),int(cBulan),int(cHari))
        else:
            return None

