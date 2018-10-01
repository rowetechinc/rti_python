import struct
import abc
from Utilities.events import EventHandler

from Ensemble.Ensemble import Ensemble
from Ensemble.BeamVelocity import BeamVelocity
from Ensemble.InstrumentVelocity import InstrumentVelocity
from Ensemble.EarthVelocity import EarthVelocity
from Ensemble.Amplitude import Amplitude
from Ensemble.Correlation import Correlation
from Ensemble.GoodBeam import GoodBeam
from Ensemble.GoodEarth import GoodEarth
from Ensemble.EnsembleData import EnsembleData
from Ensemble.AncillaryData import AncillaryData
from Ensemble.BottomTrack import BottomTrack
from Ensemble.NmeaData import NmeaData
from Ensemble.RangeTracking import RangeTracking
from Ensemble.SystemSetup import SystemSetup

from PyCRC.CRCCCITT import CRCCCITT

from log import logger


class WaveBurstInfo:
    """
    Information about the waves burst setup.
    """

    def __init__(self):
        self.SamplesPerBurst = 0
        self.Lat = ""
        self.Lon = ""
        self.Bin1 = 0
        self.Bin2 = 0
        self.Bin3 = 0


class BinaryCodec:
    """
    Decode RoweTech ADCP Binary data.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.buffer = bytearray()

        self.EnsembleEvent = EventHandler(self)

    def add(self, data):
        """
        Add to buffer and Decode
        :param data: Raw byte data.
        """
        self.buffer.extend(data)
        self.find_ensemble()

    def find_ensemble(self):
        """
        Find the start of an ensemble.  Then find the end of the ensemble.
        Then remove the ensemble from the buffer and process the raw data.
        :return:
        """

        # Look for first 16 bytes of header
        delimiter = b'\x80'*16
        ens_start = self.buffer.find(delimiter)

        if ens_start >= 0 and len(self.buffer) > Ensemble().HeaderSize + ens_start:
            # Decode the Ensemble
            self.decode_ensemble(ens_start)

    def decode_ensemble(self, ensStart):
        """
        Decode the raw ensemble data.  This will check the checksum and verify it is correct,
        then decode each datasets.  Then remove the data from the buffer.
        :param ensStart: Stare of the ensemble in the buffer.
        """

        # Check Ensemble number
        ensNum = struct.unpack("I", self.buffer[ensStart+16:ensStart+20])
        #logger.debug(print(ensNum[0]))
        #print(self.ones_complement(ensNumInv[0]))


        # Check ensemble size
        payloadSize = struct.unpack("I", self.buffer[ensStart+24:ensStart+28])
        #print(payloadSize[0])
        #payloadSizeInv = struct.unpack("I", self.buffer[ensStart+28:ensStart+32])
        #print(self.ones_complement(payloadSizeInv[0]))

        # Ensure the entire ensemble is in the buffer
        if len(self.buffer) >= ensStart + Ensemble().HeaderSize + payloadSize[0] + Ensemble().ChecksumSize:
            # Check checksum
            checksumLoc = ensStart + Ensemble().HeaderSize + payloadSize[0]
            checksum = struct.unpack("I", self.buffer[checksumLoc:checksumLoc + Ensemble().ChecksumSize])

            # Calculate Checksum
            # Use only the payload for the checksum
            ens = self.buffer[ensStart + Ensemble().HeaderSize:ensStart + Ensemble().HeaderSize + payloadSize[0]]
            calcChecksum = CRCCCITT().calculate(input_data=bytes(ens))
            #print("Calc Checksum: ", calcChecksum)
            #print("Checksum: ", checksum[0])
            #print("Checksum good: ", calcChecksum == checksum[0])

            if checksum[0] == calcChecksum:
                logger.debug(ensNum[0])
                try:
                    # Decode data
                    ensemble = self.decode_data_sets(self.buffer[ensStart:ensStart + Ensemble().HeaderSize + payloadSize[0]])

                    # ************************
                    self.process_ensemble(ensemble)
                except Exception as e:
                    logger.error("Error decoding ensemble. ", e)

            # Remove ensemble from buffer
            ensEnd = ensStart + Ensemble().HeaderSize + payloadSize[0] + Ensemble().ChecksumSize
            del self.buffer[0:ensEnd]

    @abc.abstractmethod
    def process_ensemble(self, ens):
        # Pass to event handler
        self.EnsembleEvent(ens)

    def decode_data_sets(self, ens):
        """
        Decode the datasets in the ensemble.
        :param ens: Ensemble data.  Decode the dataset.
        :return: Return the decoded ensemble.
        """
        #print(ens)
        packetPointer = Ensemble().HeaderSize
        type = 0
        numElements = 0
        elementMultiplier = 0
        imag = 0
        nameLen = 0
        name = ""
        dataSetSize = 0

        # Create the ensemble
        ensemble = Ensemble()

        # Add the raw data to the ensemble
        #ensemble.AddRawData(ens)

        # Decode the ensemble datasets
        for x in range(Ensemble().MaxNumDataSets):
            # Check if we are at the end of the payload
            if packetPointer >= len(ens):
                break;

            # Get the dataset info
            ds_type = Ensemble.GetInt32(packetPointer + (Ensemble.BytesInInt32 * 0), Ensemble().BytesInInt32, ens)
            num_elements = Ensemble.GetInt32(packetPointer + (Ensemble.BytesInInt32 * 1), Ensemble().BytesInInt32, ens)
            element_multiplier = Ensemble.GetInt32(packetPointer + (Ensemble.BytesInInt32 * 2), Ensemble().BytesInInt32, ens)
            image = Ensemble.GetInt32(packetPointer + (Ensemble.BytesInInt32 * 3), Ensemble().BytesInInt32, ens)
            name_len = Ensemble.GetInt32(packetPointer + (Ensemble.BytesInInt32 * 4), Ensemble().BytesInInt32, ens)
            name = str(ens[packetPointer+(Ensemble.BytesInInt32 * 5):packetPointer+(Ensemble.BytesInInt32 * 5)+8], 'UTF-8')

            # Calculate the dataset size
            data_set_size = Ensemble.GetDataSetSize(ds_type, name_len, num_elements, element_multiplier)

            # Beam Velocity
            if "E000001" in name:
                logger.debug(name)
                bv = BeamVelocity(num_elements, element_multiplier)
                bv.decode(ens[packetPointer:packetPointer+data_set_size])
                ensemble.AddBeamVelocity(bv)

            # Instrument Velocity
            if "E000002" in name:
                logger.debug(name)
                iv = InstrumentVelocity(num_elements, element_multiplier)
                iv.decode(ens[packetPointer:packetPointer+data_set_size])
                ensemble.AddInstrumentVelocity(iv)

            # Earth Velocity
            if "E000003" in name:
                logger.debug(name)
                ev = EarthVelocity(num_elements, element_multiplier)
                ev.decode(ens[packetPointer:packetPointer+data_set_size])
                ensemble.AddEarthVelocity(ev)

            # Amplitude
            if "E000004" in name:
                logger.debug(name)
                amp = Amplitude(num_elements, element_multiplier)
                amp.decode(ens[packetPointer:packetPointer+data_set_size])
                ensemble.AddAmplitude(amp)

            # Correlation
            if "E000005" in name:
                logger.debug(name)
                corr = Correlation(num_elements, element_multiplier)
                corr.decode(ens[packetPointer:packetPointer+data_set_size])
                ensemble.AddCorrelation(corr)

            # Good Beam
            if "E000006" in name:
                logger.debug(name)
                gb = GoodBeam(num_elements, element_multiplier)
                gb.decode(ens[packetPointer:packetPointer+data_set_size])
                ensemble.AddGoodBeam(gb)

            # Good Earth
            if "E000007" in name:
                logger.debug(name)
                ge = GoodEarth(num_elements, element_multiplier)
                ge.decode(ens[packetPointer:packetPointer+data_set_size])
                ensemble.AddGoodEarth(ge)

            # Ensemble Data
            if "E000008" in name:
                logger.debug(name)
                ed = EnsembleData(num_elements, element_multiplier)
                ed.decode(ens[packetPointer:packetPointer+data_set_size])
                ensemble.AddEnsembleData(ed)

            # Ancillary Data
            if "E000009" in name:
                logger.debug(name)
                ad = AncillaryData(num_elements, element_multiplier)
                ad.decode(ens[packetPointer:packetPointer+data_set_size])
                ensemble.AddAncillaryData(ad)

            # Bottom Track
            if "E000010" in name:
                logger.debug(name)
                bt = BottomTrack(num_elements, element_multiplier)
                bt.decode(ens[packetPointer:packetPointer + data_set_size])
                ensemble.AddBottomTrack(bt)

            # NMEA data
            if "E000011" in name:
                logger.debug(name)
                nd = NmeaData(num_elements, element_multiplier)
                nd.decode(ens[packetPointer:packetPointer + data_set_size])
                ensemble.AddNmeaData(nd)

            # System Setup
            if "E000014" in name:
                logger.debug(name)
                ss = SystemSetup(num_elements, element_multiplier)
                ss.decode(ens[packetPointer:packetPointer + data_set_size])
                ensemble.AddSystemSetup(ss)

            # Range Tracking
            if "E000015" in name:
                logger.debug(name)
                rt = RangeTracking(num_elements, element_multiplier)
                rt.decode(ens[packetPointer:packetPointer + data_set_size])
                ensemble.AddRangeTracking(rt)


            # Move to the next dataset
            packetPointer += data_set_size

        return ensemble





