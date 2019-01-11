import datetime
import humanize

class RtiBinaryWriter:
    """
    Create a writer to write data to a file.
    """

    def __init__(self, file_path=None, header="RTI_", extension=".ens"):

        if file_path:
            self.file = open(file_path, "wb")
        else:
            folder_path = "C:\\RTI_Capture\\"
            file_path = self.create_file_name(folder_path, header=header, extension=extension)
            self.file = open(file_path, "wb")

        self.bytes_written = 0

    def write(self, data):
        # Write data
        self.file.write(data)

        # Monitor bytes written
        self.bytes_written = self.bytes_written + len(data)

    def get_bytes_written(self):
        return humanize.naturalsize(self.bytes_written, binary=True)

    def close(self):
        self.file.close()

    def create_file_name(self, folder, header="RTI_", extension=".ens"):
        now = datetime.datetime.now()
        file_name_date = now.strftime("%Y%m%d_%H%M%S")

        return folder + header + file_name_date + extension
