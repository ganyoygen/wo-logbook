import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from configparser import ConfigParser
import requests
import json
from packaging import version
from _dl_patcher import PatcherDownloader

VERSION = "1.0-201026"
REMOTEADDR = os.path.join(os.getcwd(), "remote.ini")


def checkremote():
    config_object = ConfigParser()
    config_object.read(REMOTEADDR)
    try:
        if config_object.has_section("server"):
            return config_object["server"]["update"]
    except Exception:
        return ""
    return ""


def get_exe_version(file_path):
    try:
        import win32api
        info = win32api.GetFileVersionInfo(file_path, "\\")
        ms, ls = info["FileVersionMS"], info["FileVersionLS"]
        return f"{ms >> 16}.{ms & 0xFFFF}.{ls >> 16}.{ls & 0xFFFF}"
    except Exception as e:
        print("Error:", e)
        return None


class CheckVersion:
    def __init__(self, parent, verlocal):
        self.parent = parent
        self.localver = verlocal
        self.local_patch = os.path.join(os.getcwd(), "wompatcher.exe")
        self.ver_data = {}
        self.remote = checkremote() or "http://127.0.0.1/share"
        self.remotefile = f"{self.remote}/Version.json"
        self.result = False

        subprocess.call("TASKKILL /F /IM wompatcher.exe", shell=True)
        self.check_remotefile()

    def run_patcher(self):
        try:
            subprocess.Popen([self.local_patch], text=True)
        except Exception as err:
            messagebox.showerror("Error", f"{err}")
        self.keluar()

    def check_patcher(self):
        remotever = self.ver_data.get("patcher-ver", "").strip()
        print(f"Patcher Remote: {remotever}")

        localver = None
        if os.path.exists(self.local_patch):
            localver = get_exe_version(self.local_patch)
            print(f"Patcher Local: {localver}")
        else:
            print("File patcher tidak ditemukan")

        def need_update(remote, local):
            if not local:
                return True
            try:
                return version.parse(local.replace("-", ".")) < version.parse(remote.replace("-", "."))
            except Exception:
                return local < remote

        if need_update(remotever, localver):
            print("⚠️ Perlu update patcher dari server")
            dl_file = f"{self.remote}/wompatcher.exe"
            godownload = PatcherDownloader(self.parent, dl_file, self.local_patch)
            godownload.top.grab_set()
            self.parent.wait_window(godownload.top)
            self.update_or_pass()
        else:
            print("✅ Patcher sudah versi terbaru")
            self.update_or_pass()

    def check_remotefile(self):
        try:
            check = requests.get(self.remotefile, timeout=5)
            check.raise_for_status()
            self.ver_data = json.loads(check.text)
        except Exception as e:
            messagebox.showerror("Error", f"{e}")
        else:
            self.check_patcher()

    def update_or_pass(self):
        remotever = self.ver_data.get("wom-version", "").strip()
        if not remotever:
            print("⚠️ WOM remote version tidak ditemukan")
            return

        print(f"WOM Remote: {remotever}")
        print(f"WOM Local: {self.localver}")

        if version.parse(self.localver) < version.parse(remotever):
            mb1 = messagebox.askyesno(
                f"Update Available {remotever}",
                f"Ada update terbaru.\nVersi Server: {remotever}\nVersi Anda: {self.localver}\nKlik Yes untuk update.",
            )
            if mb1:
                self.result = True
                self.run_patcher()
        else:
            print("✅ WOM sudah versi terbaru")
        print(f'self.result: {self.result}')

    def keluar(self):
        if self.parent.winfo_exists():
            self.parent.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    # root.withdraw()
    root.iconify()  # root minimize
    root.after(0, lambda: CheckVersion(root, VERSION))
    root.mainloop()
