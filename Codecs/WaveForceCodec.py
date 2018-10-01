import logging
import os
import struct
import threading
from Waves.WaveEnsemble import WaveEnsemble

logger = logging.getLogger("WaveForce Codec")
logger.setLevel(logging.ERROR)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(name)s:%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)


class WaveForceCodec:
    """
    Decode the ensemble data into a WaveForce Matlab file format.
    """

    def __init__(self):
        self.Lat = 0.0
        self.Lon = 0.0
        self.EnsInBurst = 0
        self.FilePath = ""
        self.EnsInBurst = 0
        self.Buffer = []
        self.BufferCount = 0
        self.RecordCount = 0
        self.Bin1 = 0
        self.Bin2 = 0
        self.Bin3 = 0
        self.PressureSensorDepth = 0
        self.firstTime = 0
        self.secondTime = 0         # Used to calculate the sample timing
        self.selected_bin = []

    def init(self, ens_in_burst, path, lat, lon, bin1, bin2, bin3, ps_depth):
        """
        Initialize the wave recorder
        :param ens_in_burst: Number of ensembles in a burst.
        :param path: File path to store the file.
        :param lat: Latitude data.
        :param lon: Longitude data.
        :param bin1: First selected bin.
        :param bin2: Second selected bin.
        :param bin3: Third selected bin.
        :param ps_depth Pressure Sensor depth.  Depth of the ADCP.
        """
        self.EnsInBurst = ens_in_burst
        self.FilePath = path
        self.Lat = lat
        self.Lon = lon
        self.Buffer = []
        self.BufferCount = 0
        self.Bin1 = bin1
        self.Bin2 = bin2
        self.Bin3 = bin3
        self.PressureSensorDepth = ps_depth
        self.RecordCount = 0

        self.selected_bin.append(bin1)
        self.selected_bin.append(bin2)
        self.selected_bin.append(bin3)

        self.firstTime = 0
        self.secondTime = 0         # Used to calculate the sample timing

    def add(self, ens):
        """
        Add the ensemble to the buffer.  When the buffer number has been met,
        process the buffer and output the data to a matlab file.
        :param ens: Ensemble to buffer.
        """
        if self.EnsInBurst > 0:
            logger.debug("Added Ensemble to burst")

            # Add to the buffer
            self.Buffer.append(ens)
            self.BufferCount += 1

            # Process the buffer when a burst is complete
            if self.BufferCount == self.EnsInBurst:
                # Get the ensembles from the buffer
                ens_buff = self.Buffer[0:self.EnsInBurst]

                # Remove the ensembles from the buffer
                del self.Buffer[0:self.EnsInBurst]
                self.BufferCount = 0

                # Process the buffer
                th = threading.Thread(target=self.process, args=[ens_buff])
                th.start()

    def process(self, ens_buff):
        """
        Process all the data in the ensemble buffer.
        :param ens_buff: Ensemble data buffer.
        """
        logger.debug("Process Waves Burst")

        # Local variables
        num_bins = len(self.selected_bin)

        num_4beam_ens = 0
        num_vert_ens = 0

        wus_buff = bytearray()
        wvs_buff = bytearray()
        wzs_buff = bytearray()

        beam_0_vel = bytearray()
        beam_1_vel = bytearray()
        beam_2_vel = bytearray()
        beam_3_vel = bytearray()
        beam_vert_vel = bytearray()

        rt_0 = bytearray()
        rt_1 = bytearray()
        rt_2 = bytearray()
        rt_3 = bytearray()
        rt_vert = bytearray()

        pressure = bytearray()
        vert_pressure = bytearray()

        heading = bytearray()
        pitch = bytearray()
        roll = bytearray()

        water_temp = bytearray()
        height = bytearray()
        avg_range_track = bytearray()

        sel_bins_buff = bytearray()

        ps_depth_buff = bytearray()

        ens_waves_buff = []

        # Convert the buffer to wave ensembles
        # Process the data for each waves ensemble
        for ens in ens_buff:
            # Create a waves ensemble
            ens_wave = WaveEnsemble()
            ens_wave.add(ens, self.selected_bin)

            # Add the waves ensemble to the list
            ens_waves_buff.append(ens_wave)

            if ens_wave.is_vertical_ens:
                # Vertical Beam data
                num_vert_ens += 1

                # Pressure (WZP)
                vert_pressure.extend(struct.pack('f', ens_wave.pressure))

                for sel_bin in range(num_bins):
                    # Beam Velocity (WZ0)
                    beam_vert_vel.extend(struct.pack('f', ens_wave.vert_beam_vel[sel_bin]))

                # Range Tracking (WZR)
                rt_vert.extend(struct.pack('f', ens_wave.range_tracking[0]))

            else:
                # 4 Beam Data
                num_4beam_ens += 1

                pressure.extend(struct.pack('f', ens_wave.pressure))                    # Pressure (WPS)
                heading.extend(struct.pack('f', ens_wave.heading))                      # Heading (WHG)
                pitch.extend(struct.pack('f', ens_wave.pitch))                          # Pitch (WPH)
                roll.extend(struct.pack('f', ens_wave.roll))                            # Roll (WRL)
                water_temp.extend(struct.pack('f', ens_wave.water_temp))                # Water Temp (WTS)
                height.extend(struct.pack('f', ens_wave.height))                        # Height (WHS)
                avg_range_track.extend(struct.pack('f', ens_wave.avg_range_tracking))   # Avg Range Tracking (WAH)

                # Range Tracking (WR0, WR1, WR2, WR3)
                rt_0.extend(struct.pack('f', ens_wave.range_tracking[0]))       # Beam 0 RT
                if ens_wave.num_beams > 1:
                    rt_1.extend(struct.pack('f', ens_wave.range_tracking[1]))   # Beam 1 RT
                if ens_wave.num_beams > 2:
                    rt_2.extend(struct.pack('f', ens_wave.range_tracking[2]))   # Beam 2 RT
                if ens_wave.num_beams > 3:
                    rt_3.extend(struct.pack('f', ens_wave.range_tracking[3]))   # Beam 3 RT

                for sel_bin in range(num_bins):
                    # Earth Velocity (WUS, WVS, WZS)
                    wus_buff.extend(struct.pack('f', ens_wave.east_vel[sel_bin]))
                    wvs_buff.extend(struct.pack('f', ens_wave.north_vel[sel_bin]))
                    wzs_buff.extend(struct.pack('f', ens_wave.vertical_vel[sel_bin]))

                    # Beam Velocity (WB0, WB1, WB2, WB3)
                    beam_0_vel.extend(struct.pack('f', ens_wave.beam_vel[sel_bin][0]))          # Beam 0 Beam Velocity
                    if ens_wave.num_beams > 1:
                        beam_1_vel.extend(struct.pack('f', ens_wave.beam_vel[sel_bin][1]))      # Beam 1 Beam Velocity
                    if ens_wave.num_beams > 2:
                        beam_2_vel.extend(struct.pack('f', ens_wave.beam_vel[sel_bin][2]))      # Beam 2 Beam Velocity
                    if ens_wave.num_beams > 3:
                        beam_3_vel.extend(struct.pack('f', ens_wave.beam_vel[sel_bin][3]))      # Beam 3 Beam Velocity

        # Selected Bins
        if ens_buff[0].IsEnsembleData:
            for sel_bin in range(num_bins):
                bin_ht = ens_buff[0].AncillaryData.FirstBinRange + (self.selected_bin[sel_bin] * ens_buff[0].AncillaryData.BinSize)
                sel_bins_buff.extend(struct.pack('f', bin_ht))

        # Pressure Sensor Depth
        ps_depth_buff.extend(struct.pack('f', self.PressureSensorDepth))

        ba = bytearray()

        ba.extend(self.process_txt(ens_buff[0]))                            # [TXT] Txt to describe burst
        ba.extend(self.process_lat(ens_buff[0]))                            # [LAT] Latitude
        ba.extend(self.process_lon(ens_buff[0]))                            # [LON] Longitude
        ba.extend(self.process_wft(ens_buff[0]))                            # [WFT] Time from the first ensemble
        ba.extend(self.process_wdt(ens_buff))                               # [WDT] Time between ensembles
        ba.extend(self.process_whv(sel_bins_buff, num_bins))                # [WHV] Wave Cell Depths
        ba.extend(self.process_whp(ps_depth_buff))                          # [WHP] Pressure Sensor Height
        ba.extend(self.process_wus(wus_buff, num_4beam_ens, num_bins))      # [WUS] East Velocity
        ba.extend(self.process_wvs(wvs_buff, num_4beam_ens, num_bins))      # [WVS] North Velocity
        ba.extend(self.process_wzs(wzs_buff, num_4beam_ens, num_bins))      # [WZS] Vertical Velocity
        ba.extend(self.process_wb0(beam_0_vel, num_4beam_ens, num_bins))    # [WB0] Beam 0 Beam Velocity
        ba.extend(self.process_wb1(beam_1_vel, num_4beam_ens, num_bins))    # [WB1] Beam 1 Beam Velocity
        ba.extend(self.process_wb2(beam_2_vel, num_4beam_ens, num_bins))    # [WB2] Beam 2 Beam Velocity
        ba.extend(self.process_wb3(beam_3_vel, num_4beam_ens, num_bins))    # [WB3] Beam 3 Beam Velocity
        ba.extend(self.process_wr0(rt_0, num_4beam_ens))                    # [WR0] Beam 0 Range Tracking
        ba.extend(self.process_wr1(rt_1, num_4beam_ens))                    # [WR1] Beam 1 Range Tracking
        ba.extend(self.process_wr2(rt_2, num_4beam_ens))                    # [WR2] Beam 2 Range Tracking
        ba.extend(self.process_wr3(rt_3, num_4beam_ens))                    # [WR3] Beam 3 Range Tracking
        ba.extend(self.process_wps(pressure, num_4beam_ens))                # [WPS] Pressure
        ba.extend(self.process_whg(heading, num_4beam_ens))                 # [WHG] Heading
        ba.extend(self.process_wph(pitch, num_4beam_ens))                   # [WPH] Pitch
        ba.extend(self.process_wrl(roll, num_4beam_ens))                    # [WRL] Roll
        ba.extend(self.process_wts(water_temp, num_4beam_ens))              # [WTS] Water Temp
        ba.extend(self.process_whs(height, num_4beam_ens))                  # [WHS] Wave Height Source. (User Select. Range Tracking Beam or Vertical Beam or Pressure)
        ba.extend(self.process_wah(avg_range_track, num_4beam_ens))         # [WAH] Average Range Tracking

        ba.extend(self.process_wz0(beam_3_vel, num_vert_ens, num_bins))     # [WZ0] Vertical Beam Beam Velocity
        ba.extend(self.process_wzp(vert_pressure, num_vert_ens))            # [WZP] Vertical Beam Pressure
        ba.extend(self.process_wzr(rt_vert, num_vert_ens))                  # [WZR] Vertical Beam Range Tracking

        # Write the file
        self.write_file(ba)

        # Increment the record count
        self.RecordCount += 1

    def write_file(self, ba):
        """
        Write the Bytearray to a file.  Save it with the record number
        :param ba: Byte Array with record data.
        :return:
        """
        # Check if the file path exist, if not, then create the file path
        if not os.path.isdir(self.FilePath):
            os.mkdir(self.FilePath)

        filename = self.FilePath + "D0000" + str(self.RecordCount) + ".mat"
        with open(filename, 'wb') as f:
            f.write(ba)

    def process_txt(self, ens):
        """
        This will give a text description of the burst.  This will include the record number,
        the serial number and the date and time of the burst started.

        Data Type: Text
        Rows: 1
        Columns: Text Length
        txt = 2013/07/30 21:00:00.00, Record No. 7, SN013B0000000000000000000000000000
        :param ens: Ensemble data.
        :return: Byte array of the data in MATLAB format.
        """
        txt = ens.EnsembleData.datetime_str() + ", "
        txt += "Record No. " + str(self.RecordCount) + ", "
        txt += "SN" + ens.EnsembleData.SerialNumber

        ba = bytearray()
        ba.extend(struct.pack('i', 11))         # Indicate float string
        ba.extend(struct.pack('i', 1))          # Rows - 1 per record
        ba.extend(struct.pack("i", len(txt)))   # Columns - Length of the txt
        ba.extend(struct.pack("i", 0))          # Imaginary, if 1, then the matrix has an imaginary part
        ba.extend(struct.pack("i", 4))          # Name Length

        for code in map(ord, 'txt'):           # Name
            ba.extend([code])
        ba.extend(bytearray(1))

        for code in map(ord, txt):              # Txt Value
            ba.extend(struct.pack('f', float(code)))

        return ba

    def process_lat(self, ens):
        """
        The latitude location where the burst was collected.

        Data Type: Double
        Rows: 1
        Columns: 1
        lat = 32.865
        :param ens: Ensemble data.
        """
        lat = 0.0
        if ens.IsWavesInfo:
            lat = ens.WavesInfo.Lat
        else:
            lat = self.Lat

        ba = bytearray()
        ba.extend(struct.pack('i', 0))      # Indicate double
        ba.extend(struct.pack('i', 1))      # Rows - 1 per record
        ba.extend(struct.pack("i", 1))      # Columns - 1 per record
        ba.extend(struct.pack("i", 0))      # Imaginary, if 1, then the matrix has an imaginary part
        ba.extend(struct.pack("i", 4))      # Name Length

        for code in map(ord, 'lat'):       # Name
            ba.extend([code])
        ba.extend(bytearray(1))

        ba.extend(struct.pack("d", lat))    # Lat Value

        return ba

    def process_lon(self, ens):
        """
        The longitude location where the burst was collected.

        Data Type: Double
        Rows: 1
        Columns: 1
        lon = -117.26
        :param ens: Ensemble data.
        """
        lon = 0.0
        if ens.IsWavesInfo:
            lon = ens.WavesInfo.Lat
        else:
            lon = self.Lon

        ba = bytearray()
        ba.extend(struct.pack('I', 0))      # Indicate double
        ba.extend(struct.pack('I', 1))      # Rows - 1 per record
        ba.extend(struct.pack("I", 1))      # Columns - 1 per record
        ba.extend(struct.pack("I", 0))      # Imaginary
        ba.extend(struct.pack("I", 4))      # Name Length

        for code in map(ord, 'lon'):       # Name
            ba.extend([code])
        ba.extend(bytearray(1))

        ba.extend(struct.pack("d", lon))    # Lon Value

        return ba

    def process_wft(self, ens):
        """
        First sample time of the burst in seconds. The value is in hours of a day. WFT  * 24 =

        Data Type: Double
        Rows: 1
        Columns: 1
        wft = 7.3545e+05
        :param ens: Ensemble data.
        """
        self.firstTime = self.time_stamp_seconds(ens)

        ba = bytearray()
        ba.extend(struct.pack('i', 0))      # Indicate double
        ba.extend(struct.pack('i', 1))      # Rows - 1 per record
        ba.extend(struct.pack("i", 1))      # Columns - 1 per record
        ba.extend(struct.pack("i", 0))      # Imaginary
        ba.extend(struct.pack("i", 4))      # Name Length

        for code in map(ord, 'wft'):       # Name
            ba.extend([code])
        ba.extend(bytearray(1))

        ba.extend(struct.pack("d", self.firstTime))    # WFT Value

        return ba

    def process_wdt(self, ens_buff):
        """
        Time between each sample.  The time is in seconds.

        Data Type: Double
        Rows: 1
        Columns: 1
        wft = 0.5000
        :param ens: Ensemble data.
        """
        # Find the first and second time
        # Make sure that if we are interleaved,
        # that we take the next sample that is like the original subsystem config

        ba = bytearray()

        if len(ens_buff) >= 4:
            # Get the first 4 Beam sample
            if ens_buff[0].IsEnsembleData:
                subcfg = ens_buff[0].EnsembleData.SubsystemConfig
                subcode =ens_buff[0].EnsembleData.SysFirmwareSubsystemCode
                self.firstTime = self.time_stamp_seconds(ens_buff[0])

                # Check if both subsystems match
                # If they do match, then there is no interleaving and we can take the next sample
                # If there is interleaving, then we have to wait for the next sample, because the first 2 go together
                if ens_buff[1].EnsembleData.SubsystemConfig == subcfg and ens_buff[1].EnsembleData.SysFirmwareSubsystemCode == subcode:
                    self.secondTime = WaveForceCodec.time_stamp_seconds(ens_buff[1])
                else:
                    self.secondTime = WaveForceCodec.time_stamp_seconds(ens_buff[2])

            wdt = self.secondTime - self.firstTime

            ba.extend(struct.pack('i', 0))      # Indicate double
            ba.extend(struct.pack('i', 1))      # Rows - 1 per record
            ba.extend(struct.pack("i", 1))      # Columns - 1 per record
            ba.extend(struct.pack("i", 0))      # Imaginary
            ba.extend(struct.pack("i", 4))      # Name Length

            for code in map(ord, 'wdt'):       # Name
                ba.extend([code])
            ba.extend(bytearray(1))

            ba.extend(struct.pack("d", wdt))    # WDT Value

        return ba

    def process_whv(self, whv, num_selected_bins):
        """
        Wave Cell Height for each selected bin.

        Data Type: Float
        Rows: Number of Selected Bin values
        Columns: 1
        whv = 7.3, 7.2, 7.5
        :param whv: Wave Cell Height data in byte array for each selected bin.
        :param num_selected_bins: Number of selected bins.
        :return:
        """

        ba = bytearray()
        ba.extend(struct.pack('i', 10))                 # Indicate double
        ba.extend(struct.pack('i', 1))                  # Rows - 1 per burst
        ba.extend(struct.pack("i", num_selected_bins))  # Columns - 1 each selected bin
        ba.extend(struct.pack("i", 0))                  # Imaginary
        ba.extend(struct.pack("i", 4))                  # Name Length

        for code in map(ord, 'whv'):                    # Name
            ba.extend([code])
        ba.extend(bytearray(1))

        ba.extend(whv)                                  # WHV Values

        return ba

    def process_whp(self, whp):
        """
        Wave Pressure Sensor Height for each burst.

        Data Type: Float
        Rows: Number of Selected Bin values
        Columns: 1
        whp = 7.3
        :param whp: Wave Pressure Sensor Height data in byte array for each selected bin.
        :return:
        """

        ba = bytearray()
        ba.extend(struct.pack('i', 10))                 # Indicate double
        ba.extend(struct.pack('i', 1))                  # Rows - 1 per burst
        ba.extend(struct.pack("i", 1))                  # Columns - 1 per burst
        ba.extend(struct.pack("i", 0))                  # Imaginary
        ba.extend(struct.pack("i", 4))                  # Name Length

        for code in map(ord, 'whp'):                    # Name
            ba.extend([code])
        ba.extend(bytearray(1))

        ba.extend(whp)                                  # WHP Values

        return ba

    def process_wus(self, wus, num_4beam_ens, num_selected_bins):
        """
        East velocity data for each selected bin.

        Data Type: Float
        Rows: Number of 4 Beam values
        Columns: Number of selected bins
        wus = 7.3, 7.2, 7.5
              7.2, 4.1, 6.7
        :param wus: East velocity data in byte array for each selected bin.
        :param num_4beam_ens: Number of 4 Beam ensembles.
        :param num_selected_bins: Number of selected bins.
        :return:
        """

        ba = bytearray()
        ba.extend(struct.pack('i', 10))                 # Indicate double
        ba.extend(struct.pack('i', num_4beam_ens))      # Rows - Number of 4 Beam ensembles
        ba.extend(struct.pack("i", num_selected_bins))  # Columns - Number of selected bins
        ba.extend(struct.pack("i", 0))                  # Imaginary
        ba.extend(struct.pack("i", 4))                  # Name Length

        for code in map(ord, 'wus'):                    # Name
            ba.extend([code])
        ba.extend(bytearray(1))

        ba.extend(wus)                                  # WUS Values

        return ba

    def process_wvs(self, wvs, num_4beam_ens, num_selected_bins):
        """
        North velocity data for each selected bin.

        Data Type: Float
        Rows: Number of 4 Beam values
        Columns: Number of selected bins
        wvs = 7.3, 7.2, 7.5
              7.2, 4.1, 6.7
        :param wvs: North velocity data in byte array for each selected bin.
        :param num_4beam_ens: Number of 4 Beam ensembles.
        :param num_selected_bins: Number of selected bins.
        :return:
        """

        ba = bytearray()
        ba.extend(struct.pack('i', 10))                 # Indicate double
        ba.extend(struct.pack('i', num_4beam_ens))      # Rows - Number of 4 Beam ensembles
        ba.extend(struct.pack("i", num_selected_bins))  # Columns - Number of selected bins
        ba.extend(struct.pack("i", 0))                  # Imaginary
        ba.extend(struct.pack("i", 4))                  # Name Length

        for code in map(ord, 'wvs'):                    # Name
            ba.extend([code])
        ba.extend(bytearray(1))

        ba.extend(wvs)                                  # WVS Values

        return ba

    def process_wzs(self, wzs, num_4beam_ens, num_selected_bins):
        """
        Vertical velocity data for each selected bin.

        Data Type: Float
        Rows: Number of 4 Beam values
        Columns: Number of selected bins
        wzs = 7.3, 7.2, 7.5
              7.2, 4.1, 6.7
        :param wzs: North velocity data in byte array for each selected bin.
        :param num_4beam_ens: Number of 4 Beam ensembles.
        :param num_selected_bins: Number of selected bins.
        :return:
        """

        ba = bytearray()
        ba.extend(struct.pack('i', 10))                 # Indicate double
        ba.extend(struct.pack('i', num_4beam_ens))      # Rows - Number of 4 Beam ensembles
        ba.extend(struct.pack("i", num_selected_bins))  # Columns - Number of selected bins
        ba.extend(struct.pack("i", 0))                  # Imaginary
        ba.extend(struct.pack("i", 4))                  # Name Length

        for code in map(ord, 'wzs'):                    # Name
            ba.extend([code])
        ba.extend(bytearray(1))

        ba.extend(wzs)                                  # WZS Values

        return ba

    def process_wb0(self, wb0, num_4beam_ens, num_selected_bins):
        """
        Beam 0 Beam velocity data for each selected bin.

        Data Type: Float
        Rows: Number of 4 Beam values
        Columns: Number of selected bins
        wb0 = 7.3, 7.2, 7.5
              7.2, 4.1, 6.7
        :param wb0: Beam 0 Beam velocity data in byte array for each selected bin.
        :param num_4beam_ens: Number of 4 Beam ensembles.
        :param num_selected_bins: Number of selected bins.
        :return:
        """

        ba = bytearray()
        ba.extend(struct.pack('i', 10))                 # Indicate double
        ba.extend(struct.pack('i', num_4beam_ens))      # Rows - Number of 4 Beam ensembles
        ba.extend(struct.pack("i", num_selected_bins))  # Columns - Number of selected bins
        ba.extend(struct.pack("i", 0))                  # Imaginary
        ba.extend(struct.pack("i", 4))                  # Name Length

        for code in map(ord, 'wb0'):                    # Name
            ba.extend([code])
        ba.extend(bytearray(1))

        ba.extend(wb0)                                  # WB0 Values

        return ba

    def process_wb1(self, wb1, num_4beam_ens, num_selected_bins):
        """
        Beam 1 Beam velocity data for each selected bin.

        Data Type: Float
        Rows: Number of 4 Beam values
        Columns: Number of selected bins
        wb1 = 7.3, 7.2, 7.5
              7.2, 4.1, 6.7
        :param wb1: Beam 1 Beam velocity data in byte array for each selected bin.
        :param num_4beam_ens: Number of 4 Beam ensembles.
        :param num_selected_bins: Number of selected bins.
        :return:
        """

        ba = bytearray()
        ba.extend(struct.pack('i', 10))                 # Indicate double
        ba.extend(struct.pack('i', num_4beam_ens))      # Rows - Number of 4 Beam ensembles
        ba.extend(struct.pack("i", num_selected_bins))  # Columns - Number of selected bins
        ba.extend(struct.pack("i", 0))                  # Imaginary
        ba.extend(struct.pack("i", 4))                  # Name Length

        for code in map(ord, 'wb1'):                    # Name
            ba.extend([code])
        ba.extend(bytearray(1))

        ba.extend(wb1)                                  # WB1 Values

        return ba

    def process_wb2(self, wb2, num_4beam_ens, num_selected_bins):
        """
        Beam 2 Beam velocity data for each selected bin.

        Data Type: Float
        Rows: Number of 4 Beam values
        Columns: Number of selected bins
        wb2 = 7.3, 7.2, 7.5
              7.2, 4.1, 6.7
        :param wb2: Beam 2 Beam velocity data in byte array for each selected bin.
        :param num_4beam_ens: Number of 4 Beam ensembles.
        :param num_selected_bins: Number of selected bins.
        :return:
        """

        ba = bytearray()
        ba.extend(struct.pack('i', 10))                 # Indicate double
        ba.extend(struct.pack('i', num_4beam_ens))      # Rows - Number of 4 Beam ensembles
        ba.extend(struct.pack("i", num_selected_bins))  # Columns - Number of selected bins
        ba.extend(struct.pack("i", 0))                  # Imaginary
        ba.extend(struct.pack("i", 4))                  # Name Length

        for code in map(ord, 'wb2'):                    # Name
            ba.extend([code])
        ba.extend(bytearray(1))

        ba.extend(wb2)                                  # WB2 Values

        return ba

    def process_wb3(self, wb3, num_4beam_ens, num_selected_bins):
        """
        Beam 3 Beam velocity data for each selected bin.

        Data Type: Float
        Rows: Number of 4 Beam values
        Columns: Number of selected bins
        wb3 = 7.3, 7.2, 7.5
              7.2, 4.1, 6.7
        :param wb3: Beam 3 Beam velocity data in byte array for each selected bin.
        :param num_4beam_ens: Number of 4 Beam ensembles.
        :param num_selected_bins: Number of selected bins.
        :return:
        """

        ba = bytearray()
        ba.extend(struct.pack('i', 10))                 # Indicate double
        ba.extend(struct.pack('i', num_4beam_ens))      # Rows - Number of 4 Beam ensembles
        ba.extend(struct.pack("i", num_selected_bins))  # Columns - Number of selected bins
        ba.extend(struct.pack("i", 0))                  # Imaginary
        ba.extend(struct.pack("i", 4))                  # Name Length

        for code in map(ord, 'wb3'):                    # Name
            ba.extend([code])
        ba.extend(bytearray(1))

        ba.extend(wb3)                                  # WB3 Values

        return ba

    def process_wps(self, wps, num_4beam_ens):
        """
        Pressure data.

        Data Type: Float
        Rows: Number of 4 Beam values
        Columns: 1
        WPS = 7.3, 7.2, 7.5
        :param wps: Pressure data in byte array.
        :param num_4beam_ens: Number of 4 beam ensembles.
        :return:
        """

        ba = bytearray()
        ba.extend(struct.pack('i', 10))                 # Indicate double
        ba.extend(struct.pack('i', num_4beam_ens))      # Rows - Number of 4 Beam ensembles
        ba.extend(struct.pack("i", 1))                  # Columns - 1
        ba.extend(struct.pack("i", 0))                  # Imaginary
        ba.extend(struct.pack("i", 4))                  # Name Length

        for code in map(ord, 'wps'):                    # Name
            ba.extend([code])
        ba.extend(bytearray(1))

        ba.extend(wps)                                  # WPS Values

        return ba

    def process_whg(self, whg, num_4beam_ens):
        """
        Heading data.

        Data Type: Float
        Rows: Number of 4 Beam values
        Columns: 1
        WHG = 7.3, 7.2, 7.5
        :param whg: Heading data in byte array.
        :param num_4beam_ens: Number of 4 beam ensembles.
        :return:
        """

        ba = bytearray()
        ba.extend(struct.pack('i', 10))                 # Indicate double
        ba.extend(struct.pack('i', num_4beam_ens))      # Rows - Number of 4 Beam ensembles
        ba.extend(struct.pack("i", 1))                  # Columns - 1
        ba.extend(struct.pack("i", 0))                  # Imaginary
        ba.extend(struct.pack("i", 4))                  # Name Length

        for code in map(ord, 'whg'):                    # Name
            ba.extend([code])
        ba.extend(bytearray(1))

        ba.extend(whg)                                  # WHG Values

        return ba

    def process_wph(self, wph, num_4beam_ens):
        """
        Pitch data.

        Data Type: Float
        Rows: Number of 4 Beam values
        Columns: 1
        WPH = 7.3, 7.2, 7.5
        :param wph: Heading data in byte array.
        :param num_4beam_ens: Number of 4 beam ensembles.
        :return:
        """

        ba = bytearray()
        ba.extend(struct.pack('i', 10))                 # Indicate double
        ba.extend(struct.pack('i', num_4beam_ens))      # Rows - Number of 4 Beam ensembles
        ba.extend(struct.pack("i", 1))                  # Columns - 1
        ba.extend(struct.pack("i", 0))                  # Imaginary
        ba.extend(struct.pack("i", 4))                  # Name Length

        for code in map(ord, 'wph'):                    # Name
            ba.extend([code])
        ba.extend(bytearray(1))

        ba.extend(wph)                                  # WPH Values

        return ba

    def process_wrl(self, wrl, num_4beam_ens):
        """
        Roll data.

        Data Type: Float
        Rows: Number of 4 Beam values
        Columns: 1
        WRL = 7.3, 7.2, 7.5
        :param wrl: Roll data in byte array.
        :param num_4beam_ens: Number of 4 beam ensembles.
        :return:
        """

        ba = bytearray()
        ba.extend(struct.pack('i', 10))                 # Indicate double
        ba.extend(struct.pack('i', num_4beam_ens))      # Rows - Number of 4 Beam ensembles
        ba.extend(struct.pack("i", 1))                  # Columns - 1
        ba.extend(struct.pack("i", 0))                  # Imaginary
        ba.extend(struct.pack("i", 4))                  # Name Length

        for code in map(ord, 'wrl'):                    # Name
            ba.extend([code])
        ba.extend(bytearray(1))

        ba.extend(wrl)                                  # WRL Values

        return ba

    def process_wts(self, wts, num_4beam_ens):
        """
        Water Temp data.

        Data Type: Float
        Rows: Number of 4 Beam values
        Columns: 1
        WTS = 7.3, 7.2, 7.5
        :param wts: Water Temp data in byte array.
        :param num_4beam_ens: Number of 4 beam ensembles.
        :return:
        """

        ba = bytearray()
        ba.extend(struct.pack('i', 10))                 # Indicate double
        ba.extend(struct.pack('i', num_4beam_ens))      # Rows - Number of 4 Beam ensembles
        ba.extend(struct.pack("i", 1))                  # Columns - 1
        ba.extend(struct.pack("i", 0))                  # Imaginary
        ba.extend(struct.pack("i", 4))                  # Name Length

        for code in map(ord, 'wts'):                    # Name
            ba.extend([code])
        ba.extend(bytearray(1))

        ba.extend(wts)                                  # WTS Values

        return ba

    def process_whs(self, whs, num_4beam_ens):
        """
        Wave height source data.
        Average of RT, or a single RT value, or pressure.

        Data Type: Float
        Rows: Number of 4 Beam values
        Columns: 1
        WHS = 7.3, 7.2, 7.5
        :param whs: Wave height source data in byte array.
        :param num_4beam_ens: Number of 4 beam ensembles.
        :return:
        """

        ba = bytearray()
        ba.extend(struct.pack('i', 10))                 # Indicate double
        ba.extend(struct.pack('i', num_4beam_ens))      # Rows - Number of 4 Beam ensembles
        ba.extend(struct.pack("i", 1))                  # Columns - 1
        ba.extend(struct.pack("i", 0))                  # Imaginary
        ba.extend(struct.pack("i", 4))                  # Name Length

        for code in map(ord, 'whs'):                    # Name
            ba.extend([code])
        ba.extend(bytearray(1))

        ba.extend(whs)                                  # WHS Values

        return ba

    def process_wah(self, wah, num_4beam_ens):
        """
        Average height data.
        Average of all Range Tracking.

        Data Type: Float
        Rows: Number of 4 Beam values
        Columns: 1
        WAH = 7.3, 7.2, 7.5
        :param wah: Average Range Tracking data in byte array.
        :param num_4beam_ens: Number of 4 beam ensembles.
        :return:
        """

        ba = bytearray()
        ba.extend(struct.pack('i', 10))                 # Indicate double
        ba.extend(struct.pack('i', num_4beam_ens))      # Rows - Number of 4 Beam ensembles
        ba.extend(struct.pack("i", 1))                  # Columns - 1
        ba.extend(struct.pack("i", 0))                  # Imaginary
        ba.extend(struct.pack("i", 4))                  # Name Length

        for code in map(ord, 'wah'):                    # Name
            ba.extend([code])
        ba.extend(bytearray(1))

        ba.extend(wah)                                  # WAH Values

        return ba

    def process_wr0(self, wr0, num_4beam_ens):
        """
        Range Tracking Beam 0 data.

        Data Type: Float
        Rows: Number of 4 Beam values
        Columns: 1
        WR0 = 7.3, 7.2, 7.5
        :param wr0: Range Tracking Beam 0 data in byte array.
        :param num_4beam_ens: Number of 4 beam ensembles.
        :return:
        """

        ba = bytearray()
        ba.extend(struct.pack('i', 10))                 # Indicate double
        ba.extend(struct.pack('i', num_4beam_ens))      # Rows - Number of 4 Beam ensembles
        ba.extend(struct.pack("i", 1))                  # Columns - 1
        ba.extend(struct.pack("i", 0))                  # Imaginary
        ba.extend(struct.pack("i", 4))                  # Name Length

        for code in map(ord, 'wr0'):                    # Name
            ba.extend([code])
        ba.extend(bytearray(1))

        ba.extend(wr0)                                  # WR0 Values

        return ba

    def process_wr1(self, wr1, num_4beam_ens):
        """
        Range Tracking Beam 1 data.

        Data Type: Float
        Rows: Number of 4 Beam values
        Columns: 1
        WR1 = 7.3, 7.2, 7.5
        :param wr1: Range Tracking Beam 1 data in byte array.
        :param num_4beam_ens: Number of 4 beam ensembles.
        :return:
        """

        ba = bytearray()
        ba.extend(struct.pack('i', 10))                 # Indicate double
        ba.extend(struct.pack('i', num_4beam_ens))      # Rows - Number of 4 Beam ensembles
        ba.extend(struct.pack("i", 1))                  # Columns - 1
        ba.extend(struct.pack("i", 0))                  # Imaginary
        ba.extend(struct.pack("i", 4))                  # Name Length

        for code in map(ord, 'wr1'):                    # Name
            ba.extend([code])
        ba.extend(bytearray(1))

        ba.extend(wr1)                                  # WR1 Values

        return ba

    def process_wr2(self, wr2, num_4beam_ens):
        """
        Range Tracking Beam 2 data.

        Data Type: Float
        Rows: Number of 4 Beam values
        Columns: 1
        WR2 = 7.3, 7.2, 7.5
        :param wr2: Range Tracking Beam 2 data in byte array.
        :param num_4beam_ens: Number of 4 beam ensembles.
        :return:
        """

        ba = bytearray()
        ba.extend(struct.pack('i', 10))                 # Indicate double
        ba.extend(struct.pack('i', num_4beam_ens))      # Rows - Number of 4 Beam ensembles
        ba.extend(struct.pack("i", 1))                  # Columns - 1
        ba.extend(struct.pack("i", 0))                  # Imaginary
        ba.extend(struct.pack("i", 4))                  # Name Length

        for code in map(ord, 'wr2'):                    # Name
            ba.extend([code])
        ba.extend(bytearray(1))

        ba.extend(wr2)                                  # WR2 Values

        return ba

    def process_wr3(self, wr3, num_4beam_ens):
        """
        Range Tracking Beam 3 data.

        Data Type: Float
        Rows: Number of 4 Beam values
        Columns: 1
        WR0 = 7.3, 7.2, 7.5
        :param wr3: Range Tracking Beam 3 data in byte array.
        :param num_4beam_ens: Number of 4 beam ensembles.
        :return:
        """

        ba = bytearray()
        ba.extend(struct.pack('i', 10))                 # Indicate double
        ba.extend(struct.pack('i', num_4beam_ens))      # Rows - Number of 4 Beam ensembles
        ba.extend(struct.pack("i", 1))                  # Columns - 1
        ba.extend(struct.pack("i", 0))                  # Imaginary
        ba.extend(struct.pack("i", 4))                  # Name Length

        for code in map(ord, 'wr3'):                    # Name
            ba.extend([code])
        ba.extend(bytearray(1))

        ba.extend(wr3)                                  # WR3 Values

        return ba

    def process_wz0(self, wz0, num_vert_ens, num_selected_bins):
        """
        Beam 0 Vertical Beam velocity data for each selected bin.

        Data Type: Float
        Rows: Number of Vertical values
        Columns: Number of selected bins
        WZ0 = 7.3, 7.2, 7.5
        :param wz0: Beam 0 Vertical Beam velocity data in byte array for each selected bin.
        :param num_vert_ens: Number of 4 Beam ensembles.
        :param num_selected_bins: Number of selected bins.
        :return:
        """

        ba = bytearray()
        ba.extend(struct.pack('i', 10))                 # Indicate double
        ba.extend(struct.pack('i', num_vert_ens))       # Rows - Number of Vertical ensembles
        ba.extend(struct.pack("i", num_selected_bins))  # Columns - Number of selected bins
        ba.extend(struct.pack("i", 0))                  # Imaginary
        ba.extend(struct.pack("i", 4))                  # Name Length

        for code in map(ord, 'wz0'):                    # Name
            ba.extend([code])
        ba.extend(bytearray(1))

        ba.extend(wz0)                                  # WZ0 Values

        return ba

    def process_wzp(self, wzp, num_vert_ens):
        """
        Vertical Beam Pressure data.

        Data Type: Float
        Rows: Number of Vertical values
        Columns: 1
        WZP = 7.3, 7.2, 7.5
        :param wzp: Vertical Beam pressure data in byte array.
        :param num_vert_ens: Number of vertical ensembles.
        :return:
        """

        ba = bytearray()
        ba.extend(struct.pack('i', 10))                 # Indicate double
        ba.extend(struct.pack('i', num_vert_ens))       # Rows - Number of Vertical ensembles
        ba.extend(struct.pack("i", 1))                  # Columns - 1
        ba.extend(struct.pack("i", 0))                  # Imaginary
        ba.extend(struct.pack("i", 4))                  # Name Length

        for code in map(ord, 'wzp'):                    # Name
            ba.extend([code])
        ba.extend(bytearray(1))

        ba.extend(wzp)                                  # WZP Values

        return ba

    def process_wzr(self, wzr, num_vert_ens):
        """
        Range Tracking Vertical Beam data.

        Data Type: Float
        Rows: Number of Vertical Beam values
        Columns: 1
        WZR = 7.3, 7.2, 7.5
        :param wzr: Range Tracking Vertical Beam data in byte array.
        :param num_vert_ens: Number of Vertical beam ensembles.
        :return:
        """

        ba = bytearray()
        ba.extend(struct.pack('i', 10))                 # Indicate double
        ba.extend(struct.pack('i', num_vert_ens))      # Rows - Number of Vertical ensembles
        ba.extend(struct.pack("i", 1))                  # Columns - 1
        ba.extend(struct.pack("i", 0))                  # Imaginary
        ba.extend(struct.pack("i", 4))                  # Name Length

        for code in map(ord, 'wzr'):                    # Name
            ba.extend([code])
        ba.extend(bytearray(1))

        ba.extend(wzr)                                  # WZR Values

        return ba

    @staticmethod
    def time_stamp_seconds(ens):
        """
        Calcualte the timestamp.  This is the number of seconds for the given
        date and time.
        :param ens: Ensemble to get the timestamp.
        :return: Timestamp in seconds.
        """

        ts = 0.0

        if ens.IsEnsembleData:
            year = ens.EnsembleData.Year
            month = ens.EnsembleData.Month
            day = ens.EnsembleData.Day
            hour = ens.EnsembleData.Hour
            minute = ens.EnsembleData.Minute
            second = ens.EnsembleData.Second
            hsec = ens.EnsembleData.HSec
            jdn = WaveForceCodec.julian_day_number(year, month, day)

            ts = (24.0 * 3600.0 * jdn) + (3600.0 * hour) + (60.0 * minute) + second + (hsec / 100.0)

        return ts

    @staticmethod
    def julian_day_number(year, month, day):
        """
        Count the number of calendar days there are for the given
        year, month and day.
        :param year: Years.
        :param month: Months.
        :param day: Days.
        :return: Number of days.
        """
        a = (14 - month) / 12
        y = year + 4800 - a
        m = month - 12 * a - 3

        return day + (153 * m + 2) / 5 + (365 * y) + y / 4 - y / 100 + y / 400 - 32045
