import os
import platform
import subprocess
import requests
from threading import Thread
from tkinter import ttk, Toplevel, messagebox
from configparser import ConfigParser
from pathlib import Path
from bs4 import BeautifulSoup
from zipfile import ZipFile
import tkinter as tk
import winshell

VERSION = "2.2-250922"
GETFILE = Path.cwd() / "remote.ini"


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

    def _set_transient(self, master, relx=0.5, rely=1.6):
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

class CrShortcut:
    def __init__(self, working_directory, target_path):
        """Buat shortcut di desktop Windows."""
        shortcut_name = "Work Order Manager.lnk"
        desktop_path = winshell.desktop()
        shortcut_filepath = os.path.join(desktop_path, shortcut_name)

        with winshell.shortcut(shortcut_filepath) as link:
            link.description = "Work Order Manager"
            link.path = str(target_path)
            link.working_directory = str(working_directory)

        print(f"Shortcut '{shortcut_name}' created on {desktop_path}.")

class Pathcing:
    def __init__(self, parent: tk.Tk):
        self.parent = parent
        self.parent.protocol("WM_DELETE_WINDOW", self.disable_event)
        self.parent.title(f"WOM Patcher v{VERSION} for Patch or Update")

        # folder update & exe
        self.local = Path.cwd()
        # self.local = Path.cwd() / "_testupdate" # for debugging
        self.pathexe = self.local / "wom.exe"
        self.local.mkdir(parents=True, exist_ok=True)

        # hentikan process (Windows only)
        if platform.system() == "Windows":
            for prog in ("main.exe", "wom.exe"):
                try:
                    subprocess.run(["TASKKILL", "/F", "/IM", prog], shell=True)
                except Exception as e:
                    print(f"WARNING: gagal kill {prog}: {e}")
        # subprocess.call("TASKKILL /F /IM main.exe", shell=True)
        # subprocess.call("TASKKILL /F /IM wom.exe", shell=True)

        self.komponen() # build UI
        self.startwiththread() # start patch thread

    # ---------------------------
    # Thread handling
    # ---------------------------
    def startwiththread(self):
        self.dlthread = Thread(target=self.running, daemon=True)
        self.dlthread.start()

    # ---------------------------
    # UI komponen
    # ---------------------------
    def komponen(self):
        lebar, tinggi = 650, 125
        setTengahX = (self.parent.winfo_screenwidth() - lebar) // 2
        setTengahY = (self.parent.winfo_screenheight() - tinggi) // 2
        self.parent.geometry(f"{lebar}x{tinggi}+{setTengahX}+{setTengahY-40}")

        # progress bar per file
        self.pbar_file = ttk.Progressbar(
            orient="horizontal", length=500, mode="determinate", maximum=100, value=0
        )
        self.pbar_file.pack()
        self.plabel_file = ttk.Label(text="")
        self.plabel_file.pack()

        # progress bar total
        self.pbar_total = ttk.Progressbar(
            orient="horizontal", length=500, mode="determinate", maximum=100, value=0
        )
        self.pbar_total.pack()
        self.plabel_total = ttk.Label(text="")
        self.plabel_total.pack()

        # pesan status
        self.replab = ttk.Label(text="")
        self.replab.pack()

    # ---------------------------
    # Main worker function
    # ---------------------------
    def running(self):
        self.read_file()
        if self.unpackupdate(self.local):
            self.replab.config(text="Success: Your WOM has been successfully updated.")
            # buat shortcut di main thread (hindari COM error di thread worker)
            self.parent.after(0, lambda: CrShortcut(self.local, self.pathexe))
            self.run_main()
        else:
            self.write_file()

    # ---------------------------
    # Exit / event handling
    # ---------------------------
    def disable_event(self):
        if messagebox.askokcancel("Attention", "Quit Update?"):
            self.keluar()

    def keluar(self, event=None):
        try:
            subprocess.call("TASKKILL /F /IM wompatcher.exe", shell=True)
        except Exception:
            pass
        self.parent.destroy()

    # ---------------------------
    # Main program launcher
    # ---------------------------
    def run_main(self):
        oldwom = self.local / "main.exe"
        if oldwom.exists():
            print("Deleted File:", oldwom)
            oldwom.unlink()
        print("Starting main program:", self.pathexe)
        try:
            subprocess.call([str(self.pathexe)])
        except Exception as err:
            messagebox.showerror("Error", f"{err}")
        self.keluar()

    # ---------------------------
    # Download & unpack logic
    # ---------------------------
    def checkurl(self):
        self.listfile = []
        try:
            self.page = requests.get(self.remote, timeout=5)
        except requests.exceptions.RequestException as e:
            self.plabel_file.config(text="")
            self.plabel_total.config(text="")
            self.replab.config(text=f"{e}")
            return False
        else:
            soup = BeautifulSoup(self.page.content, "html.parser")
            for link in soup.find_all("a"):
                self.listfile.append(link["href"])

            if self.fileup in self.listfile:
                print("File:", self.fileup, "ditemukan di server.")
                return True
            else:
                self.replab.config(text=f"No such file: {self.fileup} in: {self.remote}")
                return False

    def downloadallindex(self):
        print(f"From: {self.remote}")
        print(f"Path: {self.local}")
        print(f"Found: {len(self.listfile)}")

        total_files = len(self.listfile)
        chunk_size = 32768 # 10240 = 10 KB
        for idx, link in enumerate(self.listfile, start=1):
            req = requests.get(f"{self.remote}/{link}", stream=True)
            try:
                with open(self.local / link, "wb") as file:
                    length = int(req.headers.get("content-length", 0))
                    downloaded = 0
                    self.pbar_file["value"] = 0  # reset progress per file
                    for chunk in req.iter_content(chunk_size):
                        if chunk:
                            file.write(chunk)
                            downloaded += len(chunk)
                            # progress per file
                            percentage_file = downloaded * 100 / length if length else 0
                            self.pbar_file["value"] = percentage_file
                            self.plabel_file.config(
                                text=f"{link} : {int(percentage_file)}%"
                            )
                    # setelah file selesai → update progress total
                    percentage_total = idx * 100 / total_files
                    self.pbar_total["value"] = percentage_total
                    self.plabel_total.config(
                        text=f"Total: {idx}/{total_files} files ({int(percentage_total)}%)"
                    )
                    self.replab.config(text=f"Downloaded {link}")
            except Exception as e:
                self.replab.config(text=f"{idx} : {e}")

    def unpackupdate(self, destination: Path):
        sourcefile = destination / self.fileup
        try:
            with ZipFile(sourcefile, "r") as zObject:
                zObject.extractall(path=destination)
        except Exception as e:
            self.replab.config(text=str(e))
            # File Update tidak sesuai, hapus file yang telah terdownload
            for file in self.listfile:
                f = destination / file
                if f.exists():
                    f.unlink()
                    print("Deleted File:", f)
            return False
        else:
            self.replab.config(text="success unpack, then delete zip file")
            if sourcefile.exists():
                sourcefile.unlink()
            return True

    # ---------------------------
    # Config handling
    # ---------------------------
    def read_file(self):
        try:
            config_object = ConfigParser()
            config_object.read(GETFILE)
            if config_object.has_section("server"):
                item = config_object["server"]
                self.remote = item["update"]
                self.fileup = item["fileup"]
                if self.checkurl():
                    self.downloadallindex()
                else:
                    self.write_file()
            else:
                self.replab.config(text=f"URL not found in {GETFILE}")
                self.write_file()
        except Exception as err:
            self.replab.config(text=str(err))
            self.write_file()

    def write_file(self):
        self.gopopup=PopupAddress(self.parent)
        self.parent.wait_window(self.gopopup.top)
        config_object = ConfigParser()
        config_object['server'] = {
            "update": self.gopopup.value, # data dari input entry
            "fileup": "WOM_Update.zip"
            }
        with open(GETFILE, 'w') as conf:
            config_object.write(conf)
        self.running()


def start():
    root = tk.Tk()
    Pathcing(root)
    try:
        root.iconbitmap(str(Path.cwd() / "icon-patcher.ico"))
    except Exception:
        pass
    root.mainloop()


if __name__ == "__main__":
    start()
