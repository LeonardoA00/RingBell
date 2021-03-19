import tkinter as tk
import time
import beepy
from threading import Thread
from socket import *


##########
# CONFIG #
##########

serverIp = "78.134.80.218"
serverPort = 1200

# login username
username = "leo"
# destination username
destUsr = "ricky"


###########
# NETWORK #
###########

# Listen to the server
def listener(sock):
    while True:
        inmsg = sock.recv(1024).decode('utf-8')
        cmd = inmsg.split()
        print("-<-:", inmsg)
        if cmd[0] == "RING":
            ring_thread = Thread(target=ring_handler, args=(cmd[1], ))
            ring_thread.start()


clientSocket = socket(AF_INET, SOCK_STREAM)
serverAddress = (serverIp, serverPort)

clientSocket.connect(serverAddress)

# Authentication
msg = clientSocket.recv(1024)
print("-<-:", msg.decode("utf-8"))
clientSocket.send(username.encode("utf-8"))
msg = clientSocket.recv(1024)
print("-<-:", msg.decode("utf-8"))


# Launch the listener thread
thread = Thread(target=listener, args=(clientSocket, ))
thread.start()

############
# HANDLERS #
############

def buttonRing_handler(event):
    dest = destUsr
    message = "RING " + dest
    clientSocket.send(message.encode("utf-8"))

def ring_handler(sender):
    print("RING from", sender)
    title.configure(bg='yellow')
    beepy.beep(sound='ping')
    time.sleep(3)
    title.configure(bg='white')

###########
# TKINTER #
###########

window = tk.Tk()

title = tk.Label(
    text="RINGBELL",
    bg="white",
    padx=65
)
buttonRing = tk.Button(
    text="Ring",
    width=22
)

# Rendering
title.grid(row=0, columnspan=2)
buttonRing.grid(row=5, columnspan=2)

buttonRing.bind("<Button-1>", buttonRing_handler)

window.mainloop()
clientSocket.send("CLOSE".encode("utf-8"))