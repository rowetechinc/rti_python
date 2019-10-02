import struct
import json
import datetime
from PyCRC.CRCCCITT import CRCCCITT
import math
import logging


class Ensemble:
    """
    RoweTech Binary Ensemble.
    RTB format.

    """

    # Ensemble header size in bytes
    HeaderSize = 32

    # Checksum size
    ChecksumSize = 4

    # Maximum number of datasets.
    MaxNumDataSets = 20

    # Number of bytes in Int32
    BytesInInt32 = 4

    # Number of bytes in Float
    BytesInFloat = 4

    # Number of elements in dataset header
    NUM_DATASET_HEADER_ELEMENTS = 6

    # Bad Velocity
    BadVelocity = float(88.888000)

    # CSV Data Types
    CSV_AMP = "Amp"
    CSV_CORR = "Corr"
    CSV_BEAM_VEL = "BeamVel"
    CSV_INSTR_VEL = "InstrVel"
    CSV_EARTH_VEL = "EarthVel"
    CSV_GOOD_BEAM = "GoodBeam"
    CSV_GOOD_EARTH = "GoodEarth"
    CSV_PRESSURE = "Pressure"
    CSV_XDCR_DEPTH = "XdcrDepth"
    CSV_HEADING = "Heading"
    CSV_PITCH = "Pitch"
    CSV_ROLL = "Roll"
    CSV_WATER_TEMP = "WaterTemp"
    CSV_SYS_TEMP = "SysTemp"
    CSV_SOS = "SpeedOfSound"
    CSV_FIRST_PING_TIME = "FirstPingTime"
    CSV_LAST_PING_TIME = "LastPingTime"
    CSV_STATUS = "Status"
    CSV_RT = "RT"
    CSV_BT_HEADING = "BT_Heading"
    CSV_BT_PITCH = "BT_PITCH"
    CSV_BT_ROLL = "BT_ROLL"
    CSV_BT_PRESSURE = "BT_PRESSURE"
    CSV_BT_XDCR_DEPTH = "BT_XdcrDepth"
    CSV_BT_STATUS = "BT_Status"
    CSV_BT_RANGE = "BT_Range"
    CSV_BT_BEAM_VEL = "BT_BeamVel"
    CSV_BT_BEAM_GOOD = "BT_BeamGood"
    CSV_BT_INSTR_VEL = "BT_InstrVel"
    CSV_BT_INSTR_GOOD = "BT_InstrGood"
    CSV_BT_EARTH_VEL = "BT_EarthVel"
    CSV_BT_EARTH_GOOD = "BT_EarthGood"
    CSV_RT_RANGE = "RT_Range"
    CSV_RT_PINGS = "RT_Pings"
    CSV_RT_BEAM_VEL = "RT_BeamVel"
    CSV_RT_INSTR_VEL = "RT_InstrVel"
    CSV_RT_EARTH_VEL = "RT_EarthVel"
    CSV_GPS_HEADING = "GPS_Heading"
    CSV_GPS_VTG = "GPS_VTG"
    CSV_NMEA = "NMEA"
    CSV_VOLTAGE = "Voltage"
    CSV_MAG = "Magnitude"
    CSV_DIR = "Direction"

    CSV_DATETIME_FORMAT = "%m/%d/%Y %H:%M:%S.%f"

    def __init__(self):
        self.RawData = None
        self.IsBeamVelocity = False
        self.BeamVelocity = None
        self.IsInstrumentVelocity = False
        self.InstrumentVelocity = None
        self.IsEarthVelocity = False
        self.EarthVelocity = None
        self.IsAmplitude = False
        self.Amplitude = None
        self.IsCorrelation = False
        self.Correlation = None
        self.IsGoodBeam = False
        self.GoodBeam = None
        self.IsGoodEarth = False
        self.GoodEarth = None
        self.IsEnsembleData = False
        self.EnsembleData = None
        self.IsAncillaryData = False
        self.AncillaryData = None
        self.IsBottomTrack = False
        self.BottomTrack = None
        self.IsWavesInfo = False
        self.WavesInfo = None
        self.IsRangeTracking = False
        self.RangeTracking = None
        self.IsSystemSetup = False
        self.SystemSetup = None
        self.IsNmeaData = False
        self.NmeaData = None

    def AddRawData(self, data):
        """
        Add Raw bytearray data to the ensemble.
        :param data: Raw data.
        """
        self.RawData = data

    def AddBeamVelocity(self, ds):
        """
        Add a Beam Velocity object to the ensemble.
        Set the flag that the dataset is added.
        :param ds: Beam Velocity object.
        """
        self.IsBeamVelocity = True
        self.BeamVelocity = ds

    def AddInstrumentVelocity(self, ds):
        """
        Add a Instrument Velocity object to the ensemble.
        Set the flag that the dataset is added.
        :param ds: Instrument Velocity object.
        """
        self.IsInstrumentVelocity = True
        self.InstrumentVelocity = ds

    def AddEarthVelocity(self, ds):
        """
        Add a Earth Velocity object to the ensemble.
        Set the flag that the dataset is added.
        :param ds: Earth Velocity object.
        """
        self.IsEarthVelocity = True
        self.EarthVelocity = ds

    def AddAmplitude(self, ds):
        """
        Add a Amplitude object to the ensemble.
        Set the flag that the dataset is added.
        :param ds: Amplitude object.
        """
        self.IsAmplitude = True
        self.Amplitude = ds

    def AddCorrelation(self, ds):
        """
        Add a Correlation object to the ensemble.
        Set the flag that the dataset is added.
        :param ds: Correlation object.
        """
        self.IsCorrelation = True
        self.Correlation = ds

    def AddGoodBeam(self, ds):
        """
        Add a Good Beam object to the ensemble.
        Set the flag that the dataset is added.
        :param ds: GoodBeam object.
        """
        self.IsGoodBeam = True
        self.GoodBeam = ds

    def AddGoodEarth(self, ds):
        """
        Add a Good Earth object to the ensemble.
        Set the flag that the dataset is added.
        :param ds: Good Earth object.
        """
        self.IsGoodEarth = True
        self.GoodEarth = ds

    def AddEnsembleData(self, ds):
        """
        Add a EnsembleData object to the ensemble.
        Set the flag that the dataset is added.
        :param ds: Ensemble Data object.
        """
        self.IsEnsembleData = True
        self.EnsembleData = ds

    def AddAncillaryData(self, ds):
        """
        Add a AncillaryData object to the ensemble.
        Set the flag that the dataset is added.
        :param ds: Ancillary Data object.
        """
        self.IsAncillaryData = True
        self.AncillaryData = ds

    def AddBottomTrack(self, ds):
        """
        Add a Bottom Track Data object to the ensemble.
        Set the flag that the dataset is added.
        :param ds: Bottom Track Data object.
        """
        self.IsBottomTrack = True
        self.BottomTrack = ds

    def AddRangeTracking(self, ds):
        """
        Add a Range Tracking object to the ensemble.
        Set the flag that the dataset is added.
        :param ds: Range Tracking Data object.
        """
        self.IsRangeTracking = True
        self.RangeTracking = ds

    def AddSystemSetup(self, ds):
        """
        Add a System Setup object to the ensemble.
        Set the flag that the dataset is added.
        :param ds: System Setup Data object.
        """
        self.IsSystemSetup = True
        self.SystemSetup = ds

    def AddNmeaData(self, ds):
        """
        Add a NMEA data object to the ensemble.
        Set the flag that the dataset is added.
        :param ds: NMEA data Data object.
        """
        self.IsNmeaData = True
        self.NmeaData = ds

    def encode(self):
        """
        Encode the ensemble to RTB format.
        :return:
        """
        payload = []

        # Generate Payload
        if self.IsEnsembleData:
            payload += self.EnsembleData.encode()
        if self.IsAncillaryData:
            payload += self.AncillaryData.encode()
        if self.IsAmplitude:
            payload += self.Amplitude.encode()
        if self.IsCorrelation:
            payload += self.Correlation.encode()
        if self.IsBeamVelocity:
            payload += self.BeamVelocity.encode()
        if self.IsInstrumentVelocity:
            payload += self.InstrumentVelocity.encode()
        if self.IsEarthVelocity:
            payload += self.EarthVelocity.encode()
        if self.IsGoodBeam:
            payload += self.GoodBeam.encode()
        if self.IsGoodEarth:
            payload += self.GoodEarth.encode()
        if self.IsBottomTrack:
            payload += self.BottomTrack.encode()
        if self.IsRangeTracking:
            payload += self.RangeTracking.encode()
        if self.IsSystemSetup:
            payload += self.SystemSetup.encode()
        if self.IsNmeaData:
            payload += self.NmeaData.encode()

        # Generate the header
        # Get the ensemble number
        ens_num = 0
        if self.IsEnsembleData:
            ens_num = self.EnsembleData.EnsembleNumber

        # Get the payload size
        payload_size = len(payload)

        header = Ensemble.generate_ens_header(ens_num, payload_size)

        # Generate the Checksum
        checksum = Ensemble.int32_to_bytes(CRCCCITT().calculate(input_data=bytes(payload)))

        result = []
        result += header
        result += payload
        result += checksum

        return bytearray(result)

    @staticmethod
    def generate_ens_header(ens_num, payload_size):
        """
        Generate the header for an ensemble.  This will include
        16 0x80 and then the ensemble number and payload size.
        The inverse of the ensemble number and payload size are included.
        :param ens_num: Ensemble number.
        :param payload_size: Payload size.
        :return: Header for an ensemble.
        """

        header = []

        # Get the Header ID
        for cnt in range(0, 16):
            header.append(0x80)

        # Ensemble Number and inverse
        header += Ensemble.int32_to_bytes(ens_num)
        header += struct.pack("i", ~ens_num)

        # Payload size and inverse
        header += Ensemble.int32_to_bytes(payload_size)
        header += struct.pack("i", ~payload_size)

        return header

    def encode_csv(self,
                   is_ensemble_data=True,
                   is_ancillary_data=True,
                   is_amplitude=True,
                   is_correlation=True,
                   is_beam_velocity=True,
                   is_instrument_velocity=True,
                   is_earth_velocity=True,
                   is_good_beam=True,
                   is_good_earth=True,
                   is_bottom_track=True,
                   is_range_tracking=True,
                   is_nmea_data=True,
                   is_system_setup=True):
        """
        Encode the ensemble into CSV data.
        Each line is a value with a the datetime, KEY, subsystem config, subsystem code,
        bin and beam number.
        :return:
        """
        result = []

        dt = datetime.datetime.now()
        blank = 0
        bin_size = 0
        if self.IsAncillaryData:
            blank = self.AncillaryData.FirstBinRange
            bin_size = self.AncillaryData.BinSize

        # Get the subsystem code and config
        ss_code = ""
        ss_config = ""
        if self.IsEnsembleData and is_ensemble_data:
            ss_code = self.EnsembleData.SysFirmwareSubsystemCode
            ss_config = self.EnsembleData.SubsystemConfig

            # Create a new datetime based off ensemble date and time
            dt = self.EnsembleData.datetime()

            result += self.EnsembleData.encode_csv(dt, ss_code, ss_config, blank, bin_size)

        if self.IsAncillaryData and is_ancillary_data:
            result += self.AncillaryData.encode_csv(dt, ss_code, ss_config, blank, bin_size)
        if self.IsAmplitude and is_amplitude:
            result += self.Amplitude.encode_csv(dt, ss_code, ss_config, blank, bin_size)
        if self.IsCorrelation and is_correlation:
            result += self.Correlation.encode_csv(dt, ss_code, ss_config, blank, bin_size)
        if self.IsBeamVelocity and is_beam_velocity:
            result += self.BeamVelocity.encode_csv(dt, ss_code, ss_config, blank, bin_size)
        if self.IsInstrumentVelocity and is_instrument_velocity:
            result += self.InstrumentVelocity.encode_csv(dt, ss_code, ss_config, blank, bin_size)
        if self.IsEarthVelocity and is_earth_velocity:
            result += self.EarthVelocity.encode_csv(dt, ss_code, ss_config, blank, bin_size)
        if self.IsGoodBeam and is_good_beam:
            result += self.GoodBeam.encode_csv(dt, ss_code, ss_config, blank, bin_size)
        if self.IsGoodEarth and is_good_earth:
            result += self.GoodEarth.encode_csv(dt, ss_code, ss_config, blank, bin_size)
        if self.IsBottomTrack and is_bottom_track:
            result += self.BottomTrack.encode_csv(dt, ss_code, ss_config, blank, bin_size)
        if self.IsRangeTracking and is_range_tracking:
            result += self.RangeTracking.encode_csv(dt, ss_code, ss_config, blank, bin_size)
        if self.IsNmeaData and is_nmea_data:
            result += self.NmeaData.encode_csv(dt, ss_code, ss_config, blank, bin_size)
        if self.IsSystemSetup and is_system_setup:
            result += self.SystemSetup.encode_csv(dt, ss_code, ss_config, blank, bin_size)

        return result

    @staticmethod
    def generate_header(value_type, num_elements, element_multiplier, imag, name_length, name):
        """
        Generate the header for an ensemble dataset.

        Big Endian
        :param value_type: Value type (float, int, string)
        :param num_elements: Number of elements or number of bins.
        :param element_multiplier: Element multipler or number of beams.
        :param imag: NOT USED
        :param name_length: Length of the name.
        :param name: Name of the dataset.
        :return: Header for a dataset.
        """
        result = []

        result += Ensemble.int32_to_bytes(value_type)                   # Value Type
        result += Ensemble.int32_to_bytes(num_elements)                 # Number of elements
        result += Ensemble.int32_to_bytes(element_multiplier)           # Element Multiplier
        result += Ensemble.int32_to_bytes(imag)                         # Image
        result += Ensemble.int32_to_bytes(name_length)                  # Name Length
        result += name.encode()                                         # Name

        return result

    @staticmethod
    def toJSON(self, pretty=False):
        """
        Convert to JSON.
        :return: JSON string with indents.
        """
        if pretty is True:
            return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4) + "\n"
        else:
            return json.dumps(self, default=lambda o: o.__dict__) + "\n"

    @staticmethod
    def gen_csv_line(dt, data_type, ss_code, ss_config, bin_num, beam_num, blank, bin_size, value):
        """
        Create a csv line.  Use this so all the lines have the same format.

        Ex:
        2019/03/07 00:51:35:478159, Amp, 1, 3, A, 1, 7.4, 23.03
        :param dt:
        :param data_type: Data type.  Names given above starting CSV_
        :param ss_code: Subsystem code.
        :param ss_config: Subsystem configuration number.
        :param bin_num: Bin Number
        :param beam_num: Beam Number.
        :param blank: Blank or first bin position in meters.
        :param bin_size: Bin size in meters.
        :param value: Value for this line.
        :return: CSV line with all the data.
        """
        #dt_str = dt.strftime(Ensemble.CSV_DATETIME_FORMAT)
        dt_str = dt.isoformat()

        bin_depth = Ensemble.get_bin_depth(blank, bin_size, bin_num)

        return "{},{},{},{},{},{},{},{}".format(dt_str, data_type, ss_code, ss_config, bin_num, beam_num, bin_depth, value)

    @staticmethod
    def get_bin_depth(blank, bin_size, bin_num):
        """
        Give the depth of the given bin number.
        Bin number is 0 based. So the first bin is bin_num=0

        The depth is the center of the bin.

        :param blank: Blanking distance of depth of the first bin in meters.
        :param bin_size: Bin size in meters.
        :param bin_num: Bin number. Zero starting.
        :return: The depth of the given bin in meters.
        """
        return round(float(blank) + (float(bin_size) * float(bin_num)), 2)

    @staticmethod
    def GetInt32(start, numBytes, ens):
        """
        Convert the bytes given into an Int32.
        This will look in the ens given.
        :param start: Start location.
        :param numBytes: Number of bytes in the int32.
        :param ens: Buffer containing the bytearray data.
        :return: Int32 of the data in the buffer.
        """
        try:
            return struct.unpack("i", ens[start:start + numBytes])[0]
        except Exception as e:
            logging.error("Error creating a Int32 from bytes. " + str(e))
            return 0

    @staticmethod
    def GetUInt32(start, numBytes, ens):
        """
        Convert the bytes given into an UInt32.
        This will look in the ens given.
        :param start: Start location.
        :param numBytes: Number of bytes in the int32.
        :param ens: Buffer containing the bytearray data.
        :return: Int32 of the data in the buffer.
        """
        try:
            return struct.unpack("I", ens[start:start + numBytes])[0]
        except Exception as e:
            logging.error("Error creating a UInt32 from bytes. " + str(e))
            return 0

    @staticmethod
    def int32_to_bytes(value):
        """
        Convert the given Int32 value to 4 bytes.
        :param value: Value to convert.
        :return: 4 Bytes representing the value.
        """
        return struct.pack("i", value)

    @staticmethod
    def uint32_to_bytes(value):
        """
        Convert the given UInt32 value to 4 bytes.
        :param value: Value to convert.
        :return: 4 Bytes representing the value.
        """
        return struct.pack("I", value)

    @staticmethod
    def GetUInt16(start, numBytes, ens):
        """
        Convert the bytes given into an uint16.
        This will look in the ens given.
        :param start: Start location.
        :param numBytes: Number of bytes in the uint16.
        :param ens: Buffer containing the bytearray data.
        :return: uint16 of the data in the buffer.
        """
        try:
            return struct.unpack("b", ens[start:start + numBytes])[0]
        except Exception as e:
            logging.error("Error creating a UInt16 from bytes. " + str(e))
            return 0

    @staticmethod
    def uint16_to_bytes(value):
        """
        Convert the given UInt16 value to 4 bytes.
        :param value: Value to convert.
        :return: 4 Bytes representing the value.
        """
        return struct.pack("b", value)

    @staticmethod
    def GetFloat(start, numBytes, ens):
        """
        Convert the bytes given into an int32.
        This will look in the ens given.
        :param start: Start location.
        :param numBytes: Number of bytes in the int32.
        :param ens: Buffer containing the bytearray data.
        :return: Int32 of the data in the buffer.
        """
        try:
            return struct.unpack("f", ens[start:start + numBytes])[0]
        except Exception as e:
            logging.debug("Error creating a float from bytes. " + str(e))
            return 0.0

    @staticmethod
    def float_to_bytes(value):
        """
        Convert the given float value to 4 bytes.
        :param value: Value to convert.
        :return: 4 Bytes representing the value.
        """
        return struct.pack("f", value)

    @staticmethod
    def GetDataSetSize(ds_type, name_len, num_elements, element_multipler):
        """
        Get the dataset size.
        :param ds_type: Dataset type. (Int, float, ...)
        :param name_len: Length of the name.
        :param num_elements: Number of elements.
        :param element_multipler: Element mulitpiler.
        :return: Size of the dataset in bytes.
        """

        # Number of bytes in the data type
        datatype_size = 4
        if ds_type is 50:      # Byte Datatype
            datatype_size = 1
        elif ds_type is 20:    # Int Datatype
            datatype_size = 4
        elif ds_type is 10:    # Float Datatype
            datatype_size = 4

        return ((num_elements * element_multipler) * datatype_size) + Ensemble.GetBaseDataSize(name_len)

    @staticmethod
    def GetBaseDataSize(name_len):
        """
        Get the size of the header for a dataset.
        :param name_len: Length of the name.
        :return: Dataset header size in bytes.
        """
        return name_len + (Ensemble().BytesInInt32 * (Ensemble().NUM_DATASET_HEADER_ELEMENTS-1))

    @staticmethod
    def ensembleSize(payloadSize):
        return Ensemble.HeaderSize + payloadSize + Ensemble.ChecksumSize

    @staticmethod
    def ones_complement(val):
        """
        Calclaute the 1's compliment of a number.
        :param val: Values to calculate.
        :return: 1's compliment of value.
        """
        #mask = (1 << val.bit_length()) - 1
        #return int(hex(val ^ mask), 16)
        b = bin(val)
        b = b.replace('0', 'x')
        b = b.replace('1', '0')
        b = b.replace('x', '1')
        b = b.replace('1b', '0b')
        return int(b, 2)

    @staticmethod
    def oness_complement(val):

        # Find number of bits in
        # the given integer
        number_of_bits = (int)(math.floor(math.log(val) /
                                          math.log(2))) + 1;

        # XOR the given integer with poe(2,
        # number_of_bits-1 and print the result
        return ((1 << number_of_bits) - 1) ^ val;

    @staticmethod
    def is_float_close(a, b, rel_tol=1e-09, abs_tol=0.0):
        """
        Check if the float values are the same.
        :param a: First float value
        :param b: Second float value
        :param rel_tol: Value within this
        :param abs_tol: Absolute value within this
        :return:
        """
        return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)