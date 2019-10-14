from modbus_tcp.compiled_ui.modbus_window import Ui_MainWindow
from modbus_tcp.utils import network_status
from modbus_tcp.utils import connectivity
from modbus_tcp.utils import data_format
from PySide2.QtWidgets import QMainWindow
from PySide2.QtWidgets import QPlainTextEdit
from PySide2.QtCore import Slot


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)
        self.showMasterDeviceIp()

        self.gui.connect_button.clicked.connect(self.connectButtonClicked)

        self.ui_elements_refnames = {'connect_button' : self.gui.connect_button,
                                     'relay_1' : self.gui.relay_1_checkBox,
                                     'relay_2' : self.gui.relay_2_checkBox,
                                     'relay_3' : self.gui.relay_3_checkBox,
                                     'relay_4' : self.gui.relay_4_checkBox,
                                     'output' : self.gui.communication_inspector_textEdit}

    def showMasterDeviceIp(self):
        self.gui.master_ip_lineEdit.setText(network_status.getIpAdress())

    def connectButtonClicked(self):
        if(self.inputDataFieldsValid()):
            coupler_ip = self.gui.coupler_ip_lineEdit.text()
            port = self.gui.port_lineEdit.text()
            
            self.modbus_connection = connectivity.Modbus(coupler_ip, port)
            self.modbus_connection.communication.updateUI.connect(self.updateUI)
            self.modbus_connection.start()

    def closeEvent(self, event):
        self.modbus_connection.stop()

    def inputDataFieldsValid(self):
        coupler_ip = self.gui.coupler_ip_lineEdit.text()
        port = self.gui.port_lineEdit.text()

        coupler_ip_valid = data_format.isIpAdress(coupler_ip)
        port_valid = data_format.isPort(port)

        # output to user which field is not valid
        if not coupler_ip_valid : self.gui.coupler_ip_lineEdit.setText("non valid ip adress")
        if not port_valid : self.gui.port_lineEdit.setText("non valid port value")

        return coupler_ip_valid and port_valid

    @Slot(dict)
    def updateUI(self, ui_states):
        '''Changes ui elements depending on ui_states'''
        print("signal update ui recived")

        for ui_state in ui_states:
            if(ui_state in self.ui_elements_refnames):
                state = ui_states.get(ui_state)
                widget = self.ui_elements_refnames.get(ui_state)

                if(isinstance(state, bool)):
                    widget.setEnabled(state)

                if(isinstance(widget, QPlainTextEdit)):
                    widget.appendPlainText(state)

            else:
                print("error : ui element referenced by non existing name")
