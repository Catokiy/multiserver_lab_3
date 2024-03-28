#2) Реализовать программу 2 и модифицировать программу 1 так, чтоб при условии, что
#программа 1 запущена 2 программа устанавливает сетевое взаимодействие с программой 1.
#Пользователь 2 программы может отправить команду 1 программе для обновления
#информации о программах и получения соответствующего файла с данными.


import socket #для работы с сетью
import json
import pickle

def saving():
    
    with open('pr_inf.json', 'w', encoding = "UTF-8") as file:
        json.dump(pickle.loads(data, encoding="utf-8"), file, indent=4, ensure_ascii=False)
        file.close()
        
        #json.dump(programs_info, file, indent=4, ensure_ascii=False)
        #file.close()
        print("File was saved")
 #устанавливает связь с другой программой 
host = 'localhost'
port = 9090
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #создаём канал связи, казываем тип, протокол. 
#! связь будет закрыта автоматически после завершения работы!
s.connect((host, port)) #устанавливаем связь 
flag = True
while True:
    m = input("Please, input your command ")
    if m == 'close':
        s.send(m.encode())
        flag = False
        break
    elif m == 'update':
        s.send(m.encode())
        p_l = int(s.recv(1024))
        byt = 0
        data = b''

        while byt <p_l:
            ch = s.recv(min(p_l-byt, 2048))
            byt = byt + len(ch)
            data += ch
        saving()
        print("Success!!!")
s.close()

 #принимаем данные от удалённого хоста, серез соединение.
   
        #Метод блокирует выполнение программы, пока не будет полученно указанное кол-во байт данных



