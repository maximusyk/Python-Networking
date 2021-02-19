import socket


ADDRESS = ('127.0.0.1', 5050)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(ADDRESS)

while True:
    message = input(
        f"Enter message to {ADDRESS[0]}(type \'d\' to disconnect) -> ")
    client.send(message.encode('utf-8'))
    if message == 'd' or message == 'D':
        client.close()
        break
