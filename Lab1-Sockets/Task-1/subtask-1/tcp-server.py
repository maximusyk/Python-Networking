import socket
from datetime import datetime
import time


ADDRESS = ('127.0.0.1', 5050)
FORMAT = 'utf-8'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(ADDRESS)
server.listen()
print("\n[STARTING] Server is starting...")
print(f"[LISTENING] Server is listening on {ADDRESS[0]}")

client, addr = server.accept()
message = client.recv(1024).decode(FORMAT)
timeM = datetime.now().strftime('%H:%M:%S')

print(
    f"\nClient message -> {message}\nReceiving time -> {timeM}")

print("\n[CLOSING] Server is closing...")
server.close()
