import socket
import threading


class MessengerClient:

    def __init__(self, server_ip, server_port, username):

        self.server_ip = server_ip
        self.server_port = server_port
        self.username = username

        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.running = False

        self.on_users_updated = None
        self.on_message_received = None

    def connect(self):

        self.socket.connect(
            (self.server_ip, self.server_port)
        )

        self.socket.send(
            self.username.encode("utf-8")
        )

        self.running = True

        receive_thread = threading.Thread(
            target=self.receive_messages,
            daemon=True
        )

        receive_thread.start()

    def receive_messages(self):

        while self.running:

            try:

                data = self.socket.recv(1024)

                if not data:
                    break

                message = data.decode("utf-8")

                self.process_message(message)

            except:

                break

    def process_message(self, message):

        if message.startswith("USERS|"):

            users = message.split("|", 1)[1]

            if users:

                users = users.split(",")

            else:

                users = []

            if self.on_users_updated:

                self.on_users_updated(users)

        else:

            if self.on_message_received:

                self.on_message_received(message)

    def send_message(self, message):

        if not self.running:
            return

        self.socket.send(
            message.encode("utf-8")
        )

    def disconnect(self):

        self.running = False

        try:
            self.socket.shutdown(
                socket.SHUT_RDWR
            )
        except:
            pass

        self.socket.close()