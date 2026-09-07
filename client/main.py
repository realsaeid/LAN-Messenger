import sys

from PySide6.QtWidgets import (
    QApplication,
    QInputDialog,
)

from network_client import MessengerClient
from ui.main_window import MainWindow


SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000


def main():

    app = QApplication(sys.argv)

    username, ok = QInputDialog.getText(
        None,
        "Login",
        "Username:"
    )

    if not ok:
        return

    username = username.strip()

    if not username:
        return

    client = MessengerClient(
        SERVER_IP,
        SERVER_PORT,
        username
    )

    try:

        client.connect()

    except Exception as error:

        print(
            f"Could not connect to server: {error}"
        )

        return

    window = MainWindow(
        username,
        client
    )

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()