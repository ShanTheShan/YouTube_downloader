from pytube import YouTube
import subprocess

def download_video(URL:str):
    assert isinstance(URL,str), 'URL was not provided'
    
    youtube_obj = YouTube(URL)
    obj_stream = youtube_obj.streams.get_highest_resolution()
    try:
        print('Starting download...')
        obj_stream.download()
    except:
        print('Download error, try again.')
    
probe_cmd = ['ffprobe', '-hide_banner', '-pretty', 'Horse kicks tree farts on dogs then runs away.mp4']
p = subprocess.Popen(probe_cmd)
p.wait()
#user_link = input("Enter Video Link:")
#user_res = input("Enter Resolution:")
#download_video('https://www.youtube.com/watch?v=KCzwyFHSMdY')

