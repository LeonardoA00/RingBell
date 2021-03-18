import tkinter as tk
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
            ring_handler(cmd[1])

serverIp = "78.134.80.218"
serverPort = 1200

username = "leo"

clientSocket = socket(AF_INET, SOCK_STREAM)
serverAddress = (serverIp, serverPort)

clientSocket.connect(serverAddress)

# Authentication
msg = clientSocket.recv(1024)
# print("-<-:", msg.decode("utf-8"))
clientSocket.send(username.encode("utf-8"))
msg = clientSocket.recv(1024)
# print("-<-:", msg.decode("utf-8"))


############
# HANDLERS #
############

def buttonRing_handler(event):
    dest = destEntry.get()
    message = "RING " + dest
    clientSocket.send(message.encode("utf-8"))

def buttonChangeState_handler(event):
    state = stateEntry.get()
    message = "SETSTATE" + state
    clientSocket.send(message.encode("utf-8"))

def ring_handler(sender):
    title.configure(backgroud='yellow')

###########
# TKINTER #
###########

# Window definition
window = tk.Tk()

title = tk.Label(
    text="RINGBELL",
    bg="white"
)
destLabel = tk.Label(
    text="Username:",
    bg="cyan"
)
destEntry = tk.Entry(

)
stateLabel = tk.Label(
    text="Password:",
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
destEntry.grid(row=2, columnspan=2)
stateLabel.grid(row=3, columnspan=2)
stateEntry.grid(row=4, columnspan=2)
buttonRing.grid(row=5)
buttonChangeState.grid(row=5, column=1)

# Wait button ok to get input
buttonRing.bind("<Button-1>", buttonRing_handler)
buttonChangeState.bind("<Button-1>", buttonChangeState_handler)

window.mainloop()
clientSocket.send("CLOSE".encode("utf-8"))