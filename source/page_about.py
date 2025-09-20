import tkinter as tk
import os
from tkinter import *
from tkinter import ttk, messagebox
from sys_mysql import getdata_one,insert_data
from sys_pwhash import generate_hash,verify_password
from sys_entry import LimitEntry


class About(tk.Frame):
    def __init__(self,parent,user,dept):
        ttk.Frame.__init__(self, parent)
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
        ttk.Label(self.topFrame, text='UID - Username').grid(row=1,column=1,sticky=W,padx=10,pady=5)
        ttk.Label(self.topFrame, text=':').grid(row=1,column=2,sticky=W,padx=10,pady=5)
        frEntUid = ttk.Frame(self.topFrame)
        frEntUid.grid(row=1,column=3,sticky=W)
        self.entUid = ttk.Entry(frEntUid,width=5)
        self.entUid.grid(row=1,column=1,sticky=W)
        self.entName = ttk.Entry(frEntUid,width=20)
        self.entName.grid(row=1,column=2,sticky=W)

        ttk.Label(self.topFrame, text='Department').grid(row=2,column=1,sticky=W,padx=10,pady=5)
        ttk.Label(self.topFrame, text=':').grid(row=2,column=2,sticky=W,padx=10,pady=5)
        self.entDept = ttk.Entry(self.topFrame,width=8)
        self.entDept.grid(row=2,column=3,sticky=W)

        ttk.Label(self.topFrame, text='Email').grid(row=3,column=1,sticky=W,padx=10,pady=5)
        ttk.Label(self.topFrame, text=':').grid(row=3,column=2,sticky=W,padx=10,pady=5)
        self.entEmail = ttk.Entry(self.topFrame,width=30)
        self.entEmail.grid(row=3,column=3,sticky=W,pady=10)

        self.colLabCpw = ttk.Frame(self.topFrame)
        self.colLabCpw.grid(row=4,column=1,sticky=W)
        self.labChPw = ttk.Label(self.colLabCpw, text='Change Password')
        self.labChPw.grid(row=1,column=1,sticky=W,padx=10,pady=5)
        self.labCur = ttk.Label(self.colLabCpw,text="Current Password")
        self.labNew = ttk.Label(self.colLabCpw,text="New Password")
        self.labCon = ttk.Label(self.colLabCpw,text="Confirm Password")

        ttk.Label(self.topFrame, text=':').grid(row=4,column=2,sticky=W,padx=10,pady=5)
        
        self.colChPw = ttk.Frame(self.topFrame)
        self.colChPw.grid(row=4,column=3,sticky=W)

        self.entCurPw = ttk.Entry(self.colChPw,show='*',width=20)
        self.entNewPw = LimitEntry(self.colChPw,maxlen=16,show='*',width=20)
        self.entConfPw = ttk.Entry(self.colChPw,show='*',width=20)
        
        self.btnChPw = ttk.Button(self.colChPw,text="Change",command=self.openChPw)
        self.btnCclPw = ttk.Button(self.colChPw,text="Cancel",command=self.cancelChPw)
        self.btnSetPw = ttk.Button(self.colChPw,text="Set",command=self.setChPw)
        self.btnChPw.grid(row=1,column=1,sticky=W)

        ttk.Label(self.topFrame, text='Last Login-Host-IP').grid(row=5,column=1,sticky=W,padx=10,pady=5)
        ttk.Label(self.topFrame, text=':').grid(row=5,column=2,sticky=W,padx=10,pady=5)
        colEntLast = ttk.Frame(self.topFrame)
        colEntLast.grid(row=5,column=3,sticky=W,pady=10)
        self.entLastLog = ttk.Entry(colEntLast,width=18)
        self.entLastLog.grid(row=1,column=1,sticky=W)
        self.entLastPC = ttk.Entry(colEntLast,width=12)
        self.entLastPC.grid(row=1,column=2,sticky=W)
        self.entLastIP = ttk.Entry(colEntLast,width=15)
        self.entLastIP.grid(row=1,column=3,sticky=W)

    def komponenTengah(self):
        pass
    
    def komponenBawah(self):
        self.user_detail()

    def entryset(self,opsi):
        if opsi == "clear":
            self.entUid.config(state="normal")
            self.entName.config(state="normal")
            self.entDept.config(state="normal")
            self.entEmail.config(state="normal")
            self.entLastLog.config(state="normal")
            self.entLastPC.config(state="normal")
            self.entLastIP.config(state="normal")
            self.entUid.delete(0,END)
            self.entName.delete(0,END)
            self.entDept.delete(0,END)
            self.entEmail.delete(0,END)
            self.entLastLog.delete(0,END)
            self.entLastPC.delete(0,END)
            self.entLastIP.delete(0,END)
        elif opsi == "read":
            self.entUid.config(state="readonly")
            self.entName.config(state="readonly")
            self.entDept.config(state="readonly")
            self.entEmail.config(state="readonly")
            self.entLastLog.config(state="readonly")
            self.entLastPC.config(state="readonly")
            self.entLastIP.config(state="readonly")
        else: pass

    def user_detail(self):
        self.entryset("clear")
        sql = "SELECT * FROM acct WHERE username = %s"
        val = (self.user,)
        data = getdata_one(sql,val)
        if data != None :
            self.entUid.insert(END,data[0])
            self.entName.insert(END,data[1])
            self.entDept.insert(END,data[4])
            self.entEmail.insert(END,data[3])
            self.entLastLog.insert(END,data[9])
            self.entLastPC.insert(END,data[10])
            self.entLastIP.insert(END,data[11])
        self.entryset("read")

    def cancelChPw(self,event=None):
        self.labChPw.grid(row=1,column=1,sticky=W,padx=10,pady=5)
        self.btnChPw.grid(row=1,column=1,sticky=W)
        self.labCur.grid_forget()
        self.labNew.grid_forget()
        self.labCon.grid_forget()
        self.entCurPw.delete(0, END)
        self.entNewPw.delete(0, END)
        self.entConfPw.delete(0, END)
        self.entCurPw.grid_forget()
        self.entNewPw.grid_forget()
        self.entConfPw.grid_forget()
        self.btnCclPw.grid_forget()
        self.btnSetPw.grid_forget()

    def openChPw(self,event=None):
        self.labChPw.grid_forget()
        self.btnChPw.grid_forget()
        self.labCur.grid(row=1,column=1,stick=W,padx=10,pady=5)
        self.labNew.grid(row=2,column=1,stick=W,padx=10,pady=5)
        self.labCon.grid(row=3,column=1,stick=W,padx=10,pady=5)
        self.entCurPw.grid(row=1,column=1,sticky=W)
        self.entNewPw.grid(row=2,column=1,sticky=W)
        self.entConfPw.grid(row=3,column=1,sticky=W)
        self.btnCclPw.grid(row=1,column=3,sticky=W)
        self.btnSetPw.grid(row=3,column=3,sticky=W)

    def setChPw(self):
        if len(self.entUid.get()) <= 0 : return
        sql = "SELECT * FROM acct WHERE uid = %s"
        val = (self.entUid.get(),)
        data = getdata_one(sql,val)
        if data != None :
            uid = data[0]
            password = data[2]
            matchpw = verify_password(self.entCurPw.get(),password)
            if matchpw == False:
                messagebox.showerror(title="Error",message="Password lama tidak sesuai")
                self.entCurPw.focus_set()
            elif (len(self.entNewPw.get()) <= 0) or (str(self.entNewPw.get()) != str(self.entConfPw.get())):
                messagebox.showerror(title="Error",message="Konfirmasi Password tidak sesuai")
                self.entConfPw.focus_set()
            elif messagebox.askokcancel('Change Password','Anda yakin akan mengganti Password?') == True:
                storepw = generate_hash(self.entNewPw.get())
                sql = "UPDATE acct SET passhash=%s WHERE uid=%s"
                val = (storepw,uid)
                if (insert_data(sql,val)) == True:
                    messagebox.showinfo(title="Change Password", \
                        message="Password baru sudah berhasil diupdate.")
                self.cancelChPw(0)
            else:
                self.cancelChPw(0)

def testrun(user,dept):
    notebook = ttk.Notebook(root) # lihat, self.parent = root
    notebook.pack(fill="both", expand=True)
    notebook.add(About(notebook,user,dept), text="Profile")
    root.title("Project Logbook by GanyoyGen - Debug - Test Log: {0}.{1}".format(user,dept))
    root.iconbitmap(str(os.getcwd()+"\\"+"icon-main.ico"))
    root.mainloop()

if __name__ == "__main__":
    from ttkthemes import ThemedTk
    from sys_usrdebug import PopupUser
    root = ThemedTk(theme='clearlooks')
    setuser = PopupUser(root)
    root.wait_window(setuser.top)
    try: testrun(setuser.user,setuser.dept)
    except: pass