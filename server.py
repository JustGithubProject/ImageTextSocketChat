import socket
import threading

from helper import get_image_data

connections = list()

def handle_connection(connection: socket.socket, address: str) -> None:
    """Function to handle user connection in a separate thread"""
    while True:
        try:
            print("Start to handle client")
            image_data = get_image_data(connection)
            if image_data:
                print(f"{address[0]}:{address[1]} -> Bytes of image")
                broadcast(image_data, connection)
            else:
                remove_connection(connection)
                break
        except Exception as ex:
            print(f"Error handling user connection: {ex}")
            remove_connection(connection)
            break

def broadcast(message: bytes, connection: socket.socket) -> None:
    """Function to broadcast message to all users except sender"""
    for client_socket in connections:
        if client_socket != connection:
            try:
                print("Sent received data from client1 to client2")
                client_socket.sendall(message)
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
        socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_server.bind(('127.0.0.1', PORT))
        socket_server.listen(4)
        print('Server running!')
        
        while True:
            client_socket, address = socket_server.accept()
            connections.append(client_socket)
            threading.Thread(target=handle_connection, args=(client_socket, address)).start()
    except Exception as e:
        print(f'An error occurred when instancing socket: {e}')
    finally:
        if connections:
            for conn in connections:
                remove_connection(conn)
        socket_server.close()

if __name__ == "__main__":
    server()
