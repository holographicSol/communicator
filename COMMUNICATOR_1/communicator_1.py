"""
Written by Benjamin Jack Cullen aka Holographic_Sol
"""
import datetime
import os
import sys
import subprocess
import time
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel
from PyQt5.QtCore import Qt, QThread, QTimer
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor
from win32api import GetSystemMetrics
import socket

btnx_var = []
btnx_title = []

SOCKET_LOOPBACK_SERVER = []
SOCKET_LOOPBACK_SEND = []
SOCKET_LOCAL_SERVER = []
SOCKET_LOCAL_SEND = []
SOCKET_PUBLIC_SERVER = []
SOCKET_PUBLIC_SEND = []

CLIENT_ADDRESS = []
LOOPBACK_SERVER_ADDRESS = ''
LOCAL_SERVER_ADDRESS = ''
PUBLIC_SERVER_ADDRESS = ''

loopback_server_thread_key = ''
loopback_send_thread_key = ''
loopback_server_log = './loopback_server_log.txt'

local_server_thread_key = ''
local_send_thread_key = ''
local_server_log = './local_server_log.txt'

public_server_thread_key = ''
public_send_thread_key = ''
public_server_log = './public_server_log.txt'

configuration_thread_key = ''

configuration_thread_completed = False


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()

        self.title = "SERVER_CLIENT_0"

        app_w = 480
        app_h = 136
        scr_w = GetSystemMetrics(0)  # Native Resolution Width.
        scr_h = GetSystemMetrics(1)  # Native Resolution Height.
        app_pos_w = (scr_w / 2 - (app_w / 2))
        app_pos_h = (scr_h / 2 - (app_h / 2))
        self.left = int(app_pos_w)
        self.top = int(app_pos_h)
        self.width = int(app_w)
        self.height = int(app_h)

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
        # self.setWindowOpacity(0.5)
        self.initUI()

    def initUI(self):
        global btnx_title
        self.setWindowTitle('SERVER_CLIENT_0')
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)

        self.server_header_width = 80
        self.btnx_wh = 40
        self.btnx_spacing_w = 4
        self.zone_spacing_h = 8

        self.loopback_zone_header = QLabel(self)
        self.loopback_zone_header.resize(self.server_header_width, self.btnx_wh)
        self.loopback_zone_header.move(self.btnx_spacing_w, self.btnx_spacing_w)
        self.loopback_zone_header.setText('LOOPBACK')
        self.loopback_zone_header.setAlignment(Qt.AlignCenter)
        self.loopback_zone_header.setStyleSheet(
            """QLabel{background-color: rgb(0, 0, 0);
            color: rgb(255, 0, 0);
            border: 1px solid rgb(0, 0, 255);}"""
        )
        btnx_title.append(self.loopback_zone_header)

        self.local_zone_header = QLabel(self)
        self.local_zone_header.resize(self.server_header_width, self.btnx_wh)
        self.local_zone_header.move(self.btnx_spacing_w, self.btnx_spacing_w * 2 + self.btnx_wh)
        self.local_zone_header.setText('LOCAL')
        self.local_zone_header.setAlignment(Qt.AlignCenter)
        self.local_zone_header.setStyleSheet(
            """QLabel{background-color: rgb(0, 0, 0);
            color: rgb(255, 0, 0);
            border: 1px solid rgb(0, 0, 255);}"""
        )
        btnx_title.append(self.local_zone_header)

        self.public_zone_header = QLabel(self)
        self.public_zone_header.resize(self.server_header_width, self.btnx_wh)
        self.public_zone_header.move(self.btnx_spacing_w, self.btnx_spacing_w * 3 + self.btnx_wh * 2)
        self.public_zone_header.setText('PUBLIC')
        self.public_zone_header.setAlignment(Qt.AlignCenter)
        self.public_zone_header.setStyleSheet(
            """QLabel{background-color: rgb(0, 0, 0);
            color: rgb(255, 0, 0);
            border: 1px solid rgb(0, 0, 255);}"""
        )
        btnx_title.append(self.public_zone_header)

        def generateButtonFunction():
            global btnx_var
            print('\nplugged in: generateButtonFunction')
            btnx_gencount = 9
            i = 0
            while i < btnx_gencount:
                btnx_name = 'btnx_' + str(i)
                self.btnx = btnx_name
                self.btnx = QPushButton(self)
                self.btnx.resize(self.btnx_wh, self.btnx_wh)
                self.btnx.setStyleSheet(
                    """QPushButton{background-color: rgb(0, 0, 0);
                    color: rgb(200, 200, 200);
                    border: 1px solid rgb(0, 0, 255);}"""
                )
                btnx_var.append(self.btnx)
                self.btnx.show()
                print('created object:', self.btnx, '. naming object:', btnx_name)
                i += 1

            btnx_var[0].move(self.btnx_spacing_w * 2 + self.server_header_width, self.btnx_spacing_w)
            btnx_var[1].move(self.btnx_spacing_w * 3 + self.server_header_width + self.btnx_wh, self.btnx_spacing_w)
            btnx_var[2].move(self.btnx_spacing_w * 4 + self.server_header_width + self.btnx_wh * 2, self.btnx_spacing_w)

            btnx_var[3].move(self.btnx_spacing_w * 2 + self.server_header_width, self.btnx_spacing_w * 2 + self.btnx_wh)
            btnx_var[4].move(self.btnx_spacing_w * 3 + self.server_header_width + self.btnx_wh, self.btnx_spacing_w * 2 + self.btnx_wh)
            btnx_var[5].move(self.btnx_spacing_w * 4 + self.server_header_width + self.btnx_wh * 2, self.btnx_spacing_w * 2 + self.btnx_wh)

            btnx_var[6].move(self.btnx_spacing_w * 2 + self.server_header_width, self.btnx_spacing_w * 3 + self.btnx_wh * 2)
            btnx_var[7].move(self.btnx_spacing_w * 3 + self.server_header_width + self.btnx_wh, self.btnx_spacing_w * 3 + self.btnx_wh * 2)
            btnx_var[8].move(self.btnx_spacing_w * 4 + self.server_header_width + self.btnx_wh * 2, self.btnx_spacing_w * 3 + self.btnx_wh * 2)

            btnx_var[0].setText('START')
            btnx_var[1].setText('STOP')
            btnx_var[2].setText('COM1')

            btnx_var[3].setText('START')
            btnx_var[4].setText('STOP')
            btnx_var[5].setText('COM1')

            btnx_var[6].setText('START')
            btnx_var[7].setText('STOP')
            btnx_var[8].setText('COM1')

            btnx_var[0].clicked.connect(loopback_start_function)
            btnx_var[1].clicked.connect(loopback_stop_function)
            btnx_var[2].clicked.connect(loopback_com1_function)

            btnx_var[3].clicked.connect(local_start_function)
            btnx_var[4].clicked.connect(local_stop_function)
            btnx_var[5].clicked.connect(local_com1_function)

            btnx_var[6].clicked.connect(public_start_function)
            btnx_var[7].clicked.connect(public_stop_function)
            btnx_var[8].clicked.connect(public_com1_function)

        loopback_server_thread = LoopBackServerClass()
        loopback_send_thread = LoopBackSendClass()

        local_server_thread = LocalServerClass()
        local_send_thread = LocalSendClass()

        public_server_thread = PublicServerClass()
        public_send_thread = PublicSendClass()

        configuration_thread = ConfigurationClass()

        self.HOST_SEND = "127.0.0.1"  # The server's hostname or IP address
        self.PORT_SEND = 65433  # The port used by the server

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

        generateButtonFunction()

        global configuration_thread_key
        configuration_thread_key = 'ALL'
        configuration_thread.start()
        global configuration_thread_completed
        print('configuration_thread_completed:', configuration_thread_completed)
        while configuration_thread_completed is False:
            time.sleep(1)
        print('configuration_thread_completed:', configuration_thread_completed)

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

            fo.close()

            for _ in CLIENT_ADDRESS:
                print('CLIENT:', _)

        configuration_thread_completed = True


class LoopBackSendClass(QThread):
    def __init__(self):
        QThread.__init__(self)

        self.HOST_SEND = "127.0.0.1"
        self.PORT_SEND = 65432

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
                SOCKET_LOOPBACK_SEND.sendall(b"COM1")
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
        global btnx_var, btnx_title

        btnx_title[0].setStyleSheet(
            """QLabel{background-color: rgb(0, 0, 0);
            color: rgb(0, 255, 0);
            border: 1px solid rgb(0, 0, 255);}"""
        )

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
                            btnx_var[2].setStyleSheet(
                                """QPushButton{background-color: rgb(255, 0, 0);
                                color: rgb(200, 200, 200);
                                border: 1px solid rgb(0, 0, 255);}"""
                            )
                            time.sleep(1)
                            btnx_var[2].setStyleSheet(
                                """QPushButton{background-color: rgb(0, 0, 0);
                                color: rgb(200, 200, 200);
                                border: 1px solid rgb(0, 0, 255);}"""
                            )
                        else:
                            print('invalid client request:', str(addr))
                            # user option to add client_key mapped to user_name

        except Exception as e:
            print(e)
            btnx_title[0].setStyleSheet(
                """QLabel{background-color: rgb(0, 0, 0);
                color: rgb(255, 0, 0);
                border: 1px solid rgb(0, 0, 255);}"""
            )

    def stop(self):
        global SOCKET_LOOPBACK_SERVER
        global btnx_title
        print('-' * 200)
        self.data = str(datetime.datetime.now()) + ' [LOOPBACK_SERVER] loopback server terminating'
        print(self.data)
        self.server_logger()
        try:
            SOCKET_LOOPBACK_SERVER.close()
        except Exception as e:
            print(e)
        btnx_title[0].setStyleSheet(
            """QLabel{background-color: rgb(0, 0, 0);
            color: rgb(255, 0, 0);
            border: 1px solid rgb(0, 0, 255);}"""
        )
        self.terminate()


class LocalSendClass(QThread):
    def __init__(self):
        QThread.__init__(self)

        self.HOST_SEND = "192.168.1.11"
        self.PORT_SEND = 65432

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
        global btnx_var, btnx_title

        btnx_title[1].setStyleSheet(
            """QLabel{background-color: rgb(0, 0, 0);
            color: rgb(0, 255, 0);
            border: 1px solid rgb(0, 0, 255);}"""
        )

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
                            btnx_var[5].setStyleSheet(
                                """QPushButton{background-color: rgb(255, 0, 0);
                                color: rgb(200, 200, 200);
                                border: 1px solid rgb(0, 0, 255);}"""
                            )
                            time.sleep(1)
                            btnx_var[5].setStyleSheet(
                                """QPushButton{background-color: rgb(0, 0, 0);
                                color: rgb(200, 200, 200);
                                border: 1px solid rgb(0, 0, 255);}"""
                            )
        except Exception as e:
            print(e)
            btnx_title[1].setStyleSheet(
                """QLabel{background-color: rgb(0, 0, 0);
                color: rgb(255, 0, 0);
                border: 1px solid rgb(0, 0, 255);}"""
            )

    def stop(self):
        global SOCKET_LOCAL_SERVER
        global btnx_title
        print('-' * 200)
        self.data = str(datetime.datetime.now()) + ' [LOCAL_SERVER] local server terminating'
        print(self.data)
        self.server_logger()
        try:
            SOCKET_LOCAL_SERVER.close()
        except Exception as e:
            print(e)
        btnx_title[1].setStyleSheet(
            """QLabel{background-color: rgb(0, 0, 0);
            color: rgb(255, 0, 0);
            border: 1px solid rgb(0, 0, 255);}"""
        )
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
        global btnx_var, btnx_title

        btnx_title[2].setStyleSheet(
            """QLabel{background-color: rgb(0, 0, 0);
            color: rgb(0, 255, 0);
            border: 1px solid rgb(0, 0, 255);}"""
        )

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
                            btnx_var[8].setStyleSheet(
                                """QPushButton{background-color: rgb(255, 0, 0);
                                color: rgb(200, 200, 200);
                                border: 1px solid rgb(0, 0, 255);}"""
                            )
                            time.sleep(1)
                            btnx_var[8].setStyleSheet(
                                """QPushButton{background-color: rgb(0, 0, 0);
                                color: rgb(200, 200, 200);
                                border: 1px solid rgb(0, 0, 255);}"""
                            )
        except Exception as e:
            print(e)
            btnx_title[2].setStyleSheet(
                """QLabel{background-color: rgb(0, 0, 0);
                color: rgb(255, 0, 0);
                border: 1px solid rgb(0, 0, 255);}"""
            )

    def stop(self):
        global SOCKET_PUBLIC_SERVER
        global btnx_title
        print('-' * 200)
        self.data = str(datetime.datetime.now()) + '  [PUBLIC_SERVER] public server terminating'
        print(self.data)
        self.server_logger()
        try:
            SOCKET_PUBLIC_SERVER.close()
        except Exception as e:
            print(e)
        btnx_title[2].setStyleSheet(
            """QLabel{background-color: rgb(0, 0, 0);
            color: rgb(255, 0, 0);
            border: 1px solid rgb(0, 0, 255);}"""
        )
        self.terminate()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
