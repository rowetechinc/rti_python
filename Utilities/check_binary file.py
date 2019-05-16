import tkinter as tk
from tkinter import filedialog
from rti_python.Utilities.read_binary_file import ReadBinaryFile


class RtiCheckFile:
    """
    Check for any issues in ensemble file.
    """

    def __init__(self):
        self.prev_ens_num = 0
        self.is_missing_ens = False
        self.is_status_issue = False

    def process(self):
        """
        Display a dialog to select a file.  Then read the file and look for any issues in the file.
        :return:
        """
        # Dialog to ask for a file to select
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()

        reader = ReadBinaryFile()
        reader.ensemble_event += self.ens_handler
        reader.playback(file_path)

        if self.is_missing_ens or self.is_status_issue:
            print("FOUND ISSUE WITH FILE")
        else:
            print("File " + file_path + " checked and is all GOOD.")

    def ens_handler(self, sender, ens):
        """
        Process the ensemble data.  Check for any issues.
        :param sender: NOT USED.
        :param ens: Ensemble data
        :return:
        """
        #print("ens number %s" % ens.EnsembleData.EnsembleNumber)
        # Checking missing Ensemble
        is_missing_ens = self.check_missing_ens(ens)
        if is_missing_ens:
            self.is_missing_ens = True

        # Check status
        is_status_issue = self.check_status(ens)
        if is_status_issue:
            self.is_status_issue = True

    def check_status(self, ens):
        """
        Check the status for any errors.
        :param ens: Ensemble data.
        :return: True = Found an issue
        """
        if ens.IsEnsembleData:
            if not ens.EnsembleData.Status == 0:
                print("Error in ensemble " + str(ens.EnsembleData.EnsembleNumber) + " Status: [" + str(ens.EnsembleData.Status) + "] " + ens.EnsembleData.status_str())
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
                    print("Missing Ensemble: " + str(self.prev_ens_num + 1))
                    found_issue = True

            self.prev_ens_num = ens.EnsembleData.EnsembleNumber

        return found_issue


if __name__ == "__main__":
    checker = RtiCheckFile()
    checker.process()
