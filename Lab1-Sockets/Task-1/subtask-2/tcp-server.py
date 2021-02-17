"""
      1 - Send message to the server and print it with sended time.
      2 - Send message to the server, which repeat this message after 5 sec.
      3 - Send few message to the server; Server can stop
      connections after command.
      4 - Server with few connections.
      5 - Server with nonblocking mode.
"""


import socket
from datetime import datetime
import time
import sys


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

print("\n[WAITING] Server waiting 5 sec to send...")
time.sleep(5)

rcvByteSize = client.send(message.encode(FORMAT))
dataCheck = "[SUCCESS] Sending was successfull" if rcvByteSize == len(
    message) else "[ERROR] Failed to send"

print(dataCheck)

print("\n[CLOSING] Server is closing...")
server.close()
