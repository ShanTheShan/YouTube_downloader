from pytube import YouTube
import tkinter as tk
from tkinter import Entry,Button,Label, Radiobutton, StringVar, IntVar, Text, END, ttk ,HORIZONTAL,filedialog
import ffmpeg
import os
import re
import subprocess
from threading import Thread

#to allow ffmpeg function to run simulataenously with tkinter, previous windows not responsing
def threading(): 
    displayOutput.config(state="normal")
    displayOutput.delete(1.0, END)
    displayOutput.tag_configure("center", justify='center')
    displayOutput.insert(END, "Downloading... Do not close window!")
    displayOutput.tag_add("center", "1.0", "end")
    displayOutput.config(state="disabled")

    t1=Thread(target=download) 
    t1.start()


class Bar:
    def __init__(self,window):
        self.progress = ttk.Progressbar(window, orient = HORIZONTAL, length = 100, mode = 'indeterminate')
        self.progress.start(15)

    def show_bar(self):
        self.progress.pack() 

    def hide_bar(self):
        self.progress.pack_forget()


def ff_conversion(vid,aud,directory,outputname):
    ffmpeg.concat(vid, aud, v=1, a=1).output(os.path.join(directory, f"{outputname}.mp4")).overwrite_output().run()
    progressBar.hide_bar()


def download_video(URL:str,resolution):
    assert isinstance(URL,str), 'URL was not provided'
    
    global mp4_flag,mp3_flag

    if mp3_flag is True:
        #create folder to store files
        path = './YouTube Downloader Files'
        if not os.path.exists(path):
            os.mkdir(path)

        youtube_obj = YouTube(URL)
        obj_stream = youtube_obj.streams.filter(only_audio=True).first()
        output_name = "".join([c for c in obj_stream.title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        obj_stream.download(output_path=path,filename=output_name+'.mp3')

        #set display to write, enter text, then set to read only
        progressBar.hide_bar()

        displayOutput.config(state="normal")
        displayOutput.delete(1.0, END)
        displayOutput.tag_configure("center", justify='center')
        displayOutput.insert(END, "Downloaded successfully!")
        displayOutput.tag_add("center", "1.0", "end")
        displayOutput.config(state="disabled")
        

    else:
        #create folder to store files
        path = './YouTube Downloader Files'
        if not os.path.exists(path):
            os.mkdir(path)

        filter_res = None

        if resolution == 1:
            filter_res = '1080p'

        if resolution == 2:
            filter_res = '720p'

        if resolution == 3:
            filter_res = '360p'

        #for 1080p, have to combine audio video manually
        if filter_res == '1080p':
            path = './YouTube Downloader Files'
            if not os.path.exists(path):
                os.mkdir(path)

            youtube_obj = YouTube(URL)
            #downloads audio
            obj_stream = youtube_obj.streams.filter(only_audio=True).first()
            output_name = "".join([c for c in obj_stream.title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
            obj_stream.download(output_path=path,filename=output_name+'.mp3')
            #downloads video, video file name has '_g.mp4'
            obj_stream_video = youtube_obj.streams.filter(res=filter_res)
            obj_stream_video[0].download(output_path=path,filename=output_name+'_g.mp4')
            
            #define relative path to the audio and video files
            relative_V = os.path.join(path,output_name +"_g.mp4").replace('\\','/')
            relative_A = os.path.join(path,output_name +".mp3").replace('\\','/')

            #combine files into one
            video_f = ffmpeg.input(relative_V)
            audio_f = ffmpeg.input(relative_A)
            
            ff_conversion(video_f, audio_f,path,output_name)

            #delete the mp4 and mp3 file
            os.remove(relative_A)
            os.remove(relative_V)

            #set display to write, enter text, then set to read only
            displayOutput.config(state="normal")
            displayOutput.delete(1.0, END)
            displayOutput.tag_configure("center", justify='center')
            displayOutput.insert(END, "Downloaded successfully!")
            displayOutput.tag_add("center", "1.0", "end")
            displayOutput.config(state="disabled")
        
        else:
            youtube_obj = YouTube(URL,use_oauth=False)
            obj_stream = youtube_obj.streams.filter(res=filter_res)
            print(obj_stream[0])
            obj_stream[0].download(output_path=path)
            
            #set display to write, enter text, then set to read only
            progressBar.hide_bar()

            displayOutput.config(state="normal")
            displayOutput.delete(1.0, END)
            displayOutput.tag_configure("center", justify='center')
            displayOutput.insert(END, "Downloaded successfully!")
            displayOutput.tag_add("center", "1.0", "end")
            displayOutput.config(state="disabled")


#flag for button
mp4_flag = False
mp3_flag = False

#main GUI
window = tk.Tk()
progressBar = Bar(window)

#display size
window.geometry('600x530')
window.eval('tk::PlaceWindow . center')

#labels
window.title("YTD")
url_prompt = tk.Label(window, text="Enter YouTube URL",font=2)
url_prompt.pack(side="top")

#input for URL
url_type = StringVar()
url_input = Entry(window, width=60, textvariable=url_type)
url_input.pack(side="top")


#function to toggle display
def toggle_mp4():
    global mp4_flag #prevents creation of a local radioiable called mp4_flag

    if not mp4_flag:
        mp4_button.config(bg = "green")
        mp4_flag = True

    else:
        mp4_button.config(bg = "#C6C6C6")
        mp4_flag = False

def toggle_mp3():
    global mp3_flag

    if not mp3_flag:
        mp3_button.config(bg = "green")
        mp3_flag = True
    
    else:
        mp3_button.config(bg = "#C6C6C6")
        mp3_flag = False

#calls the pytube script, contains logic as well
def download():
    global download_flag,ok

    #if both audio and video options were selected, stop!
    if mp4_flag is True and mp3_flag is True:
        #set display to write, enter text, then set to read only
        displayOutput.config(state="normal")
        displayOutput.delete(1.0, END)
        displayOutput.tag_configure("center", justify='center')
        displayOutput.insert(END, "Select either VIDEO or AUDIO, not both...")
        displayOutput.tag_add("center", "1.0", "end")
        displayOutput.config(state="disabled")
        return
    
    selected_radio = radio.get()
    selected_url = url_input.get()

    #ensure format is chosen
    if mp4_flag is False and mp3_flag is False:
        displayOutput.config(state="normal")
        displayOutput.delete(1.0, END)
        displayOutput.tag_configure("center", justify='center')
        displayOutput.insert(END, "Select a format first.")
        displayOutput.tag_add("center", "1.0", "end")
        displayOutput.config(state="disabled")
        return

    #ensure res is selected
    if selected_radio == 0 and mp4_flag is True:
        displayOutput.config(state="normal")
        displayOutput.delete(1.0, END)
        displayOutput.tag_configure("center", justify='center')
        displayOutput.insert(END, "Choose a resolution.")
        displayOutput.tag_add("center", "1.0", "end")
        displayOutput.config(state="disabled")
        return
 
    try:
        #display progress bar for video download
        progressBar.show_bar()
        download_video(selected_url,selected_radio)

    except Exception as e:
        displayOutput.config(state="normal")
        displayOutput.delete(1.0, END)
        displayOutput.tag_configure("center", justify='center')
        displayOutput.insert(END, "Download failed..." + str(e))
        displayOutput.tag_add("center", "1.0", "end")
        displayOutput.config(state="disabled")
        


#global var, all related to mp3 to wav conversion
fullMusicPath = None
match = None

# Function for opening the 
# file explorer window
def browseFiles():
    try:
        filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes=(
                                            ("MP3 files", "*.mp3"),
                                            ))
    
        global fullMusicPath
        fullMusicPath = filename

        pattern = "[^\/]+$"
        global match

        match = re.search(pattern,filename)
        match = match.group(0)
        # Change label contents
        label_file_explorer.config(text = match)

    except Exception as e:
        return



def convertFile(file):
    if file != None:
        #create folder to store files
        path = './Converted Files'
        if not os.path.exists(path):
            os.mkdir(path)
    else:
        displayOutputConversion.config(state="normal")
        displayOutputConversion.delete(1.0, END)
        displayOutputConversion.tag_configure("center", justify='center')
        displayOutputConversion.insert(END, "Open a file first...")
        displayOutputConversion.tag_add("center", "1.0", "end")
        displayOutputConversion.config(state="disabled")
        return

    try:
        progressBar.show_bar()
        print('progress bar shown')
        fileString = match.split('.')[0]
        convertedFileName = fileString + '.wav'
        output_path = os.path.join('./Converted Files', convertedFileName)
        subprocess.call(['ffmpeg', '-y', '-i', fullMusicPath,
            output_path])
        
        progressBar.hide_bar()
        print('progress bar hidden')
        displayOutputConversion.config(state="normal")
        displayOutputConversion.delete(1.0, END)
        displayOutputConversion.tag_configure("center", justify='center')
        displayOutputConversion.insert(END, "Converted successfully!")
        displayOutputConversion.tag_add("center", "1.0", "end")
        displayOutputConversion.config(state="disabled")

    except Exception as e:
        progressBar.hide_bar()
        displayOutputConversion.config(state="normal")
        displayOutputConversion.delete(1.0, END)
        displayOutputConversion.tag_configure("center", justify='center')
        displayOutputConversion.insert(END, "Conversion failed..." + str(e))
        displayOutputConversion.tag_add("center", "1.0", "end")
        displayOutputConversion.config(state="disabled")

    

        



#instruction for video or audio download
my_label = Label(window, text = "Download the video or just the audio?")
my_label.pack(pady=2)

#buttons
mp4_button = Button(window,text='Video',bg = "#C6C6C6",height=1,width=10, command=toggle_mp4)
mp4_button.pack(side="top",pady="10")

mp3_button = Button(window,text='Audio',bg = "#C6C6C6",height=1,width=10, command=toggle_mp3)
mp3_button.pack(side="top",pady="10")

res_label = Label(window, text = "Choose video resolution (for video only)").pack(side='top')

#assigns radiobutton to be of type integer
radio = IntVar()

Radiobutton(window,text='1080p',variable=radio, value=1).pack(side='top')
Radiobutton(window,text='720p',variable=radio, value=2).pack(side='top')
Radiobutton(window,text='360p',variable=radio, value=3).pack(side='top')

#download video
main_btn = Button(window,text='DOWNLOAD',bg ="#00FF00",height=1,width=10,command=threading).pack(side='top',pady=5)

displayOutput = Text(window, height = 1, width = 47)
displayOutput.config(state="disabled")
displayOutput.pack(side='top',pady=5)

#conversion to wav
wav_label = Label(window, text = "Convert mp3 to wav").pack(side='top')

# Create a File Explorer label
label_file_explorer = Label(window, 
                            text = "Your uploaded file will appear here...",
                            width = 100, height = 2, 
                            fg = "blue")
label_file_explorer.pack(side='top')

button_Open_Explorer = Button(window, 
                        text = "Browse File",
                        command = browseFiles).pack(side='top',pady=5)

#convert mp3 to wav button
main_btn = Button(window,text='CONVERT',bg ="#00FF00",height=1,width=10,command=lambda: convertFile(fullMusicPath)).pack(side='top',pady=5)

displayOutputConversion = Text(window, height = 1, width = 47)
displayOutputConversion.config(state="disabled")
displayOutputConversion.pack(side='top',pady=10)

window.mainloop()
