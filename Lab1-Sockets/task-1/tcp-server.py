import socket
from datetime import datetime


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
port = 5555

server_socket.bind((host, port))
server_socket.listen(5)
print('The server is waiting for connection......')

clientsocket, addr = server_socket.accept()
client_message = clientsocket.recv(1024)
print('\nClient message -> ' + client_message.decode('utf-8') +
      "\nReceive time -> " + str(datetime.now()))

server_socket.close()
