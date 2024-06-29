"""File to connect to tcp-server (tcp-client :) )"""

import socket
import select
import time
import threading

from helper import (
    draw_on_image,
    get_image_data,
    read_file,
    compose_image_from_bytes
)


def receive_data(client_socket):
    while True:
        # Check if there are data to receive
        try:
            received_image_data = get_image_data(client_socket)
            compose_image_from_bytes(received_image_data)
            print("Image received and composed")
        except BlockingIOError:
            time.sleep(5)



def tcp_client(host: str = "127.0.0.1", port: int = 8000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect to the server
        client_socket.connect((host, port))
        client_socket.setblocking(False)
        

        receive_thread = threading.Thread(target=receive_data, args=(client_socket, ))
        receive_thread.daemon = True
        receive_thread.start()

        while True:
            message = input("Enter the message you want to put on the picture: ")

            # Putting a message on an image
            output_image = draw_on_image(message)
            
            # Getting the bytes of this image
            image_data = read_file(output_image)
            client_socket.sendall(image_data)



if __name__ == "__main__":
    tcp_client()