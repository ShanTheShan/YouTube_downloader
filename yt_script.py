from pytube import YouTube
import tkinter as tk
from tkinter import Entry,Button,Label, Radiobutton, StringVar, IntVar
import subprocess

def download_video(URL:str):
    assert isinstance(URL,str), 'URL was not provided'
    
    youtube_obj = YouTube(URL)
    obj_stream = youtube_obj.streams.get_highest_resolution()
    obj_stream.download()

    
#probe_cmd = ['ffprobe', '-hide_banner', '-pretty', 'Horse kicks tree farts on dogs then runs away.mp4']
#p = subprocess.Popen(probe_cmd)
#p.wait()
#user_link = input("Enter Video Link:")
#user_res = input("Enter Resolution:")
#download_video('https://www.youtube.com/watch?v=KCzwyFHSMdY')

#flag for button
mp4_flag = False
mp3_flag = False
download_flag = False

#main GUI
window = tk.Tk()

#display size
window.geometry('600x360')

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

def download():
    global download_flag,ok

    if download_flag == True:
        print(download_flag)
        ok.forget()
        download_flag = False

        selected_radio = radio.get()
        selected_url = url_input.get()
        selected_video= mp4_button.get()
        selected_audio = mp3_button.get()
        #call pytube func
        try:
            validate = download_video(selected_url)
            download_flag = True
            ok = Label(window, text = "Video downloaded successfully!")
            ok.pack(side='top')
        except Exception as e:
            print(e)
            Label(window, text = "Download failed...check your inputs.").pack(side='top')
    else:
        selected_radio = radio.get()
        selected_url = url_input.get()
        #call pytube func
        try:
            validate = download_video(selected_url)
            download_flag = True
            ok = Label(window, text = "Video downloaded successfully!")
            ok.pack(side='top')
        except Exception as e:
            print(e)
            Label(window, text = "Download failed...check your inputs.").pack(side='top')
    

#instruction for video or audio download
my_label = Label(window, text = "Download the video or just the audio?")
my_label.pack(pady=2)

#buttons
mp4_button = Button(window,text='Video',bg = "#C6C6C6",height=1,width=10, command=toggle_mp4)
mp4_button.pack(side="top",pady="10")

mp3_button = Button(window,text='Audio',bg = "#C6C6C6",height=1,width=10, command=toggle_mp3)
mp3_button.pack(side="top",pady="10")

res_label = Label(window, text = "Choose video resolution").pack(side='top')

#assigns radiobutton to be of type integer
radio = IntVar()

Radiobutton(window,text='1080p',variable=radio, value=1).pack(side='top')
Radiobutton(window,text='720p',variable=radio, value=2).pack(side='top')
Radiobutton(window,text='480p',variable=radio, value=3).pack(side='top')
Radiobutton(window,text='360p',variable=radio, value=4).pack(side='top')

#download video
main_btn = Button(window,text='DOWNLOAD',bg ="#00FF00",height=1,width=10,command=download).pack(side='top',pady=5)
window.mainloop()
