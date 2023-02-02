from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox, QTextEdit
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
        self.brokerAddrTextbox = self.findChild(QTextEdit, 'brokerAddrTextbox')
        self.brokerPortTextbox = self.findChild(QTextEdit, 'brokerPortTextbox')
        self.connectButton = self.findChild(QPushButton, 'connectButton')

        # reference widgets (Publishing)
        self.topicTextbox = self.findChild(QTextEdit, 'topicTextbox')
        self.messageTextbox = self.findChild(QTextEdit, 'messageTextbox')
        self.sendMessageButton = self.findChild(QPushButton, 'sendMessageButton')

        # mqtt client
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        # self.client.on_message = on_message
        self.client.on_disconnect = self.on_disconnect

        # set default port textfield to 1883
        self.brokerPortTextbox.setPlainText("1883")

        # connect button
        self.connectButton.clicked.connect(self.connect_button_clicked)
        self.sendMessageButton.clicked.connect(self.send_message_button_clicked)

    def connect_button_clicked(self):
        print("connect button clicked")
        broker_addr = self.brokerAddrTextbox.toPlainText()
        broker_port = int(self.brokerPortTextbox.toPlainText())

        if broker_addr == "" or broker_port == "":
            QMessageBox.about(self, "Error", "Please fill in broker address and port")
        else:
            print(f'Connecting now to {broker_addr}:{broker_port}')
            self.client.connect(broker_addr, broker_port, 60)
            self.client.loop_start()
            # QMessageBox.about(self, "Success", "Broker address and port are filled in")

    def on_connect(self, *args):
        print(f"connected to broker. Result code:{args[3]}")
        print("Connected to broker")

    def on_disconnect(self, *args):
        print("Disconnected from broker")
        self.client.loop_stop()

    # publish a message to a topic
    def send_message_button_clicked(self, *args):
        # read topic and message from topic textbox
        topic = self.topicTextbox.toPlainText()
        message = self.messageTextbox.toPlainText()
        print(f'Publishing message: {message} to topic: {topic}')
        self.client.publish(topic, message)




def main():
    app = QApplication(sys.argv)
    print("hello")
    ui_window = MainApp()
    ui_window.show()
    app.exec_()


if __name__ == '__main__':
    main()
