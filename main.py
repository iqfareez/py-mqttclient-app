from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox, QPlainTextEdit
from PyQt5 import uic
import sys
import os


class MainApp(QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()

        # Load the UI Page
        ui_path = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(ui_path, "mainapp.ui"), self)

        # reference textbox
        self.broker_addr_textbox = self.findChild(QPlainTextEdit, 'brokerAddrTextbox')
        self.broker_port_textbox = self.findChild(QPlainTextEdit, 'brokerPortTextbox')
        self.connectButton = self.findChild(QPushButton, 'connectButton')

        # set default port textfield to 1883
        self.broker_port_textbox.setPlainText("1883")

        # connect button
        self.connectButton.clicked.connect(self.connectButtonClicked)

    def connectButtonClicked(self):
        print("connect button clicked")
        broker_addr = self.broker_addr_textbox.toPlainText()
        broker_port = self.broker_port_textbox.toPlainText()
        print(broker_addr)
        print(broker_port)
        if broker_addr == "" or broker_port == "":
            QMessageBox.about(self, "Error", "Please fill in broker address and port")
        else:
            QMessageBox.about(self, "Success", "Broker address and port are filled in")


def main():
    app = QApplication(sys.argv)
    print("hello")
    ui_window = MainApp()
    ui_window.show()
    app.exec_()


if __name__ == '__main__':
    main()
