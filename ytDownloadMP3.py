import yt_dlp
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube MP3 Downloader")
        self.root.geometry("400x250")
        
        # URL Label and Entry
        self.url_label = ttk.Label(root, text="YouTube URL:")
        self.url_label.pack(pady=5)
        
        self.url_entry = ttk.Entry(root, width=50)
        self.url_entry.pack(pady=5)
        
        # Output Directory Label and Entry
        self.dir_label = ttk.Label(root, text="Output Directory (optional):")
        self.dir_label.pack(pady=5)
        
        self.dir_entry = ttk.Entry(root, width=50)
        self.dir_entry.pack(pady=5)
        
        # Progress Label
        self.progress_label = ttk.Label(root, text="")
        self.progress_label.pack(pady=5)
        
        # Download Button
        self.download_button = ttk.Button(root, text="Download MP3", command=self.start_download)
        self.download_button.pack(pady=10)
        
        # Status Label
        self.status_label = ttk.Label(root, text="Ready")
        self.status_label.pack(pady=5)

    def download_progress(self, d):
        """Update progress label during download"""
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%')
            self.progress_label.config(text=f"Progress: {p}")
        elif d['status'] == 'finished':
            self.progress_label.config(text="Converting to MP3...")

    def download_youtube_mp3(self, url, output_dir):
        try:
            # Use current directory if no output dir specified
            if not output_dir:
                output_dir = "."
            
            # Create directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Download options
            options = {
                'format': 'bestaudio/best',
                'keepvideo': False,
                'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'progress_hooks': [self.download_progress],
            }
            
            # Download the audio
            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([url])
            
            self.status_label.config(text="Download completed!")
            self.progress_label.config(text="")
            messagebox.showinfo("Success", "MP3 download completed successfully!")
            
        except Exception as e:
            self.status_label.config(text="Error occurred")
            self.progress_label.config(text="")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        # Re-enable download button
        self.download_button.config(state="normal")

    def start_download(self):
        """Start download in a separate thread"""
        url = self.url_entry.get().strip()
        output_dir = self.dir_entry.get().strip()
        
        if not url:
            messagebox.showwarning("Warning", "Please enter a YouTube URL")
            return
            
        # Disable button during download
        self.download_button.config(state="disabled")
        self.status_label.config(text="Downloading...")
        
        # Run download in separate thread to prevent GUI freezing
        download_thread = threading.Thread(
            target=self.download_youtube_mp3,
            args=(url, output_dir)
        )
        download_thread.start()

def main():
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()