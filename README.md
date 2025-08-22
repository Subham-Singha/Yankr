# Yankr 🎥🎶

Yankr is a simple, user-friendly GUI application for downloading YouTube videos, audio (MP3), and thumbnails using the powerful `yt-dlp` backend.

This app supports:
- Downloading videos in resolutions like 360p, 480p, 720p, and 1080p  
- Downloading MP3s in high-quality audio (128 kbps to 320 kbps)  
- Downloading and converting video thumbnails to `.jpg`  
- Embedded **FFmpeg** support (no external installation needed)  
- Bundled into a portable `.exe` with **PyInstaller**  
- Persistent **download folder setting** (user can choose once, and it’s remembered)  

---

## 🚀 Features

- ✅ Simple, clean interface with Tkinter  
- ✅ Multi-threaded downloading (no UI freeze)  
- ✅ Custom icon embedded in the executable  
- ✅ Built-in **“Change Download Folder”** option  
- ✅ Saves settings locally, so your chosen folder is remembered next time  
- ✅ Automatically uses embedded FFmpeg if bundled  
- ✅ Portable `.exe` build, no external dependencies required  

---

## 🖥️ Requirements

- **Python 3.8 – 3.11 recommended** (3.13 has limited PyInstaller/cffi support at the moment)  
- Modules:  
  - `yt-dlp`  
  - `tkinter` (comes with Python)  
  - `ffmpeg` (binary, included in the bundled release)  

Install dependencies:

```bash
pip install yt-dlp
```

---

## 📦 Build Instructions (Windows)

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Place `ffmpeg.exe` and `ffprobe.exe` inside a folder named `ffmpeg/`  

3. Run build command:
   ```bash
   pyinstaller --onefile --windowed --icon=myicon.ico ^
   --add-data "ffmpeg/ffmpeg.exe;ffmpeg" ^
   --add-data "ffmpeg/ffprobe.exe;ffmpeg" ^
   --add-data "myicon.ico;." main.py
   ```

4. The built `.exe` will be inside the `dist/` folder.

---

## 📝 Notes

- First run will create a config file (e.g. `config.json`) to remember your download folder.  
- You can always change it later using the **Change Download Folder** button.  
- If you see Windows SmartScreen warning “unrecognized app,” it’s because the `.exe` is unsigned. To distribute widely, you’d need a code-signing certificate (not free).  
