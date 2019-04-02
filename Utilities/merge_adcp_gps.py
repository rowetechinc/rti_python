import os
from os import listdir
from os.path import isfile, join
import logging

from rti_python.Codecs.BinaryCodec import BinaryCodec


class MergeAdcpGps:

    def __init__(self, gps_folder_path, adcp_folder_path):
        # Usually GPS messages come in blocks
        # List the last GPS message in the block
        # Then the GPS file will be divided by this message
        # A date and time will then be associated with this block based
        # off one of the GPS messages (GGA) in the block
        self.LAST_GPS_ID = '$GPRMC'

        # GPS List.  The list will contain a block
        # The block will contain 1 or more GPS messages.
        self.gps_list = []

        # ADCP List.  List of all the ADCP data.
        self.adcp_list = []

        # Load the GPS data
        self.load_gps_dir(gps_folder_path)

        # Load the ADCP data
        self.load_adcp_dir(adcp_folder_path)

        # Merge the ADCP and GPS data
        self.merge_data()

    def load_gps_dir(self, folder_path):
        """
        Load all the GPS data in the GPS directory.
        :param folder_path: GPS folder path.
        :return:
        """

        # Get a list of all the files in the GPS dir
        gps_files = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]

        # Read in all the GPS data
        for gps in gps_files:
            self.read_gps_data(folder_path + os.sep + gps)

    def read_gps_data(self, file_name):
        """
        Read in the GPS data from the file.
        Create blocks of GPS data based off the last GPS ID.
        :param file_name: File path
        :return:
        """

        # Create a temp list to create a GPS block
        temp_gps_list = []

        with open(file_name, 'r', encoding='utf-8') as f:
            # Read in the line from the file
            for gps_line in f:

                # Add it to the temp list
                temp_gps_list.append(gps_line)

                # When the last GPS id is found, add it to the list
                if self.LAST_GPS_ID in gps_line:
                    self.gps_list.append(temp_gps_list)

                    # Create a new list
                    temp_gps_list = []

        # Close the file
        f.close()

    def load_adcp_dir(self, folder_path):
        """
        Load all the ADCP data in the ADCP directory.
        :param folder_path: ADCP folder path.
        :return:
        """

        # Get a list of all the files in the GPS dir
        adcp_files = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]

        # Read in all the GPS data
        for adcp in adcp_files:
            self.read_adcp_data(folder_path + os.sep + adcp)

    def read_adcp_data(self, file_path):
        #with open(file_path, "rb") as f:
        #    self.logger.debug("Loading file: " + str(file_path))

        #    # Read in the file
        #    for chunk in iter(lambda: f.read(4096), b''):
        #        self.adcp_codec.add(chunk)

        DELIMITER = b'\x80' * 16

        # Open the file
        file = open(file_path, 'rb')

        # Split the data by delimiter
        ens_raw = file.read().split(DELIMITER)

        # Close the file
        file.close()

        for ens_data in ens_raw:
            # Verify the ENS data is good
            # This will check that all the data is there and the checksum is good
            if BinaryCodec.verify_ens_data(DELIMITER + ens_data):
                # Decode the ens binary data
                ens = BinaryCodec.decode_data_sets(DELIMITER + ens_data)

                # Add the ensemble to the list
                if ens:
                    self.adcp_list.append(ens)
                    print(".")

    def merge_data(self):
        for ens in self.adcp_list:
            if ens.IsEnsembleData:
                print(str(ens.EnsembleData.datetime()))


if __name__ == '__main__':

    #FORMAT = '%(asctime)s - %(levelname)s - %(module)s - (%(threadName)-10s) - %(message)s'
    #logging.basicConfig(format=FORMAT, level=logging.DEBUG)

    gps_folder = "G:\\RTI\\data\\uw\\gps"
    adcp_folder = "G:\\RTI\\data\\uw\\ADCP"

    MergeAdcpGps(gps_folder, adcp_folder)