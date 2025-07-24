# Yankr 🎥🎶

Yankr is a simple, user-friendly GUI application for downloading YouTube videos, audio (MP3), and thumbnails using the powerful `yt-dlp` backend.

This app supports:
- Downloading videos in resolutions like 360p, 480p, 720p, and 1080p
- Downloading MP3s in high-quality audio (128 kbps to 320 kbps)
- Downloading and converting video thumbnails to `.jpg`
- Embedded FFmpeg support (no external installation needed)
- Bundled into a portable `.exe` with PyInstaller

---

## 🚀 Features

- ✅ Simple, clean interface with Tkinter
- ✅ Multi-threaded downloading (no UI freeze)
- ✅ Custom icon embedded in the executable
- ✅ Automatically uses embedded FFmpeg if bundled

---

## 🖥️ Requirements

- Python 3.8 or later
- Modules:
  - `yt-dlp`
  - `tkinter` (comes with Python)
- FFmpeg binary (`ffmpeg.exe`) placed alongside your Python script

Install dependencies:

```bash
pip install yt-dlp
