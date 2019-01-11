import sys
from UI import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore, QtGui
from ScanThread import ScanThread
from LinkThread import LinkThread
from pywifi import PyWiFi
from Link_Dialog import Link_Dialog
from Detect_Dialog import Detect_Dialog
from DetectThread import DetectThread
from datetime import datetime

AKM = {0: 'NONE', 1: 'WPA', 2: 'WPA-PSK', 3: 'WPA2', 4: 'WPA2-PSK', 5: 'UNKNOWN'}
Channel = {2412: '1', 2417: '2', 2422: '3', 2427: '4', 2432: '5', 2437: '6', 2442: '7', 2447: '8', 2452: '9',
           2457: '10', 2462: '11', 2467: '12', 2472: '13'}

iface_list = PyWiFi().interfaces()
items = sorted([iface.name() for iface in iface_list])


class Mywindow (QtWidgets.QWidget, Ui_MainWindow):

    def __init__(self):

        super(Mywindow, self).__init__()
        self.setupUi(self)
        self.scan_list = list()
        self.ScanButton.clicked.connect(self.scan_button_click)
        self.LinkButton.clicked.connect(self.link_button_click)
        self.DetectButton.clicked.connect(self.detect_button_click)
        self.ClearButton.clicked.connect(self.clear_button_click)

        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.setStatusTip('Exit application')
        self.exit_action.triggered.connect(QtGui.QGuiApplication.quit)

        self.help_action.triggered.connect(self.__show_help)

        self.stop_action.setShortcut('Ctrl+P')
        self.stop_action.setStatusTip('Pause the application')

        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)

    def scan_button_click(self):

        set_network = QtWidgets.QInputDialog()
        iface_name, ok = set_network.getItem(self, 'Nic Selector', 'Select a wireless network interface card:', items, 0,
                                             False)
        if ok:
            self.scan_thread = ScanThread(iface_name)
            self.scan_thread.notify_Progress.connect(self.__on_Progress)
            self.scan_thread.listSignal.connect(self.scan_list_update)
            self.scan_thread.notify_Label.connect(self.__on_Label)
            self.stop_action.triggered.connect(self.__on_stop_scan)
            self.scan_thread.start()

    def scan_list_update(self, scan_list):

        self.ScantableWidget.clearContents()
        for row, bss in enumerate(scan_list):
            ssid = bss.ssid
            bssid = bss.bssid
            signal = str(bss.signal)
            if 2412 <= int(bss.freq) <= 2472:
                freq = Channel[bss.freq]
            else:
                freq = bss.freq
            if bss.akm:
                akm = AKM[bss.akm[-1]]
            else:
                akm = 'None'
            self.ScantableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(ssid))
            self.ScantableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(bssid))
            self.ScantableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(signal))
            self.ScantableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(freq))
            self.ScantableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(akm))

        self.label.setText('AP list updated!')
        self.scan_list = scan_list

    def link_button_click(self):

        link_form = Link_Dialog()
        link_form.setupUi(link_form)
        link_form.setFixedSize(link_form.width(), link_form.height())
        current_row = self.ScantableWidget.currentRow()
        target_ssid = self.ScantableWidget.item(current_row, 0)
        target_bssid = self.ScantableWidget.item(current_row, 1)
        target_akm = self.ScantableWidget.item(current_row, 4)
        link_form.interface_choose.addItems(items)
        if target_bssid and target_ssid and target_akm:
            ssid_text = target_ssid.text()
            bssid_text = target_bssid.text()
            akm_text = target_akm.text()
            link_form.AP_ssid.setText(ssid_text)
            link_form.AP_bssid.setText(bssid_text)
            link_form.AP_akm.setText(akm_text)
        if link_form.exec():
            net_card = link_form.get_interface()
            key = link_form.get_AP_Key()
            self.link_thread = LinkThread(net_card, current_row, key, self.scan_list)
            self.link_thread.notify_Label.connect(self.__on_Label)
            self.link_thread.notify_Progress.connect(self.__on_Progress)
            self.link_thread.start()

    def detect_button_click(self):

        detect_form = Detect_Dialog()
        detect_form.setupUi(detect_form)
        ap_number_list = list()
        for currentRows in self.ScantableWidget.selectionModel().selectedRows():
            row = QtCore.QPersistentModelIndex(currentRows).row()
            ap_number_list.append(row)
        if len(ap_number_list) <= 1:
            QtWidgets.QMessageBox.critical(self, "Error", "Select at least two item")
        else:
            ap_str_list = [str(i + 1) for i in ap_number_list]
            ap_str = ','.join(ap_str_list)
            detect_form.AP_list.setText(ap_str)
            detect_form.Listen_card.addItems(items)
            detect_form.Send_card.addItems(items)
            if ap_number_list[0]:
                target_akm = self.ScantableWidget.item(ap_number_list[0], 4)
                if target_akm:
                    detect_form.AP_akm.setText(target_akm.text())
            if detect_form.exec():
                listen_card = detect_form.get_listen_card()
                send_card = detect_form.get_send_card()
                key = detect_form.get_ap_key()
                self.detect_thread = DetectThread(listen_card, send_card, key, ap_number_list, self.scan_list)
                self.detect_thread.TextBrowser_text_signal.connect(self.__on_TextBroswer)
                self.detect_thread.TextBrowser_div_signal.connect(self.__on_div_Broswer)
                self.detect_thread.start()

    def clear_button_click(self):

        self.RecordTextBrowser.clear()

    def __on_stop_scan(self):

        if self.scan_thread.isRunning():
            self.scan_thread.terminate()
            self.scan_thread.wait()

    def __on_Progress(self, i):

        self.progressBar.setValue(i)

    def __on_TextBroswer(self, i):

        self.RecordTextBrowser.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S ') + i)

    def __on_div_Broswer(self):

        self.RecordTextBrowser.append("-" * 116)

    def __on_Label(self, i):

        self.label.setText(i)

    def __show_help(self):

        use_help = u"This program is used for evil twin attackes detection.\n" \
                   u"Program use:\n" \
                   u"1. Scan function: Click the Scan button to start scanning APs in surrounding wireless network.\n" \
                   u"2. Connection function: Click the Connect button to connect multiple target APs.\n" \
                   u"3.Detection function: Click Detect button to perform Bi-directional reflection ETAs detection.\n" \
                   u"Thank you for your use!\n" \
                   u"                                                     Contact:oycillessen@foxmail.com"
        QtWidgets.QMessageBox.information(self, u"About", use_help)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    my_show = Mywindow()
    my_show.setFixedSize(my_show.width(), my_show.height())
    my_show.show()
    sys.exit(app.exec_())
