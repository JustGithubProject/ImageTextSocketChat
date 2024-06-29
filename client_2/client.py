import socket
import threading
import struct

from helper import (
    draw_on_image,
    read_file,
)

def receive_data(client_socket):
    while True:
        # Receive the length prefix
        length_data = client_socket.recv(4)
        if not length_data:
            break
        # Unpack the length
        length = struct.unpack('!I', length_data)[0]

        # Receive the actual image data
        received_image_data = b""
        while len(received_image_data) < length:
            chunk = client_socket.recv(4096)
            if not chunk:
                break
            received_image_data += chunk
        
        if len(received_image_data) == length:
            # Process the received image data
            compose_image_from_bytes(received_image_data)
            print("Image received and composed")
        else:
            print("Incomplete image data received")

def tcp_client(host: str = "127.0.0.1", port: int = 8000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect to the server
        client_socket.connect((host, port))

        receive_thread = threading.Thread(target=receive_data, args=(client_socket,))
        receive_thread.start()

        while True:
            message = input("Enter the message you want to put on the picture: ")

            # Putting a message on an image
            output_image = draw_on_image(message)
            
            # Getting the bytes of this image
            image_data = read_file(output_image)

            # Pack the length of the data
            length = struct.pack('!I', len(image_data))
            
            # Send length prefix followed by the actual data
            client_socket.sendall(length + image_data)

if __name__ == "__main__":
    tcp_client()
