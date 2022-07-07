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
import encodings

# Threads
configuration_thread = []


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

# Initialize Notification Player_default In Memory
player_url_default = QUrl.fromLocalFile("./resources/audio/communicator_0.wav")
player_content_default = QMediaContent(player_url_default)
player_default = QMediaPlayer()
player_default.setMedia(player_content_default)
player_default.setVolume(100)

# Images
server_public_white = './resources/image/globe_white.png'
server_public_yellow = './resources/image/globe_yellow.png'
server_public_amber = './resources/image/globe_amber.png'
server_public_green = './resources/image/globe_green.png'
server_public_off = './resources/image/globe_off.png'
mute_0 = './resources/image/mute_0.png'
mute_1 = './resources/image/mute_1.png'
advanced_save_0 = './resources/image/advanced_save_0.png'
advanced_save_1 = './resources/image/advanced_save_1.png'
arrow_left = './resources/image/arrow_left.png'
arrow_right = './resources/image/arrow_right.png'
send_white = './resources/image/send_white.png'
send_green = './resources/image/send_green.png'
send_red = './resources/image/send_red.png'
send_yellow = './resources/image/send_yellow.png'
clear_all = './resources/image/clear_all.png'
visibility_0 = './resources/image/visibility_0.png'
visibility_1 = './resources/image/visibility_1.png'
play_green = './resources/image/play_green.png'
play_yellow = './resources/image/play_yellow.png'
replay_yellow = './resources/image/replay_yellow.png'
stop_red = './resources/image/stop_red.png'
undo_white = './resources/image/undo_white.png'

# Boolean
dial_out_dial_out_cipher_bool = True
configuration_thread_completed = False
write_server_configuration_engaged = False
write_client_configuration_engaged = False
mute_server_notify_alien_bool = False
mute_server_notify_cipher_bool = False
bool_dial_out_override = False
server_save_bool = False
address_reveal_bool = False
bool_socket_options = False
address_override_string = ''
unpopulated = None

COMMUNICATOR_SOCK = {
    "Unselected" : unpopulated,
    "AF_APPLETALK" : socket.AF_APPLETALK,
    "AF_BLUETOOTH" : socket.AF_BLUETOOTH,
    "AF_DECnet" : socket.AF_DECnet,
    "AF_INET" : socket.AF_INET,
    "AF_INET6" : socket.AF_INET6,
    "AF_IPX" : socket.AF_IPX,
    "AF_IRDA" : socket.AF_IRDA,
    "AF_LINK" : socket.AF_LINK,
    "AF_SNA" : socket.AF_SNA,
    "AF_UNSPEC" : socket.AF_UNSPEC,
    "AI_ADDRCONFIG" : socket.AI_ADDRCONFIG,
    "AI_ALL" : socket.AI_ALL,
    "AI_CANONNAME" : socket.AI_CANONNAME,
    "AI_NUMERICHOST" : socket.AI_NUMERICHOST,
    "AI_NUMERICSERV" : socket.AI_NUMERICSERV,
    "AI_PASSIVE" : socket.AI_PASSIVE,
    "AI_V4MAPPED" : socket.AI_V4MAPPED,
    "BDADDR_ANY" : socket.BDADDR_ANY,
    "BDADDR_LOCAL" : socket.BDADDR_LOCAL,
    "BTPROTO_RFCOMM" : socket.BTPROTO_RFCOMM,
    "EAI_AGAIN" : socket.EAI_AGAIN,
    "EAI_BADFLAGS" : socket.EAI_BADFLAGS,
    "EAI_FAIL" : socket.EAI_FAIL,
    "EAI_FAMILY" : socket.EAI_FAMILY,
    "EAI_MEMORY" : socket.EAI_MEMORY,
    "EAI_NODATA" : socket.EAI_NODATA,
    "EAI_NONAME" : socket.EAI_NONAME,
    "EAI_SERVICE" : socket.EAI_SERVICE,
    "EAI_SOCKTYPE" : socket.EAI_SOCKTYPE,
    "has_ipv6" : socket.has_ipv6,
    "INADDR_ALLHOSTS_GROUP" : socket.INADDR_ALLHOSTS_GROUP,
    "INADDR_ANY" : socket.INADDR_ANY,
    "INADDR_BROADCAST" : socket.INADDR_BROADCAST,
    "INADDR_LOOPBACK" : socket.INADDR_LOOPBACK,
    "INADDR_MAX_LOCAL_GROUP" : socket.INADDR_MAX_LOCAL_GROUP,
    "INADDR_NONE" : socket.INADDR_NONE,
    "INADDR_UNSPEC_GROUP" : socket.INADDR_UNSPEC_GROUP,
    "IPPORT_RESERVED" : socket.IPPORT_RESERVED,
    "IPPORT_USERRESERVED" : socket.IPPORT_USERRESERVED,
    "IPPROTO_AH" : socket.IPPROTO_AH,
    "IPPROTO_CBT" : socket.IPPROTO_CBT,
    "IPPROTO_DSTOPTS" : socket.IPPROTO_DSTOPTS,
    "IPPROTO_EGP" : socket.IPPROTO_EGP,
    "IPPROTO_ESP" : socket.IPPROTO_ESP,
    "IPPROTO_FRAGMENT" : socket.IPPROTO_FRAGMENT,
    "IPPROTO_GGP" : socket.IPPROTO_GGP,
    "IPPROTO_HOPOPTS" : socket.IPPROTO_HOPOPTS,
    "IPPROTO_ICLFXBM" : socket.IPPROTO_ICLFXBM,
    "IPPROTO_ICMP" : socket.IPPROTO_ICMP,
    "IPPROTO_ICMPV6" : socket.IPPROTO_ICMPV6,
    "IPPROTO_IDP" : socket.IPPROTO_IDP,
    "IPPROTO_IGMP" : socket.IPPROTO_IGMP,
    "IPPROTO_IGP" : socket.IPPROTO_IGP,
    "IPPROTO_IP" : socket.IPPROTO_IP,
    "IPPROTO_IPV4" : socket.IPPROTO_IPV4,
    "IPPROTO_IPV6" : socket.IPPROTO_IPV6,
    "IPPROTO_L2TP" : socket.IPPROTO_L2TP,
    "IPPROTO_MAX" : socket.IPPROTO_MAX,
    "IPPROTO_ND" : socket.IPPROTO_ND,
    "IPPROTO_NONE" : socket.IPPROTO_NONE,
    "IPPROTO_PGM" : socket.IPPROTO_PGM,
    "IPPROTO_PIM" : socket.IPPROTO_PIM,
    "IPPROTO_PUP" : socket.IPPROTO_PUP,
    "IPPROTO_RAW" : socket.IPPROTO_RAW,
    "IPPROTO_RDP" : socket.IPPROTO_RDP,
    "IPPROTO_ROUTING" : socket.IPPROTO_ROUTING,
    "IPPROTO_SCTP" : socket.IPPROTO_SCTP,
    "IPPROTO_ST" : socket.IPPROTO_ST,
    "IPPROTO_TCP" : socket.IPPROTO_TCP,
    "IPPROTO_UDP" : socket.IPPROTO_UDP,
    "IPV6_CHECKSUM" : socket.IPV6_CHECKSUM,
    "IPV6_DONTFRAG" : socket.IPV6_DONTFRAG,
    "IPV6_HOPLIMIT" : socket.IPV6_HOPLIMIT,
    "IPV6_HOPOPTS" : socket.IPV6_HOPOPTS,
    "IPV6_JOIN_GROUP" : socket.IPV6_JOIN_GROUP,
    "IPV6_LEAVE_GROUP" : socket.IPV6_LEAVE_GROUP,
    "IPV6_MULTICAST_HOPS" : socket.IPV6_MULTICAST_HOPS,
    "IPV6_MULTICAST_IF" : socket.IPV6_MULTICAST_IF,
    "IPV6_MULTICAST_LOOP" : socket.IPV6_MULTICAST_LOOP,
    "IPV6_PKTINFO" : socket.IPV6_PKTINFO,
    "IPV6_RECVRTHDR" : socket.IPV6_RECVRTHDR,
    "IPV6_RECVTCLASS" : socket.IPV6_RECVTCLASS,
    "IPV6_RTHDR" : socket.IPV6_RTHDR,
    "IPV6_TCLASS" : socket.IPV6_TCLASS,
    "IPV6_UNICAST_HOPS" : socket.IPV6_UNICAST_HOPS,
    "IPV6_V6ONLY" : socket.IPV6_V6ONLY,
    "IP_ADD_MEMBERSHIP" : socket.IP_ADD_MEMBERSHIP,
    "IP_DROP_MEMBERSHIP" : socket.IP_DROP_MEMBERSHIP,
    "IP_HDRINCL" : socket.IP_HDRINCL,
    "IP_MULTICAST_IF" : socket.IP_MULTICAST_IF,
    "IP_MULTICAST_LOOP" : socket.IP_MULTICAST_LOOP,
    "IP_MULTICAST_TTL" : socket.IP_MULTICAST_TTL,
    "IP_OPTIONS" : socket.IP_OPTIONS,
    "IP_RECVDSTADDR" : socket.IP_RECVDSTADDR,
    "IP_TOS" : socket.IP_TOS,
    "IP_TTL" : socket.IP_TTL,
    "MSG_BCAST" : socket.MSG_BCAST,
    "MSG_CTRUNC" : socket.MSG_CTRUNC,
    "MSG_DONTROUTE" : socket.MSG_DONTROUTE,
    "MSG_ERRQUEUE" : socket.MSG_ERRQUEUE,
    "MSG_MCAST" : socket.MSG_MCAST,
    "MSG_OOB" : socket.MSG_OOB,
    "MSG_PEEK" : socket.MSG_PEEK,
    "MSG_TRUNC" : socket.MSG_TRUNC,
    "MSG_WAITALL" : socket.MSG_WAITALL,
    "NI_DGRAM" : socket.NI_DGRAM,
    "NI_MAXHOST" : socket.NI_MAXHOST,
    "NI_MAXSERV" : socket.NI_MAXSERV,
    "NI_NAMEREQD" : socket.NI_NAMEREQD,
    "NI_NOFQDN" : socket.NI_NOFQDN,
    "NI_NUMERICHOST" : socket.NI_NUMERICHOST,
    "NI_NUMERICSERV" : socket.NI_NUMERICSERV,
    "RCVALL_MAX" : socket.RCVALL_MAX,
    "RCVALL_OFF" : socket.RCVALL_OFF,
    "RCVALL_ON" : socket.RCVALL_ON,
    "RCVALL_SOCKETLEVELONLY" : socket.RCVALL_SOCKETLEVELONLY,
    "SHUT_RD" : socket.SHUT_RD,
    "SHUT_RDWR" : socket.SHUT_RDWR,
    "SHUT_WR" : socket.SHUT_WR,
    "SIO_KEEPALIVE_VALS" : socket.SIO_KEEPALIVE_VALS,
    "SIO_LOOPBACK_FAST_PATH" : socket.SIO_LOOPBACK_FAST_PATH,
    "SIO_RCVALL" : socket.SIO_RCVALL,
    "SOCK_DGRAM" : socket.SOCK_DGRAM,
    "SOCK_RAW" : socket.SOCK_RAW,
    "SOCK_RDM" : socket.SOCK_RDM,
    "SOCK_SEQPACKET" : socket.SOCK_SEQPACKET,
    "SOCK_STREAM" : socket.SOCK_STREAM,
    "SOL_IP" : socket.SOL_IP,
    "SOL_SOCKET" : socket.SOL_SOCKET,
    "SOL_TCP" : socket.SOL_TCP,
    "SOL_UDP" : socket.SOL_UDP,
    "SOMAXCONN" : socket.SOMAXCONN,
    "SO_ACCEPTCONN" : socket.SO_ACCEPTCONN,
    "SO_BROADCAST" : socket.SO_BROADCAST,
    "SO_DEBUG" : socket.SO_DEBUG,
    "SO_DONTROUTE" : socket.SO_DONTROUTE,
    "SO_ERROR" : socket.SO_ERROR,
    "SO_EXCLUSIVEADDRUSE" : socket.SO_EXCLUSIVEADDRUSE,
    "SO_KEEPALIVE" : socket.SO_KEEPALIVE,
    "SO_LINGER" : socket.SO_LINGER,
    "SO_OOBINLINE" : socket.SO_OOBINLINE,
    "SO_RCVBUF" : socket.SO_RCVBUF,
    "SO_RCVLOWAT" : socket.SO_RCVLOWAT,
    "SO_RCVTIMEO" : socket.SO_RCVTIMEO,
    "SO_REUSEADDR" : socket.SO_REUSEADDR,
    "SO_SNDBUF" : socket.SO_SNDBUF,
    "SO_SNDLOWAT" : socket.SO_SNDLOWAT,
    "SO_SNDTIMEO" : socket.SO_SNDTIMEO,
    "SO_TYPE" : socket.SO_TYPE,
    "SO_USELOOPBACK" : socket.SO_USELOOPBACK,
    "TCP_FASTOPEN" : socket.TCP_FASTOPEN,
    "TCP_KEEPCNT" : socket.TCP_KEEPCNT,
    "TCP_KEEPIDLE" : socket.TCP_KEEPIDLE,
    "TCP_KEEPINTVL" : socket.TCP_KEEPINTVL,
    "TCP_MAXSEG" : socket.TCP_MAXSEG,
    "TCP_NODELAY" : socket.TCP_NODELAY
}

label_stylesheet_black_bg_text_white = """QLabel{background-color: rgb(0, 0, 0);
                       color: rgb(200, 200, 200);
                       border-bottom:0px solid rgb(5, 5, 5);
                       border-right:0px solid rgb(5, 5, 5);
                       border-top:0px solid rgb(5, 5, 5);
                       border-left:0px solid rgb(5, 5, 5);}"""

title_stylesheet_default = """QLabel{background-color: rgb(10, 10, 10);
                       color: rgb(255, 255, 255);
                       border-bottom:2px solid rgb(5, 5, 5);
                       border-right:2px solid rgb(5, 5, 5);
                       border-top:2px solid rgb(5, 5, 5);
                       border-left:2px solid rgb(5, 5, 5);}"""

label_stylesheet_red_text = """QLabel{background-color: rgb(10, 10, 10);
                       color: rgb(190, 0, 0);
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

button_stylesheet_white_text_high = """QPushButton{background-color: rgb(10, 10, 10);
                       color: rgb(255, 255, 255);
                       border-bottom:2px solid rgb(5, 5, 5);
                       border-right:2px solid rgb(5, 5, 5);
                       border-top:2px solid rgb(5, 5, 5);
                       border-left:2px solid rgb(5, 5, 5);}"""

button_stylesheet_white_text_low = """QPushButton{background-color: rgb(10, 10, 10);
                       color: rgb(100, 100, 100);
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

button_stylesheet_red_text_low = """QPushButton{background-color: rgb(10, 10, 10);
                       color: rgb(200, 0, 0);
                       border-bottom:0px solid rgb(177, 177, 177);
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

textbox_stylesheet_black_bg = """QTextBrowser {background-color: rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: rgb(0, 180, 0);
                color: rgb(200, 200, 200);
                border-bottom:2px solid rgb(5, 5, 5);
                border-right:2px solid rgb(5, 5, 5);
                border-top:2px solid rgb(5, 5, 5);
                border-left:2px solid rgb(5, 5, 5);}"""

cmb_menu_style = """QComboBox {background-color: rgb(10, 10, 10);
                   color: rgb(200, 200, 200);
                   border-top:2px solid rgb(5, 5, 5);
                   border-bottom:2px solid rgb(5, 5, 5);
                   border-right:2px solid rgb(5, 5, 5);
                   border-left:2px solid rgb(0, 0, 0);}"""

global_self = []


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
                                    image:url('./resources/image/scroll_white.png');
                                    height: 11px;
                                    width: 11px;
                                    }
                                    QScrollBar::down-arrow:vertical {
                                    image:url('./resources/image/scroll_white.png');
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
                                    image:url('./resources/image/scroll_white.png');
                                    height: 11px;
                                    width: 11px;
                                    }
                                    QScrollBar::right-arrow:horizontal {
                                    image:url('./resources/image/scroll_white.png');
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

        self.key_string = ''
        self.fingerprint_str = ''

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

            # Attempt to only run this function if this function is not already in progress
            if write_client_configuration_engaged is False:
                write_client_configuration_engaged = True

                # Name must not be empty
                if self.dial_out_name.text() != '':
                    if self.dial_out_ip_port.text() != '':

                        # Create a temporary list to manipulate and use to compare to line in the address book
                        remove_address = client_address[client_address_index]

                        # Check if address book exists
                        if os.path.exists('./communicator_address_book.txt'):

                            # Create a temporary list to store lines from the address book
                            fo_list = []

                            # Set a boolean condition to prevent an unnecessary write if the event that a target line is not found
                            write_bool = False

                            # Open the address book to read
                            with open('./communicator_address_book.txt', 'r') as fo:
                                for line in fo:
                                    line = line.strip()

                                    # Create a list from the expected space delimited line and then check the line
                                    line_split = line.split(' ')
                                    if len(line_split) > 0:
                                        if line != '' and line_split[0] == 'DATA':

                                            # Create a thorough but partial list from current client address in memory (item excluded is the actual fingerprint)
                                            compare_remove_address = [str(remove_address[0]),
                                                                      str(remove_address[1]),
                                                                      str(remove_address[2]),
                                                                      remove_address[3].decode('utf-8'),
                                                                      str(remove_address[5]),
                                                                      str(remove_address[6]),
                                                                      str(remove_address[7]),
                                                                      str(remove_address[8]),
                                                                      str(remove_address[9]),
                                                                      str(remove_address[10])]

                                            # Create a thorough but partial list from line in file (item excluded is fingerprint path)
                                            compare_line_address = [str(line_split[1]),
                                                                    str(line_split[2]),
                                                                    str(line_split[3]),
                                                                    str(line_split[4]),
                                                                    str(line_split[6]),
                                                                    str(line_split[7]),
                                                                    str(line_split[8]),
                                                                    str(line_split[9]),
                                                                    str(line_split[10]),
                                                                    str(line_split[11])]

                                            # Display to compare
                                            print('-- MEM LIST COMPARE: ', compare_remove_address)
                                            print('-- FILE LIST COMPARE:', compare_line_address)

                                            # Append unequal lines to a list
                                            if compare_remove_address != compare_line_address:
                                                fo_list.append(line)
                                                print('-- KEEPING LINE:', line)

                                            # Clearly display the line that is equal and do not add the line to a list
                                            elif compare_remove_address == compare_line_address:
                                                print('-- TARGET REMOVE:', line)
                                                write_bool = True

                            # If the target line in address book was found then write lines from the list into a temporary file
                            if write_bool is True:
                                open('./communicator_address_book.tmp', 'w').close()
                                with open('./communicator_address_book.tmp', 'w') as fo:
                                    for _ in fo_list:
                                        fo.write(str(_) + '\n')
                                fo.close()

                                # Replace address book contents with the contents of the temporary file
                                if os.path.exists('./communicator_address_book.tmp'):
                                    os.replace('./communicator_address_book.tmp', './communicator_address_book.txt')

                                # Remove the currently selected address from client address list in memory
                                del client_address[client_address_index]

                                # Turn the page (previous and next address functions handle empty address list)
                                client_previous_address_function()

                    write_client_configuration_engaged = False

        def client_save_address():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.client_save_address')
            global write_client_configuration_engaged
            global client_address
            global client_address_index
            global address_save_mode
            global button_stylesheet_green_text
            global internal_messages

            # Attempt to only run this function if this function is not already in progress
            if write_client_configuration_engaged is False:
                write_client_configuration_engaged = True

                # Name must not be empty and there must not be space in name
                if self.dial_out_name.text() != '' and ' ' not in self.dial_out_name.text():

                    # Address field must not be empty
                    if self.dial_out_ip_port.text() != '':

                        # Clearly display the save mode
                        print(str(datetime.datetime.now()) + ' -- App.client_save_address using address_save_mode:', address_save_mode)

                        # Create a pre-flight check list
                        allow_save_bool = []

                        # Codec must be selected
                        if str(self.codec_select_box.currentText()) != 'Unselected':
                            print('-- check_0: pass')
                            s_enc = str(self.codec_select_box.currentText()).split()[0] + '______' + str(self.codec_select_box.currentText()).split()[1]
                        else:
                            print('-- check_0: fail')
                            allow_save_bool.append(False)

                        # Address Family must be selected
                        if str(self.communicator_socket_options_box_0.currentText()) != 'Unselected':
                            print('-- check_1: pass')
                            s_address_family = str(self.communicator_socket_options_box_0.currentText())
                        else:
                            print('-- check_1: fail')
                            allow_save_bool.append(False)

                        # Socket Type must be selected
                        if str(self.communicator_socket_options_box_1.currentText()) != 'Unselected':
                            print('-- check_2: pass')
                            s_soc_type = str(self.communicator_socket_options_box_1.currentText())
                        else:
                            print('-- check_2: fail')
                            allow_save_bool.append(False)

                        # Continue if not False in the pre-flight check list
                        if False not in allow_save_bool:

                            # Set a new boolean to False and use this variable to allow or disallow the final address book amendment later
                            bool_allow_write = False

                            # Get the socket options and create a string of all the socket arguments
                            s_options_0 = str(self.communicator_socket_options_box_2.currentText())
                            s_options_1 = str(self.communicator_socket_options_box_3.currentText())
                            s_args = s_enc + ' ' + s_address_family + ' ' + s_soc_type + ' ' + s_options_0 + ' ' + s_options_1

                            # Display current address index for comparison later
                            print('-- current index before potentially sorting:', client_address_index)

                            # Initiate an empty string which can be used as the string to append to the address book later
                            to_address_book = ''

                            # Basic Save Mode
                            if address_save_mode == 'basic':

                                # Save mode is basic so ensure key and fingerprint have been cleared
                                self.address_key.setText('')
                                self.tb_fingerprint.setText('')

                                # Expects address and port each seperated by a space (over sanitizing will make addressing less powerful and less future-proof, so this statement just checks for two items)
                                if len(self.dial_out_ip_port.text().split(' ')) == 2:

                                    # Set the string which should be appended to the address book
                                    to_address_book = 'DATA ' + self.dial_out_name.text() + ' ' + str(self.dial_out_ip_port.text()) + ' x' + ' x' + ' x ' + s_args

                                    # Append a new list to the address book list in memory
                                    client_address.append([str(self.dial_out_name.text()), str(self.dial_out_ip_port.text().split(' ')[0]), int(self.dial_out_ip_port.text().split(' ')[1]), bytes('x', 'utf-8'), 'x', 'x', s_enc, s_address_family, s_soc_type, s_options_0, s_options_1])

                                    # Alphabetically sort the address book in memory
                                    client_address.sort(key=lambda x: x[0])

                                    # Find the new index of the new address book entry in memory after sorting and set the new current address book index accordingly
                                    client_address_index = client_address.index([str(self.dial_out_name.text()), str(self.dial_out_ip_port.text().split(' ')[0]), int(self.dial_out_ip_port.text().split(' ')[1]), bytes('x', 'utf-8'), 'x', 'x', s_enc, s_address_family, s_soc_type, s_options_0, s_options_1])

                                    bool_allow_write = True

                                # Expects address, port and broadcast address each seperated by a space (over sanitizing will make addressing less powerful and less future-proof, so this statement just checks for two items)
                                elif len(self.dial_out_ip_port.text().split(' ')) == 3:
                                    broadcast_address = self.dial_out_ip_port.text().split()[2]

                                    # Set the string which should be appended to the address book
                                    to_address_book = 'DATA ' + self.dial_out_name.text() + ' ' + str(self.dial_out_ip_port.text().split()[0]) + ' ' + str(self.dial_out_ip_port.text().split()[1]) + ' x' + ' x' + ' ' + str(self.dial_out_ip_port.text().split()[2]) + ' ' + s_args

                                    # Append a new list to the address book list in memory
                                    client_address.append([str(self.dial_out_name.text()), str(self.dial_out_ip_port.text().split(' ')[0]), int(self.dial_out_ip_port.text().split(' ')[1]), bytes('x', 'utf-8'), 'x', broadcast_address, s_enc, s_address_family, s_soc_type, s_options_0, s_options_1])

                                    # Alphabetically sort the address book in memory
                                    client_address.sort(key=lambda x: x[0])

                                    # Find the new index of the new address book entry in memory after sorting and set the new current address book index accordingly
                                    client_address_index = client_address.index([str(self.dial_out_name.text()), str(self.dial_out_ip_port.text().split(' ')[0]), int(self.dial_out_ip_port.text().split(' ')[1]), bytes('x', 'utf-8'), 'x', broadcast_address, s_enc, s_address_family, s_soc_type, s_options_0, s_options_1])

                                    bool_allow_write = True

                            # Advanced Save Mode
                            elif address_save_mode == 'advanced':

                                # Display key and fingerprint
                                print('key:', str(self.address_key.text()))
                                print('fingerprint:', self.tb_fingerprint.toPlainText().strip())

                                # Create a new fingerprint filename using the name in the name input field
                                fingerprint_fname = self.dial_out_name.text()

                                # List and display each filename in the fingerprints directory
                                fingerprint_fname_list = os.listdir('./fingerprints')
                                print('fingerprint_fname_list:', fingerprint_fname_list)

                                # Check if the newly created fingerprint filename already exists in the fingerprint directory
                                if fingerprint_fname + '.txt' in fingerprint_fname_list:
                                    fingerprint_fname_ready_bool = False

                                    #  While fingerprint filename exists, try appending numbers to the filename until a filename does not exist in the fingerprints directory
                                    i = 0
                                    while fingerprint_fname_ready_bool is False:
                                        var = fingerprint_fname + str(i) + '.txt'
                                        if var not in fingerprint_fname_list:
                                            fingerprint_fname = var
                                            fingerprint_fname_ready_bool = True
                                        else:
                                            i += 1

                                # Append fingerprint filename suffix if not already exists
                                if not fingerprint_fname.endswith('.txt'):
                                    fingerprint_fname = fingerprint_fname + '.txt'

                                # Pre-append intended path to the newly created fingerprint filename
                                fingerprint_fname = './fingerprints/' + fingerprint_fname

                                # Display the new intended fingerprint path plus filename
                                print('fingerprint_fname:', fingerprint_fname)

                                # Concatenate each line in fingerprint textbox into a single clean string
                                self.fingerprint_str = ''
                                for line in self.tb_fingerprint.toPlainText():
                                    line = line.strip()
                                    self.fingerprint_str = self.fingerprint_str + line

                                # Display the new fingerprint string
                                print('self.fingerprint_str:', self.fingerprint_str)

                                # Check Lengths of both key and fingerprint
                                print('len(self.address_key.text()) has to be 32 to continue:', len(self.address_key.text()))
                                print('len(self.fingerprint_str) has to be 1024 to continue:', len(self.fingerprint_str))
                                if len(self.address_key.text()) == 32:
                                    if len(self.fingerprint_str) == 1024:

                                        # Expects address and port each seperated by a space (over sanitizing will make addressing less powerful and less future-proof, so this statement just checks for two items)
                                        if len(self.dial_out_ip_port.text().split(' ')) == 2:

                                            # Set the string which should be appended to the address book
                                            to_address_book = 'DATA ' + self.dial_out_name.text() + ' ' + str(self.dial_out_ip_port.text()) + ' ' + self.address_key.text() + ' ' + fingerprint_fname + ' x ' + s_args

                                            # Append a new list to the address book list in memory
                                            client_address.append([str(self.dial_out_name.text()), str(self.dial_out_ip_port.text().split(' ')[0]), int(self.dial_out_ip_port.text().split(' ')[1]), bytes(self.address_key.text(), 'utf-8'), self.fingerprint_str, 'x', s_enc, s_address_family, s_soc_type, s_options_0, s_options_1])

                                            # Alphabetically sort the address book in memory
                                            client_address.sort(key=lambda x: x[0])

                                            # Find the new index of the new address book entry in memory after sorting and set the new current address book index accordingly
                                            client_address_index = client_address.index([str(self.dial_out_name.text()), str(self.dial_out_ip_port.text().split(' ')[0]), int(self.dial_out_ip_port.text().split(' ')[1]), bytes(self.address_key.text(), 'utf-8'), self.fingerprint_str, 'x', s_enc, s_address_family, s_soc_type, s_options_0, s_options_1])

                                            bool_allow_write = True

                                        # Expects address, port and broadcast address each seperated by a space (over sanitizing will make addressing less powerful and less future-proof, so this statement just checks for two items)
                                        elif len(self.dial_out_ip_port.text().split(' ')) == 3:
                                            broadcast_address = self.dial_out_ip_port.text().split()[2]

                                            # Set the string which should be appended to the address book
                                            to_address_book = 'DATA ' + self.dial_out_name.text() + ' ' + str(self.dial_out_ip_port.text().split()[0]) + ' ' + str(self.dial_out_ip_port.text().split()[1]) + ' ' + self.address_key.text() + ' ' + fingerprint_fname + ' ' + broadcast_address + ' ' + s_args

                                            # Append a new list to the address book list in memory
                                            client_address.append([str(self.dial_out_name.text()), str(self.dial_out_ip_port.text().split(' ')[0]), int(self.dial_out_ip_port.text().split(' ')[1]), bytes(self.address_key.text(), 'utf-8'), self.fingerprint_str, broadcast_address, s_enc, s_address_family, s_soc_type, s_options_0, s_options_1])

                                            # Alphabetically sort the address book in memory
                                            client_address.sort(key=lambda x: x[0])

                                            # Find the new index of the new address book entry in memory after sorting and set the new current address book index accordingly
                                            client_address_index = client_address.index([str(self.dial_out_name.text()), str(self.dial_out_ip_port.text().split(' ')[0]), int(self.dial_out_ip_port.text().split(' ')[1]), bytes(self.address_key.text(), 'utf-8'), self.fingerprint_str, broadcast_address, s_enc, s_address_family, s_soc_type, s_options_0, s_options_1])

                                            bool_allow_write = True

                                        # Write fingerprint file to the fingerprint directory with a 32-character limit on each line (to make the fingerprint file contents neat)
                                        split_strings = [self.fingerprint_str[index: index + 32] for index in range(0, len(self.fingerprint_str), 32)]
                                        if not os.path.exists(fingerprint_fname):
                                            open(fingerprint_fname, 'w').close()
                                        with open(fingerprint_fname, 'w') as fo:
                                            for _ in split_strings:
                                                fo.write(_ + '\n')
                                        fo.close()

                            # Append the new address book entry to the address book file conditionally
                            if to_address_book != '':
                                if bool_allow_write is True:
                                    if os.path.exists('./communicator_address_book.txt'):
                                        with open('./communicator_address_book.txt', 'a') as fo:
                                            fo.write(to_address_book + '\n')
                                        fo.close()
                                else:
                                    print('-- entry will not be appended to the address book as something went wrong. try again.')

                            # Display the potentially new current index as the index may have changed
                            print('-- current index after sorting:', client_address_index)
                else:
                    print('-- ip and port should not be empty!')
            else:
                print('-- name should not be empty!')

            write_client_configuration_engaged = False

        def server_prev_addr_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.server_prev_addr_function')
            global_self.setFocus()
            global server_address_index
            global server_address

            self.server_add_addr.setStyleSheet(button_stylesheet_white_text_low)
            self.server_add_addr.setEnabled(False)

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

            self.server_add_addr.setStyleSheet(button_stylesheet_white_text_low)
            self.server_add_addr.setEnabled(False)

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

        def sck_set_arguments_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.sck_set_arguments_function')
            global client_address
            global client_address_index

            # ENCODING
            enc_var = client_address[client_address_index][6].replace('______', ' ')
            index = self.codec_select_box.findText(enc_var, QtCore.Qt.MatchFixedString)
            if index >= 0:
                print('-- [ENCODING] found index:', index, 'for', client_address[client_address_index][6])
                self.codec_select_box.setCurrentIndex(index)
            else:
                print('-- [ENCODING] could not find index for:', client_address[client_address_index][6])

            # ADDRESS FAMILY
            index = self.communicator_socket_options_box_0.findText(client_address[client_address_index][7],
                                                                    QtCore.Qt.MatchFixedString)
            if index >= 0:
                print('-- [ADDRESS FAMILY] found index:', index, 'for', client_address[client_address_index][7])
                self.communicator_socket_options_box_0.setCurrentIndex(index)
            else:
                print('-- [ADDRESS FAMILY] could not find index for:', client_address[client_address_index][7])

            # SOCKET TYPE
            index = self.communicator_socket_options_box_1.findText(client_address[client_address_index][8],
                                                                    QtCore.Qt.MatchFixedString)
            if index >= 0:
                print('-- [SOCKET TYPE] found index:', index, 'for', client_address[client_address_index][8])
                self.communicator_socket_options_box_1.setCurrentIndex(index)
            else:
                print('-- [SOCKET TYPE] could not find index for:', client_address[client_address_index][8])

            # SOCKET OPTION 0
            index = self.communicator_socket_options_box_2.findText(client_address[client_address_index][9],
                                                                    QtCore.Qt.MatchFixedString)
            if index >= 0:
                print('-- [SOCKET OPTION  0] found index:', index, 'for', client_address[client_address_index][9])
                self.communicator_socket_options_box_2.setCurrentIndex(index)
            else:
                print('-- [SOCKET OPTION  0] could not find index for:', client_address[client_address_index][9])

            # SOCKET OPTION 1
            index = self.communicator_socket_options_box_3.findText(client_address[client_address_index][10],
                                                                    QtCore.Qt.MatchFixedString)
            if index >= 0:
                print('-- [SOCKET OPTION  1] found index:', index, 'for', client_address[client_address_index][10])
                self.communicator_socket_options_box_3.setCurrentIndex(index)
            else:
                print('-- [SOCKET OPTION  1] could not find index for:', client_address[client_address_index][10])

        def client_previous_address_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.client_previous_address_function')
            global_self.setFocus()
            global client_address
            global client_address_index
            global dial_out_dial_out_cipher_bool

            self.dial_out_name.setText('')
            self.dial_out_ip_port.setText('')
            self.address_key.setText('')
            self.tb_fingerprint.setText('')

            print(str(datetime.datetime.now()) + ' -- len(client_address):', len(client_address))
            if len(client_address) > 0:
                if client_address_index == 0:
                    client_address_index = len(client_address) - 1
                else:
                    client_address_index = client_address_index - 1
                print(str(datetime.datetime.now()) + ' -- client_address_index setting client_address_index:', client_address_index)

                self.dial_out_name.setText(str(client_address[client_address_index][0]))

                if len(client_address[client_address_index]) >= 10:

                    print('client_address[client_address_index]:', client_address[client_address_index])
                    print('LEN client_address[client_address_index]:', len(client_address[client_address_index]))
                    if 'x' == str(client_address[client_address_index][5]):
                        print(' -- skipping as [5] is x.')
                        self.dial_out_ip_port.setText(client_address[client_address_index][1] + ' ' + str(client_address[client_address_index][2]))
                    else:
                        print('-- using broadcast address')
                        self.dial_out_ip_port.setText(client_address[client_address_index][1] + ' ' + str(client_address[client_address_index][2]) + ' ' + str(client_address[client_address_index][5]) )

                    check_key()
                    format_fingerprint()

                    self.dial_out_cipher_bool_btn.setStyleSheet(button_stylesheet_red_text)
                    dial_out_dial_out_cipher_bool = False
                    self.dial_out_cipher_bool_btn.setEnabled(False)

                    if client_address[client_address_index][3] != '#' and len(client_address[client_address_index][3]) == 32:
                        print(str(datetime.datetime.now()) + ' -- address entry appears to have a key:', client_address[client_address_index][3])
                        if client_address[client_address_index][4] != '#' and len(client_address[client_address_index][4]) == 1024:
                            print(str(datetime.datetime.now()) + ' -- address entry appears to have a fingerprint:', client_address[client_address_index][4])
                            self.dial_out_cipher_bool_btn.setStyleSheet(button_stylesheet_green_text)
                            dial_out_dial_out_cipher_bool = True
                            self.dial_out_cipher_bool_btn.setEnabled(True)

                    sck_set_arguments_function()

                    print(str(datetime.datetime.now()) + ' -- dial_out_dial_out_cipher_bool:', dial_out_dial_out_cipher_bool)
            else:
                print(str(datetime.datetime.now()) + ' -- client_address unpopulated')

            print(str(datetime.datetime.now()) + ' -- current client_address updated')

        def client_next_address_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.client_next_address_function')
            global_self.setFocus()
            global client_address
            global client_address_index
            global dial_out_dial_out_cipher_bool

            self.dial_out_name.setText('')
            self.dial_out_ip_port.setText('')
            self.address_key.setText('')
            self.tb_fingerprint.setText('')

            print(str(datetime.datetime.now()) + ' -- len(client_address):', len(client_address))
            if len(client_address) > 0:
                if client_address_index == len(client_address) - 1:
                    client_address_index = 0
                else:
                    client_address_index += 1
                print(str(datetime.datetime.now()) + ' -- client_address_index setting client_address_index:', client_address_index)

                self.dial_out_name.setText(str(client_address[client_address_index][0]))

                if len(client_address[client_address_index]) >= 10:

                    print('client_address[client_address_index]:', client_address[client_address_index])
                    if 'x' == str(client_address[client_address_index][5]):
                        print(' -- skipping as [5] is x.')
                        self.dial_out_ip_port.setText(client_address[client_address_index][1] + ' ' + str(client_address[client_address_index][2]))
                    else:
                        print('-- using broadcast address')
                        self.dial_out_ip_port.setText(client_address[client_address_index][1] + ' ' + str(client_address[client_address_index][2]) + ' ' + str(client_address[client_address_index][5]))

                    check_key()
                    format_fingerprint()

                    self.dial_out_cipher_bool_btn.setStyleSheet(button_stylesheet_red_text)
                    dial_out_dial_out_cipher_bool = False
                    self.dial_out_cipher_bool_btn.setEnabled(False)

                    if client_address[client_address_index][3] != '#' and len(client_address[client_address_index][3]) == 32:
                        print(str(datetime.datetime.now()) + ' -- address entry appears to have a key:', client_address[client_address_index][3])
                        if client_address[client_address_index][4] != '#' and len(client_address[client_address_index][4]) == 1024:
                            print(str(datetime.datetime.now()) + ' -- address entry appears to have a fingerprint:', client_address[client_address_index][4])
                            self.dial_out_cipher_bool_btn.setStyleSheet(button_stylesheet_green_text)
                            dial_out_dial_out_cipher_bool = True
                            self.dial_out_cipher_bool_btn.setEnabled(True)

                    sck_set_arguments_function()

            else:
                print(str(datetime.datetime.now()) + ' -- client_address unpopulated')

            print(str(datetime.datetime.now()) + ' -- current client_address updated')

        def server_line_edit_return_pressed():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.server_line_edit_return_pressed')
            global_self.setFocus()
            global server_address
            global server_address_index
            global server_save_bool

            server_address_var = self.server_ip_port.text()

            if server_address_var != '':
                bool_address_match = False
                server_address_match_index = 0

                i = 0
                for _ in server_address:
                    if str(_[0] + ' ' + str(_[1])) == server_address_var:
                        bool_address_match = True
                        server_address_match_index = i
                    i += 1

                if bool_address_match is False:
                    print(str(datetime.datetime.now()) + ' -- new server address detected:', server_address_var)
                    server_address.append([server_address_var.split(' ')[0], int(server_address_var.split(' ')[1])])
                    server_address_index = len(server_address)-1
                    print(str(datetime.datetime.now()) + ' -- changing server_address_index to:', server_address_index)
                    self.server_status_label_ip_in_use.setText(str(server_address[server_address_index][0]) + ' ' + str(server_address[server_address_index][1]))
                    self.server_add_addr.setStyleSheet(button_stylesheet_white_text_high)
                    server_save_bool = True
                    self.server_add_addr.setEnabled(True)
                    server_thread.stop()
                    server_thread.start()

                else:
                    print(str(datetime.datetime.now()) + ' -- server address already exists:', server_address_var)
                    print('server_address_match_index:', server_address_match_index)
                    self.server_status_label_ip_in_use.setText(str(server_address[server_address_match_index][0]) + ' ' + str(server_address[server_address_match_index][1]))
                    server_address_index = server_address_match_index
                    self.server_add_addr.setStyleSheet(button_stylesheet_white_text_low)
                    server_save_bool = False
                    self.server_add_addr.setEnabled(False)
                    server_thread.stop()
                    server_thread.start()

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
                self.mute_server_notify_alien.setIcon(QIcon(mute_0))
                print(str(datetime.datetime.now()) + ' -- plugged in: App.mute_server_notify_alien_function setting mute:', mute_server_notify_alien_bool)
            elif mute_server_notify_alien_bool is False:
                mute_server_notify_alien_bool = True
                self.mute_server_notify_alien.setIcon(QIcon(mute_1))
                print(str(datetime.datetime.now()) + ' -- plugged in: App.mute_server_notify_alien_function setting mute:', mute_server_notify_alien_bool)

        def mute_server_notify_cipher_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.mute_server_notify_cipher_function')
            global mute_server_notify_cipher_bool
            if mute_server_notify_cipher_bool is True:
                mute_server_notify_cipher_bool = False
                self.mute_server_notify_cipher.setIcon(QIcon(mute_0))
                print(str(datetime.datetime.now()) + ' -- plugged in: App.mute_server_notify_alien_function setting mute:', mute_server_notify_cipher_bool)
            elif mute_server_notify_cipher_bool is False:
                mute_server_notify_cipher_bool = True
                self.mute_server_notify_cipher.setIcon(QIcon(mute_1))
                print(str(datetime.datetime.now()) + ' -- plugged in: App.mute_server_notify_alien_function setting mute:', mute_server_notify_cipher_bool)

        def server_save_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.server_save_function')
            global write_server_configuration_engaged
            global server_address
            global server_address_index
            global server_save_bool

            self.server_add_addr.setEnabled(False)

            if server_save_bool is True:

                if write_server_configuration_engaged is False:
                    write_server_configuration_engaged = True
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
                    non_success_write = []
                    if os.path.exists('./config.txt'):
                        with open('./config.txt', 'r') as fo:
                            i = 0
                            for line in fo:
                                line = line.strip()
                                print('-- comparing line:')
                                print('fo_line:      ', line)
                                print('fo_list_line: ', str(fo_list[i]))
                                if not line == fo_list[i]:
                                    non_success_write.append(False)
                                i += 1
                    if not False in non_success_write:
                        print('-- server address saved successfully')
                    else:
                        print('-- server address save failed')
                write_server_configuration_engaged = False
                self.server_add_addr.setStyleSheet(button_stylesheet_white_text_low)

        def server_delete_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.server_delete_function')
            global write_server_configuration_engaged
            global server_address
            global server_address_index

            if self.server_ip_port.text() != '':

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

        def dial_out_cipher_btn_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.dial_out_cipher_btn_function')
            global client_address
            global client_address_index
            global dial_out_dial_out_cipher_bool

            print('len(client_address[client_address_index][3]:', len(client_address[client_address_index][3]))
            print('len(client_address[client_address_index][4]:', len(client_address[client_address_index][4]))

            # First Check If The Address Entry HAS A Key And Fingerprint
            if client_address[client_address_index][3] != '#' and len(client_address[client_address_index][3]) == 32:
                print(str(datetime.datetime.now()) + ' -- address entry appears to have a key:', client_address[client_address_index][3])
                if client_address[client_address_index][4] != '#' and len(client_address[client_address_index][4]) == 1024:
                    print(str(datetime.datetime.now()) + ' -- address entry appears to have a fingerprint:', client_address[client_address_index][4])

                    if dial_out_dial_out_cipher_bool is False:
                        dial_out_dial_out_cipher_bool = True
                        self.dial_out_cipher_bool_btn.setStyleSheet(button_stylesheet_green_text)
                    elif dial_out_dial_out_cipher_bool is True:
                        dial_out_dial_out_cipher_bool = False
                        self.dial_out_cipher_bool_btn.setStyleSheet(button_stylesheet_red_text)
                    print(str(datetime.datetime.now()) + ' -- setting dial_out_dial_out_cipher_bool:', dial_out_dial_out_cipher_bool)

        def dial_out_override_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.dial_out_override_function')
            global client_address
            global client_address_index
            global bool_dial_out_override
            global address_override_string

            if bool_dial_out_override is True:
                bool_dial_out_override = False

                self.dial_override.setStyleSheet(button_stylesheet_default)
                self.address_book_label.setText('ADDRESS BOOK')
                self.dial_out_label.setText('TRANSMIT')

                self.dial_out_prev_addr.show()
                self.dial_out_next_addr.show()

                self.dial_out_add_addr.show()
                self.dial_out_rem_addr.show()

                self.dial_out_name.show()

                self.address_clear_form.show()

                if len(client_address) > 0:
                    self.dial_out_name.setText(client_address[client_address_index][0])
                    self.dial_out_ip_port.setText(client_address[client_address_index][1] + ' ' + str(client_address[client_address_index][2]))

                self.dial_out_cipher_bool_btn.show()

                self.address_key.show()
                self.address_key_label.show()
                self.address_fingerprint_label.show()
                self.tb_fingerprint.show()
                self.reveal_btn.show()
                self.dial_out_save_with_key.show()

                self.address_book_name_label.show()
                self.generate_fingerprint.show()
                self.generate_key.show()

                self.address_undo_form.show()

            elif bool_dial_out_override is False:
                bool_dial_out_override = True

                self.dial_override.setStyleSheet(button_stylesheet_red_text)
                self.address_book_label.setText('[ OVERRIDE ]')
                self.dial_out_label.setText('[ TRANSMIT OVERRIDE ]')

                self.dial_out_prev_addr.hide()
                self.dial_out_next_addr.hide()

                self.dial_out_add_addr.hide()
                self.dial_out_rem_addr.hide()

                self.dial_out_name.hide()
                self.dial_out_ip_port.setText(address_override_string)

                self.dial_out_cipher_bool_btn.hide()

                self.address_key_label.hide()
                self.address_key.hide()
                self.address_fingerprint_label.hide()
                self.tb_fingerprint.hide()
                self.reveal_btn.hide()
                self.dial_out_save_with_key.hide()

                self.address_clear_form.hide()

                self.address_book_name_label.hide()
                self.generate_fingerprint.hide()
                self.generate_key.hide()

                self.address_undo_form.hide()

            print(str(datetime.datetime.now()) + ' -- App.dial_out_override_function setting bool_dial_out_override:', bool_dial_out_override)

        def dial_out_ip_port_return_funtion():
            global bool_dial_out_override
            global address_override_string
            print(str(datetime.datetime.now()) + ' -- plugged in: App.dial_out_ip_port_return_funtion')
            if bool_dial_out_override is True:
                address_override_string = self.dial_out_ip_port.text()
                print(str(datetime.datetime.now()) + ' -- App.dial_out_ip_port_return_funtion setting address_override_string:', address_override_string)
            else:
                dial_out_name_check_details()

        def dial_out_name_return_funtion():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.dial_out_name_return_funtion')
            dial_out_name_check_details()

        def dial_out_name_check_details():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.dial_out_name_check_details')
            print(self.dial_out_name.text())
            print(self.dial_out_ip_port.text())
            var_dial_out_name = [str(self.dial_out_name.text()), str(self.dial_out_ip_port.text().split(' ')[0]), int(self.dial_out_ip_port.text().split(' ')[1]), bytes('x', 'utf-8'), str('x')]
            if var_dial_out_name not in client_address:
                print('-- basic name and ip not in client_address')

        def dial_out_save_with_key_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.dial_out_save_with_key_function')
            global address_save_mode
            global address_reveal_bool

            if address_save_mode is 'basic':
                address_save_mode = 'advanced'
                address_reveal_bool = True
                self.generate_key.setEnabled(True)
                self.generate_fingerprint.setEnabled(True)
                self.dial_out_save_with_key.setIcon(QIcon(advanced_save_1))
                self.generate_key.setStyleSheet(button_stylesheet_green_text)
                self.generate_fingerprint.setStyleSheet(button_stylesheet_green_text)
                self.dial_out_add_addr.setText('ADVANCED SAVE')
                self.dial_out_add_addr.setStyleSheet(button_stylesheet_green_text)
            elif address_save_mode is 'advanced':
                address_save_mode = 'basic'
                address_reveal_bool = False
                self.generate_key.setEnabled(False)
                self.generate_fingerprint.setEnabled(False)
                self.dial_out_save_with_key.setIcon(QIcon(advanced_save_0))
                self.generate_key.setStyleSheet(button_stylesheet_red_text)
                self.generate_fingerprint.setStyleSheet(button_stylesheet_red_text)
                self.dial_out_add_addr.setText('SAVE')
                self.dial_out_add_addr.setStyleSheet(button_stylesheet_white_text_high)
            print(str(datetime.datetime.now()) + ' -- setting address_save_mode:', address_save_mode)

        def format_fingerprint():
            global client_address
            global client_address_index
            print(str(datetime.datetime.now()) + ' -- plugged in: App.format_fingerprint')
            if address_reveal_bool is True:
                if len(client_address) > 0:
                    if len(client_address[client_address_index]) >= 10:
                        if len(client_address[client_address_index][4]) == 1024:
                            self.tb_fingerprint.setText('')
                            self.fingerprint_str = ''
                            finger_print_var = str(client_address[client_address_index][4])
                            self.fingerprint_str = finger_print_var
                            split_strings = [finger_print_var[index: index + 64] for index in range(0, len(finger_print_var), 64)]
                            print(split_strings)
                            for _ in split_strings:
                                self.tb_fingerprint.append(_)
                            self.tb_fingerprint.verticalScrollBar().setValue(0)

        def check_key():
            global address_reveal_bool
            global client_address
            global client_address_index
            print(str(datetime.datetime.now()) + ' -- plugged in: App.check_key')
            if address_reveal_bool is True:
                if len(client_address) > 0:
                    if len(client_address[client_address_index]) >= 10:
                        if client_address[client_address_index][3] != bytes('x', 'utf-8'):
                            self.address_key.setText(str(client_address[client_address_index][3], 'utf-8'))

        def address_clear_form_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.address_clear_form_function')
            self.dial_out_name.setText('')
            self.dial_out_ip_port.setText('')
            self.address_key.setText('')
            self.tb_fingerprint.setText('')

        def address_undo_form_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.address_undo_form_function')
            client_previous_address_function()
            client_next_address_function()

        def address_clear_form_sensitive_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.address_clear_form_sensitive_function')
            global address_reveal_bool
            global client_address
            global client_address_index

            print(str(datetime.datetime.now()) + ' -- address_reveal_bool is currently set at:', address_reveal_bool)

            if address_reveal_bool is True:
                address_reveal_bool = False
                self.address_key.setText('')
                self.tb_fingerprint.setText('')
                self.reveal_btn.setIcon(QIcon(visibility_0))

            elif address_reveal_bool is False:
                address_reveal_bool = True
                if len(client_address) > 0:
                    if len(client_address[client_address_index]) == 5:
                        if client_address[client_address_index][3] != bytes('x', 'utf-8'):
                            self.address_key.setText(str(client_address[client_address_index][3], 'utf-8'))
                        if client_address[client_address_index][4] != 'x':
                            format_fingerprint()
                self.reveal_btn.setIcon(QIcon(visibility_1))

            print(str(datetime.datetime.now()) + ' -- setting address_reveal_bool:', address_reveal_bool)

        def randStr(chars=string.ascii_uppercase + string.digits, N=32):
            return ''.join(random.choice(chars) for _ in range(N))

        def iter_rand():
            self.key_string = randStr(chars=string.ascii_lowercase + string.ascii_uppercase + string.punctuation.replace("'", "f"))
            self.fingerprint_str = self.fingerprint_str + self.key_string

        def generate_key_function():
            self.key_string = ''
            print(str(datetime.datetime.now()) + ' -- plugged in: App.generate_key_function')
            iter_rand()
            print(self.key_string)
            self.address_key.setText(self.key_string)
            print('self.address_key:', self.address_key.text())
            print('len(self.address_key):', len(self.address_key.text()))

        def generate_fingerprint_function():
            self.key_string = ''
            self.fingerprint_str = ''
            print(str(datetime.datetime.now()) + ' -- plugged in: App.generate_fingerprint_function')
            i = 0
            while i < 32:
                iter_rand()
                i += 1
            print(self.fingerprint_str)
            split_strings = [self.fingerprint_str[index: index + 64] for index in range(0, len(self.fingerprint_str), 64)]
            print(split_strings)
            self.tb_fingerprint.setText('')
            for _ in split_strings:
                self.tb_fingerprint.append(str(_).strip())
            self.tb_fingerprint.verticalScrollBar().setValue(0)
            
            print('fingerprint_str:', len(self.fingerprint_str))

        def bool_socket_options_function():
            print(str(datetime.datetime.now()) + ' -- plugged in: App.generate_fingerprint_function')
            global bool_socket_options
            if bool_socket_options is True:
                bool_socket_options = False
                self.bool_socket_options_btn.setStyleSheet(button_stylesheet_red_text)
            elif bool_socket_options is False:
                bool_socket_options = True
                self.bool_socket_options_btn.setStyleSheet(button_stylesheet_green_text)
            print(str(datetime.datetime.now()) + ' -- setting bool_socket_options:', bool_socket_options)

        # Window Title
        self.title = "Communicator"
        self.setWindowTitle('Communicator')
        self.setWindowIcon(QIcon('./resources/image/icon.ico'))

        # Window Geometry
        self.width, self.height = 1132, 426
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
        self.btn_100 = 100
        self.btn_120 = 120
        self.btn_140 = 140
        self.btn_180 = 180
        self.btn_240 = 240
        self.btn_280 = 280
        self.btn_360 = 360

        # ##########################################################################################################

        self.server_status_label = QLabel(self)
        self.server_status_label.move(4, 28)
        self.server_status_label.resize(self.width - 8, 20)
        self.server_status_label.setFont(self.font_s7b)
        self.server_status_label.setText('SERVER STATUS:  OFFLINE')
        self.server_status_label.setAlignment(Qt.AlignCenter)
        self.server_status_label.setStyleSheet(title_stylesheet_default)

        self.server_status_label_ip_in_use = QLabel(self)
        self.server_status_label_ip_in_use.move((self.width / 2) - (self.btn_240 / 2), 52)
        self.server_status_label_ip_in_use.resize(self.btn_240, 20)
        self.server_status_label_ip_in_use.setFont(self.font_s7b)
        self.server_status_label_ip_in_use.setText('')
        self.server_status_label_ip_in_use.setAlignment(Qt.AlignCenter)
        self.server_status_label_ip_in_use.setStyleSheet(label_stylesheet_black_bg_text_white)

        self.server_start = QPushButton(self)
        self.server_start.move((self.width / 2) - (self.btn_60 / 2), 4)
        self.server_start.resize(self.btn_60, self.btn_20)
        self.server_start.setIcon(QIcon(play_green))
        self.server_start.setIconSize(QSize(9, 9))
        self.server_start.setStyleSheet(button_stylesheet_red_text)
        self.server_start.clicked.connect(start_function)

        self.server_stop = QPushButton(self)
        self.server_stop.move((self.width / 2) - (self.btn_240 / 2), 4)
        self.server_stop.resize(self.btn_60, self.btn_20)
        self.server_stop.setIcon(QIcon(stop_red))
        self.server_stop.setIconSize(QSize(9, 9))
        self.server_stop.setStyleSheet(button_stylesheet_red_text)
        self.server_stop.clicked.connect(stop_function)

        self.server_restart = QPushButton(self)
        self.server_restart.move((self.width / 2) + (self.btn_240 / 2) - self.btn_60, 4)
        self.server_restart.resize(self.btn_60, self.btn_20)
        self.server_restart.setIcon(QIcon(replay_yellow))
        self.server_restart.setIconSize(QSize(9, 9))
        self.server_restart.setStyleSheet(button_stylesheet_red_text)
        self.server_restart.clicked.connect(restart_function)

        self.server_ip_port = QLineEdit(self)
        self.server_ip_port.move((self.width / 2) - (self.btn_240 / 2), 76)
        self.server_ip_port.resize(self.btn_240, 20)
        self.server_ip_port.returnPressed.connect(server_line_edit_return_pressed)
        self.server_ip_port.setFont(self.font_s7b)
        self.server_ip_port.setText('')
        self.server_ip_port.setStyleSheet(line_edit_stylesheet_white_text)
        self.server_ip_port.setAlignment(Qt.AlignCenter)

        self.server_prev_addr = QPushButton(self)
        self.server_prev_addr.move((self.width / 2) - (self.btn_240 / 2) - self.btn_20 - self.btn_4, 76)
        self.server_prev_addr.resize(self.btn_20, 20)
        self.server_prev_addr.setIcon(QIcon(arrow_left))
        self.server_prev_addr.setIconSize(QSize(20, 20))
        self.server_prev_addr.setStyleSheet(button_stylesheet_default)
        self.server_prev_addr.clicked.connect(server_prev_addr_function)

        self.server_next_addr = QPushButton(self)
        self.server_next_addr.move((self.width / 2) + (self.btn_240 / 2) + self.btn_4, 76)
        self.server_next_addr.resize(20, 20)
        self.server_next_addr.setIcon(QIcon(arrow_right))
        self.server_next_addr.setIconSize(QSize(20, 20))
        self.server_next_addr.setStyleSheet(button_stylesheet_default)
        self.server_next_addr.clicked.connect(server_next_addr_function)

        self.server_add_addr = QPushButton(self)
        self.server_add_addr.move((self.width / 2) - (self.btn_240 / 2), 104)
        self.server_add_addr.resize(60, int(self.btn_40 / 2))
        self.server_add_addr.setFont(self.font_s7b)
        self.server_add_addr.setText('SAVE')
        self.server_add_addr.setStyleSheet(button_stylesheet_white_text_low)
        self.server_add_addr.clicked.connect(server_save_function)

        self.server_rem_addr = QPushButton(self)
        self.server_rem_addr.move((self.width / 2) + (self.btn_240 / 2) - self.btn_60, 104)
        self.server_rem_addr.resize(self.btn_60, int(self.btn_40 / 2))
        self.server_rem_addr.setFont(self.font_s7b)
        self.server_rem_addr.setText('DELETE')
        self.server_rem_addr.setIconSize(QSize(14, 14))
        self.server_rem_addr.setStyleSheet(button_stylesheet_default)
        self.server_rem_addr.clicked.connect(server_delete_function)

        self.server_incoming = QPushButton(self)
        self.server_incoming.move(self.width - 72, 52)
        self.server_incoming.resize(68, 68)
        self.server_incoming.setIcon(QIcon(server_public_off))
        self.server_incoming.setIconSize(QSize(48, 48))
        self.server_incoming.setStyleSheet(button_stylesheet_background_matching)

        self.soft_block_ip_notification = QPushButton(self)
        self.soft_block_ip_notification.move(self.width - 136, 100)
        self.soft_block_ip_notification.resize(60, 20)
        self.soft_block_ip_notification.setText(str(soft_block_ip_count))
        self.soft_block_ip_notification.setStyleSheet(button_stylesheet_red_text)
        self.soft_block_ip_notification.clicked.connect(soft_block_ip_notofication_function)

        self.server_notify_alien = QPushButton(self)
        self.server_notify_alien.move(self.width - 136, 76)
        self.server_notify_alien.resize(60, int(self.btn_40 / 2))
        self.server_notify_alien.setStyleSheet(button_stylesheet_amber_text)
        self.server_notify_alien.setFont(self.font_s7b)
        self.server_notify_alien.setText(str(alien_message_count))
        self.server_notify_alien.clicked.connect(server_notify_alien_function)

        self.server_notify_cipher = QPushButton(self)
        self.server_notify_cipher.move(self.width - 136, 52)
        self.server_notify_cipher.resize(60, int(self.btn_40 / 2))
        self.server_notify_cipher.setStyleSheet(button_stylesheet_white_text_high)
        self.server_notify_cipher.setFont(self.font_s7b)
        self.server_notify_cipher.setText(str(cipher_message_count))
        self.server_notify_cipher.clicked.connect(server_notify_cipher_function)

        self.mute_server_notify_cipher = QPushButton(self)
        self.mute_server_notify_cipher.move(self.width - 200, 52)
        self.mute_server_notify_cipher.resize(60, int(self.btn_40 / 2))
        self.mute_server_notify_cipher.setStyleSheet(button_stylesheet_default)
        self.mute_server_notify_cipher.setIcon(QIcon(mute_0))
        self.mute_server_notify_cipher.setIconSize(QSize(14, 14))
        self.mute_server_notify_cipher.clicked.connect(mute_server_notify_cipher_function)

        self.mute_server_notify_alien = QPushButton(self)
        self.mute_server_notify_alien.move(self.width - 200, 76)
        self.mute_server_notify_alien.resize(60, int(self.btn_40 / 2))
        self.mute_server_notify_alien.setStyleSheet(button_stylesheet_amber_text)
        self.mute_server_notify_alien.setIcon(QIcon(mute_0))
        self.mute_server_notify_alien.setIconSize(QSize(14, 14))
        self.mute_server_notify_alien.clicked.connect(mute_server_notify_alien_function)

        # ##########################################################################################################

        self.address_book_label = QLabel(self)
        self.address_book_label.move(4, 140)
        self.address_book_label.resize(self.width - 8, 20)
        self.address_book_label.setFont(self.font_s7b)
        self.address_book_label.setText('ADDRESS BOOK')
        self.address_book_label.setAlignment(Qt.AlignCenter)
        self.address_book_label.setStyleSheet(title_stylesheet_default)

        self.dial_out_encoding = QLabel(self)
        self.dial_out_encoding.move(32, 168)
        self.dial_out_encoding.resize(self.btn_120, 20)
        self.dial_out_encoding.setFont(self.font_s7b)
        self.dial_out_encoding.setText('ENCODING')
        self.dial_out_encoding.setAlignment(Qt.AlignCenter)
        self.dial_out_encoding.setStyleSheet(title_stylesheet_default)

        self.codec_select_box = QComboBox(self)
        self.codec_select_box.move(32 + self.btn_120 + 4, 168)
        self.codec_select_box.resize(186, 20)
        self.codec_select_box.setStyleSheet(cmb_menu_style)
        self.codec_select_box.setFont(self.font_s7b)
        self.codec_select_box.addItem('Unselected')
        communicator_codecs = encodings._aliases
        for k, v in communicator_codecs.items():
            self.codec_select_box.addItem(str(str(k).strip() + ' ' + str(v).strip()))

        self.dial_out_family_type = QLabel(self)
        self.dial_out_family_type.move(32, 168 + 24)
        self.dial_out_family_type.resize(self.btn_120, 20)
        self.dial_out_family_type.setFont(self.font_s7b)
        self.dial_out_family_type.setText('ADDRESS FAMILY')
        self.dial_out_family_type.setAlignment(Qt.AlignCenter)
        self.dial_out_family_type.setStyleSheet(title_stylesheet_default)

        self.communicator_socket_options_box_0 = QComboBox(self)
        self.communicator_socket_options_box_0.move(32 + self.btn_120 + 4, 168 + 24)
        self.communicator_socket_options_box_0.resize(186, 20)
        self.communicator_socket_options_box_0.setStyleSheet(cmb_menu_style)
        self.communicator_socket_options_box_0.setFont(self.font_s7b)
        self.communicator_socket_options_box_0.addItem('Unselected')
        for v in COMMUNICATOR_SOCK:
            self.communicator_socket_options_box_0.addItem(str(v))

        self.dial_out_socket_type = QLabel(self)
        self.dial_out_socket_type.move(32, 168 + 24 + 24)
        self.dial_out_socket_type.resize(self.btn_120, 20)
        self.dial_out_socket_type.setFont(self.font_s7b)
        self.dial_out_socket_type.setText('SOCKET TYPE')
        self.dial_out_socket_type.setAlignment(Qt.AlignCenter)
        self.dial_out_socket_type.setStyleSheet(title_stylesheet_default)

        self.communicator_socket_options_box_1 = QComboBox(self)
        self.communicator_socket_options_box_1.move(32 + self.btn_120 + 4, 168 + 24 + 24)
        self.communicator_socket_options_box_1.resize(186, 20)
        self.communicator_socket_options_box_1.setStyleSheet(cmb_menu_style)
        self.communicator_socket_options_box_1.setFont(self.font_s7b)
        self.communicator_socket_options_box_1.addItem('Unselected')
        for v in COMMUNICATOR_SOCK:
            self.communicator_socket_options_box_1.addItem(str(v))

        self.bool_socket_options_btn = QPushButton(self)
        self.bool_socket_options_btn.move(32, 168 + 24 + 24 + 24)
        self.bool_socket_options_btn.resize(self.btn_120, self.btn_20)
        self.bool_socket_options_btn.setStyleSheet(button_stylesheet_red_text)
        self.bool_socket_options_btn.setText('SOCKET OPTIONS')
        self.bool_socket_options_btn.setFont(self.font_s7b)
        self.bool_socket_options_btn.clicked.connect(bool_socket_options_function)

        self.communicator_socket_options_box_2 = QComboBox(self)
        self.communicator_socket_options_box_2.move(32 + self.btn_120 + 4, 168 + 24 + 24 + 24)
        self.communicator_socket_options_box_2.resize(186, 20)
        self.communicator_socket_options_box_2.setStyleSheet(cmb_menu_style)
        self.communicator_socket_options_box_2.setFont(self.font_s7b)
        self.communicator_socket_options_box_2.addItem('Unselected')
        for v in COMMUNICATOR_SOCK:
            self.communicator_socket_options_box_2.addItem(str(v))

        self.communicator_socket_options_box_3 = QComboBox(self)
        self.communicator_socket_options_box_3.move(32 + self.btn_120 + 4, 168 + 24 + 24 + 24 + 24)
        self.communicator_socket_options_box_3.resize(186, 20)
        self.communicator_socket_options_box_3.setStyleSheet(cmb_menu_style)
        self.communicator_socket_options_box_3.setFont(self.font_s7b)
        self.communicator_socket_options_box_3.addItem('Unselected')
        for v in COMMUNICATOR_SOCK:
            self.communicator_socket_options_box_3.addItem(str(v))

        self.reveal_btn = QPushButton(self)
        self.reveal_btn.move((self.width / 2) + (self.btn_240 / 2) - self.btn_120 + 2, 168)
        self.reveal_btn.resize(self.btn_120 - 2, self.btn_20)
        self.reveal_btn.setIcon(QIcon(visibility_0))
        self.reveal_btn.setIconSize(QSize(self.btn_20 - 8, self.btn_20 - 8))
        self.reveal_btn.setFont(self.font_s7b)
        self.reveal_btn.setStyleSheet(button_stylesheet_white_text_low)
        self.reveal_btn.clicked.connect(address_clear_form_sensitive_function)

        self.address_clear_form = QPushButton(self)
        self.address_clear_form.move((self.width / 2) - (self.btn_240 / 2), 168)
        self.address_clear_form.resize(self.btn_120 - 2, self.btn_20)
        self.address_clear_form.setIcon(QIcon(clear_all))
        self.address_clear_form.setIconSize(QSize(self.btn_20 - 8, self.btn_20 - 8))
        self.address_clear_form.setFont(self.font_s7b)
        self.address_clear_form.setStyleSheet(button_stylesheet_white_text_high)
        self.address_clear_form.clicked.connect(address_clear_form_function)

        self.address_undo_form = QPushButton(self)
        self.address_undo_form.move((self.width / 2) - (self.btn_240 / 2) - self.btn_4 - self.btn_80, 168)
        self.address_undo_form.resize(self.btn_80, self.btn_20)
        self.address_undo_form.setIcon(QIcon(undo_white))
        self.address_undo_form.setIconSize(QSize(self.btn_20 - 8, self.btn_20 - 8))
        self.address_undo_form.setFont(self.font_s7b)
        self.address_undo_form.setStyleSheet(button_stylesheet_white_text_high)
        self.address_undo_form.clicked.connect(address_undo_form_function)

        self.address_book_name_label = QLabel(self)
        self.address_book_name_label.move((self.width / 2) - (self.btn_240 / 2) - self.btn_4 - self.btn_80, 196)
        self.address_book_name_label.resize(self.btn_80, 20)
        self.address_book_name_label.setFont(self.font_s7b)
        self.address_book_name_label.setText('NAME')
        self.address_book_name_label.setAlignment(Qt.AlignCenter)
        self.address_book_name_label.setStyleSheet(title_stylesheet_default)

        self.dial_out_name = QLineEdit(self)
        self.dial_out_name.move((self.width / 2) - (self.btn_240 / 2), 196)
        self.dial_out_name.resize(self.btn_240, 20)
        self.dial_out_name.setFont(self.font_s7b)
        self.dial_out_name.setText('')
        self.dial_out_name.setStyleSheet(line_edit_stylesheet_white_text)
        self.dial_out_name.setAlignment(Qt.AlignCenter)
        self.dial_out_name.returnPressed.connect(dial_out_name_return_funtion)

        self.address_book_address_label = QLabel(self)
        self.address_book_address_label.move((self.width / 2) - (self.btn_240 / 2) - self.btn_4 - self.btn_80, 220)
        self.address_book_address_label.resize(self.btn_80, 20)
        self.address_book_address_label.setFont(self.font_s7b)
        self.address_book_address_label.setText('ADDRESS')
        self.address_book_address_label.setAlignment(Qt.AlignCenter)
        self.address_book_address_label.setStyleSheet(title_stylesheet_default)

        self.dial_out_ip_port = QLineEdit(self)
        self.dial_out_ip_port.move((self.width / 2) - (self.btn_240 / 2), 220)
        self.dial_out_ip_port.resize(self.btn_240, 20)
        self.dial_out_ip_port.setFont(self.font_s7b)
        self.dial_out_ip_port.setText('')
        self.dial_out_ip_port.setStyleSheet(line_edit_stylesheet_white_text)
        self.dial_out_ip_port.setAlignment(Qt.AlignCenter)
        self.dial_out_ip_port.returnPressed.connect(dial_out_ip_port_return_funtion)

        self.generate_fingerprint = QPushButton(self)
        self.generate_fingerprint.move(self.width - self.btn_4 - self.btn_20 - 4 - 24, 188 + 4)
        self.generate_fingerprint.resize(self.btn_20, self.btn_20)
        self.generate_fingerprint.setText('+')
        self.generate_fingerprint.setFont(self.font_s7b)
        self.generate_fingerprint.setStyleSheet(button_stylesheet_red_text)
        self.generate_fingerprint.clicked.connect(generate_fingerprint_function)
        self.generate_fingerprint.setEnabled(False)

        self.generate_key = QPushButton(self)
        self.generate_key.move(self.width - self.btn_4 - self.btn_20 - 4 - 24, 164 + 4)
        self.generate_key.resize(self.btn_20, self.btn_20)
        self.generate_key.setText('+')
        self.generate_key.setFont(self.font_s7b)
        self.generate_key.setStyleSheet(button_stylesheet_red_text)
        self.generate_key.clicked.connect(generate_key_function)
        self.generate_key.setEnabled(False)

        self.address_fingerprint_label = QLabel(self)
        self.address_fingerprint_label.move(self.width - self.btn_360 - self.btn_4 - self.btn_20 - 8, 188 + 4)
        self.address_fingerprint_label.resize(338, 20)
        self.address_fingerprint_label.setFont(self.font_s7b)
        self.address_fingerprint_label.setText('FINGERPRINT')
        self.address_fingerprint_label.setAlignment(Qt.AlignCenter)
        self.address_fingerprint_label.setStyleSheet(title_stylesheet_default)

        self.tb_fingerprint = QTextBrowser(self)
        self.tb_fingerprint.move(self.width - self.btn_360 - self.btn_4 - self.btn_20 - 8, 208 + 4)
        self.tb_fingerprint.resize(self.btn_360, 72)
        self.tb_fingerprint.setObjectName("tb_fingerprint")
        self.tb_fingerprint.setFont(self.font_s7b)
        self.tb_fingerprint.setStyleSheet(textbox_stylesheet_black_bg)
        self.tb_fingerprint.setLineWrapMode(QTextBrowser.NoWrap)
        self.tb_fingerprint.horizontalScrollBar().setValue(0)
        self.tb_fingerprint.verticalScrollBar().setValue(0)

        self.address_key_label = QLabel(self)
        self.address_key_label.move(self.width - self.btn_360 - self.btn_4 - self.btn_20 - 8, 164 + 4)
        self.address_key_label.resize(self.btn_80 - 4, 20)
        self.address_key_label.setFont(self.font_s7b)
        self.address_key_label.setText('KEY')
        self.address_key_label.setAlignment(Qt.AlignCenter)
        self.address_key_label.setStyleSheet(title_stylesheet_default)

        self.address_key = QLineEdit(self)
        self.address_key.move(self.width - self.btn_280 - self.btn_4 - self.btn_20 - 8, 164 + 4)
        self.address_key.resize(258, 20)
        self.address_key.setFont(self.font_s7b)
        self.address_key.setStyleSheet(line_edit_stylesheet_white_text)

        self.dial_out_save_with_key = QPushButton(self)
        self.dial_out_save_with_key.move(self.width - self.btn_360 - self.btn_4 - self.btn_20 - self.btn_4 - self.btn_20 - 8, 164 + 4)
        self.dial_out_save_with_key.resize(self.btn_20, 116)
        self.dial_out_save_with_key.setIcon(QIcon(advanced_save_0))
        self.dial_out_save_with_key.setIconSize(QSize(20, 20))
        self.dial_out_save_with_key.setStyleSheet(button_stylesheet_white_text_low)
        self.dial_out_save_with_key.clicked.connect(dial_out_save_with_key_function)

        self.dial_out_prev_addr = QPushButton(self)
        self.dial_out_prev_addr.move(4, 164 + 4)
        self.dial_out_prev_addr.resize(20, 116)
        self.dial_out_prev_addr.setIcon(QIcon(arrow_left))
        self.dial_out_prev_addr.setIconSize(QSize(20, 20))
        self.dial_out_prev_addr.setStyleSheet(button_stylesheet_default)
        self.dial_out_prev_addr.clicked.connect(client_previous_address_function)

        self.dial_out_next_addr = QPushButton(self)
        self.dial_out_next_addr.move(self.width - self.btn_20 - self.btn_4, 164 + 4)
        self.dial_out_next_addr.resize(20, 116)
        self.dial_out_next_addr.setIcon(QIcon(arrow_right))
        self.dial_out_next_addr.setIconSize(QSize(20, 20))
        self.dial_out_next_addr.setStyleSheet(button_stylesheet_default)
        self.dial_out_next_addr.clicked.connect(client_next_address_function)

        self.dial_out_add_addr = QPushButton(self)
        self.dial_out_add_addr.move((self.width / 2) - (self.btn_240 / 2), 248)
        self.dial_out_add_addr.resize(self.btn_120 - 2, 20)
        self.dial_out_add_addr.setFont(self.font_s7b)
        self.dial_out_add_addr.setText('SAVE')
        self.dial_out_add_addr.setStyleSheet(button_stylesheet_default)
        self.dial_out_add_addr.clicked.connect(client_save_address)
        self.dial_out_add_addr.setEnabled(True)

        self.dial_out_rem_addr = QPushButton(self)
        self.dial_out_rem_addr.move((self.width / 2) + (self.btn_240 / 2) - self.btn_120 + 2, 248)
        self.dial_out_rem_addr.resize(self.btn_120 - 2, 20)
        self.dial_out_rem_addr.setFont(self.font_s7b)
        self.dial_out_rem_addr.setText('DELETE')
        self.dial_out_rem_addr.setStyleSheet(button_stylesheet_default)
        self.dial_out_rem_addr.clicked.connect(client_remove_address)

        # ##########################################################################################################

        self.dial_out_label = QLabel(self)
        self.dial_out_label.move(4, 292)
        self.dial_out_label.resize(self.width - 8, 20)
        self.dial_out_label.setFont(self.font_s7b)
        self.dial_out_label.setText('TRANSMIT')
        self.dial_out_label.setAlignment(Qt.AlignCenter)
        self.dial_out_label.setStyleSheet(title_stylesheet_default)

        self.dial_override = QPushButton(self)
        self.dial_override.move((self.width / 2) - (self.btn_240 / 2), 334)
        self.dial_override.resize(self.btn_60, self.btn_20)
        self.dial_override.setStyleSheet(button_stylesheet_white_text_high)
        self.dial_override.setText('OVERRIDE')
        self.dial_override.setFont(self.font_s7b)
        self.dial_override.clicked.connect(dial_out_override_function)

        self.dial_out_message = QLineEdit(self)
        self.dial_out_message.move((self.width / 2) - (self.btn_240 / 2), 356)
        self.dial_out_message.resize(self.btn_240, self.btn_20)
        self.dial_out_message.setFont(self.font_s7b)
        self.dial_out_message.setText('')
        self.dial_out_message.setStyleSheet(line_edit_stylesheet_white_text)

        self.dial_out_message_send = QPushButton(self)
        self.dial_out_message_send.move((self.width / 2) + (self.btn_240 / 2) + self.btn_4, 356)
        self.dial_out_message_send.resize(self.btn_60, self.btn_20)
        self.dial_out_message_send.setIcon(QIcon(send_white))
        self.dial_out_message_send.setIconSize(QSize(self.btn_20, self.btn_20))
        self.dial_out_message_send.setStyleSheet(button_stylesheet_default)
        self.dial_out_message_send.clicked.connect(send_message_function)

        self.dial_out_cipher_bool_btn = QPushButton(self)
        self.dial_out_cipher_bool_btn.move((self.width / 2) + (self.btn_240 / 2) + self.btn_4, 332)
        self.dial_out_cipher_bool_btn.resize(self.btn_60, self.btn_20)
        self.dial_out_cipher_bool_btn.setText('CIPHER')
        self.dial_out_cipher_bool_btn.setFont(self.font_s7b)
        self.dial_out_cipher_bool_btn.setStyleSheet(button_stylesheet_green_text)
        self.dial_out_cipher_bool_btn.clicked.connect(dial_out_cipher_btn_function)

        # ##########################################################################################################

        # Thread - Public Server
        server_thread = ServerClass(self.server_incoming, self.server_status_label, self.soft_block_ip_notification, self.server_status_label_ip_in_use, self.server_start)

        # Thread - ServerDataHandlerClass
        server_data_handler_class = ServerDataHandlerClass(self.server_incoming, self.server_notify_cipher, self.server_notify_alien)
        server_data_handler_class.start()

        # Thread - Dial_Out
        dial_out_thread = DialOutClass(self.dial_out_message_send, self.dial_out_message, self.dial_out_ip_port, self.codec_select_box,
                                       self.communicator_socket_options_box_0,
                                       self.communicator_socket_options_box_1,
                                       self.communicator_socket_options_box_2,
                                       self.communicator_socket_options_box_3)

        # Thread - Configuration
        global configuration_thread
        configuration_thread_ = ConfigurationClass()
        configuration_thread.append(configuration_thread_)
        configuration_thread[0].start()

        # Configuration Thread - Wait For Configuration Thread To Complete
        global configuration_thread_completed
        print(str(datetime.datetime.now()) + ' configuration_thread_completed:', configuration_thread_completed)
        while configuration_thread_completed is False:
            time.sleep(1)
        print(str(datetime.datetime.now()) + ' configuration_thread_completed:', configuration_thread_completed)

        if len(server_address) > 0:
            self.server_ip_port.setText(server_address[0][0] + ' ' + str(server_address[0][1]))
            self.server_status_label_ip_in_use.setText(str(server_address[0][0] + ' ' + str(server_address[0][1])))

        global client_address
        global dial_out_dial_out_cipher_bool

        self.dial_out_cipher_bool_btn.setStyleSheet(button_stylesheet_red_text)
        dial_out_dial_out_cipher_bool = False
        self.dial_out_cipher_bool_btn.setEnabled(False)

        if len(client_address) > 0:
            self.dial_out_name.setText(client_address[0][0])
            self.dial_out_ip_port.setText(client_address[0][1] + ' ' + str(client_address[0][2]))
            if client_address[0][5] != 'x':
                print(str(datetime.datetime.now()) + ' -- address entry appears to have a broadcast address:', client_address[0][5])
                self.dial_out_ip_port.setText(client_address[0][1] + ' ' + str(client_address[0][2]) + ' ' + str(client_address[0][5]))

            if client_address[0][3] != 'x' and len(client_address[0][3]) == 32:
                print(str(datetime.datetime.now()) + ' -- address entry appears to have a key:', client_address[0][3])
                if client_address[client_address_index][4] != '#' and len(client_address[client_address_index][4]) == 1024:
                    print(str(datetime.datetime.now()) + ' -- address entry appears to have a fingerprint:', client_address[client_address_index][4])
                    self.dial_out_cipher_bool_btn.setStyleSheet(button_stylesheet_green_text)
                    dial_out_dial_out_cipher_bool = True
                    self.dial_out_cipher_bool_btn.setEnabled(True)

            try:
                sck_set_arguments_function()
            except Exception as e:
                print(str(datetime.datetime.now()) + ' -- handled error setting advanced socket options on the frontend:', e)

            print(str(datetime.datetime.now()) + ' -- dial_out_dial_out_cipher_bool:', dial_out_dial_out_cipher_bool)

        self.tb_0 = QTextBrowser(self)
        self.tb_0.move(4, 52)
        self.tb_0.resize(400, 84)
        self.tb_0.setObjectName("tb_0")
        self.tb_0.setFont(self.font_s7b)
        self.tb_0.setStyleSheet(textbox_stylesheet_default)
        self.tb_0.setLineWrapMode(QTextBrowser.NoWrap)
        self.tb_0.horizontalScrollBar().setValue(0)

        # QTimer - Used For Appending Output To tb_0 Using QtSlots
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
            print('internal_message_system received message:', internal_messages[-1])


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
                    print('len(line):', len(line))
                    if len(line) == 12:
                        client_address.append([str(line[1]), str(line[2]), int(line[3]), bytes(line[4], 'utf-8'), str(line[5]), str(line[6]), str(line[7]), str(line[8]), str(line[9]), str(line[10]), str(line[11])])
                        print('entry:', client_address[-1])

        client_address.sort(key=lambda x: x[0])
        print('sort complete')

        for _ in client_address:
            print('handling:', _)
            if os.path.exists(_[4]):
                print('path found:', _[4])
                address_fingerprint_string = ''
                with open(_[4], 'r') as fo:
                    for line in fo:
                        line = line.strip()
                        address_fingerprint_string = address_fingerprint_string + line
                fo.close()
                _[4] = address_fingerprint_string
            print('sorted:', _)

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
    def __init__(self, dial_out_message_send, dial_out_message, dial_out_ip_port, codec_select_box,
                 communicator_socket_options_box_0,
                 communicator_socket_options_box_1,
                 communicator_socket_options_box_2,
                 communicator_socket_options_box_3):
        QThread.__init__(self)

        self.dial_out_message_send = dial_out_message_send
        self.dial_out_message = dial_out_message
        self.dial_out_ip_port = dial_out_ip_port

        self.codec_select_box = codec_select_box
        self.communicator_socket_options_box_0 = communicator_socket_options_box_0
        self.communicator_socket_options_box_1 = communicator_socket_options_box_1
        self.communicator_socket_options_box_2 = communicator_socket_options_box_2
        self.communicator_socket_options_box_3 = communicator_socket_options_box_3

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
        global address_override_string

        print(str(datetime.datetime.now()) + ' -- DialOutClass.run bool_dial_out_override:', bool_dial_out_override)

        if bool_dial_out_override is True:
            print(str(datetime.datetime.now()) + ' -- DialOutClass.run using address_override_string:', address_override_string)
            self.HOST_SEND = address_override_string.split(' ')[0]
            self.PORT_SEND = int(address_override_string.split(' ')[1])
            self.KEY = bytes('#', 'utf-8')
            self.FINGERPRINT = bytes('#', 'utf-8')
            self.MESSAGE_CONTENT = str(self.dial_out_message.text())

        elif bool_dial_out_override is False:
            print(str(datetime.datetime.now()) + ' -- DialOutClass.run using client_address_index:', client_address_index)
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
        global bool_dial_out_override
        global bool_socket_options

        print('-' * 200)
        print(str(datetime.datetime.now()) + f" -- DialOutClass.message_send outgoing to: {self.HOST_SEND} : {self.PORT_SEND}")

        try:
            data_response = ''
            if len(client_address[client_address_index]) >= 10:

                # Setup Socket
                sok = socket.socket(COMMUNICATOR_SOCK.get(self.communicator_socket_options_box_0.currentText()), COMMUNICATOR_SOCK.get(self.communicator_socket_options_box_1.currentText()))
                print('-- variably setting socket as:', sok)

                # Setup Socket Options
                if bool_socket_options is True:
                    sok.setsockopt(COMMUNICATOR_SOCK.get(self.communicator_socket_options_box_2.currentText()), COMMUNICATOR_SOCK.get(self.communicator_socket_options_box_3.currentText()), 1)
                    print('-- variably setting socket options:', sok)

                with sok as SOCKET_DIAL_OUT:
                    if client_address[client_address_index][5] == 'x':
                        print('-- using address ip/mac:', self.HOST_SEND)
                        SOCKET_DIAL_OUT.connect((self.HOST_SEND, self.PORT_SEND))
                    else:
                        print('-- using broadcast address:', client_address[client_address_index][5])
                        SOCKET_DIAL_OUT.connect((str(client_address[client_address_index][5]), self.PORT_SEND))

                    if dial_out_dial_out_cipher_bool is True and bool_dial_out_override is False:
                        print(str(datetime.datetime.now()) + ' -- DialOutClass.message_send: handing message to AESCipher')
                        print(str(datetime.datetime.now()) + ' -- DialOutClass.message_send using KEY:', self.KEY)
                        print(str(datetime.datetime.now()) + ' -- DialOutClass.message_send using FINGERPRINT:', self.FINGERPRINT)
                        cipher = AESCipher(self.KEY)
                        ciphertext = cipher.encrypt(str(self.FINGERPRINT) + self.MESSAGE_CONTENT)
                        print(str(datetime.datetime.now()) + ' -- DialOutClass.message_send ciphertext:', str(ciphertext))
                        textbox_0_messages.append('[' + str(datetime.datetime.now()) + '] [SENDING ENCRYPTED] [' + str(self.HOST_SEND) + ':' + str(self.PORT_SEND) + ']')
                    else:
                        ciphertext = bytes(self.MESSAGE_CONTENT, str(client_address[client_address_index][6]).split('______')[1])
                        textbox_0_messages.append('[' + str(datetime.datetime.now()) + '] [SENDING UNENCRYPTED] [' + str(self.HOST_SEND) + ':' + str(self.PORT_SEND) + ']')

                    print(str(datetime.datetime.now()) + ' -- DialOutClass.message_send: attempting to send ciphertext')

                    SOCKET_DIAL_OUT.send(ciphertext)
                    SOCKET_DIAL_OUT.settimeout(1)

                    print(str(datetime.datetime.now()) + ' -- DialOutClass.message_send: waiting for response from recipient')

                    try:
                        data_response = SOCKET_DIAL_OUT.recv(2048)
                    except Exception as e:
                        print(str(datetime.datetime.now()) + ' -- DialOutClass.message_send:', e)
                        self.data = '[' + str(datetime.datetime.now()) + '] [EXCEPTION HANDLED DURING WAITING FOR RESPONSE] [' + str(self.HOST_SEND) + ':' + str(self.PORT_SEND) + ']'
                        textbox_0_messages.append(self.data)
                        self.dial_out_logger()

                if data_response == ciphertext:
                    self.dial_out_message.setText('')
                    self.data = '[' + str(datetime.datetime.now()) + '] [DELIVERY CONFIRMATION] [' + str(self.HOST_SEND) + ':' + str(self.PORT_SEND) + ']'
                    textbox_0_messages.append(self.data)

                    print(str(datetime.datetime.now()) + ' -- DialOutClass.message_send response from recipient equals ciphertext:', data_response)
                    self.dial_out_message_send.setIcon(QIcon(send_green))
                    time.sleep(1)
                    self.dial_out_message_send.setIcon(QIcon(send_white))

                else:
                    self.dial_out_message.setText('')
                    self.data = '[' + str(datetime.datetime.now()) + '] [WARNING] [MESSAGE RECEIVED DOES NOT MATCH MESSAGE SENT] [' + str(self.HOST_SEND) + ':' + str(self.PORT_SEND) + '] ' + str(data_response)
                    print(self.data)
                    textbox_0_messages.append(self.data)
                    self.dial_out_logger()

                    self.dial_out_message_send.setIcon(QIcon(send_yellow))
                    time.sleep(1)
                    self.dial_out_message_send.setIcon(QIcon(send_white))

        except Exception as e:
            print(str(datetime.datetime.now()) + ' -- DialOutClass.message_send failed:', e)
            self.dial_out_message_send.setIcon(QIcon(send_red))
            time.sleep(1)
            self.dial_out_message_send.setIcon(QIcon(send_white))
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
            self.server_incoming.setIcon(QIcon(server_public_green))
            if mute_server_notify_cipher_bool is False:
                self.play_notification_sound()

        elif self.notification_key == 'amber':
            self.server_incoming.setIcon(QIcon(server_public_amber))
            if mute_server_notify_alien_bool is False:
                self.play_notification_sound()

        time.sleep(1)

        self.server_incoming.setIcon(QIcon(server_public_white))

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
                                if _[3] != bytes('x', 'utf-8'):
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
                                        if decrypted.startswith(str(_[4])):
                                            print(str(datetime.datetime.now()) + ' -- ServerDataHandlerClass.run fingerprint: validated as', str(_[0]))
                                            decrypted_message = decrypted.replace(str(_[4]), '')
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
    def __init__(self, server_incoming, server_status_label, soft_block_ip_notification, server_status_label_ip_in_use, server_start):
        QThread.__init__(self)
        self.server_incoming = server_incoming
        self.server_status_label = server_status_label
        self.soft_block_ip_notification = soft_block_ip_notification
        self.server_status_label_ip_in_use = server_status_label_ip_in_use
        self.server_start = server_start
        self.data = ''
        self.SERVER_HOST = ''
        self.SERVER_PORT = ''
        self.time_con = 0
        self.server_status_current = False
        self.server_status_prev = None

    def run(self):
        print(str(datetime.datetime.now()) + ' -- ServerClass.run: plugged in:')
        global server_address
        global server_address_index

        self.server_status_label_ip_in_use.setText(str(server_address[server_address_index][0] + ' ' + str(server_address[server_address_index][1])))

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
                self.server_status_label.setText('SERVER STATUS: TRYING TO START')
                self.server_incoming.setIcon(QIcon(server_public_yellow))
                self.server_start.setIcon(QIcon(play_yellow))
                time.sleep(1)

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

        print('-' * 200)
        print(str(datetime.datetime.now()) + ' -- ServerClass.listen SERVER_HOST:', self.SERVER_HOST)
        print(str(datetime.datetime.now()) + ' -- ServerClass.listen SERVER_PORT:', self.SERVER_PORT)
        print(str(datetime.datetime.now()) + ' -- ServerClass.listen SERVER: attempting to listen')

        x_time = round(time.time() * 1000)

        self.server_status_current = False
        self.server_status_prev = None

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
                    if self.server_status_current != self.server_status_prev:
                        self.server_status_prev = self.server_status_current
                        self.server_status_label.setText('SERVER STATUS: ONLINE')
                        self.server_incoming.setIcon(QIcon(server_public_white))
                        self.server_start.setIcon(QIcon(play_green))

                    SOCKET_SERVER.listen()

                    self.server_status_current = True
                    # ToDo --> set another object for incoming connection to keep server incoming object free to set on the wire every time
                    conn, addr = SOCKET_SERVER.accept()
                    print(str(datetime.datetime.now()) + ' -- ServerClass.listen conn, addr: ' + str(conn) + str(addr))

                    addr_exists_already = False
                    if len(soft_block_ip) > 0:
                        i = 0
                        for _ in soft_block_ip:
                            print('comparing:', soft_block_ip[i][0], ' ---> ', addr[0])
                            if soft_block_ip[i][0] == addr[0]:
                                print(str(datetime.datetime.now()) + ' -- ServerClass.listen SOCKET_SERVER ATTEMPTING BLOCK: ' + str(SOCKET_SERVER))
                                try:
                                    SOCKET_SERVER.close()
                                except Exception as e:
                                    print(str(datetime.datetime.now()) + ' -- ServerClass.stop failed:', e)
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
                                    self.server_status_current = False
                                    print(str(datetime.datetime.now()) + ' ' + str(e))
                                    textbox_0_messages.append('[' + str(datetime.datetime.now()) + '] ' + str(e))
                                    print(str(datetime.datetime.now()) + ' -- ServerClass.listen failed:', e)
                                    textbox_0_messages.append('[' + str(datetime.datetime.now()) + '] ' + str(e))
                                    self.server_status_label.setText('SERVER STATUS: TRYING TO START')
                                    self.server_incoming.setIcon(QIcon(server_public_yellow))
                                    self.server_start.setIcon(QIcon(play_yellow))
                                    time.sleep(1)
                                    break

            except Exception as e:
                self.server_status_current = False
                print(str(datetime.datetime.now()) + ' -- ServerClass.listen failed:', e)
                textbox_0_messages.append('[' + str(datetime.datetime.now()) + '] ' + str(e))
                self.server_status_label.setText('SERVER STATUS: TRYING TO START')
                self.server_incoming.setIcon(QIcon(server_public_yellow))
                self.server_start.setIcon(QIcon(play_yellow))
                time.sleep(1)
                break

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
        self.server_incoming.setIcon(QIcon(server_public_off))
        self.server_start.setIcon(QIcon(play_green))
        global_self.setFocus()
        self.terminate()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
