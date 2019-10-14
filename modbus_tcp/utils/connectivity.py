import socket
import threading
import time

from PySide2.QtCore import QObject
from PySide2.QtCore import Signal

class Communication(QObject):
    updateUI = Signal(dict)

class Modbus(QObject):
    def __init__(self, coupler_ip, port):
        self.coupler_ip = coupler_ip
        self.port = int(port)
        self.data_to_send = None
        self.running = True

        self.communication = Communication()

    def start(self):
        thread = threading.Thread(target=self.run)
        thread.setDaemon(None)
        thread.start()

    def run(self):
        socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # connecting
            self.communication.updateUI.emit({'output' : "connecting to " + self.coupler_ip + ":" + str(self.port)})
            socket_tcp.connect((self.coupler_ip, self.port), )
        except socket.error as e:
            self.communication.updateUI.emit({'output', 'could not connect'})
            return

        # update UI
        self.communication.updateUI.emit({'relay_1' : True, 'relay_2' : True, 'relay_3' : True, 'relay_4' : True})
        self.communication.updateUI.emit({'output' : "connected to "  + self.coupler_ip + ":" + str(self.port)})

        while self.running:
            time.sleep(1)

            if self.data_to_send is not None:
                try:
                    socket_tcp.send(self.data_to_send)
                except socket.error as e:
                    self.communication.updateUI.emit({'output' : 'Error'})
                    self.data_to_send = None

                    if (e.errno == socket.errno.ECONNABORTED):
                        return
                    # update UI

    def sendData(self, data):
        self.data_to_send = data

    def finish(self):
        self.running = False
