import pynmea2
from Ensemble.Ensemble import Ensemble
from log import logger

class NmeaData:
    """
    NMEA DataSet.
    String data to decode.
    """

    def __init__(self, num_elements, element_multiplier):
        self.ds_type = 10
        self.num_elements = num_elements
        self.element_multiplier = element_multiplier
        self.image = 0
        self.name_len = 8
        self.Name = "E000011"
        self.nmea_sentences = []

        # Initialize with bad values
        self.GPGGA = None
        self.GPVTG = None
        self.GPRMC = None
        self.GPRMF = None
        self.GPGLL = None
        self.GPGSV = None
        self.GPGSA = None
        self.GPHDT = None
        self.GPHDG = None
        self.latitude = 0.0
        self.longitude = 0.0
        self.speed_knots = 0.0
        self.heading = 0.0
        self.datetime = None                              # Date and Time from GGA

    def decode(self, data):
        """
        Take the data bytearray.  Decode the data to populate
        the NMEA data.
        :param data: Bytearray for the dataset.
        """
        packet_pointer = Ensemble.GetBaseDataSize(self.name_len)

        nmea_str = str(data[packet_pointer:], "UTF-8")

        self.nmea_sentences = nmea_str.split()

        for msg in self.nmea_sentences:
            try:
                # Parse the NMEA data
                nmea_msg = pynmea2.parse(msg)

                if isinstance(nmea_msg, pynmea2.types.talker.GGA):
                    self.GPGGA = nmea_msg
                    self.latitude = nmea_msg.latitude
                    self.longitude = nmea_msg.longitude
                    self.datetime = nmea_msg.timestamp
                if isinstance(nmea_msg, pynmea2.types.talker.VTG):
                    self.GPVTG = nmea_msg
                    self.speed_knots = nmea_msg.spd_over_grnd_kts
                if isinstance(nmea_msg, pynmea2.types.talker.RMC):
                    self.GPRMC = nmea_msg
                if isinstance(nmea_msg, pynmea2.types.talker.RMF):
                    self.GPRMF = nmea_msg
                if isinstance(nmea_msg, pynmea2.types.talker.GLL):
                    self.GPGLL = nmea_msg
                if isinstance(nmea_msg, pynmea2.types.talker.GSV):
                    self.GPGSV = nmea_msg
                if isinstance(nmea_msg, pynmea2.types.talker.GSA):
                    self.GPGSA = nmea_msg
                if isinstance(nmea_msg, pynmea2.types.talker.HDT):
                    self.GPHDT = nmea_msg
                    self.heading = nmea_msg.heading
                if isinstance(nmea_msg, pynmea2.types.talker.HDG):
                    self.GPHDG = nmea_msg

            except Exception:
                logger.debug("Error decoding NMEA msg")

        logger.debug(nmea_str)
        logger.debug(self.nmea_sentences)

