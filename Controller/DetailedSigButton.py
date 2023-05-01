from PyQt5.QtWidgets import QMessageBox


class DetailedSigButton:
    def __init__(self):
        message = QMessageBox()
        message.setIcon(QMessageBox.Information)
        message.setWindowTitle("Informatii semnal")
        message.setDetailedText("Frecventa:\nAmplitudine:\nOffset:\n")
        message.setText("Detalii despre semnal")
        message.setStandardButtons(QMessageBox.Ok)
        message.exec()