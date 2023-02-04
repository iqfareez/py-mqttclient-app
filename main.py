from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox, QTextEdit, QLabel, QLineEdit, \
    QTableWidgetItem, QTableWidget
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
        self.brokerAddrTextbox: QLineEdit = self.findChild(QLineEdit, 'brokerAddrTextbox')
        self.brokerPortTextbox: QLineEdit = self.findChild(QLineEdit, 'brokerPortTextbox')
        self.connectButton: QPushButton = self.findChild(QPushButton, 'connectButton')
        self.connectionStatusLabel: QLabel = self.findChild(QLabel, 'connectionStatusLabel')

        # reference widgets (Publishing)
        self.publishTopicTextbox: QLineEdit = self.findChild(QLineEdit, 'publishTopicTextbox')
        self.messageTextbox: QTextEdit = self.findChild(QTextEdit, 'messageTextbox')
        self.sendMessageButton: QPushButton = self.findChild(QPushButton, 'sendMessageButton')

        # reference widgets (Subscribing)
        self.subscribeTopicTextbox: QLineEdit = self.findChild(QLineEdit, 'subscribeTopicTextbox')
        self.addSubscriptionButton: QPushButton = self.findChild(QPushButton, 'addSubscriptionButton')
        self.incomingMessageTable: QTableWidget = self.findChild(QTableWidget, 'incomingMessagesTable')

        # mqtt client
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        self.mqtt_connected = False

        # connect button
        self.connectButton.clicked.connect(self.handle_connect_click)
        self.sendMessageButton.clicked.connect(self.send_message_button_clicked)
        self.addSubscriptionButton.clicked.connect(self.add_subscription_button_clicked)

        # initial UI setup
        self.incomingMessageTable.setColumnCount(2)
        self.incomingMessageTable.setHorizontalHeaderLabels(['Topic', 'Message'])

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

    def on_message(self, client, userdata, message):
        print(f"Received message: {message.payload.decode()} on topic: {message.topic}")

        # add topic and message to QTableWidget rows
        row_position = self.incomingMessageTable.rowCount()
        self.incomingMessageTable.insertRow(row_position)

        self.incomingMessageTable.setItem(row_position, 0, QTableWidgetItem(message.topic))
        self.incomingMessageTable.setItem(row_position, 1, QTableWidgetItem(message.payload.decode()))

    def send_message_button_clicked(self, *args):
        """publish a message to a topic"""

        # read topic and message from topic textbox
        topic = self.publishTopicTextbox.text()
        message = self.messageTextbox.toPlainText()
        print(f'Publishing message: {message} to topic: {topic}')
        # publish message
        self.client.publish(topic, message)

    def add_subscription_button_clicked(self, *args):
        """add a subscription to a topic"""

        # read topic from topic textbox
        topic = self.subscribeTopicTextbox.text()
        print(f'Adding subscription to topic: {topic}')
        # subscribe to topic
        self.client.subscribe(topic)


def main():
    app = QApplication(sys.argv)
    print("hello")
    ui_window = MainApp()
    ui_window.show()
    app.exec_()


if __name__ == '__main__':
    main()
