# Ringbell
A client-server app to that works as a ringbell

# Protocol
The RING protocol is a human-readable utf-8 protocol.
utf-8 null terminated encoded strings are sent between the server and the client.
The commands mean different things according to direction of the message (C->S or viceversa)
## Authentication
After a connection is established with the server three steps are required to authenticate
the client and log it into a username
- The server acknowledge the connection
- The client sends a registered username
- The server acknowledge the username or closes the connection
## Command Syntax
All commands start with the comand name in ALL CAPS then followed by the arguments
### RING
Client > Server
```
RING [dest]
```
Sends a ring to the destination
Server > Client
```
RING [sender]
```
A ring is recieved from the sender
### SETSTATE
Client > Server
```
SETSTATE [state]
```
Sets a state for the user.
A state is a string used to the describe the availability of the user.
### GETSTATE
Client > Server
```
GETSTATE [user]
```
Get the state of a user
### GETONLINE
Client > Server
```
GETONLINE
```
Get a list of all the online users