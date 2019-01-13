import datetime
import humanize
import os


class RtiBinaryWriter:
    """
    Create a writer to write data to a file.
    """

    def __init__(self, folder_path=None, header="RTI_", extension=".ens", max_file_size=16):
        """
        Create an object to write binary data to a file.
        :param folder_path: Folder path to store the data.  Default: User Folder depending on OS
        :param header: What to put in the beginning of the file name.  Default: RTI_
        :param extension: File extension.  Default: .ens
        :param max_file_size: Maximum file size.  Default: 16mb
        """

        BYTES_PER_MB = 1048576
        self.max_file_size = max_file_size * BYTES_PER_MB
        self.folder_path = folder_path
        self.header = header
        self.extension = extension

        if not self.folder_path:
            self.folder_path = os.path.expanduser('~')

        file_path = self.create_file_name(self.folder_path, header=header, extension=extension)
        self.file = open(file_path, "wb")

        self.bytes_written = 0          # Bytes written for current file
        self.total_bytes = 0            # All bytes written since start

    def write(self, data):
        # Write data
        self.file.write(data)

        # Monitor bytes written
        self.bytes_written += len(data)
        self.total_bytes += len(data)

        # Check if the file exceeds the max file size
        # If it does, create a new file
        if self.bytes_written > self.max_file_size:
            file_path = self.create_file_name(self.folder_path, self.header, self.extension)
            self.close()
            self.file = open(file_path, "wb")
            self.bytes_written = 0

    def get_current_file_bytes_written(self):
        return humanize.naturalsize(self.bytes_written, binary=True)

    def get_total_bytes_written(self):
        return humanize.naturalsize(self.total_bytes, binary=True)

    def get_file_path(self):
        return self.file.name

    def close(self):
        self.file.close()

    def create_file_name(self, folder, header="RTI_", extension=".ens"):
        now = datetime.datetime.now()
        file_name_date = now.strftime("%Y%m%d_%H%M%S")

        return folder + os.sep + header + file_name_date + extension
