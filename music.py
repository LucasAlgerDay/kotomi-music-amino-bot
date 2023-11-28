
import requests
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from yt_dlp import YoutubeDL
import requests
from selenium.webdriver.common.action_chains import ActionChains
import urllib.parse, urllib.request, sys
import os

import re
from easy_playlist import Playlists
pls = Playlists()
drivers = []


def search_internet_music(music_name):
    query_string = urllib.parse.urlencode({"search_query": music_name})
    formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)

    search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
    clip2 = "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])
    return clip2



def telecharger(url,name):
    
    #file = f'{name}.mp3'

    # music = None
    if ("=" in url and "/" in url and " " not in url) or ("/" in url and " " not in url):
        if "=" in url and "/" in url:
            # music = url.rsplit("=", 1)[-1]
            pass
        elif "/" in url:
            # music = url.rsplit("/")[-1]
            pass

        
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
                }],
            'extract-audio': True,
            'outtmpl': f"audio/{name}.mp3",
            }

        with YoutubeDL(ydl_opts) as ydl:
            video_length = ydl.extract_info(url, download=False).get('duration')
            print(video_length)

            if int(video_length) < 420:
                ydl.extract_info(url, download=True)
                ydl.cache.remove()
                return "done"
            else:
                return "song length exceeded"

    # return "done"

def tex(text):
    r="".join(text.split())
    return r.lower()

def add(channel,key,uid,chatId):
    options = Options()
    options.add_argument('use-fake-device-for-media-stream')
    options.add_argument('use-fake-ui-for-media-stream')
    options.add_argument('--use-file-for-fake-audio-capture=Silent.wav')
    options.add_argument(f'--new-window={chatId}')
    driver = webdriver.Chrome(options=options)
    sabaruk = 'https://kotomimusic1.renchoncute.repl.co'
    driver.get(sabaruk)
    driver.tab_name = chatId
    driver.find_element(By.ID,'appid').send_keys('2b0567d3ff534f0593528432dac20dc1')
    driver.find_element(By.ID,'token').send_keys(key)
    driver.find_element(By.ID,'channel').send_keys(channel)
    driver.find_element(By.ID,'uid').send_keys(uid)
    driver.find_element(By.ID,'join').click()
    sleep(1)
    driver.find_element(By.ID,'mute-audio').click()
    return driver

def create_channel(channel,key,uid,chatId):
    drivers.append(add(channel,key,uid,chatId))

def switch(chatId):
    for driver in drivers:
        if driver.tab_name == chatId:
            driver.switch_to.window(driver.current_window_handle)
            
            break
    return driver

def play(song_name,chatId,custom:str ="no"):
    driver=switch(chatId)
    print(tex(song_name))
    pl = pls.get_playlist(chatId)
    index=pl.index
    if custom =="no":
        if str(index) !='-1':
            if pl.playlist[index].playing==True:
                return "song is curretly playing"
    path = os.path.join(os.getcwd(), 'audio', f'{tex(song_name)}.mp3')
    if os.path.exists(path):
        driver.find_element(By.ID,'local-file').send_keys(path)
        driver.find_element(By.ID,'stop-audio-mixing').click()
        driver.find_element(By.ID,'local-audio-mixing').click()
        
        pl.add_music(path)
        pl.play()
        return f"playing song ----{song_name}"
    else:
        url=search_internet_music(song_name)
        telecharger(url,tex(song_name))
        path = os.path.join(os.getcwd(), 'audio', f'{tex(song_name)}.mp3')
        if os.path.exists(path):
            driver.find_element(By.ID,'local-file').send_keys(path)
            driver.find_element(By.ID,'stop-audio-mixing').click()
            driver.find_element(By.ID,'local-audio-mixing').click()
            pl = pls.get_playlist(chatId)
            pl.add_music(path)
            pl.play()
            return f"playing song ----{song_name}"
        else:
            return "song not found"
    


def next_song(chatId):
     pl = pls.get_playlist(chatId)
     try:
        print(pl.index)
        name=pl.playlist[int(pl.index)+1].name.replace(".mp3", "")
        r=play(name,chatId,"yes")
        if r!="song not found":
             
             pl.next()
             return f"playing song ----{name}"
     except:
         return "no more songs"
     

def previous_song(chatId):
     pl = pls.get_playlist(chatId)
     try:
        print(pl.index)
        name=pl.playlist[int(pl.index)-1].name.replace(".mp3", "")
        r=play(name,chatId,"yes")
        if r!="song not found":
             pl.previous()
             return f"playing song ----{name}"
     except:
         return "no more songs"
         
          #data.subClient.send_message(data.chatId,message="no more song")

def add_music(song_name,chatId):
    
    path = os.path.join(os.getcwd(), 'audio', f'{tex(song_name)}.mp3')
    pl = pls.get_playlist(chatId)
    if os.path.exists(path):
        pl.add_music(path)
        return f"song added ----{song_name}"
    else:
        url=search_internet_music(song_name)
        r=telecharger(url,tex(song_name))
        path = os.path.join(os.getcwd(), 'audio', f'{tex(song_name)}.mp3')
        if os.path.exists(path):
            pl.add_music(path)
            return f"song added ----{song_name}"
        else:
            return "song not found"


def playlist_name(chatId):
    pl = pls.get_playlist(chatId)
    return pl.playlist



def pause(chatId):
    driver=switch(chatId)
    driver.find_element(By.ID,'pause').click()
    pl = pls.get_playlist(chatId)
    pl.pause()

def resume(chatId):
    driver=switch(chatId)
    pl = pls.get_playlist(chatId)
    driver.find_element(By.ID,'resume').click()
    pl.resume()


def mute(chatId):
    driver=switch(chatId)
    driver.find_element(By.ID,'mute-audio').click()


def unmute(chatId):
    driver=switch(chatId)
    driver.find_element(By.ID,'unmute-audio').click()

def stop(chatId):
    driver=switch(chatId)
    pl = pls.get_playlist(chatId)
    driver.find_element(By.ID,'stop-audio-mixing').click()
    pl.stop()
    driver.find_element(By.ID,'mute-audio').click()

def playlist_clear(chatId):
    pl = pls.get_playlist(chatId)
    pl.stop()
    pl.exit()
    driver=switch(chatId)
    driver.close()
    drivers.remove(driver)

def volume(chatId,volume):
    driver=switch(chatId)
    driver.execute_script(f'setVolume({volume});')

def skip(chatId,sec):
    driver=switch(chatId)
    progress_bar = driver.find_element(By.CSS_SELECTOR,".progress-bar")
    width = progress_bar.size["width"]
    #width = progress_bar.size['width']

    # Calculate the middle point of the progress bar
    middle_point = width / 2

    # Create an action chain to move to the middle point and click
    action = ActionChains(driver)
    action.move_to_element_with_offset(progress_bar, middle_point, 0)
    action.click()
    action.perform()



@pls.event("music_over")
def music_over(data):
    print(f"[{data.playlist.name}] {data.music.name} is over, next song now!")
    pl = pls.get_playlist(data.playlist.name)
    if data.playlist.is_over():
        driver=switch(data.playlist.name)
        driver.find_element(By.ID,'stop-audio-mixing').click()
        #pl.stop()
        driver.find_element(By.ID,'mute-audio').click()
    else:
        try:
            name=pl.playlist[int(pl.index)+1].name.replace(".mp3", "")
            r=play(name,data.playlist.name)
            if r!="song not found":
                data.playlist.next()
        except Exception as e:
            print(e)
            pass