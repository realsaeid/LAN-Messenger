import sys

from PySide6.QtWidgets import QApplication, QInputDialog

from ui.main_window import MainWindow


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

    window = MainWindow(username)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()