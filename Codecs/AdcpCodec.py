import logging
from rti_python.Codecs.BinaryCodec import BinaryCodec
from rti_python.Codecs.BinaryCodecUdp import BinaryCodecUdp
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

        # Setup the event handler
        self.binary_codec.ensemble_event += self.process_ensemble

    def shutdown(self):
        """
        Shutdown the object.
        :return:
        """
        self.binary_codec.shutdown()

    def add(self, data):
        """
        Add the data to the codecs.
        :param data: Raw data to add to the codecs.
        """
        self.binary_codec.add(data)

    def process_ensemble(self, sender, ens):
        """
        Take the ensemble from the codec and pass it to all the subscribers.
        If the WaveForce codec is enabled, pass the ensemble to the WaveForce
        codec to process.
        :param ens: Ensemble data.
        """
        logging.debug("Received processed ensemble")

        # Pass ensemble to all subscribers of the ensemble data.
        self.ensemble_event(ens)

    @event
    def ensemble_event(self, ens):
        """
        Event to subscribe to this object to receive the latest ensemble data.
        :param ens: Ensemble object.
        :return:
        """
        logging.debug("Ensemble received")
