import sys
from Controller import Controller
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Controller.Window()
    win.show()
    sys.exit(app.exec())


