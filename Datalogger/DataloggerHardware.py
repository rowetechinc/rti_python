import rti_python.Comm.adcp_serial_port as adcp_serial
from typing import List


def get_serial_ports() -> List[str]:
    return adcp_serial.get_serial_ports()

def get_baud_rates() -> List[str]:
    return adcp_serial.get_baud_rates()

def get_serial_ports_tuple() -> List[tuple]:
    result = []

    for port in adcp_serial.get_serial_ports():
        result.append((port, port))

    return result

def get_baud_rates_tuple() -> List[tuple]:
    result = []

    for baud in adcp_serial.get_baud_rates():
        result.append((baud, baud))

    return result

class DataLoggerHardware:

    def __init__(self):
        self.serial = None

    def connect_serial(self,
                       port: str,
                       baud: int):
        self.serial = adcp_serial.AdcpSerialPort(port, baud)