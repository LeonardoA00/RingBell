from socket import *
from threading import Thread

debug = True

# Global user list
# Contains instances of the registered users
registeredUsers = []

# USER CLASS
# Defines an user
# ip and username must be unique
class User:
    username = ""
    ip = ""
    state = "busy"
    connectionStatus = False
    connectionSocket = ""

    def __init__(self, username):
        self.username = username
    
    def connnectSocket(self, connectionSocket):
        self.ip = connectionSocket.getsockname()[0]
        self.connectionSocket = connectionSocket
        self.connectionStatus = True

    def setState(self, newState):
        self.state = newState    

    def tag(self):
        return self.username + '@' + self.ip
    
    def print(self):
        printStr = '----\n' + self.username + '\n' + self.ip + '\n' + self.state + '\n' + \
        "Connected: " + str(self.connectionStatus) + '\n' + str(connectionSocket) + '\n----'
        print(printStr)
    
    @staticmethod 
    def reconFromAddr(ipAddr):
        for user in registeredUsers:
            if user.ip == ipAddr:
                return user
        return -1
    
    @staticmethod 
    def reconFromUsr(username):
        for user in registeredUsers:
            if user.username == username:
                return user
        return -1
    
    @staticmethod
    def authenticate(connectionSocket):
        msg = "CONNECTION ACK. PLEASE AUTH WITH USERNAME"
        connectionSocket.send(msg.encode('utf-8'))
        rec = connectionSocket.recv(1024)
        rec = rec.decode('utf-8')
        user = User.reconFromUsr(rec)
        if user == -1:
            msg = "AUTH FAILED"
        else:
            msg = "AUTH AS " + user.username
            user.connnectSocket(connectionSocket)
        connectionSocket.send(msg.encode('utf-8'))
        return user

######################
# COMMANDS FUNCTIONS #
######################

# RING
# Sends a ring to destination
def ring(sender, dest):
    if dest.connectionStatus == False:
        print("Failed to RING: dest offline")
        return -1
    ringMessage = "RING " + sender.username
    dest.connectionSocket.send(ringMessage.encode('utf-8'))




# CONNECTION HANDLER
# Handle a connection with a client
def handler(connecitonSocket):
    user = User.authenticate(connecitonSocket)
    if user == -1:
        print(connecitonSocket.getsockname(), "failed to authenticate")
        connecitonSocket.close()
    else:
        print(connecitonSocket.getsockname(), "authenticated as", user.username)
    while True:
        message = user.connectionSocket.recv(1024)
        message = message.decode("utf-8")
        print(user.tag(), ': ', message)

        handlerExit = commandHandler(message, user)

        if debug:
            for u in registeredUsers:
                u.print()
        
        if handlerExit == "CLOSE":
            break

    user.connecitonSocket.close()
    user.connectionStatus = False
    print("Closed connection with ", user.tag())

# COMMAND HANDLER
# Recognizes the command and execute work
# Or launch a handler for the command
# Returns the name of the command decoded
def commandHandler(message, user):
    cmd = message.split()
    if cmd[0] == "RING":
        dest = User.reconFromUsr(cmd[1])
        ring(user, dest)
    elif cmd[0] == "SETSTATE":
        user.setState(cmd[1])   
    # Returns the code for the command as connHndlr checks for CLOSE     
    return cmd[0]



# SERVER STARTUP
# Setting up and launching server

serverPort = 1200
serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

binding = ("", serverPort)
serverSocket.bind(binding)

# Load users
# TODO implement from a file
registeredUsers.append(User("mac"))
registeredUsers.append(User("surface"))
registeredUsers.append(User("localhost"))

# Launch server
serverSocket.listen()
print("Server is listening...")

while True:
    connectionSocket, clientAddr = serverSocket.accept()

    print("Request from:", clientAddr[0])
    # user = User.reconFromAddr(clientAddr[0])
    # user.connnectSocket(connectionSocket)

    thread = Thread(target=handler, args=(connectionSocket, ))
    print("Opened connection with:", connectionSocket.getsockname(), "using Thread", thread)
    thread.start()

serverSocket.close()

