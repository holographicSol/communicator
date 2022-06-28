"""
Written by Benjamin Jack Cullen aka Holographic_Sol
"""

import os
import sys
import time
import datetime
import socket
from win32api import GetSystemMetrics
from PyQt5.QtCore import Qt, QThread, QSize, QPoint, QCoreApplication, QObject, QTimer
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5 import QtCore
from Crypto.Cipher import AES
from hashlib import sha256
import base64
from Crypto import Random
import random
import string
import unicodedata


def NFD(text):
    return unicodedata.normalize('NFD', text)


def canonical_caseless(text):
    return NFD(NFD(text).casefold())

# key, initialization vector and padding
# crypt_iv = bytes('This is an IV456', 'utf-8')
BS = 16
pad = lambda s: bytes(s + (BS - len(s) % BS) * chr(BS - len(s) % BS), 'utf-8')
unpad = lambda s : s[0:-ord(s[-1:])]

# Socket Instances
SOCKET_DIAL_OUT = []
SOCKET_SERVER = []

# Addresses
DIAL_OUT_ADDRESSES = []
server_data = []

# NEW ADDRESS SETTINGS
server_addresses = []
server_address = ''
server_address_index = 0
server_ip = []
server_port = []

# Dial Out Settings
dial_out_thread_key = ''
dial_out_address = ''
dial_out_address_index = 0
address_name = []
address_ip = []
address_port = []
address_key = []
address_fingerprint = []
dial_out_dial_out_cipher_bool = True

# Wild Addresses
wild_addresses_ip = []

# Messages
messages = []
address_server_data = []
cipher_message_count = 0
alien_message_count = 0

# Public Settings
server_thread_key = ''
send_thread_key = ''
server_log = './log/server_log.txt'

# Configuration Settings
configuration_thread_key = ''
configuration_thread_completed = False
write_configuration_engaged = False

# Stylesheet - Server Title (Mode 0)
server_title_stylesheet_0 = """QLabel{background-color: rgb(10, 10, 10);
                       color: rgb(200, 200, 200);
                       border-bottom:2px solid rgb(5, 5, 5);
                       border-right:2px solid rgb(5, 5, 5);
                       border-top:2px solid rgb(5, 5, 5);
                       border-left:2px solid rgb(5, 5, 5);}"""

# Stylesheet - Server Switches (Mode 0)
button_stylesheet_0 = """QPushButton{background-color: rgb(10, 10, 10);
                       color: rgb(200, 200, 200);
                       border-bottom:2px solid rgb(5, 5, 5);
                       border-right:2px solid rgb(5, 5, 5);
                       border-top:2px solid rgb(5, 5, 5);
                       border-left:2px solid rgb(5, 5, 5);}"""

non_standard_communication_count = """QPushButton{background-color: rgb(10, 10, 10);
                       color: rgb(200, 100, 0);
                       border-bottom:2px solid rgb(5, 5, 5);
                       border-right:2px solid rgb(5, 5, 5);
                       border-top:2px solid rgb(5, 5, 5);
                       border-left:2px solid rgb(5, 5, 5);}"""

standard_communication_count = """QPushButton{background-color: rgb(10, 10, 10);
                       color: rgb(200, 200, 200);
                       border-bottom:2px solid rgb(5, 5, 5);
                       border-right:2px solid rgb(5, 5, 5);
                       border-top:2px solid rgb(5, 5, 5);
                       border-left:2px solid rgb(5, 5, 5);}"""

# Stylesheet - Server Switches (Mode 2)
dial_out_message_stylesheet = """QLineEdit{background-color: rgb(10, 10, 10);
                       color: rgb(0, 255, 0);
                       border-bottom:2px solid rgb(5, 5, 5);
                       border-right:2px solid rgb(5, 5, 5);
                       border-top:2px solid rgb(5, 5, 5);
                       border-left:2px solid rgb(5, 5, 5);}"""

# Stylesheet - QLineEdit Default
qline_edit_style_sheet_default = """QLineEdit{background-color: rgb(10, 10, 10);
                       color: rgb(200, 200, 200);
                       border-bottom:2px solid rgb(5, 5, 5);
                       border-right:2px solid rgb(5, 5, 5);
                       border-top:2px solid rgb(5, 5, 5);
                       border-left:2px solid rgb(5, 5, 5);}"""

# Stylesheet - Dial Out COM1 (Mode 2)
dial_out_add_addr_stylesheet_red = """QPushButton{background-color: rgb(10, 10, 10);
                       color: rgb(200, 200, 200);
                       border-bottom:2px solid rgb(5, 5, 5);
                       border-right:2px solid rgb(5, 5, 5);
                       border-top:2px solid rgb(5, 5, 5);
                       border-left:2px solid rgb(5, 5, 5);}"""

# Stylesheet - Fingerprint Gen (Mode 0)
fingerprint_generator_stylesheet = """QPushButton{background-color: rgb(255, 120, 0);
                       color: rgb(200, 200, 200);
                       border-bottom:2px solid rgb(5, 5, 5);
                       border-right:2px solid rgb(5, 5, 5);
                       border-top:2px solid rgb(5, 5, 5);
                       border-left:2px solid rgb(5, 5, 5);}"""

dial_out_cipher_stylesheet_0 = """QPushButton{background-color: rgb(10, 10, 10);
                       color: rgb(255, 0, 0);
                       border-bottom:2px solid rgb(5, 5, 5);
                       border-right:2px solid rgb(5, 5, 5);
                       border-top:2px solid rgb(5, 5, 5);
                       border-left:2px solid rgb(5, 5, 5);}"""

dial_out_cipher_stylesheet_1 = """QPushButton{background-color: rgb(10, 10, 10);
                       color: rgb(0, 255, 0);
                       border-bottom:2px solid rgb(5, 5, 5);
                       border-right:2px solid rgb(5, 5, 5);
                       border-top:2px solid rgb(5, 5, 5);
                       border-left:2px solid rgb(5, 5, 5);}"""

tb_0_stylesheet = """QTextBrowser {background-color: rgb(10, 10, 10);
                selection-color: black;
                selection-background-color: rgb(0, 180, 0);
                color: rgb(200, 200, 200);
                border-bottom:2px solid rgb(5, 5, 5);
                border-right:2px solid rgb(5, 5, 5);
                border-top:2px solid rgb(5, 5, 5);
                border-left:2px solid rgb(5, 5, 5);}"""

global_self = []


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        global global_self
        global_self = self

        self.font_s7b = QFont("Segoe UI", 7, QFont.Bold)

        self.setStyleSheet("""
                                    QScrollBar:vertical {width: 11px;
                                    margin: 11px 0 11px 0;
                                    background-color: black;
                                    }
                                    QScrollBar::handle:vertical {
                                    background-color: black;
                                    min-height: 11px;
                                    }
                                    QScrollBar::add-line:vertical {
                                    background-color: black;
                                    height: 11px;
                                    subcontrol-position: bottom;
                                    subcontrol-origin: margin;
                                    }
                                    QScrollBar::sub-line:vertical {
                                    background-color: black;
                                    height: 11px;
                                    subcontrol-position: top;
                                    subcontrol-origin: margin;
                                    }
                                    QScrollBar::up-arrow:vertical {
                                    image:url('./resources/image/small_img_menu_up.png');
                                    height: 11px;
                                    width: 11px;
                                    }
                                    QScrollBar::down-arrow:vertical {
                                    image:url('./resources/image/small_img_menu_down.png');
                                    height: 11px;
                                    width: 11px;
                                    }
                                    QScrollBar::add-page:vertical {
                                    background: rgb(25, 25, 25);
                                    }
                                    QScrollBar::sub-page:vertical {
                                    background: rgb(25, 25, 25);
                                    }

                                    QScrollBar:horizontal {
                                    height: 11px;
                                    margin: 0px 11px 0 11px;
                                    background-color: black;
                                    }
                                    QScrollBar::handle:horizontal {
                                    background-color: black;
                                    min-width: 11px;
                                    }
                                    QScrollBar::add-line:horizontal {
                                    background-color: black;
                                    width: 11px;
                                    subcontrol-position: right;
                                    subcontrol-origin: margin;
                                    }
                                    QScrollBar::sub-line:horizontal {
                                    background-color: black;
                                    width: 11px;
                                    subcontrol-position: top left;
                                    subcontrol-origin: margin;
                                    position: absolute;
                                    }
                                    QScrollBar::left-arrow:horizontal {
                                    image:url('./resources/image/small_img_menu_left.png');
                                    height: 11px;
                                    width: 11px;
                                    }
                                    QScrollBar::right-arrow:horizontal {
                                    image:url('./resources/image/small_img_menu_right.png');
                                    height: 11px;
                                    width: 11px;
                                    }
                                    QScrollBar::add-page:horizontal {
                                    background: rgb(25, 25, 25);
                                    }
                                    QScrollBar::sub-page:horizontal {
                                    background: rgb(25, 25, 25);
                                    }
                                    """)

        """ Tooltip """
        self.tooltip_style = """QToolTip {background-color: rgb(35, 35, 35);
                                   color: rgb(200, 200, 200);
                                   border-top:0px solid rgb(35, 35, 35);
                                   border-bottom:0px solid rgb(35, 35, 35);
                                   border-right:0px solid rgb(0, 0, 0);
                                   border-left:0px solid rgb(0, 0, 0);}"""
        self.setStyleSheet(self.tooltip_style)

        def dial_out_prev_addr_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.dial_out_prev_addr_function')
            global_self.setFocus()
            global dial_out_address, dial_out_address_index
            global address_name, address_ip, address_port, address_key, address_fingerprint

            # Get length of address book
            LEN_DIAL_OUT_ADDRESSES = len(DIAL_OUT_ADDRESSES)
            print(str(datetime.datetime.now()) + ' -- len(DIAL_OUT_ADDRESSES):', len(DIAL_OUT_ADDRESSES))

            # Step through address book
            if dial_out_address_index == 0:
                print(str(datetime.datetime.now()) + ' -- dial_out_address_index is zero: setting dial_out_address_index to len(DIAL_OUT_ADDRESSES)')
                dial_out_address_index = LEN_DIAL_OUT_ADDRESSES - 1
            else:
                print(str(datetime.datetime.now()) + ' -- dial_out_address_index is not zero: subtracting 1 from DIAL_OUT_ADDRESSES')
                dial_out_address_index = dial_out_address_index - 1

            print(str(datetime.datetime.now()) + ' -- setting dial_out_address_index:', dial_out_address_index)
            print(str(datetime.datetime.now()) + ' -- setting dial_out_address using dial_out_address_index:', DIAL_OUT_ADDRESSES[dial_out_address_index])

            dial_out_address = address_ip[dial_out_address_index] + ' ' + str(address_port[dial_out_address_index])
            print(str(datetime.datetime.now()) + ' -- dial_out_address:', dial_out_address)
            self.dial_out_ip_port.setText(dial_out_address)
            print(str(datetime.datetime.now()) + ' -- set dial_out_ip_port text:', dial_out_address)
            self.dial_out_name.setText(address_name[dial_out_address_index])
            print(str(datetime.datetime.now()) + ' -- set dial_out_name text:', address_name[dial_out_address_index])

        def dial_out_next_addr_function():
            global address_name, address_ip, address_port, address_key, address_fingerprint
            print(str(datetime.datetime.now()) + ' -- plugged in: App.dial_out_next_addr_function')
            global_self.setFocus()
            global dial_out_address, dial_out_address_index

            # Get length of address book
            LEN_DIAL_OUT_ADDRESSES = len(DIAL_OUT_ADDRESSES)
            print(str(datetime.datetime.now()) + ' -- len(DIAL_OUT_ADDRESSES):', len(DIAL_OUT_ADDRESSES))

            # Step through address book
            if dial_out_address_index == LEN_DIAL_OUT_ADDRESSES - 1:
                print(str(datetime.datetime.now()) + ' -- dial_out_address_index is reached max: setting dial_out_address_index to zero')
                dial_out_address_index = 0
            else:
                print(str(datetime.datetime.now()) + ' -- dial_out_address_index is not max: adding 1 to dial_out_address_index')
                dial_out_address_index += 1

            print(str(datetime.datetime.now()) + ' -- setting dial_out_address_index:', dial_out_address_index)
            print(str(datetime.datetime.now()) + ' -- setting dial_out_address using dial_out_address_index:', DIAL_OUT_ADDRESSES[dial_out_address_index])

            dial_out_address = address_ip[dial_out_address_index] + ' ' + str(address_port[dial_out_address_index])
            print(str(datetime.datetime.now()) + ' -- dial_out_address:', dial_out_address)
            self.dial_out_ip_port.setText(dial_out_address)
            print(str(datetime.datetime.now()) + ' -- set dial_out_ip_port text:', dial_out_address)
            self.dial_out_name.setText(address_name[dial_out_address_index])
            print(str(datetime.datetime.now()) + ' -- set dial_out_name text:', address_name[dial_out_address_index])

        def dial_out_ip_port_function_set():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.dial_out_ip_port_function_set')
            global_self.setFocus()
            global dial_out_address
            dial_out_address = self.dial_out_ip_port.text()
            print(str(datetime.datetime.now()) + ' -- setting dial out address:', dial_out_address)

        def dial_out_com1_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.dial_out_com1_function')
            global_self.setFocus()
            global dial_out_thread_key
            if dial_out_thread.isRunning() is True:
                dial_out_thread.stop()
            dial_out_thread_key = 'COM1'
            dial_out_thread.start()

        def dial_out_message_send_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.dial_out_com1_function')
            global_self.setFocus()
            global dial_out_thread_key
            if not self.dial_out_message.text() == '':
                if dial_out_thread.isRunning() is True:
                    dial_out_thread.stop()
                dial_out_thread_key = 'MESSAGE'
                dial_out_thread.start()
            else:
                print(str(datetime.datetime.now()) + ' -- dial_out_message_send_function: blocking empty message send')

        def start_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.start_function')
            global_self.setFocus()
            global server_thread_key
            server_thread.stop()
            server_thread_key = 'listen'
            server_thread.start()

        def stop_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.stop_function')
            global_self.setFocus()
            if server_thread.isRunning() is True:
                server_thread.stop()
            else:
                print('public server: already stopped')

        def server_ip_port_write_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.server_ip_port_write_function')
            global_self.setFocus()
            global server_addresses
            global server_address
            global server_ip
            global server_port
            global write_configuration_engaged
            global server_address_index
            if write_configuration_engaged is False:

                write_configuration_engaged = True

                server_address_var = self.server_ip_port.text()
                if server_address_var not in server_addresses:
                    print(str(datetime.datetime.now()) + ' -- new server address detected:', server_address_var)

                    self.write_var = 'SERVER_ADDRESS ' + self.server_ip_port.text()
                    print(str(datetime.datetime.now()) + ' -- setting write variable:', self.write_var)

                    with open('./config.txt', 'a') as fo:
                        fo.write(self.write_var + '\n')
                    fo.close()

                    server_addresses.append(server_address_var)
                    server_ip.append(server_address_var.split()[0])
                    server_port.append(server_address_var.split()[1])
                    server_address_index = server_addresses.index(server_address_var)
                    print(str(datetime.datetime.now()) + ' -- changing server_address_index to:', server_address_index)
                    server_address = server_addresses[server_address_index]
                    print(str(datetime.datetime.now()) + ' -- setting server_address using server_address_index:', server_address)

                else:
                    print(str(datetime.datetime.now()) + ' -- server address already exists:', server_address_var)
                    server_address_index = server_addresses.index(server_address_var)
                    print(str(datetime.datetime.now()) + ' -- changing server_address_index to:', server_address_index)
                    server_address = server_addresses[server_address_index]
                    print(str(datetime.datetime.now()) + ' -- setting server_address using server_address_index:', server_address)

                write_configuration_engaged = False

            else:
                print(str(datetime.datetime.now()) + ' -- write_configuration_engaged:', write_configuration_engaged)

        def server_prev_addr_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.server_prev_addr_function')
            global_self.setFocus()
            global server_address, server_address_index, server_addresses
            global server_ip, server_port

            LEN_SERVER_ADDRESSES = len(server_addresses)
            print(str(datetime.datetime.now()) + ' -- len(server_addresses):', len(server_addresses))

            # Step through address book
            if server_address_index == 0:
                print(str(datetime.datetime.now()) + ' -- server_address_index is zero: setting server_address_index to len(server_addresses)')
                server_address_index = LEN_SERVER_ADDRESSES - 1
            else:
                print(str(datetime.datetime.now()) + ' -- server_address_index is not zero: subtracting 1 from server_address_index')
                server_address_index = server_address_index - 1

            print(str(datetime.datetime.now()) + ' -- setting server_address_index:', server_address_index)
            print(str(datetime.datetime.now()) + ' -- setting server_address using server_address_index:', server_addresses[server_address_index])

            server_address = server_addresses[server_address_index]
            print(str(datetime.datetime.now()) + ' -- server_address:', server_address)
            self.server_ip_port.setText(server_address)
            print(str(datetime.datetime.now()) + ' -- set server_ip_port text:', server_address)

        def server_next_addr_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.server_next_addr_function')
            global_self.setFocus()
            global server_address, server_address_index, server_addresses
            global server_ip, server_port

            # Get length of address book
            LEN_SERVER_ADDRESSES = len(server_addresses)
            print(str(datetime.datetime.now()) + ' -- len(server_addresses):', len(server_addresses))

            # Step through address book
            if server_address_index == LEN_SERVER_ADDRESSES - 1:
                print(str(datetime.datetime.now()) + ' -- server_address_index reached max: setting server_address_index to zero')
                server_address_index = 0
            else:
                print(str(datetime.datetime.now()) + ' -- server_address_index is not max: adding 1 to server_address_index')
                server_address_index += 1

            print(str(datetime.datetime.now()) + ' -- setting server_address_index:', server_address_index)
            print(str(datetime.datetime.now()) + ' -- setting server_address using server_address_index:', server_addresses[server_address_index])

            server_address = server_addresses[server_address_index]
            print(str(datetime.datetime.now()) + ' -- server_address:', server_address)
            self.server_ip_port.setText(server_address)
            print(str(datetime.datetime.now()) + ' -- set server_ip_port text:', server_address)

        def dial_out_next_add_addr_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.dial_out_next_add_addr_function')
            finger_print_gen_thread.start()

        def dial_out_next_rem_addr_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.dial_out_next_rem_addr_function')

        def dial_out_name_function_set():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.dial_out_name_function_set')
            if self.dial_out_name.text() not in address_name:
                print('-- accepting name as name does not already exist')

        def dial_out_dial_out_cipher_bool_btn_function():
            global dial_out_dial_out_cipher_bool
            print(str(datetime.datetime.now()) + ' -- plugged in: App.dial_out_dial_out_cipher_bool_function')
            if dial_out_dial_out_cipher_bool is True:
                dial_out_dial_out_cipher_bool = False
                self.dial_out_cipher_bool_btn.setStyleSheet(dial_out_cipher_stylesheet_0)
                print(str(datetime.datetime.now()) + ' -- setting dial_out_dial_out_cipher_bool:', dial_out_dial_out_cipher_bool)
            else:
                dial_out_dial_out_cipher_bool = True
                self.dial_out_cipher_bool_btn.setStyleSheet(dial_out_cipher_stylesheet_1)
                print(str(datetime.datetime.now()) + ' -- setting dial_out_dial_out_cipher_bool:', dial_out_dial_out_cipher_bool)

        def server_notify_cipher_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.server_notify_cipher_function')
            global cipher_message_count
            cipher_message_count = 0
            self.server_notify_cipher.setText(str(cipher_message_count))

        def server_notify_alien_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.server_notify_alien_function')
            global alien_message_count
            alien_message_count = 0
            self.server_notify_alien.setText(str(alien_message_count))

        # Variable should be set before running write_configuration function
        self.write_var = ''

        # Window Title
        self.title = "Communicator"
        self.setWindowTitle('Communicator')
        self.setWindowIcon(QIcon('./resources/image/icon.ico'))

        # Window Geometry
        self.width, self.height = 496, 226
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
        self.server_ip_port.move(self.button_spacing_w * 5 + self.server_title_width + self.button_wh * 3, self.zone_spacing_h)
        self.server_ip_port.returnPressed.connect(server_ip_port_write_function)
        self.server_ip_port.setText('')
        self.server_ip_port.setStyleSheet(qline_edit_style_sheet_default)
        self.server_ip_port.setAlignment(Qt.AlignCenter)

        # QPushButton - Server Received Communication COM1
        self.server_com1 = QPushButton(self)
        self.server_com1.resize(self.button_wh, self.button_wh)
        self.server_com1.move(self.width - self.button_wh - self.button_spacing_w, self.zone_spacing_h)
        self.server_com1.setIcon(QIcon("./resources/image/public_FILL1_wght100_GRAD200_opsz40_WHITE.png"))
        self.server_com1.setIconSize(QSize(self.button_wh - 8, self.button_wh - 8))
        self.server_com1.setStyleSheet(button_stylesheet_0)

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
        self.dial_out_ip_port.move(self.button_spacing_w * 5 + self.server_title_width + self.button_wh * 3, self.zone_spacing_h * 2 + self.button_wh)
        self.dial_out_ip_port.returnPressed.connect(dial_out_ip_port_function_set)
        self.dial_out_ip_port.setText('')
        self.dial_out_ip_port.setStyleSheet(qline_edit_style_sheet_default)
        self.dial_out_ip_port.setAlignment(Qt.AlignCenter)

        # QPushButton - Dial Out Send COM1 message
        self.dial_out_com1 = QPushButton(self)
        self.dial_out_com1.resize(self.button_wh, self.button_wh)
        self.dial_out_com1.move(self.width - self.button_wh - self.button_spacing_w, self.zone_spacing_h * 2 + self.button_wh)
        self.dial_out_com1.setIcon(QIcon("./resources/image/cell_tower_FILL1_wght200_GRAD200_opsz40_WHITE.png"))
        self.dial_out_com1.setIconSize(QSize(self.button_wh - 12, self.button_wh - 12))
        self.dial_out_com1.setStyleSheet(button_stylesheet_0)
        self.dial_out_com1.clicked.connect(dial_out_com1_function)

        # QPushButton - Dial Out Previous Address
        self.dial_out_prev_addr = QPushButton(self)
        self.dial_out_prev_addr.resize(self.button_wh, self.button_wh)
        self.dial_out_prev_addr.move(self.button_spacing_w * 4 + self.server_title_width + self.button_wh * 2, self.zone_spacing_h * 2 + self.button_wh)
        self.dial_out_prev_addr.setIcon(QIcon("./resources/image/baseline_keyboard_arrow_left_white_18dp.png"))
        self.dial_out_prev_addr.setIconSize(QSize(self.button_wh, self.button_wh))
        self.dial_out_prev_addr.setStyleSheet(button_stylesheet_0)
        self.dial_out_prev_addr.clicked.connect(dial_out_prev_addr_function)

        # QPushButton - Dial Out Next Address
        self.dial_out_next_addr = QPushButton(self)
        self.dial_out_next_addr.resize(self.button_wh, self.button_wh)
        self.dial_out_next_addr.move(self.button_spacing_w * 6 + self.server_title_width + self.button_wh * 3 + self.ip_port_width, self.zone_spacing_h * 2 + self.button_wh)
        self.dial_out_next_addr.setIcon(QIcon("./resources/image/baseline_keyboard_arrow_right_white_18dp.png"))
        self.dial_out_next_addr.setIconSize(QSize(self.button_wh, self.button_wh))
        self.dial_out_next_addr.setStyleSheet(button_stylesheet_0)
        self.dial_out_next_addr.clicked.connect(dial_out_next_addr_function)

        # QPushButton - Dial Out Set Encryption Boolean
        self.dial_out_cipher_bool_btn = QPushButton(self)
        self.dial_out_cipher_bool_btn.resize(self.button_wh, self.button_wh)
        self.dial_out_cipher_bool_btn.move(self.button_spacing_w * 7 + self.server_title_width + self.button_wh * 4 + self.ip_port_width, self.zone_spacing_h * 2 + self.button_wh)
        # self.dial_out_cipher_bool_btn.setIcon(QIcon("./resources/image/baseline_keyboard_arrow_right_white_18dp.png"))
        # self.dial_out_cipher_bool_btn.setIconSize(QSize(self.button_wh, self.button_wh))
        self.dial_out_cipher_bool_btn.setText('CIPHER')
        self.dial_out_cipher_bool_btn.setFont(self.font_s7b)
        self.dial_out_cipher_bool_btn.setStyleSheet(dial_out_cipher_stylesheet_1)
        self.dial_out_cipher_bool_btn.clicked.connect(dial_out_dial_out_cipher_bool_btn_function)

        # QPushButton - Dial Out Name
        self.dial_out_name = QLineEdit(self)
        self.dial_out_name.resize(self.button_wh * 2 + 4, int(self.button_wh / 2))
        self.dial_out_name.move(self.button_spacing_w * 2 + self.server_title_width, self.zone_spacing_h * 2 + self.button_wh)
        self.dial_out_name.setText('')
        self.dial_out_name.setStyleSheet(qline_edit_style_sheet_default)
        self.dial_out_name.setAlignment(Qt.AlignCenter)
        self.dial_out_name.returnPressed.connect(dial_out_name_function_set)

        # QPushButton - Dial Out Add Address
        self.dial_out_add_addr = QPushButton(self)
        self.dial_out_add_addr.resize(self.button_wh, int(self.button_wh / 2) - 4)
        self.dial_out_add_addr.move(self.button_spacing_w * 3 + self.server_title_width + self.button_wh, self.zone_spacing_h * 2 + self.button_wh + int(self.button_wh / 2) + 4)
        self.dial_out_add_addr.setIcon(QIcon("./resources/image/add_FILL0_wght400_GRAD200_opsz18_WHITE.png"))
        self.dial_out_add_addr.setIconSize(QSize(14, 14))
        self.dial_out_add_addr.setStyleSheet(button_stylesheet_0)
        self.dial_out_add_addr.clicked.connect(dial_out_next_add_addr_function)
        self.dial_out_add_addr.setToolTip(" ADD ADDRESS\n\n 1. Enter Name\n 2. Enter IP & Port\n 3. Then press this button if you wish to add to the address book.\n\n An entry in the address book will be created with a key and a path to a generated fingerprint file.\n You may then share the fingerprint with the contact and they can add you as the key name in their address book.\n\n WARNING! Use a unique name to avoid an existing matching name being overwritten!")

        # QPushButton - Dial Out Remove Address
        self.dial_out_rem_addr = QPushButton(self)
        self.dial_out_rem_addr.resize(self.button_wh, int(self.button_wh / 2) - 4)
        self.dial_out_rem_addr.move(self.button_spacing_w * 2 + self.server_title_width, self.zone_spacing_h * 2 + self.button_wh + int(self.button_wh / 2) + 4)
        self.dial_out_rem_addr.setFont(self.font_s7b)
        self.dial_out_rem_addr.setText('DEL')
        self.dial_out_rem_addr.setIconSize(QSize(14, 14))
        self.dial_out_rem_addr.setStyleSheet(button_stylesheet_0)
        self.dial_out_rem_addr.clicked.connect(dial_out_next_rem_addr_function)

        # QLabel - Dial Out Message Title
        self.dial_out_message_title = QLabel(self)
        self.dial_out_message_title.resize(self.server_title_width, self.button_wh)
        self.dial_out_message_title.move(self.button_spacing_w, self.zone_spacing_h * 3 + self.button_wh * 2)
        self.dial_out_message_title.setText('MESSAGE')
        self.dial_out_message_title.setAlignment(Qt.AlignCenter)
        self.dial_out_message_title.setStyleSheet(server_title_stylesheet_0)

        # QLabel - Dial Out Message
        self.dial_out_message = QLineEdit(self)
        self.dial_out_message.resize(360, self.button_wh - 20)
        self.dial_out_message.move(self.button_spacing_w * 2 + self.server_title_width, self.zone_spacing_h * 3 + self.button_wh * 2)
        self.dial_out_message.setText('')
        self.dial_out_message.setStyleSheet(dial_out_message_stylesheet)

        # QLabel - Dial Out Message Send
        self.dial_out_message_send = QPushButton(self)
        self.dial_out_message_send.resize(self.button_wh, self.button_wh)
        self.dial_out_message_send.move(self.width - self.button_wh - self.button_spacing_w, self.zone_spacing_h * 3 + self.button_wh * 2)
        self.dial_out_message_send.setIcon(QIcon("./resources/image/send_FILL1_wght100_GRAD-25_opsz40_WHITE.png"))
        self.dial_out_message_send.setIconSize(QSize(self.button_wh - 14, self.button_wh - 14))
        self.dial_out_message_send.setStyleSheet(button_stylesheet_0)
        self.dial_out_message_send.clicked.connect(dial_out_message_send_function)

        # QPushButton - Server Previous Address
        self.server_prev_addr = QPushButton(self)
        self.server_prev_addr.resize(self.button_wh, self.button_wh)
        self.server_prev_addr.move(self.button_spacing_w * 4 + self.server_title_width + self.button_wh * 2, self.zone_spacing_h)
        self.server_prev_addr.setIcon(QIcon("./resources/image/baseline_keyboard_arrow_left_white_18dp.png"))
        self.server_prev_addr.setIconSize(QSize(self.button_wh, self.button_wh))
        self.server_prev_addr.setStyleSheet(button_stylesheet_0)
        self.server_prev_addr.clicked.connect(server_prev_addr_function)

        # QPushButton - Server Out Next Address
        self.server_next_addr = QPushButton(self)
        self.server_next_addr.resize(self.button_wh, self.button_wh)
        self.server_next_addr.move(self.button_spacing_w * 6 + self.server_title_width + self.button_wh * 3 + self.ip_port_width, self.zone_spacing_h)
        self.server_next_addr.setIcon(QIcon("./resources/image/baseline_keyboard_arrow_right_white_18dp.png"))
        self.server_next_addr.setIconSize(QSize(self.button_wh, self.button_wh))
        self.server_next_addr.setStyleSheet(button_stylesheet_0)
        self.server_next_addr.clicked.connect(server_next_addr_function)

        # QPushButton - Server Cipher Message Count
        self.server_notify_cipher = QPushButton(self)
        self.server_notify_cipher.resize(self.button_wh, int(self.button_wh / 2))
        self.server_notify_cipher.move(self.button_spacing_w * 7 + self.server_title_width + self.button_wh * 4 + self.ip_port_width, self.zone_spacing_h)
        self.server_notify_cipher.setStyleSheet(standard_communication_count)
        self.server_notify_cipher.setText(str(cipher_message_count))
        self.server_notify_cipher.clicked.connect(server_notify_cipher_function)

        # QPushButton - Server Alien Message
        self.server_notify_alien = QPushButton(self)
        self.server_notify_alien.resize(self.button_wh, int(self.button_wh / 2))
        self.server_notify_alien.move(self.button_spacing_w * 7 + self.server_title_width + self.button_wh * 4 + self.ip_port_width, self.zone_spacing_h + int(self.button_wh / 2))
        self.server_notify_alien.setStyleSheet(non_standard_communication_count)
        self.server_notify_alien.setText(str(alien_message_count))
        self.server_notify_alien.clicked.connect(server_notify_alien_function)

        # QLabel - Server Status
        self.server_status_label = QLabel(self)
        self.server_status_label.resize(156, 20)
        self.server_status_label.move(int(self.width / 2) - int(156 / 2), 134)
        self.server_status_label.setText('SERVER STATUS: OFFLINE')
        self.server_status_label.setAlignment(Qt.AlignCenter)
        self.server_status_label.setStyleSheet(server_title_stylesheet_0)

        # Thread - Public Server
        server_thread = ServerClass(self.server_title, self.server_com1, self.server_status_label)

        # Thread - ServerDataHandlerClass
        server_data_handler_class = ServerDataHandlerClass(self.server_title, self.server_com1, self.server_notify_cipher, self.server_notify_alien)
        server_data_handler_class.start()

        # Thread - Dial_Out
        dial_out_thread = DialOutClass(self.dial_out_title, self.dial_out_com1, self.dial_out_message_send, self.dial_out_message)

        # Thread - Configuration
        configuration_thread = ConfigurationClass()

        finger_print_gen_thread = FingerprintGeneration(self.dial_out_name, self.dial_out_ip_port, self.dial_out_add_addr)

        # Configuration Thread - Set Configuration Key
        global configuration_thread_key, server_addresses
        configuration_thread_key = 'ALL'

        # Configuration Thread - Run Configuration Thread
        configuration_thread.start()

        # Configuration Thread - Wait For Configuration Thread To Complete
        global configuration_thread_completed
        print(str(datetime.datetime.now()) + ' configuration_thread_completed:', configuration_thread_completed)
        while configuration_thread_completed is False:
            time.sleep(1)
        print(str(datetime.datetime.now()) + ' configuration_thread_completed:', configuration_thread_completed)

        if len(server_addresses) > 0:
            self.server_ip_port.setText(server_addresses[server_address_index])

        if len(address_name) > 0:
            self.dial_out_name.setText(address_name[dial_out_address_index])
        if len(address_ip) > 0 and len(address_port) > 0:
            self.dial_out_ip_port.setText(address_ip[dial_out_address_index] + ' ' + str(address_port[dial_out_address_index]))

        # QTextBrowser - Message Output
        self.tb_0 = QTextBrowser(self)
        self.tb_0.move(4, 154)
        self.tb_0.resize(self.width - 8, 60)
        self.tb_0.setObjectName("tb_0")
        self.tb_0.setStyleSheet(tb_0_stylesheet)
        self.tb_0.setLineWrapMode(QTextBrowser.NoWrap)
        self.tb_0.horizontalScrollBar().setValue(0)

        # RAPID TEXT APPEND EXAMPLE STEP 3: Create Timer That Connects To A Function (In This Case A PyQtSlot)
        self.timer_0 = QTimer(self)
        self.timer_0.setInterval(0)
        self.timer_0.timeout.connect(self.update_tb)
        self.server_start.clicked.connect(self.jumpstart_1)
        self.server_stop.clicked.connect(self.stop_timer_1)

        self.initUI()

    def initUI(self):
        self.show()

    def stop_timer_1(self):
        self.timer_0.stop()

    # Step 2 Connects To Here
    @QtCore.pyqtSlot()
    def jumpstart_1(self):
        self.timer_0.start()

    # Step 3 Connects To Here
    @QtCore.pyqtSlot()
    def update_tb(self):
        if messages:
            self.tb_0.append(messages[-1])
            messages.remove(messages[-1])


class FingerprintGeneration(QThread):
    def __init__(self, dial_out_name, dial_out_ip_port, dial_out_add_addr):
        QThread.__init__(self)
        self.fingerprint_var = []
        self.dial_out_ip_port = dial_out_ip_port
        self.dial_out_name = dial_out_name
        self.dial_out_add_addr = dial_out_add_addr
        self.key_string = ''
        self.entry_address_book = ''

    def update_values(self):
        global dial_out_address_index
        global dial_out_address
        global address_name
        global address_ip
        global address_port
        global address_key
        global address_fingerprint
        global DIAL_OUT_ADDRESSES

        dial_out_address_split = self.entry_address_book.split(' ')
        print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run dial_out_address_split:', dial_out_address_split)

        # Name
        print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run setting dial out name:', dial_out_address_split[1])
        address_name.append(dial_out_address_split[1])

        # IP
        print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run setting dial out ip:', dial_out_address_split[2])
        address_ip.append(dial_out_address_split[2])

        # Port
        print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run setting dial out port:', dial_out_address_split[3])
        address_port.append(int(dial_out_address_split[3]))

        # Key
        print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run setting address_key:', dial_out_address_split[4])
        address_key.append(bytes(dial_out_address_split[4], 'utf-8'))

        # Fingerprint
        print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run setting fingerprint:', dial_out_address_split[5])
        address_fingerprint.append(bytes(dial_out_address_split[5], 'utf-8'))

        DIAL_OUT_ADDRESSES.append(self.entry_address_book)

        print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run:', address_name)
        print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run:', address_ip)
        print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run:', address_port)
        print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run:', address_key)
        print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run:', address_fingerprint)
        dial_out_address_index = address_name.index(self.dial_out_name.text())
        dial_out_address = self.dial_out_ip_port.text()

    def randStr(self, chars=string.ascii_uppercase + string.digits, N=32):
        return ''.join(random.choice(chars) for _ in range(N))

    def iter_rand(self):
        self.key_string = self.randStr(chars=string.ascii_lowercase + string.ascii_uppercase + string.punctuation.replace("'", "f"))
        self.fingerprint_var.append(self.key_string)

    def run(self):
        print('-' * 200)
        print(str(datetime.datetime.now()) + ' [ thread started: FingerprintGeneration(QThread).run(self) ]')
        global address_name
        global dial_out_address_index
        
        try:

            self.dial_out_add_addr.setStyleSheet(fingerprint_generator_stylesheet)
    
            forbidden_fname = ['con', 'prn', 'aux', 'nul',
                               'com1', 'com2', 'com3', 'com4', 'com5', 'com6', 'com7', 'com8', 'com9',
                               'lpt1', 'lpt2', 'lpt3', 'lpt4', 'lpt5', 'lpt6', 'lpt7', 'lpt8', 'lpt9']
    
            address_name_var = str(self.dial_out_name.text()).replace('_', '')
            if str(address_name_var).isalnum():
                address_name_var = str(self.dial_out_name.text())
                if canonical_caseless(address_name_var) not in forbidden_fname:
                    print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run address_name[dial_out_address_index]: is not in forbidden_fname')
    
                    # Create initial address book entry consisting of name ip and port
                    self.entry_address_book = 'DATA ' + str(address_name_var) + ' ' + str(self.dial_out_ip_port.text())
                    print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run initial address book entry string:', self.entry_address_book)
    
                    # Create Key
                    self.iter_rand()
                    print(str(datetime.datetime.now()) + ' -- generating key:', self.key_string)
    
                    # Add key to address book entry string
                    self.entry_address_book = self.entry_address_book + ' ' + self.key_string
    
                    # Generate Fingerprint
                    i = 0
                    while i < 32:
                        self.iter_rand()
                        i += 1
    
                    print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run: fingerprint generated')
                    finger_print_fname = str('./fingerprints/' + str(address_name_var) + '.txt')
                    print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run generated finger_print_fname:', finger_print_fname)
    
                    self.entry_address_book = self.entry_address_book + ' ' + finger_print_fname
                    print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run full address book entry string:', self.entry_address_book)
    
                    # Write the fingerprint file
                    with open(finger_print_fname, 'w') as fo:
                        for _ in self.fingerprint_var:
                            print(_)
                            fo.write(_ + '\n')
                    fo.close()
    
                    # Check the fingerprint file
                    fingerprint_validation_bool = True
                    with open(finger_print_fname, 'r') as fo:
                        i = 0
                        for line in fo:
                            line = line.strip()
                            if line == self.fingerprint_var[i]:
                                print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run validating line:', str(i), 'in new fingerprint file:', line, '-->', self.fingerprint_var[i], '  [valid]')
                            elif line != self.fingerprint_var[i]:
                                print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run validating line:', str(i), 'in new fingerprint file:', line, '-->', self.fingerprint_var[i], '  [invalid]')
                                fingerprint_validation_bool = False
                            i += 1
                    fo.close()
                    print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run new fingerprint file validation:', fingerprint_validation_bool)
    
                    # If name in address book, overwrite existing entry in the address book
                    print('-' * 200)
                    if address_name_var in address_name:
                        print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run attempting to overwrite existing address book entry')
                        addr_var = []
                        if os.path.exists('./communicator_address_book.txt'):
                            print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run: address book exists')
                            with open('./communicator_address_book.txt', 'r') as fo:
                                for line in fo:
                                    line = line.strip()
                                    line_split = line.split(' ')
                                    if len(line_split) >= 2:
                                        if line_split[1] == address_name_var:
                                            print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run  changing existing entry:', line, '  -->  ', self.entry_address_book)
                                            addr_var.append(self.entry_address_book)
                                        else:
                                            print('--', line)
                                            addr_var.append(line)
                            with open('./communicator_address_book.txt', 'w') as fo:
                                for _ in addr_var:
                                    print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run writing address book line:', _)
                                    fo.write(_ + '\n')
                            fo.close()
                    else:
                        print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run appending new address book entry to address book')
                        with open('./communicator_address_book.txt', 'a') as fo:
                            fo.write(self.entry_address_book + '\n')
                        fo.close()
                    print('-' * 200)

                    self.update_values()
                    self.dial_out_add_addr.setStyleSheet(qline_edit_style_sheet_default)
                    time.sleep(1)

                    print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run -- complete')
    
                else:
                    print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run invalid address_name[dial_out_address_index] forbidden file name:', address_name_var)
                    self.dial_out_add_addr.setStyleSheet(dial_out_add_addr_stylesheet_red)
                    time.sleep(1)
            else:
                print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run invalid address_name[dial_out_address_index]:', address_name_var)
                self.dial_out_add_addr.setStyleSheet(dial_out_add_addr_stylesheet_red)
                time.sleep(1)

            self.dial_out_add_addr.setStyleSheet(button_stylesheet_0)
        except Exception as e:
            print(str(datetime.datetime.now()) + ' -- :', e)
            self.dial_out_add_addr.setStyleSheet(dial_out_add_addr_stylesheet_red)
            time.sleep(1)
            self.dial_out_add_addr.setStyleSheet(button_stylesheet_0)


class ConfigurationClass(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        print('-' * 200)
        print(str(datetime.datetime.now()) + ' [ thread started: ConfigurationClass(QThread).run(self) ]')
        global configuration_thread_key, configuration_thread_completed
        global DIAL_OUT_ADDRESSES

        global server_ip
        global server_port
        global server_address
        global server_addresses

        global address_name
        global address_ip
        global address_port
        global address_key
        global address_fingerprint

        if configuration_thread_key == 'ALL':
            server_addresses = []
            server_ip = []
            server_port = []
            print('-' * 200)
            print(str(datetime.datetime.now()) + ' ConfigurationClass(QThread): updating all values from configuration file...')

            with open('./config.txt', 'r') as fo:
                for line in fo:
                    line = line.strip()
                    line = line.split(' ')

                    if str(line[0]) == 'SERVER_ADDRESS':
                        if len(line) == 3:
                            server_ip.append(str(line[1]))
                            server_port.append(int((line[2])))
                            server_addresses.append(str(line[1]) + ' ' + str(line[2]))
                            print(str(datetime.datetime.now()) + ' server_ip:', str(line[1]), 'server_port:', str(line[2]))
            fo.close()
            print('-' * 200)
            print(str(datetime.datetime.now()) + ' ConfigurationClass(QThread): updating all values from communicator address book...')

            DIAL_OUT_ADDRESSES = []

            with open('./communicator_address_book.txt', 'r') as fo:
                for line in fo:
                    line = line.strip()

                    if line.startswith('DATA'):
                        DIAL_OUT_ADDRESSES.append(line)

            for _ in DIAL_OUT_ADDRESSES:

                # ToDo --> Sanitize Strings and check len(dial_out_address_split) before calling index ints

                # Split address
                dial_out_address_split = _.split(' ')
                print(str(datetime.datetime.now()) + ' dial_out_address_split:', dial_out_address_split)

                if len(dial_out_address_split) == 6:

                    # Name
                    print(str(datetime.datetime.now()) + ' setting dial out name:', dial_out_address_split[1])
                    address_name.append(dial_out_address_split[1])

                    # IP
                    print(str(datetime.datetime.now()) + ' setting dial out ip:', dial_out_address_split[2])
                    address_ip.append(dial_out_address_split[2])

                    # Port
                    print(str(datetime.datetime.now()) + ' setting dial out port:', dial_out_address_split[3])
                    address_port.append(int(dial_out_address_split[3]))

                    # Key
                    print(str(datetime.datetime.now()) + ' address_key:', dial_out_address_split[4])
                    address_key.append(bytes(dial_out_address_split[4], 'utf-8'))

                    # Fingerprint
                    fingerprint_file = dial_out_address_split[5]
                    print(str(datetime.datetime.now()) + ' reading fingerprint_file:', fingerprint_file)
                    address_fingerprint_string = ''
                    if os.path.exists(fingerprint_file):
                        with open(fingerprint_file, 'r') as fingerprint_fo:
                            for line in fingerprint_fo:
                                address_fingerprint_string = address_fingerprint_string + line
                                print(line.strip())
                        fingerprint_fo.close()
                        address_fingerprint.append(bytes(address_fingerprint_string, 'utf-8'))

        configuration_thread_completed = True


class AESCipher:

    def __init__(self, KEY):
        self.key = KEY

    def encrypt(self, raw):
        print(str(datetime.datetime.now()) + ' -- AESCipher: encrypting')
        try:
            raw = pad(raw)
            iv = Random.new().read(AES.block_size)
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return base64.b64encode(iv + cipher.encrypt(raw))

        except Exception as e:
            print('AESCipher.encrypt:', e)

    def decrypt(self, enc):
        print(str(datetime.datetime.now()) + ' -- AESCipher: decrypting')
        try:
            enc = base64.b64decode(enc)
            iv = enc[:16]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return unpad(cipher.decrypt(enc[16:])).decode('utf-8')

        except Exception as e:
            print('AESCipher.decrypt:', e)


class DialOutClass(QThread):
    def __init__(self, dial_out_title, dial_out_com1, dial_out_message_send, dial_out_message):
        QThread.__init__(self)
        global address_name, address_ip, address_port, address_key, address_fingerprint

        self.dial_out_title = dial_out_title
        self.dial_out_com1 = dial_out_com1
        self.dial_out_message_send = dial_out_message_send
        self.dial_out_message = dial_out_message

        self.HOST_SEND = ''
        self.PORT_SEND = ''
        self.KEY = ''
        self.FINGERPRINT = ''

        self.message_snd = ''

    def run(self):
        print('-' * 200)
        print(str(datetime.datetime.now()) + ' [ thread started: DialOutClass(QThread).run(self) ]')
        global dial_out_thread_key

        self.HOST_SEND = address_ip[dial_out_address_index]
        self.PORT_SEND = address_port[dial_out_address_index]
        self.KEY = address_key[dial_out_address_index]
        self.FINGERPRINT = address_fingerprint[dial_out_address_index]

        self.message_snd = ''

        if dial_out_thread_key == 'COM1':
            self.message_snd = 'COM1'
            self.message_send()

        elif dial_out_thread_key == 'MESSAGE':
            self.message_snd = str(self.dial_out_message.text())
            self.message_send()

        else:
            print(str(datetime.datetime.now()) + ' -- DialOutClass.run: dial_out_thread_key has no key')

    def message_send(self):
        global SOCKET_DIAL_OUT
        global dial_out_dial_out_cipher_bool
        global dial_out_thread_key

        dial_out_thread_key = ''
        print('-' * 200)
        print(str(datetime.datetime.now()) + f" -- DialOutClass.COM1 outgoing to: {self.HOST_SEND} : {self.PORT_SEND}")

        try:
            data_response = ''
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SOCKET_DIAL_OUT:
                SOCKET_DIAL_OUT.connect((self.HOST_SEND, self.PORT_SEND))

                if dial_out_dial_out_cipher_bool is True:
                    print(str(datetime.datetime.now()) + ' -- DialOutClass.COM1: handing message to AESCipher')
                    cipher = AESCipher(self.KEY)
                    ciphertext = cipher.encrypt(str(self.FINGERPRINT) + self.message_snd)
                    print(str(datetime.datetime.now()) + ' -- DialOutClass.COM1 ciphertext:', str(ciphertext))
                    messages.append('[' + str(datetime.datetime.now()) + '] [SENDING] [' + str(self.HOST_SEND) + ':' + str(self.PORT_SEND) + '] [ENCRYPTED] ' + str(ciphertext))
                else:
                    ciphertext = bytes(self.message_snd, 'utf-8')
                    messages.append('[' + str(datetime.datetime.now()) + '] [SENDING] [' + str(self.HOST_SEND) + ':' + str(self.PORT_SEND) + '] [UNENCRYPTED] ' + str(ciphertext))

                self.dial_out_message.setText('')

                print(str(datetime.datetime.now()) + ' -- DialOutClass.COM1: attempting to send ciphertext')

                SOCKET_DIAL_OUT.send(ciphertext)
                SOCKET_DIAL_OUT.settimeout(1)

                print(str(datetime.datetime.now()) + ' -- DialOutClass.COM1: waiting for response from recipient')

                try:
                    data_response = SOCKET_DIAL_OUT.recv(2048)
                except Exception as e:
                    print(str(datetime.datetime.now()) + ' -- DialOutClass.COM1 failed:', e)
                    self.dial_out_com1.setIcon(QIcon("./resources/image/cell_tower_FILL1_wght200_GRAD200_opsz40_RED.png"))

            if data_response == ciphertext:
                if self.message_snd == 'COM1':
                    print(str(datetime.datetime.now()) + ' -- DialOutClass.COM1 response from recipient equals ciphertext:', data_response)
                    self.dial_out_com1.setIcon(QIcon("./resources/image/cell_tower_FILL1_wght200_GRAD200_opsz40_GREEN.png"))
                    time.sleep(1)
                    self.dial_out_com1.setIcon(QIcon("./resources/image/cell_tower_FILL1_wght200_GRAD200_opsz40_WHITE.png"))
                else:
                    print(str(datetime.datetime.now()) + ' -- DialOutClass.COM1 response from recipient equals ciphertext:', data_response)
                    self.dial_out_message_send.setIcon(QIcon("./resources/image/send_FILL1_wght100_GRAD-25_opsz40_GREEN.png"))
                    time.sleep(1)
                    self.dial_out_message_send.setIcon(QIcon("./resources/image/send_FILL1_wght100_GRAD-25_opsz40_WHITE.png"))
                global_self.setFocus()

        except Exception as e:

            if self.message_snd == 'COM1':
                print(str(datetime.datetime.now()) + ' -- DialOutClass.COM1 failed:', e)
                self.dial_out_com1.setIcon(QIcon("./resources/image/cell_tower_FILL1_wght200_GRAD200_opsz40_RED.png"))
                time.sleep(1)
                self.dial_out_com1.setIcon(QIcon("./resources/image/cell_tower_FILL1_wght200_GRAD200_opsz40_WHITE.png"))
            else:
                print(str(datetime.datetime.now()) + ' -- DialOutClass.COM1 failed:', e)
                self.dial_out_message_send.setIcon(QIcon("./resources/image/send_FILL1_wght100_GRAD-25_opsz40_RED.png"))
                time.sleep(1)
                self.dial_out_message_send.setIcon(QIcon("./resources/image/send_FILL1_wght100_GRAD-25_opsz40_WHITE.png"))
            global_self.setFocus()

    def stop(self):
        global SOCKET_DIAL_OUT
        print('-' * 200)
        print(str(datetime.datetime.now()) + ' [ thread terminating: DialOutClass(QThread).run(self) ]')
        try:
            SOCKET_DIAL_OUT.close()
        except Exception as e:
            print(str(datetime.datetime.now()) + ' -- DialOutClass.stop failed:', e)
        global_self.setFocus()
        self.terminate()


class ServerDataHandlerClass(QThread):
    def __init__(self, server_title, server_com1, server_notify_cipher, server_notify_alien):
        QThread.__init__(self)
        self.server_com1 = server_com1
        self.server_title = server_title
        self.server_notify_cipher = server_notify_cipher
        self.server_notify_alien = server_notify_alien
        self.server_data_0 = []
        self.data = ''
        self.notification_key = ''

    def server_logger(self):
        if not os.path.exists(server_log):
            open(server_log, 'w').close()
        with open(server_log, 'a') as fo:
            fo.write(self.data + '\n')
        fo.close()

    def notification(self):
        print(str(datetime.datetime.now()) + ' -- ServerDataHandlerClass.notification: attempting communicator notification')

        self.server_com1.setIcon(QIcon("./resources/image/public_FILL1_wght100_GRAD200_opsz40.png"))

        if self.notification_key == 'green':
            self.server_com1.setIcon(QIcon("./resources/image/public_FILL1_wght100_GRAD200_opsz40_GREEN.png"))
        elif self.notification_key == 'amber':
            self.server_com1.setIcon(QIcon("./resources/image/public_FILL1_wght100_GRAD200_opsz40_AMBER.png"))

        url = QUrl.fromLocalFile("./resources/audio/communicator_0.wav")
        content = QMediaContent(url)
        player = QMediaPlayer()
        player.setMedia(content)
        player.setVolume(100)
        player.play()
        time.sleep(1)

        self.server_com1.setIcon(QIcon("./resources/image/public_FILL1_wght100_GRAD200_opsz40_WHITE.png"))

    def run(self):
        print('-' * 200)
        self.data = str(datetime.datetime.now()) + ' -- ServerDataHandlerClass.run: plugged in'
        print(self.data)
        global server_data
        global address_key
        global messages
        global address_server_data
        global cipher_message_count
        global alien_message_count

        while True:
            try:
                self.server_data_0 = server_data
                i_0 = 0
                for self.server_data_0s in self.server_data_0:
                    try:
                        ciphertext = self.server_data_0[i_0]
                        addr_data = address_server_data[i_0]

                        # remove currently iterated over item from server_data to keep the list low and performance high
                        server_data.remove(ciphertext)
                        address_server_data.remove(addr_data)

                        decrypted = ''
                        decrypted_message = ''
                        print(str(datetime.datetime.now()) + ' -- ServerDataHandlerClass.run: attempting to decrypt message')

                        # Communicator Standard Communication fingerprint is 1024 bytes so attempt decryption of any message larger than 1024 bytes
                        if len(ciphertext) > 1024:

                            # Use Keys in address book to attempt decryption (dictionary attack the message)
                            i_1 = 0
                            for _ in address_key:
                                print(str(datetime.datetime.now()) + ' -- ServerDataHandlerClass.run trying key:', _)
                                try:
                                    print(str(datetime.datetime.now()) + ' -- ServerDataHandlerClass.run: handing message to AESCipher')
                                    cipher = AESCipher(_)
                                    decrypted = cipher.decrypt(ciphertext)
                                except Exception as e:
                                    print(str(datetime.datetime.now()) + ' -- ServerDataHandlerClass.run (address_key loop): ' + str(e))
                                    break

                                # If decrypted then display the name associated with the key else try next key
                                if decrypted:
                                    print(str(datetime.datetime.now()) + ' -- ServerDataHandlerClass.run: successfully decrypted message')
                                    print(str(datetime.datetime.now()) + ' -- ServerDataHandlerClass.run searching incoming message for fingerprint associated with:', address_name[i_1])
                                    if decrypted.startswith(str(address_fingerprint[i_1])):
                                        print(str(datetime.datetime.now()) + ' -- ServerDataHandlerClass.run fingerprint: validated as', address_name[i_1])
                                        decrypted_message = decrypted.replace(str(address_fingerprint[i_1]), '')
                                        messages.append('[' + str(datetime.datetime.now()) + '] [' + str(addr_data) + '] [DECIPHER] [' + address_name[i_1] + '] ' + decrypted_message)
                                        print(str(datetime.datetime.now()) + ' -- ServerDataHandlerClass.run decrypted_message:', decrypted_message)

                                        if not cipher_message_count == '999+':
                                            if cipher_message_count < 999:
                                                cipher_message_count += 1
                                            else:
                                                cipher_message_count = str('999+')
                                        self.server_notify_cipher.setText(str(cipher_message_count))

                                        break
                                    else:
                                        print(str(datetime.datetime.now()) + ' -- ServerDataHandlerClass.run fingerprint: missing or invalid')
                                else:
                                    print(str(datetime.datetime.now()) + ' -- ServerDataHandlerClass.run decrypt: empty (try another key)')
                                i_1 += 1

                        # Display Server incoming message's
                        if len(decrypted_message) > 0:
                            self.data = str(datetime.datetime.now()) + ' -- ServerDataHandlerClass.run decrypted message: ' + str(decrypted_message)
                            self.server_logger()
                            self.notification_key = 'green'
                            self.notification()
                            global_self.setFocus()
                        else:
                            self.data = str(datetime.datetime.now()) + ' -- ServerDataHandlerClass.run message is not encrypted using keys in address book: ' + str(ciphertext)
                            print(self.data)
                            self.server_logger()
                            if str(ciphertext).startswith("b'"):
                                ciphertext = str(ciphertext).replace("b'", '')
                                if str(ciphertext).endswith("'"):
                                    ciphertext = ciphertext[:len(ciphertext)-1]
                            messages.append('[' + str(datetime.datetime.now()) + '] [' + str(addr_data) + '] [ALIEN] ' + ciphertext)

                            if not alien_message_count == '999+':
                                if alien_message_count < 999:
                                    alien_message_count += 1
                                else:
                                    alien_message_count = str('999+')
                            self.server_notify_alien.setText(str(alien_message_count))

                            self.notification_key = 'amber'
                            self.notification()
                            global_self.setFocus()
                        i_0 += 1

                    except Exception as e:
                        print(str(datetime.datetime.now()) + ' -- ServerDataHandlerClass.run (body_0): ' + str(e))
                        i_0 += 1
            except Exception as e:
                print(str(datetime.datetime.now()) + ' -- ServerDataHandlerClass.run (main_exception): ' + str(e))


class ServerClass(QThread):
    def __init__(self, server_title, server_com1, server_status_label):
        QThread.__init__(self)
        self.server_com1 = server_com1
        self.server_title = server_title
        self.server_status_label = server_status_label
        self.data = ''
        self.SERVER_HOST = ''
        self.SERVER_PORT = ''

    def run(self):

        global server_ip
        global server_port
        global server_address_index

        print(server_ip)
        print(server_port)

        self.SERVER_HOST = server_ip[server_address_index]
        self.SERVER_PORT = int(server_port[server_address_index])

        print('-' * 200)
        self.data = str(datetime.datetime.now()) + ' -- ServerClass.run: public server started'
        print(self.data)
        self.server_logger()

        global server_thread_key
        while True:
            if server_thread_key == 'listen':
                try:
                    self.listen()
                except Exception as e:
                    print(str(datetime.datetime.now()) + ' -- ServerClass.run failed:', e)

    def server_logger(self):
        if not os.path.exists(server_log):
            open(server_log, 'w').close()
        with open(server_log, 'a') as fo:
            fo.write(self.data + '\n')
        fo.close()

    def listen(self):
        global server_ip
        global server_port
        global SOCKET_SERVER
        global DIAL_OUT_ADDRESSES
        global server_data
        global wild_addresses_ip
        global address_server_data

        self.server_status_label.setText('SERVER STATUS: ONLINE')

        print('-' * 200)
        print(str(datetime.datetime.now()) + ' -- ServerClass.listen SERVER_HOST:', self.SERVER_HOST)
        print(str(datetime.datetime.now()) + ' -- ServerClass.listen SERVER_PORT:', self.SERVER_PORT)
        print(str(datetime.datetime.now()) + ' -- ServerClass.listen SERVER: attempting to listen')

        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SOCKET_SERVER:
                    SOCKET_SERVER.bind((self.SERVER_HOST, self.SERVER_PORT))
                    SOCKET_SERVER.listen()
                    conn, addr = SOCKET_SERVER.accept()
                    wild_address_ip = str(addr[0])
                    wild_address_port = str(addr[1])
                    if wild_address_ip not in address_ip:
                        print(str(datetime.datetime.now()) + ' -- ServerClass.listen incoming wild address:', wild_address_ip, str(wild_address_port))
                        wild_addresses_ip.append(str(wild_address_ip + ' ' + wild_address_port))
                    with conn:
                        print('-' * 200)
                        self.data = str(datetime.datetime.now()) + ' -- ServerClass.listen incoming connection: ' + str(addr)
                        messages.append('[' + str(datetime.datetime.now()) + '] [INCOMING CONNECTION] [' + str(addr[0]) + ':' + str(addr[1]) + ']')
                        print(self.data)
                        self.server_logger()
                        while True:
                            try:
                                server_data_0 = conn.recv(2048)
                                if not server_data_0:
                                    break

                                # ToDo --> This may make the data_handler_thread infinitely slower so be sure to clear this list periodically and safely without disrupting the data_handler_thread
                                # dump server_data_0 into a stack for the server_data_handler
                                server_data.append(server_data_0)
                                address_server_data.append(str(addr[0]) + ' ' + str(addr[1]))

                                # show connection received data
                                self.data = str(datetime.datetime.now()) + ' -- ServerClass.listen connection received server_data: ' + str(addr) + ' server_data: ' + str(server_data_0)
                                print(self.data)
                                self.server_logger()

                                # ToDo --> SECURITY RISK: Only send delivery confirmation conditionally! also change the delivery message
                                # send delivery confirmation message
                                print(str(datetime.datetime.now()) + ' -- ServerClass.listen: sending delivery confirmation message to:' + str(conn))
                                conn.sendall(server_data_0)

                            except Exception as e:
                                print(str(datetime.datetime.now()) + ' ' + str(e))
                                messages.append('[' + str(datetime.datetime.now()) + '] ' + str(e))
                                break

            except Exception as e:
                print(str(datetime.datetime.now()) + ' -- ServerClass.listen failed:', e)
                messages.append('[' + str(datetime.datetime.now()) + '] ' + str(e))
                self.server_status_label.setText('SERVER STATUS: OFFLINE')
                global_self.setFocus()

    def stop(self):
        global SOCKET_SERVER
        print('-' * 200)
        self.data = str(datetime.datetime.now()) + ' -- ServerClass.stop public server terminating'
        print(self.data)
        self.server_logger()
        try:
            SOCKET_SERVER.close()
        except Exception as e:
            print(str(datetime.datetime.now()) + ' -- ServerClass.stop failed:', e)
        self.server_status_label.setText('SERVER STATUS: OFFLINE')
        global_self.setFocus()
        self.terminate()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())