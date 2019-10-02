import tkinter as tk
from tkinter import filedialog
from rti_python.Utilities.read_binary_file import ReadBinaryFile
from tqdm import tqdm

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
        self.file_path = ""
        self.pbar = None
        self.first_ens = None
        self.last_ens = None
        self.show_live_errors = False
        self.bad_status_count = 0
        self.missing_ens_count = 0

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
        if self.is_missing_ens or self.is_status_issue:
            print(str(self.found_issues) + " ISSUES FOUND WITH FILES")
            print("*********************************************")
            print(self.found_issue_str)
            print("Total Bad Status: " + str(self.bad_status_count))
            print("Total Missing Ensembles: " + str(self.missing_ens_count))
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
        is_missing_ens = self.check_missing_ens(ens)
        if is_missing_ens:
            self.is_missing_ens = True
            self.found_issues += 1

        # Check status
        is_status_issue = self.check_status(ens)
        if is_status_issue:
            self.is_status_issue = True
            self.found_issues += 1

        # Count the number of ensembles
        self.ens_count += 1

        # Update the progress bar
        #self.pbar.update(1)

    def check_status(self, ens):
        """
        Check the status for any errors.
        :param ens: Ensemble data.
        :return: True = Found an issue
        """
        if ens.IsEnsembleData:
            if not ens.EnsembleData.Status == 0:
                err_str = "Error in ensemble: " + str(ens.EnsembleData.EnsembleNumber) + "\tStatus: [" + str(hex(ens.EnsembleData.Status)) + "]: " + ens.EnsembleData.status_str()

                # Display the error if turned on
                if self.show_live_errors:
                    print(err_str)

                # Record the error
                self.found_issue_str += err_str + "\n"
                self.bad_status_count += 1
                return True

        return False

    def check_missing_ens(self, ens):
        """
        Check if the ensemble numbers are not in order.
        :param ens: Ensemble
        :return: TRUE = Found an Issue
        """
        found_issue = False

        if ens.IsEnsembleData:
            if not self.prev_ens_num == 0:
                if not ens.EnsembleData.EnsembleNumber == (self.prev_ens_num + 1):
                    err_str = "Missing Ensemble: " + str(self.prev_ens_num + 1)

                    # Display the error if turned on
                    if self.show_live_errors:
                        print(err_str)

                    # Record the error
                    self.found_issue_str += err_str + "\n"
                    self.missing_ens_count += 1
                    found_issue = True

            self.prev_ens_num = ens.EnsembleData.EnsembleNumber

        return found_issue


if __name__ == "__main__":
    checker = RtiCheckFile()
    checker.select_and_process()
