from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QListWidget,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
)


class MainWindow(QMainWindow):

    def __init__(self, username):
        super().__init__()

        self.username = username

        self.setWindowTitle(
            f"LAN Messenger - {username}"
        )

        self.resize(900, 600)

        self.create_ui()

    def create_ui(self):

        central_widget = QWidget()

        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(
            central_widget
        )

        # -------------------------
        # Users
        # -------------------------

        users_layout = QVBoxLayout()

        users_label = QLabel("Users")

        self.users_list = QListWidget()

        users_layout.addWidget(users_label)
        users_layout.addWidget(self.users_list)

        # -------------------------
        # Chat
        # -------------------------

        chat_layout = QVBoxLayout()

        self.chat_area = QTextEdit()

        self.chat_area.setReadOnly(True)

        self.message_input = QLineEdit()

        self.message_input.setPlaceholderText(
            "Type your message..."
        )

        self.send_button = QPushButton("Send")

        input_layout = QHBoxLayout()

        input_layout.addWidget(
            self.message_input
        )

        input_layout.addWidget(
            self.send_button
        )

        chat_layout.addWidget(
            self.chat_area
        )

        chat_layout.addLayout(
            input_layout
        )

        # -------------------------
        # Main layout
        # -------------------------

        main_layout.addLayout(
            users_layout,
            1
        )

        main_layout.addLayout(
            chat_layout,
            3
        )