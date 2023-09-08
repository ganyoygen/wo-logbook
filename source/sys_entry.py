import tkinter as tk
from tkinter import ttk,StringVar
from tkcalendar import DateEntry

class LimitEntry(ttk.Entry):
    def __init__(self,parent,maxlen=9,**kw):
        self.parent = parent
        self.maxlen = maxlen
        self.sv = sv = StringVar(parent)
        sv.trace("w", lambda name, index, mode, sv=sv: self.callback(sv))
        ttk.Entry.__init__(self,parent,textvariable=sv,**kw)

    def callback(self,sv):
        if len(sv.get()) > self.maxlen: self.bell()
        c = sv.get()[0:self.maxlen]
        sv.set(c.replace(" ", "")) # (remove whitespace) tidak boleh pake spasi
        # sv.set(c)

class CusDateEnt(ttk.Entry): # input tgl format 'en_UK' (dd-mm-yyyy)
    def __init__(self,parent,maxlen=10,**kw):
        self.parent = parent
        self.maxlen = maxlen
        self.sv = sv = StringVar(parent)
        sv.trace("w", lambda name, index, mode, sv=sv: self.callback(sv))
        ttk.Entry.__init__(self,parent,textvariable=sv,**kw)

    def callback(self,sv):
        if len(sv.get()) > self.maxlen: self.bell()
        sv.set(sv.get()[0:self.maxlen].replace(" ", ""))
        sv.set(sv.get()[0:self.maxlen].replace("/", "-"))

        tgl = sv.get()[:2]
        bln = sv.get()[3:5]
        thn = sv.get()[6:]
        if ((len(sv.get()) <= 3 and not tgl.isdigit()) or
            (len(sv.get()) == 4 and not bln.isdigit()) or
            (len(sv.get()) >= 7 and not thn.isdigit())): 
            sv.set('')
    
    def keycheck(self, event):
        s = event.widget
        if (len(s.get()) == 2 and event.keysym=="BackSpace" or
            len(s.get()) == 5 and event.keysym=="BackSpace"):
            s.delete(len(s.get())-1, tk.END)

        if event.keysym=="BackSpace":
            return
        
        tgl = s.get()[:2]
        bln = s.get()[3:5]
        thn = s.get()[6:]
        # if ((len(s.get()) <= 3 and not tgl.isdigit()) or
        #     (len(s.get()) == 4 and not bln.isdigit()) or
        #     (len(s.get()) >= 7 and not thn.isdigit())): 
        #     s.delete(0, tk.END)
        if (len(s.get()) == 1 and s.get() > '3' or
            len(s.get()) == 4 and s.get()[3] > '1'):
            s.insert(len(s.get())-1, "0")
            s.insert("end", "-")
        elif ((len(s.get()) == 2 and tgl < '32') or
            (len(s.get()) == 5 and bln < '13')):
            s.insert(len(s.get()), "-")
        elif (len(s.get()) >= 2 and s.get()[2:3] != "-" or # beri "-" setelah tgl
            len(s.get()) >= 5 and s.get()[5:6] != "-"): # beri "-" setelah bln
            self.bell()
            s.delete(len(s.get())-1, tk.END)

class CusHourEnt(ttk.Entry):
    def __init__(self,parent,maxlen=4,**kw):
        self.parent = parent
        self.maxlen = maxlen

        vcmd = (parent.register(self.onValidate), '%d', '%s', '%S')
        ttk.Entry.__init__(self,parent,validate="key",validatecommand=vcmd,**kw)

    def onValidate(self, d, s, S):
        # if it's deleting return True
        if d == "0":
            return True
        # Allow only digit, ":" and check the length of the string
        # if len(s) > self.maxlen: return False
        if ((S == ":" and len(s) != 2) or 
            (len(s) == 1 and str(S) > '9') or 
            (len(s) == 3 and str(S) > '5') or 
            len(s) > 4 or S == " "):
            # self.bell()
            return False
        return True

    def hour_24(self, event):
        """
        Check and build the correct format hour: hh:mm in 24 format
        it keep in mind the 0x, 1x and 2x hours and the max minutes can be 59
        """
 
        # get the object that triggered the event
        s = event.widget

        # if delete a char do return ok or delete the char ":" and the previous number
        
        if len(s.get()) == 2 and event.keysym=="BackSpace":
            s.delete(len(s.get())-1, tk.END)

        if event.keysym=="BackSpace":
            return
        
        # check the hour format and add : between hours and minutes
        jam = s.get()[:2]
        mnt = s.get()[3:]
        if len(s.get()) <= 3 and not jam.isdigit(): 
            s.delete(0, tk.END)
        elif len(s.get()) >= 4 and not mnt.isdigit(): 
            s.delete(0, tk.END)
        elif len(s.get()) == 1 and s.get() > '2':
            s.insert(0, "0")
            s.insert("end", ":")
        elif len(s.get()) == 2 and str(s.get()) < '24':
            s.insert(2, ":")
        elif len(s.get()) >= 2 and s.get()[2:3] != ":":
            self.bell()
            s.delete(1, tk.END)

class TestRun(object):
    def __init__(self,master):
        frame = ttk.Frame(master)
        frame.grid(row=0,column=0)
        ttk.Label(frame,text="Limit Entry").grid(row=1,column=0)
        entlimit = LimitEntry(frame,maxlen=6,width=10)
        entlimit.grid(row=1, column=1)
        ttk.Label(frame,text="Date Entry").grid(row=2,column=0)
        eCusDate = CusDateEnt(frame,width=10)
        eCusDate.grid(row=2, column=1)
        eCusDate.bind("<KeyRelease>", eCusDate.keycheck)
        ttk.Label(frame,text="Jam Entry").grid(row=3,column=0)
        entJam = CusHourEnt(frame,width=10)
        entJam.grid(row=3, column=1)
        entJam.bind("<KeyRelease>", entJam.hour_24)

if __name__ == "__main__":
    root=tk.Tk()
    TestRun(root)
    root.mainloop()