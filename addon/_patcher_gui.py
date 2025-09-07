import tkinter as tk
import requests # pip3 install requests
import subprocess
import os
from threading import Thread
from configparser import ConfigParser
from tkinter import ttk,messagebox
from bs4 import BeautifulSoup # pip install BeautifulSoup4
from zipfile import ZipFile

getfile = str(os.getcwd())+"\\"+"remote.ini"

class pathcing(object):
    def __init__(self,parent):
        self.parent = parent
        self.parent.protocol("WM_DELETE_WINDOW",self.disable_event)
        self.parent.title("Downloading")
        self.result = False
        self.local = os.getcwd()
        # self.local = str(os.getcwd()+"\\"+"_testupdate") # for debugging

        subprocess.call("TASKKILL /F /IM main.exe", shell=True) # kill program before patching
        self.komponen()

    def komponen(self):
        lebar=500
        tinggi=50
        setTengahX = (self.parent.winfo_screenwidth()-lebar)//2
        setTengahY = (self.parent.winfo_screenheight()-tinggi)//2
        self.parent.geometry("%ix%i+%i+%i" %(lebar, tinggi,setTengahX, setTengahY-40)) # setTengahY-40 : Biar lebih keatas
        # self.parent.overrideredirect(1)

        self.pbar = ttk.Progressbar(orient="horizontal",length=500,mode="determinate", maximum=100, value=0)
        self.pbar.pack()
        self.plabel = ttk.Label(text="")
        self.plabel.pack()
        Thread(target=self.running).start()
        # self.running()

    def running(self):
        self.read_file()
        self.downloadallindex()
        if self.unpackupdate(self.local) == True:
            self.result = True
            print('Result:',self.result)
            print('Success: Your WOM has been succcessfuly update.')
            self.run_main()
    
    def disable_event(self):
        pass
        # if (messagebox.askokcancel("Attention","Do you really want to exit the App?")):
        #     print("ok")
        #     self.run_main()
        # else: print("no")

    def keluar(self,event=None):
        subprocess.call("TASKKILL /F /IM wompatcher.exe", shell=True)
        self.parent.destroy()

    def run_main(self):
        pathexe = str(self.local+"\\"+"main.exe")
        print("Starting mainprogram:",pathexe)
        subprocess.call([pathexe])
        self.keluar()

    def downloadallindex(self):
        links = []
        chunk_size = 512
        try: 
            page = requests.get(self.remote, timeout=5)
        except requests.exceptions.RequestException as e:
            # Tangkap semua error lain yang mungkin terjadi (misal: URL tidak valid)
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
            self.parent.destroy()
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
                    i += length - i
                    print(cek,':',file)
                    print('inc:',i,'size:',length)
                    print(percentage,'%')
            except OSError as e:
                pass
                print(cek,':',e)

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
            print(e)
            return False
        else:
            print('success unpack, then delete zip file')
            checkfile = os.path.isfile(sourcefile)
            if checkfile == True:
                os.remove(sourcefile)
            return True
    
    def read_file(self):
        config_object = ConfigParser()
        config_object.read(getfile)
        if config_object.has_section('server'):
            item = config_object['server']
            self.remote = item['update']
            self.fileup = item['fileup']
        else:
            print('{0} not found in the {1} file'.format('server',getfile))
            self.write_file()
    
    def write_file(self):
        config_object = ConfigParser()
        config_object['server'] = {
            "update": "http://127.0.0.1/test-server",
            "fileup": "WOM_Update.zip"
            }
        with open(getfile, 'w') as conf:
            config_object.write(conf)
        self.read_file()


if __name__ == "__main__":
    root=tk.Tk()
    pathcing(root)
    # TestRun(root)
    root.mainloop()