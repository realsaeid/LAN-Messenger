import socket
import threading


HOST = "0.0.0.0"
PORT = 5000

clients = {}
clients_lock = threading.Lock()


def broadcast_user_list():
    with clients_lock:
        usernames = list(clients.keys())

    user_list = ",".join(usernames)

    message = f"USERS|{user_list}"

    with clients_lock:
        for client_socket in clients.values():
            try:
                client_socket.send(message.encode("utf-8"))
            except:
                pass


def handle_client(client_socket, address):
    username = None

    print(f"[NEW CONNECTION] {address} connected.")

    try:
        username = client_socket.recv(1024).decode("utf-8").strip()

        if not username:
            return

        with clients_lock:

            if username in clients:
                client_socket.send(
                    "ERROR|Username already exists".encode("utf-8")
                )
                return

            clients[username] = client_socket

        print(f"[ONLINE] {username} - {address}")

        client_socket.send("CONNECTED".encode("utf-8"))

        broadcast_user_list()

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

        if username:

            with clients_lock:

                if username in clients:
                    del clients[username]

            print(f"[OFFLINE] {username}")

            broadcast_user_list()

        client_socket.close()


def start_server():

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

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
            args=(client_socket, address),
            daemon=True
        )

        thread.start()

        print(
            f"[ACTIVE CONNECTIONS] "
            f"{threading.active_count() - 1}"
        )


if name == "__main__":
    start_server()