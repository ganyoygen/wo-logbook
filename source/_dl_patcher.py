import os
import requests
import threading
import tkinter as tk
from tkinter import ttk, messagebox


class PatcherDownloader:
    def __init__(self, parent, url: str, local_path: str, on_finish=None):
        self.parent = parent
        self.url = url
        self.local_path = local_path
        self.on_finish = on_finish
        self.parent.protocol("WM_DELETE_WINDOW",self.keluar)

        # ==== Atur posisi window di tengah ====
        self.center_window(650, 125)

        # Frame UI
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(self.frame, text="Downloading Patcher...").pack()

        # Progress bar
        self.pbar = ttk.Progressbar(self.frame, orient="horizontal",
                                    length=500, mode="determinate")
        self.pbar.pack(pady=5)

        # Label status
        self.label_status = ttk.Label(self.frame, text="Menunggu...")
        self.label_status.pack()

        # Tombol mulai
        self.btn_start = ttk.Button(self.frame, text="Mulai Download",
                                    command=self.start_download_thread)
        # self.btn_start.pack(pady=5)
        self.start_download_thread()

    def keluar(self,event=None):
        self.parent.destroy()

    def center_window(self, width, height):
        """Atur window parent agar muncul di tengah layar"""
        self.parent.update_idletasks()
        ws = self.parent.winfo_screenwidth()
        hs = self.parent.winfo_screenheight()
        x = (ws // 2) - (width // 2)
        y = (hs // 2) - (height // 2)
        self.parent.geometry(f"{width}x{height}+{x}+{y}")

    def start_download_thread(self):
        """Jalankan proses download di thread terpisah"""
        self.btn_start.config(state="disabled")
        self.label_status.config(text="Memulai download...")
        thread = threading.Thread(target=self.download_file, daemon=True)
        thread.start()

    def download_file(self):
        """Proses download file dengan progress"""
        try:
            with requests.get(self.url, stream=True, timeout=10) as r:
                r.raise_for_status()
                total_size = int(r.headers.get("content-length", 0))
                downloaded = 0

                os.makedirs(os.path.dirname(self.local_path), exist_ok=True)

                with open(self.local_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=10240):  # 10 KB
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)

                            # Hitung persen
                            percent = int(downloaded * 100 / total_size) if total_size else 0

                            # Update GUI lewat .after
                            self.parent.after(0, self.update_progress, percent, downloaded, total_size)
                            
            # === Validasi ukuran file ===
            if total_size and downloaded < total_size:
                self.parent.after(0, lambda: messagebox.showerror(
                "Error", "Download tidak lengkap, update dibatalkan."
                ))
                return
            
            # === Download sukses ===
            # self.parent.after(0, lambda: messagebox.showinfo("Selesai", f"Patcher berhasil diunduh ke:\n{self.local_path}"))
            # self.parent.after(0, lambda: self.keluar())
            print(f'onfinish {self.on_finish}')
            if self.on_finish:
                self.parent.after(0, self.on_finish)
            self.keluar() # setelah download selesai, agar bisa jalankan wompatcher.exe di _checkver.py
                        
        except Exception as e:
            self.parent.after(0, lambda: messagebox.showerror("Error", f"Gagal download patcher:\n{e}"))
        finally:
            self.parent.after(0, lambda: self.btn_start.config(state="normal"))

    def update_progress(self, percent, downloaded, total_size):
        """Update progress bar dan label status"""
        self.pbar["value"] = percent
        self.label_status.config(text=f"{percent}% ({downloaded}/{total_size} bytes)")


# Contoh pemakaian langsung
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Patcher Downloader")

    url = "http://127.0.0.1/share/wompatcher.exe"   # ganti sesuai servermu
    local_path = os.path.join(os.getcwd(), "wompatcher.exe")
    # local_path = os.path.join(os.getcwd(), "_testupdate", "wompatcher.exe")  # for debugging

    downloader = PatcherDownloader(root, url, local_path)

    root.mainloop()
