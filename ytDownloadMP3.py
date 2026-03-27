import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import os
import sys
import threading

class YouTubeMP3Downloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube MP3 Downloader")
        self.root.geometry("480x340")
        
        # Cross-platform default output directory
        if os.name == 'nt':  # Windows
            self.default_output_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        else:
            self.default_output_dir = os.path.expanduser("~/Downloads")
        
        os.makedirs(self.default_output_dir, exist_ok=True)
        
        # Find bundled ffmpeg/ffprobe when running as .exe
        self.ffmpeg_location = self.get_ffmpeg_path()
        
        # URL
        ttk.Label(root, text="YouTube / YouTube Music URL:").pack(pady=8)
        self.url_entry = ttk.Entry(root, width=65)
        self.url_entry.pack(pady=5, padx=20)
        
        # Output Directory
        ttk.Label(root, text="Output Directory:").pack(pady=8)
        self.dir_var = tk.StringVar(value=self.default_output_dir)
        self.dir_entry = ttk.Entry(root, textvariable=self.dir_var, width=65)
        self.dir_entry.pack(pady=5, padx=20)
        
        ttk.Button(root, text="Browse...", command=self.browse_folder).pack(pady=5)
        
        self.progress_label = ttk.Label(root, text="", foreground="blue")
        self.progress_label.pack(pady=10)
        
        ttk.Button(root, text="Download MP3", command=self.start_download).pack(pady=10)
        
        self.status_label = ttk.Label(root, text="Ready")
        self.status_label.pack(pady=5)

    def get_ffmpeg_path(self):
        """Return path to ffmpeg when running as PyInstaller onefile"""
        if getattr(sys, 'frozen', False):  # Running as .exe
            base_path = sys._MEIPASS
            ffmpeg_path = os.path.join(base_path, "ffmpeg.exe")
            if os.path.exists(ffmpeg_path):
                return base_path  # Return the directory containing ffmpeg.exe
        return None  # Fall back to system/default

    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.default_output_dir)
        if folder:
            self.dir_var.set(folder)

    def start_download(self):
        url = self.url_entry.get().strip()
        output_dir = self.dir_var.get().strip() or self.default_output_dir
        
        if not url:
            messagebox.showerror("Error", "Please enter a valid URL")
            return
        
        self.download_button = self.root.nametowidget(".!button")  # rough way, or store reference
        # For simplicity we'll disable the main button later if needed

        self.progress_label.config(text="Starting...")
        self.status_label.config(text="Downloading...")

        threading.Thread(target=self.download_video, args=(url, output_dir), daemon=True).start()

    def download_video(self, url, output_dir):
        try:
            output_template = os.path.join(output_dir, '%(title)s - %(artist)s.%(ext)s')
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_template,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'noplaylist': True,
                'no_check_certificate': True,
            }
            
            # Pass ffmpeg location if we bundled it
            if self.ffmpeg_location:
                ydl_opts['ffmpeg_location'] = self.ffmpeg_location
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.progress_label.config(text="Downloading audio...")
                ydl.download([url])
            
            self.root.after(0, self.download_success)
            
        except Exception as e:
            self.root.after(0, lambda: self.download_error(str(e)))

    def download_success(self):
        self.progress_label.config(text="")
        self.status_label.config(text="✅ Download completed!")
        messagebox.showinfo("Success", "MP3 downloaded successfully to your chosen folder!")

    def download_error(self, error_msg):
        self.progress_label.config(text="")
        self.status_label.config(text="❌ Failed")
        messagebox.showerror("Download Error", f"Error:\n{error_msg}")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeMP3Downloader(root)
    root.mainloop()
