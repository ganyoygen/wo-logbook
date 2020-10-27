import tkinter as tk
from tkinter import ttk,StringVar

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
       
if __name__ == '__main__':
    root=tk.Tk()
    LimitEntry(root,maxlen=5,width=10).pack() # cek limit entry max 5 char 
    root.mainloop()