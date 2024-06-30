"""File to create tcp-server and handle clients"""

import socket
import threading

from helper import (
    get_image_data
)


# Global variable to store connections
connections = list()


def handle_connection(connection: socket.socket, address: str) -> None:
    """Function to handle user connection in separate thread"""
    while True:
        try:
            image_data = get_image_data(connection)
            if image_data:
                print(f"{address[0]}:{address[1]} -> Bytes of image")
                broadcast(image_data, connection)
            else:
                remove_connection(connection)
                break

        except Exception as ex:
            print(f"Error to handle user connection: {ex}")
            remove_connection(connection)
            break


def broadcast(message: bytes, connection: socket.socket) -> None:
    """Function to broadcast message to all users except sender"""
    for client_socket in connections:
        if client_socket != connection:
            try:
                client_socket.send(message)
            except Exception as ex:
                print(f"Error broadcasting message: {ex}")
                remove_connection(client_socket)


def remove_connection(connection: socket.socket):
    """Remove socket from monitoring list and close it"""
    if connection in connections:
        connection.close()
        connections.remove(connection)



def server() -> None:
    """TCP-Server"""
    PORT = 8000
    
    try:
        # Create server and specifying that it can only handle 4 connections by time!
        socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_server.bind(('127.0.0.1', PORT))
        socket_server.listen(4)

        print('Server running!')
        
        while True:

            # Accept client connection
            client_socket, address = socket_server.accept()
            # Add client connection to connections list
            connections.append(client_socket)
            # Start a new thread to handle client connection and receive it's messages
            # in order to send to others connections
            threading.Thread(target=handle_connection, args=[client_socket, address]).start()

    except Exception as e:
        print(f'An error has occurred when instancing socket: {e}')
    finally:
        # In case of any problem we clean all connections and close the server connection
        if len(connections) > 0:
            for conn in connections:
                remove_connection(conn)

        socket_server.close()


if __name__ == "__main__":
    server()