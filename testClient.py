# Il client dovrà avere 2 thread
# uno per la ricezione e uno per l'invio
# perchè non sempre le due cose sono sequenziali
# Ad esempio in un ring si riceve senza inviare
# Esempio stupido ma per ricordare

from socket import *
from threading import Thread
import sys

CURSOR_UP_ONE = '\x1b[1A' 
ERASE_LINE = '\x1b[2K' 

#############
# FUNCTIONS #
#############

# Listen to the server
def listener(sock):
    while True:
        inmsg = sock.recv(1024).decode('utf-8')
        sys.stdout.write(CURSOR_UP_ONE) 
        # sys.stdout.write(ERASE_LINE)
        print("-<-:", inmsg)
        print("->-: ", end="")


##########
# SCRIPT #
##########
print("RINGBELL.py")
# serverIp = input("Server ip: ")
serverIp = "78.134.80.218"
serverPort = 1200

clientSocket = socket(AF_INET, SOCK_STREAM)
serverAddress = (serverIp, serverPort)

clientSocket.connect(serverAddress)
print("Connected to", serverAddress)
print("------------\n\n")

# Authentication process
msg = clientSocket.recv(1024)
print("-<-:", msg.decode("utf-8"))
username = input("->-: ")
clientSocket.send(username.encode("utf-8"))
msg = clientSocket.recv(1024)
print("-<-:", msg.decode("utf-8"))

# Launch the listener thread
thread = Thread(target=listener, args=(clientSocket, ))
thread.start()

while True:
    message = input("->-: ")
    clientSocket.send(message.encode("utf-8"))

    if message == 'CLOSE':
        break

print("Connection closed by client")
clientSocket.close()
