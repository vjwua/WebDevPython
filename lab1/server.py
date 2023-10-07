import socket
from datetime import datetime

HOST = "127.0.0.1"
PORT = 25050

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen()
conn, addr = sock.accept()
print(f"Connected by {addr}")

data = conn.recv(1024)
conn.sendall(data)
print(f"\t[Message] - {data.decode()}")
print(f"\t[Time] - {datetime.now()}")
