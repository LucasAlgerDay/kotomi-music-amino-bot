import os
#os.system("pip uninstall websocket")
#os.system("pip install websocket-client")
#os.system("pip install BotAmino")
#os.system("pip install pysocks")
#os.system("pip install requests[socks]")
os.system("clear||cls")
from keep_alive import keep_alive
from BotAmino import BotAmino
import io
import json 
from time import sleep
from music import *
import random
import time
import threading
from random import uniform, choice, randint
from functools import wraps
from sys import argv as args
#import json
import sys
keep_alive() #==>Solo activar para hostear
drivers = []
music_chat=[]

def checklive(data):
     return data.chatId in music_chat


client = BotAmino("","")



###NO COMANDOS
@client.command("Kotomi")
def hello(data):
    dreven = random.choice(["¡Tontito! Dejame dormir.. :c", "Sabia que no puedes vivir sin mi.. >w<", "Hola, mi amante todo precioso.. :33", "¿Necesitas ayuda en algo? Utiliza !help 2 y entraras en un mundo magico.. :3"])
    data.subClient.send_message(data.chatId, dreven, replyTo = data.messageId)


@client.command("vc")
def vcc(data):
    
        client.start_vc(data.comId,data.chatId)
        sleep(3)
        client.send(json.dumps({"o":{"ndcId":data.comId,"threadId":data.chatId,"id":"337496"},"t":200}))


@client.command("end_vc")
def vcc(data):
    client.end_vc(data.comId,data.chatId)
    music_chat.remove(data.chatId)



# Play command - starts playing music
@client.command("play")
def play_music(data):
    result = play(data.message, data.chatId)
    data.subClient.send_message(data.chatId, result, replyTo=data.messageId)

# Pause command - pauses the currently playing music
@client.command("pause")
def pause_music(data):
    pause(data.chatId)

# Resume command - resumes the previously paused music
@client.command("resume")
def resume_music(data):
    resume(data.chatId)

# Mute command - mutes the audio output
@client.command("mute")
def mute_audio(data):
    mute(data.chatId)

# Add song command - adds a new song to the playlist
@client.command("add_song")
def add_new_song(data):
    result = add_music(data.message, data.chatId)
    data.subClient.send_message(data.chatId, message=result, replyTo=data.messageId)

# Next command - skips to the next song in the playlist
@client.command("next")
def skip_to_next_song(data):
    result = next_song(data.chatId)
    data.subClient.send_message(data.chatId, message=result, replyTo=data.messageId)

# Previous command - goes back to the previous song in the playlist
@client.command("previous")
def go_to_previous_song(data):
    result = previous_song(data.chatId)
    data.subClient.send_message(data.chatId, message=result, replyTo=data.messageId)

# Stop command - stops the playlist
@client.command("stop")
def stop_playlist(data):
    stop(data.chatId)
    data.subClient.send_message(data.chatId, message="Playlist stopped", replyTo=data.messageId)

# Volume command - changes the volume of the audio output
@client.command("volume")
def change_volume(data):
    volume(data.chatId, data.message)

# Skip command - skips the currently playing song (not working currently)
@client.command("skip")
def skip_current_song(data):
    skip(data.chatId, data.message)

# Unmute command - unmutes the audio output
@client.command("unmute")
def unmute_audio(data):
    unmute(data.chatId)

# Playlist command - displays the list of songs in the current playlist
@client.command("playlist")
def display_playlist(data):
    playlist_list = playlist_name(data.chatId)
    song_names = "\n".join([str(song.name.replace(".mp3", "")) for song in playlist_list])


# Playlist command - displays the list of songs in the current playlist
@client.command("playlist")
def playlist(data):
     d=playlist_name(data.chatId)
     string=""
     for ss in d:
          string = "\n".join([string,str(ss.name.replace(".mp3", ""))])
     data.subClient.send_message(data.chatId,message=string,replyTo=data.messageId)


@client.event("on_voice_chat_end")
def on_chat_(data):
    try:
        commuId = int(data.json["ndcId"])
        subClient = client.get_community(commuId)
    except Exception:
        return

    args = Parameters(data, subClient)
    if args.chatId in music_chat:
         playlist_clear(args.chatId)
         music_chat.remove(args.chatId)

@client.event("on_screen_room_end")
def on_c_invi(data):
    try:
        commuId = int(data.json["ndcId"])
        subClient = client.get_community(commuId)
    except Exception:
        return

    args = Parameters(data, subClient)
    if args.chatId in music_chat:
         playlist_clear(args.chatId)
         music_chat.remove(args.chatId)         



@client.event("on_fetch_channel")
def on_chatvite(data):
    
    t=data.json
    print(t)
    channel=t["channelName"]
    key=t["channelKey"]
    uid=t["channelUid"]
    chatId=t["threadId"]
    create_channel(channel,key,uid,chatId)
    pls.add_playlist(chatId)
    music_chat.append(chatId)
    
    
archivo = io.open("mensajes.txt", "a", encoding="utf-8") # abre o crea el archivo mensajes.txt en modo append

@client.on_message()
def read_message(data):
    print(data.message) # imprime el mensaje recibido
    archivo.write(data.message + "\n") # escribe el mensaje en el archivo con un salto de línea


client.launch(True)
print("pronto!")

###COMANDO_REINICIAR_CADA 2_HORAS

def restart_script():
    # Ruta absoluta del archivo de script
    script_path = 'main.py'

    # Ejecuta el nuevo proceso, reemplazando el proceso actual
    os.execv(sys.executable, [sys.executable, script_path])

while True:
    # Espera 1 minuto antes de reiniciar el script
    time.sleep(5000)
    restart_script()


#####
"""
#socket
def restart():
    while True:
        time.sleep(120)
        count = 0
        for i in threading.enumerate():
            if i.name == "restart_thread":
                count += 1
        if count <= 1:
            print("Restart")
            client.socket.close()
            client.socket.start()
"""
import threading
import time

# Creamos un Lock para asegurarnos de que solo un proceso de reinicio ocurra a la vez
restart_lock = threading.Lock()

def restart():
    with restart_lock:
        print("Restarting...")
        try:
            # Agrega aquí la lógica de cierre del socket
            client.socket.close()

            # Agrega aquí la lógica para iniciar el socket
            client.socket.start()

            print("Restart completed")
        except Exception as e:
            print(f"Error during restart: {e}")

        # Lanzamos un temporizador para ejecutar restart nuevamente después de 120 segundos
        threading.Timer(120, restart).start()

# Simulamos la definición de un objeto client
class Client:
    def __init__(self):
        # Agrega aquí la inicialización del objeto client y el socket
        self.socket = Socket()

    def close_socket(self):
        # Agrega aquí la lógica de cierre del socket
        print("Closing socket")
        self.socket.close()

    def start_socket(self):
        # Agrega aquí la lógica para iniciar el socket
        print("Starting socket")
        self.socket.start()

class Socket:
    def __init__(self):
        self.connection_pool = threading.Semaphore(10)  # Tamaño máximo del pool de conexiones

    def close(self):
        # Agrega aquí la lógica de cierre del socket
        print("Closing the socket")

    def start(self):
        with self.connection_pool:
            # Agrega aquí la lógica para iniciar el socket
            print("Starting the socket")

# Creamos una instancia del objeto client
client = Client()

# Iniciamos el proceso de reinicio
restart()

# El bucle principal puede seguir funcionando sin problemas
while True:
    try:
        print("Main loop is running...")
        time.sleep(60)  # Intervalo de espera entre verificaciones
    except KeyboardInterrupt:
        print("Main loop interrupted")
        client.close_socket()  # Cerramos el socket antes de detener el script
        break

#socket
def restart():
    while True:
        time.sleep(120)
        count = 0
        for i in threading.enumerate():
            if i.name == "restart_thread":
                count += 1
        if count <= 1:
            print("Restart")
            client.socket.close()
            client.socket.start()
