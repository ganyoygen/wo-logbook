import tkinter as tk
import requests # pip3 install requests
import subprocess
import os
from clint.textui import progress # pip install clint
from configparser import ConfigParser
from tkinter import ttk
from bs4 import BeautifulSoup # pip install BeautifulSoup4
from zipfile import ZipFile

getfile = str(os.getcwd())+"\\"+"remote.ini"

class pathcing(object):
    def __init__(self,parent):
        self.parent = parent
        self.parent.protocol("WM_DELETE_WINDOW",self.disable_event)
        self.result = False
        self.local = os.getcwd()
        # self.local = str(os.getcwd()+"\\"+"_testupdate") # for debugging

        subprocess.call("TASKKILL /F /IM main.exe", shell=True) # kill program before patching

        self.read_file()
        self.downloadallindex()
        if self.unpackupdate(self.local) == True:
            self.result = True
            print('Result:',self.result)
            print('Success: Your WOM has been succcessfuly update.')
            self.run_main()
    
    def disable_event(self):
        pass

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
        chunk_size = 384
        page = requests.get(self.remote)
        soup = BeautifulSoup(page.content, 'html.parser')

        for link in (soup.find_all('a')):
            links.append(link['href'])

        print("")
        print('From:',self.remote)
        print('path:',self.local)
        print("")
        print('Found:',len(links))

        u=0
        cek = 0
        for link in links:
            req = requests.get(self.remote + '/' + link, stream = True)
            cek += 1
            try:
                i=0
                with open(self.local + '\\' + link, "wb") as file:
                    length = int(req.headers.get('content-length')) # byte size of file
                    # progbar = SetProgBar(self.parent,length)
                    # for chunk in progress.bar(req.iter_content(chunk_size), expected_size = (length/chunk_size), label = link):
                    for chunk in progress.bar(req.iter_content(chunk_size), expected_size = (length/chunk_size), label = link + "  "):
                    # for chunk in req.iter_content(chunk_size):
                        if chunk:
                            file.write(chunk)
                            i+= 1
                            # progbar.bytes += i
                    # progbar.bytes += length - i
                    u+=1
                    # print('Downloading:',i)
                    i += length - i
                    # print(cek,'File ke:',u,file)
                    # print('i=',i,'length:',length)
            except OSError as e:
                print(cek,':',e)

    def unpackupdate(self,destination):
        # destination = str(os.getcwd()+"\\"+"down")
        # sourcefile = str(os.getcwd()+"\\"+"down"+"\\"+"WOM_Update.zip")
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

def checkremote():
    #Read config.ini file
    config_object = ConfigParser()
    config_object.read(getfile)
    try:
        if config_object.has_section('server'):
            remoteaddr = config_object['server']
            return str(remoteaddr['update']) # tampilkan address dari file
    except:
        return ''

class TestRun(object):
    def __init__(self,master):
        self.master=master
        self.setbtn=ttk.Button(master,text="Update",command=self.popup)
        self.setbtn.pack()

    def popup(self):
        gopopup=pathcing(self.master)
        # self.setbtn["state"] = "disabled"
        # self.master.wait_window(gopopup.top)
        # try: self.setbtn["state"] = "normal"
        # except: pass

if __name__ == "__main__":
    root=tk.Tk()
    pathcing(root)
    # TestRun(root)
    # root.mainloop()
