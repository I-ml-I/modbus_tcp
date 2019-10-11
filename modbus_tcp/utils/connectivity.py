import socket
import threading
import time

class Modbus():
    def __init__(self, coupler_ip, port):
        self.coupler_ip = coupler_ip
        self.port = int(port)
        self.data_to_send = None
        self.running = True

    def start(self):
        thread = threading.Thread(target=self.run)
        thread.setDaemon(None)
        thread.start()

    def run(self):
        socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # connecting
            print("connecting to " + self.coupler_ip + ":" + str(self.port))
            socket_tcp.connect((self.coupler_ip, self.port), )
        except socket.error as e:
            # could not connect
            print("could not connect")
            return

        # update UI
        print("connected to "  + self.coupler_ip + ":" + str(self.port))

        while self.running:
            time.sleep(1)

            if self.data_to_send is not None:
                try:
                    socket_tcp.send(self.data_to_send)
                except socket.error as e:
                    print("Error")
                    self.data_to_send = None

                    if (e.errno == socket.errno.ECONNABORTED):
                        return
                    # update UI

    def sendData(self, data):
        self.data_to_send = data

    def finish(self):
        self.running = False
