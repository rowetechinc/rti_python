from rti_python.Ensemble.Ensemble import Ensemble
import logging


class SystemSetup:
    """
    System Setup DataSet.
    Float values that give details about the system setup.
    """

    def __init__(self, num_elements, element_multiplier):
        self.ds_type = 10
        self.num_elements = num_elements
        self.element_multiplier = element_multiplier
        self.image = 0
        self.name_len = 8
        self.Name = "E000014"

        self.BtSamplesPerSecond = 0.0           # Bottom Track Samples Per Second
        self.BtSystemFreqHz = 0.0               # Bottom Track System Frequency (Hz)
        self.BtCPCE = 0.0                       # Bottom Track Cycles per Code Elements
        self.BtNCE = 0.0                        # Bottom Track Number of Code Elements
        self.BtRepeatN = 0.0                    # Bottom Track Number of Code Repeats
        self.WpSamplesPerSecond = 0.0           # Water Profile Samples per Second
        self.WpSystemFreqHz = 0.0               # Water Profile System Frequency (Hz)
        self.WpCPCE = 0.0                       # Water Profile Cycles per Code Element
        self.WpNCE = 0.0                        # Water Profile Number of Code Element
        self.WpRepeatN = 0.0                    # Water Profile Number of Code Repeats
        self.WpLagSamples = 0.0                 # Water Profile Lag Samples
        self.Voltage = 0.0                      # Voltage input to ADCP
        self.XmtVoltage = 0.0                   # Transmit Voltage
        self.BtBroadband = 0.0                  # Bottom Track Broadband
        self.BtLagLength = 0.0                  # Bottom Track Lag Length
        self.BtNarrowband = 0.0                 # Bottom Track Narrowband
        self.BtBeamMux = 0.0                    # Bottom Track Beam MUX
        self.WpBroadband = 0.0                  # Water Profile Broadband
        self.WpLagLength = 0.0                  # Water Profile Lag Length
        self.WpTransmitBandwidth = 0.0          # Water Profile Transmit Bandwidth
        self.WpReceiveBandwidth = 0.0           # Water Profile Receive Bandwidth

    def decode(self, data):
        """
        Take the data bytearray.  Decode the data to populate
        the values.
        :param data: Bytearray for the dataset.
        """
        packet_pointer = Ensemble.GetBaseDataSize(self.name_len)

        self.BtSamplesPerSecond = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 0, Ensemble().BytesInFloat, data)
        self.BtSystemFreqHz = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 1, Ensemble().BytesInFloat, data)
        self.BtCPCE = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 2, Ensemble().BytesInFloat, data)
        self.BtNCE = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 3, Ensemble().BytesInFloat, data)
        self.BtRepeatN = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 4, Ensemble().BytesInFloat, data)
        self.WpSamplesPerSecond = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 5, Ensemble().BytesInFloat, data)
        self.WpSystemFreqHz = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 6, Ensemble().BytesInFloat, data)
        self.WpCPCE = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 7, Ensemble().BytesInFloat, data)
        self.WpNCE = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 8, Ensemble().BytesInFloat, data)
        self.WpRepeatN = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 9, Ensemble().BytesInFloat, data)
        self.WpLagSamples = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 10, Ensemble().BytesInFloat, data)
        self.Voltage = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 11, Ensemble().BytesInFloat, data)

        if self.num_elements > 12:
            self.XmtVoltage = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 12, Ensemble().BytesInFloat, data)
            self.BtBroadband = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 13, Ensemble().BytesInFloat, data)
            self.BtLagLength = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 14, Ensemble().BytesInFloat, data)
            self.BtNarrowband = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 15, Ensemble().BytesInFloat, data)
            self.BtBeamMux = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 16, Ensemble().BytesInFloat, data)
            self.WpBroadband = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 17, Ensemble().BytesInFloat, data)
            self.WpLagLength = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 18, Ensemble().BytesInFloat, data)
            self.WpTransmitBandwidth = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 19, Ensemble().BytesInFloat, data)
            self.WpReceiveBandwidth = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 20, Ensemble().BytesInFloat, data)

        logging.debug(self.BtSamplesPerSecond)
        logging.debug(self.BtSystemFreqHz)
        logging.debug(self.BtCPCE)
        logging.debug(self.BtNCE)
        logging.debug(self.BtRepeatN)
        logging.debug(self.WpSamplesPerSecond)
        logging.debug(self.WpSystemFreqHz)
        logging.debug(self.WpCPCE)
        logging.debug(self.WpNCE)
        logging.debug(self.WpRepeatN)
        logging.debug(self.WpLagSamples)
        logging.debug(self.Voltage)
        logging.debug(self.XmtVoltage)
        logging.debug(self.BtBroadband)
        logging.debug(self.BtLagLength)
        logging.debug(self.BtNarrowband)
        logging.debug(self.BtBeamMux)
        logging.debug(self.WpBroadband)
        logging.debug(self.WpLagLength)
        logging.debug(self.WpTransmitBandwidth)
        logging.debug(self.WpReceiveBandwidth)



