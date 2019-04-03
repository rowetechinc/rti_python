import os
from os import listdir
from os.path import isfile, join
import logging
from tqdm import tqdm
import pynmea2
import datetime

from rti_python.Codecs.BinaryCodec import BinaryCodec
from rti_python.Ensemble.NmeaData import NmeaData

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
        self.gps_dict = {}

        # ADCP List.  List of all the ADCP data.
        self.adcp_list = []

        # Load the GPS data
        self.load_gps_dir(gps_folder_path)

        # Load the ADCP data and merge it with GPS data
        self.load_adcp_dir(adcp_folder_path)


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

        # Create a NMEA dataset to create a GPS block
        nmea_dataset = NmeaData()

        with open(file_name, 'r', encoding='utf-8') as f:

            print("Loading GPS data: " + file_name)

            # Read in the line from the file
            for gps_line in tqdm(f):
                # Add the NMEA data to the dataset
                nmea_dataset.add_nmea(gps_line)

                # When the last GPS id is found, add it to the list
                if self.LAST_GPS_ID in gps_line:

                    # Create a new entry in the dictionary
                    if nmea_dataset.datetime and nmea_dataset.datetime not in self.gps_dict.keys():
                        self.gps_dict[nmea_dataset.datetime] = nmea_dataset

                    # Create a new dataset
                    nmea_dataset = NmeaData()

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

        # Create Output file path
        file_name = os.path.splitext(file_path)[0]              # Get the file name
        mod_file_path = file_name + "_gps.ens"                  # Create a new file path

        DELIMITER = b'\x80' * 16
        datetime_delta = datetime.timedelta(seconds=1)

        print("Loading file: " + file_path)

        # Open the file
        file = open(file_path, 'rb')

        # Split the data by delimiter
        ens_raw = file.read().split(DELIMITER)

        # Close the file
        file.close()

        with open(mod_file_path, "wb") as output_file:

            for ens_data in tqdm(ens_raw):
                # Verify the ENS data is good
                # This will check that all the data is there and the checksum is good
                if BinaryCodec.verify_ens_data(DELIMITER + ens_data):
                    # Decode the ens binary data
                    ens = BinaryCodec.decode_data_sets(DELIMITER + ens_data)

                    # Add the ensemble to the list
                    if ens:
                        #self.adcp_list.append(ens)
                        # Find the GPS in the dictionary matching the datetime
                        matching_key = [x for x in self.gps_dict.keys() if x and (ens.EnsembleData.datetime() - datetime_delta).time() <= x <= (ens.EnsembleData.datetime() + datetime_delta).time()]

                        # Get the last matching key
                        nmea_ds = None
                        if matching_key:
                            nmea_ds = self.gps_dict[matching_key[-1]]

                        # Add the NMEA data to the file if it exist
                        if nmea_ds:
                            ens.AddNmeaData(nmea_ds)

                        # Write the ensemble to the file
                        output_file.write(ens.encode())

            # Close the file
            output_file.close()


if __name__ == '__main__':

    #FORMAT = '%(asctime)s - %(levelname)s - %(module)s - (%(threadName)-10s) - %(message)s'
    #logging.basicConfig(format=FORMAT, level=logging.DEBUG)

    #gps_folder = "G:\\RTI\\data\\uw\\gps"
    #adcp_folder = "G:\\RTI\\data\\uw\\ADCP"
    gps_folder = "C:\\RTI\\Data\\uw\\gps"
    adcp_folder = "C:\\RTI\\Data\\uw\\ADCP"


    MergeAdcpGps(gps_folder, adcp_folder)
    print("process complete")