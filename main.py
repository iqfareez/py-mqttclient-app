from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox, QTextEdit, QLabel
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
        self.connectionStatusLabel = self.findChild(QLabel, 'connectionStatusLabel')

        # reference widgets (Publishing)
        self.topicTextbox = self.findChild(QTextEdit, 'topicTextbox')
        self.messageTextbox = self.findChild(QTextEdit, 'messageTextbox')
        self.sendMessageButton = self.findChild(QPushButton, 'sendMessageButton')

        # mqtt client
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        # self.client.on_message = on_message
        self.client.on_disconnect = self.on_disconnect

        self.mqtt_connected = False

        # set default port textfield to 1883
        self.brokerPortTextbox.setPlainText("1883")

        # connect button
        self.connectButton.clicked.connect(self.handle_connect_click)
        self.sendMessageButton.clicked.connect(self.send_message_button_clicked)

    def handle_connect_click(self):
        print("connect button clicked")
        if not self.mqtt_connected:
            broker_addr = self.brokerAddrTextbox.toPlainText()
            broker_port = int(self.brokerPortTextbox.toPlainText())

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
