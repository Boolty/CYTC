import time, os, re, threading
import moviepy.editor as mp
## Script
from ffmpeg import *
#from spotdl.download import DownloadManager
#from spotdl.parsers import parse_query
#from spotdl.search import SpotifyClient
##
from pytube import YouTube
from pytube import Playlist
from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox

window=Tk()
Path    = "YT_Download"
name    = "CYTC"
version = "Version. "
ver     = "1.0.3"
info    = "By Alala"

# Title
window.title(name + " | " + version + ver + " | " + info)
window.resizable(width=False, height=False)
window.geometry("500x300+10+10")

# Download Playlist
chk_state = IntVar()
chk_state.set(0)
chk = Checkbutton(window, text='Downlaod YT-Playlist', onvalue=1, offvalue=0, variable=chk_state, font=("Helvetica", 13))
chk.grid(column=0, row=0)
chk.place(x=100, y=100)
mpr_state = IntVar()
#Remove MP4 hacken
mpr_state.set(1)
mpr = Checkbutton(window, text='Remove MP4', onvalue=1, offvalue=0, variable=mpr_state, font=("Helvetica", 13))
mpr.grid(column=0, row=0)
mpr.place(x=290, y=125)
#Start Converting
mp4_state = IntVar()
mp4_state.set(1)
mp4 = Checkbutton(window, text='Converting to MP3', onvalue=1, offvalue=0, variable=mp4_state, font=("Helvetica", 13))
mp4.grid(column=0, row=0)
mp4.place(x=100, y=125)
#Skipp Infos
inf_state = IntVar()
inf_state.set(0)
inf = Checkbutton(window, text='Skipp infobox', onvalue=1, offvalue=0, variable=inf_state, font=("Helvetica", 13))
inf.grid(column=0, row=0)
inf.place(x=290, y=100)
#Spotify Downloader
spot_state = IntVar()
spot_state.set(0)
spot = Checkbutton(window, text='Spotify', onvalue=1, offvalue=0, variable=spot_state, font=("Helvetica", 13))
spot.grid(column=0, row=0)
spot.place(x=10, y=125)

# Inputfield
txtfld = Entry(window, width=50, bd=6)
txtfld.place(x=160, y=40)
pathf = Entry(window, width=20, bd=6)
pathf.place(x=160, y=70)
pathf.insert(INSERT, Path)

# Button-Download
def download():
    if spot_state.get() == 0:
        if chk_state.get() == 1:          
            playlist()
        elif chk_state.get() == 0:
            yout()
    elif spot_state.get() == 1:
        threading.Thread(target=spotify).start()
    txt.insert(INSERT, "\nStart Converting...")
    txt.insert(INSERT, "\nAlle VIDEO`s in ", pathf.get(), " werden zu mp3 Convertiert.")

# Button-Path
def folder():
    os.startfile(pathf.get())

# Button-reconvert
def reconvert():
    threading.Thread(target=conv).start()
    
#Download Button
btn = Button(window, text="Download", fg='blue', font=("Helvetica", 14), command=download)
btn.place(x=190, y=160)

#Folder button   
btn1 = Button(window, text="Ordner", fg='blue', font=("Helvetica", 8), command=folder)
btn1.place(x=450, y=5)

#Reconvert button   
btn2 = Button(window, text="REConvert", fg='blue', font=("Helvetica", 8), command=reconvert)
btn2.place(x=10, y=5)

# Lable
lbl = Label(window, text="Clean YouTube Converter", fg='black', font=("Helvetica", 16))
lbl.place(x=125, y=0)
lbl1 = Label(window, text="Settings:", fg='black', font=("Helvetica", 14))
lbl1.place(x=10, y=100)
lbl2 = Label(window, text="Youtube Link:", fg='black', font=("Helvetica", 14))
lbl2.place(x=10, y=40)
lbl3 = Label(window, text="Download Pfad:", fg='black', font=("Helvetica", 14))
lbl3.place(x=10, y=70)

# Scroll Info
txt = scrolledtext.ScrolledText(window,width=60,height=6)
txt.grid(column=0,row=0)
txt.place(x=0, y=200)


################################################################
# Single Download Youtube
def yout():
    #ask for the link from user  
    #link = input("Enter YOUTUBE Link:  ")
    yt = YouTube(txtfld.get())
    
    #Showing details
    txt.insert(INSERT, "Title: " + str(yt.title.encode('utf-8')))
    txt.insert(INSERT, "\nNumber of views: " + str(yt.views))
    txt.insert(INSERT, "\nLength of video: " + str(yt.length))
    txt.insert(INSERT, "\nRating of video: " + str(yt.rating))
    txt.see("insert")

    #Starting download
    txt.insert(INSERT, "\nStart Downloading...\n")
    threading.Thread(target=youthred).start()
    txt.insert(INSERT, "\nVIDEO wird in " + pathf.get() + " Gespeichert.\n")
    
    

def youthred():
    #ask for the link from user  
    #link = input("Enter YOUTUBE Link:  ")
    yt = YouTube(txtfld.get())

    #Getting the highest resolution possible   
    ys = yt.streams.get_highest_resolution()

    #Starting download
    ys.download(pathf.get())
    if inf_state.get() == 0: 
        messagebox.showinfo('Completed', 'Download Done...')
    if mp4_state.get() == 1:
        threading.Thread(target=conv).start()         
    

########################################################################################
# Definition playlisz youtube
def playlist():

    #ask for the link from user
    txt.insert(INSERT, "\nPlaylist Convertig Modus...\n") 

    #Showing details
    txt.insert(INSERT, "\nStart Downloading...")

    #Playlist Threding
    threading.Thread(target=plthread).start()
    txt.insert(INSERT, "\nVIDEO wird in " + pathf.get() + " Gespeichert.\n")    
  
    
def plthread():
    playlist = Playlist(txtfld.get())
    count = 0

    for video_url in playlist.video_urls: 
        link = video_url

        yt = YouTube(link)       
        
        count = count + 1
        #Info
        txt.insert(INSERT, "\nVideo Nummer: " + str(count))
        txt.insert(INSERT, "\nTitle: " + str(yt.title.encode('utf-8')))
        txt.insert(INSERT, "\nNumber of views: " + str(yt.views))
        txt.insert(INSERT, "\nLength of video: " + str(yt.length))
        txt.insert(INSERT, "\nRating of video: " + str(yt.rating) + "\n")
        txt.see("insert")

        #Getting the highest resolution possible   
        ys = yt.streams.get_highest_resolution()

        #Starting Download
        ys.download(pathf.get())   
    if inf_state.get() == 0:    
        messagebox.showinfo('Completed', 'Download Done...')
    if mp4_state.get() == 1:
        threading.Thread(target=conv).start() 


# Definition Converting
def conv():
    txt.insert(INSERT, "\nStart Converting...")
    txt.see("insert")
    for file in os.listdir(pathf.get()):        
        if re.search('mp4', file):
            mp4_path = os.path.join(pathf.get(),file)
            mp3_path = os.path.join(pathf.get(),os.path.splitext(file)[0]+'.mp3')
            new_file = mp.AudioFileClip(mp4_path)
            new_file.write_audiofile(str(mp3_path))
            if mpr_state.get() == 1:
                os.remove(mp4_path)    
    txt.insert(INSERT, "\nConverting Beendet...")
    txt.see("insert")
    if inf_state.get() == 0: 
        messagebox.showinfo('Completed', 'Converting Done...')

# Spotify Downlaoder
def spotify():
    try:
        os.mkdir(pathf.get())
    except:
        pass

    os.chdir(pathf.get())

     # Initialize spotify client
    SpotifyClient.init(
        client_id="5f573c9620494bae87890c0f08a60293",
        client_secret="212476d9b0f3472eaa762d90b19b0ba8",
        user_auth=False,
    )
    
    spotdl_opts = {
        "query": [txtfld.get()],     
        "output_format": "wav",
        "download_threads": 6,
        "use_youtube": False,
        "generate_m3u": False,
        "search_threads": 2,
    }
    
    with DownloadManager(spotdl_opts) as downloader:
        # Get songs
        song_list = parse_query(
            spotdl_opts["query"], 
            spotdl_opts["output_format"],
            spotdl_opts["use_youtube"],
            spotdl_opts["generate_m3u"],
            spotdl_opts["search_threads"],          
        )
    
        # Start downloading
        if len(song_list) > 0:
            downloader.download_multiple_songs(song_list)   

    txt.insert(INSERT, "\nStart Download from Spotify see Console...")
    txt.see("insert")

window.mainloop()
