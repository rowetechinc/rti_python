from rti_python.Codecs.BinaryCodec import BinaryCodec
from obsub import event
import logging


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

        BLOCK_SIZE = 4096

        # Create a buffer
        buff = bytes()

        with open(file_path, "rb") as f:

            # Read in the file
            # for chunk in iter(lambda: f.read(4096), b''):
            #    self.adcp_codec.add(chunk)

            data = f.read(BLOCK_SIZE)  # Read in data

            while data:  # Verify data was found
                buff += data  # Accumulate the buffer
                if DELIMITER in buff:  # Check for the delimiter
                    chunks = buff.split(DELIMITER)  # If delimiter found, split to get the remaining buffer data
                    buff = chunks.pop()  # Put the remaining data back in the buffer

                    for chunk in chunks:  # Take out the ens data
                        self.process_playback_ens(DELIMITER + chunk)  # Process the binary ensemble data

                data = f.read(BLOCK_SIZE)  # Read the next batch of data

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


if __name__ == '__main__':

    import tkinter as tk
    from tkinter import filedialog

    def process_ens_func(sender, ens):
        """
        Receive the data from the file.  It will process the file.
        When an ensemble is found, it will call this function with the
        complete ensemble.
        :param ens: Ensemble to process.
        :return:
        """
        if ens.IsEnsembleData:
            print(str(ens.EnsembleData.EnsembleNumber))

    # Create the file reader to read the binary file
    read_binary = ReadBinaryFile()
    read_binary.ensemble_event += process_ens_func

    # Just define the file path
    #file_path = "/path/to/file/ensembles.ens"

    # GUI to ask for file
    # Ask for a file
    # You can use any way to get the file path
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()

    # Pass the file path to the reader
    read_binary.playback(file_path)




