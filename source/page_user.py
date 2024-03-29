import tkinter as tk
import time
import datetime
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
# from sys_mysql import *
from sys_mysql import getdata_all,getdata_one,insert_data
from sys_date import GetSeconds 
from sys_account import RemoveAcct
from sys_pwhash import generate_hash,get_random_string
from sys_treevsort import sort_treeview

kolomUser = ("UID","Username","Class","Date Created","Activated","Locked",\
    "Date Locked","Last Login","Last Host","Last IP","Last Logout","Email")

class UserMgmt(tk.Frame):
    def __init__(self,parent,user,dept):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.user = user
        self.dept = dept
        self.genlistpw = {}

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
        colDept = ttk.Frame(self.topFrame)
        colDept.grid(row=2,column=3,sticky=W)
        self.entDept = ttk.Combobox(colDept, \
            values = ["","ROOT","ENG","DOCON","CS","RCP"],\
            state="readonly", width=8)
        self.entDept.current(0)
        self.entDept.grid(row=1, column=1,sticky=W)
        self.entDept.bind('<<ComboboxSelected>>',self.selboxdept)
        self.btnSetDept = ttk.Button(colDept,text="Set",command=self.setDept)
        self.btnSetDept.grid(row=1,column=2,sticky=W)

        ttk.Label(self.topFrame, text='Email').grid(row=3,column=1,sticky=W,padx=10,pady=5)
        ttk.Label(self.topFrame, text=':').grid(row=3,column=2,sticky=W,padx=10,pady=5)
        self.entEmail = ttk.Entry(self.topFrame,width=30)
        self.entEmail.grid(row=3,column=3,sticky=W)

        ttk.Label(self.topFrame, text='Status').grid(row=4,column=1,sticky=W,padx=10,pady=5)
        ttk.Label(self.topFrame, text=':').grid(row=4,column=2,sticky=W,padx=10,pady=5)
        colSts = ttk.Frame(self.topFrame)
        colSts.grid(row=4,column=3,sticky=W)
        self.entSts = ttk.Entry(colSts,width=10)
        self.entSts.grid(row=1,column=1,sticky=W)
        self.btnLock = ttk.Button(colSts,text="Lock/Unlock",command=self.setLock)

        ttk.Label(self.topFrame, text='Last Login-Host-IP').grid(row=5,column=1,sticky=W,padx=10,pady=5)
        ttk.Label(self.topFrame, text=':').grid(row=5,column=2,sticky=W,padx=10,pady=5)
        colEntLast = ttk.Frame(self.topFrame)
        colEntLast.grid(row=5,column=3,sticky=W)
        self.entLastLog = ttk.Entry(colEntLast,width=18)
        self.entLastLog.grid(row=1,column=1,sticky=W)
        self.entLastPC = ttk.Entry(colEntLast,width=12)
        self.entLastPC.grid(row=1,column=2,sticky=W)
        self.entLastIP = ttk.Entry(colEntLast,width=15)
        self.entLastIP.grid(row=1,column=3,sticky=W)

        ttk.Label(self.topFrame, text='Reset Password').grid(row=6,column=1,sticky=W,padx=10,pady=5)
        ttk.Label(self.topFrame, text=':').grid(row=6,column=2,sticky=W,padx=10,pady=5)
        colEntPw = ttk.Frame(self.topFrame)
        colEntPw.grid(row=6,column=3,sticky=W)
        self.btnGenerPw = ttk.Button(colEntPw,text="Generate",command=self.generatePw)
        self.entPw = ttk.Entry(colEntPw,width=18)
        
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

        ttk.Button(self.botFrame,text="Refresh",command=self.refresh).grid(row=1,column=1,sticky=W)
        ttk.Label(self.botFrame,text="").grid(row=2,column=1,pady=50)

        self.refresh()

    def entryset(self,opsi):
        if opsi == "clear":
            self.entUid.config(state="normal")
            self.entName.config(state="normal")
            self.entEmail.config(state="normal")
            self.entSts.config(state="normal")
            self.entLastLog.config(state="normal")
            self.entLastPC.config(state="normal")
            self.entLastIP.config(state="normal")
            self.entUid.delete(0,END)
            self.entName.delete(0,END)
            self.entEmail.delete(0,END)
            self.entSts.delete(0,END)
            self.entLastLog.delete(0,END)
            self.entLastPC.delete(0,END)
            self.entLastIP.delete(0,END)
            
            self.entPw.config(state="normal")
            self.entPw.delete(0,END)
            self.entPw.grid_forget()

            self.entDept.current(0)
            # self.selboxdept(None)
            self.btnLock.grid_forget()
            self.btnGenerPw.grid_forget()
            self.btnSetDept["state"] = "disable"
            
        elif opsi == "read":
            self.entUid.config(state="readonly")
            self.entName.config(state="readonly")
            self.entEmail.config(state="readonly")
            self.entSts.config(state="readonly")
            self.entLastLog.config(state="readonly")
            self.entLastPC.config(state="readonly")
            self.entLastIP.config(state="readonly")
            self.entPw.config(state="readonly")
        else: pass

    def user_detail(self,event=None):
        try:
            self.entryset("clear")
            curItem = self.tabelUser.item(self.tabelUser.focus())
            self.entUid.insert(END,curItem['values'][0])
            self.entName.insert(END,curItem['values'][1])
            self.entEmail.insert(END,curItem['values'][11])

            if curItem['values'][2] == "ROOT": self.entDept.current(1)
            elif curItem['values'][2] == "ENG": self.entDept.current(2)
            elif curItem['values'][2] == "DOCON": self.entDept.current(3)
            elif curItem['values'][2] == "CS": self.entDept.current(4)
            elif curItem['values'][2] == "RCP": self.entDept.current(5)
            else: self.entDept.current(0)

            if curItem['values'][4] != True: 
                self.entSts.insert(END,"Temporary")
                self.btnLock.grid_forget()
            elif curItem['values'][5] == True: 
                self.entSts.insert(END,"Locked")
                self.btnLock.config(text='Unlock')
                self.btnLock.grid(row=1,column=2,sticky=W)
            else: 
                self.entSts.insert(END,"Usage")
                self.btnLock.config(text='Lock')
                self.btnLock.grid(row=1,column=2,sticky=W)
            self.entLastLog.insert(END,curItem['values'][7])
            self.entLastPC.insert(END,curItem['values'][8])
            self.entLastIP.insert(END,curItem['values'][9])
            generpwcek = self.genlistpw.get(self.entUid.get()) #cek apakah uid sudah digenerate
            if generpwcek == None: #jika belum generate, tampilkan tombol
                self.btnGenerPw.grid(row=1,column=1,sticky=W)
            else:  #jika sudah generate, tampilkan pw baru
                self.entPw.grid(row=1,column=2,sticky=W)
                self.entPw.insert(END,generpwcek)
            self.entryset("read")
        except:
            print('Tidak ada data di tabel')

    def generatePw(self):
        def dochangepw():
            uid = data[0]
            self.entPw.grid(row=1,column=2,sticky=W)
            self.entPw.config(state="normal")
            self.entPw.delete(0,END)
            self.entPw.insert(END,get_random_string(8)) # 8 Char
            self.btnGenerPw.grid_forget()
            self.entryset("read")
            self.genlistpw.update({str(uid):self.entPw.get()})
            storepw = generate_hash(self.entPw.get())
            sql = "UPDATE acct SET passhash=%s WHERE uid=%s"
            val = (storepw,uid)
            if (insert_data(sql,val)) == True:
                return True
            return False

        if messagebox.askokcancel('Change Password','Anda yakin akan mengganti Password?') == True:
            sql = "SELECT * FROM acct WHERE uid = %s"
            val = (self.entUid.get(),)
            data = getdata_one(sql,val)
            if data != None :
                if dochangepw() == True:
                    messagebox.showinfo(title="Change Password", \
                        message="Password baru sudah berhasil diupdate.")
                else: print("Password gagal diupdate. UID tidak ditemukan")
            else: messagebox.showerror(title="Change Password", \
                    message="Password gagal diupdate. UID tidak ditemukan")

    def refresh(self):
        self.entryset("clear")
        # sql = "SELECT * FROM acct"
        sql = "SELECT `uid`,`username`,`dept`,`date_create`,`activated`,`lock`,\
            `date_lock`,`last_login`,`last_host`,`last_ip`,`last_logout`,`email` FROM `acct`"
        val = ()
        results = getdata_all(sql,val)
        self.tabelUser.delete(*self.tabelUser.get_children()) #refresh, hapus dulu tabel lama
        for kolom in kolomUser:
            # self.tabelUser.heading(kolom,text=kolom)
            self.tabelUser.heading(kolom,text=kolom,command=lambda c=kolom: sort_treeview(self.tabelUser, c, False))
        self.tabelUser.column("UID", width=30,anchor="w")
        self.tabelUser.column("Username", width=100,anchor="w")
        self.tabelUser.column("Class", width=50,anchor="w")
        self.tabelUser.column("Date Created", width=120,anchor="w")
        self.tabelUser.column("Activated", width=30,anchor="w")
        self.tabelUser.column("Locked", width=30,anchor="w")
        self.tabelUser.column("Date Locked", width=120,anchor="w")
        self.tabelUser.column("Last Login", width=120,anchor="w")
        self.tabelUser.column("Last Host", width=80,anchor="w")
        self.tabelUser.column("Last IP", width=80,anchor="w")
        self.tabelUser.column("Last Logout", width=80,anchor="w")
        self.tabelUser.column("Email", width=80,anchor="w")
        
        remacctlist = []
        i=0
        for dat in results:
            if(i%2):
                baris="genap"
            else:
                baris="ganjil"
            # checking temporary user for delete them
            # dat[0] = uid, dat[3] = date_create, dat[4] = activated -lihat sql = ...
            datetodrop = GetSeconds(str(dat[3])).value + 604800 # 86400*7 (7 hari). Lebih baik buat custom
            if (dat[4] != True and (datetodrop - time.time()) <=0 and RemoveAcct(dat[0]).result == True):
                remacctlist.append(dat[1])
            else: # tampilkan user yang tidak di delete pada tabel
                self.tabelUser.insert('', 'end', values=dat, tags=baris)
            i+=1
        self.tabelUser.tag_configure("ganjil", background="gainsboro")
        self.tabelUser.tag_configure("genap", background="floral white")
        if len(remacctlist) > 0: # berikan info jika ada username yang berhasil dihapus
            messagebox.showwarning(title="Account Info",message="Ditemukan {0} Account telah berhasil dihapus:\
                \r\n{1}".format(len(remacctlist),remacctlist))

    def selboxdept(self,event):
        if self.entDept.get() == "":
            messagebox.showwarning("Warning", "This set about remove account!")
            self.btnSetDept["state"] = "normal"
        else:
            self.btnSetDept["state"] = "normal"

    def setDept(self):
        if len(self.entUid.get()) <= 0 : return
        if self.entDept.get() == "":
            confirm = messagebox.askokcancel('Setting Department','Remove Username: [{0}]?'\
                .format(self.entName.get()))
            dept = "USER"
            activated = None
        else:
            confirm = messagebox.askokcancel('Setting Department','Set Username: {0} - Dept: {1}?'\
                .format(self.entName.get(),self.entDept.get()))
            dept = self.entDept.get()
            activated = True
        if confirm == True:
            sql = "UPDATE acct SET dept=%s, activated=%s WHERE uid=%s"
            val = (dept,activated,self.entUid.get())
            if (insert_data(sql,val)) == True:
                messagebox.showinfo(title="Setting Department", \
                    message="Data sudah diupdate.")
                self.refresh()

    def setLock(self):
        if len(self.entUid.get()) <= 0 : return
        if self.entSts.get() == "Locked":
            sql = "UPDATE acct SET `lock`=%s, date_lock=%s WHERE uid=%s"
            val = (False,datetime.now(),self.entUid.get())
            if (insert_data(sql,val)) == True:
                messagebox.showinfo(title="Locking System", \
                    message="Unlock success.")
        elif self.entSts.get() == "Usage":
            sql = "UPDATE acct SET `lock`=%s, date_lock=%s WHERE uid=%s"
            val = (True,datetime.now(),self.entUid.get())
            if (insert_data(sql,val)) == True:
                messagebox.showinfo(title="Locking System", \
                    message="Lock success.")
        else: pass
        self.refresh()

def testrun(user,dept):
    notebook = ttk.Notebook(root) # lihat, self.parent = root
    notebook.pack(fill="both", expand=True)
    notebook.add(UserMgmt(notebook,user,dept), text="User Mgmt")
    root.title("Project Logbook by GanyoyGen - Debug - Test Log: {0}.{1}".format(user,dept))
    # root.iconbitmap(str(os.getcwd()+"\\"+"icon-icons.com_main.ico"))
    root.mainloop()

if __name__ == "__main__":
    from ttkthemes import ThemedTk
    root = ThemedTk(theme='clearlooks')
    user = 'Debug'
    dept = 'ROOT'
    testrun(user,dept)