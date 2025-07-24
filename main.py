import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import yt_dlp
import sys
import threading


# Used to find the icon whether you're running from .py or bundled .exe
def get_resource_path(relative_path):
    try:
        # This will be defined by PyInstaller in onefile mode
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

# progress bar
def progress_popup():
    progress_win = tk.Toplevel(root)
    progress_win.title("Downloading...")
    progress_win.geometry("300x100")
    progress_win.resizable(False, False)
    progress_win.configure(bg='white')

    label = tk.Label(progress_win, text="Downloading...", font=('Arial', 11), bg='white')
    label.pack(pady=(15, 5))

    progress = ttk.Progressbar(progress_win, length=250, mode='determinate')
    progress.pack(pady=(5, 15))

    return progress_win, progress


# video download function
def download_video(url, resolution):
    # Create popup on main thread
    progress_win = tk.Toplevel(root)
    progress_win.title("Downloading...")
    progress_win.geometry("300x100")
    progress_win.resizable(False, False)
    progress_win.configure(bg='white')

    label = tk.Label(progress_win, text="Downloading...", font=('Arial', 11), bg='white')
    label.pack(pady=(15, 5))

    progress_bar = ttk.Progressbar(progress_win, length=250, mode='determinate')
    progress_bar.pack(pady=(5, 15))

    # Force rendering before download starts
    progress_win.update_idletasks()

    def progress_hook(d):
        if d['status'] == 'downloading':
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 1)
            percent = (downloaded / total) * 100
            progress_bar['value'] = percent
            progress_win.update_idletasks()
        elif d['status'] == 'finished':
            progress_bar['value'] = 100
            progress_win.update_idletasks()

    try:
        ydl_opts = {
            'format': f'bestvideo[height={resolution}]+bestaudio/best',
            'ffmpeg_location': ffmpeg_location,
            'outtmpl': '%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'progress_hooks': [progress_hook],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        progress_win.destroy()
        messagebox.showinfo("Done", "Download completed successfully!")

    except Exception as e:
        progress_win.destroy()
        messagebox.showerror("Error", f"Download failed:\n{e}")



# audio download function
def download_mp3(url, mp3_quality):
    # Create progress popup
    progress_win = tk.Toplevel(root)
    progress_win.title("Downloading MP3...")
    progress_win.geometry("300x100")
    progress_win.resizable(False, False)
    progress_win.configure(bg='white')

    label = tk.Label(progress_win, text="Downloading MP3...", font=('Arial', 11), bg='white')
    label.pack(pady=(15, 5))

    progress_bar = ttk.Progressbar(progress_win, length=250, mode='determinate')
    progress_bar.pack(pady=(5, 15))

    progress_win.update_idletasks()

    def progress_hook(d):
        if d['status'] == 'downloading':
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 1)
            percent = (downloaded / total) * 100
            progress_bar['value'] = percent
            progress_win.update_idletasks()
        elif d['status'] == 'finished':
            progress_bar['value'] = 100
            progress_win.update_idletasks()

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'ffmpeg_location': ffmpeg_location,
            'outtmpl': '%(title)s.%(ext)s',
            'progress_hooks': [progress_hook],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': mp3_quality,
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        progress_win.destroy()
        messagebox.showinfo("Done", "Download completed successfully!")

    except Exception as e:
        progress_win.destroy()
        messagebox.showerror("Error", f"Download failed:\n{e}")


# thumnail download function
def download_thumbnail(url):
    try:
        ydl_opts = {
            'skip_download': True,
            'writethumbnail': True,
            'outtmpl': '%(title)s.%(ext)s',
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
        messagebox.showinfo("Done", "Download completed successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"Download failed:\n{e}")

#function calls
def download_video_press():
    thread = threading.Thread(target=download_video, args=(url.get(), res_options_map[resolution.get()]))
    thread.start()

def download_mp3_press():
    thread = threading.Thread(target=download_mp3, args=(url.get(), quality_map[mp3_quality.get()]))
    thread.start()


def download_thumbnail_press():
    download_thumbnail(url.get())


# Define root window
root = tk.Tk()
root.title("Yankr")
root.geometry("400x250")
root.configure(bg='white')
root.resizable(False, False)
root.iconbitmap(get_resource_path("myicon.ico"))

# Variables
url = tk.StringVar()
resolution = tk.StringVar(value="1080p")
mp3_quality = tk.StringVar(value="High")

# Frame for spacing and layout
main_frame = tk.Frame(root, bg='white')
main_frame.pack(pady=20)

# URL Entry
url_entry = tk.Entry(main_frame, textvariable=url, font=('Arial', 12), relief='groove', bd=2, width=38)
url_entry.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Resolution Dropdown
res_options = ["360p", "480p", "720p", "1080p"]
res_options_map = {"360p": "360", "480p": "480", "720p": "720", "1080p": "1080"}

res_dropdown = ttk.Combobox(main_frame, textvariable=resolution, values=res_options, state="readonly", width=17)
res_dropdown.grid(row=1, column=0, padx=(10, 5), pady=10)

# MP3 Quality Dropdown
quality_display = ["Low", "Medium", "High"]
quality_map = {"Low": "128", "Medium": "192", "High": "320"}

quality_dropdown = ttk.Combobox(main_frame, textvariable=mp3_quality, values=quality_display, state="readonly", width=17)
quality_dropdown.grid(row=1, column=1, padx=(5, 10), pady=10)

# Download Button
download_btn = tk.Button(main_frame, text="Download", command=download_video_press, font=('Arial', 11, 'bold'), bg='#e5e5e5', fg='black',
                         height=2, width=32, relief='flat')
download_btn.grid(row=2, column=0, columnspan=2, pady=(5, 10))

# MP3 and Thumbnail Buttons
mp3_btn = tk.Button(main_frame, text="Download MP3", command=download_mp3_press, font=('Arial', 10, 'bold'), bg='#f0f0f0',
                    fg='black', width=17, relief='flat')
mp3_btn.grid(row=3, column=0, pady=5, padx=(10, 5))

thumb_btn = tk.Button(main_frame, text="Download Thumbnail", command=download_thumbnail_press, font=('Arial', 10, 'bold'), bg='#f0f0f0',
                      fg='black', width=17, relief='flat')
thumb_btn.grid(row=3, column=1, pady=5, padx=(5, 10))

root.mainloop()



