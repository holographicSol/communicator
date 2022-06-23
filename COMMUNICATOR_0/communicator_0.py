"""
Written by Benjamin Jack Cullen aka Holographic_Sol
"""

import os
import sys
import time
import datetime
import socket
from win32api import GetSystemMetrics
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Socket Instances
SOCKET_LOOPBACK_SERVER = []
SOCKET_LOOPBACK_SEND = []
SOCKET_LOCAL_SERVER = []
SOCKET_LOCAL_SEND = []
SOCKET_PUBLIC_SERVER = []
SOCKET_PUBLIC_SEND = []

# Addresses (simplify)
CLIENT_ADDRESS = []
LOOPBACK_SERVER_ADDRESS = ''
LOCAL_SERVER_ADDRESS = ''
PUBLIC_SERVER_ADDRESS = ''

# Loopback Settings
loopback_server_thread_key = ''
loopback_send_thread_key = ''
loopback_server_log = './loopback_server_log.txt'

# Local Settings
local_server_thread_key = ''
local_send_thread_key = ''
local_server_log = './local_server_log.txt'

# Public Settings
public_server_thread_key = ''
public_send_thread_key = ''
public_server_log = './public_server_log.txt'

# Configuration Settings
configuration_thread_key = ''
configuration_thread_completed = False

# Object Lists
button_var = []
server_title = []

# Stylesheet - Server Title (Mode 0)
server_title_stylesheet_0 = """QLabel{background-color: rgb(0, 0, 0);
            color: rgb(255, 0, 0);
            border: 1px solid rgb(0, 0, 255);}"""

# Stylesheet - Server Title (Mode 1)
server_title_stylesheet_1 = """QLabel{background-color: rgb(0, 0, 0);
            color: rgb(0, 255, 0);
            border: 1px solid rgb(0, 0, 255);}"""

# Stylesheet - Server Switches (Mode 0)
button_stylesheet_0 = """QPushButton{background-color: rgb(0, 0, 0);
                    color: rgb(200, 200, 200);
                    border: 1px solid rgb(0, 0, 255);}"""

# Stylesheet - Server Switches (Mode 1)
button_stylesheet_1 = """QPushButton{background-color: rgb(255, 0, 0);
                                color: rgb(200, 200, 200);
                                border: 1px solid rgb(0, 0, 255);}"""


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()

        def generate_button_function():
            global button_var
            print('\nplugged in: generateButtonFunction')
            button_gencount = 9
            i = 0
            while i < button_gencount:
                button_name = 'button_' + str(i)
                self.button = button_name
                self.button = QPushButton(self)
                self.button.resize(self.button_wh, self.button_wh)
                self.button.setStyleSheet(button_stylesheet_0)
                button_var.append(self.button)
                self.button.show()
                print('created object:', self.button, '. naming object:', button_name)
                i += 1

        def loopback_start_function():
            global loopback_server_thread_key
            loopback_server_thread.stop()
            loopback_server_thread_key = 'listen'
            loopback_server_thread.start()

        def loopback_stop_function():
            if loopback_server_thread.isRunning() is True:
                loopback_server_thread.stop()
            else:
                print('loopback server: already stopped')

        def loopback_com1_function():
            global loopback_send_thread_key
            if loopback_send_thread.isRunning() is True:
                loopback_send_thread.stop()
            loopback_send_thread_key = 'COM1'
            loopback_send_thread.start()

        def local_start_function():
            global local_server_thread_key
            local_server_thread.stop()
            local_server_thread_key = 'listen'
            local_server_thread.start()

        def local_stop_function():
            if local_server_thread.isRunning() is True:
                local_server_thread.stop()
            else:
                print('local server: already stopped')

        def local_com1_function():
            global local_send_thread_key
            if local_send_thread.isRunning() is True:
                local_send_thread.stop()
            local_send_thread_key = 'COM1'
            local_send_thread.start()

        def public_start_function():
            global public_server_thread_key
            public_server_thread.stop()
            public_server_thread_key = 'listen'
            public_server_thread.start()

        def public_stop_function():
            if public_server_thread.isRunning() is True:
                public_server_thread.stop()
            else:
                print('public server: already stopped')

        def public_com1_function():
            global public_send_thread_key
            if public_send_thread.isRunning() is True:
                public_send_thread.stop()
            public_send_thread_key = 'COM1'
            public_send_thread.start()

        # Window Title
        self.title = "Communicator"
        self.setWindowTitle('Communicator')

        # Window Geometry
        self.width, self.height = 480, 136
        app_pos_w, app_pos_h = (GetSystemMetrics(0) / 2 - (self.width / 2)), (GetSystemMetrics(1) / 2 - (self.height / 2))
        self.left, self.top = int(app_pos_w), int(app_pos_h)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)

        # Window Colour
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

        # Object Geometry
        self.server_title_width = 80
        self.button_wh = 40
        self.button_spacing_w = 4
        self.zone_spacing_h = 8

        global server_title

        # QLabel - loopback_server_title
        self.loopback_server_title = QLabel(self)
        self.loopback_server_title.resize(self.server_title_width, self.button_wh)
        self.loopback_server_title.move(self.button_spacing_w, self.button_spacing_w)
        self.loopback_server_title.setText('LOOPBACK')
        self.loopback_server_title.setAlignment(Qt.AlignCenter)
        self.loopback_server_title.setStyleSheet(server_title_stylesheet_0)
        server_title.append(self.loopback_server_title)

        # QLabel - local_server_title
        self.local_server_title = QLabel(self)
        self.local_server_title.resize(self.server_title_width, self.button_wh)
        self.local_server_title.move(self.button_spacing_w, self.button_spacing_w * 2 + self.button_wh)
        self.local_server_title.setText('LOCAL')
        self.local_server_title.setAlignment(Qt.AlignCenter)
        self.local_server_title.setStyleSheet(server_title_stylesheet_0)
        server_title.append(self.local_server_title)

        # QLabel - public_server_title
        self.public_server_title = QLabel(self)
        self.public_server_title.resize(self.server_title_width, self.button_wh)
        self.public_server_title.move(self.button_spacing_w, self.button_spacing_w * 3 + self.button_wh * 2)
        self.public_server_title.setText('PUBLIC')
        self.public_server_title.setAlignment(Qt.AlignCenter)
        self.public_server_title.setStyleSheet(server_title_stylesheet_0)
        server_title.append(self.public_server_title)

        # QPushButton - Loop Generate
        generate_button_function()

        # QPushButton - LoopBack Server Geometry
        button_var[0].move(self.button_spacing_w * 2 + self.server_title_width, self.button_spacing_w)
        button_var[1].move(self.button_spacing_w * 3 + self.server_title_width + self.button_wh, self.button_spacing_w)
        button_var[2].move(self.button_spacing_w * 4 + self.server_title_width + self.button_wh * 2, self.button_spacing_w)

        # QPushButton - Local Server Geometry
        button_var[3].move(self.button_spacing_w * 2 + self.server_title_width, self.button_spacing_w * 2 + self.button_wh)
        button_var[4].move(self.button_spacing_w * 3 + self.server_title_width + self.button_wh, self.button_spacing_w * 2 + self.button_wh)
        button_var[5].move(self.button_spacing_w * 4 + self.server_title_width + self.button_wh * 2, self.button_spacing_w * 2 + self.button_wh)

        # QPushButton - Public Server Geometry
        button_var[6].move(self.button_spacing_w * 2 + self.server_title_width, self.button_spacing_w * 3 + self.button_wh * 2)
        button_var[7].move(self.button_spacing_w * 3 + self.server_title_width + self.button_wh, self.button_spacing_w * 3 + self.button_wh * 2)
        button_var[8].move(self.button_spacing_w * 4 + self.server_title_width + self.button_wh * 2, self.button_spacing_w * 3 + self.button_wh * 2)

        # QPushButton - LoopBack Server Text
        button_var[0].setText('START')
        button_var[1].setText('STOP')
        button_var[2].setText('COM1')

        # QPushButton - Local Server Text
        button_var[3].setText('START')
        button_var[4].setText('STOP')
        button_var[5].setText('COM1')

        # QPushButton - Public Server Text
        button_var[6].setText('START')
        button_var[7].setText('STOP')
        button_var[8].setText('COM1')

        # QPushButton - LoopBack Server Clicked Connect
        button_var[0].clicked.connect(loopback_start_function)
        button_var[1].clicked.connect(loopback_stop_function)
        button_var[2].clicked.connect(loopback_com1_function)

        # QPushButton - Local Server Clicked Connect
        button_var[3].clicked.connect(local_start_function)
        button_var[4].clicked.connect(local_stop_function)
        button_var[5].clicked.connect(local_com1_function)

        # QPushButton - Public Server Clicked Connect
        button_var[6].clicked.connect(public_start_function)
        button_var[7].clicked.connect(public_stop_function)
        button_var[8].clicked.connect(public_com1_function)

        # Thread - LoopBack Server
        loopback_server_thread = LoopBackServerClass()
        loopback_send_thread = LoopBackSendClass()

        # Thread - Local Server
        local_server_thread = LocalServerClass()
        local_send_thread = LocalSendClass()

        # Thread - Public Server
        public_server_thread = PublicServerClass()
        public_send_thread = PublicSendClass()

        # Thread - Configuration
        configuration_thread = ConfigurationClass()

        # Configuration Thread - Set Configuration Key
        global configuration_thread_key
        configuration_thread_key = 'ALL'

        # Configuration Thread - Run Configuration Thread
        configuration_thread.start()

        # Configuration Thread - Wait For Configuration Thread To Complete
        global configuration_thread_completed
        print('configuration_thread_completed:', configuration_thread_completed)
        while configuration_thread_completed is False:
            time.sleep(1)
        print('configuration_thread_completed:', configuration_thread_completed)

        self.initUI()

    def initUI(self):
        self.show()


class ConfigurationClass(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        print('-' * 200)
        print('[ thread started: ConfigurationClass(QThread).run(self) ]')
        global configuration_thread_key, configuration_thread_completed
        global LOOPBACK_SERVER_ADDRESS
        global LOCAL_SERVER_ADDRESS
        global PUBLIC_SERVER_ADDRESS
        global CLIENT_ADDRESS

        if configuration_thread_key is 'ALL':
            print('-' * 200)
            print('ConfigurationClass(QThread): updating all values from configuration file...')

            LOOPBACK_SERVER_ADDRESS = ''
            LOCAL_SERVER_ADDRESS = ''
            CLIENT_ADDRESS = []

            with open('./config.txt', 'r') as fo:
                for line in fo:
                    line = line.strip()
                    line = line.split(' ')
                    # print(line)

                    if str(line[0]) == 'LOOPBACK_SERVER_ADDRESS':
                        if len(line) is 3:
                            LOOPBACK_SERVER_ADDRESS = str(str(line[1]) + ' ' + str(line[2]))
                            print('LOOPBACK_SERVER_ADDRESS:', LOOPBACK_SERVER_ADDRESS)

                    elif str(line[0]) == 'LOCAL_SERVER_ADDRESS':
                        if len(line) is 3:
                            LOCAL_SERVER_ADDRESS = str(str(line[1]) + ' ' + str(line[2]))
                            print('LOCAL_SERVER_ADDRESS:', LOCAL_SERVER_ADDRESS)

                    elif str(line[0]) == 'PUBLIC_SERVER_ADDRESS':
                        if len(line) is 3:
                            PUBLIC_SERVER_ADDRESS = str(str(line[1]) + ' ' + str(line[2]))
                            print('PUBLIC_SERVER_ADDRESS:', PUBLIC_SERVER_ADDRESS)

                    elif str(line[0]) == 'CLIENT':
                        if len(line) is 4:
                            CLIENT_ADDRESS.append(str(line[1]) + ' ' + str(line[2]) + ' ' + str(line[3]))
                            print('CLIENT_ADDRESS:', str(line[1]) + ' ' + str(line[2]) + ' ' + str(line[3]))

            fo.close()

        configuration_thread_completed = True


class LoopBackSendClass(QThread):
    def __init__(self):
        QThread.__init__(self)

        self.HOST_SEND = "127.0.0.1"
        self.PORT_SEND = 65433

    def run(self):
        print('-' * 200)
        print('[ thread started: LoopBackSendClass(QThread).run(self) ]')
        global loopback_send_thread_key

        if loopback_send_thread_key is 'COM1':
            self.COM1()

    def COM1(self):
        global SOCKET_LOOPBACK_SEND
        print('-' * 200)
        print(f"[LOOPBACK_SERVER] outgoing: COM1 to {self.HOST_SEND} : {self.PORT_SEND}")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SOCKET_LOOPBACK_SEND:
                SOCKET_LOOPBACK_SEND.connect((self.HOST_SEND, self.PORT_SEND))
                data = "COM1"
                SOCKET_LOOPBACK_SEND.send(data.encode())
                SOCKET_LOOPBACK_SEND.settimeout(1)
                try:
                    data = SOCKET_LOOPBACK_SEND.recv(1024)
                except Exception as e:
                    print(e)
            if str(data) == "b'COM1'":
                print(f"[LOOPBACK_SERVER] incoming: COM1 received by {self.HOST_SEND} : {self.PORT_SEND}")
        except Exception as e:
            print(e)

    def stop(self):
        global SOCKET_LOOPBACK_SEND
        print('-' * 200)
        print('[ thread terminating: LoopBackSendClass(QThread).run(self) ]')
        try:
            SOCKET_LOOPBACK_SEND.close()
        except Exception as e:
            print(e)
        self.terminate()


class LoopBackServerClass(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.data = ''

    def run(self):
        print('-' * 200)
        self.data = str(datetime.datetime.now()) + ' [LOOPBACK_SERVER] loopback server started'
        print(self.data)
        self.server_logger()

        global loopback_server_thread_key
        while True:
            if loopback_server_thread_key is 'listen':
                self.listen()

    def server_logger(self):
        if not os.path.exists(loopback_server_log):
            open(loopback_server_log, 'w').close()
        with open(loopback_server_log, 'a') as fo:
            fo.write(self.data + '\n')
        fo.close()

    def listen(self):
        global LOOPBACK_SERVER_ADDRESS
        global SOCKET_LOOPBACK_SERVER
        global button_var, server_title

        server_title[0].setStyleSheet(server_title_stylesheet_1)

        print('[LoopBackServerClass] LOOPBACK_SERVER_ADDRESS:', LOOPBACK_SERVER_ADDRESS)
        self.LOOPBACK_SERVER_HOST = LOOPBACK_SERVER_ADDRESS.split(' ')[0]
        self.LOOPBACK_SERVER_PORT = int(LOOPBACK_SERVER_ADDRESS.split(' ')[1])

        print('-' * 200)
        print('LOOPBACK_SERVER_HOST:', self.LOOPBACK_SERVER_HOST)
        print('LOOPBACK_SERVER_PORT:', self.LOOPBACK_SERVER_PORT)
        print('LOOPBACK_SERVER: attempting to listen')

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SOCKET_LOOPBACK_SERVER:
                SOCKET_LOOPBACK_SERVER.bind((self.LOOPBACK_SERVER_HOST, self.LOOPBACK_SERVER_PORT))
                SOCKET_LOOPBACK_SERVER.listen()
                conn, addr = SOCKET_LOOPBACK_SERVER.accept()
                with conn:
                    print('-' * 200)
                    self.data = str(datetime.datetime.now()) + ' [LOOPBACK_SERVER] incoming connection: ' + str(addr)
                    print(self.data)
                    self.server_logger()
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        self.data = str(datetime.datetime.now()) + ' [LOOPBACK_SERVER] connection received data: ' + str(addr) + ' data: ' + str(data)
                        print(self.data)
                        self.server_logger()
                        conn.sendall(data)
                        if str(data) == "b'COM1'":
                            self.data = str(datetime.datetime.now()) + ' [LOOPBACK_SERVER] data recognized as internal command COM1: ' + str(addr)
                            print(self.data)
                            self.server_logger()
                            button_var[2].setStyleSheet(button_stylesheet_1)
                            time.sleep(1)
                            button_var[2].setStyleSheet(button_stylesheet_0)
        except Exception as e:
            print(e)
            server_title[0].setStyleSheet(server_title_stylesheet_0)

    def stop(self):
        global SOCKET_LOOPBACK_SERVER
        global server_title
        print('-' * 200)
        self.data = str(datetime.datetime.now()) + ' [LOOPBACK_SERVER] loopback server terminating'
        print(self.data)
        self.server_logger()
        try:
            SOCKET_LOOPBACK_SERVER.close()
        except Exception as e:
            print(e)
        server_title[0].setStyleSheet(server_title_stylesheet_0)
        self.terminate()


class LocalSendClass(QThread):
    def __init__(self):
        QThread.__init__(self)

        self.HOST_SEND = "192.168.1.11"
        self.PORT_SEND = 65433

    def run(self):
        print('-' * 200)
        print('[ thread started: LocalSendClass(QThread).run(self) ]')
        global local_send_thread_key

        if local_send_thread_key is 'COM1':
            self.COM1()

    def COM1(self):
        global SOCKET_LOCAL_SEND
        print('-' * 200)
        print(f"[LOCAL_SERVER] outgoing: COM1 to {self.HOST_SEND} : {self.PORT_SEND}")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SOCKET_LOOPBACK_SEND:
                SOCKET_LOOPBACK_SEND.connect((self.HOST_SEND, self.PORT_SEND))
                SOCKET_LOOPBACK_SEND.sendall(b"COM1")
                SOCKET_LOOPBACK_SEND.settimeout(1)
                try:
                    data = SOCKET_LOOPBACK_SEND.recv(1024)
                except Exception as e:
                    print(e)
            if str(data) == "b'COM1'":
                print(f"[LOCAL_SERVER] incoming: COM1 received by {self.HOST_SEND} : {self.PORT_SEND}")
        except Exception as e:
            print(e)

    def stop(self):
        global SOCKET_LOCAL_SEND
        print('-' * 200)
        print('[ thread terminating: LocalSendClass(QThread).run(self) ]')
        try:
            SOCKET_LOCAL_SEND.close()
        except Exception as e:
            print(e)
        self.terminate()


class LocalServerClass(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.data = ''

    def run(self):
        print('-' * 200)
        self.data = str(datetime.datetime.now()) + ' [LOCAL_SERVER] local server started'
        print(self.data)
        self.server_logger()

        global local_server_thread_key
        while True:
            if local_server_thread_key is 'listen':
                self.listen()

    def server_logger(self):
        if not os.path.exists(local_server_log):
            open(local_server_log, 'w').close()
        with open(local_server_log, 'a') as fo:
            fo.write(self.data + '\n')
        fo.close()

    def listen(self):
        global LOCAL_SERVER_ADDRESS
        global SOCKET_LOCAL_SERVER
        global button_var, server_title

        server_title[1].setStyleSheet(server_title_stylesheet_1)

        print('[LocalServerClass] LOCAL_SERVER_ADDRESS:', LOCAL_SERVER_ADDRESS)
        self.LOCAL_SERVER_HOST = LOCAL_SERVER_ADDRESS.split(' ')[0]
        self.LOCAL_SERVER_PORT = int(LOCAL_SERVER_ADDRESS.split(' ')[1])

        print('-' * 200)
        print('LOCAL_SERVER_HOST:', self.LOCAL_SERVER_HOST)
        print('LOCAL_SERVER_PORT:', self.LOCAL_SERVER_PORT)
        print('LOCAL_SERVER: attempting to listen')

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SOCKET_LOCAL_SERVER:
                SOCKET_LOCAL_SERVER.bind((self.LOCAL_SERVER_HOST, self.LOCAL_SERVER_PORT))
                SOCKET_LOCAL_SERVER.listen()
                conn, addr = SOCKET_LOCAL_SERVER.accept()
                with conn:
                    print('-' * 200)
                    self.data = str(datetime.datetime.now()) + ' [LOCAL_SERVER] incoming connection: ' + str(addr)
                    print(self.data)
                    self.server_logger()
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        self.data = str(datetime.datetime.now()) + ' [LOCAL_SERVER] connection received data: ' + str(addr) + ' data: ' + str(data)
                        print(self.data)
                        self.server_logger()
                        conn.sendall(data)
                        if str(data) == "b'COM1'":
                            self.data = str(datetime.datetime.now()) + ' [LOCAL_SERVER] data recognized as internal command COM1: ' + str(addr)
                            print(self.data)
                            self.server_logger()
                            button_var[5].setStyleSheet(button_stylesheet_1)
                            time.sleep(1)
                            button_var[5].setStyleSheet(button_stylesheet_0)
        except Exception as e:
            print(e)
            server_title[1].setStyleSheet(server_title_stylesheet_0)

    def stop(self):
        global SOCKET_LOCAL_SERVER
        global server_title
        print('-' * 200)
        self.data = str(datetime.datetime.now()) + ' [LOCAL_SERVER] local server terminating'
        print(self.data)
        self.server_logger()
        try:
            SOCKET_LOCAL_SERVER.close()
        except Exception as e:
            print(e)
        server_title[1].setStyleSheet(server_title_stylesheet_0)
        self.terminate()


class PublicSendClass(QThread):
    def __init__(self):
        QThread.__init__(self)

        self.HOST_SEND = ""
        self.PORT_SEND = 55555

    def run(self):
        print('-' * 200)
        print('[ thread started: PublicSendClass(QThread).run(self) ]')
        global public_send_thread_key

        if public_send_thread_key is 'COM1':
            self.COM1()

    def COM1(self):
        global SOCKET_PUBLIC_SEND
        print('-' * 200)
        print(f"[LOCAL_SERVER] outgoing: COM1 to {self.HOST_SEND} : {self.PORT_SEND}")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SOCKET_PUBLIC_SEND:
                SOCKET_PUBLIC_SEND.connect((self.HOST_SEND, self.PORT_SEND))
                SOCKET_PUBLIC_SEND.sendall(b"COM1")
                SOCKET_PUBLIC_SEND.settimeout(1)
                try:
                    data = SOCKET_PUBLIC_SEND.recv(1024)
                except Exception as e:
                    print(e)
            if str(data) == "b'COM1'":
                print(f"[PUBLIC_SERVER] incoming: COM1 received by {self.HOST_SEND} : {self.PORT_SEND}")
        except Exception as e:
            print(e)

    def stop(self):
        global SOCKET_PUBLIC_SEND
        print('-' * 200)
        print('[ thread terminating: PublicSendClass(QThread).run(self) ]')
        try:
            SOCKET_PUBLIC_SEND.close()
        except Exception as e:
            print(e)
        self.terminate()


class PublicServerClass(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.data = ''

    def run(self):
        print('-' * 200)
        self.data = str(datetime.datetime.now()) + ' [PUBLIC_SERVER] public server started'
        print(self.data)
        self.server_logger()

        global public_server_thread_key
        while True:
            if public_server_thread_key is 'listen':
                self.listen()

    def server_logger(self):
        if not os.path.exists(public_server_log):
            open(public_server_log, 'w').close()
        with open(public_server_log, 'a') as fo:
            fo.write(self.data + '\n')
        fo.close()

    def listen(self):
        global PUBLIC_SERVER_ADDRESS
        global SOCKET_PUBLIC_SERVER
        global button_var, server_title

        server_title[2].setStyleSheet(server_title_stylesheet_1)

        print('[PublicServerClass] PUBLIC_SERVER_ADDRESS:', PUBLIC_SERVER_ADDRESS)
        self.PUBLIC_SERVER_HOST = PUBLIC_SERVER_ADDRESS.split(' ')[0]
        self.PUBLIC_SERVER_PORT = int(PUBLIC_SERVER_ADDRESS.split(' ')[1])

        print('-' * 200)
        print('PUBLIC_SERVER_HOST:', self.PUBLIC_SERVER_HOST)
        print('PUBLIC_SERVER_PORT:', self.PUBLIC_SERVER_PORT)
        print('PUBLIC_SERVER: attempting to listen')

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SOCKET_PUBLIC_SERVER:
                SOCKET_PUBLIC_SERVER.bind((self.PUBLIC_SERVER_HOST, self.PUBLIC_SERVER_PORT))
                SOCKET_PUBLIC_SERVER.listen()
                conn, addr = SOCKET_PUBLIC_SERVER.accept()
                with conn:
                    print('-' * 200)
                    self.data = str(datetime.datetime.now()) + ' [PUBLIC_SERVER] incoming connection: ' + str(addr)
                    print(self.data)
                    self.server_logger()
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        self.data = str(datetime.datetime.now()) + ' [PUBLIC_SERVER] connection received data: ' + str(addr) + ' data: ' + str(data)
                        print(self.data)
                        self.server_logger()
                        conn.sendall(data)
                        if str(data) == "b'COM1'":
                            self.data = str(datetime.datetime.now()) + ' [PUBLIC_SERVER] data recognized as internal command COM1: ' + str(addr)
                            print(self.data)
                            self.server_logger()
                            button_var[8].setStyleSheet(button_stylesheet_1)
                            time.sleep(1)
                            button_var[8].setStyleSheet(button_stylesheet_0)
        except Exception as e:
            print(e)
            server_title[2].setStyleSheet(server_title_stylesheet_0)

    def stop(self):
        global SOCKET_PUBLIC_SERVER
        global server_title
        print('-' * 200)
        self.data = str(datetime.datetime.now()) + '  [PUBLIC_SERVER] public server terminating'
        print(self.data)
        self.server_logger()
        try:
            SOCKET_PUBLIC_SERVER.close()
        except Exception as e:
            print(e)
        server_title[2].setStyleSheet(server_title_stylesheet_0)
        self.terminate()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
