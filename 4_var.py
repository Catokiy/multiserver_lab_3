#Ладыгина А.А. Вариант 4.
#1) Реализовать программу, которая используя модуль os получает информацию о системных
#переменных окружения, находит с их помощью имена программ, которые можно прописать в
#консоли без указания пути к ним(в переменной окружения PATH указаны директории, в
#которых лежат такие программы). Программа создает файл объектно-ориентированного
#формата данных(json/xml), в котором храниться древовидная информация о папках и о
#лежащих в них вышеуказанных программах.


#1 Получение информации о системных переменных окружения

import os #функции для работы с ос
import json
from json import load
import socket
import pickle
import threading

def create_programs_info_json(): #создание словаря 
    programs_info = {} #словарь собственно 
    paths = os.environ['PATH'].split(os.pathsep) #полученные пути из окружения PATH разделяем 
    for path in paths:
        programs = [] #список для путей к программам 
        for root, dirs, files in os.walk(path): # os.walk нужен для рекурсивного сканирования всех файлов
            for file in files:
                programs.append(os.path.join(root, file))
                programs_info[path] = programs
    
    with open('pr_inf.json', 'w', encoding = "UTF-8") as file:
        json.dump(programs_info, file, indent=4, ensure_ascii=False)
        
def start_server(conn):
    print("Creating server")
    while True:
        data = conn.recv(1024)
        print(data.decode())
        if data == b'close':
            break
        if data == b'update':
            create_programs_info_json()
            with open('pr_inf.json', 'r', encoding = 'UTF-8') as file:
                pr_inf = json.load(file)
            with open(r'D:\visual studio\курс по питону\pr_inf.pickle', 'wb') as pic_f:
                pickle.dump(pr_inf, pic_f)
            with open(r'D:\visual studio\курс по питону\pr_inf.pickle', 'rb') as pic_f:
                pac = pic_f.read()
            
            conn.send(str(len(pac)).encode())
            conn.sendall(pac)
        else:
            conn.send(data.upper())
            print('Data has been recived')
            break
                

server = socket.socket()
server.bind(('', 9090))
server.listen()

while True:
    client, _ = server.accept()
    t = threading.Thread(target = start_server, args=[client])
    t.start()
server.close()


