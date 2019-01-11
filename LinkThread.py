from PyQt5.QtCore import *
from scapy.all import *
from pywifi import PyWiFi, const, Profile
import subprocess

ip_assign = ["dhclient"]
ip_release = ["dhclient", "-r"]


class LinkThread(QThread):

    notify_Progress = pyqtSignal(int)
    notify_Label = pyqtSignal(str)

    def __init__(self, face_name, ap_number, key, scan_list, parent=None):
        super(LinkThread, self).__init__(parent)
        QThread.__init__(self)
        self.iface_name = face_name
        self.key = key
        self.scan_list = scan_list
        self.ap_number = ap_number

    @staticmethod
    def iface_choose(face_name):
        iface_list = PyWiFi().interfaces()
        for interface in iface_list:
            if interface.name() == face_name:
                return interface

    def connect_open(self, interface, bss):

        self.notify_Label.emit('Disconnecting from the current network...')
        interface.disconnect()
        time.sleep(2)
        profile_info = Profile()
        profile_info.ssid = bss.ssid
        profile_info.bssid = bss.bssid
        profile_info.akm.append(const.AKM_TYPE_NONE)
        interface.remove_all_network_profiles()
        tmp_profile = interface.add_network_profile(profile_info)
        self.notify_Label.emit("Begin to connect the AP:%s(%s)..." % (bss.ssid, bss.bssid))
        interface.connect(tmp_profile)

    def connect_encrypt(self, interface, bss, wifi_password):

        self.notify_Label.emit('Disconnecting from the current network...')
        interface.disconnect()
        time.sleep(2)
        profile_info = Profile()
        profile_info.ssid = bss.ssid
        profile_info.bssid = bss.bssid
        profile_info.akm.append(bss.akm[-1])
        profile_info.key = wifi_password
        interface.remove_all_network_profiles()
        tmp_profile = interface.add_network_profile(profile_info)
        self.notify_Label.emit("Begin to connect the AP:%s(%s)..." % (bss.ssid, bss.bssid))
        interface.connect(tmp_profile)

    def run(self):

        bss = self.scan_list[self.ap_number]
        interface = self.iface_choose(self.iface_name)
        self.notify_Label.emit('Currently selected the WLAN card:%s,' % self.iface_name)
        if bss.akm:
            self.connect_encrypt(interface, bss, self.key)
        else:
            self.connect_open(interface, bss)
        for value in range(0, 101):
            time.sleep(0.04)
            self.notify_Progress.emit(value)
        if interface.status() == const.IFACE_CONNECTED:
            self.notify_Label.emit('Connection Complete,IP address is being assigned...')
            subprocess.call(ip_release, shell=False)
            subprocess.call(ip_assign, shell=False)
            self.notify_Label.emit('IP address assignment is done')
            self.notify_Label.emit('%s is connected to %s(%s)' % (self.iface_name, bss.ssid, bss.bssid))
            conf.route.resync()
        else:
            self.notify_Label.emit("wifi:%s(%s) connect failed！" % (bss.ssid, bss.bssid))
            self.notify_Label.emit("%s disconnected..." % self.iface_name)
