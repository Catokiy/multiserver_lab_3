import os
import json
import xml.etree.ElementTree as ET
import time
import sys
import struct
import socket
from binarytree import build, Node  

def create_folder():
    folder_name = time.strftime("%d-%m-%Y_%H-%M-%S")  
    os.makedirs(folder_name)
    return folder_name

def save_data(data, folder):
    file_format = os.path.join(folder, "{}.{}")
    for i, item in enumerate(data, start=1):
        with open(file_format.format(i, 'json'), 'w') as f:
            json.dump(item, f)
        with open(file_format.format(i, 'xml'), 'w') as f:
            xml_data = ET.Element('data')
            for key, value in item.items():
                sub_element = ET.SubElement(xml_data, str(key))
                sub_element.text = str(value)
            tree = ET.ElementTree(xml_data)
            tree.write(file_format.format(i, 'xml'))

def build_binary_tree(data):
    root = None
    for item in data:
        root = insert(root, item["number"])  # Передаем только число для вставки в дерево
    return root

def insert(root, value):
    if root is None:
        return Node(value)
    if value < root.value:
        root.left = insert(root.left, value)
    else:
        root.right = insert(root.right, value)
    return root

def main():
    data = []
    while True:
        try:
            user_input = input("Enter a number or press Enter to finish: ")
            if not user_input:
                break
            data.append({"number": int(user_input), "position": len(data) + 1})  # Сохраняем число и его позицию в списке
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    folder_name = create_folder()
    save_data(data, folder_name)
    tree = build_binary_tree(data)
    print("Binary Search Tree:")
    print(tree)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9999))
    server_socket.listen(1)
    print("Waiting for connection...")
    client_socket, client_address = server_socket.accept()
    print("Connected to:", client_address)

    num_files = len(data) * 2  
    folder_name_bytes = folder_name.encode('utf-8')
    packet = struct.pack('!I', len(folder_name_bytes)) + folder_name_bytes + struct.pack('!I', num_files)
    client_socket.sendall(packet)
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()
