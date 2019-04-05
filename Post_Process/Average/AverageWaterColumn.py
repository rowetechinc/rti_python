from collections import deque
import logging
from rti_python.Ensemble.Ensemble import Ensemble
from threading import Lock
import copy


class AverageWaterColumn:
    """
    Average the water column
    This will average the Beam, Instrument and Earth veocity.

    Screening of the data should be done before data is added to the
    accumulator.

    This uses deque instead of a list because it has better performance
    for popping the first element.
    """

    # Index for the results
    INDEX_BEAM = 0
    INDEX_INSTRUMENT = 1
    INDEX_EARTH = 2
    INDEX_MAG = 3
    INDEX_DIR = 4
    INDEX_PRESSURE = 5
    INDEX_XDCR_DEPTH = 6
    INDEX_FIRST_TIME = 7
    INDEX_LAST_TIME = 8

    def __init__(self, num_ens, ss_code, ss_config):

        # Store the parameters
        self.num_ens = num_ens
        self.ss_code = ss_code
        self.ss_config = ss_config

        # Create the list to hold the ensembles
        self.ens_beam_list = deque([], self.num_ens)
        self.ens_instr_list = deque([], self.num_ens)
        self.ens_earth_list = deque([], self.num_ens)
        self.ens_magnitude = deque([], self.num_ens)
        self.ens_direction = deque([], self.num_ens)
        self.pressure = deque([], self.num_ens)
        self.xdcr_depth = deque([], self.num_ens)
        self.blank = 0.0
        self.bin_size = 0.0
        self.first_time = None
        self.last_time = None

        self.thread_lock = Lock()

    def add_ens(self, ens):
        """
        Check if the ensemble has the same subsystem configuration and subsystem code.
        If they match, then accumulate the velocity data if it exist.

        :param ens: Ensemble to accumulate and average
        :return:
        """
        if ens.IsEnsembleData:
            # Check if the subsystem config and code match
            # Then add the velocity data to the list
            if ens.EnsembleData.SubsystemConfig == self.ss_config and ens.EnsembleData.SysFirmwareSubsystemCode == self.ss_code:
                if ens.IsAncillaryData:
                    self.blank = ens.AncillaryData.FirstBinRange
                    self.bin_size = ens.AncillaryData.BinSize
                    self.pressure.append([ens.AncillaryData.Pressure])
                    self.xdcr_depth.append([ens.AncillaryData.TransducerDepth])
                if ens.IsBeamVelocity:
                    self.ens_beam_list.append(ens.BeamVelocity.Velocities)
                if ens.IsInstrumentVelocity:
                    self.ens_instr_list.append(ens.InstrumentVelocity.Velocities)
                if ens.IsEarthVelocity:
                    self.ens_earth_list.append(ens.EarthVelocity.Velocities)
                    self.ens_magnitude.append(ens.EarthVelocity.Magnitude)
                    self.ens_direction.append(ens.EarthVelocity.Direction)

                # Set the times
                if not self.first_time:
                    self.first_time = ens.EnsembleData.datetime()

                # Always store the last time
                self.last_time = ens.EnsembleData.datetime()

    def average(self, is_running_avg=False):
        """
        Average the accumulated data.

        If there were any errors averaging, NONE is returned for the average result.  It no
        data existed, NONE is also returned.  If data type does not exist, NONE is returned.
        :return: Averaged data [Beam, Instrument, Earth, Mag, Dir]
        """
        first_time = self.first_time
        last_time = self.last_time

        # Average the Beam data
        avg_beam_results = self.avg_beam_data()

        # Average the Instrument data
        avg_instr_results = self.avg_instr_data()

        # Average the Earth data
        avg_earth_results = self.avg_earth_data()

        # Average the Magnitude data
        avg_mag_results = self.avg_mag_data()

        # Average the Direction data
        avg_dir_results = self.avg_dir_data()

        # Average the Pressure data
        avg_pressure_results = self.avg_pressure_data()

        # Average the Pressure data
        avg_xdcr_depth_results = self.avg_xdcr_depth_data()

        # Clear the lists
        if not is_running_avg:
            self.reset()

        return [avg_beam_results, avg_instr_results, avg_earth_results, avg_mag_results, avg_dir_results, avg_pressure_results, avg_xdcr_depth_results, first_time, last_time]

    def reset(self):
        """
        Clear all the list of data.
        Clear the times.
        This can also be used to start the averaging over.
        :return:
        """
        self.ens_beam_list.clear()
        self.ens_instr_list.clear()
        self.ens_earth_list.clear()
        self.ens_magnitude.clear()
        self.ens_direction.clear()
        self.pressure.clear()
        self.xdcr_depth.clear()
        self.first_time = None
        self.last_time = None

    def avg_beam_data(self):
        """
        Average the Beam velocity data
        :return:
        """
        try:
            return self.avg_vel(self.ens_beam_list)
        except Exception as e:
            logging.error("Error processing data to average Beam water column.  " + str(e))
            if self.thread_lock.locked():
                self.thread_lock.release()
            return None

    def avg_instr_data(self):
        """
        Average the Instrument velocity data
        :return:
        """
        try:
            return self.avg_vel(self.ens_instr_list)
        except Exception as e:
            logging.error("Error processing data to average Instrument water column. " + str(e))
            if self.thread_lock.locked():
                self.thread_lock.release()
            return None

    def avg_earth_data(self):
        """
        Average the Earth velocity data
        :return:
        """
        try:
            return self.avg_vel(self.ens_earth_list)
        except Exception as e:
            logging.error("Error processing data to average Earth water column. " + str(e))
            if self.thread_lock.locked():
                self.thread_lock.release()
            return None

    def avg_mag_data(self):
        """
        Average the water current magnitude data
        :return:
        """
        try:
            return self.avg_mag_dir(self.ens_magnitude)
        except Exception as e:
            logging.error("Error processing data to average Magnitude water column. " + str(e))
            if self.thread_lock.locked():
                self.thread_lock.release()
            return None

    def avg_dir_data(self):
        """
        Average the water current direction data
        :return:
        """
        try:
            return self.avg_mag_dir(self.ens_direction)
        except Exception as e:
            logging.error("Error processing data to average Direction water column. " + str(e))
            if self.thread_lock.locked():
                self.thread_lock.release()
            return None

    def avg_pressure_data(self):
        """
        Average the water pressure data
        :return:
        """
        try:
            return self.avg_mag_dir(self.pressure)
        except Exception as e:
            logging.error("Error processing data to average Pressure. " + str(e))
            if self.thread_lock.locked():
                self.thread_lock.release()
            return None

    def avg_xdcr_depth_data(self):
        """
        Average the water Tranducer Depth data
        :return:
        """
        try:
            return self.avg_mag_dir(self.xdcr_depth)
        except Exception as e:
            logging.error("Error processing data to average Transducer Depth. " + str(e))
            if self.thread_lock.locked():
                self.thread_lock.release()
            return None

    def avg_vel(self, vel):
        """
        Average the velocity data given.
        This will verify the number of bins and beams
        is the same between ensembles.  If any ensembles have a different
        number of beams or bins, then a exception will be thrown.

        This will not average the data if the data is BAD VELOCITY.

        :param vel:  Velocity data from each ensemble.
        :return: Average of all the velocities in the all the ensembles.
        """
        # Determine number of bins and beams
        num_bins = 0
        num_beams = 0
        avg_accum = []
        avg_count = []
        avg_vel = None

        # lock the thread when iterating the deque
        #self.thread_lock.acquire(True, 1000)

        # Create a deep copy of the data
        # This will make it thread safe
        #deep_copy_vel = copy.deepcopy(vel)

        for ens_vel in vel:
            temp_num_bins = len(ens_vel)
            temp_num_beams = len(ens_vel[0])

            # Verify the bins and beams has not changed
            if num_beams == 0:
                num_beams = temp_num_beams
            elif num_beams != temp_num_beams:
                logging.error("Number of beams is not consistent between ensembles")
                self.thread_lock.release()
                raise Exception("Number of beams is not consistent between ensembles")

            if num_bins == 0:
                num_bins = temp_num_bins
            elif num_bins != temp_num_bins:
                logging.error("Number of bins is not consistent between ensembles")
                self.thread_lock.release()
                raise Exception("Number of bins is not consistent between ensembles")

            # Create the average lists
            if num_bins != 0 and num_beams != 0 and len(avg_accum) == 0:
                avg_accum = [[0 for ens_bin in range(num_beams)] for beams in range(num_bins)]
                avg_count = [[0 for ens_bin in range(num_beams)] for beams in range(num_bins)]
                avg_vel = [[0 for ens_bin in range(num_beams)] for beams in range(num_bins)]

            # Accumulate the data
            for ens_bin in range(len(ens_vel)):
                for beam in range(len(ens_vel[0])):
                    if ens_vel[ens_bin][beam] != Ensemble.BadVelocity:
                        avg_accum[ens_bin][beam] += ens_vel[ens_bin][beam]      # Accumulate velocity
                        avg_count[ens_bin][beam] += 1                           # Count good data

        # Unlock thread
        #self.thread_lock.release()

        # Average the data accumulate
        for ens_bin in range(len(avg_accum)):
            for beam in range(len(avg_accum[0])):
                if avg_count[ens_bin][beam] > 0:                                # Verify data was accumulated
                    avg_vel[ens_bin][beam] = avg_accum[ens_bin][beam] / avg_count[ens_bin][beam]    # Average data

        return avg_vel

    def avg_mag_dir(self, data):
        """
        Average the magnitude or direction data given.
        This will verify the number of bins
        is the same between ensembles.  If any ensembles have a different
        number of bins, then a exception will be thrown.

        This will not average the data if the data is BAD VELOCITY.

        :param vel:  Magnitude or direction data from each ensemble.
        :return: Average of all the velocities in the all the ensembles.
        """
        # Determine number of bins and beams
        num_bins = 0
        avg_accum = []
        avg_count = []
        avg_vel = None

        # lock the thread when iterating the deque
        #self.thread_lock.acquire(True, 1000)

        # Create a deep copy of the data
        # This will make it thread safe
        #deep_copy_data = copy.deepcopy(data)

        for ens_data in data:
            temp_num_bins = len(ens_data)
            if num_bins == 0:
                num_bins = temp_num_bins
            elif num_bins != temp_num_bins:
                logging.error("Number of bins is not consistent between ensembles")
                self.thread_lock.release()
                raise Exception("Number of bins is not consistent between ensembles")

            # Create the average lists
            if num_bins != 0 and len(avg_accum) == 0:
                avg_accum = [0 for b in range(num_bins)]
                avg_count = [0 for b in range(num_bins)]
                avg_vel = [0 for b in range(num_bins)]

            # Accumulate the data
            for ens_bin in range(len(ens_data)):
                if ens_data[ens_bin] != Ensemble.BadVelocity:
                    avg_accum[ens_bin] += ens_data[ens_bin]           # Accumulate velocity
                    avg_count[ens_bin] += 1                           # Count good data

        # Unlock thread
        #self.thread_lock.release()

        # Average the data accumulate
        for ens_bin in range(len(avg_accum)):
            if avg_count[ens_bin] > 0:                                # Verify data was accumulated
                avg_vel[ens_bin] = avg_accum[ens_bin] / avg_count[ens_bin]    # Average data

        return avg_vel