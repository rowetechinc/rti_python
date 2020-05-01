import rti_python.Comm.adcp_serial_port as adcp_serial
from typing import List


class DataLoggerHardware:

    def __init__(self):
        self.serial = None

    def get_serial_ports(self) -> List[str]:
        return adcp_serial.get_serial_ports()

    def get_baud_rates(self) -> List[str]:
        return adcp_serial.get_baud_rates()

    def connect_serial(self,
                       port: str,
                       baud: int):
        self.serial = adcp_serial.AdcpSerialPort(port, baud)