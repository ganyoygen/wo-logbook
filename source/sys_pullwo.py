import tkinter as tk
import os
from tkinter import *
from tkinter import ttk,messagebox
from ttkwidgets import CheckboxTreeview
from ttkthemes import ThemedTk
from datetime import datetime
from sys_mysql import getdata_one,getdata_all,insert_data
from sys_date import CustomDateEntry,store_date
from sys_entry import LimitEntry
from ico_images import iconimage

judul_kolom = ("WO","IFCA","Tanggal","UNIT","Work Request","Staff","Work Action","Tanggal Done","Jam Done","Received")

class PullWoTable(object):
    def __init__(self,parent,user,dept):
        top = self.top = Toplevel(parent)
        top.title("Work Order Manager")
        top.iconbitmap(str(os.getcwd()+"\\"+"icon-icons.com_main2.ico"))
        self.parent = parent
        self.user = user
        self.dept = dept
        self.icon = iconimage(self.parent)
        self.top.protocol("WM_DELETE_WINDOW", self.keluar)

        if self.dept == "ENG":
            self.btnWoSel = StringVar(parent,value="BM")
        elif (self.dept == "CS") or (self.dept == "RCP"):
            self.btnWoSel = StringVar(parent,value="TN")
        else: self.btnWoSel = StringVar(parent,value="TN") # DOCON, tampilkan pilihan

        top.wait_visibility() # window needs to be visible for the grab
        top.grab_set()
        # top.bind("<FocusOut>", self.alarm)
        self._set_transient(parent)
        self.komponen()

    def _set_transient(self, master, relx=0.1, rely=0.1):
        # window proses ikut parent (without icon taskbar)
        widget = self.top
        widget.withdraw() # Remain invisible while we figure out the geometry
        # widget.transient(master) # saat ini matikan saja, karena jika showdesktop wom sudah dibuka kembali
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

    def komponen(self):
        mainframe = ttk.Frame(self.top)
        mainframe.pack(side=TOP,fill=X)
        ttk.Label(mainframe, text='''
        Tabel hanya menampilkan data WO untuk:
        1. ALL DEPT: Berdasarkan Tipe TN/BM yang dipilih
        2. CS/RCP/ENG: WO yang telah DONE atau CANCEL
        3. CS/RCP/ENG: WO yang telah ditarik DOCON
        4. DOCON: WO yang telah ditarik CS/RCP/ENG
        Tabel TIDAK menampilkan WO yang telah ditarik oleh dept sendiri (departement yang sama)
        ''').grid(row=0, column=0)

        btnfrm = ttk.Frame(mainframe)
        btnfrm.grid(row=1,column=0)

        tblfrm = ttk.Frame(mainframe)
        tblfrm.grid(row=2,column=0)

        self.rbtnTN = ttk.Radiobutton(btnfrm, text="TN", variable=self.btnWoSel, value="TN", command='self.showtable')
        self.rbtnTN.grid(row=1, column=1,sticky=W,pady=10,padx=5)
        self.rbtnBM = ttk.Radiobutton(btnfrm, text="BM", variable=self.btnWoSel, value="BM", command='self.showtable')
        ttk.Label(btnfrm, text=" ").grid(row=1,column=2,sticky=E)
        self.rbtnBM.grid(row=1, column=3,sticky=W,pady=10,padx=5)

        self.opsicari = ttk.Combobox(btnfrm, \
            values = ["IFCA","Tanggal"], \
            state="readonly", width=10)
        self.opsicari.current(1)
        self.opsicari.grid(row=1,column=4,padx=5,sticky=W)
        self.opsicari.bind('<<ComboboxSelected>>',self.boxsearchsel)

        self.entCari = ttk.Entry(btnfrm, width=20)
        self.entCari.grid(row=1,column=5,pady=10,padx=5)
        self.dateStart = CustomDateEntry(btnfrm,width=10,locale='en_UK')
        self.dateEnd = CustomDateEntry(btnfrm,width=10,locale='en_UK')
        ttk.Label(btnfrm, text='~').grid(row=1,column=6)
        self.entCari.bind('<Return>',self.showtable)
        self.dateStart.bind('<Return>',self.showtable)
        self.dateEnd.bind('<Return>',self.showtable)
        self.dateStart.bind("<KeyRelease>", self.dateStart.keycheck)
        self.dateEnd.bind("<KeyRelease>", self.dateEnd.keycheck)

        self.btnSearch=ttk.Button(btnfrm,text="Search",command=self.showtable,\
            width=6, image=self.icon.icosrctab,compound=tk.LEFT)
        self.btnSearch.grid(row=1,column=8,pady=10,padx=5)
        self.btnReceived=ttk.Button(btnfrm,text="Received",command=self.onReceived,\
            width=6, image=self.icon.icorcv,compound=tk.LEFT)
        self.btnReceived.grid(row=1,column=9,pady=10,padx=5)

        style = ttk.Style(self.parent)
        # remove the indicator in the treeview 
        style.layout('Checkbox.Treeview.Item', 
                    [('Treeitem.padding',
                    {'sticky': 'nswe',
                        'children': [('Treeitem.image', {'side': 'left', 'sticky': ''}),
                                    ('Treeitem.focus', {'side': 'left', 'sticky': '',
                                                        'children': [('Treeitem.text', 
                                                                    {'side': 'left', 'sticky': ''})]})]})])
        # make it look more like a listbox                                                               
        style.configure('Checkbox.Treeview', borderwidth=1, relief='sunken')

        # ct = CheckboxTreeview(root, show='tree') # hide tree headings
        self.table = CheckboxTreeview(tblfrm,columns=judul_kolom,show=('headings','tree'))
        self.table.bind("<ButtonRelease-1>", self.selectItem)
        sbVer = ttk.Scrollbar(tblfrm, orient='vertical',command=self.table.yview)
        sbVer.pack(side=RIGHT, fill=Y)
        sbHor = ttk.Scrollbar(tblfrm, orient='horizontal',command=self.table.xview)
        sbHor.pack(side=BOTTOM, fill=X)
        self.table.configure(yscrollcommand=sbVer.set)
        self.table.configure(xscrollcommand=sbHor.set)
        self.table.pack(side=TOP, fill=BOTH)

        for kolom in judul_kolom:
            self.table.heading(kolom,text=kolom)
        self.table.column("#0", width=1,anchor="w")
        self.table.column("WO", width=50,anchor="w")
        self.table.column("IFCA", width=80,anchor="w")
        self.table.column("Tanggal", width=80,anchor="w")
        self.table.column("UNIT", width=80,anchor="w")
        self.table.column("Work Request", width=150,anchor="w")
        self.table.column("Staff", width=70,anchor="w")
        self.table.column("Work Action", width=150,anchor="w")
        self.table.column("Tanggal Done", width=80,anchor="w")
        self.table.column("Jam Done", width=40,anchor="w")
        self.table.column("Received", width=40,anchor="w")

        self.btnCheckDept(None)
        self.boxsearchsel(None)

    def btnCheckDept(self,event=None):
        if self.dept == "ENG":
            self.rbtnTN.config(state="disable")
        elif (self.dept == "CS") or (self.dept == "RCP"):
            self.rbtnBM.config(state="disable")
        else: pass

    def boxsearchsel(self,event):
        if self.opsicari.get() == "Tanggal":
            self.entCari.delete(0, END)
            self.entCari.grid_forget()
            self.dateStart.grid(row=1,column=5)
            self.dateEnd.grid(row=1,column=7)
        else:
            self.entCari.delete(0, END)
            self.dateStart.grid_forget()
            self.dateEnd.grid_forget()
            self.entCari.grid(row=1,column=5,pady=10,padx=5)

    def selectItem(self,event=None):
        pass
        # debug select item di tabel
        '''
        curItem = self.table.item(self.table.focus())
        # col = self.table.identify_column(event.x)
        col = int(self.table.identify_column(event.x)[1:])
        os.system("cls")
        print ('curItem =', curItem)
        print ('col =', col)
        print ('cell_value =',curItem['values'][col-1])
        print('Tags =',curItem['tags'][0])
        if curItem['values'][9] == False:
            print('WO belum pernah ditarik')
        else: print('Wo Rec By =',curItem['values'][10])
        '''

    def showtable(self,event=None):
        self.table.delete(*self.table.get_children()) #refresh, hapus dulu tabel lama
        self.querySearch() # set dulu variabel self.sql dan self.val
        results = getdata_all(self.sql,self.val) # hasil dari query
        tipe = str(self.btnWoSel.get()) # cek tipe wo
        # Todo: cek ulang
        for value in results:
            dept = value[11].split(".")
            if (self.dept == "DOCON" and value[10] == False and tipe != "BM"):
                # kondisi jika wo belum diterima pertama kali, skip wo TN for docon
                # print('skip ',value[2],' received:',value[10],'youre:',self.dept)
                continue
            elif (len(dept) >= 2) and (dept[1] == "CS" or dept[1] == "RCP") and \
                (self.dept == "CS" or self.dept == "RCP"):
                # kondisi jika wo rec by cs/rcp skip for cs/rcp
                # (len(dept) >= 2) untuk memastikan wo telah direceived departmen ex: user.dept
                # print('skip ',value[2],' by:',value[11],'youre:',self.dept)
                continue
            elif self.dept == "ROOT": 
                # lewat jika akun ROOT
                continue
            else:
                # tampilkan data di tabel
                self.table.insert('', 'end', text="",values=value[1:])

        self.table.tag_configure("checked", background="light salmon")
        # self.table.tag_configure("unchecked", background="floral white")

    def querySearch(self):
        '''
        Tabel hanya menampilkan data WO untuk:
        1. ALL DEPT: Berdasarkan Tipe TN/BM yang dipilih
        2. CS/RCP/ENG: WO yang telah DONE atau CANCEL
        3. CS/RCP/ENG: WO yang telah ditarik DOCON
        4. DOCON: WO yang telah ditarik CS/RCP/ENG
        Tabel TIDAK menampilkan WO yang telah ditarik oleh dept sendiri (departement yang sama)
        '''
        tipe = str(self.btnWoSel.get()) # pencarian berdasarkan tipe WO
        opsi = self.opsicari.get()
        cari = self.entCari.get()
        if opsi == "Tanggal":
            if self.dateStart.get() == self.dateEnd.get():
                cari = store_date(self.dateStart.get())
                self.sql = "SELECT * FROM logbook WHERE (no_ifca LIKE %s AND date_create LIKE %s) AND \
                    (status_ifca = %s OR status_ifca = %s) AND \
                    (wo_receiver NOT LIKE %s) ORDER BY no_ifca DESC"
                self.val = ("%{}%".format(tipe),"%{}%".format(cari),\
                    'DONE','CANCEL',"%{}%".format(self.dept))
            else: #part jika search between date
                sdate = store_date(self.dateStart.get())
                edate = store_date(self.dateEnd.get())
                self.sql = "SELECT * FROM logbook WHERE (date_create BETWEEN %s AND %s AND no_ifca LIKE %s) AND \
                    (status_ifca = %s OR status_ifca = %s) AND \
                    (wo_receiver NOT LIKE %s) ORDER BY no_ifca DESC"
                self.val = ('{}'.format(sdate),'{}'.format(edate),"%{}%".format(tipe),\
                    'DONE','CANCEL',"%{}%".format(self.dept))
        elif opsi == "IFCA":
            self.sql = "SELECT * FROM logbook WHERE (no_ifca LIKE %s AND no_ifca LIKE %s) AND \
                (status_ifca = %s OR status_ifca = %s) AND \
                (wo_receiver NOT LIKE %s) ORDER BY no_ifca DESC"
            self.val = ("%{}%".format(cari),"%{}%".format(tipe),\
                'DONE','CANCEL',"%{}%".format(self.dept))
        else: pass

    def keluar(self,event=None):
        print("exit")
        self.top.destroy()
    
    def onReceived(self):
        def doReceive(data):
            sql = "UPDATE logbook SET date_received=%s,received=%s,wo_receiver=%s WHERE no_ifca =%s"
            val = (tsekarang,True,receiver,data)
            if (insert_data(sql,val)) == True: return True

        receiver = self.user + "." + self.dept
        tsekarang = datetime.now()
        results = self.table.get_children() # dalam format [list]
        i=0
        if len(results) > 0:
            for dat in results:
                ifca = self.table.item(dat)['values'][1]
                cek = self.table.item(dat)['tags'][0]
                if cek == "unchecked": continue # skip yang tidak dicek
                else: 
                    if doReceive(ifca) == True: i+=1
                    else: continue # lanjut, gagal update data
            if i == 0: print("Tidak ada yang diceklis, results:",str(i))
            else: 
                messagebox.showinfo(title="Pull WO", \
                    message="WO diterima [{0}]: {1} sheets".format(receiver,i))
            self.showtable(None)
        else: print("Tabel kosong, results:",len(results))

# class TestRun(object):
#     def __init__(self,master):
#         self.master=master
#         self.entUser = LimitEntry(master,width=20)
#         self.entUser.bind("<KeyRelease>", self.setuser)
#         self.entUser.pack()
#         self.opsidept = ttk.Combobox(master, \
#             values = ["ENG","DOCON","RCP","CS"], \
#             state="readonly",width=15)
#         self.opsidept.current(1)
#         self.opsidept.pack()
#         self.setbtn=ttk.Button(master,text="OpenTable",command=self.popup,width=10)
#         self.setbtn.pack()
#         self.setbtn["state"] = "disabled"

#     def setuser(self,event):
#         s = event.widget
#         if len(s.get()) < 1: self.setbtn["state"] = "disabled"
#         else: self.setbtn["state"] = "normal"

#     def popup(self):
#         self.gopopup=PullWoTable(self.master,self.entUser.get(),self.opsidept.get())
#         self.setbtn["state"] = "disabled"
#         self.master.wait_window(self.gopopup.top)
#         self.setbtn["state"] = "normal"

# if __name__ == "__main__":
#     root = ThemedTk(theme='scidblue')
#     TestRun(root)
#     root.mainloop()

def testrun(user,dept):
    root.title("Project Logbook by GanyoyGen - Debug - Test Log: {0}.{1}".format(user,dept))
    root.iconbitmap(str(os.getcwd()+"\\"+"icon-icons.com_main.ico"))
    PullWoTable(root,user,dept)
    root.mainloop()

if __name__ == "__main__":
    from ttkthemes import ThemedTk
    from sys_usrdebug import PopupUser
    root = ThemedTk(theme='scidblue')
    setuser = PopupUser(root)
    root.wait_window(setuser.top)
    try: testrun(setuser.user,setuser.dept)
    except: pass