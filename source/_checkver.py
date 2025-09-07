import tkinter as tk
import requests # pip3 install requests
import subprocess
import os
from configparser import ConfigParser
from tkinter import ttk,messagebox

getfile = str(os.getcwd())+"\\"+"remote.ini"
VERSION = "1.0-201026" # sample version

class checkversion(object):
    def __init__(self,parent,version):
        self.parent = parent
        self.result = False
        self.local = os.getcwd()
        # self.local = str(os.getcwd()+"\\"+"_testupdate") # for debugging
        self.localver = version

        if checkremote() == '' or checkremote() == None:
            print("ERROR: Missing file remote.ini")
            self.remote = 'http://127.0.0.1/test-server'
        else:
            self.remote = checkremote()
        
        subprocess.call("TASKKILL /F /IM wompatcher.exe", shell=True) # kill wompatcher while running main
        self.begin_checkupdate()

    def keluar(self,event=None):
        subprocess.call("TASKKILL /F /IM main.exe", shell=True)
        self.parent.destroy()

    def run_main(self):
        pathexe = str(self.local+"\\"+"wompatcher.exe")
        print("Starting patcher:",pathexe)
        subprocess.call([pathexe],text=True) #Console hilang
        # subprocess.call([pathexe]) #patcher keluar tapi keterangan blank hitam
        self.keluar()

    def begin_checkupdate(self):
        update = str(self.remote)+'/'+'version.txt'
        try:
            check = requests.get(update, timeout=5)
            self.remotever = check.text
        
            print('V-Remote:',check.text.replace('.','').replace('-',''))

            if self.localver.replace('.','').replace('-','') < check.text.replace('.','').replace('-',''):
                mb1 = messagebox.askyesno('Update Available Version: {0}'.format(self.remotever), \
                    'There is an update available. \
                    \r\nYour local Version: {0} \
                    \r\nClick yes to update.'.format(self.localver)) #confirming update with user
                if mb1 is True:
                    self.result = True
                    self.run_main()
                elif mb1 is False:
                    print('Result:',self.result)
            else:
                # messagebox.showinfo('Updates Not Available', 'No updates are available')
                print("No updates are available")
        
        except requests.exceptions.Timeout:
            messagebox.showerror("Error", "Request timeout! Server tidak merespons tepat waktu.")
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error", "Gagal terhubung ke server. Periksa koneksi internet.")
        except requests.exceptions.HTTPError as e:
            messagebox.showerror("Error", f"HTTP Error: {e.response.status_code}")
        except requests.exceptions.RequestException as e:
        # Tangkap semua error lain yang mungkin terjadi (misal: URL tidak valid)
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
        

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

if __name__ == "__main__":
    root=tk.Tk()
    version = VERSION
    checkversion(root,version)