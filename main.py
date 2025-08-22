import os
import json
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import yt_dlp
from pathlib import Path


CONFIG_FILE = "config.json"

# Load saved config or set default
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    else:
        return {"download_folder": str(Path.home() / "Downloads")}

# Save config
def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

# Ask user for new folder
def change_download_folder():
    folder_selected = filedialog.askdirectory(
        initialdir=config["download_folder"],
        title="Select Download Folder"
    )
    if folder_selected:
        config["download_folder"] = folder_selected
        save_config(config)
        messagebox.showinfo("Download Folder Changed", f"New location:\n{folder_selected}")

# Get current download path for yt-dlp
def get_download_path():
    return os.path.join(config["download_folder"], "%(title)s.%(ext)s")


# Used to find the icon whether you're running from .py or bundled .exe
def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Point to local ffmpeg binary
def get_ffmpeg_path():
    if getattr(sys, 'frozen', False):  # Running in PyInstaller bundle
        return os.path.join(sys._MEIPASS, "ffmpeg")
    else:  # Running as script
        return os.path.abspath("ffmpeg")


ffmpeg_location = get_ffmpeg_path()


# ---------------- Progress Popup ----------------
def create_progress_window(title="Downloading..."):
    progress_win = tk.Toplevel(root)
    progress_win.title(title)
    progress_win.geometry("300x100")
    progress_win.resizable(False, False)
    progress_win.configure(bg='white')

    label = tk.Label(progress_win, text=title, font=('Arial', 11), bg='white')
    label.pack(pady=(15, 5))

    progress_bar = ttk.Progressbar(progress_win, length=250, mode='determinate')
    progress_bar.pack(pady=(5, 15))

    return progress_win, progress_bar


# ---------------- Download Video ----------------
def download_video(url, resolution):
    progress_win, progress_bar = create_progress_window("Downloading Video...")

    def progress_hook(d):
        if d['status'] == 'downloading':
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 1)
            percent = (downloaded / total) * 100
            progress_bar['value'] = percent
            progress_win.after(100, lambda: None)  # Non-blocking update
        elif d['status'] == 'finished':
            progress_bar['value'] = 100
            progress_win.after(100, lambda: None)

    try:
        ydl_opts = {
            'format': f'bestvideo[height={resolution}]+bestaudio/best/best',
            'ffmpeg_location': ffmpeg_location,
            'outtmpl': get_download_path(),
            'merge_output_format': 'mp4',
            'progress_hooks': [progress_hook],
            'concurrent_fragment_downloads': 5,  # Faster downloads
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        progress_win.destroy()
        messagebox.showinfo("Done", "Video downloaded successfully!")

    except Exception as e:
        progress_win.destroy()
        messagebox.showerror("Error", f"Video download failed:\n{e}")


# ---------------- Download MP3 ----------------
def download_mp3(url, mp3_quality):
    progress_win, progress_bar = create_progress_window("Downloading MP3...")

    def progress_hook(d):
        if d['status'] == 'downloading':
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 1)
            percent = (downloaded / total) * 100
            progress_bar['value'] = percent
            progress_win.after(100, lambda: None)
        elif d['status'] == 'finished':
            progress_bar['value'] = 100
            progress_win.after(100, lambda: None)

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'ffmpeg_location': ffmpeg_location,
            'outtmpl': get_download_path(),
            'progress_hooks': [progress_hook],
            'concurrent_fragment_downloads': 5,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': mp3_quality,
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        progress_win.destroy()
        messagebox.showinfo("Done", "MP3 downloaded successfully!")

    except Exception as e:
        progress_win.destroy()
        messagebox.showerror("Error", f"MP3 download failed:\n{e}")


# ---------------- Download Thumbnail ----------------
def download_thumbnail(url):
    try:
        ydl_opts = {
            'skip_download': True,
            'writethumbnail': True,
            'outtmpl': get_download_path(),
            'ffmpeg_location': ffmpeg_location,
            'postprocessors': [{
                'key': 'EmbedThumbnail',
            }, {
                'key': 'FFmpegThumbnailsConvertor',
                'format': 'jpg',
                'when': 'before_dl',
            }],
        }
        yt_dlp.YoutubeDL(ydl_opts).download([url])
        messagebox.showinfo("Done", "Thumbnail downloaded successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"Thumbnail download failed:\n{e}")


# ---------------- Thread Wrappers ----------------
def download_video_press():
    threading.Thread(
        target=download_video,
        args=(url.get(), res_options_map[resolution.get()]),
        daemon=True
    ).start()


def download_mp3_press():
    threading.Thread(
        target=download_mp3,
        args=(url.get(), quality_map[mp3_quality.get()]),
        daemon=True
    ).start()


def download_thumbnail_press():
    threading.Thread(
        target=download_thumbnail,
        args=(url.get(),),
        daemon=True
    ).start()


config = load_config()


# ---------------- UI Setup ----------------
root = tk.Tk()
root.title("Yankr")
root.geometry("400x265")
root.configure(bg='white')
root.resizable(False, False)
root.iconbitmap(get_resource_path("myicon.ico"))

# Variables
url = tk.StringVar()
resolution = tk.StringVar(value="1080p")
mp3_quality = tk.StringVar(value="High")

# Frame
main_frame = tk.Frame(root, bg='white')
main_frame.pack(pady=20, fill="both", expand=True)

# Configure grid columns to expand evenly
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)

# URL Entry
url_entry = tk.Entry(main_frame, textvariable=url, font=('Arial', 12), relief='groove', bd=2)
url_entry.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Resolution Dropdown
res_options = ["360p", "480p", "720p", "1080p"]
res_options_map = {"360p": "360", "480p": "480", "720p": "720", "1080p": "1080"}

res_dropdown = ttk.Combobox(main_frame, textvariable=resolution, values=res_options, state="readonly")
res_dropdown.grid(row=1, column=0, padx=(10, 5), pady=10, sticky="ew")

# MP3 Quality Dropdown
quality_display = ["Low", "Medium", "High"]
quality_map = {"Low": "128", "Medium": "192", "High": "320"}

quality_dropdown = ttk.Combobox(main_frame, textvariable=mp3_quality, values=quality_display, state="readonly")
quality_dropdown.grid(row=1, column=1, padx=(5, 10), pady=10, sticky="ew")

# Buttons
download_btn = tk.Button(main_frame, text="Download", command=download_video_press,
                         font=('Arial', 11, 'bold'), bg='#e5e5e5', fg='black',
                         height=2, relief='flat')
download_btn.grid(row=2, column=0, columnspan=2, pady=(5, 10), padx=10, sticky="ew")

# MP3 Button
mp3_btn = tk.Button(main_frame, text="Download MP3", command=download_mp3_press,
                    font=('Arial', 10, 'bold'), bg='#f0f0f0', fg='black',
                    relief='flat')
mp3_btn.grid(row=3, column=0, pady=5, padx=(10, 5), sticky="ew")

# Thumbnail Button
thumb_btn = tk.Button(main_frame, text="Download Thumbnail", command=download_thumbnail_press,
                      font=('Arial', 10, 'bold'), bg='#f0f0f0', fg='black',
                      relief='flat')
thumb_btn.grid(row=3, column=1, pady=5, padx=(5, 10), sticky="ew")

# Change Folder Button
btn_change_folder = tk.Button(main_frame, text="Change Download Folder", command=change_download_folder,
                              font=('Arial', 10, 'bold'), bg='#f0f0f0', fg='black',
                              relief='flat')
btn_change_folder.grid(row=4, column=0, columnspan=2, pady=(10, 5), padx=10, sticky="ew")

root.mainloop()
