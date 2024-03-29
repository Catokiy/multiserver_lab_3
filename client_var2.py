import socket
import struct
from binarytree import build, Node
import socket

def send_request(data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 9090)
    client_socket.connect(server_address)

    #try:
    client_socket.send('buildtree'.encode())
    resp = client_socket.recv(1024)
    if resp == b'insert tree':
        client_socket.sendall(data.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        print("Received response from server:", response)

    #finally:
        #client_socket.close()

def main():
    data = input("Enter numbers separated by spaces: ")
    send_request(data)

if __name__ == "__main__":
    main()
