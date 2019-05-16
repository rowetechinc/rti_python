import tkinter as tk
from tkinter import filedialog
from rti_python.Utilities.read_binary_file import ReadBinaryFile
from tqdm import tqdm

class RtiCheckFile:
    """
    Check for any issues in ensemble file.
    """

    def __init__(self):
        self.prev_ens_num = 0
        self.is_missing_ens = False
        self.is_status_issue = False
        self.file_path = ""
        self.pbar = tqdm()
        self.first_ens = None
        self.last_ens = None
        self.ens_count = 0
        self.found_issues = 0
        self.found_issue_str = ""

    def process(self):
        """
        Display a dialog to select a file.  Then read the file and look for any issues in the file.
        :return:
        """
        # Dialog to ask for a file to select
        root = tk.Tk()
        root.withdraw()
        self.file_path = filedialog.askopenfilename()

        if self.file_path:
            reader = ReadBinaryFile()
            reader.ensemble_event += self.ens_handler
            reader.playback(self.file_path)

            # Print the summary at the end
            self.print_summary()

        # Close the progress bar
        self.pbar.close()

    def print_summary(self):
        """
        Print a summary of the results.
        :return:
        """
        print("---------------------------------------------")
        print("---------------------------------------------")
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
        print("Total number of ensembles in file: " + str(self.ens_count))

        # Check results for any fails
        if self.is_missing_ens or self.is_status_issue:
            print(str(self.found_issues) + " ISSUES FOUND WITH FILE")
            print("*********************************************")
            print(self.found_issue_str)
            print("*********************************************")
        else:
            if not self.prev_ens_num == 0:
                print("File " + self.file_path + " checked and is all GOOD.")
            else:
                print("No RTB Ensembles Found in: " + self.file_path)
        print("---------------------------------------------")
        print("---------------------------------------------")

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
        self.pbar.update(1)

    def check_status(self, ens):
        """
        Check the status for any errors.
        :param ens: Ensemble data.
        :return: True = Found an issue
        """
        if ens.IsEnsembleData:
            if not ens.EnsembleData.Status == 0:
                err_str = "Error in ensemble " + str(ens.EnsembleData.EnsembleNumber) + "\tStatus: [" + str(hex(ens.EnsembleData.Status)) + "]: " + ens.EnsembleData.status_str()
                print(err_str)
                self.found_issue_str += err_str + "\n"
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
                    print(err_str)
                    self.found_issue_str += err_str + "\n"
                    found_issue = True

            self.prev_ens_num = ens.EnsembleData.EnsembleNumber

        return found_issue


if __name__ == "__main__":
    checker = RtiCheckFile()
    checker.process()
