import socket
import os

host = "localhost"
port = 8000
buffer_size = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(1)

while True:
	connection, address = server.accept()
	request = connection.recv(buffer_size)
	if address == "/index.html" or "/":
		file = open(os.path.dirname(os.path.realpath("__file__")) + "/index.html", "rb")
		connection.send(b"HTTP/1.1 200 OK\n\n" + file.read())
		file.close()

	if address == "/about/aboutme.html":
		file = open(os.path.dirname(os.path.realpath("__file__")) + "/about/aboutme.html", "rb")
		connection.send(b"HTTP/1.1 200 OK\n\n" + file.read())
		file.close()

	connection.close()
server.close()

