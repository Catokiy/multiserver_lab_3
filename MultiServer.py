import pickle
import socket
import threading
import os
import json
from json import load

global count_users

def create_programs_info_json(): 
    programs_info = {} 
    paths = os.environ['PATH'].split(os.pathsep) 
    for path in paths:
        programs = []  
        for root, dirs, files in os.walk(path): 
            for file in files:
                programs.append(os.path.join(root, file))
                programs_info[path] = programs
    
    with open('pr_inf.json', 'w', encoding = "UTF-8") as file:
        json.dump(programs_info, file, indent=4, ensure_ascii=False)

def get_active_processes():
    cmd = 'tasklist /FO CSV'
    text = os.popen(cmd).read()
    text = text.encode('cp1251').decode('cp866')
    arr = [[j for j in i.replace('\xa0', ' ').split(",")] for i in text.replace('"', '').split('\n')][:-1]

    dic = {}
    names = ['process_name', 'PID', 'session_name', '№', 'memory']
    for i in arr[1:]:
        dic[i[0]] = {names[1]: i[1], names[2]: i[2], names[3]: i[3], names[4]: i[4]}

    with open('server_folder\\data.json', 'w', encoding='UTF-8') as new_file:
        json.dump(dic, new_file, indent=4, ensure_ascii=False)


# По аналогии в эту функцию вставить запуск своих функций при нужном вводе
# и соответсвенно вставить свою функцию выше ДОЛЖНА РАБОТАТЬ НЕ ТОЛЬКО НА ЯБЛОКЕ
def client_thread(conn):
    print('User #'+str(count_users))
    while True:
        data = conn.recv(1024)
        print(data.decode())
        if data == b'close':
            break
        if data == b'tasklist':
            get_active_processes()
            package = pickle.dumps(json.load(open("server_folder\\data.json", encoding='UTF-8')))
            conn.send(str(len(package)).encode())
            conn.sendall(package)
        if data == b'update':
            create_programs_info_json()
            with open('pr_inf.json', 'r', encoding = 'UTF-8') as file:
                pr_inf = json.load(file)
            with open('server_folder\\pr_inf.pickle', 'wb') as pic_f:
                pickle.dump(pr_inf, pic_f)
            with open('server_folder\\pr_inf.pickle', 'rb') as pic_f:
                pac = pic_f.read()
            conn.send(str(len(pac)).encode())
            conn.sendall(pac)
        else:
            conn.send(data.upper())
            print('data has been received')


server = socket.socket()

server.bind(('', 9090))
server.listen()
count_users = 0

while True:
    client, _ = server.accept()
    count_users += 1
    t = threading.Thread(target=client_thread, args=[client])
    t.start()

server.close()
