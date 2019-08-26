from PyQt5.QtCore import *
from scapy.all import *
from pywifi import PyWiFi, const, Profile
from threading import Thread
import time
from random import choice, randint
import subprocess


server_ip_list = ['39.156.66.14','39.156.66.18','14.215.177.39','14.215.177.38','103.235.46.39','202.108.22.5','119.75.217.26', '119.75.217.109', '119.75.217.63', '119.75.217.56','61.135.169.105']


class DetectThread(QThread):

    TextBrowser_text_signal = pyqtSignal(str)
    TextBrowser_div_signal = pyqtSignal()

    def __init__(self, sniff_card, send_card, key, ap_number_list, scan_list, parent=None):

        super(DetectThread, self).__init__(parent)
        QThread.__init__(self)

        self.listen_card = sniff_card
        self.send_card = send_card
        self.key = key
        self.scan_list = scan_list
        self.ap_number_list = ap_number_list
        self.time_start = 0
        self.time_end = 0
        self.ap_record = list()
        self.ap_results = list()

    @staticmethod
    def get_ap_list(scan_list, ap_number_list):

        ap_list = list()
        for ap_number in ap_number_list:
            bss = scan_list[ap_number]
            ap_list.append(bss)
        return ap_list

    @staticmethod
    def get_gateway_ip(ip_address):

        seq = ip_address.split(".")
        seq[-1] = "1"
        gateway_ip = ".".join(seq)
        return gateway_ip

    @staticmethod
    def get_wifi_card(face_name):

        iface_list = PyWiFi().interfaces()
        for interface in iface_list:
            if interface.name() == face_name:
                return interface

    def ap_link(self, interface, ap):

        if ap.akm:
            self.connect_encrypt(interface, ap, self.key)
        else:
            self.connect_open(interface, ap)

    def connect_open(self, interface, bss):

        iface_name = interface.name()
        interface.disconnect()
        time.sleep(2)
        profile_info = Profile()
        profile_info.ssid = bss.ssid
        profile_info.bssid = bss.bssid
        profile_info.akm.append(const.AKM_TYPE_NONE)
        interface.remove_all_network_profiles()
        tmp_profile = interface.add_network_profile(profile_info)
        interface.connect(tmp_profile)
        time.sleep(3)
        if interface.status() == const.IFACE_CONNECTED:
            self.TextBrowser_text_signal.emit('%s is connected to %s(%s)' % (iface_name, bss.ssid, bss.bssid))
        else:
            self.TextBrowser_text_signal.emit("AP:%s(%s) connect failed！" % (bss.ssid, bss.bssid))
            self.TextBrowser_text_signal.emit("%s disconnected..." % iface_name)

    def connect_encrypt(self, interface, bss, wifi_password):

        iface_name = interface.name()
        interface.disconnect()
        time.sleep(2)
        profile_info = Profile()
        profile_info.ssid = bss.ssid
        profile_info.bssid = bss.bssid
        profile_info.akm.append(bss.akm[-1])
        profile_info.key = wifi_password
        interface.remove_all_network_profiles()
        tmp_profile = interface.add_network_profile(profile_info)
        interface.connect(tmp_profile)
        time.sleep(3)
        if interface.status() == const.IFACE_CONNECTED:
            self.TextBrowser_text_signal.emit('%s is connected to %s(%s)' % (iface_name, bss.ssid, bss.bssid))
        else:
            self.TextBrowser_text_signal.emit("AP:%s(%s) connect failed！" % (bss.ssid, bss.bssid))
            self.TextBrowser_text_signal.emit("%s disconnected..." % iface_name)

    def send_process(self, src_mac, interface, src_ip, server_ip, src_port, dst_mac):

        pkt = Ether(src=src_mac, dst=dst_mac)/IP(src=src_ip, dst=server_ip) / TCP(sport=src_port, dport=80, flags="S")
        pkt_info = pkt.summary()
        self.TextBrowser_text_signal.emit("The send_packet is :%s" % pkt_info)
        sendp(pkt, iface=interface)
        self.time_start = time.time()

    def sniff_process(self, interface, server_ip, dst_port, ap_mac):

        packets = sniff(iface=interface, filter="dst port "+str(dst_port)+" and src host "+server_ip, count=1,
                        timeout=7)
        self.time_end = time.time()
        if packets:
            if packets[0]["TCP"].flags.value == 18:
                self.ap_record.append(ap_mac)
                pkt_info = packets[0].summary()
                self.TextBrowser_text_signal.emit("Response packet received:%s" % pkt_info)
            else:
                self.TextBrowser_text_signal.emit("No SA packet received!")
        else:
            self.TextBrowser_text_signal.emit("No packet received!")

    def detect_thread(self, sniff_interface, send_interface, bssid_send):

        ip_sniff = get_if_addr(sniff_interface)
        ip_send = get_if_addr(send_interface)
        gateway_ip = self.get_gateway_ip(ip_send)
        conf.route.resync()
        mac_recv = getmacbyip(gateway_ip)
        mac_send = get_if_hwaddr(send_interface)
        self.TextBrowser_text_signal.emit("The sniff NIC is %s(%s)" % (sniff_interface, ip_sniff))
        self.TextBrowser_text_signal.emit("The send NIC is %s(%s)" % (send_interface, ip_send))
        server_ip = choice(server_ip_list)
        src_port = randint(10000, 65535)
        p_sniff = Thread(target=self.sniff_process, args=(sniff_interface, server_ip, src_port, bssid_send))
        p_send = Thread(target=self.send_process, args=(mac_send, send_interface, ip_sniff, server_ip, src_port,
                                                        mac_recv))
        p_sniff.start()
        time.sleep(2)
        p_send.start()
        p_send.join()
        p_sniff.join()

    def detect_main(self, ap_list, iface_send, iface_listen):

        sniff_name = iface_listen.name()
        send_name = iface_send.name()
        ap_listen = ap_list[0]
        ap_numbers = len(ap_list)

        self.TextBrowser_text_signal.emit("Detection Start...")
        self.TextBrowser_text_signal.emit("AP Name:%s" % ap_listen.ssid)

        self.TextBrowser_div_signal.emit()
        self.ap_link(iface_listen, ap_listen)
        ap_listen_bssid = ap_listen.bssid

        for index, ap_send in enumerate(ap_list[1:], start=1):
            ap_send_bssid = ap_send.bssid
            self.ap_link(iface_send, ap_send)
            try:
                subprocess.call(["dhclient", "-r"], shell=False)
                subprocess.call(["dhclient"], shell=False)
            except Exception as Error:
                print(Error)
                sys.exit(1)
            else:
                self.TextBrowser_text_signal.emit("IP is assigning,please wait...")
                time.sleep(4)
            self.detect_thread(sniff_name, send_name, ap_send_bssid)
            self.TextBrowser_text_signal.emit("Time_difference:" + str(abs(self.time_end - self.time_start)) + "(s)")
            self.time_start = self.time_end = 0
            self.detect_thread(send_name, sniff_name, ap_listen_bssid)
            self.TextBrowser_text_signal.emit("Time_difference:" + str(abs(self.time_end - self.time_start)) + "(s)")
            self.time_start = self.time_end = 0
            if len(self.ap_record) == 0:
                self.TextBrowser_div_signal.emit()
                self.TextBrowser_text_signal.emit("An ETA-DiffGty exists in target APs")
                break
            elif len(self.ap_record) == 2:
                self.ap_record.clear()
                if index == ap_numbers - 1:
                    self.TextBrowser_div_signal.emit()
                    self.TextBrowser_text_signal.emit("Target APs are legal")
            else:
                self.ap_results.append(self.ap_record[0])

        if self.ap_results:
            self.TextBrowser_div_signal.emit()
            for ap in self.ap_results:
                self.TextBrowser_text_signal.emit("An ETA-SameGty exists in target APs:%s" % ap)

        self.TextBrowser_div_signal.emit()

    def run(self):

        ap_list = self.get_ap_list(self.scan_list, self.ap_number_list)
        iface_send = self.get_wifi_card(self.send_card)
        iface_listen = self.get_wifi_card(self.listen_card)
        self.detect_main(ap_list, iface_send, iface_listen)
