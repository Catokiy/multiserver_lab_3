import os
import pickle
import socket
import datetime
import json


def save_json():
    now = datetime.datetime.now()
    date = now.strftime("%d-%m-%Y")
    time = now.strftime("%H-%M-%S")
    path = f"{date}\\{time}.json"
    try:
        os.mkdir(date)
    except FileExistsError:
        pass
    with open(path, 'w', encoding='UTF-8') as file:
        json.dump(pickle.loads(data, encoding="utf-8"), file, indent=4, ensure_ascii=False)
    file.close()
    print("Saved to " + path)


sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(('localhost', 9090))

flag = True
while flag:
    message = input('Введите команду, которую хотите отправить: ')
    if message == 'close':
        sock.send(message.encode())
        flag = False
    elif message == 'tasklist':
        sock.send(message.encode())
        package_len = int(sock.recv(1024))
        bytes_received = 0
        data = b''

        while bytes_received < package_len:
            print("Данных получено" + str(round(bytes_received / package_len, 3)) + "%")
            chunk = sock.recv(min(package_len - bytes_received, 2048))
            bytes_received = bytes_received + len(chunk)
            data += chunk
        save_json()
        print('Success!!!')

sock.close()
