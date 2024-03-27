import os
import socket
import json
import pickle


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


sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
flag = True
sock.bind(('', 9090))
sock.listen(1)
conn, addr = sock.accept()
while flag:
    data = conn.recv(1024)
    print(data)
    if data == b'close':
        flag = False
    if data == b'update':

        get_active_processes()
        package = pickle.dumps(json.load(open("server_folder\\data.json", encoding='UTF-8')))
        conn.send(str(len(package)).encode())
        conn.sendall(package)

    else:
        conn.send(data.upper())
        print('data has been received')

conn.close()
