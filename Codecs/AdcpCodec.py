import logging
from Codecs.BinaryCodec import BinaryCodec
from Codecs.BinaryCodecUdp import BinaryCodecUdp
from Codecs.WaveForceCodec import WaveForceCodec
from Utilities.events import EventHandler

logger = logging.getLogger("ADCP Codec")
logger.setLevel(logging.ERROR)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(name)s:%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)


class AdcpCodec:
    """
    ADCP Codec will decode the 
    ADCP data.  There are more than one ADCP format, this will use all the different
    codecs to decode the data.
    """

    def __init__(self, is_udp=False, udp_port=55057):
        if not is_udp:
            self.binary_codec = BinaryCodec()
        else:
            self.binary_codec = BinaryCodecUdp(udp_port)
        self.binary_codec.EnsembleEvent += self.process_ensemble

        # WaveForce codec
        self.WaveForceCodec = WaveForceCodec()
        self.IsWfcEnabled = False

        # Event to receive the ensembles
        self.EnsembleEvent = EventHandler(self)

    def add(self, data):
        """
        Add the data to the codecs.
        :param data: Raw data to add to the codecs.
        """
        self.binary_codec.add(data)

    def enable_waveforce_codec(self, ens_in_burst, path, lat, lon, bin1, bin2, bin3, ps_depth):
        """
        Enable the WaveForce codec.  This data will be encoded
        into the Matlab format.
        :param ens_in_burst: Ensembles in a burst.
        :param path: Path to record the burst matlab files.
        :param lat: Latitude where data was recorded.
        :param lon: Longitude where data was recorded.
        :param bin1: First bin to measure.
        :param bin2: Second bin to measure.
        :param bin3: Third bin to measure.
        :param ps_depth: Pressure sensor depth.
        :return:
        """

        self.WaveForceCodec.init(ens_in_burst, path, lat, lon, bin1, bin2, bin3, ps_depth)
        self.IsWfcEnabled = True

    def process_ensemble(self, sender, ens):
        """
        Take the ensemble from the codec and pass it to all the subscribers.
        If the WaveForce codec is enabled, pass the ensemble to the WaveForce
        codec to process.
        :param ens: Ensemble data.
        """
        logger.debug("Received processed ensemble")

        # If the WaveForce codec is enabled, then pass the ensemble data to the WaveForce codec
        if self.IsWfcEnabled:
            logger.debug("Send to WaveForce Codec")
            self.WaveForceCodec.add(ens)

        # Pass ensemble to all subscribers of the ensemble data.
        self.EnsembleEvent(ens)



