import logging
import struct
import copy
from PyCRC.CRCCCITT import CRCCCITT
from threading import Thread, Event, Condition
from rti_python.Ensemble.Ensemble import Ensemble
from rti_python.Codecs.BinaryCodec import BinaryCodec

# Buffer to hold the incoming data
buffer = bytearray()

# Condition
condition = Condition()


class BinaryCodecThreaded:

    def __init__(self):
        # Start the Add Data Thread
        self.add_data_thread = AddDataThread()
        self.add_data_thread.start()

        # Start the Processing Data Thread
        self.process_data_thread = ProcessDataThread()
        self.process_data_thread.start()

    def add_data(self, data):
        self.add_data_thread.add(data)
        #print('data')


class AddDataThread(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.event = Event()
        self.alive = True
        self.temp_data = bytes()

    def add(self, data):
        # Store the data to be buffered
        self.temp_data = data

        # Wakeup the thread
        self.event.set()

    def run(self):
        # Get the global buffer
        # It is shared with the 2 threads
        global buffer

        # Verify the thread is still alive
        while self.alive:

            # Wait to wakeup when data arrives
            self.event.wait(timeout=1000)

            condition.acquire()             # Acquire condition

            buffer += self.temp_data             # Set the data to the buffer

            # Check if enough data is in the buffer to process
            if len(buffer) > Ensemble.HeaderSize + Ensemble.ChecksumSize + 200:
                condition.notify()          # Notify to process the buffer

            condition.release()             # Unlock buffer


class ProcessDataThread(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.alive = True
        self.MAX_TIMEOUT = 5
        self.timeout = 0
        self.DELIMITER = b'\x80' * 16

    def shutdown(self):
        self.alive = False
        condition.acquire()
        condition.notify()
        condition.release()
        self.join()

    def run(self):
        # Get the global buffer
        # It is shared with the 2 threads
        global buffer

        # Create a buffer to hold the ensemble
        bin_ens_list = []
        timeout = 0

        # Verify the thread is still alive
        while self.alive:
            # Wait for data
            condition.acquire()

            if self.DELIMITER in buffer:                        # Check for the delimiter
                chunks = buffer.split(self.DELIMITER)           # If delimiter found, split to get the remaining buffer data
                buffer = chunks.pop()                           # Put the remaining data back in the buffer

                for chunk in chunks:                            # Take out the ens data
                    self.process_ens(self.DELIMITER + chunk)    # Process the binary ensemble data

            # Release lock on buffer
            condition.release()

    def process_ens(self, ens_bin):
        # Verify the ENS data is good
        # This will check that all the data is there and the checksum is good
        if BinaryCodec.verify_ens_data(ens_bin):
            # Decode the ens binary data
            ens = BinaryCodec.decode_data_sets(ens_bin)

            # Pass the ensemble
            if ens:
                #self.ensemble_rcv(None, ens)
                if ens.IsEnsembleData:
                    print(str(ens.EnsembleData.EnsembleNumber))

    def decode_ensemble(self, ensStart):
        """
        Decode the raw ensemble data.  This will check the checksum and verify it is correct,
        then decode each datasets.  Then remove the data from the buffer.
        :param ensStart: Stare of the ensemble in the buffer.
        """
        # Get the global buffer
        # It is shared with the 2 threads
        global buffer

        bin_ens = []

        # Check Ensemble number
        ens_num = struct.unpack("I", buffer[ensStart+16:ensStart+20])

        # Check ensemble size
        payload_size = struct.unpack("I", buffer[ensStart+24:ensStart+28])

        # Ensure the entire ensemble is in the buffer
        if len(buffer) >= ensStart + Ensemble.HeaderSize + payload_size[0] + Ensemble.ChecksumSize:
            # Reset timeout
            self.timeout = 0

            # Check checksum
            checksumLoc = ensStart + Ensemble.HeaderSize + payload_size[0]
            checksum = struct.unpack("I", buffer[checksumLoc:checksumLoc + Ensemble.ChecksumSize])

            # Calculate Checksum
            # Use only the payload for the checksum
            ens = buffer[ensStart + Ensemble.HeaderSize:ensStart + Ensemble.HeaderSize + payload_size[0]]
            calcChecksum = CRCCCITT().calculate(input_data=bytes(ens))
            #print("Calc Checksum: ", calcChecksum)
            #print("Checksum: ", checksum[0])
            #print("Checksum good: ", calcChecksum == checksum[0])

            if checksum[0] == calcChecksum:
                logging.debug(ens_num[0])
                try:
                    # Make a deep copy of the ensemble data
                    bin_ens = copy.deepcopy(buffer[ensStart:ensStart + Ensemble.HeaderSize + payload_size[0]])

                    # Remove ensemble from buffer
                    ens_end = ensStart + Ensemble.HeaderSize + payload_size[0] + Ensemble.ChecksumSize
                    del buffer[0:ens_end]

                except Exception as e:
                    logging.error("Error processing ensemble. ", str(e))
        else:
            logging.warning("Not a complete buffer.  Waiting for data")

            # Give it a couple tries to see if more data will come in to make a complete header
            self.timeout += 1

            # Check for timeout
            if self.timeout > self.MAX_TIMEOUT:
                del buffer[0]
                logging.warning("Buffered data did not have a good header.  Header search TIMEOUT")
                self.timeout = 0

        return bin_ens
