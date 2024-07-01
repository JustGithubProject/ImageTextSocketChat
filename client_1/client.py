import socket
import threading
import struct
import os
import random

from helper import (
    draw_on_image,
    read_file,
    get_image_data,
    compose_image_from_bytes
)


def handle_messages(connection):
    while True:
        try:
            received_image_data = get_image_data(connection)
            print(received_image_data[:10])
            if received_image_data:
                print("Can you compose for Client_1?")
                base_path = os.path.abspath(".")
                filename = f"received_message_{random.randint(1, 19999999999999999)}.png"
                full_path = os.path.join(base_path, filename)
                compose_image_from_bytes(received_image_data, full_path)
                print("Image received and composed")
            else:
                connection.close()
                break
        except Exception as ex:
            print(f'Error handling message from server: {ex}')
            connection.close()
            break

def client(host: str = "127.0.0.1", port: int = 8000) -> None:
    """TCP-Client"""
    try:
        client_socket = socket.socket()
        client_socket.connect((host, port))
        threading.Thread(target=handle_messages, args=(client_socket,)).start()
        print('Connected to chat!')
        
        while True:
            msg = input()
            if msg == 'quit':
                break
            output_image_name = draw_on_image(msg)
            image_data = read_file(output_image_name)
            data_length = struct.pack("!I", len(image_data))
            client_socket.sendall(data_length + image_data)

        client_socket.close()
    except Exception as e:
        print(f'Error connecting to server socket: {e}')
        client_socket.close()


# client()