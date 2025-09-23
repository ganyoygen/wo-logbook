import tkinter as tk
import requests # pip3 install requests
import subprocess
import os
import win32api
import json
from configparser import ConfigParser
from tkinter import messagebox
from packaging import version
from _dl_patcher import PatcherDownloader

REMOTEADDR = str(os.getcwd())+"\\"+"remote.ini"
VERSION = "1.0-201026" # sample version

class CheckVersion(object):
    def __init__(self,parent,verlocal):
        self.parent = parent
        self.parent.protocol("WM_DELETE_WINDOW",self.keluar)
    
        self.result = False
        self.local = os.getcwd()
        # self.local = str(os.getcwd()+"\\"+"_testupdate") # for debugging
        self.localver = verlocal
        self.ver_data = {}

        if checkremote() == '' or checkremote() == None:
            print("ERROR: Missing file remote.ini")
            self.remote = 'http://127.0.0.1/share'
        else:
            self.remote = checkremote()
        
        self.remotefile = str(self.remote)+'/'+'Version.json'

        subprocess.call("TASKKILL /F /IM wompatcher.exe", shell=True) # kill wompatcher while running main
        self.check_remotefile()
        # self.update_or_pass()

#cek lagi ini, jika update tersedia tapi wompathcher tidak ditemukan jgn close wom
    def keluar(self,event=None):
        # subprocess.call("TASKKILL /F /IM main.exe", shell=True) # kill old program
        # subprocess.call("TASKKILL /F /IM wom.exe", shell=True)
        self.parent.destroy()

    def begin_update(self):
        pathexe = str(self.local+"\\"+"wompatcher.exe")
        self.check_patcher(pathexe)
        print("Starting patcher:",pathexe)
        print("Debug tahan dulu, return")
        return
        try: 
            subprocess.Popen([pathexe],text=True) #Console hilang
            # subprocess.call([pathexe]) #patcher keluar tapi keterangan blank hitam
        except Exception as err:
            messagebox.showerror("Error", f"{err}")
        # self.keluar()

    def check_patcher(self,pathpatcher):
        def need_update(remotever: str, localver: str | None) -> bool:
            """
            Return True kalau perlu update.
            """
            # Normalisasi remote
            remote_norm = remotever.replace("-", ".").strip()

            # Kalau localver tidak ada → wajib update
            if not localver:
                return True

            # Normalisasi local
            local_norm = localver.replace("-", ".").strip()

            try:
                return version.parse(local_norm) < version.parse(remote_norm)
            except Exception:
                # Fallback: bandingkan string angka saja
                r = "".join(ch for ch in remotever if ch.isdigit())
                l = "".join(ch for ch in localver if ch.isdigit())
                return l < r
        
        localver = None
        remotever = self.ver_data.get("patcher-ver", "").strip()
        print(f'Patcher Remote: {remotever}')
        if os.path.exists(pathpatcher):
            localver = get_exe_version(pathpatcher)
            print(f'Patcher _Local: {localver}')
        else:
            print("File Patcher tidak ditemukan.")
            # print("Seharusnya download patcher dari server")
        
        if need_update(remotever, localver):
            dl_file = f"{self.remote}/wompatcher.exe"
            # self.parent.after(0, lambda: PatcherDownloader(self.parent, dl_file, pathpatcher))
            self.parent.after(0, lambda: PatcherDownloader(
            self.parent,
            dl_file,
            pathpatcher,
            on_finish=lambda: (
                subprocess.Popen([pathpatcher]) if os.path.exists(pathpatcher) else messagebox.showerror("Error", "Patcher gagal diunduh")
            )
            ))
            print("⚠️ Perlu update patcher dari server")
        else:
            print("✅ Patcher sudah versi terbaru")

    def check_remotefile(self):
        try:
            check = requests.get(self.remotefile, timeout=5)
            check.raise_for_status()  # raise error jika status bukan 200
            # remotever = check.text.strip() # ini dari file .txt

            self.ver_data = json.loads(check.text) # Parse sebagai JSON
            # return self.ver_data

        except requests.exceptions.Timeout:
            messagebox.showerror("Error", "Request timeout! Server tidak merespons tepat waktu.")
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error", "Gagal terhubung ke server. Periksa koneksi internet.")
        except requests.exceptions.HTTPError as e:
            messagebox.showerror("Error", f"HTTP Error: {e.response.status_code}")
        except requests.exceptions.RequestException as e:
        # Tangkap semua error lain yang mungkin terjadi (misal: URL tidak valid)
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
        else: 
            print(f'self.ver_data: {self.ver_data}')
            self.update_or_pass()
        # return

    def update_or_pass(self):
        # remotever = str(self.check_remotefile()("wom-version", "").strip())
        remotever = self.ver_data.get("wom-version", "").strip()
        if not remotever:
            print("⚠️ versi remote tidak ditemukan")
            return

        print(f'WOM Remote: {remotever}')
        print(f'WOM _Local: {self.localver}')

        # if self.localver.replace('.','').replace('-','') < check.text.replace('.','').replace('-',''):
        if version.parse(self.localver) < version.parse(remotever):
            mb1 = messagebox.askyesno('Update Available Version: {0}'.format(remotever), \
                'There is an update available. \
                \r\nYour local Version: {0} \
                \r\nClick yes to update.'.format(self.localver)) #confirming update with user
            if mb1 is True:
                self.result = True
                self.begin_update()
        else:
            # messagebox.showinfo('Updates Not Available', 'No updates are available')
            print("No updates are available")      
        print(f'self.resut = {self.result}')
        return


def checkremote():
    #Read config.ini file
    config_object = ConfigParser()
    config_object.read(REMOTEADDR)
    try:
        if config_object.has_section('server'):
            remoteaddr = config_object['server']
            return str(remoteaddr['update']) # tampilkan address dari file
    except:
        return ''

def get_exe_version(file_path):
    try:
        info = win32api.GetFileVersionInfo(file_path, '\\')
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        version = f"{ms >> 16}.{ms & 0xFFFF}.{ls >> 16}.{ls & 0xFFFF}"
        return version
    except Exception as e:
        print("Error:", e)
        return None

if __name__ == "__main__":
    root=tk.Tk()
    # root.iconify()  # root minimize
    CheckVersion(root,VERSION)
    root.mainloop()