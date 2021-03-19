import tkinter as tk
import time
import beepy
from threading import Thread
from socket import *

###########
# NETWORK #
###########

# Listen to the server
def listener(sock):
    while True:
        inmsg = sock.recv(1024).decode('utf-8')
        cmd = inmsg.split()
        if cmd[0] == "RING":
            ring_thread = Thread(target=ring_handler, args=(cmd[1], ))
            ring_thread.start()
        else: # online list
            online_refresh(cmd)

def getOnline(sock):
    time.sleep(5)
    while True:
        message = "GETONLINE"
        sock.send(message.encode("utf-8"))
        time.sleep(30)


serverIp = "78.134.80.218"
serverPort = 1200

username = "leo"

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
# Launch the GetOnline thread
getOnline_thread = Thread(target=getOnline, args=(clientSocket, ))
getOnline_thread.start()

############
# HANDLERS #
############

def buttonRing_handler(event):
    dest = destUsr.get()
    message = "RING " + dest
    clientSocket.send(message.encode("utf-8"))

def buttonChangeState_handler(event):
    state = stateEntry.get()
    message = "SETSTATE " + state
    clientSocket.send(message.encode("utf-8"))

def ring_handler(sender):
    print("RING from", sender)
    title.configure(bg='yellow')
    beepy.beep(sound='ping')
    time.sleep(3)
    title.configure(bg='white')

# TODO FIX!
def online_refresh(oplist):
    destList.option_clear()
    for l in oplist:
        destList.option_add(l, destUsr)

###########
# TKINTER #
###########

# Window definition
window = tk.Tk()

title = tk.Label(
    text="RINGBELL",
    bg="white",
    padx=65
)
destLabel = tk.Label(
    text="Username:",
    bg="cyan",
    padx=45
)
destEntry = tk.Entry(

)
destUsr = tk.StringVar(window)
destList = tk.OptionMenu(
    window,
    destUsr,
    "-----"
)
destUsr.set("-----")
stateLabel = tk.Label(
    text="State:",
    bg="cyan"
)
stateEntry = tk.Entry(
    
)
buttonRing = tk.Button(
    text="Ring"
)
buttonChangeState = tk.Button(
    text="SetState"
)

# Rendering
title.grid(row=0, columnspan=2)
destLabel.grid(row=1, columnspan=2)
# destEntry.grid(row=2, columnspan=2)
destList.grid(row=2, columnspan=1)
stateLabel.grid(row=3, columnspan=2)
stateEntry.grid(row=4, columnspan=2)
buttonRing.grid(row=5)
buttonChangeState.grid(row=5, column=1)

# Wait button ok to get input
buttonRing.bind("<Button-1>", buttonRing_handler)
buttonChangeState.bind("<Button-1>", buttonChangeState_handler)

window.mainloop()
clientSocket.send("CLOSE".encode("utf-8"))