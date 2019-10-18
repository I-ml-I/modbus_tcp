import socket
import threading
import time
from PySide2.QtCore import QObject
from PySide2.QtCore import Signal
from utils.modbus_packet import ModbusPacket
from utils import relay_state

class Modbus(QObject):
    updateUI = Signal(dict)

    def __init__(self, coupler_ip, port):
        QObject.__init__(self, parent=None)

        self.coupler_ip = coupler_ip
        self.port = int(port)
        self.data_to_send = None
        self.running = True 

    def start(self):
        '''Function start creates new thread and, sets some
        parameters and starts created thread'''

        thread = threading.Thread(target=self.run)
        thread.setDaemon(None)
        thread.start()

    def stop(self):
        '''Function stop, updates UI for disconnected status
        and stops thread'''

        self.update_ui_status(connected=False)
        self.running = False

    def run(self):
        socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_tcp.settimeout(1)

        # connecting
        try:
            self.output_to_ui("connecting to " + self.coupler_ip + ":" + str(self.port))
            socket_tcp.connect((self.coupler_ip, self.port))
        except socket.error:
            self.output_to_ui('could not connect')
            return

        # connected
        # update UI with connected relay module register
        self.update_ui_status(connected=True)
        self.read_relay_states()

        # sending data and receiving data
        while self.running:
            time.sleep(1)

            if self.data_to_send is not None:
                try:
                    # send data
                    socket_tcp.send(self.data_to_send)
                    self.output_to_ui("Tx: " + str(self.data_to_send))
                    data_received = socket_tcp.recv(1024)
                    self.output_to_ui("Rx: " + str(data_received))

                    # send data to check register value 
                    socket_tcp.send(ModbusPacket(4, 0x400, 1).pack())

                    # receive response with register value
                    data_received = socket_tcp.recv(1024)

                    # update UI with response or output error in operation
                    self.update_relays_statuses_with_response(data_received)
                        
                    self.data_to_send = None

                except socket.error:
                    self.running = False
                    self.update_ui_status(False)
                    self.output_to_ui('connection dropped')

        socket_tcp.close()

    def read_relay_states(self):
        '''Function read_relay_states sends read request
        packet needed to get response from coupler containing
        output register value'''

        packet = ModbusPacket(4, 0x400, 1).pack()
        self.send_data(packet)

    def send_data(self, data):
        '''Function send_data pends data to be sent, and 
        will be sent as soon as thread wakes up from sleep'''

        self.data_to_send = data

    def update_relays_statuses_with_response(self, response):
        '''Function updates check boxes with current state of relays'''
        
        rx_packet = ModbusPacket(packet=response)

        try:
            rx_packet.unpack()
            relay_states = relay_state.relay_states_from_register_value(rx_packet.value)

            self.update_relays_statuses(relay_states[3], relay_states[2],
                                        relay_states[1], relay_states[0])

        except Exception as e:
            self.output_to_ui("modbus response with error code"+ str(e))

    def update_ui_status(self, connected):
        if connected:
            self.updateUI.emit({'connect_button' : False,
                                'disconnect_button' : True,
                                'relay_1' : True,
                                'relay_2' : True,
                                'relay_3' : True,
                                'relay_4' : True,
                                'coupler_ip' : False,
                                'port' : False,
                                'output' : 'connected'})

        else:
            self.updateUI.emit({'connect_button' : True,
                                'disconnect_button' : False,
                                'relay_1' : False,
                                'relay_2' : False,
                                'relay_3' : False,
                                'relay_4' : False,
                                'coupler_ip' : True,
                                'port' : True,
                                'output' : 'disconnected'})

    def output_to_ui(self, output):
        '''Function output_to_ui prints data to edit text widget'''
        
        self.updateUI.emit({'output' : output})

    def update_relays_statuses(self, relay_1 : int, relay_2 : int, relay_3 : int, relay_4 : int):
        '''Function update_relays_statuses controls check boxes'''

        self.updateUI.emit({'relay_1' : relay_1,
                            'relay_2' : relay_2,
                            'relay_3' : relay_3,
                            'relay_4' : relay_4})
