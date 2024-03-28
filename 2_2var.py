import struct
import socket

def send_data(data):
    server_address = ('localhost', 9999)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)

    # Отправляем данные на сервер
    for number in data:
        number_bytes = number.encode('utf-8')
        packet = struct.pack('!I', len(number_bytes)) + number_bytes
        client_socket.sendall(packet)

    # Отправляем пустую строку для завершения передачи данных
    client_socket.sendall(struct.pack('!I', 0))

    client_socket.close()

def receive_files():
    server_address = ('localhost', 9999)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)

    folder_name_len = struct.unpack('!I', client_socket.recv(4))[0]
    folder_name = client_socket.recv(folder_name_len).decode('utf-8')
    num_files = struct.unpack('!I', client_socket.recv(4))[0]

    for i in range(num_files):
        file_name = client_socket.recv(1024).decode('utf-8')
        file_data_len = struct.unpack('!I', client_socket.recv(4))[0]
        file_data = client_socket.recv(file_data_len)
        with open(os.path.join(folder_name, file_name), 'wb') as f:
            f.write(file_data)

    client_socket.close()

def main():
    choice = input("Do you want to send data to Program 1 (Y/N)? ").strip().lower()
    if choice == 'y':
        data = input("Enter numbers separated by spaces: ").split()
        send_data(data)
        print("Data sent successfully.")
    elif choice == 'n':
        receive_files()
        print("Files received successfully.")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
