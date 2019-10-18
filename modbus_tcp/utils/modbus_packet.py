from struct import pack
from struct import unpack
from random import randint
from sys import maxsize

class ModbusPacket():
    def __init__(self, function_code = None, address = None, value = None, packet = None):
        self.packet_num = randint(0, 1024)
        self.function_code = function_code
        self.lenght = 6
        self.unit_id = 1
        self.address = address
        self.value = value

        self.packet = packet

    def pack(self):
        if self.function_code and self.address and self.value is not None:
            self.packet = pack('>HHHBBHH', self.packet_num, 0, self.lenght, self.unit_id,
                                self.function_code, self.address, self.value)

        return self.packet

    def unpack(self):
        if self.packet is not None:
            (self.packet_num, zero, self.lenght,
            self.unit_id, self.function_code,
            self.address, self.value) = unpack('>HHHBBBH', self.packet)
            