import socket

ADDRESS = ('127.0.0.1', 5050)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(ADDRESS)

client.send(input(f"Enter message to {ADDRESS[0]} -> ").encode('utf-8'))
client.close()
