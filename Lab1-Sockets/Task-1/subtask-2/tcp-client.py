import socket


ADDRESS = ('127.0.0.1', 5050)
FORMAT = 'utf-8'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(ADDRESS)

message = input(f"Enter message to {ADDRESS[0]} -> ").encode(FORMAT)
client.send(message)

svrMessage = client.recv(1024).decode(FORMAT)
print('Message from server: ' + svrMessage)

client.close()
