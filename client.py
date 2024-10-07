import socket
import threading

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))
    
def receive_message():
    while True:
        
        command = client.recv(2048).decode(FORMAT)
            
        if command == "VOTE":
            round_one_vote = input("Who would you like to remove: ")
            message = ("VOTE1 "+round_one_vote)
            send(message)
            
        else:
            print(command)
            
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
print("Connected!")

receive_message()