import tkinter as tk
import os
import datetime
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
from sys_mysql import getdata_one,getdata_all,insert_data
from sys_date import PopupDateTime,CustomDateEntry,get_date,store_date
from sys_entry import LimitEntry
from sys_treevsort import sort_treeview
from ico_images import iconimage

kolomProgIfca = ("#","WO","IFCA","UNIT")
kolomCommIfca = ("TANGGAL","UPDATE","OLEH","DEPT")

class PageProg(tk.Frame):
    def __init__(self,parent,user,dept):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.user = user
        self.dept = dept
        self.icon = iconimage(self.parent)
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
        
        entBtnRight = ttk.Frame(self.topFrame)
        entBtnRight.grid(row=4,column=4,sticky=W)
        
        self.btnCommUpdate = ttk.Button(entBtnRight,text='Update',command=self.onProgCommUpd,width=6,\
            image=self.icon.icoupdt,compound=tk.LEFT)
        self.btnCommUpdate.grid(row=1,column=0,padx=5,sticky=W)
        self.btnSetSched = ttk.Button(entBtnRight,text='Schedule it',command=self.ScheduleIt,width=6,\
            image=self.icon.icoschd,compound=tk.LEFT)
        self.btnSetSched.grid(row=2,column=0,padx=5,sticky=W)
        self.btnCommTake = ttk.Button(entBtnRight,text='Take',command=self.onTakeWO,width=6,\
            image=self.icon.icotake,compound=tk.LEFT)
        self.btnCommTake.grid(row=3,column=0,padx=5)
        self.btnCommDone = ttk.Button(entBtnRight,text='Done',command=self.onDoneWo,width=6,\
            image=self.icon.icodone,compound=tk.LEFT)
        self.btnCommDone.grid(row=4,column=0,padx=5)

    def komponenTengah(self):
        btnselect = ttk.Frame(self.midFrame)
        btnselect.grid(row=1,column=1,sticky=N,pady=5)
        ttk.Radiobutton(btnselect,text="PROGRESS",variable=self.statwosel,value="PENDING",\
            command=self.progress_refresh).grid(row=1,column=1,sticky=W)
        ttk.Radiobutton(btnselect,text="Taken by CS",variable=self.statwosel,value="BYCS",\
            command=self.progress_refresh).grid(row=1,column=2,sticky=W,padx=20)
        ttk.Radiobutton(btnselect,text="Taken by ENG",variable=self.statwosel,value="BYENG",\
            command=self.progress_refresh).grid(row=1,column=3,sticky=W)
        ttk.Radiobutton(btnselect,text="Scheduled",variable=self.statwosel,value="SCHED",\
            command=self.progress_refresh).grid(row=1,column=4,sticky=W,padx=20)
        ttk.Radiobutton(btnselect,text="DONE",variable=self.statwosel,value="DONE",\
            command=self.progress_refresh).grid(row=1,column=5,sticky=W)

    def komponenBawah(self):
        srchbox = ttk.Frame(self.botFrame)
        srchbox.grid(row=0,column=1,sticky=W)
        ttk.Label(srchbox,text='Search:').grid(row=0,column=2,sticky=S)
        # .grid di progress_refresh
        self.labifca = ttk.Label(srchbox,text='IFCA:')
        self.srcifca = LimitEntry(srchbox,maxlen=10,width=12)
        self.labunit = ttk.Label(srchbox,text='Unit:')
        self.srcunit = LimitEntry(srchbox,maxlen=10,width=12)
        self.srcifca.bind("<FocusIn>",self.srchbindifca)
        self.srcunit.bind("<FocusIn>",self.srchbindunit)
        self.srcifca.bind('<Return>',self.srchprogtable)
        self.srcunit.bind('<Return>',self.srchprogtable)
        self.srcdate = CustomDateEntry(srchbox,width=10,locale='en_UK')
        self.srcdate.bind('<Return>',self.srchprogtable)
        self.srcdate.bind("<KeyRelease>", self.srcdate.keycheck)
        self.varcek=IntVar()
        # self.varcek.set(1) # default On
        # self.srcdate.config(state="disable")
        self.btncek = ttk.Checkbutton(srchbox,variable=self.varcek,\
                        text='All Scheduled',command=self.check_changed)

        self.btnFind = ttk.Button(srchbox,command=self.srchprogtable,\
            image=self.icon.icofind)
        self.btnFind.grid(row=1,column=4,sticky=W,padx=5)

        listprog = ttk.Frame(self.botFrame)
        listprog.grid(row=1,column=1,sticky=W)
        listcomm = ttk.Frame(self.botFrame)
        listcomm.grid(row=1,column=2,sticky=W,padx=10)

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
        for kolom in kolomCommIfca:
            self.tabelcomm.heading(kolom,text=kolom)
        self.tabelcomm.column("TANGGAL", width=110,anchor="w")
        self.tabelcomm.column("UPDATE", width=400,anchor="w")
        self.tabelcomm.column("OLEH", width=110,anchor="w")
        self.tabelcomm.column("DEPT", width=70,anchor="w")

        profrm = ttk.Frame(self.botFrame)
        profrm.grid(row=2,column=1,sticky=W,padx=10)
        comfrm = ttk.Frame(self.botFrame)
        comfrm.grid(row=2,column=2,sticky=W,padx=10)
        self.recProgTab = ttk.Label(profrm, text='this label for showing table record(s)')
        self.recProgTab.pack(side=BOTTOM, fill=BOTH)
        self.recCommTab = ttk.Label(comfrm, text='this label for showing table record(s)')
        self.recCommTab.pack(side=BOTTOM, fill=BOTH)

        self.progress_refresh()
    
    def srchbindifca(self,event):
        self.srcunit.delete(0, END)

    def srchbindunit(self,event):
        self.srcifca.delete(0, END)

    def srchprogtable(self,event=None):
        tipe = str(self.statwosel.get())
        tablefind = UnitorIfca = None
        srunit = self.srcunit.get()
        srifca = self.srcifca.get()
        self.entrySet("disablebtn")
        self.entrySet("progclear")
        if len(srunit) == 0 and len(srifca) > 0: # cari ifca
            tablefind = srifca.upper()
            UnitorIfca = 'no_ifca'
        elif len(srifca) == 0 and len(srunit) > 0: # cari unit
            tablefind = srunit.upper()
            UnitorIfca = "unit"
        else:
            self.progress_table(tipe) # tidak ada yg dicari, buka ProgTable
            return # stop

        if UnitorIfca != None:
            if tipe == "PENDING":
                sql = "SELECT `no_wo`, `no_ifca`, `unit` FROM `logbook` WHERE \
                ({} LIKE %s AND `status_ifca` = 'PENDING') \
                ORDER BY `no_ifca` DESC".format(UnitorIfca)
                val = ("%{}%".format(tablefind),)
            elif tipe == "BYENG":
                sql = "SELECT no_wo, no_ifca, unit FROM logbook WHERE \
                {} LIKE %s AND (stsprog_ifca LIKE %s OR stsprog_ifca LIKE '') AND \
                status_ifca = 'PENDING' ORDER BY no_ifca DESC".format(UnitorIfca)
                val = ("%{}%".format(tablefind),"%{}%".format(tipe))
            elif tipe == "DONE":
                sql = "SELECT `no_wo`, `no_ifca`, `unit` FROM `logbook` WHERE \
                ({} LIKE %s AND `stsprog_ifca` = 'DONE') \
                ORDER BY `no_ifca` DESC".format(UnitorIfca)
                val = ("%{}%".format(tablefind),)
            else:
                sql = "SELECT no_wo, no_ifca, unit FROM logbook WHERE \
                ({} LIKE %s AND status_ifca = 'PENDING' AND stsprog_ifca LIKE %s) \
                ORDER BY no_ifca DESC".format(UnitorIfca)
                val = ("%{}%".format(tablefind),"%{}%".format(tipe))
            tablefind = getdata_all(sql,val)
        else: print("Query sql:",UnitorIfca)
        
        if tablefind != None:
            self.tabelProg.delete(*self.tabelProg.get_children()) #refresh, hapus dulu tabel lama
            i=0
            for dat in tablefind: 
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
        else: print("srchprogtable:",tablefind)

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
            self.tabelcomm.delete(*self.tabelcomm.get_children()) #refresh, hapus dulu tabel lama
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
            self.btnCommTake.config(state="disable")
            self.btnCommDone.config(state="disable")
        else : pass
        # 3 #

    def check_changed(self):
        if self.varcek.get() == 0:
            self.srcdate.config(state="normal")
        else :
            self.srcdate.config(state="disable")
        self.progress_refresh() # jalankan saat ceklis berubah

    def progress_table(self,opsi):
        '''
        opsi = <Value Radio Button>
        '''
        self.srcunit.delete(0, END)
        self.srcifca.delete(0, END)
        for kolom in kolomProgIfca:
            self.tabelProg.heading(kolom,text=kolom,command=lambda c=kolom: sort_treeview(self.tabelProg, c, False))
        self.tabelProg.column("#", width=35,anchor="w")
        self.tabelProg.column("WO", width=50,anchor="e")
        self.tabelProg.column("IFCA", width=90,anchor="w")
        self.tabelProg.column("UNIT", width=90,anchor="w")
        bysched = False
        if opsi == "PENDING" :
            sql = "SELECT no_wo, no_ifca, unit FROM logbook WHERE status_ifca LIKE %s ORDER BY no_ifca DESC"
        elif opsi == "BYENG":
            sql = "SELECT no_wo, no_ifca, unit FROM logbook WHERE +\
                (stsprog_ifca LIKE %s OR stsprog_ifca LIKE '') AND status_ifca = 'PENDING' ORDER BY no_ifca DESC"
        elif opsi == "SCHED":
            bysched = True
            sql = "SELECT unit, no_ifca, sched_prog FROM logbook WHERE +\
                sched_prog LIKE %s ORDER BY sched_prog ASC"
            opsi = store_date(self.srcdate.get())
            self.tabelProg.heading('1', text='UNIT')
            self.tabelProg.heading('3', text='Scheduled')
            self.tabelProg.column("0", width=15,anchor="w")
            self.tabelProg.column("1", width=60,anchor="w")
            self.tabelProg.column("2", width=80,anchor="w")
            self.tabelProg.column("3", width=120,anchor="w")
        else:
            sql = "SELECT no_wo, no_ifca, unit FROM logbook WHERE stsprog_ifca LIKE %s ORDER BY no_ifca DESC"
        val = ("%{}%".format(opsi),)
        if (opsi == "" or self.varcek.get() == 1) and bysched == True:
            # jika format tanggal gagal atau All Scheduled ON, tampilkan hanya schedule by tanggal tersedia
            sql = "SELECT unit, no_ifca, sched_prog FROM logbook WHERE +\
                sched_prog > %s ORDER BY sched_prog ASC"
            val = (0,)
        results = getdata_all(sql, val)

        self.recCommTab.config(text="")
        if len(results) == 0:
            self.recProgTab.config(text="")
        else:
            self.recProgTab.config(text=(len(results),"Record(s)"))

        self.tabelProg.delete(*self.tabelProg.get_children()) #refresh, hapus dulu tabel lama

        if results != None:
            i=0
            for dat in results: 
                if(i%2):
                    baris="genap"
                else:
                    baris="ganjil"
                i+=1
                # tambah dan tampilkan nomor sebelum wo 
                if str(self.statwosel.get()) == "SCHED":
                    item = (str(i),dat[0],dat[1],get_date(str(dat[2])))
                else: 
                    item = (str(i),dat[0],dat[1],dat[2])
                self.tabelProg.insert('', 'end', values=item, tags=baris)
                # self.tabelProg.insert('', 'end', values=dat, tags=baris)
            self.tabelProg.tag_configure("ganjil", background="gainsboro")
            self.tabelProg.tag_configure("genap", background="floral white")
        else: print("progress_table:",results)

    def commited_table(self,data):
        sql = "SELECT date_update,commit_update,auth_by,auth_dept \
                FROM onprogress WHERE no_ifca LIKE %s ORDER BY date_update DESC"
        val = ("%{}%".format(data),)
        results = getdata_all(sql, val)

        if len(results) == 0:
            self.recCommTab.config(text="")
        else:
            self.recCommTab.config(text=(len(results),"Record(s)"))

        for kolom in kolomCommIfca:
            self.tabelcomm.heading(kolom,text=kolom)
        self.tabelcomm.column("TANGGAL", width=110,anchor="w")
        self.tabelcomm.column("UPDATE", width=400,anchor="w")
        self.tabelcomm.column("OLEH", width=110,anchor="w")
        self.tabelcomm.column("DEPT", width=70,anchor="w")

        i=0
        for dat in results: 
            if(i%2):
                baris="genap"
            else:
                baris="ganjil"
            item = (get_date(str(dat[0])),dat[1],dat[2],dat[3])
            self.tabelcomm.insert('', 'end', values=item, tags=baris)
            # self.tabelcomm.insert('', 'end', values=dat, tags=baris)
            i+=1
        self.tabelcomm.tag_configure("ganjil", background="gainsboro")
        self.tabelcomm.tag_configure("genap", background="floral white")                      

    def progress_detail(self, event):
        try:
            curItem = self.tabelProg.item(self.tabelProg.focus())
            ifca_value = curItem['values'][2]
            self.entrySet("progclear")
            self.entrySet("disablebtn")
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
            if ((self.dept == "ENG" or self.dept == "CS") and data[7] == "PENDING"):
                #status pending kasi normal
                self.btnCommUpdate.config(state="normal")
                self.btnSetSched.config(state="normal")
                self.btnCommTake.config(state="normal")
                self.btnCommDone.config(state="normal")
            else : pass #fungsi diatas hanya untuk cs-eng
            self.commitby.focus_set()         
        except:
            print('ProgDetail: tidak ada')

    def prog_comm_detail(self, event):
        try:
            # detail by data from treeview
            curItem = self.tabelcomm.item(self.tabelcomm.focus())
            self.commitdate.config(state="normal")
            self.commitby.config(state="normal")
            self.commitDetail.config(state="normal")
            self.commitdate.delete(0, END)
            self.commitby.delete(0, END)
            self.commitDetail.delete('1.0', 'end')
            # self.commitdate.insert(END,get_date(str(curItem['values'][0])))
            self.commitdate.insert(END,curItem['values'][0]) # tgl sudah diseting pada tabel
            self.commitby.insert(END,curItem['values'][2])
            self.commitDetail.insert(END,curItem['values'][1])
            self.commitdate.config(state="readonly")
            self.commitby.config(state="readonly")
            self.commitDetail.config(state="disable")
            self.entrySet("disablebtn")
        except:
            print('CommDetail: tidak ada')

    def progress_refresh(self):
        self.entrySet("disablebtn")
        self.entrySet("progclear")
        tipe = str(self.statwosel.get())
        if tipe == "SCHED":
            self.labifca.grid_forget()
            self.srcifca.grid_forget()
            self.labunit.grid_forget()
            self.srcunit.grid_forget()
            self.srcdate.grid(row=1,column=2,padx=1,sticky=W)
            self.btncek.grid(row=0,column=4,sticky=S)
        else :
            self.srcdate.grid_forget()
            self.btncek.grid_forget()
            self.labifca.grid(row=1,column=0,sticky=W,padx=3)
            self.srcifca.grid(row=1,column=1,padx=1,sticky=W)
            self.labunit.grid(row=1,column=2,sticky=E,padx=3)
            self.srcunit.grid(row=1,column=3,padx=1,sticky=W)
        self.progress_table(tipe)

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
                sqlmain = "UPDATE logbook SET staff=%s,work_act=%s WHERE no_ifca =%s"
                valmain = (getUsrUpd.upper(),getcommit,getIfca)
                if (insert_data(sqlmain,valmain)) == True:
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

        if (setStatus == getStatus or \
            (self.dept == "ENG" and (getStatus == None or getStatus == ''))): # batalkan jika Dept. ENG sts BYENG atau None
            messagebox.showerror(title="Error",message="WO tidak dapat diterima oleh Dept yang sama") 
        elif len(getAccBy.strip()) == 0:
            messagebox.showwarning(title="Peringatan",message="Siapa yang menerima WO?")
            self.commitby.focus_set()
            self.commitby.delete(0, END)
        elif messagebox.askokcancel('Take WO','WO sudah diterima?') == True: 
            sql = "INSERT INTO onprogress (no_ifca,date_update,commit_update,auth_by,auth_login,auth_dept)"+\
            "VALUES(%s,%s,%s,%s,%s,%s)"
            val = (getIfca,getTimeNow,autocom,accandusr,self.user,self.dept)
            if (insert_data(sql,val)) == True:
                # take wo ga usah update commit ke main logbook
                # sqlmain = "UPDATE logbook SET stsprog_ifca=%s,staff=%s,work_act=%s WHERE no_ifca =%s"
                # valmain = (setStatus,getAccBy.upper(),autocom,getIfca)
                sqlmain = "UPDATE logbook SET stsprog_ifca=%s WHERE no_ifca =%s"
                valmain = (setStatus,getIfca)
                if (insert_data(sqlmain,valmain)) == True:
                    messagebox.showinfo(title="Informasi",message="WO Sudah diterima oleh {}.".format(getAccBy))
                    self.progress_detail(self)
        else: pass

    def ScheduleIt(self):
        getIfca = self.progIfca.get()
        getAccBy = self.commitby.get()
        accandusr = getAccBy.upper().strip()+"@"+self.user
        from datetime import datetime
        getTimeNow = datetime.now()

        if (self.dept != "CS"):
            messagebox.showerror(title="Peringatan",message="Jadwal ditentukan oleh Dept. CS")
            self.commitby.focus_set()
        elif len(getAccBy.strip()) == 0:
            messagebox.showwarning(title="Peringatan",message="Isikan PIC terlebih dahulu")
            self.commitby.focus_set()
            self.commitby.delete(0, END)
        else: 
            setdate = PopupDateTime(self.parent)
            setdate.parent.wait_window(setdate.top)
            if len(setdate.value.strip()) > 0: 
                autocom = "[Scheduled] Rencana pengerjaan oleh {0} pada {1}.".format(getAccBy.upper(),setdate.value)
            else: return
            sql = "INSERT INTO onprogress (no_ifca,date_update,commit_update,auth_by,auth_login,auth_dept)"+\
                "VALUES(%s,%s,%s,%s,%s,%s)"
            val = (getIfca,getTimeNow,autocom,accandusr,self.user,self.dept)
            if (insert_data(sql,val)) == True:
                sqlmain = "UPDATE logbook SET sched_prog=%s,staff=%s,work_act=%s WHERE no_ifca =%s"
                valmain = (store_date(setdate.value),getAccBy.upper(),autocom,getIfca)
                if (insert_data(sqlmain,valmain)) == True:
                    messagebox.showinfo(title="Informasi",message="Jadwal sudah ditetapkan untuk Unit {}.".format(self.progUnit.get()))
                    self.progress_detail(self)

    def onDoneWo (self):
        getIfca = self.progIfca.get()
        getUsrUpd = self.commitby.get()
        getcommit = self.commitDetail.get('1.0', 'end').upper().strip()
        accandusr = getUsrUpd.upper().strip()+"@"+self.user
        from datetime import datetime
        getTime = datetime.now()

        sql = "SELECT stsprog_ifca FROM logbook WHERE no_ifca LIKE %s"
        val = (getIfca,)
        getStatus = getdata_one(sql,val)[0]

        if (self.dept != "ENG"):
            messagebox.showerror(title="Error",message="WO hanya dapat diselesaikan oleh Dept ENG") 
        elif getStatus == 'BYCS':
            messagebox.showerror(title="Error",message="Update tidak selesai, status WO Taken by CS") 
        elif len(getUsrUpd.strip()) == 0:
                messagebox.showwarning(title="Peringatan",message="Siapa staff yang handle WO?")
                self.commitby.focus_set()
                self.commitby.delete(0, END)
        elif len(getcommit.strip()) == 0: # .strip memastikan space/tab termasuk len 0
                messagebox.showwarning(title="Peringatan",message="Silahkan isi perubahan terlebih dahulu")
                self.commitDetail.focus_set()
                self.commitDetail.delete('1.0','end')
        else:
            autocom = "[DONE] {}.".format(getcommit)
            setdate = PopupDateTime(self.parent)
            setdate.parent.wait_window(setdate.top)
            if len(setdate.value.strip()) > 0: 
                getdate, gettime = setdate.value.split() #pisah tanggal dan jam

                sql = "INSERT INTO onprogress (no_ifca,date_update,commit_update,auth_by,auth_login,auth_dept)"+\
                    "VALUES(%s,%s,%s,%s,%s,%s)"
                val = (getIfca,getTime,autocom,accandusr,self.user,self.dept)
                if (insert_data(sql,val)) == True:
                    sqlmain = "UPDATE logbook SET staff=%s,status_ifca='DONE',stsprog_ifca='DONE',\
                        date_done=%s,time_done=%s,work_act=%s WHERE no_ifca =%s"
                    valmain = (getUsrUpd.upper(),store_date(getdate),gettime,autocom,getIfca)
                    if (insert_data(sqlmain,valmain)) == True:
                        messagebox.showinfo(title="Informasi",message="Update telah tersimpan oleh {}.".format(getUsrUpd))
                    self.progress_refresh()
            else: 
                # output kosong, batalkan perintah DONE
                print("batalkan done")

def testrun(user,dept):
    notebook = ttk.Notebook(root) # lihat, self.parent = root
    notebook.pack(fill="both", expand=True)
    notebook.add(PageProg(notebook,user,dept), text="Progress")
    root.title("Project Logbook by GanyoyGen - Debug - Test Log: {0}.{1}".format(user,dept))
    root.iconbitmap(str(os.getcwd()+"\\"+"icon-icons.com_main.ico"))
    root.mainloop()

if __name__ == "__main__":
    from ttkthemes import ThemedTk
    from sys_usrdebug import PopupUser
    root = ThemedTk(theme='clearlooks')
    setuser = PopupUser(root)
    root.wait_window(setuser.top)
    try: testrun(setuser.user,setuser.dept)
    except: pass
