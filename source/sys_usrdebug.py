from tkinter import *
from tkinter import ttk
from sys_entry import LimitEntry

class PopupUser(object):
    def __init__(self,master):
        top = self.top = Toplevel(master)
        self.parent = master
        self.user = ""
        self.dept = ""
        self.top.protocol("WM_DELETE_WINDOW", self.keluar)
        self.entUser = LimitEntry(top,width=20)
        self.entUser.bind("<KeyRelease>", self.setuser)
        self.entUser.pack()
        self.entUser.insert(END, 'Debug')
        self.opsidept = ttk.Combobox(top, \
            values = ["ENG","DOCON","RCP","CS","ROOT"], \
            state="readonly",width=15)
        self.opsidept.current(0)
        self.opsidept.pack()
        self.setbtn=ttk.Button(top,text="Start",command=self.cleanup,width=10)
        self.setbtn.pack()
        self.setbtn["state"] = "disabled"
        # top.bind("<FocusOut>", self.alarm)
        # top.resizable(0,0)
        self._set_transient(master)

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
    
    def keluar(self,event=None):
        pass
        # close app by master windows
    
    def setuser(self,event):
        s = event.widget
        if len(s.get()) < 1: self.setbtn["state"] = "disabled"
        else: self.setbtn["state"] = "normal"

    def cleanup(self,event=None):
        self.user = self.entUser.get()
        self.dept = self.opsidept.get()
        print("User:",self.user)
        print("Dept:",self.dept)
        self.top.destroy()

if __name__ == "__main__":
    from ttkthemes import ThemedTk
    root = ThemedTk(theme='clearlooks')
    setuser = PopupUser(root)
    setuser.parent.wait_window(setuser.top)
    print('Finish')