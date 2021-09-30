import socket
import sys
import time

HEADER = 2048  # the max length of the messages (in bytes)
PORT = 5050

SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)  # bound this socket to this address


def send(msg):
    message = msg.encode(FORMAT)
    client.send(message)
    print(client.recv(HEADER).decode(FORMAT))


promptAsk = True
while promptAsk:
    prompt = input("Enter your Select in order to execute a select command or disconnect if you want to terminate the "
                   "process : ")
    if prompt == "Disconnect":
        send(DISCONNECT_MESSAGE)
        sys.exit("Exiting ... Thank you for using miniDB!")
    else:
        # checks would probably happen in the compiler side
        send(prompt)
