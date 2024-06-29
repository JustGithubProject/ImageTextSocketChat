"""File to connect to tcp-server (tcp-client :) )"""

import socket

from helper import draw_on_image


def tcp_client(host: str = "127.0.0.1", port: int = 8000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect to the server
        client_socket.connect((host, port))

        while True:
            message = input("Enter the message you want to put on the picture: ")

            # Putting a message on an image
            output_image = draw_on_image(message)
            
            # Getting the bytes of this image
            image_data = read_file(output_image)
            client_socket.sendall(image_data)


if __name__ == "__main__":
    tcp_client()