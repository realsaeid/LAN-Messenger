import socket
import threading


HOST = "0.0.0.0"
PORT = 5000

clients = {}


def handle_client(client_socket, address):
    print(f"[NEW CONNECTION] {address} connected.")

    try:
        username = client_socket.recv(1024).decode("utf-8")

        if not username:
            return

        username = username.strip()

        clients[client_socket] = username

        print(f"[ONLINE] {username} - {address}")

        client_socket.send("CONNECTED".encode("utf-8"))

        while True:
            data = client_socket.recv(1024)

            if not data:
                break

            message = data.decode("utf-8")

            print(f"[MESSAGE] {username}: {message}")

    except ConnectionResetError:
        pass

    except Exception as error:
        print(f"[ERROR] {username}: {error}")

    finally:
        if client_socket in clients:
            del clients[client_socket]

        client_socket.close()

        print(f"[OFFLINE] {address}")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, PORT))

    server.listen()

    print("=" * 50)
    print("LAN Messenger Server")
    print("=" * 50)
    print(f"Server listening on port {PORT}")
    print("Waiting for clients...")

    while True:
        client_socket, address = server.accept()

        thread = threading.Thread(
            target=handle_client,
            args=(client_socket, address)
        )

        thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == "__main__":
    start_server()