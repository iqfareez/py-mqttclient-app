from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox, QTextEdit, QLabel, QLineEdit
from PyQt5 import uic
import paho.mqtt.client as mqtt
import sys
import os


class MainApp(QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()

        # Load the UI Page
        ui_path = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(ui_path, "mainapp.ui"), self)

        # reference widgets (Connectivity)
        self.brokerAddrTextbox : QLineEdit = self.findChild(QLineEdit, 'brokerAddrTextbox')
        self.brokerPortTextbox : QLineEdit = self.findChild(QLineEdit, 'brokerPortTextbox')
        self.connectButton : QPushButton = self.findChild(QPushButton, 'connectButton')
        self.connectionStatusLabel : QLabel = self.findChild(QLabel, 'connectionStatusLabel')

        # reference widgets (Publishing)
        self.topicTextbox : QLineEdit = self.findChild(QLineEdit, 'topicTextbox')
        self.messageTextbox : QTextEdit = self.findChild(QTextEdit, 'messageTextbox')
        self.sendMessageButton : QPushButton = self.findChild(QPushButton, 'sendMessageButton')

        # mqtt client
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        # self.client.on_message = on_message
        self.client.on_disconnect = self.on_disconnect

        self.mqtt_connected = False

        # connect button
        self.connectButton.clicked.connect(self.handle_connect_click)
        self.sendMessageButton.clicked.connect(self.send_message_button_clicked)

    def handle_connect_click(self):
        """connect/disconnect to broker according its current state"""

        if not self.mqtt_connected:
            broker_addr = self.brokerAddrTextbox.text()
            broker_port = int(self.brokerPortTextbox.text())

            if broker_addr == "" or broker_port == "":
                QMessageBox.about(self, "Error", "Please fill in broker address and port")
            else:
                print(f'Connecting now to {broker_addr}:{broker_port}')
                self.client.connect(broker_addr, broker_port, 60)
                self.client.loop_start()

        else:
            self.client.disconnect()

    def on_connect(self, *args):
        print(f"connected to broker. Result code:{args[3]}")
        # show connected status with green color
        self.connectionStatusLabel.setStyleSheet("QLabel { color : green; }")
        self.connectionStatusLabel.setText("Connected")
        # update connect button label
        self.connectButton.setText("Disconnect")
        self.mqtt_connected = True

    def on_disconnect(self, *args):
        print("Disconnected from broker")
        # update status label with red color
        self.connectionStatusLabel.setStyleSheet("QLabel { color : red; }")
        self.connectionStatusLabel.setText("Disconnected")
        # update connect button and function
        self.connectButton.setText("Connect")
        self.mqtt_connected = False
        # stop loop
        self.client.loop_stop()

    def send_message_button_clicked(self, *args):
        """publish a message to a topic"""

        # read topic and message from topic textbox
        topic = self.topicTextbox.text()
        message = self.messageTextbox.toPlainText()
        print(f'Publishing message: {message} to topic: {topic}')
        # publish message
        self.client.publish(topic, message)


def main():
    app = QApplication(sys.argv)
    print("hello")
    ui_window = MainApp()
    ui_window.show()
    app.exec_()


if __name__ == '__main__':
    main()
