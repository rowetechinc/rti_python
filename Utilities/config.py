import configparser
import os
import logging


class RtiConfig():
    """
    Read and Write a configuration.
    """

    def __init__(self, file_path='config.ini'):
        # Create a default config if no config exist
        if not os.path.exists('config.ini'):
            self.create_default_config()

        # File path to configuration
        self.config_file_path = file_path

        # Current configuration
        self.config = self.read()

    def write(self):
        """
        Write the configuration.
        :return:
        """
        # Load the configuration file
        try:
            with open(self.config_file_path, 'w') as f:
                self.config.write(f)
        except Exception as e:
            logging.error("Error writing configuration. " + e)

    def read(self):
        """
        Read latest configuration in the file.
        :return: Configuration
        """
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file_path)
        return self.config

    def create_default_config(self):
        self.config = configparser.ConfigParser()

        # Write the default config
        self.write(self.config)




