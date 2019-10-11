from modbus_tcp.compiled_ui.modbus_window import Ui_MainWindow
from modbus_tcp.utils import network_status
from modbus_tcp.utils import connectivity
from modbus_tcp.utils import data_format
from PySide2.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)

        self.gui.connect_button.clicked.connect(self.connectButtonClicked)

        self.showMasterDeviceIp()

    def showMasterDeviceIp(self):
        self.gui.master_ip_lineEdit.setText(network_status.getIpAdress())

    def connectButtonClicked(self):
        if(self.inputDataFieldsValid()):
            coupler_ip = self.gui.coupler_ip_lineEdit.text()
            port = self.gui.port_lineEdit.text()
            
            self.modbus_connection = connectivity.Modbus(coupler_ip, port)
            self.modbus_connection.start()

    def inputDataFieldsValid(self):
        coupler_ip = self.gui.coupler_ip_lineEdit.text()
        port = self.gui.port_lineEdit.text()

        coupler_ip_valid = data_format.isIpAdress(coupler_ip)
        port_valid = data_format.isPort(port)

        # output to user which field is not valid
        if not coupler_ip_valid : self.gui.coupler_ip_lineEdit.setText("non valid ip adress")
        if not port_valid : self.gui.port_lineEdit.setText("non valid port value")

        return coupler_ip_valid and port_valid
