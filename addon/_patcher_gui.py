import tkinter as tk
import requests # pip3 install requests
import subprocess
import os
from threading import Thread
from configparser import ConfigParser
from tkinter import ttk,Toplevel,messagebox
from bs4 import BeautifulSoup # pip install BeautifulSoup4
from zipfile import ZipFile

VERSION = "2.1-250920"

getfile = str(os.getcwd())+"\\"+"remote.ini"

class PopupAddress(object):
    def __init__(self,master):
        top = self.top = Toplevel(master)
        top.title("Input Remote Address")
        top.protocol("WM_DELETE_WINDOW",self.keluar)
        self.parent = master
        self.value = ""
        topFrame = ttk.Frame(top)
        topFrame.grid(row=0,column=0)
        host=ttk.Label(topFrame,text="Host")
        host.grid(row=0,column=0)
        tikdua = ttk.Label(topFrame,text=":")
        tikdua.grid(row=0,column=1)
        self.host = ttk.Entry(topFrame,width=50)
        self.host.grid(row=0, column=2)
        self.host.bind('<Return>', self.cleanup)
        self.okbtn=ttk.Button(topFrame,text="OK",width=7,command=self.cleanup)
        self.okbtn.grid(row=1,column=2)
        self._set_transient(master)

    def _set_transient(self, master, relx=0.5, rely=3):
        # window proses ikut parent (without icon taskbar)
        widget = self.top
        widget.withdraw() # Remain invisible while we figure out the geometry
        widget.transient(master) # saat ini matikan saja, karena jika showdesktop wom sudah dibuka kembali
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
        self.value = self.host.get()
        self.top.destroy()

    def keluar(self,event=None):
        pass
        # close app by master windows

class pathcing(object):
    def __init__(self,parent):
        self.parent = parent
        self.parent.protocol("WM_DELETE_WINDOW",self.disable_event)
        self.parent.title("Downloading")
        self.result = False
        self.local = os.getcwd()
        # self.local = str(os.getcwd()+"\\"+"_testupdate") # for debugging

        subprocess.call("TASKKILL /F /IM main.exe", shell=True) # kill program before patching
        subprocess.call("TASKKILL /F /IM wom.exe", shell=True) # kill program before patching
        self.komponen()
        self.startwiththread()

    def startwiththread(self):
        dlthread = Thread(target=self.running)
        dlthread.daemon = True # Allows the thread to exit with the main program
        dlthread.start()

    def komponen(self):
        lebar=650
        tinggi=70
        setTengahX = (self.parent.winfo_screenwidth()-lebar)//2
        setTengahY = (self.parent.winfo_screenheight()-tinggi)//2
        self.parent.geometry("%ix%i+%i+%i" %(lebar, tinggi,setTengahX, setTengahY-40)) # setTengahY-40 : Biar lebih keatas
        # root.eval('tk::PlaceWindow . center')

        self.pbar = ttk.Progressbar(orient="horizontal",length=500,mode="determinate", maximum=100, value=0)
        self.pbar.pack()
        self.plabel = ttk.Label(text="")
        self.plabel.pack()
        self.replab = ttk.Label(text="")
        self.replab.pack()

    def running(self):
        self.read_file()
        if self.unpackupdate(self.local) == True:
            self.result = True
            print('Result:',self.result)
            self.replab.config(text='Success: Your WOM has been succcessfuly update.')
            self.run_main()
        else: self.write_file()
    
    def disable_event(self):
        pass
        if (messagebox.askokcancel("Attention","Quit Update?")):
            print("quit")
            self.keluar()
        else: print("no")

    def keluar(self,event=None):
        subprocess.call("TASKKILL /F /IM wompatcher.exe", shell=True)
        self.parent.destroy()

    def run_main(self):
        pathexe = str(self.local+"\\"+"wom.exe")
        oldwom = str(self.local+"\\"+"main.exe")
        checkfile = os.path.isfile(oldwom)
        if checkfile == True:
            print('Deleted File:',oldwom)
            os.remove(oldwom)
        print("Starting mainprogram:",pathexe)
        try: 
            subprocess.call([pathexe])
        except Exception as err:
            messagebox.showerror("Error", f"{err}")
        self.keluar()

    def checkurl(self):
        try: 
            self.page = requests.get(self.remote, timeout=5)
            return True
        except requests.exceptions.RequestException as e:
            # Tangkap semua error lain yang mungkin terjadi (misal: URL tidak valid)
            self.plabel.config(text='')
            self.replab.config(text=f"{e}")
            return False

    def downloadallindex(self,page):
        self.listfile = links = []
        chunk_size = 512
        soup = BeautifulSoup(page.content, 'html.parser')

        for link in (soup.find_all('a')):
            links.append(link['href'])

        print("")
        print('From:',self.remote)
        print('path:',self.local)
        print("")
        print('Found:',len(links))

        cek = 0
        for link in links:
            req = requests.get(self.remote + '/' + link, stream = True)
            cek += 1
            try:
                i=0
                with open(self.local + '\\' + link, "wb") as file:
                    length = int(req.headers.get('content-length')) # byte size of file
                    # for chunk in progress.bar(req.iter_content(chunk_size), expected_size = (length/chunk_size), label = link + "  "):
                    for chunk in req.iter_content(chunk_size):
                        if chunk:
                            file.write(chunk)
                            i+= chunk_size
                            percentage = i * 100/length
                            self.pbar["value"] = percentage
                            self.plabel.config(text=str(int(percentage))+"%")
                            self.replab.config(text=str(cek)+' / '+str(len(links))+' : '+str(link)+' : '+str(i)+' / '+str(length))
                    i += length - i
                    # print(cek,':',file)
                    # print('inc:',i,'size:',length)
                    # print(percentage,'%')
            except OSError as e:
                self.plabel.config(text='Found: '+str(len(links))+" Result(s)")
                self.replab.config(text=str(cek)+' : '+str(e))
                pass
            except Exception as e:
                self.replab.config(text=str(cek)+' : '+str(e))
                pass

    def unpackupdate(self,destination):
        # sourcefile = current dir + file name
        sourcefile = str(destination+"\\"+self.fileup)
        # loading the temp.zip and creating a zip object
        try:
            with ZipFile(sourcefile, 'r') as zObject:
            # Extracting all the members of the zip 
            # into a specific location.
                zObject.extractall(path=destination)
        except Exception as e:
            self.replab.config(text=str(e))
            # File Update tidak sesuai, hapus file yang telah terdownload
            for file in self.listfile:
                sourcefile = str(destination+"\\"+file)
                if os.path.isfile(sourcefile) == True:
                    os.remove(sourcefile)
                    print('Deleted File:',sourcefile)
            return False
        else:
            self.replab.config(text='success unpack, then delete zip file')
            checkfile = os.path.isfile(sourcefile)
            if checkfile == True:
                os.remove(sourcefile)
            return True
    
    def read_file(self):
        try:
            config_object = ConfigParser()
            config_object.read(getfile)
            if config_object.has_section('server'):
                item = config_object['server']
                self.remote = item['update']
                self.fileup = item['fileup']
                if self.checkurl() == True:
                    self.downloadallindex(self.page)
                else: self.write_file()
            else:
                self.replab.config(text='{0} not found in {1}'.format('URL',getfile))
                self.write_file()
        except Exception as err:
            self.replab.config(text=err)
            self.write_file()
    
    def write_file(self):
        self.gopopup=PopupAddress(self.parent)
        self.parent.wait_window(self.gopopup.top)
        config_object = ConfigParser()
        config_object['server'] = {
            "update": self.gopopup.value, # data dari input entry
            "fileup": "WOM_Update.zip"
            }
        with open(getfile, 'w') as conf:
            config_object.write(conf)
        self.running()


def start():
    global root
    root=tk.Tk()
    pathcing(root)
    try: root.iconbitmap(str(os.getcwd()+"\\"+"icon-patcher.ico"))
    except: pass
    root.mainloop()

if __name__ == "__main__":
    start()