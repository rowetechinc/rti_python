import struct
import json


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