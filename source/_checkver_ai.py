import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from configparser import ConfigParser
import requests
import json
from urllib.parse import urljoin

# import downloader patcher (file terpisah)
from _dl_patcher import PatcherDownloader

VERSION = "2.1-250920"
GETFILE = str(os.getcwd())+"\\"+"remote.ini"


def get_exe_version(path: str) -> str:
    """Dummy contoh baca versi EXE (kamu bisa ganti dengan implementasi asli)."""
    try:
        import win32api
        info = win32api.GetFileVersionInfo(path, "\\")
        ms = info["FileVersionMS"]
        ls = info["FileVersionLS"]
        return f"{ms >> 16}.{ms & 0xFFFF}.{ls >> 16}.{ls & 0xFFFF}"
    except Exception:
        return "0.0.0.0"


def normalize_version(ver: str) -> str:
    """Normalisasi versi agar bisa dibandingkan."""
    ver = ver.replace("-", ".").strip()
    parts = ver.split(".")
    while len(parts) < 4:
        parts.append("0")
    return ".".join(parts)


def to_tuple(ver: str):
    return tuple(int(p) for p in ver.split("."))


class CheckVersion:
    def __init__(self, parent, local_version: str):
        self.parent = parent
        self.local_version = local_version
        self.remotefile = None
        self.ver_data = {}

        # baca file remote.ini
        self.read_file()

        if self.remotefile:
            self.check_remotefile()

    def read_file(self):
        """Baca remote.ini untuk mendapatkan URL server."""
        if os.path.exists(GETFILE):
            config_object = ConfigParser()
            config_object.read(GETFILE)
            if config_object.has_section("server"):
                self.remotefile = config_object["server"].get("update", "").strip()
        else:
            messagebox.showerror("Error", f"Config file {GETFILE} tidak ditemukan.")

    def check_remotefile(self):
        """Ambil file versi dari server (format JSON)."""
        try:
            check = requests.get(self.remotefile, timeout=5)
            check.raise_for_status()
            self.ver_data = json.loads(check.text)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal cek versi di server:\n{e}")
            return

        # cek versi patcher
        self.check_patcher(os.path.join(os.getcwd(), "wompatcher.exe"))

    def check_patcher(self, pathpatcher):
        """Bandingkan versi patcher lokal vs remote."""
        remotever = self.ver_data.get("patcher-ver", "").strip()
        print(f"Patcher Remote: {remotever}")

        if os.path.exists(pathpatcher):
            localver = get_exe_version(pathpatcher)
            print(f"Patcher Local : {localver}")
        else:
            localver = "0.0.0.0"
            print("File patcher tidak ditemukan, dianggap versi 0.0.0.0")

        # normalisasi
        local_norm = normalize_version(localver)
        remote_norm = normalize_version(remotever)

        if to_tuple(local_norm) < to_tuple(remote_norm):
            print("⚠️ Patcher perlu update dari server")
            patcher_url = urljoin(self.remotefile.rstrip("/") + "/", "wompatcher.exe")

            # jalankan downloader
            self.parent.after(
                0,
                lambda: PatcherDownloader(
                    tk.Toplevel(self.parent),  # gunakan Toplevel agar window baru
                    patcher_url,
                    pathpatcher,
                    on_finish=lambda: subprocess.Popen([pathpatcher]),
                ),
            )
        else:
            print("✅ Patcher sudah versi terbaru")


# ====== Entry Point ======
if __name__ == "__main__":
    root = tk.Tk()
    # root.withdraw()  # sembunyikan root agar tidak muncul window kosong
    CheckVersion(root, VERSION)
    root.mainloop()
