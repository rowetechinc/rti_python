from Ensemble.Ensemble import Ensemble
from log import logger


class BottomTrack:
    """
    Ensemble Data DataSet.
    Integer values that give details about the ensemble.
    """

    def __init__(self, num_elements, element_multiplier):
        self.ds_type = 10
        self.num_elements = num_elements
        self.element_multiplier = element_multiplier
        self.image = 0
        self.name_len = 8
        self.Name = "E000010"

        self.FirstPingTime = 0.0
        self.LastPingTime = 0.0
        self.Heading = 0.0
        self.Pitch = 0.0
        self.Roll = 0.0
        self.WaterTemp = 0.0
        self.SystemTemp = 0.0
        self.Salinity = 0.0
        self.Pressure = 0.0
        self.TransducerDepth = 0.0
        self.SpeedOfSound = 0.0
        self.Status = 0.0
        self.NumBeams = 0.0
        self.ActualPingCount = 0.0
        self.Range = []
        self.SNR = []
        self.Amplitude = []
        self.Correlation = []
        self.BeamVelocity = []
        self.BeamGood = []
        self.InstrumentVelocity = []
        self.InstrumentGood = []
        self.EarthVelocity = []
        self.EarthGood = []
        self.SNR_PulseCoherent = []
        self.Amp_PulseCoherent = []
        self.Vel_PulseCoherent = []
        self.Noise_PulseCoherent = []
        self.Corr_PulseCoherent = []

        """
        for beams in range(element_multiplier):
            self.Range.append(Ensemble().BadVelocity)
            self.SNR.append(Ensemble().BadVelocity)
            self.Amplitude.append(Ensemble().BadVelocity)
            self.Correlation.append(Ensemble().BadVelocity)
            self.BeamVelocity.append(Ensemble().BadVelocity)
            self.BeamGood.append(Ensemble().BadVelocity)
            self.InstrumentVelocity.append(Ensemble().BadVelocity)
            self.InstrumentGood.append(Ensemble().BadVelocity)
            self.EarthVelocity.append(Ensemble().BadVelocity)
            self.EarthGood.append(Ensemble().BadVelocity)
        """

    def decode(self, data):
        """
        Take the data bytearray.  Decode the data to populate
        the velocities.
        :param data: Bytearray for the dataset.
        """
        packet_pointer = Ensemble.GetBaseDataSize(self.name_len)

        self.FirstPingTime = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 0, Ensemble().BytesInFloat, data)
        self.LastPingTime = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 1, Ensemble().BytesInFloat, data)
        self.Heading = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 2, Ensemble().BytesInFloat, data)
        self.Pitch = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 3, Ensemble().BytesInFloat, data)
        self.Roll = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 4, Ensemble().BytesInFloat, data)
        self.WaterTemp = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 5, Ensemble().BytesInFloat, data)
        self.SystemTemp = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 6, Ensemble().BytesInFloat, data)
        self.Salinity = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 7, Ensemble().BytesInFloat, data)
        self.Pressure = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 8, Ensemble().BytesInFloat, data)
        self.TransducerDepth = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 9, Ensemble().BytesInFloat, data)
        self.SpeedOfSound = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 10, Ensemble().BytesInFloat, data)
        self.Status = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 11, Ensemble().BytesInFloat, data)
        self.NumBeams = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 12, Ensemble().BytesInFloat, data)
        self.ActualPingCount = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 13, Ensemble().BytesInFloat, data)

        index = 14
        numBeam = int(self.NumBeams)
        for beams in range(numBeam):
            self.Range.append(Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * index, Ensemble().BytesInFloat, data))
            index += 1

        for beams in range(numBeam):
            self.SNR.append(Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * index, Ensemble().BytesInFloat, data))
            index += 1

        for beams in range(numBeam):
            self.Amplitude.append(Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * index, Ensemble().BytesInFloat, data))
            index += 1

        for beams in range(numBeam):
            self.Correlation.append(Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * index, Ensemble().BytesInFloat, data))
            index += 1

        for beams in range(numBeam):
            self.BeamVelocity.append(Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * index, Ensemble().BytesInFloat, data))
            index += 1

        for beams in range(numBeam):
            self.BeamGood.append(Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * index, Ensemble().BytesInFloat, data))
            index += 1

        for beams in range(numBeam):
            self.InstrumentVelocity.append(Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * index, Ensemble().BytesInFloat, data))
            index += 1

        for beams in range(numBeam):
            self.InstrumentGood.append(Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * index, Ensemble().BytesInFloat, data))
            index += 1

        for beams in range(numBeam):
            self.EarthVelocity.append(Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * index, Ensemble().BytesInFloat, data))
            index += 1

        for beams in range(numBeam):
            self.EarthGood.append(Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * index, Ensemble().BytesInFloat, data))
            index += 1

        if self.num_elements > 54:
            for beams in range(numBeam):
                self.SNR_PulseCoherent.append(Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * index, Ensemble().BytesInFloat, data))
                index += 1

            for beams in range(numBeam):
                self.Amp_PulseCoherent.append(Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * index, Ensemble().BytesInFloat, data))
                index += 1

            for beams in range(numBeam):
                self.Vel_PulseCoherent.append(Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * index, Ensemble().BytesInFloat, data))
                index += 1

            for beams in range(numBeam):
                self.Noise_PulseCoherent.append(Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * index, Ensemble().BytesInFloat, data))
                index += 1

            for beams in range(numBeam):
                self.Corr_PulseCoherent.append(Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * index, Ensemble().BytesInFloat, data))
                index += 1
        else:
            # Fill in with 0.0
            for beams in range(numBeam):
                self.SNR_PulseCoherent.append(0.0)

            for beams in range(numBeam):
                self.Amp_PulseCoherent.append(0.0)

            for beams in range(numBeam):
                self.Vel_PulseCoherent.append(0.0)

            for beams in range(numBeam):
                self.Noise_PulseCoherent.append(0.0)

            for beams in range(numBeam):
                self.Corr_PulseCoherent.append(0.0)


        logger.debug(self.FirstPingTime)
        logger.debug(self.LastPingTime)
        logger.debug(self.Heading)
        logger.debug(self.Pitch)
        logger.debug(self.Roll)
        logger.debug(self.Salinity)
        logger.debug(self.SpeedOfSound)
        logger.debug(self.EarthVelocity)



