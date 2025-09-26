# Module download wompatcher.exe
# Test atau debug di _checkver.py
import os
import requests
import threading
import tkinter as tk
from tkinter import ttk, messagebox


class PatcherDownloader:
    def __init__(self, parent, url: str, local_path: str, on_finish=None):
        self.top = tk.Toplevel(parent)
        self.top.title("Patcher Downloader")

        self.url = url
        self.local_path = local_path
        self.on_finish = on_finish

        # ✅ posisikan window di tengah
        self.center_window(650, 125)

        # UI
        ttk.Label(self.top, text="Downloading patcher...").pack(pady=5)
        self.pbar = ttk.Progressbar(self.top, orient="horizontal", length=500, mode="determinate")
        self.pbar.pack(pady=5)
        self.label_status = ttk.Label(self.top, text="Menunggu...")
        self.label_status.pack()

        # mulai langsung
        threading.Thread(target=self.download_file, daemon=True).start()

    def center_window(self, width, height):
        """Tempatkan window di tengah layar"""
        self.top.update_idletasks()
        ws = self.top.winfo_screenwidth()
        hs = self.top.winfo_screenheight()
        x = (ws // 2) - (width // 2)
        y = (hs // 2) - (height // 2)
        self.top.geometry(f"{width}x{height}+{x}+{y}")

    def download_file(self):
        try:
            with requests.get(self.url, stream=True, timeout=10) as r:
                r.raise_for_status()
                total_size = int(r.headers.get("content-length", 0))
                downloaded = 0

                os.makedirs(os.path.dirname(self.local_path), exist_ok=True)
                with open(self.local_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=10240):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            percent = int(downloaded * 100 / total_size) if total_size else 0
                            self.top.after(0, self.update_progress, percent, downloaded, total_size)

            # sukses
            # self.top.after(0, lambda: messagebox.showinfo("Selesai", f"Berhasil download patcher ke:\n{self.local_path}"))
            self.top.after(0, print(f'Berhasil download patcher ke:\n{self.local_path}'))
            if self.on_finish:
                self.top.after(0, self.on_finish)

        except Exception as e:
            self.top.after(0, lambda: messagebox.showerror("Error", f"Gagal download patcher:\n{e}"))

        finally:
            self.top.after(0, self.keluar)

    def update_progress(self, percent, downloaded, total_size):
        if self.top.winfo_exists():
            self.pbar["value"] = percent
            self.label_status.config(text=f"{percent}% ({downloaded}/{total_size} bytes)")

    def keluar(self):
        if self.top.winfo_exists():
            self.top.destroy()
