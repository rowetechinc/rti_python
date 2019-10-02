from rti_python.Codecs.BinaryCodec import BinaryCodec
from obsub import event
import logging
import os


class ReadBinaryFile:

    def playback(self, file_path):
        """
        Playback the given file.  This will read the file
        then call ensemble_rcv to process the ensemble.
        :param file_path: Ensemble file path.
        :return:
        """
        # RTB ensemble delimiter
        DELIMITER = b'\x80' * 16

        BLOCK_SIZE = 4096 *100

        # Create a buffer
        buff = bytes()

        # Get the total file size
        file_size = os.stat(file_path).st_size
        total_bytes_read = 0

        with open(file_path, "rb") as f:
            data = f.read(BLOCK_SIZE)                                   # Read in data

            # Monitor progress
            total_bytes_read += BLOCK_SIZE
            self.file_progress(total_bytes_read, file_size, BLOCK_SIZE)

            while data:                                                 # Verify data was found
                buff += data                                            # Accumulate the buffer
                if DELIMITER in buff:                                   # Check for the delimiter
                    chunks = buff.split(DELIMITER)                      # If delimiter found, split to get the remaining buffer data
                    buff = chunks.pop()                                 # Put the remaining data back in the buffer

                    for chunk in chunks:                                # Take out the ens data
                        self.process_playback_ens(DELIMITER + chunk)    # Process the binary ensemble data

                data = f.read(BLOCK_SIZE)                               # Read the next batch of data

                # Monitor progress
                total_bytes_read += BLOCK_SIZE
                self.file_progress(total_bytes_read, file_size, BLOCK_SIZE)

        # Process whatever is remaining in the buffer
        self.process_playback_ens(DELIMITER + buff)

        # Close the file
        f.close()

    def process_playback_ens(self, ens_bin):
        """
        Process the playback ensemble found.  This will verify the ensemble is good.
        If the data is verified to be a good ensemble, then decode the ensemble and
        pass it to the event handler.
        :param ens_bin: Binary Ensemble data to decode
        :return:
        """
        # Verify the ENS data is good
        # This will check that all the data is there and the checksum is good
        if BinaryCodec.verify_ens_data(ens_bin):
            # Decode the ens binary data
            ens = BinaryCodec.decode_data_sets(ens_bin)

            if ens:
                # Pass the ensemble to the event handler
                self.ensemble_event(ens)

    @event
    def ensemble_event(self, ens):
        """
        Event to subscribe to receive decoded ensembles.
        :param ens: Ensemble object.
        :return:
        """
        if ens.IsEnsembleData:
            logging.debug(str(ens.EnsembleData.EnsembleNumber))

    @event
    def file_progress(self, bytes_read, total_size, block_size):
        """
        Event to subscribe to receive the file progress.

        For tqbm use the following code:
        if self.pbar is None:
            self.pbar = tqdm(total=total_size)

        self.pbar.update(block_size)

        :param total_size: Total size of the file.
        :param bytes_read: Current number of bytes read from the file.
        :param block_size: Number of bytes read in this iteration.
        :return:
        """
        logging.debug("File Progress: " + str(bytes_read) + " : " + str(total_size) + " : " + str(block_size))
