# Il client dovrà avere 2 thread
# uno per la ricezione e uno per l'invio
# perchè non sempre le due cose sono sequenziali
# Ad esempio in un ring si riceve senza inviare
# Esempio stupido ma per ricordare

from socket import *


# serverIp = input("Server ip: ")
serverIp = "78.134.80.218"
serverPort = 1200

clientSocket = socket(AF_INET, SOCK_STREAM)
serverAddress = (serverIp, serverPort)

clientSocket.connect(serverAddress)
print("Conneted to", serverAddress)
print("CLOSE to close the connection")

# Authentication process
msg = clientSocket.recv(1024)
print("-<-:", msg.decode("utf-8"))
username = input("->-: ")
clientSocket.send(username.encode("utf-8"))
msg = clientSocket.recv(1024)
print("-<-:", msg.decode("utf-8"))

while True:
    message = input("->-: ")
    clientSocket.send(message.encode("utf-8"))

    if message == 'CLOSE':
        break

    modifiedMessage = clientSocket.recv(1024)
    print("-<-:", modifiedMessage.decode("utf-8"))

print("Connection closed by client")
clientSocket.close()
