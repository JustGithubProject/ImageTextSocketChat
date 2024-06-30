import socket
import threading
import struct

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
            
            if received_image_data:
                compose_image_from_bytes(received_image_data)
                print("Image received and composed")
            else:
                connection.close()
                break
        except Exception as ex:
            print(f'Error handling message from server: {e}')
            connection.close()
            break
        
        

def client() -> None:
    """TCP-Client"""

    SERVER_ADDRESS = '127.0.0.1'
    SERVER_PORT = 8000

    try:
        # Instantiate socket and start connection with server
        client_socket = socket.socket()
        client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
        # Create a thread in order to handle messages sent by server
        threading.Thread(target=handle_messages, args=[client_socket]).start()

        print('Connected to chat!')

        # Read user's input until it quit from chat and close connection
        while True:
            msg = input()

            if msg == 'quit':
                break

            output_image_name = draw_on_image(msg)
            image_data = read_file(output_image_name)
            client_socket.send(image_data)

        # Close connection with the server
        client_socket.close()

    except Exception as e:
        print(f'Error connecting to server socket {e}')
        client_socket.close()


if __name__ == "__main__":
    client()
