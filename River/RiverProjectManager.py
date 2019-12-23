import h5py
import os
from rti_python.Utilities.config import RtiConfig
from rti_python.River.Transect import Transect


class RiverProjectManager:

    def __init__(self, rti_config: RtiConfig):
        """
        Initialize the list of projects.
        It will look in the directory listed in the config.ini file.
        :param rti_config: RTI Config config.ini file.
        """
        # Set Config file
        self.config = rti_config

        # List of all the projects available
        self.projects = {}

        # Set current project file
        self.prj_file = None

        # Search for all available projects
        self.search_for_projects()

    def search_for_projects(self):
        """
        Search for any projects already created.
        This will look in the directory set in the config.ini
        file for any HDF5 files already created.  If the file
        already exist in the directory, then the project is added
        to the list.
        :return:
        """
        # Look inside the folder for any hdf5 files
        for file in os.listdir(self.config.config['RIVER']['output_dir']):
            if file.endswith(".hdf5"):
                # The project name is the file name without the extension
                prj_name = os.path.splitext(file)

                # Add it to the list
                self.projects[prj_name] = os.path.join(self.config.config['RIVER']['output_dir'], file)

    def get_project_list(self):
        """
        Get the list of available projects.
        :return: List of available projects.
        """
        return self.projects.keys()

    def add_project(self, name: str, project_file_path: str):
        if os.path.exists(project_file_path):
            # Check if the project already exist
            # If it does, create a new project name with an index
            project_already_exist_index = 0

            # Create files paths until a unique file name is found
            while name in self.projects.keys():
                # Create a new name with an index
                name = name + "_" + str(project_already_exist_index)

                project_already_exist_index += 1

            # Add project to the list
            self.projects[name] = project_file_path

            # Create the H5DF file
            self.prj_file = h5py.File(project_file_path, "a")

            # Return the project file
            return self.prj_file

        # Return None if the project HDF5 does not exist
        return None

    def create_project(self, name: str):
        """
        Create a project and add it to the list of projects.
        This will use the name given to create a new project file.
        The file is a HDF5 file.  The project file will contain all
        the settings and transects and discharge calculation results.

        The HDF5 file is created in the directory set in the config.ini
        file.

        If the project already exist, it will create the project with an
        index number at the end of project name.
        :param name: Name of the project.
        :return: Return the HDF5 project file.
        """
        # Create a file name and path
        file_path = os.path.join(self.config.config['RIVER']['output_dir'], name + ".hdf5")

        # Check if the project already exist
        # If it does, create a new project name with an index
        file_already_exist_index = 0

        # Create a new name with an index
        new_name = name + "_" + str(file_already_exist_index)

        if os.path.exists(file_path):
            # Create a new file with index
            file_path = os.path.join(self.config.config['RIVER']['output_dir'], new_name + ".hdf5")

            # Create files paths until a unique file name is found
            while os.path.exists(file_path):
                file_already_exist_index += 1
                new_name = name + "_" + str(file_already_exist_index)
                file_path = os.path.join(self.config.config['RIVER']['output_dir'], new_name + ".hdf5")

            # Add project to the list
            self.projects[new_name] = os.path.join(self.config.config['RIVER']['output_dir'], new_name + ".hdf5")

            # Set the name variable to new_name now
            name = new_name
        else:
            # Add project to the list using original project name
            self.projects[name] = os.path.join(self.config.config['RIVER']['output_dir'], name + ".hdf5")

        # Create the H5DF file
        self.prj_file = h5py.File(file_path, "a")

        # Create a folder for transects to be stored
        self.prj_file.create_group("transects")

        # Create a folder for moving bed tests
        self.prj_file.create_group("moving_bed_test")

        # Set the name for the project file
        self.prj_file.attrs["Name"] = name

        return self.prj_file

    def create_transect(self, project_name: str, transect: Transect):

        # Verify project is created.
        if project_name not in self.projects:
            self.create_project(project_name)

        # Create a transect within the transect folder
        transect_grp = self.prj_file.create_group("transect/" + transect.get_name())

        # Set the meta data for the transect
        self.set_transect_meta(transect_grp, transect)

    def set_transect_meta(self, transect_grp: h5py.Group, transect: Transect):
        transect_grp.attrs["StationName"] = transect.station_name
        transect_grp.attrs["StationInfo"] = transect.station_info
        transect_grp.attrs["Comments"] = transect.comments



