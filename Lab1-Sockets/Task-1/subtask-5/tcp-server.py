import socket
from datetime import datetime
import time


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
port = 5555

server_socket.bind((host, port))
server_socket.listen(5)
print('The server is waiting for connection......')
while True:
    client_socket, addr = server_socket.accept()
    client_message = client_socket.recv(1024)
    while client_message:
        client_message = client_socket.recv(1024)
    print("*********All data recieved!*****************")
    server_socket.close()
    break
