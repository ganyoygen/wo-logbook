import tkinter as tk
import mysql.connector
import os
import csv # untuk write ke Excel
import time
import datetime
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
from sys_mysql import read_db_config,getdata_one,getdata_all,insert_data
from sys_date import PopupDateTime,get_date,store_date

kolomProgIfca = ("#","WO","IFCA","UNIT")
kolomCommIfca = ("TANGGAL","UPDATE","OLEH","DEPT")

class PageProg(tk.Frame):
    def __init__(self,parent,user,dept):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.user = user
        self.dept = dept
        self.statwosel = StringVar(parent,value="PENDING")

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
        footer.pack(side=BOTTOM, fill=X)
        
        ttk.Label(self.topFrame, text='').grid(row=0,column=0,padx=10)
        ttk.Label(self.midFrame, text='').grid(row=0,column=0,padx=10)
        ttk.Label(self.botFrame, text='').grid(row=0,column=0,padx=10)
        ttk.Label(footer, text='').grid(row=0,column=0)
        
    def komponenAtas(self):
        entOne = ttk.Frame(self.topFrame)
        entOne.grid(row=1,column=1,sticky=W)
        ttk.Label(entOne,text='WO:').grid(row=1,column=0,sticky=W,padx=3)
        self.progWo = ttk.Entry(entOne,width=10)
        self.progWo.grid(row=1,column=1,padx=2,sticky=W)
        ttk.Label(entOne,text='Unit:').grid(row=2,column=0,sticky=W,padx=3)
        self.progUnit = ttk.Entry(entOne,width=10)
        self.progUnit.grid(row=2,column=1,padx=2,sticky=W)
        ttk.Label(entOne,text='   ').grid(row=1,column=2,sticky=W,padx=5)
        ttk.Label(entOne,text='IFCA:').grid(row=1,column=3,sticky=E,padx=3)
        self.progIfca = ttk.Entry(entOne,width=16)
        self.progIfca.grid(row=1,column=4,padx=2,sticky=W)
        ttk.Label(entOne,text='Date Create:').grid(row=2,column=3,sticky=W,padx=3)
        self.progTgl = ttk.Entry(entOne,width=16)
        self.progTgl.grid(row=2,column=4,padx=2)

        entTwo = ttk.Frame(self.topFrame)
        entTwo.grid(row=2,column=1,sticky=W) 
        ttk.Label(entTwo,text='Staff:').grid(row=1,column=0,sticky=W,padx=3)
        self.progStaff = ttk.Entry(entTwo,width=16)
        self.progStaff.grid(row=1,column=1)
        ttk.Label(entTwo,text='Work Request:').grid(row=1,column=2,sticky=W,padx=5)
        
        self.progWorkReq = ScrolledText(self.topFrame,height=8,width=40)
        self.progWorkReq.grid(row=4, column=1,sticky=W)
        
        ttk.Label(self.topFrame, text='     ').grid(row=4,column=2,padx=10)
        self.commitDetail = ScrolledText(self.topFrame,height=8,width=50)
        self.commitDetail.grid(row=4, column=3,sticky=W)

        ttk.Label(self.topFrame,text='Update Detail:').grid(row=1,column=3,sticky=SW)

        entRight = ttk.Frame(self.topFrame)
        entRight.grid(row=2,column=3,sticky=W)
        ttk.Label(entRight, text='Date:').grid(row=2, column=0, sticky=E,padx=3)
        self.commitdate = ttk.Entry(entRight, width=18)
        self.commitdate.grid(row=2, column=1,sticky=W)
        ttk.Label(entRight,text='   ').grid(row=2,column=2,padx=5)
        ttk.Label(entRight, text='By:').grid(row=2, column=3, sticky=W,padx=3)
        self.commitby = ttk.Entry(entRight, width=20)
        self.commitby.grid(row=2, column=4,sticky=W)
        self.btnSetSched = ttk.Button(entRight,text='Schedule it',command=self.ScheduleIt,width=10)
        self.btnSetSched.grid(row=2,column=5,padx=5)
        
        entBtnRight = ttk.Frame(self.topFrame)
        entBtnRight.grid(row=4,column=4,sticky=W)
        
        self.btnCommUpdate = ttk.Button(entBtnRight,text='Update',command=self.onProgCommUpd,width=10)
        self.btnCommUpdate.grid(row=1,column=0,sticky=N,pady=2,padx=5)
        self.btnCommReturn = ttk.Button(entBtnRight,text='Return',command=self.onReturnWO,width=10)
        self.btnCommReturn.bind("<Button-3>",self.onReturnWO) # percobaan tooltips
        self.btnCommReturn.grid(row=2,column=0,sticky=N,pady=2,padx=5)
        self.btnCommTake = ttk.Button(entBtnRight,text='Take',command=self.onTakeWO,width=10)
        self.btnCommTake.grid(row=3,column=0,sticky=N,pady=2,padx=5)
        self.btnCommDone = ttk.Button(entBtnRight,text='Done',command=self.onSetDoneWO,width=10)
        self.btnCommDone.bind("<Button-3>",self.onSetDoneWO) # percobaan tooltips
        self.btnCommDone.grid(row=4,column=0,sticky=N,pady=2,padx=5)

    def komponenTengah(self):
        btnselect = ttk.Frame(self.midFrame)
        btnselect.grid(row=1,column=1,sticky=W)
        ttk.Radiobutton(btnselect,text="PROGRESS",variable=self.statwosel,value="PENDING",\
            command=self.progress_refresh).grid(row=1,column=1,sticky=W)
        ttk.Radiobutton(btnselect,text="Taken by CS",variable=self.statwosel,value="BYCS",\
            command=self.progress_refresh).grid(row=1,column=3,sticky=W,padx=20)
        ttk.Radiobutton(btnselect,text="Taken by ENG",variable=self.statwosel,value="BYENG",\
            command=self.progress_refresh).grid(row=1,column=5,sticky=W)
        ttk.Radiobutton(btnselect,text="DONE",variable=self.statwosel,value="DONE",\
            command=self.progress_refresh).grid(row=1,column=7,sticky=W,padx=20)

    def komponenBawah(self):
        listprog = ttk.Frame(self.botFrame)
        listprog.grid(row=1,column=1,sticky=W)
        listcomm = ttk.Frame(self.botFrame)
        listcomm.grid(row=1,column=2,sticky=W,padx=20)

        self.tabelProg = ttk.Treeview(listprog, columns=kolomProgIfca,show='headings')
        self.tabelProg.bind("<Double-1>",self.progress_detail)
        sbVer = ttk.Scrollbar(listprog, orient='vertical',command=self.tabelProg.yview)
        sbVer.pack(side=RIGHT, fill=Y)
        sbHor = ttk.Scrollbar(listprog, orient='horizontal',command=self.tabelProg.xview)
        sbHor.pack(side=BOTTOM, fill=X)
        self.tabelProg.pack(side=TOP, fill=BOTH)
        self.tabelProg.configure(yscrollcommand=sbVer.set)
        self.tabelProg.configure(xscrollcommand=sbHor.set)
        for kolom in kolomProgIfca:
            self.tabelProg.heading(kolom,text=kolom)
        self.tabelProg.column("#", width=35,anchor="w")
        self.tabelProg.column("WO", width=50,anchor="e")
        self.tabelProg.column("IFCA", width=80,anchor="w")
        self.tabelProg.column("UNIT", width=80,anchor="w")

        self.tabelcomm = ttk.Treeview(listcomm, columns=kolomCommIfca,show='headings')
        self.tabelcomm.bind("<Double-1>",self.prog_comm_detail)
        sbVer = ttk.Scrollbar(listcomm, orient='vertical',command=self.tabelcomm.yview)
        sbVer.pack(side=RIGHT, fill=Y)
        sbHor = ttk.Scrollbar(listcomm, orient='horizontal',command=self.tabelcomm.xview)
        sbHor.pack(side=BOTTOM, fill=X)
        self.tabelcomm.pack(side=TOP, fill=BOTH)
        self.tabelcomm.configure(yscrollcommand=sbVer.set)
        self.tabelcomm.configure(xscrollcommand=sbHor.set)
        for kolom in kolomCommIfca:
            self.tabelcomm.heading(kolom,text=kolom)
        # self.tabelcomm.column("No", width=10,anchor="w")
        self.tabelcomm.column("TANGGAL", width=110,anchor="w")
        self.tabelcomm.column("UPDATE", width=400,anchor="w")
        self.tabelcomm.column("OLEH", width=120,anchor="w")
        self.tabelcomm.column("DEPT", width=70,anchor="w")
        
        self.progress_refresh()
    
    def entrySet(self,opsi):
        # 3 progress entry clear
        if opsi == "progclear":
            self.progWo.config(state="normal")
            self.progIfca.config(state="normal")
            self.progUnit.config(state="normal")
            self.progTgl.config(state="normal")
            self.progStaff.config(state="normal")
            self.progWorkReq.config(state="normal")
            self.commitdate.config(state="normal")
            self.commitby.config(state="normal")
            self.commitDetail.config(state="normal")
            self.progWo.delete(0, END)
            self.progIfca.delete(0, END)
            self.progUnit.delete(0, END)
            self.progTgl.delete(0, END)
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
            self.progStaff.config(state="readonly")
            self.progWorkReq.config(state="disable")
            # self.commitDetail.config(state="disable")
        elif opsi == "disablebtn":
            self.btnSetSched.config(state="disable")
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
        if opsi == "PENDING" :
            sql = "SELECT no_wo, no_ifca, unit FROM logbook WHERE status_ifca LIKE %s ORDER BY no_ifca DESC"
        elif opsi == "BYENG":
            sql = "SELECT no_wo, no_ifca, unit FROM logbook WHERE +\
                (stsprog_ifca LIKE %s OR stsprog_ifca IS NULL) AND status_ifca = 'PENDING' ORDER BY no_ifca DESC"
        else:
            sql = "SELECT no_wo, no_ifca, unit FROM logbook WHERE stsprog_ifca LIKE %s ORDER BY no_ifca DESC"
        val = ("%{}%".format(opsi),)
        results = getdata_all(sql, val)

        self.tabelProg.delete(*self.tabelProg.get_children()) #refresh, hapus dulu tabel lama

        i=0
        for dat in results: 
            if(i%2):
                baris="genap"
            else:
                baris="ganjil"
            i+=1
            # tambah dan tampilkan nomor sebelum wo 
            item = (str(i),dat[0],dat[1],dat[2])
            self.tabelProg.insert('', 'end', values=item, tags=baris)
            # self.tabelProg.insert('', 'end', values=dat, tags=baris)
        self.tabelProg.tag_configure("ganjil", background="gainsboro")
        self.tabelProg.tag_configure("genap", background="floral white")                       

    def commited_table(self,data):
        sql = "SELECT date_update,commit_update,auth_by,auth_dept \
                FROM onprogress WHERE no_ifca LIKE %s ORDER BY date_update DESC"
        val = ("%{}%".format(data),)
        results = getdata_all(sql, val)
        self.tabelcomm.delete(*self.tabelcomm.get_children()) #refresh, hapus dulu tabel lama
        
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

    def progress_detail(self, event):
        try:
            curItem = self.tabelProg.item(self.tabelProg.focus())
            ifca_value = curItem['values'][2]
            self.entrySet("progclear")
            self.commited_table(ifca_value)
            self.progIfca.insert(END, ifca_value)
            # sql = "SELECT no_wo, no_ifca, date_create, unit, work_req, staff, work_act, time_create, status_ifca FROM logbook WHERE no_ifca = %s"
            sql = "SELECT no_wo,no_ifca,date_create,time_create,unit,\
                work_req,staff,status_ifca FROM logbook WHERE no_ifca = %s"
            val = (ifca_value,)
            data = getdata_one(sql,val)
            self.progWo.insert(END, data[0])
            #TGL buat
            self.progTgl.insert(END,get_date(str(data[2]))+' '+data[3])
            self.progUnit.insert(END, data[4])
            self.progWorkReq.insert(END, data[5])
            self.progStaff.insert(END, data[6])
            self.entrySet("progread")
            self.commitdate.config(state="disable")
            if (self.dept == "ENG") or (self.dept == "CS"):
                if data[7] == "PENDING": 
                    self.btnCommUpdate.config(state="normal")
                    self.btnSetSched.config(state="normal") #status pending kasi normal
                    self.btnCommTake.config(state="normal") #status pending kasi normal
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
        except:
            print('Tidak ada data di tabel')

    def prog_comm_detail(self, event):
        try:
            # detail by data from mysql
            '''
            curItem = self.tabelcomm.item(self.tabelcomm.focus())
            comDate = curItem['values'][0]
            valIfca = self.progIfca.get()
            sql = "SELECT * FROM onprogress WHERE no_ifca LIKE %s AND date_update = %s"
            val = (valIfca,comDate)
            data = getdata_one(sql,val)
            self.commitdate.config(state="normal")
            self.commitby.config(state="normal")
            self.commitDetail.config(state="normal")
            self.commitdate.delete(0, END)
            self.commitby.delete(0, END)
            self.commitDetail.delete('1.0', 'end')
            self.commitdate.insert(END,get_date(str(data[2])))
            self.commitby.insert(END, data[4])
            self.commitDetail.insert(END, data[3])
            self.commitdate.config(state="readonly")
            self.commitby.config(state="readonly")
            self.commitDetail.config(state="disable")
            self.entrySet("disablebtn")
            '''
            # detail by data from treeview
            curItem = self.tabelcomm.item(self.tabelcomm.focus())
            self.commitdate.config(state="normal")
            self.commitby.config(state="normal")
            self.commitDetail.config(state="normal")
            self.commitdate.delete(0, END)
            self.commitby.delete(0, END)
            self.commitDetail.delete('1.0', 'end')
            self.commitdate.insert(END,get_date(str(curItem['values'][0])))
            self.commitby.insert(END,curItem['values'][2])
            self.commitDetail.insert(END,curItem['values'][1])
            self.commitdate.config(state="readonly")
            self.commitby.config(state="readonly")
            self.commitDetail.config(state="disable")
            self.entrySet("disablebtn")
        except:
            print('Tidak ada data di tabel')

    def progress_refresh(self):
        self.entrySet("disablebtn")
        self.entrySet("progclear")
        tipe = str(self.statwosel.get())
        # if tipe == "PEND": self.progress_table("PENDING")
        # elif tipe == "PROG": self.progress_table("ONPROGRESS")
        # elif tipe == "RETU": self.progress_table("RETURNED")
        # elif tipe == "TAKE": self.progress_table("TAKEN")
        # else : pass
        self.progress_table(tipe)
        self.tabelcomm.delete(*self.tabelcomm.get_children()) #refresh, hapus dulu tabel lama
        for kolom in kolomCommIfca:
            self.tabelcomm.heading(kolom,text=kolom)

    def onProgCommUpd(self):
        getIfca = self.progIfca.get()
        getUsrUpd = self.commitby.get()
        getcommit = self.commitDetail.get('1.0', 'end').upper().strip()
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
            val = (getIfca,getTime,getcommit,accandusr,self.user,self.dept)
            if (insert_data(sql,val)) == True:
                messagebox.showinfo(title="Informasi",message="Update telah tersimpan oleh {}.".format(getUsrUpd))
                self.progress_detail(self)

    def onTakeWO(self):
        getIfca = self.progIfca.get()
        getAccBy = self.commitby.get()
        accandusr = getAccBy.upper().strip()+"@"+self.user
        from datetime import datetime
        getTimeNow = datetime.now()
        autocom = "[WO Taken] diterima oleh {}.".format(getAccBy.upper())

        if (self.dept == "CS"): setStatus = "BYCS"
        elif (self.dept == "ENG"): setStatus = "BYENG"
        else: pass

        sql = "SELECT stsprog_ifca FROM logbook WHERE no_ifca LIKE %s"
        val = (getIfca,)
        getStatus = getdata_one(sql,val)[0]
        print('setstatus',setStatus)
        print('getstatus',getStatus)

        if len(getAccBy.strip()) == 0:
            messagebox.showwarning(title="Peringatan",message="Siapa yang menerima WO?")
            self.commitby.focus_set()
            self.commitby.delete(0, END)
        elif (setStatus == getStatus or \
            (self.dept == "ENG" and getStatus == None)): # batalkan jika Dept. ENG sts BYENG atau None
            messagebox.showerror(title="Error",message="WO tidak dapat diterima oleh Dept yang sama") 
        elif messagebox.askokcancel('Take WO','WO sudah diterima?') == True: 
            sql = "INSERT INTO onprogress (no_ifca,date_update,commit_update,auth_by,auth_login,auth_dept)"+\
            "VALUES(%s,%s,%s,%s,%s,%s)"
            val = (getIfca,getTimeNow,autocom,accandusr,self.user,self.dept)
            if (insert_data(sql,val)) == True:
                sql = "UPDATE logbook SET stsprog_ifca=%s WHERE no_ifca =%s"
                val = (setStatus,getIfca)
                if (insert_data(sql,val)) == True:
                    messagebox.showinfo(title="Informasi",message="WO Sudah diterima oleh {}.".format(getAccBy))
                    self.progress_detail(self)
        else: pass
        #########
### baru sampe sini [PAGEPROG]Optimization
    def ScheduleIt(self):
        getIfca = self.progIfca.get()
        getAccBy = self.commitby.get()
        accandusr = getAccBy.upper().strip()+"@"+self.user
        from datetime import datetime
        getTimeNow = datetime.now()
        if len(getAccBy.strip()) == 0:
            messagebox.showwarning(title="Peringatan",message="Isikan PIC terlebih dahulu")
            self.commitby.focus_set()
        elif (self.dept != "CS"):
            messagebox.showerror(title="Peringatan",message="Jadwal ditentukan oleh Dept. CS")
            self.commitby.focus_set()
        else: 
            setdate = PopupDateTime(self.parent)
            setdate.parent.wait_window(setdate.top)
            autocom = "[Scheduled] Rencana pengerjaan oleh {0} pada {1}.".format(getAccBy.upper(),setdate.value)
            
            sql = "UPDATE logbook SET sched_prog=%s WHERE no_ifca =%s"
            val = (store_date(setdate.value),getIfca)
            if (insert_data(sql,val)) == True:
                sql = "INSERT INTO onprogress (no_ifca,date_update,commit_update,auth_by,auth_login,auth_dept)"+\
                "VALUES(%s,%s,%s,%s,%s,%s)"
                val = (getIfca,getTimeNow,autocom,accandusr,self.user,self.dept)
                if (insert_data(sql,val)) == True:
                    messagebox.showinfo(title="Informasi",message="WO Sudah diterima oleh {}.".format(getAccBy))
                    self.progress_detail(self)

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

def testrun(user,dept):
    notebook = ttk.Notebook(root) # lihat, self.parent = root
    notebook.pack(fill="both", expand=True)
    notebook.add(PageProg(notebook,user,dept), text="Progress")
    root.title("Project Logbook by GanyoyGen")
    root.iconbitmap(str(os.getcwd()+"\\"+"icon-icons.com_main.ico"))
    root.mainloop()

if __name__ == "__main__":
    from ttkthemes import ThemedTk
    root = ThemedTk(theme='scidblue')
    testrun("Udin","CS")
