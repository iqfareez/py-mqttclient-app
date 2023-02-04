![Python](https://img.shields.io/badge/python-3.9-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Qt](https://img.shields.io/badge/Qt-5-%23217346.svg?style=for-the-badge&logo=Qt&logoColor=white)
![Raspberry Pi](https://img.shields.io/badge/RaspberryPi-Pico-C51A4A?style=for-the-badge&logo=Raspberry-Pi)

# Simple MQTT Client

:construction: This project is still **under development**. :construction:

Simple PyQt5 and Python based **MQTT client application**. It uses the Paho MQTT library for 
communication with MQTT brokers, and can be used for publishing and subscribing to topics, as well as for viewing 
message payloads. I make this just for fun hehe to get myself exposed to QT framework.

## Screenshot

![Screenshot](https://i.imgur.com/zpy1lxh.png)

## Get started

Python 3.9 is needed. Newer Python version can't run the app.

1. Clone the repository
1. Get dependencies
   - Run the following command to install the required packages: `pip install -r requirements.txt`
1. Run the following command to start the application: `python main.py`
1. Use the app:
    - Connect to an MQTT broker by entering the broker URL, port, and other required details in the appropriate fields.
    - Publish messages to a topic or subscribe to a topic to receive messages.
    - You can view the payload of the messages received in the message window.
