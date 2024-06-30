# """File to connect to tcp-server (tcp-client :) )"""

# import socket
# import select

# from helper import (
#     draw_on_image,
#     get_image_data,
#     read_file,
#     compose_image_from_bytes
# )


# def tcp_client(host: str = "127.0.0.1", port: int = 8000):
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
#         # Connect to the server
#         client_socket.connect((host, port))

#         while True:
#             message = input("Enter the message you want to put on the picture: ")

#             # Putting a message on an image
#             output_image = draw_on_image(message)
            
#             # Getting the bytes of this image
#             image_data = read_file(output_image)
#             client_socket.sendall(image_data)

#             # Check if there are data to receive
#             ready_to_read, _, _ = select.select([client_socket], [], [], 0.1)  # Timeout of 0.1 seconds
#             if client_socket in ready_to_read:
#                 # Receive image_data
#                 image_data = get_image_data(client_socket)
#                 compose_image_from_bytes(image_data)


# if __name__ == "__main__":
#     tcp_client()


import os

path = os.path.abspath(".")
print(os.path.join(path, "received_message.png"))