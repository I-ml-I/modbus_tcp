from modbus_tcp.compiled_ui.modbus_window import Ui_MainWindow
from modbus_tcp.utils import network_status
from modbus_tcp.utils import connectivity
from modbus_tcp.utils import data_format
from modbus_tcp.utils import modbus_packet
from modbus_tcp.utils import relay_state
from PySide2.QtWidgets import QMainWindow
from PySide2.QtWidgets import QPlainTextEdit
from PySide2.QtWidgets import QPushButton
from PySide2.QtWidgets import QCheckBox
from PySide2.QtCore import Slot

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)
        self.show_master_device_ip()

        self.gui.connect_button.clicked.connect(self.connect_button_clicked)
        self.gui.disconnect_button.clicked.connect(self.disconnect_button_clicked)
        self.gui.relay_1_check_box.clicked.connect(self.check_box_clicked)
        self.gui.relay_2_check_box.clicked.connect(self.check_box_clicked)
        self.gui.relay_3_check_box.clicked.connect(self.check_box_clicked)
        self.gui.relay_4_check_box.clicked.connect(self.check_box_clicked)

        self.modbus_connection = None
        self.ui_elements_refnames = {'connect_button' : self.gui.connect_button,
                                     'disconnect_button' : self.gui.disconnect_button,
                                     'relay_1' : self.gui.relay_1_check_box,
                                     'relay_2' : self.gui.relay_2_check_box,
                                     'relay_3' : self.gui.relay_3_check_box,
                                     'relay_4' : self.gui.relay_4_check_box,
                                     'coupler_ip' : self.gui.coupler_ip_line_edit,
                                     'port' : self.gui.port_line_edit,
                                     'output' : self.gui.communication_inspector_text_edit}

    def show_master_device_ip(self):
        self.gui.master_ip_line_edit.setText(network_status.get_ip_adress())

    def check_box_clicked(self):
        '''Function sends Modbus packet containing check box states'''

        relay_1_state = self.gui.relay_1_check_box.isChecked()
        relay_2_state = self.gui.relay_2_check_box.isChecked()
        relay_3_state = self.gui.relay_3_check_box.isChecked()
        relay_4_state = self.gui.relay_4_check_box.isChecked()

        output_registar_value = relay_state.relay_states_registar_value([relay_1_state, relay_2_state,
                                                                       relay_3_state, relay_4_state])

        packet = modbus_packet.ModbusPacket(6, 0x0400, output_registar_value)

        self.modbus_connection.send_data(packet.pack())

    def connect_button_clicked(self):
        if(self.input_data_fields_valid()):
            coupler_ip = self.gui.coupler_ip_line_edit.text()
            port = self.gui.port_line_edit.text()
            
            self.modbus_connection = connectivity.Modbus(coupler_ip, port)
            self.modbus_connection.updateUI.connect(self.updateUI)
            self.modbus_connection.start()

    def disconnect_button_clicked(self):
        if  self.modbus_connection is not None:
            self.modbus_connection.stop()

    def input_data_fields_valid(self):
        coupler_ip = self.gui.coupler_ip_line_edit.text()
        port = self.gui.port_line_edit.text()

        coupler_ip_valid = data_format.is_ip_adress(coupler_ip)
        port_valid = data_format.is_port(port)

        # output to user which field is not valid
        if not coupler_ip_valid : self.gui.coupler_ip_line_edit.setText("non valid ip adress")
        if not port_valid : self.gui.port_line_edit.setText("non valid port value")

        return coupler_ip_valid and port_valid

    @Slot(dict)
    def updateUI(self, ui_states):
        '''Changes ui elements depending on ui_states'''
        print("signal update ui recived")

        for ui_state in ui_states:
            if ui_state in self.ui_elements_refnames:
                state = ui_states.get(ui_state)
                widget = self.ui_elements_refnames.get(ui_state)

                if isinstance(state, bool):
                    widget.setEnabled(state)

                elif isinstance(widget, QPlainTextEdit):
                    widget.appendPlainText(state)

                elif isinstance(widget, QCheckBox):
                    if isinstance(state, int):
                        if state == 0 : widget.setChecked(False)
                        if state == 1 : widget.setChecked(True)
            else:
                print("error : ui element referenced by non existing name")

    def closeEvent(self, event):
        self.modbus_connection.stop()
