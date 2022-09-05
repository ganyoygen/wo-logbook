import os
import mysql.connector
import pypyodbc # pip install pypyodbc
import tkinter as tk
from tkinter import *
from tkinter import ttk,Toplevel,messagebox
from configparser import ConfigParser
from sys_entry import LimitEntry
from sys_mysql import read_db_config
from sys_mssql import read_db_config_ms

getfile = str(os.getcwd())+"\\"+"config.ini"
secmysql = 'mysql'
secmssql = 'mssql'

class SetConfig(object):
    def __init__(self,parent):
        top = self.top = Toplevel(parent)
        top.title("Config to Connect DB")
        self.parent = parent
        topFr = ttk.Frame(top)
        topFr.grid(row=0,column=0)
        ttk.Label(topFr,text="MySql WOM Db").grid(row=0,column=2,sticky=W)
        ttk.Label(topFr,text="Host").grid(row=1,column=1,sticky=W)
        ttk.Label(topFr,text="Port").grid(row=2,column=1,sticky=W)
        ttk.Label(topFr,text="Database").grid(row=3,column=1,sticky=W)
        ttk.Label(topFr,text="User").grid(row=4,column=1,sticky=W)
        ttk.Label(topFr,text="Password").grid(row=5,column=1,sticky=W)
        
        ttk.Label(topFr,text="MSSQL IFCA Db").grid(row=0,column=4,sticky=W)
        ttk.Label(topFr,text="-").grid(row=1,column=3,sticky=W)
        ttk.Label(topFr,text="-").grid(row=2,column=3,sticky=W)
        ttk.Label(topFr,text="-").grid(row=3,column=3,sticky=W)
        ttk.Label(topFr,text="-").grid(row=4,column=3,sticky=W)
        ttk.Label(topFr,text="-").grid(row=5,column=3,sticky=W)

        self.entHost = LimitEntry(topFr,maxlen=16,width=20)
        self.entHost.grid(row=1, column=2)
        self.entPort = LimitEntry(topFr,maxlen=16,width=20)
        self.entPort.grid(row=2, column=2)
        self.entDb = LimitEntry(topFr,maxlen=16,width=20)
        self.entDb.grid(row=3, column=2)
        self.entUser = LimitEntry(topFr,maxlen=16,width=20)
        self.entUser.grid(row=4, column=2)
        self.entPass = LimitEntry(topFr,maxlen=16,show='*',width=20)
        self.entPass.grid(row=5, column=2)

        self.entMSHost = LimitEntry(topFr,maxlen=16,width=20)
        self.entMSHost.grid(row=1, column=4)
        self.entMSDb = LimitEntry(topFr,maxlen=16,width=20)
        self.entMSDb.grid(row=3, column=4)
        self.entMSUser = LimitEntry(topFr,maxlen=16,width=20)
        self.entMSUser.grid(row=4, column=4)
        self.entMSPass = LimitEntry(topFr,maxlen=16,show='*',width=20)
        self.entMSPass.grid(row=5, column=4)
        
        self.btnEdit=ttk.Button(topFr,text="Edit",width=7,command=self.edit_file)
        self.btnEdit.grid(row=6,column=1)
        self.btnSave=ttk.Button(topFr,text="Save",width=7,command=self.update_file)
        self.btnSave.grid(row=6,column=2)
        self.btnTest=ttk.Button(topFr,text="Test",width=7,command=self.test_conn)
        self.btnTest.grid(row=6,column=4)

        topFr.wait_visibility() # window needs to be visible for the grab
        topFr.grab_set()
        topFr.bind("<FocusOut>", self.alarm)
        self._set_transient(parent)
        self.read_file()

    def _set_transient(self, master, relx=0.5, rely=0.3):
        # window proses ikut parent (without icon taskbar)
        widget = self.top
        widget.withdraw() # Remain invisible while we figure out the geometry
        widget.transient(master)
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

    def entry_set(self,opsi):
        if opsi == "clear":
            self.entHost.delete(0,END)
            self.entPort.delete(0,END)
            self.entDb.delete(0,END)
            self.entUser.delete(0,END)
            self.entPass.delete(0,END)
            self.entMSHost.delete(0,END)
            self.entMSDb.delete(0,END)
            self.entMSUser.delete(0,END)
            self.entMSPass.delete(0,END)
        elif opsi == "read":
            self.entHost.config(state="readonly")
            self.entPort.config(state="readonly")
            self.entDb.config(state="readonly")
            self.entUser.config(state="readonly")
            self.entPass.config(state="readonly")
            self.entMSHost.config(state="readonly")
            self.entMSDb.config(state="readonly")
            self.entMSUser.config(state="readonly")
            self.entMSPass.config(state="readonly")
        elif opsi == "disable":
            self.entHost.config(state="disable")
            self.entPort.config(state="disable")
            self.entDb.config(state="disable")
            self.entUser.config(state="disable")
            self.entPass.config(state="disable")
            self.entMSHost.config(state="disable")
            self.entMSDb.config(state="disable")
            self.entMSUser.config(state="disable")
            self.entMSPass.config(state="disable")
        elif opsi == "normal":
            self.entHost.config(state="normal")
            self.entPort.config(state="normal")
            self.entDb.config(state="normal")
            self.entUser.config(state="normal")
            self.entPass.config(state="normal")
            self.entMSHost.config(state="normal")
            self.entMSDb.config(state="normal")
            self.entMSUser.config(state="normal")
            self.entMSPass.config(state="normal")
        else: pass

    def test_conn(self):
        try:
            con = mysql.connector.connect(**read_db_config())
            info = con.get_server_info()
            messagebox.showinfo(title="Version",parent=self.top,\
                message="Connected to MySQL Server version {}".format(info))
            cur = con.cursor()
            cur.execute("select database();")
            record = cur.fetchone()
            messagebox.showinfo(title="Database",parent=self.top,\
                message="You're connected to database: {}".format(record))
            cur.close()
            con.close()
            messagebox.showinfo(title="Finish",parent=self.top,\
                message="Checking finished, MySQL connection is closed")
        except mysql.connector.Error as err:
            messagebox.showerror(title="Error",parent=self.top,\
                message="SQL Log: {}".format(err))
        # Try connect MSSQL
        try:
            con = pypyodbc.connect(**read_db_config_ms())
            # info = con.get_server_info()
            # messagebox.showinfo(title="Version",parent=self.top,\
            #     message="Connected to MSSQL Server version {}".format(info))
            cur = con.cursor()
            cur.execute("SELECT @@version;")
            record = cur.fetchone()
            messagebox.showinfo(title="Database",parent=self.top,\
                message="You're connected to MSSQL: {}".format(record))
            cur.close()
            con.close()
            messagebox.showinfo(title="Finish",parent=self.top,\
                message="Checking finished, MSSQL connection is closed")
        except pypyodbc.Error as err:
            messagebox.showerror(title="Error",parent=self.top,\
                message="SQL Log: {}".format(err))

    def write_file(self):
        config_object = ConfigParser()
        config_object[secmysql] = {
            "host": "Server IP",
            "port": "Port Address",
            "database": "db name",
            "user": "username",
            "password": "password",
            "autocommit":"True"
            }
        config_object[secmssql] = {
            "driver": "{SQL Server Native Client 11.0}",
            "server": "Server IP",
            "database": "db name",
            "uid": "username",
            "pwd": "password",
            }
        #Write the above sections to config.ini file
        with open(getfile, 'w') as conf:
            config_object.write(conf)
        self.read_file()

    def read_file(self):
        self.btnEdit["state"] = "normal"
        self.btnTest["state"] = "normal"
        self.btnSave["state"] = "disabled"
        self.entry_set("clear")
        #Read config.ini file
        config_object = ConfigParser()
        config_object.read(getfile)
        if config_object.has_section(secmysql):
            userinfo = config_object[secmysql]
            self.entHost.insert(END,userinfo["host"])
            self.entPort.insert(END,userinfo["port"])
            self.entDb.insert(END,userinfo["database"])
            self.entUser.insert(END,userinfo["user"])
            self.entPass.insert(END,userinfo["password"])
        if config_object.has_section(secmssql):
            userinfoms = config_object[secmssql]
            self.entMSHost.insert(END,userinfoms["server"])
            self.entMSDb.insert(END,userinfoms["database"])
            self.entMSUser.insert(END,userinfoms["uid"])
            self.entMSPass.insert(END,userinfoms["pwd"])
            self.entry_set("disable")
        else:
            print('{0} not found in the {1} file'.format(secmysql,getfile))
            self.write_file()

    def edit_file(self,event=None):
        self.btnEdit["state"] = "disabled"
        self.btnTest["state"] = "disabled"
        self.btnSave["state"] = "normal"
        self.entry_set("normal")

    def update_file(self,event=None):
        #Read config.ini file
        config_object = ConfigParser()
        config_object.read(getfile)
        #Get the section
        update = config_object[secmysql]
        updatems = config_object[secmssql]
        #Update the items
        update["host"] = self.entHost.get()
        update["port"] = self.entPort.get()
        update["database"] = self.entDb.get()
        update["user"] = self.entUser.get()
        update["password"] = self.entPass.get()

        updatems["server"] = self.entMSHost.get()
        updatems["database"] = self.entMSDb.get()
        updatems["uid"] = self.entMSUser.get()
        updatems["pwd"] = self.entMSPass.get()
        #Write changes back to file
        with open(getfile, 'w') as conf:
            config_object.write(conf)
        self.read_file()

class TestRun(object):
    def __init__(self,master):
        self.master=master
        self.setbtn=ttk.Button(master,text="Config",command=self.popup)
        self.setbtn.pack()

    def popup(self):
        self.gopopup=SetConfig(self.master)
        self.setbtn["state"] = "disabled"
        self.master.wait_window(self.gopopup.top)
        self.setbtn["state"] = "normal"

if __name__ == "__main__":
    root=tk.Tk()
    TestRun(root)
    root.mainloop()

