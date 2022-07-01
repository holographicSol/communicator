"""
Written by Benjamin Jack Cullen aka Holographic_Sol
"""

import os
import sys
import time
import datetime
import socket
from win32api import GetSystemMetrics
from PyQt5.QtCore import Qt, QThread, QSize, QTimer
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5 import QtCore
from Crypto.Cipher import AES
import base64
from Crypto import Random
import random
import string
import unicodedata


def NFD(text):
    return unicodedata.normalize('NFD', text)


def canonical_caseless(text):
    return NFD(NFD(text).casefold())


# Addresses
server_address = []
client_address = []
server_address_index = 0
client_address_index = 0

address_save_mode = 'basic'

# Socket Instances
SOCKET_DIAL_OUT = []
SOCKET_SERVER = []

# Soft Blocking Variables
x_time = round(time.time() * 1000)
z_time = []
prev_addr = []
soft_block_ip = []
violation_count = []

# textbox_0_Messages
server_messages = []
textbox_0_messages = []
server_address_messages = []
internal_messages = []
cipher_message_count = 0
alien_message_count = 0
soft_block_ip_count = 0

# Files
server_log = './log/server_log.txt'
dial_out_log = './log/dial_out_log.txt'

# Boolean
dial_out_dial_out_cipher_bool = True
configuration_thread_completed = False
write_server_configuration_engaged = False
write_client_configuration_engaged = False
mute_server_notify_alien_bool = False
mute_server_notify_cipher_bool = False

# Threads
configuration_thread = []

title_stylesheet_default = """QLabel{background-color: rgb(10, 10, 10);
                       color: rgb(200, 200, 200);
                       border-bottom:2px solid rgb(5, 5, 5);
                       border-right:2px solid rgb(5, 5, 5);
                       border-top:2px solid rgb(5, 5, 5);
                       border-left:2px solid rgb(5, 5, 5);}"""

button_stylesheet_default = """QPushButton{background-color: rgb(10, 10, 10);
                       color: rgb(200, 200, 200);
                       border-bottom:2px solid rgb(5, 5, 5);
                       border-right:2px solid rgb(5, 5, 5);
                       border-top:2px solid rgb(5, 5, 5);
                       border-left:2px solid rgb(5, 5, 5);}"""

button_stylesheet_background_matching = """QPushButton{background-color: rgb(0, 0, 0);
                       color: rgb(200, 200, 200);
                       border-bottom:0px solid rgb(5, 5, 5);
                       border-right:0px solid rgb(5, 5, 5);
                       border-top:0px solid rgb(5, 5, 5);
                       border-left:0px solid rgb(5, 5, 5);}"""

button_stylesheet_amber_text = """QPushButton{background-color: rgb(10, 10, 10);
                       color: rgb(200, 100, 0);
                       border-bottom:2px solid rgb(5, 5, 5);
                       border-right:2px solid rgb(5, 5, 5);
                       border-top:2px solid rgb(5, 5, 5);
                       border-left:2px solid rgb(5, 5, 5);}"""

button_stylesheet_white_text = """QPushButton{background-color: rgb(10, 10, 10);
                       color: rgb(255, 255, 255);
                       border-bottom:2px solid rgb(5, 5, 5);
                       border-right:2px solid rgb(5, 5, 5);
                       border-top:2px solid rgb(5, 5, 5);
                       border-left:2px solid rgb(5, 5, 5);}"""

button_stylesheet_red_text = """QPushButton{background-color: rgb(10, 10, 10);
                       color: rgb(200, 0, 0);
                       border-bottom:2px solid rgb(5, 5, 5);
                       border-right:2px solid rgb(5, 5, 5);
                       border-top:2px solid rgb(5, 5, 5);
                       border-left:2px solid rgb(5, 5, 5);}"""

button_stylesheet_green_text = """QPushButton{background-color: rgb(10, 10, 10);
                       color: rgb(0, 255, 0);
                       border-bottom:2px solid rgb(5, 5, 5);
                       border-right:2px solid rgb(5, 5, 5);
                       border-top:2px solid rgb(5, 5, 5);
                       border-left:2px solid rgb(5, 5, 5);}"""

line_edit_stylesheet_white_text = """QLineEdit{background-color: rgb(10, 10, 10);
                       color: rgb(200, 200, 200);
                       border-bottom:2px solid rgb(5, 5, 5);
                       border-right:2px solid rgb(5, 5, 5);
                       border-top:2px solid rgb(5, 5, 5);
                       border-left:2px solid rgb(5, 5, 5);}"""

textbox_stylesheet_default = """QTextBrowser {background-color: rgb(10, 10, 10);
                selection-color: black;
                selection-background-color: rgb(0, 180, 0);
                color: rgb(200, 200, 200);
                border-bottom:2px solid rgb(5, 5, 5);
                border-right:2px solid rgb(5, 5, 5);
                border-top:2px solid rgb(5, 5, 5);
                border-left:2px solid rgb(5, 5, 5);}"""

global_self = []

# Initialize Notification Player_default In Memory
player_url_default = QUrl.fromLocalFile("./resources/audio/communicator_0.wav")
player_content_default = QMediaContent(player_url_default)
player_default = QMediaPlayer()
player_default.setMedia(player_content_default)
player_default.setVolume(100)


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        global global_self
        global server_address
        global client_address
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

        def send_message_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.send_message_function')
            global_self.setFocus()
            if self.dial_out_message.text() != '':
                if dial_out_thread.isRunning() is True:
                    dial_out_thread.stop()
                dial_out_thread.start()
            else:
                print(str(datetime.datetime.now()) + ' -- send_message_function: blocking empty message send')

        def client_remove_address():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.client_remove_addresss')
            global write_client_configuration_engaged
            global client_address
            global client_address_index

            if write_client_configuration_engaged is False:
                write_client_configuration_engaged = True

                if os.path.exists('./communicator_address_book.txt'):
                    fo_list = []
                    with open('./communicator_address_book.txt', 'r') as fo:
                        for line in fo:
                            line = line.strip()
                            line_split = line.split(' ')
                            if len(line_split) >= 1:
                                if line != '':
                                    if line_split[1] != client_address[client_address_index][0]:
                                        fo_list.append(line)
                    open('./communicator_address_book.tmp', 'w').close()
                    with open('./communicator_address_book.tmp', 'w') as fo:
                        for _ in fo_list:
                            fo.write(str(_) + '\n')
                    fo.close()
                    if os.path.exists('./communicator_address_book.tmp'):
                        os.replace('./communicator_address_book.tmp', './communicator_address_book.txt')
                    del client_address[client_address_index]
                    client_previous_address_function()

            write_client_configuration_engaged = False

        def client_save_address():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.client_save_address')
            global write_client_configuration_engaged
            global client_address
            global client_address_index
            global internal_messages
            global address_save_mode

            name_non_duplicate = True
            for _ in client_address:
                if _[0] == self.dial_out_name.text():
                    print('-- comparing:', _[0], ' --> ', self.dial_out_name.text())
                    name_non_duplicate = False
                    break

            if write_client_configuration_engaged is False and name_non_duplicate is True:
                write_client_configuration_engaged = True

                if self.dial_out_name.text() != '':
                    if self.dial_out_ip_port.text() != '':

                        fo_list = []
                        with open('./communicator_address_book.txt', 'r') as fo:
                            for line in fo:
                                line = line.strip()
                                if line != '':
                                    if not line.replace('DATA ', '') == str(
                                            client_address[client_address_index][0]) + ' ' + str(
                                            client_address[client_address_index][1]):
                                        fo_list.append(line)

                        # Use Save Mode
                        if address_save_mode == 'basic':
                            fo_list.append('DATA ' + self.dial_out_name.text() + ' ' + str(self.dial_out_ip_port.text() + ' x' + ' x'))
                            client_address.append([str(self.dial_out_name.text()), str(self.dial_out_ip_port.text().split(' ')[0]), int(self.dial_out_ip_port.text().split(' ')[1]), bytes('x', 'utf-8'), 'x'])
                            client_address_index = len(client_address)-1

                        with open('./communicator_address_book.txt', 'w') as fo:
                            for _ in fo_list:
                                fo.write(_ + '\n')
                        fo.close()
                        success_write = []
                        if os.path.exists('./communicator_address_book.txt'):
                            with open('./communicator_address_book.txt', 'r') as fo:
                                i = 0
                                for line in fo:
                                    line = line.strip()
                                    if not line.replace('DATA ', '') == fo_list[i]:
                                        success_write.append(False)
                    else:
                        print('-- ip and port should not be empty!')
                else:
                    print('-- name should not be empty!')

                # Save as
            write_client_configuration_engaged = False

        def server_prev_addr_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.server_prev_addr_function')
            global_self.setFocus()
            global server_address_index
            global server_address

            if len(server_address) > 0:
                if server_address_index == 0:
                    server_address_index = len(server_address) - 1
                else:
                    server_address_index = server_address_index - 1
                print(str(datetime.datetime.now()) + ' -- setting server_address_index:', server_address_index)
                self.server_ip_port.setText(server_address[server_address_index][0] + ' ' + str(server_address[server_address_index][1]))
            else:
                print(str(datetime.datetime.now()) + ' -- server_address unpopulated')
                self.server_ip_port.setText('')

        def server_next_addr_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.server_next_addr_function')
            global_self.setFocus()

            global server_address_index
            global server_address

            if len(server_address) > 0:
                if server_address_index == len(server_address) - 1:
                    server_address_index = 0
                else:
                    server_address_index += 1
                print(str(datetime.datetime.now()) + ' -- setting server_address_index:', server_address_index)
                self.server_ip_port.setText(server_address[server_address_index][0] + ' ' + str(server_address[server_address_index][1]))
            else:
                print(str(datetime.datetime.now()) + ' -- server_address unpopulated')
                self.server_ip_port.setText('')

        def client_previous_address_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.client_previous_address_function')
            global_self.setFocus()
            global client_address_index
            print(str(datetime.datetime.now()) + ' -- len(client_address):', len(client_address))
            if len(client_address) > 0:
                if client_address_index == 0:
                    client_address_index = len(client_address) - 1
                else:
                    client_address_index = client_address_index - 1
                print(str(datetime.datetime.now()) + ' -- client_address_index setting client_address_index:', client_address_index)
                self.dial_out_ip_port.setText(client_address[client_address_index][1] + ' ' + str(client_address[client_address_index][2]))
                self.dial_out_name.setText(str(client_address[client_address_index][0]))
                print(self.dial_out_ip_port.text())
            else:
                print(str(datetime.datetime.now()) + ' -- client_address unpopulated')
            # print(str(datetime.datetime.now()) + ' -- client_next_address_function client_address[client_address_index]:', str(client_address[client_address_index]))

        def client_next_address_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.client_next_address_function')
            global_self.setFocus()
            global client_address_index
            print(str(datetime.datetime.now()) + ' -- len(client_address):', len(client_address))
            if len(client_address) > 0:
                if client_address_index == len(client_address) - 1:
                    client_address_index = 0
                else:
                    client_address_index += 1
                print(str(datetime.datetime.now()) + ' -- client_address_index setting client_address_index:', client_address_index)
                self.dial_out_ip_port.setText(client_address[client_address_index][1] + ' ' + str(client_address[client_address_index][2]))
                self.dial_out_name.setText(str(client_address[client_address_index][0]))
            else:
                print(str(datetime.datetime.now()) + ' -- client_address unpopulated')
            # print(str(datetime.datetime.now()) + ' -- client_next_address_function client_address[client_address_index]:', str(client_address[client_address_index]))

        def server_line_edit_return_pressed():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.server_line_edit_return_pressed')
            global_self.setFocus()
            global server_address
            global server_address_index

            server_address_var = self.server_ip_port.text()
            bool_address_match = False

            for _ in server_address:
                if str(_[0] + ' ' + str(_[1])) == server_address_var:
                    bool_address_match = True

            if bool_address_match is False:
                print(str(datetime.datetime.now()) + ' -- new server address detected:', server_address_var)
                server_address.append([server_address_var.split(' ')[0], int(server_address_var.split(' ')[1])])
                server_address_index = len(server_address)-1
                print(str(datetime.datetime.now()) + ' -- changing server_address_index to:', server_address_index)

            else:
                print(str(datetime.datetime.now()) + ' -- server address already exists:', server_address_var)

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

        def soft_block_ip_notofication_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.soft_block_ip_notofication_function')
            global soft_block_ip_count
            global soft_block_ip
            soft_block_ip_count = 0
            self.soft_block_ip_notification.setText(str(soft_block_ip_count))
            soft_block_ip = []

        def mute_server_notify_alien_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.mute_server_notify_alien_function')
            global mute_server_notify_alien_bool
            if mute_server_notify_alien_bool is True:
                mute_server_notify_alien_bool = False
                self.mute_server_notify_alien.setIcon(QIcon("./resources/image/volume_up_FILL0_wght100_GRAD200_opsz20.png"))
                print(str(datetime.datetime.now()) + ' -- plugged in: App.mute_server_notify_alien_function setting mute:', mute_server_notify_alien_bool)
            elif mute_server_notify_alien_bool is False:
                mute_server_notify_alien_bool = True
                self.mute_server_notify_alien.setIcon(QIcon("./resources/image/volume_off_FILL0_wght100_GRAD200_opsz20.png"))
                print(str(datetime.datetime.now()) + ' -- plugged in: App.mute_server_notify_alien_function setting mute:', mute_server_notify_alien_bool)

        def mute_server_notify_cipher_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.mute_server_notify_cipher_function')
            global mute_server_notify_cipher_bool
            if mute_server_notify_cipher_bool is True:
                mute_server_notify_cipher_bool = False
                self.mute_server_notify_cipher.setIcon(QIcon("./resources/image/volume_up_FILL0_wght100_GRAD200_opsz20.png"))
                print(str(datetime.datetime.now()) + ' -- plugged in: App.mute_server_notify_alien_function setting mute:', mute_server_notify_cipher_bool)
            elif mute_server_notify_cipher_bool is False:
                mute_server_notify_cipher_bool = True
                self.mute_server_notify_cipher.setIcon(QIcon("./resources/image/volume_off_FILL0_wght100_GRAD200_opsz20.png"))
                print(str(datetime.datetime.now()) + ' -- plugged in: App.mute_server_notify_alien_function setting mute:', mute_server_notify_cipher_bool)

        def server_save_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.server_save_function')
            global write_server_configuration_engaged
            global server_address
            global server_address_index
            global internal_messages

            if write_server_configuration_engaged is False:
                write_server_configuration_engaged = True
                internal_messages.append('server_save')
                fo_list = []
                with open('./config.txt', 'r') as fo:
                    for line in fo:
                        line = line.strip()
                        if line != '':
                            if not line.replace('SERVER_ADDRESS ', '') == str(server_address[server_address_index][0]) + ' ' + str(server_address[server_address_index][1]):
                                fo_list.append(line)
                fo_list.append('SERVER_ADDRESS ' + str(self.server_ip_port.text()))
                with open('./config.txt', 'w') as fo:
                    for _ in fo_list:
                        fo.write(_ + '\n')
                fo.close()
                success_write = []
                if os.path.exists('./config.txt'):
                    with open('./config.txt', 'r') as fo:
                        i = 0
                        for line in fo:
                            line = line.strip()
                            if not line.replace('SERVER_ADDRESS ', '') == fo_list[i]:
                                success_write.append(False)
            write_server_configuration_engaged = False

        def server_delete_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.server_delete_function')
            global write_server_configuration_engaged
            global server_address
            global server_address_index

            if write_server_configuration_engaged is False:
                write_server_configuration_engaged = True

                if os.path.exists('./config.txt'):
                    fo_list = []
                    with open('./config.txt', 'r') as fo:
                        for line in fo:
                            line = line.strip()
                            if line != '':
                                if not line.replace('SERVER_ADDRESS ', '') == str(server_address[server_address_index][0]) + ' ' + str(server_address[server_address_index][1]):
                                    fo_list.append(line)
                    open('./config.tmp', 'w').close()
                    with open('./config.tmp', 'w') as fo:
                        for _ in fo_list:
                            fo.write(str(_) + '\n')
                    fo.close()
                    if os.path.exists('./config.tmp'):
                        os.replace('./config.tmp', './config.txt')
                    del server_address[server_address_index]
                    server_prev_addr_function()

                write_server_configuration_engaged = False

        def start_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.start_function')
            global_self.setFocus()
            if len(server_address) > 0:
                if server_thread.isRunning() is True:
                    server_thread.stop()
                server_thread.start()

        def stop_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.stop_function')
            global_self.setFocus()
            if server_thread.isRunning() is True:
                server_thread.stop()
            else:
                print('server: already stopped')

        def restart_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.restart_function')
            if server_thread.isRunning() is True:
                server_thread.stop()
            server_thread.start()

        # Variable should be set before running write_configuration function
        self.write_var = ''

        # Window Title
        self.title = "Communicator"
        self.setWindowTitle('Communicator')
        self.setWindowIcon(QIcon('./resources/image/icon.ico'))

        # Window Geometry
        self.width, self.height = 720, 402
        app_pos_w, app_pos_h = (GetSystemMetrics(0) / 2 - (self.width / 2)), (GetSystemMetrics(1) / 2 - (self.height / 2))
        self.left, self.top = int(app_pos_w), int(app_pos_h)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)

        # Window Colour
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

        # Object Geometry
        self.btn_4 = 4
        self.btn_8 = 8
        self.btn_20 = 20
        self.btn_40 = 40
        self.btn_60 = 60
        self.btn_80 = 80
        self.btn_140 = 140
        self.btn_240 = 240

        # QPushButton - Dial Out Set Encryption Boolean
        # self.dial_out_cipher_bool_btn = QPushButton(self)
        # self.dial_out_cipher_bool_btn.resize(self.btn_40 * 2 + 4, self.btn_40)
        # self.dial_out_cipher_bool_btn.move(self.btn_4 * 7 + self.btn_80 + self.btn_40 * 4 + self.btn_120, self.btn_8 * 2 + self.btn_40)
        # self.dial_out_cipher_bool_btn.setText('CIPHER')
        # self.dial_out_cipher_bool_btn.setFont(self.font_s7b)
        # self.dial_out_cipher_bool_btn.setStyleSheet(button_stylesheet_green_text)
        # self.dial_out_cipher_bool_btn.hide()

        self.dial_out_label = QLabel(self)
        self.dial_out_label.resize(self.width - 8, 20)
        self.dial_out_label.move(4, 280)
        self.dial_out_label.setFont(self.font_s7b)
        self.dial_out_label.setText('TRANSMIT')
        self.dial_out_label.setAlignment(Qt.AlignCenter)
        self.dial_out_label.setStyleSheet(title_stylesheet_default)

        # QLabel - Dial Out Message
        self.dial_out_message = QLineEdit(self)
        self.dial_out_message.resize(self.btn_240, self.btn_20)
        self.dial_out_message.move((self.width / 2) - (self.btn_240 / 2), 328)
        self.dial_out_message.setFont(self.font_s7b)
        self.dial_out_message.setText('')
        self.dial_out_message.setStyleSheet(line_edit_stylesheet_white_text)

        # QLabel - Dial Out Message Send
        self.dial_out_message_send = QPushButton(self)
        self.dial_out_message_send.resize(self.btn_60, self.btn_20)
        self.dial_out_message_send.move((self.width / 2) + (self.btn_240 / 2) + self.btn_4, 328)
        self.dial_out_message_send.setIcon(QIcon("./resources/image/send_FILL1_wght100_GRAD-25_opsz40_WHITE.png"))
        self.dial_out_message_send.setIconSize(QSize(self.btn_20, self.btn_20))
        self.dial_out_message_send.setStyleSheet(button_stylesheet_default)
        self.dial_out_message_send.clicked.connect(send_message_function)

        self.address_book_label = QLabel(self)
        self.address_book_label.resize(self.width - 8, 20)
        self.address_book_label.move(4, 140)
        self.address_book_label.setFont(self.font_s7b)
        self.address_book_label.setText('ADDRESS BOOK')
        self.address_book_label.setAlignment(Qt.AlignCenter)
        self.address_book_label.setStyleSheet(title_stylesheet_default)

        # QPushButton - Dial Out Name
        self.dial_out_name = QLineEdit(self)
        self.dial_out_name.resize(140, 20)
        self.dial_out_name.move((self.width / 2) - (self.btn_140 / 2), 188)
        self.dial_out_name.setFont(self.font_s7b)
        self.dial_out_name.setText('')
        self.dial_out_name.setStyleSheet(line_edit_stylesheet_white_text)
        self.dial_out_name.setAlignment(Qt.AlignCenter)

        # QLineEdit - Dial Out Address
        self.dial_out_ip_port = QLineEdit(self)
        self.dial_out_ip_port.resize(140, 20)
        self.dial_out_ip_port.move((self.width / 2) - (self.btn_140 / 2), 212)
        self.dial_out_ip_port.setFont(self.font_s7b)
        self.dial_out_ip_port.setText('')
        self.dial_out_ip_port.setStyleSheet(line_edit_stylesheet_white_text)
        self.dial_out_ip_port.setAlignment(Qt.AlignCenter)

        # QPushButton - Dial Out Previous Address
        self.dial_out_prev_addr = QPushButton(self)
        self.dial_out_prev_addr.resize(20, 20)
        self.dial_out_prev_addr.move((self.width / 2) - (self.btn_140 / 2) - self.btn_20 - self.btn_4, 212)
        self.dial_out_prev_addr.setIcon(QIcon("./resources/image/baseline_keyboard_arrow_left_white_18dp.png"))
        self.dial_out_prev_addr.setIconSize(QSize(20, 20))
        self.dial_out_prev_addr.setStyleSheet(button_stylesheet_default)
        self.dial_out_prev_addr.clicked.connect(client_previous_address_function)

        # QPushButton - Dial Out Next Address
        self.dial_out_next_addr = QPushButton(self)
        self.dial_out_next_addr.resize(20, 20)
        self.dial_out_next_addr.move((self.width / 2) + (self.btn_140 / 2) + self.btn_4, 212)
        self.dial_out_next_addr.setIcon(QIcon("./resources/image/baseline_keyboard_arrow_right_white_18dp.png"))
        self.dial_out_next_addr.setIconSize(QSize(20, 20))
        self.dial_out_next_addr.setStyleSheet(button_stylesheet_default)
        self.dial_out_next_addr.clicked.connect(client_next_address_function)

        # QPushButton - Dial Out Add Address
        self.dial_out_add_addr = QPushButton(self)
        self.dial_out_add_addr.resize(60, 20)
        self.dial_out_add_addr.move((self.width / 2) - (self.btn_140 / 2), 236)
        self.dial_out_add_addr.setFont(self.font_s7b)
        self.dial_out_add_addr.setText('SAVE')
        self.dial_out_add_addr.setStyleSheet(button_stylesheet_default)
        self.dial_out_add_addr.clicked.connect(client_save_address)

        # QPushButton - Dial Out Remove Address
        self.dial_out_rem_addr = QPushButton(self)
        self.dial_out_rem_addr.resize(60, 20)
        self.dial_out_rem_addr.move((self.width / 2) + 10, 236)
        self.dial_out_rem_addr.setFont(self.font_s7b)
        self.dial_out_rem_addr.setText('DELETE')
        self.dial_out_rem_addr.setStyleSheet(button_stylesheet_default)
        self.dial_out_rem_addr.clicked.connect(client_remove_address)

        # QLabel - Server Status
        self.server_status_label = QLabel(self)
        self.server_status_label.resize(self.width - 8, 20)
        self.server_status_label.move(4, 28)
        self.server_status_label.setFont(self.font_s7b)
        self.server_status_label.setText('SERVER STATUS:  OFFLINE')
        self.server_status_label.setAlignment(Qt.AlignCenter)
        self.server_status_label.setStyleSheet(title_stylesheet_default)

        # QPushButton - Server Start
        self.server_start = QPushButton(self)
        self.server_start.resize(60, int(self.btn_40 / 2))
        self.server_start.move(28, 52)
        self.server_start.setFont(self.font_s7b)
        self.server_start.setText('START')
        self.server_start.setStyleSheet(button_stylesheet_default)
        self.server_start.clicked.connect(start_function)

        # QPushButton - Server Stop
        self.server_stop = QPushButton(self)
        self.server_stop.resize(60, int(self.btn_40 / 2))
        self.server_stop.move(28, 76)
        self.server_stop.setFont(self.font_s7b)
        self.server_stop.setText('STOP')
        self.server_stop.setStyleSheet(button_stylesheet_default)
        self.server_stop.clicked.connect(stop_function)

        # QPushButton - Server Stop
        self.server_restart = QPushButton(self)
        self.server_restart.resize(60, int(self.btn_40 / 2))
        self.server_restart.move(28, 100)
        self.server_restart.setFont(self.font_s7b)
        self.server_restart.setText('RESTART')
        self.server_restart.setStyleSheet(button_stylesheet_default)
        self.server_restart.clicked.connect(restart_function)

        # QLineEdit - Server IP
        self.server_ip_port = QLineEdit(self)
        self.server_ip_port.resize(self.btn_140, 20)
        self.server_ip_port.move((self.width / 2) - (self.btn_140 / 2), 76)
        self.server_ip_port.returnPressed.connect(server_line_edit_return_pressed)
        self.server_ip_port.setFont(self.font_s7b)
        self.server_ip_port.setText('')
        self.server_ip_port.setStyleSheet(line_edit_stylesheet_white_text)
        self.server_ip_port.setAlignment(Qt.AlignCenter)

        # QPushButton - Server Previous Address
        self.server_prev_addr = QPushButton(self)
        self.server_prev_addr.resize(self.btn_20, 20)
        self.server_prev_addr.move((self.width / 2) - (self.btn_140 / 2) - self.btn_20 - self.btn_4, 76)
        self.server_prev_addr.setIcon(QIcon("./resources/image/baseline_keyboard_arrow_left_white_18dp.png"))
        self.server_prev_addr.setIconSize(QSize(20, 20))
        self.server_prev_addr.setStyleSheet(button_stylesheet_default)
        self.server_prev_addr.clicked.connect(server_prev_addr_function)

        # QPushButton - Server Out Next Address
        self.server_next_addr = QPushButton(self)
        self.server_next_addr.resize(20, 20)
        self.server_next_addr.move((self.width / 2) + (self.btn_140 / 2) + self.btn_4, 76)
        self.server_next_addr.setIcon(QIcon("./resources/image/baseline_keyboard_arrow_right_white_18dp.png"))
        self.server_next_addr.setIconSize(QSize(20, 20))
        self.server_next_addr.setStyleSheet(button_stylesheet_default)
        self.server_next_addr.clicked.connect(server_next_addr_function)

        # QPushButton - Dial Out Add Address
        self.server_add_addr = QPushButton(self)
        self.server_add_addr.resize(60, int(self.btn_40 / 2))
        self.server_add_addr.move((self.width / 2) - (self.btn_140 / 2), 100)
        self.server_add_addr.setFont(self.font_s7b)
        self.server_add_addr.setText('SAVE')
        self.server_add_addr.setStyleSheet(button_stylesheet_default)
        self.server_add_addr.clicked.connect(server_save_function)

        # QPushButton - Dial Out Remove Address
        self.server_rem_addr = QPushButton(self)
        self.server_rem_addr.resize(60, int(self.btn_40 / 2))
        self.server_rem_addr.move((self.width / 2) + 10, 100)
        self.server_rem_addr.setFont(self.font_s7b)
        self.server_rem_addr.setText('DELETE')
        self.server_rem_addr.setIconSize(QSize(14, 14))
        self.server_rem_addr.setStyleSheet(button_stylesheet_default)
        self.server_rem_addr.clicked.connect(server_delete_function)

        # QPushButton - Server Received Communication
        self.server_incoming = QPushButton(self)
        self.server_incoming.resize(68, 68)
        self.server_incoming.move(self.width - 72, 52)
        self.server_incoming.setIcon(QIcon("./resources/image/public_OFF_FILL0_wght100_GRAD-25_opsz48_WHITE.png"))
        self.server_incoming.setIconSize(QSize(48, 48))
        self.server_incoming.setStyleSheet(button_stylesheet_background_matching)

        # QPushButton - Soft Block Notification Count
        self.soft_block_ip_notification = QPushButton(self)
        self.soft_block_ip_notification.resize(60, 20)
        self.soft_block_ip_notification.move(self.width - 136, 100)
        self.soft_block_ip_notification.setText(str(soft_block_ip_count))
        self.soft_block_ip_notification.setStyleSheet(button_stylesheet_red_text)
        self.soft_block_ip_notification.clicked.connect(soft_block_ip_notofication_function)

        # QPushButton - Server Alien Message
        self.server_notify_alien = QPushButton(self)
        self.server_notify_alien.resize(60, int(self.btn_40 / 2))
        self.server_notify_alien.move(self.width - 136, 76)
        self.server_notify_alien.setStyleSheet(button_stylesheet_amber_text)
        self.server_notify_alien.setFont(self.font_s7b)
        self.server_notify_alien.setText(str(alien_message_count))
        self.server_notify_alien.clicked.connect(server_notify_alien_function)

        # QPushButton - Server Cipher Message Count
        self.server_notify_cipher = QPushButton(self)
        self.server_notify_cipher.resize(60, int(self.btn_40 / 2))
        self.server_notify_cipher.move(self.width - 136, 52)
        self.server_notify_cipher.setStyleSheet(button_stylesheet_white_text)
        self.server_notify_cipher.setFont(self.font_s7b)
        self.server_notify_cipher.setText(str(cipher_message_count))
        self.server_notify_cipher.clicked.connect(server_notify_cipher_function)

        # QPushButton - Server Cipher Message Toggle Mute
        self.mute_server_notify_cipher = QPushButton(self)
        self.mute_server_notify_cipher.resize(60, int(self.btn_40 / 2))
        self.mute_server_notify_cipher.move(self.width - 200, 52)
        self.mute_server_notify_cipher.setStyleSheet(button_stylesheet_white_text)
        self.mute_server_notify_cipher.setIcon(QIcon("./resources/image/volume_up_FILL0_wght100_GRAD200_opsz20.png"))
        self.mute_server_notify_cipher.setIconSize(QSize(14, 14))
        self.mute_server_notify_cipher.clicked.connect(mute_server_notify_cipher_function)

        # QPushButton - Server Alien Message Toggle Mute
        self.mute_server_notify_alien = QPushButton(self)
        self.mute_server_notify_alien.resize(60, int(self.btn_40 / 2))
        self.mute_server_notify_alien.move(self.width - 200, 76)
        self.mute_server_notify_alien.setStyleSheet(button_stylesheet_amber_text)
        self.mute_server_notify_alien.setIcon(QIcon("./resources/image/volume_up_FILL0_wght100_GRAD200_opsz20.png"))
        self.mute_server_notify_alien.setIconSize(QSize(14, 14))
        self.mute_server_notify_alien.clicked.connect(mute_server_notify_alien_function)

        # Thread - Public Server
        server_thread = ServerClass(self.server_incoming, self.server_status_label, self.soft_block_ip_notification)

        # Thread - ServerDataHandlerClass
        server_data_handler_class = ServerDataHandlerClass(self.server_incoming, self.server_notify_cipher, self.server_notify_alien)
        server_data_handler_class.start()

        # Thread - Dial_Out
        dial_out_thread = DialOutClass(self.dial_out_message_send, self.dial_out_message)

        # Thread - Configuration
        global configuration_thread
        configuration_thread_ = ConfigurationClass()
        configuration_thread.append(configuration_thread_)
        configuration_thread[0].start()

        # finger_print_gen_thread = FingerprintGeneration(self.dial_out_name, self.dial_out_ip_port, self.dial_out_add_addr)

        # Configuration Thread - Wait For Configuration Thread To Complete
        global configuration_thread_completed
        print(str(datetime.datetime.now()) + ' configuration_thread_completed:', configuration_thread_completed)
        while configuration_thread_completed is False:
            time.sleep(1)
        print(str(datetime.datetime.now()) + ' configuration_thread_completed:', configuration_thread_completed)

        if len(server_address) > 0:
            self.server_ip_port.setText(server_address[0][0] + ' ' + str(server_address[0][1]))

        if len(client_address) > 0:
            self.dial_out_name.setText(client_address[0][0])
            self.dial_out_ip_port.setText(client_address[0][1] + ' ' + str(client_address[0][2]))

        # QTextBrowser - Message Output
        self.tb_0 = QTextBrowser(self)
        self.tb_0.move(4, self.height - 60)
        self.tb_0.resize(self.width - 8, 60)
        self.tb_0.setObjectName("tb_0")
        self.tb_0.setFont(self.font_s7b)
        self.tb_0.setStyleSheet(textbox_stylesheet_default)
        self.tb_0.setLineWrapMode(QTextBrowser.NoWrap)
        self.tb_0.horizontalScrollBar().setValue(0)
        self.tb_0.hide()

        # QTimer - Used For Appending To tb_0 Using QtSlots
        self.timer_0 = QTimer(self)
        self.timer_0.setInterval(0)
        self.timer_0.timeout.connect(self.update_tb)
        self.jumpstart_1()

        # QTimer - Used For Internal Message System
        self.timer_1 = QTimer(self)
        self.timer_1.setInterval(0)
        self.timer_1.timeout.connect(self.internal_message_system)
        self.jumpstart_2()

        self.initUI()

    def initUI(self):
        self.show()

    def stop_timer_1(self):
        self.timer_0.stop()

    @QtCore.pyqtSlot()
    def jumpstart_1(self):
        self.timer_0.start()

    @QtCore.pyqtSlot()
    def update_tb(self):
        if textbox_0_messages:
            self.tb_0.append(textbox_0_messages[-1])
            textbox_0_messages.remove(textbox_0_messages[-1])

    @QtCore.pyqtSlot()
    def jumpstart_2(self):
        self.timer_1.start()

    @QtCore.pyqtSlot()
    def internal_message_system(self):
        if internal_messages:
            if internal_messages[-1] == 'server_save':
                print('internal_messages: server_save')
                internal_messages.remove(internal_messages[-1])

                # if os.path.exists('./config.txt'):

                    # if success_write is True:
                    #     self.server_add_addr.setStyleSheet(button_stylesheet_green_text)
                    # else:
                    #     self.server_add_addr.setStyleSheet(button_stylesheet_red_text)
                    # time.sleep(0.5)
                    # global write_server_configuration_engaged
                    # self.server_add_addr.setStyleSheet(button_stylesheet_default)
                    # write_server_configuration_engaged = False


class FingerprintGeneration(QThread):
    def __init__(self, dial_out_name, dial_out_ip_port, dial_out_add_addr):
        QThread.__init__(self)
        self.fingerprint_var = []
        self.dial_out_ip_port = dial_out_ip_port
        self.dial_out_name = dial_out_name
        self.dial_out_add_addr = dial_out_add_addr
        self.key_string = ''
        self.entry_address_book = ''
        self.new_full_dial_out_address = ''
        self.fingerprint_str = ''

    def update_values(self):
        global client_address_index
        global client_address
        global configuration_thread_completed

        configuration_thread_completed = False

        # Update config
        configuration_thread[0].start()

        while configuration_thread_completed is False:
            time.sleep(1)

        i = 0
        for _ in client_address:
            if _[0] == self.dial_out_name.text():
                client_address_index = i
            i += 1

    def randStr(self, chars=string.ascii_uppercase + string.digits, N=32):
        return ''.join(random.choice(chars) for _ in range(N))

    def iter_rand(self):
        self.key_string = self.randStr(chars=string.ascii_lowercase + string.ascii_uppercase + string.punctuation.replace("'", "f"))
        self.fingerprint_var.append(self.key_string)
        self.fingerprint_str = self.fingerprint_str + self.key_string

    def run(self):
        print('-' * 200)
        print(str(datetime.datetime.now()) + ' [ thread started: FingerprintGeneration(QThread).run(self) ]')
        global client_address_index
        global client_address
        global configuration_thread

        self.fingerprint_var = []

        try:

            self.dial_out_add_addr.setStyleSheet(button_stylesheet_amber_text)

            forbidden_fname = ['con', 'aux', 'nul', 'prn',
                               'com1', 'com2', 'com3', 'com4', 'com5', 'com6', 'com7', 'com8', 'com9',
                               'lpt1', 'lpt2', 'lpt3', 'lpt4', 'lpt5', 'lpt6', 'lpt7', 'lpt8', 'lpt9']

            address_name_var = str(self.dial_out_name.text()).replace('_', '')
            if str(address_name_var).isalnum():
                address_name_var = str(self.dial_out_name.text())
                if canonical_caseless(address_name_var) not in forbidden_fname:
                    print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run address_name[client_address_index]: is not in forbidden_fname')

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

                    self.new_full_dial_out_address = self.entry_address_book + ' ' + self.fingerprint_str
                    self.entry_address_book = self.entry_address_book + ' ' + finger_print_fname
                    client_address = self.entry_address_book
                    print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run full address book entry string:', self.entry_address_book)

                    # Write the fingerprint file
                    open(finger_print_fname, 'w').close()
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
                    address_name_match = False
                    for _ in client_address:
                        if _[0] == address_name_var:
                            address_name_match = True
                            break

                    if address_name_match is True:
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
                            with open('./communicator_address_book.tmp', 'w') as fo:
                                for _ in addr_var:
                                    print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run writing address book line:', _)
                                    fo.write('\n' + _ + '\n')
                            fo.close()
                            os.replace('./communicator_address_book.tmp', './communicator_address_book.txt')
                    else:
                        print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run appending new address book entry to address book')
                        with open('./communicator_address_book.txt', 'a') as fo:
                            fo.write('\n' + self.entry_address_book + '\n')
                        fo.close()
                    print('-' * 200)

                    print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run -- complete')

                    self.update_values()

                else:
                    print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run invalid address_name[client_address_index] forbidden file name:', address_name_var)
            else:
                print(str(datetime.datetime.now()) + ' -- FingerprintGeneration(QThread).run invalid address_name[client_address_index]:', address_name_var)

            time.sleep(1)
            self.dial_out_add_addr.setStyleSheet(button_stylesheet_default)

        except Exception as e:
            print(str(datetime.datetime.now()) + ' -- :', e)


class ConfigurationClass(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        print('-' * 200)
        print(str(datetime.datetime.now()) + ' [ thread started: ConfigurationClass(QThread).run(self) ]')
        global configuration_thread_completed
        global server_address
        global client_address

        print('-' * 200)
        print(str(datetime.datetime.now()) + ' ConfigurationClass(QThread): updating all values from configuration file...')

        # Read And Set Server Configuration
        server_address = []
        with open('./config.txt', 'r') as fo:
            for line in fo:
                line = line.strip()
                print('configuration server:', line)
                line = line.split(' ')
                if str(line[0]) == 'SERVER_ADDRESS':
                    if len(line) == 3:
                        server_address.append([str(line[1]), int(line[2])])
                        print(str(datetime.datetime.now()) + ' ConfigurationClass(QThread) adding server_address: ' + str(server_address[-1]))
        fo.close()

        print('-' * 200)
        print(str(datetime.datetime.now()) + ' ConfigurationClass(QThread): updating all values from communicator address book...')

        # Read And Set Client Configuration
        client_address = []
        with open('./communicator_address_book.txt', 'r') as fo:
            for line in fo:
                line = line.strip()
                line = line.split(' ')
                if str(line[0]) == 'DATA':
                    if len(line) == 6:
                        client_address.append([str(line[1]), str(line[2]), int(line[3]), bytes(line[4], 'utf-8'), line[5]])
                        print(client_address[-1])

        for _ in client_address:
            if os.path.exists(_[-1]):
                address_fingerprint_string = ''
                with open(_[-1], 'r') as fo:
                    for line in fo:
                        line = line.strip()
                        address_fingerprint_string = address_fingerprint_string + line
                fo.close()
                _[-1] = address_fingerprint_string
                print(_)

        configuration_thread_completed = True


class AESCipher:

    def __init__(self, KEY):
        self.key = KEY

        self.BS = 16
        self.pad = lambda s: bytes(s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS), 'utf-8')
        self.unpad = lambda s: s[0:-ord(s[-1:])]

    def encrypt(self, raw):
        print(str(datetime.datetime.now()) + ' -- AESCipher encrypting using key:', self.key)
        try:
            raw = self.pad(raw)
            iv = Random.new().read(AES.block_size)
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return base64.b64encode(iv + cipher.encrypt(raw))

        except Exception as e:
            print('AESCipher.encrypt:', e)

    def decrypt(self, enc):
        print(str(datetime.datetime.now()) + ' -- AESCipher decrypting using key:', self.key)
        try:
            enc = base64.b64decode(enc)
            iv = enc[:16]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return self.unpad(cipher.decrypt(enc[16:])).decode('utf-8')

        except Exception as e:
            print('AESCipher.decrypt:', e)


class DialOutClass(QThread):
    def __init__(self, dial_out_message_send, dial_out_message):
        QThread.__init__(self)

        self.dial_out_message_send = dial_out_message_send
        self.dial_out_message = dial_out_message

        self.HOST_SEND = ''
        self.PORT_SEND = ''
        self.KEY = ''
        self.FINGERPRINT = ''
        self.MESSAGE_CONTENT = ''

    def run(self):
        print('-' * 200)
        print(str(datetime.datetime.now()) + ' [ thread started: DialOutClass(QThread).run(self) ]')
        global client_address
        global client_address_index

        print(str(datetime.datetime.now()) + ' -- DialOutClass.run client_address_index:', client_address_index)

        self.HOST_SEND = client_address[client_address_index][1]
        self.PORT_SEND = client_address[client_address_index][2]
        self.KEY = client_address[client_address_index][3]
        self.FINGERPRINT = client_address[client_address_index][4]
        self.MESSAGE_CONTENT = str(self.dial_out_message.text())

        self.message_send()

    def dial_out_logger(self):
        if not os.path.exists(dial_out_log):
            open(dial_out_log, 'w').close()
        with open(dial_out_log, 'a') as fo:
            fo.write('\n' + self.data + '\n')
        fo.close()

    def message_send(self):
        global SOCKET_DIAL_OUT
        global dial_out_dial_out_cipher_bool

        print('-' * 200)
        print(str(datetime.datetime.now()) + f" -- DialOutClass.message_send outgoing to: {self.HOST_SEND} : {self.PORT_SEND}")

        try:
            data_response = ''
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SOCKET_DIAL_OUT:
                SOCKET_DIAL_OUT.connect((self.HOST_SEND, self.PORT_SEND))

                # dial_out_dial_out_cipher_bool = False
                if bytes('x', 'utf-8') == client_address[client_address_index][3]:
                    dial_out_dial_out_cipher_bool = False
                else:
                    dial_out_dial_out_cipher_bool = True

                print('dial_out_dial_out_cipher_bool:', dial_out_dial_out_cipher_bool)

                if dial_out_dial_out_cipher_bool is True:
                    print(str(datetime.datetime.now()) + ' -- DialOutClass.message_send: handing message to AESCipher')
                    print(str(datetime.datetime.now()) + ' -- DialOutClass.message_send using KEY:', self.KEY)
                    print(str(datetime.datetime.now()) + ' -- DialOutClass.message_send using FINGERPRINT:', self.FINGERPRINT)
                    cipher = AESCipher(self.KEY)
                    ciphertext = cipher.encrypt(str(self.FINGERPRINT) + self.MESSAGE_CONTENT)
                    print(str(datetime.datetime.now()) + ' -- DialOutClass.message_send ciphertext:', str(ciphertext))
                    textbox_0_messages.append('[' + str(datetime.datetime.now()) + '] [SENDING ENCRYPTED] [' + str(self.HOST_SEND) + ':' + str(self.PORT_SEND) + ']')
                else:
                    ciphertext = bytes(self.MESSAGE_CONTENT, 'utf-8')
                    textbox_0_messages.append('[' + str(datetime.datetime.now()) + '] [SENDING UNENCRYPTED] [' + str(self.HOST_SEND) + ':' + str(self.PORT_SEND) + ']')

                print(str(datetime.datetime.now()) + ' -- DialOutClass.message_send: attempting to send ciphertext')

                SOCKET_DIAL_OUT.send(ciphertext)
                SOCKET_DIAL_OUT.settimeout(1)

                print(str(datetime.datetime.now()) + ' -- DialOutClass.message_send: waiting for response from recipient')

                try:
                    data_response = SOCKET_DIAL_OUT.recv(2048)
                except Exception as e:
                    print(str(datetime.datetime.now()) + ' -- DialOutClass.message_send failed:', e)
                    self.dial_out_line_test.setIcon(QIcon("./resources/image/cell_tower_FILL1_wght200_GRAD200_opsz40_RED.png"))
                    self.data = '[' + str(datetime.datetime.now()) + '] [SENDING FAILED] [' + str(self.HOST_SEND) + ':' + str(self.PORT_SEND) + ']'
                    textbox_0_messages.append(self.data)
                    self.dial_out_logger()

            if data_response == ciphertext:
                self.dial_out_message.setText('')
                self.data = '[' + str(datetime.datetime.now()) + '] [DELIVERY CONFIRMATION] [' + str(self.HOST_SEND) + ':' + str(self.PORT_SEND) + ']'
                textbox_0_messages.append(self.data)

                print(str(datetime.datetime.now()) + ' -- DialOutClass.message_send response from recipient equals ciphertext:', data_response)
                self.dial_out_message_send.setIcon(QIcon("./resources/image/send_FILL1_wght100_GRAD-25_opsz40_GREEN.png"))
                time.sleep(1)
                self.dial_out_message_send.setIcon(QIcon("./resources/image/send_FILL1_wght100_GRAD-25_opsz40_WHITE.png"))

            else:
                self.dial_out_message.setText('')
                self.data = '[' + str(datetime.datetime.now()) + '] [WARNING] [MESSAGE RECEIVED DOES NOT MATCH MESSAGE SENT] [' + str(self.HOST_SEND) + ':' + str(self.PORT_SEND) + '] ' + str(data_response)
                print(self.data)
                textbox_0_messages.append(self.data)
                self.dial_out_logger()

                self.dial_out_message_send.setIcon(QIcon("./resources/image/send_FILL1_wght100_GRAD-25_opsz40_YELLOW.png"))
                time.sleep(1)
                self.dial_out_message_send.setIcon(QIcon("./resources/image/send_FILL1_wght100_GRAD-25_opsz40_WHITE.png"))

        except Exception as e:
            print(str(datetime.datetime.now()) + ' -- DialOutClass.message_send failed:', e)
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
    def __init__(self, server_incoming, server_notify_cipher, server_notify_alien):
        QThread.__init__(self)
        self.server_incoming = server_incoming
        self.server_notify_cipher = server_notify_cipher
        self.server_notify_alien = server_notify_alien
        self.server_data_0 = []
        self.data = ''
        self.notification_key = ''

    def server_logger(self):
        if not os.path.exists(server_log):
            open(server_log, 'w').close()
        with open(server_log, 'a') as fo:
            fo.write('\n' + self.data + '\n')
        fo.close()

    def play_notification_sound(self):
        player_default.play()
        time.sleep(1)

    def notification(self):
        print(str(datetime.datetime.now()) + ' -- ServerDataHandlerClass.notification: attempting communicator notification')
        global mute_server_notify_cipher_bool
        global mute_server_notify_alien_bool

        print('mute_server_notify_cipher_bool:', mute_server_notify_cipher_bool)

        if self.notification_key == 'green':
            self.server_incoming.setIcon(QIcon("./resources/image/public_FILL1_wght100_GRAD200_opsz40_GREEN.png"))
            if mute_server_notify_cipher_bool is False:
                self.play_notification_sound()

        elif self.notification_key == 'amber':
            self.server_incoming.setIcon(QIcon("./resources/image/public_FILL1_wght100_GRAD200_opsz40_AMBER.png"))
            if mute_server_notify_alien_bool is False:
                self.play_notification_sound()

        time.sleep(1)
        self.server_incoming.setIcon(QIcon("./resources/image/public_FILL1_wght100_GRAD200_opsz40_WHITE.png"))

    def run(self):
        print('-' * 200)
        self.data = str(datetime.datetime.now()) + ' -- ServerDataHandlerClass.run: plugged in'
        print(self.data)
        global server_messages
        global textbox_0_messages
        global server_address_messages
        global cipher_message_count
        global alien_message_count

        while True:
            try:
                self.server_data_0 = server_messages
                i_0 = 0
                for self.server_data_0s in self.server_data_0:
                    try:
                        ciphertext = self.server_data_0[i_0]
                        addr_data = server_address_messages[i_0]

                        # remove currently iterated over item from server_messages to keep the list low and performance high
                        server_messages.remove(ciphertext)
                        server_address_messages.remove(addr_data)

                        decrypted = ''
                        decrypted_message = ''
                        print(str(datetime.datetime.now()) + ' -- ServerDataHandlerClass.run: attempting to decrypt message')

                        # Communicator Standard Communication fingerprint is 1024 bytes so attempt decryption of any message larger than 1024 bytes
                        if len(ciphertext) > 1024:

                            # Use Keys in address book to attempt decryption (dictionary attack the message)
                            i_1 = 0
                            for _ in client_address:
                                print(str(datetime.datetime.now()) + ' -- ServerDataHandlerClass.run trying key:', str(_[3]))
                                try:
                                    print(str(datetime.datetime.now()) + ' -- ServerDataHandlerClass.run: handing message to AESCipher')
                                    cipher = AESCipher(_[3])
                                    decrypted = cipher.decrypt(ciphertext)
                                except Exception as e:
                                    print(str(datetime.datetime.now()) + ' -- ServerDataHandlerClass.run (address_key loop): ' + str(e))
                                    break

                                # If decrypted then display the name associated with the key else try next key
                                if decrypted:
                                    print(str(datetime.datetime.now()) + ' -- ServerDataHandlerClass.run: successfully decrypted message')
                                    print(str(datetime.datetime.now()) + ' -- ServerDataHandlerClass.run searching incoming message for fingerprint associated with:', str(_[0]))
                                    if decrypted.startswith(str(_[-1])):
                                        print(str(datetime.datetime.now()) + ' -- ServerDataHandlerClass.run fingerprint: validated as', str(_[0]))
                                        decrypted_message = decrypted.replace(str(_[-1]), '')
                                        textbox_0_messages.append('[' + str(datetime.datetime.now()) + '] [[DECIPHERED] [' + str(addr_data) + '] [' + str(_[0]) + '] ' + decrypted_message)
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
                            textbox_0_messages.append('[' + str(datetime.datetime.now()) + '] [' + str(addr_data) + '] [NON-STANDARD COMMUNICATION] ' + str(ciphertext))

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
    def __init__(self, server_incoming, server_status_label, soft_block_ip_notification):
        QThread.__init__(self)
        self.server_incoming = server_incoming
        self.server_status_label = server_status_label
        self.soft_block_ip_notification = soft_block_ip_notification
        self.data = ''
        self.SERVER_HOST = ''
        self.SERVER_PORT = ''
        self.time_con = 0

    def run(self):
        print(str(datetime.datetime.now()) + ' -- ServerClass.run: plugged in:')
        global server_address
        global server_address_index

        self.SERVER_HOST = server_address[server_address_index][0]
        print(str(datetime.datetime.now()) + ' -- ServerClass.run: SERVER_HOST:', self.SERVER_HOST)
        self.SERVER_PORT = server_address[server_address_index][1]
        print(str(datetime.datetime.now()) + ' -- ServerClass.run: SERVER_PORT:', self.SERVER_PORT)

        print('-' * 200)
        self.data = str(datetime.datetime.now()) + ' -- ServerClass.run: public server started'
        print(self.data)
        self.server_logger()

        while True:
            try:
                self.listen()
            except Exception as e:
                print(str(datetime.datetime.now()) + ' -- ServerClass.run failed:', e)

    def server_logger(self):
        if not os.path.exists(server_log):
            open(server_log, 'w').close()
        with open(server_log, 'a') as fo:
            fo.write('\n' + self.data + '\n')
        fo.close()

    def listen(self):
        global SOCKET_SERVER

        global client_address
        global client_address_index

        global server_messages
        global server_address_messages

        global x_time
        global z_time
        global prev_addr
        global soft_block_ip
        global violation_count
        global soft_block_ip_count

        self.server_status_label.setText('SERVER STATUS: ONLINE')
        self.server_incoming.setIcon(QIcon('./resources/image/public_FILL0_wght100_GRAD-25_opsz48_WHITE.png'))

        print('-' * 200)
        print(str(datetime.datetime.now()) + ' -- ServerClass.listen SERVER_HOST:', self.SERVER_HOST)
        print(str(datetime.datetime.now()) + ' -- ServerClass.listen SERVER_PORT:', self.SERVER_PORT)
        print(str(datetime.datetime.now()) + ' -- ServerClass.listen SERVER: attempting to listen')

        x_time = round(time.time() * 1000)

        while True:
            print('checking soft_block_ip:', soft_block_ip)
            if len(soft_block_ip) > 0:

                # DOS & DDOS Protection - Notify Per IP Address In Soft_Block_IP
                if len(soft_block_ip) >= 999:
                    soft_block_ip_count = '999+'
                else:
                    soft_block_ip_count = len(soft_block_ip)
                self.soft_block_ip_notification.setText(str(soft_block_ip_count))

                # DOS & DDOS Protection - Tune And Add Soft Block Time Ranges Using (Z_Time + n) And Violation Count
                i = 0
                for _ in soft_block_ip:

                    if soft_block_ip[i][2] < 20:
                        print(str(datetime.datetime.now()) + ' -- ServerClass.listen [violation < 20] ' + str(soft_block_ip[i][0]))
                        if round(time.time() * 1000) > (soft_block_ip[i][1] + 2000):  # Unblock in n [ Z_Time + TUNABLE n ] N=Milliseconds Soft Block Time
                            print(str(datetime.datetime.now()) + ' -- ServerClass.listen unblocking: ' + str(soft_block_ip[i][0]))
                            del soft_block_ip[i]

                            # DOS & DDOS Protection - Notify Per IP Address In Soft_Block_IP
                            if len(soft_block_ip) >= 999:
                                soft_block_ip_count = '999+'
                            else:
                                soft_block_ip_count = len(soft_block_ip)
                            self.soft_block_ip_notification.setText(str(soft_block_ip_count))

                        else:
                            print(str(datetime.datetime.now()) + ' -- ServerClass.listen soft block will remain: ' + str(soft_block_ip[i][0]))

                    i += 1

            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SOCKET_SERVER:
                    SOCKET_SERVER.bind((self.SERVER_HOST, self.SERVER_PORT))
                    SOCKET_SERVER.listen()
                    conn, addr = SOCKET_SERVER.accept()
                    print(str(datetime.datetime.now()) + ' -- ServerClass.listen conn, addr: ' + str(conn) + str(addr))

                    addr_exists_already = False
                    if len(soft_block_ip) > 0:
                        i = 0
                        for _ in soft_block_ip:
                            print('comparing:', soft_block_ip[i][0], ' ---> ', addr[0])
                            if soft_block_ip[i][0] == addr[0]:
                                print(str(datetime.datetime.now()) + ' -- ServerClass.listen SOCKET_SERVER ATTEMPTING BLOCK: ' + str(SOCKET_SERVER))
                                SOCKET_SERVER.close()
                                print(str(datetime.datetime.now()) + ' -- ServerClass.listen SOCKET_SERVER AFTER CLOSE ATTEMPT: ' + str(SOCKET_SERVER))
                                soft_block_ip_index = i
                                addr_exists_already = True
                            i += 1

                    # DOS & DDOS Protection - Set Previous Address
                    if addr[0] != prev_addr:
                        prev_addr = addr[0]
                    elif addr[0] == prev_addr:

                        # DOS & DDOS Protection - Initiate Y_Time
                        y_time = round(time.time() * 1000)

                        # DOS & DDOS Protection - Compare Y_Time (Now) To X_Time (Last Time)
                        if y_time < (x_time + 1000):  # Throttle Rate = n [ TUNABLE X_Time + n ] N=Milliseconds
                            print(str(datetime.datetime.now()) + ' -- ServerClass.listen checking soft block configuration for:' + str(addr[0]))

                            # DOS & DDOS Protection - Add New Entry To Soft Block List
                            if addr_exists_already is False:
                                print(str(datetime.datetime.now()) + ' -- ServerClass.listen adding IP Address to soft block list: ' + str(addr[0]))

                                # DOS & DDOS Protection - Set Z Time
                                _z_time = round(time.time() * 1000)
                                print(str(datetime.datetime.now()) + ' -- ServerClass.listen setting IP Address Z_TIME to current time: ' + str(addr[0]) + ' --> ' + str(_z_time))

                                # DOS & DDOS Protection - Set Violation Count
                                _violation_count = 1
                                print(str(datetime.datetime.now()) + ' -- ServerClass.listen setting IP Address violation count: ' + str(addr[0]) + ' --> ' + str(_violation_count))

                                new_list_entry = [addr[0], _z_time, _violation_count]
                                soft_block_ip.append(new_list_entry)

                            elif addr_exists_already is True:

                                # DOS & DDOS Protection - Amend Entry For Soft Block IP List
                                print(str(datetime.datetime.now()) + ' -- ServerClass.listen IP Address already in soft block list: ' + str(addr[0]))

                                # DOS & DDOS Protection - Amend Entry For Z_Time
                                soft_block_ip[soft_block_ip_index][1] = round(time.time() * 1000)

                                # DOS & DDOS Protection - Amend Entry For Violation Count
                                soft_block_ip[soft_block_ip_index][2] += 1

                                print('-- ammending soft_block_ip[soft_block_ip_index]:', soft_block_ip[soft_block_ip_index])

                        # DOS & DDOS Protection - Set X_Time As Time Y_Time
                        x_time = y_time
                        print(str(datetime.datetime.now()) + ' -- ServerClass.listen updating x time: ' + str(addr[0]))

                    # Handle Accepted Connection
                    if addr_exists_already is False:

                        with conn:
                            print('-' * 200)
                            self.data = str(datetime.datetime.now()) + ' -- ServerClass.listen incoming connection: ' + str(addr)
                            textbox_0_messages.append('[' + str(datetime.datetime.now()) + '] [INCOMING CONNECTION] [' + str(addr[0]) + ':' + str(addr[1]) + ']')
                            print(self.data)
                            self.server_logger()
                            while True:
                                try:
                                    server_data_0 = ''
                                    server_data_0 = conn.recv(2048)
                                    if not server_data_0:
                                        break

                                    # dump server_data_0 into a stack for the server_data_handler
                                    server_messages.append(server_data_0)
                                    server_address_messages.append(str(addr[0]) + ' ' + str(addr[1]))

                                    # show connection received data
                                    self.data = str(datetime.datetime.now()) + ' -- ServerClass.listen connection received server_messages: ' + str(addr) + ' server_messages: ' + str(server_data_0)
                                    print(self.data)
                                    self.server_logger()

                                    # send delivery confirmation message
                                    print(str(datetime.datetime.now()) + ' -- ServerClass.listen: sending delivery confirmation message to:' + str(conn))
                                    conn.sendall(server_data_0)

                                except Exception as e:
                                    print(str(datetime.datetime.now()) + ' ' + str(e))
                                    textbox_0_messages.append('[' + str(datetime.datetime.now()) + '] ' + str(e))
                                    break

            except Exception as e:
                print(str(datetime.datetime.now()) + ' -- ServerClass.listen failed:', e)
                textbox_0_messages.append('[' + str(datetime.datetime.now()) + '] ' + str(e))
                self.server_status_label.setText('SERVER STATUS: OFFLINE')
                self.server_incoming.setIcon(QIcon('./resources/image/public_OFF_FILL0_wght100_GRAD-25_opsz48_WHITE.png'))
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
        self.server_incoming.setIcon(QIcon('./resources/image/public_OFF_FILL0_wght100_GRAD-25_opsz48_WHITE.png'))
        global_self.setFocus()
        self.terminate()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
