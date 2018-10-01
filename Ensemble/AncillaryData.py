from Ensemble.Ensemble import Ensemble
from log import logger


class AncillaryData:
    """
    Ancillary Data DataSet.
    Float values that give details about the ensemble.
    """

    def __init__(self, num_elements, element_multiplier):
        self.ds_type = 10
        self.num_elements = num_elements
        self.element_multiplier = element_multiplier
        self.image = 0
        self.name_len = 8
        self.Name = "E000009"

        self.FirstBinRange = 0.0        # Blank.  Depth to the first bin in meters.
        self.BinSize = 0.0              # Size of a bin in meters.
        self.FirstPingTime = 0.0        # First Ping Time in seconds.
        self.LastPingTime = 0.0         # Last Ping Time in seconds.  (If averaging pings, this will be the last ping)
        self.Heading = 0.0              # Heading in degrees.
        self.Pitch = 0.0                # Pitch in degrees.
        self.Roll = 0.0                 # Roll in degrees.
        self.WaterTemp = 0.0            # Water Temperature in fahrenheit
        self.SystemTemp = 0.0           # System Temperature in fahrenheit
        self.Salinity = 0.0             # Water Salinity set by the user in PPT
        self.Pressure = 0.0             # Pressure from pressure sensor in Pascals
        self.TransducerDepth = 0.0      # Transducer Depth, used by Pressure sensor in meters
        self.SpeedOfSound = 0.0         # Speed of Sound in m/s.
        self.RawMagFieldStrength = 0.0  # Raw magnetic field strength
        self.PitchGravityVector = 0.0   # Pitch Gravity Vector
        self.RollGravityVector = 0.0    # Roll Gravity Vector
        self.VerticalGravityVector = 0.0 # Vertical Gravity Vector

    def decode(self, data):
        """
        Take the data bytearray.  Decode the data to populate
        the values.
        :param data: Bytearray for the dataset.
        """
        packet_pointer = Ensemble.GetBaseDataSize(self.name_len)

        self.FirstBinRange = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 0, Ensemble().BytesInFloat, data)
        self.BinSize = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 1, Ensemble().BytesInFloat, data)
        self.FirstPingTime = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 2, Ensemble().BytesInFloat, data)
        self.LastPingTime = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 3, Ensemble().BytesInFloat, data)
        self.Heading = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 4, Ensemble().BytesInFloat, data)
        self.Pitch = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 5, Ensemble().BytesInFloat, data)
        self.Roll = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 6, Ensemble().BytesInFloat, data)
        self.WaterTemp = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 7, Ensemble().BytesInFloat, data)
        self.SystemTemp = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 8, Ensemble().BytesInFloat, data)
        self.Salinity = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 9, Ensemble().BytesInFloat, data)
        self.Pressure = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 10, Ensemble().BytesInFloat, data)
        self.TransducerDepth = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 11, Ensemble().BytesInFloat, data)
        self.SpeedOfSound = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 12, Ensemble().BytesInFloat, data)

        if self.num_elements > 13:
            self.RawMagFieldStrength = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 13, Ensemble().BytesInFloat, data)
            self.PitchGravityVector = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 14, Ensemble().BytesInFloat, data)
            self.RollGravityVector = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 15, Ensemble().BytesInFloat, data)
            self.VerticalGravityVector = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 16, Ensemble().BytesInFloat, data)

        logger.debug(self.FirstBinRange)
        logger.debug(self.BinSize)
        logger.debug(self.Heading)
        logger.debug(self.Pitch)
        logger.debug(self.Roll)
        logger.debug(self.Salinity)
        logger.debug(self.SpeedOfSound)



