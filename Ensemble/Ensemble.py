import struct
import json
import datetime


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
    CSV_BT_RANGE = "BT_Range"
    CSV_BT_BEAM_VEL = "BT_BeamVel"
    CSV_BT_INSTR_VEL = "BT_InstrVel"
    CSV_BT_EARTH_VEL = "BT_EarthVel"
    CSV_BT_STATUS = "BT_Status"
    CSV_GPS_HEADING = "GPS_Heading"
    CSV_GPS_VTG = "GPS_VTG"
    CSV_NMEA = "NMEA"

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

        # Generate the header
        header = []

        # Generate the Checksum
        checksum = []

        return header + payload + checksum

    def encode_csv(self):
        result = []

        dt = datetime.datetime.now()

        # Get the subsytem code and config
        ss_code = ""
        ss_config = ""
        if self.IsEnsembleData:
            ss_code = self.EnsembleData.SysFirmwareSubsystemCode
            ss_config = self.EnsembleData.SubsystemConfig

        if self.IsAmplitude:
            result += self.Amplitude.encode_csv(dt, ss_code, ss_config)
        if self.IsCorrelation:
            result += self.Correlation.encode_csv(dt, ss_code, ss_config)
        if self.IsBeamVelocity:
            result += self.BeamVelocity.encode_csv(dt, ss_code, ss_config)
        if self.IsInstrumentVelocity:
            result += self.InstrumentVelocity.encode_csv(dt, ss_code, ss_config)
        if self.IsEarthVelocity:
            result += self.EarthVelocity.encode_csv(dt, ss_code, ss_config)
        if self.IsGoodBeam:
            result += self.GoodBeam.encode_csv(dt, ss_code, ss_config)
        if self.IsGoodEarth:
            result += self.GoodEarth.encode_csv(dt, ss_code, ss_config)
        if self.IsAncillaryData:
            result += self.AncillaryData.encode_csv(dt, ss_code, ss_config)

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
    def gen_csv_line(dt, data_type, ss_code, ss_config, bin_num, beam_num, value):
        """
        Create a csv line.  Use this so all the lines have the same format.

        The data_type options are:
        Amp = Amplitude
        Corr = Correlation
        BeamVel = Beam Velocity
        InstrVel = Instrument Velocity
        EarthVel = Earth Velocity
        Pressure = Pressure Depth
        Heading = Heading
        Pitch = Pitch
        Roll = Roll
        RT = Range Tracking
        BT_Range = Bottom Track Range
        BT_BeamVel = Bottom Track Beam Velocity
        BT_InstrVel = Bottom Track Instrument Velocity
        BT_EarthVel = Bottom Track Earth Velocity


        Ex:
        2019/03/07 00:51:35:478159, Amp, 1, 3, A, 1, 23.03
        :param dt:
        :param data_type:
        :param ss_code:
        :param ss_config:
        :param bin_num:
        :param beam_num:
        :param value:
        :return:
        """
        dt_str = dt.strftime('%Y/%m/%d %H:%M:%S:%f')

        return "{},{},{},{},{},{},{}".format(dt_str, data_type, ss_code, ss_config, bin_num, beam_num, value)

    @staticmethod
    def GetInt32(start, numBytes, ens):
        """
        Convert the bytes given into an int32.
        This will look in the ens given.
        :param start: Start location.
        :param numBytes: Number of bytes in the int32.
        :param ens: Buffer containing the bytearray data.
        :return: Int32 of the data in the buffer.
        """
        return struct.unpack("I", ens[start:start + numBytes])[0]

    @staticmethod
    def int32_to_bytes(value):
        """
        Convert the given Int32 value to 4 bytes.
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
        return struct.unpack("b", ens[start:start + numBytes])[0]

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
        return struct.unpack("f", ens[start:start + numBytes])[0]

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
        mask = (1 << val.bit_length()) - 1
        return int(hex(val ^ mask), 16)

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