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

    def __init__(self, num_ens, ss_code, ss_config):

        # Store the parameters
        self.num_ens = num_ens
        self.ss_code = ss_code
        self.ss_config = ss_config

        # Create the list to hold the ensembles
        self.ens_beam_list = deque([], self.num_ens)
        self.ens_instr_list = deque([], self.num_ens)
        self.ens_earth_list = deque([], self.num_ens)

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
                if ens.IsBeamVelocity:
                    self.ens_beam_list.append(ens.BeamVelocity.Velocities)
                if ens.IsInstrumentVelocity:
                    self.ens_instr_list.append(ens.InstrumentVelocity.Velocities)
                if ens.IsEarthVelocity:
                    self.ens_earth_list.append(ens.EarthVelocity.Velocities)

    def average(self, is_running_avg=False):
        """
        Average the accumulated data.

        If there were any errors averaging, NONE is returned for the average result.  It no
        data existed, NONE is also returned.  If data type does not exist, NONE is returned.
        :return: Averaged data [Beam, Instrument, Earth]
        """
        avg_beam_results = []
        avg_instr_results = []
        avg_earth_results = []

        # Average the Beam data
        if len(self.ens_beam_list) >= self.num_ens:
            avg_beam_results = self.avg_beam_data()

        # Average the Instrument data
        if len(self.ens_instr_list) >= self.num_ens:
            avg_instr_results = self.avg_instr_data()

        # Average the Earth data
        if len(self.ens_earth_list) >= self.num_ens:
            avg_earth_results = self.avg_earth_data()

        # Clear the lists
        if not is_running_avg:
            self.ens_beam_list.clear()
            self.ens_instr_list.clear()
            self.ens_earth_list.clear()

        return [avg_beam_results, avg_instr_results, avg_earth_results]

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
        self.thread_lock.acquire(True, 1000)

        # Create a deep copy of the data
        # This will make it thread safe
        deep_copy_vel = copy.deepcopy(vel)

        for ens_vel in deep_copy_vel:
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
        self.thread_lock.release()

        # Average the data accumulate
        for ens_bin in range(len(avg_accum)):
            for beam in range(len(avg_accum[0])):
                if avg_count[ens_bin][beam] > 0:                                # Verify data was accumulated
                    avg_vel[ens_bin][beam] = avg_accum[ens_bin][beam] / avg_count[ens_bin][beam]    # Average data

        return avg_vel
