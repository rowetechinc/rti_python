from rti_python.Ensemble.Ensemble import Ensemble
import logging
import math


class EarthVelocity:
    """
    Earth Velocity DataSet.
    [Bin x Beam] data.
    """

    def __init__(self, num_elements, element_multiplier):
        self.ds_type = 10
        self.num_elements = num_elements
        self.element_multiplier = element_multiplier
        self.image = 0
        self.name_len = 8
        self.Name = "E000003\0"
        self.Velocities = []
        self.Magnitude = []
        self.Direction = []

        # Create enough entries for all the (bins x beams)
        # Initialize with bad values
        for bins in range(num_elements):
            bins = []
            for beams in range(element_multiplier):
                bins.append(Ensemble.BadVelocity)

            self.Velocities.append(bins)                    # Mark Vel Bad
            self.Magnitude.append(Ensemble.BadVelocity)     # Mark Mag Bad
            self.Direction.append(Ensemble.BadVelocity)     # Mark Dir Bad

    def decode(self, data):
        """
        Take the data bytearray.  Decode the data to populate
        the velocities.
        :param data: Bytearray for the dataset.
        """
        packet_pointer = Ensemble.GetBaseDataSize(self.name_len)

        for beam in range(self.element_multiplier):
            for bin_num in range(self.num_elements):
                self.Velocities[bin_num][beam] = Ensemble.GetFloat(packet_pointer, Ensemble().BytesInFloat, data)
                packet_pointer += Ensemble().BytesInFloat

        # Generate Water Current Magnitude and Direction
        self.generate_velocity_vectors()

        logging.debug(self.Velocities)

    def remove_vessel_speed(self, bt_east=0.0, bt_north=0.0, bt_vert=0.0):
        """
        Remove the vessel speed.  If the bottom track data is good and
        the velocity is good, then remove the vessel speed from the earth speed.

        The bottom track velocity is the vessel velocity.  You can also use GPS data as a backup.

        Calculate the East and North component from the GPS speed
        bt_east = Convert.ToSingle(speed * Math.Sin(MathHelper.DegreeToRadian(heading)));
        bt_north = Convert.ToSingle(speed * Math.Cos(MathHelper.DegreeToRadian(heading)));

        :param bt_east: Bottom Track East velocity
        :param bt_north: Bottom Track North velocity
        :param bt_vert: Bottom Track Vertical velocity
        :return:
        """
        # Remove the vessel speed
        for bin_num in range(len(self.Velocities)):
            if self.Velocities[bin_num][0] != Ensemble.BadVelocity:
                self.Velocities[bin_num][0] = self.Velocities[bin_num][0] + bt_east            # Remove vessel speed
            if self.Velocities[bin_num][1] != Ensemble.BadVelocity:
                self.Velocities[bin_num][1] = self.Velocities[bin_num][1] + bt_north           # Remove vessel speed
            if self.Velocities[bin_num][2] != Ensemble.BadVelocity:
                self.Velocities[bin_num][2] = self.Velocities[bin_num][2] + bt_vert            # Remove vessel speed

        # Generate the new vectors after removing the vessel speed
        self.generate_velocity_vectors()

    def generate_velocity_vectors(self):
        """
        Generate the velocity vectors for this object.
        This will set both Magnitude and direction.
        :return:
        """
        self.Magnitude, self.Direction = EarthVelocity.generate_vectors(self.Velocities)

    @staticmethod
    def generate_vectors(earth_vel):
        """
        Generate the velocity vectors.  This will calculate the magnitude and direction
        of the water.  If any of the data is marked bad in a bin, then the magnitude and
        direction will also be marked bad.

        Call this again and set the self.Magnitude and self.Direction when Bottom Track Velocity is
        available.

        :param earth_vel: Earth Velocities[bin][beam]
        :return: [magnitude], [direction]  List with a value for each bin
        """
        mag = []
        dir = []

        for bin_num in range(len(earth_vel)):
            # Verify the data is good
            if earth_vel[bin_num][0] != Ensemble.BadVelocity and earth_vel[bin_num][1] != Ensemble.BadVelocity and earth_vel[bin_num][2] != Ensemble.BadVelocity:
                mag.append(EarthVelocity.calculate_magnitude(earth_vel[bin_num][0], earth_vel[bin_num][1], earth_vel[bin_num][2]))
                dir.append(EarthVelocity.calculate_direction(earth_vel[bin_num][0], earth_vel[bin_num][1]))
            else:
                # Mark the data bad
                mag.append(Ensemble.BadVelocity)
                dir.append(Ensemble.BadVelocity)

        return mag, dir

    @staticmethod
    def calculate_magnitude(east, north, vertical):
        """
        Calculate the magnitude of the water current.
        :param east: Earth East Velocity
        :param north: Earth North Velocity
        :param vertical: Earth Vertical Velocity
        :return: Magnitude value
        """
        return math.sqrt((east*east) + (north*north) + (vertical*vertical))

    @staticmethod
    def calculate_direction(east, north):
        """
        Calculate the direction of the water current.
        This will return a value between 0 and 360.
        :param east: Earth East Velocity
        :param north: Earth North Velocity
        :return: Direction of the water
        """
        dir = (math.atan2(east, north)) * (180.0 / math.pi)

        # The range is -180 to 180
        # This moves it to 0 to 360
        if dir < 0.0:
            dir = 360.0 + dir

        return dir

    def encode(self):
        """
        Encode the data into RTB format.
        :return:
        """
        result = []

        # Generate header
        result += Ensemble.generate_header(self.ds_type,
                                           self.num_elements,
                                           self.element_multiplier,
                                           self.image,
                                           self.name_len,
                                           self.Name)

        # Add the data
        for beam in range(self.element_multiplier):
            for bin_num in range(self.num_elements):
                val = self.Velocities[bin_num][beam]
                result += Ensemble.float_to_bytes(val)

        return result

    def encode_csv(self, dt, ss_code, ss_config, blank, bin_size):
        """
        Encode into CSV format.
        :param dt: Datetime object.
        :param ss_code: Subsystem code.
        :param ss_config: Subsystem Configuration
        :param blank: Blank or first bin position in meters.
        :param bin_size: Bin size in meters.
        :return: List of CSV lines.
        """
        str_result = []

        for beam in range(self.element_multiplier):
            for bin_num in range(self.num_elements):
                # Get the value
                val = self.Velocities[bin_num][beam]

                # Create the CSV string
                str_result.append(Ensemble.gen_csv_line(dt, Ensemble.CSV_EARTH_VEL, ss_code, ss_config, bin_num, beam, blank, bin_size, val))

        # Generate Magnitude and Direction CSV
        for bin_num in range(self.num_elements):
            mag = self.Magnitude[bin_num]
            dir = self.Direction[bin_num]
            str_result.append(Ensemble.gen_csv_line(dt, Ensemble.CSV_MAG, ss_code, ss_config, bin_num, 0, blank, bin_size, mag))
            str_result.append(Ensemble.gen_csv_line(dt, Ensemble.CSV_DIR, ss_code, ss_config, bin_num, 0, blank, bin_size, dir))

        return str_result
