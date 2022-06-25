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
from PyQt5.QtMultimedia import *
from Crypto.Cipher import AES
from hashlib import sha256
import base64
from Crypto import Random

# key, initialization vector and padding
default_crypt_key = 'default_communicator_key'
crypt_key = bytes('default_communicator_key', 'utf-8')
crypt_iv = bytes('This is an IV456', 'utf-8')
fingerprint = ''
BS = 16
pad = lambda s: bytes(s + (BS - len(s) % BS) * chr(BS - len(s) % BS), 'utf-8')
unpad = lambda s : s[0:-ord(s[-1:])]

# Socket Instances
SOCKET_DIAL_OUT = []
SOCKET_SERVER = []

# Addresses (simplify)
DIAL_OUT_ADDRESSES = []
SERVER_ADDRESS = ''

# Dial Out Settings
dial_out_thread_key = ''
dial_out_address = ''
dial_out_address_index = 0

# NEW DIAL OUT SETTINGS
address_name = []
address_ip = []
address_port = []
address_key = []
address_fingerprint = []

# Public Settings
server_thread_key = ''
send_thread_key = ''
server_log = './server_log.txt'

# Configuration Settings
configuration_thread_key = ''
configuration_thread_completed = False
write_configuration_engaged = False

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

# Stylesheet - Server Switches (Mode 0)
linedit_stylesheet_0 = """QLineEdit{background-color: rgb(0, 0, 0);
                    color: rgb(0, 255, 0);
                    border: 1px solid rgb(0, 0, 255);}"""

# Stylesheet - Server Switches (Mode 1)
linedit_stylesheet_1 = """QLineEdit{background-color: rgb(0, 0, 0);
                                color: rgb(0, 255, 0);
                                border: 1px solid rgb(0, 255, 0);}"""

# Stylesheet - Dial Out COM1 (Mode 0)
com1_stylesheet_default = """QPushButton{background-color: rgb(0, 0, 0);
                    color: rgb(200, 200, 200);
                    border: 1px solid rgb(0, 0, 255);}"""

# Stylesheet - Dial Out COM1 (Mode 1)
com1_stylesheet_green = """QPushButton{background-color: rgb(0, 255, 0);
                                color: rgb(0, 0, 0);
                                border: 1px solid rgb(0, 0, 255);}"""

# Stylesheet - Dial Out COM1 (Mode 2)
com1_stylesheet_red = """QPushButton{background-color: rgb(255, 0, 0);
                                color: rgb(0, 0, 0);
                                border: 1px solid rgb(0, 0, 255);}"""

# Stylesheet - Dial Out Name (Mode 0)
dial_out_name_stylesheet_0 = """QPushButton{background-color: rgb(0, 0, 0);
                                color: rgb(255, 0, 0);
                                border: 1px solid rgb(0, 0, 255);}"""

global_self = []


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        global global_self
        global_self = self

        def dial_out_prev_addr_function():
            print('plugged in: dial_out_prev_addr_function')
            global_self.setFocus()
            global dial_out_address, dial_out_address_index

            # Get length of address book
            LEN_DIAL_OUT_ADDRESSES = len(DIAL_OUT_ADDRESSES)

            # Step through address book
            if dial_out_address_index == 0:
                dial_out_address_index = LEN_DIAL_OUT_ADDRESSES - 1
            else:
                dial_out_address_index = dial_out_address_index - 1

            print('setting dial_out_address_index:', dial_out_address_index)
            print('setting dial_out_address using dial_out_address_index:', DIAL_OUT_ADDRESSES[dial_out_address_index])

            dial_out_address = address_ip[dial_out_address_index] + ' ' + str(address_port[dial_out_address_index])
            self.dial_out_ip_port.setText(dial_out_address)
            self.dial_out_name.setText(address_name[dial_out_address_index])

        def dial_out_next_addr_function():
            print('plugged in: dial_out_next_addr_function')
            global_self.setFocus()
            global dial_out_address, dial_out_address_index

            # Get length of address book
            LEN_DIAL_OUT_ADDRESSES = len(DIAL_OUT_ADDRESSES)

            # Step through address book
            if dial_out_address_index == LEN_DIAL_OUT_ADDRESSES - 1:
                dial_out_address_index = 0
            else:
                dial_out_address_index += 1

            print('setting dial_out_address_index:', dial_out_address_index)
            print('setting dial_out_address using dial_out_address_index:', DIAL_OUT_ADDRESSES[dial_out_address_index])

            dial_out_address = address_ip[dial_out_address_index] + ' ' + str(address_port[dial_out_address_index])
            print('dial_out_address:', dial_out_address)
            self.dial_out_ip_port.setText(dial_out_address)
            print('set dial_out_ip_port text:', dial_out_address)
            self.dial_out_name.setText(address_name[dial_out_address_index])
            print('set dial_out_name text:', address_name[dial_out_address_index])

        def dial_out_ip_port_function_set():
            global_self.setFocus()
            global dial_out_address
            dial_out_address = self.dial_out_ip_port.text()
            print('setting dial out address:', dial_out_address)
            self.dial_out_name.setText('')

        def dial_out_com1_function():
            global_self.setFocus()
            global dial_out_thread_key
            if dial_out_thread.isRunning() is True:
                dial_out_thread.stop()
            dial_out_thread_key = 'COM1'
            dial_out_thread.start()

        def start_function():
            global_self.setFocus()
            global server_thread_key
            server_thread.stop()
            server_thread_key = 'listen'
            server_thread.start()

        def stop_function():
            global_self.setFocus()
            if server_thread.isRunning() is True:
                server_thread.stop()
            else:
                print('public server: already stopped')

        def server_ip_port_write_function():
            global_self.setFocus()
            global write_configuration_engaged
            if write_configuration_engaged is False:
                self.write_var = 'SERVER_ADDRESS ' + self.server_ip_port.text().replace(':', ' ')
                print('setting write variable:', self.write_var)
                write_configuration()
            else:
                print('write_configuration_engaged:', write_configuration_engaged)

        def write_configuration():
            global_self.setFocus()
            global write_configuration_engaged
            write_configuration_engaged = True
            print('-' * 200)
            print('writing line to configuration file:', self.write_var)
            configuration_item = []
            with open('./config.txt', 'r') as fo:
                for line in fo:
                    line = line.strip()
                    if line.startswith(self.write_var.split()[0]):
                        print('changing line in configuration file:', line)
                        configuration_item.append(self.write_var)
                    else:
                        configuration_item.append(line)
            fo.close()
            print('-' * 200)
            print('new configuration file:')
            with open('./config.txt', 'w') as fo:
                for _ in configuration_item:
                    print(_)
                    fo.write(_ + '\n')
            fo.close()
            write_configuration_engaged = False

        # Variable should be set before running write_configuration function
        self.write_var = ''

        # Window Title
        self.title = "Communicator"
        self.setWindowTitle('Communicator')
        self.setWindowIcon(QIcon('./icon.ico'))

        # Window Geometry
        self.width, self.height = 364, 102
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
        self.ip_port_width = 140
        self.ip_port_height = 40
        self.button_wh = 40
        self.button_spacing_w = 4
        self.zone_spacing_h = 8

        # QLabel - Server Title
        self.server_title = QLabel(self)
        self.server_title.resize(self.server_title_width, self.button_wh)
        self.server_title.move(self.button_spacing_w, self.zone_spacing_h)
        self.server_title.setText('SERVER')
        self.server_title.setAlignment(Qt.AlignCenter)
        self.server_title.setStyleSheet(server_title_stylesheet_0)

        # QPushButton - Server Start
        self.server_start = QPushButton(self)
        self.server_start.resize(self.button_wh, self.button_wh)
        self.server_start.move(self.button_spacing_w * 2 + self.server_title_width, self.zone_spacing_h)
        self.server_start.setText('START')
        self.server_start.setStyleSheet(button_stylesheet_0)
        self.server_start.clicked.connect(start_function)

        # QPushButton - Server Stop
        self.server_stop = QPushButton(self)
        self.server_stop.resize(self.button_wh, self.button_wh)
        self.server_stop.move(self.button_spacing_w * 3 + self.server_title_width + self.button_wh, self.zone_spacing_h)
        self.server_stop.setText('STOP')
        self.server_stop.setStyleSheet(button_stylesheet_0)
        self.server_stop.clicked.connect(stop_function)

        # QLineEdit - Public Server IP
        self.server_ip_port = QLineEdit(self)
        self.server_ip_port.resize(self.ip_port_width, self.button_wh)
        self.server_ip_port.move(self.button_spacing_w * 4 + self.server_title_width + self.button_wh * 2, self.zone_spacing_h)
        self.server_ip_port.returnPressed.connect(server_ip_port_write_function)
        self.server_ip_port.setText('')
        self.server_ip_port.setStyleSheet(linedit_stylesheet_0)
        self.server_ip_port.setAlignment(Qt.AlignCenter)

        # QPushButton - Server Received Communication COM1
        self.server_com1 = QPushButton(self)
        self.server_com1.resize(self.button_wh, self.button_wh)
        self.server_com1.move(self.button_spacing_w * 5 + self.server_title_width + self.button_wh * 2 + self.ip_port_width, self.zone_spacing_h)
        self.server_com1.setText('COM1')
        self.server_com1.setStyleSheet(com1_stylesheet_default)

        # QLabel - Dial Out Title
        self.dial_out_title = QLabel(self)
        self.dial_out_title.resize(self.server_title_width, self.button_wh)
        self.dial_out_title.move(self.button_spacing_w, self.zone_spacing_h * 2 + self.button_wh)
        self.dial_out_title.setText('DIAL OUT')
        self.dial_out_title.setAlignment(Qt.AlignCenter)
        self.dial_out_title.setStyleSheet(server_title_stylesheet_0)

        # QLineEdit - Dial Out Address
        self.dial_out_ip_port = QLineEdit(self)
        self.dial_out_ip_port.resize(self.ip_port_width, self.button_wh)
        self.dial_out_ip_port.move(self.button_spacing_w * 2 + self.server_title_width + 88, self.zone_spacing_h * 2 + self.button_wh)
        self.dial_out_ip_port.returnPressed.connect(dial_out_ip_port_function_set)
        self.dial_out_ip_port.setText('')
        self.dial_out_ip_port.setStyleSheet(linedit_stylesheet_0)
        self.dial_out_ip_port.setAlignment(Qt.AlignCenter)

        # QPushButton - Dial Out Send COM1 message
        self.dial_out_com1 = QPushButton(self)
        self.dial_out_com1.resize(self.button_wh, self.button_wh)
        self.dial_out_com1.move(self.button_spacing_w * 3 + self.server_title_width + 88 + self.ip_port_width, self.zone_spacing_h * 2 + self.button_wh)
        self.dial_out_com1.setText('COM1')
        self.dial_out_com1.setStyleSheet(com1_stylesheet_default)
        self.dial_out_com1.clicked.connect(dial_out_com1_function)

        # QPushButton - Dial Out Previous Address
        self.dial_out_prev_addr = QPushButton(self)
        self.dial_out_prev_addr.resize(self.button_wh, self.button_wh / 2 - 4)
        self.dial_out_prev_addr.move(self.button_spacing_w * 2 + self.server_title_width, self.zone_spacing_h * 2 + self.button_wh + 24)
        self.dial_out_prev_addr.setText('-')
        self.dial_out_prev_addr.setStyleSheet(com1_stylesheet_default)
        self.dial_out_prev_addr.clicked.connect(dial_out_prev_addr_function)

        # QPushButton - Dial Out Next Address
        self.dial_out_next_addr = QPushButton(self)
        self.dial_out_next_addr.resize(self.button_wh, self.button_wh / 2 - 4)
        self.dial_out_next_addr.move(self.button_spacing_w * 3 + self.server_title_width + self.button_wh, self.zone_spacing_h * 2 + self.button_wh + 24)
        self.dial_out_next_addr.setText('+')
        self.dial_out_next_addr.setStyleSheet(com1_stylesheet_default)
        self.dial_out_next_addr.clicked.connect(dial_out_next_addr_function)

        # QPushButton - Dial Out Next Address
        self.dial_out_name = QPushButton(self)
        self.dial_out_name.resize(self.button_wh * 2 + 4, self.button_wh / 2)
        self.dial_out_name.move(self.button_spacing_w * 2 + self.server_title_width, self.zone_spacing_h * 2 + self.button_wh)
        self.dial_out_name.setText('')
        self.dial_out_name.setStyleSheet(dial_out_name_stylesheet_0)
        # self.dial_out_name.clicked.connect(dial_out_next_addr_function)

        # Thread - Public Server
        server_thread = PublicServerClass(self.server_title, self.server_com1)

        # Thread - Dial_Out
        dial_out_thread = DialOutClass(self.dial_out_title, self.dial_out_com1)

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

        self.server_ip_port.setText(SERVER_ADDRESS)

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
        global SERVER_ADDRESS
        global DIAL_OUT_ADDRESSES

        global address_name
        global address_ip
        global address_port
        global address_key
        global address_fingerprint

        if configuration_thread_key == 'ALL':
            print('-' * 200)
            print('ConfigurationClass(QThread): updating all values from configuration file...')

            SERVER_ADDRESS = ''

            with open('./config.txt', 'r') as fo:
                for line in fo:
                    line = line.strip()
                    line = line.split(' ')

                    if str(line[0]) == 'SERVER_ADDRESS':
                        if len(line) == 3:
                            SERVER_ADDRESS = str(str(line[1]) + ' ' + str(line[2]))
                            print('SERVER_ADDRESS:', SERVER_ADDRESS)
            fo.close()
            print('-' * 200)
            print('ConfigurationClass(QThread): updating all values from communicator address book...')

            DIAL_OUT_ADDRESSES = []

            with open('./communicator_address_book.txt', 'r') as fo:
                for line in fo:
                    line = line.strip()

                    if line.startswith('DATA'):
                        DIAL_OUT_ADDRESSES.append(line)

            for _ in DIAL_OUT_ADDRESSES:

                # Split address
                dial_out_address_split = _.split(' ')
                print('dial_out_address_split:', dial_out_address_split)

                if len(dial_out_address_split) == 6:

                    # Name
                    print('setting dial out name:', dial_out_address_split[1])
                    address_name.append(dial_out_address_split[1])

                    # IP
                    print('setting dial out ip:', dial_out_address_split[2])
                    address_ip.append(dial_out_address_split[2])

                    # Port
                    print('setting dial out port:', dial_out_address_split[3])
                    address_port.append(int(dial_out_address_split[3]))

                    # Key
                    print('address_key:', dial_out_address_split[4])
                    address_key.append(bytes(dial_out_address_split[4], 'utf-8'))

                    # Fingerprint
                    fingerprint_file = dial_out_address_split[5]
                    print('reading fingerprint_file:', fingerprint_file)
                    address_fingerprint_string = ''
                    if os.path.exists(fingerprint_file):
                        with open(fingerprint_file, 'r') as fingerprint_fo:
                            for line in fingerprint_fo:
                                address_fingerprint_string = address_fingerprint_string + line
                        fo.close()
                        address_fingerprint.append(bytes(address_fingerprint_string, 'utf-8'))

        configuration_thread_completed = True


class AESCipher:

    def __init__(self, KEY):
        self.key = KEY

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:])).decode('utf8')


class DialOutClass(QThread):
    def __init__(self, dial_out_title, dial_out_com1):
        QThread.__init__(self)
        global address_name, address_ip, address_port, address_key, address_fingerprint

        self.dial_out_title = dial_out_title
        self.dial_out_com1 = dial_out_com1

        self.HOST_SEND = ''
        self.PORT_SEND = ''
        self.KEY = ''
        self.FINGERPRINT = ''

    def run(self):
        print('-' * 200)
        print('[ thread started: DialOutClass(QThread).run(self) ]')
        global dial_out_thread_key

        self.HOST_SEND = address_ip[dial_out_address_index]
        self.PORT_SEND = address_port[dial_out_address_index]
        self.KEY = address_key[dial_out_address_index]
        self.FINGERPRINT = address_fingerprint[dial_out_address_index]

        if dial_out_thread_key == 'COM1':
            self.COM1()

    def COM1(self):
        global SOCKET_DIAL_OUT
        print('-' * 200)
        print(f"[DialOutClass] outgoing: COM1 to {self.HOST_SEND} : {self.PORT_SEND}")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SOCKET_DIAL_OUT:
                SOCKET_DIAL_OUT.connect((self.HOST_SEND, self.PORT_SEND))

                cipher = AESCipher(self.KEY)
                ciphertext = cipher.encrypt(str(self.FINGERPRINT) + 'COM1')
                print('sending ciphertext:', ciphertext)

                SOCKET_DIAL_OUT.send(ciphertext)
                SOCKET_DIAL_OUT.settimeout(1)

                try:
                    data = SOCKET_DIAL_OUT.recv(2048)
                except Exception as e:
                    print(e)

            print('data:      ', data)
            print('ciphertext:', ciphertext)
            if data == ciphertext:
                print(f"[DialOutClass] incoming: COM1 received by {self.HOST_SEND} : {self.PORT_SEND}")
                self.dial_out_com1.setStyleSheet(com1_stylesheet_green)
                time.sleep(1)
                self.dial_out_com1.setStyleSheet(com1_stylesheet_default)
                global_self.setFocus()

        except Exception as e:
            print(e)
            self.dial_out_com1.setStyleSheet(com1_stylesheet_red)
            time.sleep(1)
            self.dial_out_com1.setStyleSheet(com1_stylesheet_default)
            global_self.setFocus()

    def stop(self):
        global SOCKET_DIAL_OUT
        print('-' * 200)
        print('[ thread terminating: DialOutClass(QThread).run(self) ]')
        try:
            SOCKET_DIAL_OUT.close()
        except Exception as e:
            print(e)
        global_self.setFocus()
        self.terminate()


class PublicServerClass(QThread):
    def __init__(self, server_title, server_com1):
        QThread.__init__(self)
        self.server_com1 = server_com1
        self.server_title = server_title
        self.data = ''

    def run(self):
        print('-' * 200)
        self.data = str(datetime.datetime.now()) + ' [SERVER] public server started'
        print(self.data)
        self.server_logger()

        global server_thread_key
        while True:
            if server_thread_key == 'listen':
                try:
                    self.listen()
                except Exception as e:
                    print(e)

    def server_logger(self):
        if not os.path.exists(server_log):
            open(server_log, 'w').close()
        with open(server_log, 'a') as fo:
            fo.write(self.data + '\n')
        fo.close()

    def notification(self):
        self.server_com1.setStyleSheet(com1_stylesheet_green)

        url = QUrl.fromLocalFile("communicator_0.wav")
        content = QMediaContent(url)
        player = QMediaPlayer()
        player.setMedia(content)
        player.setVolume(100)
        player.play()
        time.sleep(1)

        self.server_com1.setStyleSheet(com1_stylesheet_default)

    def listen(self):
        global SERVER_ADDRESS
        global SOCKET_SERVER
        global DIAL_OUT_ADDRESSES
        global crypt_key

        self.server_title.setStyleSheet(server_title_stylesheet_1)

        print('[PublicServerClass] SERVER_ADDRESS:', SERVER_ADDRESS)
        self.SERVER_HOST = SERVER_ADDRESS.split(' ')[0]
        self.SERVER_PORT = int(SERVER_ADDRESS.split(' ')[1])

        print('-' * 200)
        print('SERVER_HOST:', self.SERVER_HOST)
        print('SERVER_PORT:', self.SERVER_PORT)
        print('SERVER: attempting to listen')

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SOCKET_SERVER:
                SOCKET_SERVER.bind((self.SERVER_HOST, self.SERVER_PORT))
                SOCKET_SERVER.listen()
                conn, addr = SOCKET_SERVER.accept()
                with conn:
                    print('-' * 200)
                    self.data = str(datetime.datetime.now()) + ' [SERVER] incoming connection: ' + str(addr)
                    print(self.data)
                    self.server_logger()
                    while True:
                        data = conn.recv(2048)
                        if not data:
                            break

                        # show connection received data
                        self.data = str(datetime.datetime.now()) + ' [SERVER] connection received data: ' + str(addr) + ' data: ' + str(data)
                        print(self.data)
                        self.server_logger()

                        decrypted = ''
                        decrypted_message = ''

                        # Next Try Named Key(s)
                        i = 0
                        for _ in address_key:
                            print(_)
                            print('trying key:', _)

                            try:
                                crypt_key = _
                                cipher = AESCipher(crypt_key)
                                decrypted = cipher.decrypt(data)
                            except Exception as e:
                                print(e)

                            print(decrypted)
                            if len(decrypted) > 0:
                                print('successfully decrypted message:', decrypted)
                                print('message appears to be from:', address_name[i])
                                print('attempting to fingerprint the message')
                                print('add_fingerprint:', address_fingerprint[i])
                                print('snd_fingerprint:', decrypted)
                                if decrypted.startswith(str(address_fingerprint[i])):
                                    print('fingerprint: validated as', address_name[i])
                                    decrypted_message = decrypted.replace(str(address_fingerprint[i]), '')
                                    print('decrypted_message:', decrypted_message)
                                else:
                                    print('fingerprint: does not match', address_name[i])
                                break
                            i += 1

                        # send delivery confirmation message
                        conn.sendall(data)

                        if decrypted_message == "COM1":
                            self.data = str(datetime.datetime.now()) + ' [SERVER] data recognized as internal command COM1: ' + str(addr)
                            print(self.data)
                            self.server_logger()
                            self.notification()
                            global_self.setFocus()

        except Exception as e:
            print(e)
            self.server_title.setStyleSheet(server_title_stylesheet_0)
            global_self.setFocus()

    def stop(self):
        global SOCKET_SERVER
        print('-' * 200)
        self.data = str(datetime.datetime.now()) + '  [SERVER] public server terminating'
        print(self.data)
        self.server_logger()
        try:
            SOCKET_SERVER.close()
        except Exception as e:
            print(e)
        self.server_title.setStyleSheet(server_title_stylesheet_0)
        global_self.setFocus()
        self.terminate()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
