import socket
from db import orm

serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_socket.bind(("185.255.133.232", 1983))

while True:
    serv_socket.listen()
    client_sock, client_address = serv_socket.accept()
    if client_sock:
        argument = client_sock.recv(1024).decode()
        if argument == "top":
            client_sock.send(orm.show_top().encode())
        else:
            client_sock.send(orm.show_result(argument).encode())
