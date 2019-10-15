import tkinter as tk
from tkinter import filedialog
from rti_python.Utilities.read_binary_file import ReadBinaryFile
from tqdm import tqdm
from obsub import event
import logging

class RtiCheckFile:
    """
    Check for any issues in ensemble file.
    """

    def __init__(self):
        self.ens_count = 0
        self.found_issues = 0
        self.found_issue_str = ""
        self.prev_ens_num = 0
        self.is_missing_ens = False
        self.is_status_issue = False
        self.is_voltage_issue = False
        self.is_amplitude_0db_issue = False
        self.is_correlation_100pct_issue = False
        self.file_path = ""
        self.pbar = None
        self.first_ens = None
        self.last_ens = None
        self.show_live_errors = False
        self.bad_status_count = 0
        self.missing_ens_count = 0
        self.bad_voltage_count = 0
        self.bad_amp_0db_count = 0
        self.bad_corr_100pct_count = 0

    def init(self):
        """
        Initialize the value for the next file.
        :return:
        """
        self.prev_ens_num = 0
        #self.is_missing_ens = False
        #self.is_status_issue = False
        self.file_path = ""
        self.pbar = None
        self.first_ens = None
        self.last_ens = None

    def select_and_process(self, show_live_error=False):
        """
        Create a dialog box to select the files.
        Then process the files.
        :param show_live_error: TRUE = Show the errors as they are found.
        :return:
        """

        files = self.select_files()
        self.process(files, show_live_error)

    def select_files(self):
        """
        Display a dialog box to select the files.
        :return: List of all the files selected.
        """
        # Dialog to ask for a file to select
        root = tk.Tk()
        root.withdraw()
        self.file_path = filedialog.askopenfilenames()

        return self.file_path

    def process(self, file_path, show_live_error=False):
        """
        Read the files and look for any issues in the files.
        :param show_live_error: TRUE = Show the errors as they are found.
        :return:
        """
        self.file_path = file_path
        self.show_live_errors = show_live_error

        if self.file_path:
            for file in self.file_path:
                reader = ReadBinaryFile()
                reader.ensemble_event += self.ens_handler               # Wait for ensembles
                reader.file_progress += self.file_progress_handler      # Monitor file progress
                self.init()                                             # Reinitialize values for next file
                reader.playback(file)                                   # Read the file for ensembles

                # Print the summary at the end
                self.print_summary(file)

                # Close the progress bar
                self.pbar.close()

    def print_summary(self, file_path):
        """
        Print a summary of the results.
        :param file_path: File path for the complete file
        :param show_live_error: TRUE = Show the errors as they are found.
        :return:
        """
        print("---------------------------------------------")
        print("---------------------------------------------")

        # Check results for any fails
        if self.is_missing_ens or self.is_status_issue or self.is_voltage_issue or self.is_amplitude_0db_issue or self.is_correlation_100pct_issue:
            print(str(self.found_issues) + " ISSUES FOUND WITH FILES")
            print("*********************************************")
            print(self.found_issue_str)
            print("Total Bad Status: " + str(self.bad_status_count))
            print("Total Missing Ensembles: " + str(self.missing_ens_count))
            print("Total Bad Voltage: " + str(self.bad_voltage_count))
            print("Total Bad Amplitude (0dB): " + str(self.bad_amp_0db_count))
            print("Total Bad Correlation (100%): " + str(self.bad_corr_100pct_count))
            print("*********************************************")
        else:
            if not self.prev_ens_num == 0:
                print("File " + file_path + " checked and is all GOOD.")
            else:
                print("No RTB Ensembles Found in: " + self.file_path)

        # Print info on first and last ensembles
        if self.first_ens and self.first_ens.IsEnsembleData:
            first_ens_dt = self.first_ens.EnsembleData.datetime_str()
            first_ens_num = self.first_ens.EnsembleData.EnsembleNumber
            print("First ENS:\t[" + str(first_ens_num) + "] " + first_ens_dt)

        if self.last_ens and self.last_ens.IsEnsembleData:
            last_ens_dt = self.last_ens.EnsembleData.datetime_str()
            last_ens_num = self.last_ens.EnsembleData.EnsembleNumber
            print("Last ENS:\t[" + str(last_ens_num) + "] " + last_ens_dt)

        # Print total number of ensembles in the file
        print("Total number of bad ensembles in file: " + str(self.found_issues))
        print("Total number of ensembles in file: " + str(self.ens_count))
        if self.ens_count > 0:
            print("Percentage of ensembles found bad: " + str(round((self.found_issues / self.ens_count)*100.0, 3)) + "%")

        print("---------------------------------------------")
        print("---------------------------------------------")

    def file_progress_handler(self, sender, bytes_read, total_size, file_name):
        """
        Monitor the file playback progress.
        :param sender: NOT USED
        :param total_size: Total size.
        :param bytes_read: Total Bytes read.
        :param block_size: Number of bytes read in this iteration.
        :return:
        """
        if self.pbar is None:
            self.pbar = tqdm(total=total_size)

        self.pbar.update(int(bytes_read))

    def ens_handler(self, sender, ens):
        """
        Process the ensemble data.  Check for any issues.
        :param sender: NOT USED.
        :param ens: Ensemble data
        :return:
        """

        # Set first and last ensemble
        if not self.first_ens:
            self.first_ens = ens
        self.last_ens = ens

        # Checking missing Ensemble
        is_missing_ens, prev_ens, err_str  = RtiCheckFile.check_missing_ens(ens, self.prev_ens_num, self.show_live_errors)
        self.prev_ens_num = prev_ens        # Log previous ens
        if is_missing_ens:
            self.is_missing_ens = True
            self.found_issues += 1
            self.found_issue_str += err_str + "\n"
            self.missing_ens_count += 1

        # Check status
        is_status_issue, err_str = self.check_status(ens, self.show_live_errors)
        if is_status_issue:
            self.is_status_issue = True
            self.found_issues += 1
            self.found_issue_str += err_str + "\n"
            self.bad_status_count += 1

        is_voltage_issue, err_str = self.check_voltage(ens, self.show_live_errors)
        if is_voltage_issue:
            self.is_voltage_issue = True
            self.found_issues += 1
            self.found_issue_str += err_str + "\n"
            self.bad_voltage_count += 1

        is_amplitude_0db_issue, err_str = self.check_amplitude_0db(ens, self.show_live_errors)
        if is_amplitude_0db_issue:
            self.is_amplitude_0db_issue = True
            self.found_issues += 1
            self.found_issue_str += err_str + "\n"
            self.bad_amp_0db_count += 1

        is_correlation_100pct_issue, err_str = self.check_correlation_1pct(ens, self.show_live_errors)
        if is_correlation_100pct_issue:
            self.is_correlation_100pct_issue = True
            self.found_issues += 1
            self.found_issue_str += err_str + "\n"
            self.bad_corr_100pct_count += 1

        # Count the number of ensembles
        self.ens_count += 1

        # Update the progress bar
        #self.pbar.update(1)

        # Send ensemble to event to let other objects process the data
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

    @staticmethod
    def check_status(ens, show_live_errors):
        """
        Check the status for any errors.
        :param ens: Ensemble data.
        :param show_live_errors: Show the errors occurring as file is read in or wait until entire file complete
        :return: True = Found an issue
        """
        err_str = ""
        found_issue = False

        if ens.IsEnsembleData:
            if not ens.EnsembleData.Status == 0:
                err_str = "Error in ensemble: " + str(ens.EnsembleData.EnsembleNumber) + "\tStatus: [" + str(hex(ens.EnsembleData.Status)) + "]: " + ens.EnsembleData.status_str()

                # Display the error if turned on
                if show_live_errors:
                    print(err_str)

                # Record the error
                found_issue = True

        return found_issue, err_str

    @staticmethod
    def check_missing_ens(ens, prev_ens_num, show_live_errors=False):
        """
        Check if the ensemble numbers are not in order.
        :param ens: Ensemble
        :param prev_ens_num: Previous ensemble number to compare against
        :param show_live_errors: Show the errors occurring as file is read in or wait until entire file complete
        :return: TRUE = Found an Issue
        """
        found_issue = False
        err_str = ""

        if ens.IsEnsembleData:
            if not prev_ens_num == 0:
                if not ens.EnsembleData.EnsembleNumber == (prev_ens_num + 1):
                    err_str = "Missing Ensemble: " + str(prev_ens_num + 1)

                    # Display the error if turned on
                    if show_live_errors:
                        print(err_str)

                    # Record the error
                    found_issue = True

            # Keep track of the previous ensemble number
            prev_ens_num = ens.EnsembleData.EnsembleNumber

        return found_issue, prev_ens_num, err_str

    @staticmethod
    def check_voltage(ens, show_live_errors):
        """
        Check if the voltage is above 36 volts or below 12v.
        The ADCP cannot handle these voltages.
        :param ens: Ensemble data.
        :param show_live_errors: Show the errors occurring as file is read in or wait until entire file complete
        :return: True = Found an issue
        """
        err_str = ""
        found_issue = False

        if ens.IsEnsembleData:
            if ens.SystemSetup.Voltage > 36 or ens.SystemSetup.Voltage < 12:
                err_str = "Error in ensemble: " + str(ens.EnsembleData.EnsembleNumber) + "\tVoltage: [" + str(ens.SystemSetup.Voltage) + "]"

                # Display the error if turned on
                if show_live_errors:
                    print(err_str)

                # Record the error
                found_issue = True

        return found_issue, err_str

    @staticmethod
    def check_amplitude_0db(ens, show_live_errors):
        """
        Check if the amplitude is less than 10 db.  If a majority of the
        bins are less then 10 dB, then there is an issue.
        :param ens: Ensemble data.
        :param show_live_errors: Show the errors occurring as file is read in or wait until entire file complete
        :return: True = Found an issue
        """
        err_str = ""
        found_issue = False

        if ens.IsAmplitude:

            # Get the number of bins and beams
            bin_count = ens.Amplitude.num_elements

            # Initialize the list with all 0's with each beam
            bad_bin = [0] * ens.Amplitude.element_multiplier

            for beam in range(ens.Amplitude.element_multiplier):
                for bin_num in range(ens.Amplitude.num_elements):

                    # Accumulate the bad bins
                    if ens.Amplitude.Amplitude[bin_num][beam] <= 7.0:
                        bad_bin[beam] += 1

            # Log all the bad beams
            bad_beams = ""
            for beam_check in range(ens.Amplitude.element_multiplier):
                if bad_bin[beam_check] > int(bin_count * 0.8):
                    bad_beams += str(beam_check) + ","

            if bad_beams:
                err_str = "Error in ensemble: " + str(ens.EnsembleData.EnsembleNumber) + " Amplitude[" + str(bad_beams[:-1]) + "] : 0 dB"

                # Display the error if turned on
                if show_live_errors:
                    print(err_str)

                # Record the error
                found_issue = True

        return found_issue, err_str

    @staticmethod
    def check_correlation_1pct(ens, show_live_errors):
        """
        Check if the correlation is less than 100 percent (1.0).  If a majority of the
        bins are 100 percent, then there is an issue.
        :param ens: Ensemble data.
        :param show_live_errors: Show the errors occurring as file is read in or wait until entire file complete
        :return: True = Found an issue
        """
        err_str = ""
        found_issue = False

        if ens.IsCorrelation:

            # Get the number of bins and beams
            bin_count = ens.Correlation.num_elements

            # Initialize the list with all 0's with each beam
            bad_bin = [0] * ens.Correlation.element_multiplier

            for beam in range(ens.Correlation.element_multiplier):
                for bin_num in range(ens.Correlation.num_elements):

                    # Accumulate the bad bins
                    if ens.Correlation.Correlation[bin_num][beam] >= 1.0:
                        bad_bin[beam] += 1

            # Log all the bad beams
            bad_beams = ""
            for beam_check in range(ens.Correlation.element_multiplier):
                if bad_bin[beam_check] > int(bin_count * 0.8):
                    bad_beams += str(beam_check) + ","

            if bad_beams:
                err_str = "Error in ensemble: " + str(ens.EnsembleData.EnsembleNumber) + " Correlation[" + str(bad_beams[:-1]) + "] : 100%"

                # Display the error if turned on
                if show_live_errors:
                    print(err_str)

                # Record the error
                found_issue = True

        return found_issue, err_str


if __name__ == "__main__":
    checker = RtiCheckFile()
    checker.select_and_process()
