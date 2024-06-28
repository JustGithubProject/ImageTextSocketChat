import socket
import threading


clients = dict()


def handle_client(client_socket: socket.socket, client_address: tuple):
    print(f"Connected by {client_address}")
    clients[client_address] = client_socket

    while True:
        try:
            # Receive message from client
            message = client_socket.recv(1024).decode()
            if not message:
                print(f'Client {client_address} disconnected')
                break
            print(f"{client_address}: {message}")

            broadcast_message(client_address, message)

        except Exception as ex:
            print(f'Error handling client {client_address}: {ex}')
            break
    del clients[client_address]
    client_socket.close()
    

def broadcast_message(sender_address, message):
    for client_address, client_socket in clients.items():
        if client_address != sender_address:
            try:
                client_socket.sendall(message.encode())
            except Exception as e:
                print(f'Error broadcasting to {client_address}: {e}')
            


def tcp_server(host: str = "127.0.0.1", port: int = 8000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f'Server is listening on {host}:{port}')

        while True:
            client_socket, client_address = server_socket.accept()

            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, ))
            client_thread.start()


def main():
    tcp_server()



if __name__ == "__main__":
    main()