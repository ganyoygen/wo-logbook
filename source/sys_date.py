import os
import sys
import tkinter as tk
from tkinter import ttk, Toplevel
from tkcalendar import DateEntry
from datetime import datetime

def store_date(inputdate):
    inputdate = inputdate.replace('/','-')
    if len(str(inputdate)) >= 16:
        vdate, vtime = inputdate.split() #pisah tanggal dan jam
        try:
            dt = datetime.strptime(vdate,'%d-%m-%Y')
            return '{0}-{1:02}-{2:02} {3}'.format(dt.year,dt.month,dt.day,vtime)
        except: return ""
    elif len(str(inputdate)) == 10:
        try:
            dt = datetime.strptime(inputdate,'%d-%m-%Y')
            # print ('{0}-{1}-{2:02}'.format(dt.month, dt.day, dt.year % 100))
            return '{0}-{1:02}-{2:02}'.format(dt.year,dt.month,dt.day)
        except: return ""
    else:
        return ""

def get_date(inputdate):
    # return string
    inputdate = inputdate.replace('/','-')
    if len(str(inputdate)) >= 16:
        vdate, vtime = inputdate.split() #pisah tanggal dan jam
        try:
            dt = datetime.strptime(vdate,'%Y-%m-%d')
            return '{0:02}-{1:02}-{2} {3}'.format(dt.day,dt.month,dt.year,vtime)
        except: return ""
    elif len(str(inputdate)) == 10:
        try:
            dt = datetime.strptime(inputdate,'%Y-%m-%d')
            return '{0:02}-{1:02}-{2}'.format(dt.day,dt.month,dt.year)
        except: return ""
    else:
        return ""

class GetSeconds():
    def __init__(self,inputdate):
        inputdate = inputdate.replace('/','-')
        if len(str(inputdate)) >= 16:
            vdate, vtime = inputdate.split() #pisah tanggal dan jam
            if len(str(vtime)) == 5:
                vtime = vtime + ":00"
                inputdate = vdate +" "+ vtime
        elif len(str(inputdate)) == 10:
            inputdate = inputdate +" 00:00:00"
        try:
            formatingdate = datetime.strptime(inputdate,'%Y-%m-%d %H:%M:%S')
            self.value = datetime.timestamp(formatingdate)
        except: self.value = ""

class GetDuration():
    def __init__(self,seconds):
        seconds_in_day = 60 * 60 * 24
        seconds_in_hour = 60 * 60
        seconds_in_minute = 60

        days = seconds // seconds_in_day
        hours = (seconds - (days * seconds_in_day)) // seconds_in_hour
        minutes = (seconds - (days * seconds_in_day) - (hours * seconds_in_hour)) // seconds_in_minute
        if hours <= 0:
            self.value = "{} menit.".format(int(minutes))
        elif days <= 0:
            self.value = "{0} jam, {1} menit.".format(int(hours),int(minutes))
        else:
            self.value = "{0} hari, {1} jam, {2} menit.".format(int(days),int(hours),int(minutes))

class CustomDateEntry(DateEntry):
    def _select(self, event=None):
        date = self._calendar.selection_get()
        if date is not None:
            self._set_text(date.strftime('%d-%m-%Y'))
            self.event_generate('<<DateEntrySelected>>')
        self._top_cal.withdraw()
        if 'readonly' not in self.state():
            self.focus_set()

class PopupDateTime(object):
    def __init__(self,master):
        top = self.top = Toplevel(master)
        top.iconbitmap(str(os.getcwd()+"\\"+"icon-icons.com_main.ico"))
        self.parent = master
        self.value = ""
        topFrame = ttk.Frame(top)
        topFrame.grid(row=0,column=0)
        tanggal=ttk.Label(topFrame,text="Tanggal")
        tanggal.grid(row=0,column=0)
        tikdua = ttk.Label(topFrame,text=":")
        tikdua.grid(row=0,column=1)
        self.date = CustomDateEntry(topFrame, width=10, locale='en_UK')
        self.date.grid(row=0,column=2,sticky='W')
        jam=ttk.Label(topFrame,text="Jam")
        jam.grid(row=1,column=0)
        tikdua = ttk.Label(topFrame,text=":")
        tikdua.grid(row=1,column=1)

        vcmd = (top.register(self.onValidate), '%d', '%s', '%S')
        self.hour = ttk.Entry(topFrame, validate="key", validatecommand=vcmd, width=7)
        self.hour.bind("<KeyRelease>", self.hour_24)
        self.hour.grid(row=1,column=2,sticky='W')      

        self.okbtn=ttk.Button(topFrame,text="OK",width=7,command=self.cleanup)
        self.okbtn.grid(row=2,column=3)
        self.okbtn["state"] = "disabled"
        top.title("Input Date and Time")
        self.hour.focus_set()
        top.wait_visibility() # window needs to be visible for the grab
        top.grab_set()
        top.bind("<FocusOut>", self.alarm)
        self._set_transient(master)

    def onValidate(self, d, s, S):
        # if it's deleting return True
        if d == "0":
            return True
        # Allow only digit, ":" and check the length of the string
        if ((S == ":" and len(s) != 2) or (not S.isdigit() and
                S != ":") or (len(s) == 3 and int(S) > 5) or len(s) > 4):
            self.alarm()
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
        if len(s.get()) < 5: 
            self.okbtn["state"] = "disabled"
            self.hour.unbind("<Return>")
        if len(s.get()) == 5: 
            self.okbtn["state"] = "normal"
            self.hour.bind("<Return>",self.cleanup)
        if event.keysym=="BackSpace":
            return
        
        # check the hour format and add : between hours and minutes
        if len(s.get()) == 1 and int(s.get()) > 2:
            s.insert(0, "0")
            s.insert("end", ":")
        elif len(s.get()) == 2 and int(s.get()) < 24:
            s.insert(2, ":")
        elif len(s.get()) >= 2 and s.get()[2:3] != ":":
            self.alarm()
            s.delete(1, tk.END)

    def alarm(self, event=None):
        self.top.bell()

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

    def cleanup(self,event=None):
        self.value=self.date.get()+" "+self.hour.get()
        self.top.destroy()

class TestRun(object):
    def __init__(self,master):
        self.master=master
        self.setbtn=ttk.Button(master,text="Set Date",command=self.popup)
        self.setbtn.pack()
        self.showbtn=ttk.Button(master,text="Get Date",command=lambda: sys.stdout.write(self.entryValue()+'\n'))
        self.showbtn.pack()
    def popup(self):
        self.gopopup=PopupDateTime(self.master)
        self.setbtn["state"] = "disabled"
        self.master.wait_window(self.gopopup.top)
        self.setbtn["state"] = "normal"
    def entryValue(self):
        return self.gopopup.value


if __name__ == "__main__":
    root=tk.Tk()
    m=TestRun(root)
    root.mainloop()