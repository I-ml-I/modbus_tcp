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
            master_ip = self.gui.master_ip_lineEdit.text()
            coupler_ip = self.gui.coupler_ip_lineEdit.text()
            port = self.gui.port_lineEdit.text()
            
            connectivity.connectToModbus(master_ip, coupler_ip, port)


    def inputDataFieldsValid(self):
        master_ip = self.gui.master_ip_lineEdit.text()
        coupler_ip = self.gui.coupler_ip_lineEdit.text()
        port = self.gui.port_lineEdit.text()

        master_ip_valid = data_format.isIpAdress(master_ip)
        coupler_ip_valid = data_format.isIpAdress(coupler_ip)
        port_valid = data_format.isPort(port)

        # output to user which field is not valid
        if not master_ip_valid : self.gui.master_ip_lineEdit.setText("non valid ip adress") 
        if not coupler_ip_valid : self.gui.coupler_ip_lineEdit.setText("non valid ip adress")
        if not port_valid : self.gui.port_lineEdit.setText("non valid port value")

        return master_ip_valid and coupler_ip_valid and port_valid
