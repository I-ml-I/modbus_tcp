import socket
import threading
import time
from PySide2.QtCore import QObject
from PySide2.QtCore import Signal

class Modbus(QObject):
    updateUI = Signal(dict)

    def __init__(self, coupler_ip, port):
        QObject.__init__(self, parent=None)

        self.coupler_ip = coupler_ip
        self.port = int(port)
        self.data_to_send = None
        self.running = True
        

    def start(self):
        thread = threading.Thread(target=self.run)
        thread.setDaemon(None)
        thread.start()

    def stop(self):
        self.update_ui_status(connected=False)
        self.running = False

    def run(self):
        socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_tcp.settimeout('')

        # connecting
        try:
            self.output_to_ui("connecting to " + self.coupler_ip + ":" + str(self.port))
            socket_tcp.connect((self.coupler_ip, self.port))

        except socket.error as e:
            self.output_to_ui('could not connect')
            return

        # connected
        # update UI
        self.update_ui_status(connected=True)

        # sending data
        while self.running:
            time.sleep(1)

            if self.data_to_send is not None:
                try:
                    socket_tcp.send(self.data_to_send)
                except socket.error as e:
                    self.update_ui_status('error')
                    self.data_to_send = None

                    if e.errno == socket.errno.ECONNABORTED:
                        return
                    # update UI

        socket_tcp.close()

    def send_data(self, data):
        self.data_to_send = data

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
        self.updateUI.emit({'output' : output})
