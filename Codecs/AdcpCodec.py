import logging
from rti_python.Codecs.BinaryCodec import BinaryCodec
from rti_python.Codecs.BinaryCodecUdp import BinaryCodecUdp
from rti_python.Codecs.WaveForceCodec import WaveForceCodec
from rti_python.Utilities.events import EventHandler
from obsub import event


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

    def enable_waveforce_codec(self, ens_in_burst, path, lat, lon, bin1, bin2, bin3, ps_depth, height_source, corr_thresh, pressure_offset):
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
        :param height_source Height source selected.
        :param corr_thresh Correlation Threshold to mark data bad.  (0.0 - 1.0)
        :param pressure_offset Pressure Sensor offset in meters to add to pressure depth.
        :return:
        """

        self.WaveForceCodec.process_data_event += self.process_wave_data
        self.WaveForceCodec.init(ens_in_burst, path, lat, lon, bin1, bin2, bin3, ps_depth, height_source, corr_thresh, pressure_offset)
        self.IsWfcEnabled = True

    def update_settings_waveforce_codec(self, ens_in_burst, path, lat, lon, bin1, bin2, bin3, ps_depth, height_source, corr_thresh, pressure_offset):
        """
        Update the settings in the Waveforce codec.
        :param ens_in_burst: Ensembles in a burst.
        :param path: Path to record the burst matlab files.
        :param lat: Latitude where data was recorded.
        :param lon: Longitude where data was recorded.
        :param bin1: First bin to measure.
        :param bin2: Second bin to measure.
        :param bin3: Third bin to measure.
        :param ps_depth: Pressure sensor depth.
        :param height_source Height source selected.
        :param corr_thresh Correlation Threshold to mark data bad. (0.0 - 1.0)
        :param pressure_offset Pressure Sensor offset to add to the pressure depth value in meters.
        :return:
        """

        self.WaveForceCodec.update_settings(ens_in_burst, path, lat, lon, bin1, bin2, bin3, ps_depth, height_source, corr_thresh, pressure_offset)

    def process_ensemble(self, sender, ens):
        """
        Take the ensemble from the codec and pass it to all the subscribers.
        If the WaveForce codec is enabled, pass the ensemble to the WaveForce
        codec to process.
        :param ens: Ensemble data.
        """
        logging.debug("Received processed ensemble")

        # If the WaveForce codec is enabled, then pass the ensemble data to the WaveForce codec
        if self.IsWfcEnabled:
            logging.debug("Send to WaveForce Codec")
            self.WaveForceCodec.add(ens)

        # Pass ensemble to all subscribers of the ensemble data.
        self.EnsembleEvent(ens)

    def process_wave_data(self, sender, file_name):
        # Handle the waves data
        self.publish_waves_event(file_name)
        logging.debug("ADCP Wave Codec Process Data" + file_name)

    @event
    def publish_waves_event(self, file_name):
        logging.debug("Publish waves event" + file_name)
