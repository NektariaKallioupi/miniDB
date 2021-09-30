import socket
import threading

# As Documentation mentions ,we first have to run the command 'python -i smallRelationsInsertFile.py' in order to
# create a database containing the smallRelations tables . The database will be saved with the name smdb. We load
# the database in a separate Python shell by running the following commands:
from database import Database

db = Database("smdb", load=True)

HEADER = 2048  # the max length of the messages (in bytes)
PORT = 5050

SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)  # the server and the port from which we are going to access the server
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# create an INET, STREAMing socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)  # bound this socket to this address


# here we handle the individual connection between the client and the server
def handle_client(conn, addr):
    # its client is handled by its own thread
    print(f"New Connection : {addr} ")

    connected = True
    while connected:
        # wait to receive command from client .Also we will not pass this line of code unless we receive a message
        # from our client.Why ? because conn.recv() its a blocking line of code.
        message = conn.recv(HEADER).decode(FORMAT)
        print(message)
        if message == DISCONNECT_MESSAGE:
            connected = False
        else:
            # here we call the command that supposedly would return a string with our results from database
            # select_command = message
            # conn.send(select_command.encode(FORMAT))
            # For demonstration purposes we would send back to the client a "sql command received" message
            conn.send("command received".encode(FORMAT))

        print(f"{addr} : {message}")

    conn.close()


# this functions handles all new connections and distributes them to where they need to go.In more detail ,this
# allows the server to start listening for connections,handling those connections and passing them to handle clients
def start():
    server.listen()
    print(f"Server is listening on ... {SERVER}")
    while True:
        conn, addr = server.accept()  # its a blocking line of code
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print("Active Connections : ")
        # how many threads are active on this python process --- here that amount of threads will represent the
        # amount of clients --- we -1 because there is always one thread that's running,the start thread
        print(threading.active_count() - 1)


print("Starting Server ...")
start()
