from PyQt5.QtCore import *
from scapy.all import *
from pywifi import PyWiFi


class ScanThread(QThread):

    notify_Progress = pyqtSignal(int)
    notify_Label = pyqtSignal(str)
    listSignal = pyqtSignal(list)

    def __init__(self, iface_name, parent=None):

        super(ScanThread, self).__init__(parent)
        QThread.__init__(self)
        self.iface_name = iface_name

    def scan_ap(self, scan_iface):

        self.notify_Label.emit('Currently selected the wireless network card:' + self.iface_name + ',Scanning...')
        scan_iface.scan()
        time.sleep(3)
        bsses = scan_iface.scan_results()
        return sorted(bsses, key=lambda x: x.ssid)

    @staticmethod
    def iface_choose(face_name):

        iface_list = PyWiFi().interfaces()
        for interface in iface_list:
            if interface.name() == face_name:
                return interface

    def run(self):

        interface = self.iface_choose(self.iface_name)
        ap_list = self.scan_ap(interface)
        self.notify_Label.emit('Scanning Complete ，Updating the list...')
        for value in range(0, 101):
            time.sleep(0.003)
            self.notify_Progress.emit(value)
        self.listSignal.emit(ap_list)
