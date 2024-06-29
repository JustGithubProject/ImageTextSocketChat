import socket
import threading
import concurrent.futures
import struct

from helper import get_image_data

# dict to store clients that connected to server
clients = dict()
clients_lock = threading.Lock()

def handle_client(client_socket: socket.socket, client_address: tuple):
    """Processing the client in a separate thread"""
    print(f"Connected by {client_address}")
    with clients_lock:
        clients[client_address] = client_socket

    try:
        while True:
            # Receive message from client
            image_data = get_image_data(client_socket)
            if not image_data:
                break
            print(f"Received from {client_address}: {image_data[:5]} ")
            # Broadcast to clients
            broadcast_message(client_address, image_data)

    except Exception as ex:
        print(f'Error handling client {client_address}: {ex}')
    
    finally:
        with clients_lock:
            if client_address in clients:
                del clients[client_address]
        client_socket.close()
        print(f"Connection closed by {client_address}")

def broadcast_message(sender_address, message):
    """Broadcast messages to clients except sender"""
    with clients_lock:
        for client_address, client_socket in clients.items():
            if client_address != sender_address:
                try:
                    client_socket.sendall(message)
                except Exception as e:
                    print(f'Error broadcasting to {client_address}: {e}')

def tcp_server(host: str = "127.0.0.1", port: int = 8000):
    """start tcp-server"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen()
        print(f'Server is listening on {host}:{port}')

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            while True:
                try:
                    client_socket, client_address = server_socket.accept()
                    executor.submit(handle_client, client_socket, client_address)
                except KeyboardInterrupt:
                    print("Server shutting down...")
                    break
                except Exception as e:
                    print(f'Error accepting clients: {e}')

if __name__ == "__main__":
    tcp_server()
