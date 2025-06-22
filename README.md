# YouTube_downloader

mp4 and mp3 downloader with GUI
using Tkinter and ffmpeg,
packed into an .exe with pyinstaller

![youtubess](https://github.com/ShanTheShan/YouTube_downloader/assets/96246152/603ae35b-f6f5-4555-8477-94a390a312a0)

# Installation

Download ffmpeg (https://www.ffmpeg.org/download.html) (WINDOWS ONLY)<br>
Add a system path variable to the ffmpeg bin folder containing the .exe files<br>
Run yt_script.exe<br>
Enjoy!

# To Solve age restriction problem

open pytube script file named "_main_.py"
line 253, change client to `ANDROID`

# Build command

pyinstaller --onefile --noconsole yt_script.py
