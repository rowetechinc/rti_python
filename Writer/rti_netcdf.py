from rti_python.Ensemble.Ensemble import Ensemble
import logging
from netCDF4 import Dataset
from typing import List, Set, Dict, Tuple, Optional

"""
Convert full profile Rowe Technologies Inc. ADCP data ensembles currents to a netCDF4 file.

Reference:
    Code referenced from https://github.com/mmartini-usgs/ADCPy
"""


class RtiNetcdf:

    def __init__(self, cdf_file_path: str):
        self.cdf_file_path = cdf_file_path
        self.ensemble_count = 0
        self.netcdf_index = 0

        # Create the CDF file
        self.cdf_file = self.setup_netcdf_file(self.cdf_file_path)

    def setup_netcdf_file(self, fname: str, ens: Ensemble, gens: Tuple, serial_number: str, time_type: str, delta_t: str):
        """
        create the netcdf output file, define dimensions and variables
        :param str fname: path and name of netcdf file
        :param dict ens: Ensemble data from the first ensemble to be read
        :param tuple gens: start and end ensemble indices
        :param str serial_number: instrument serial number
        :param str time_type: indicate if "CF", "CF_with_EPIC", "EPIC_with_CF" or "EPIC" timebase for "time"
        :param str delta_t: time between ensembles
        :return: netcdf file object, string describing the time units for CF time
        """
        # note that
        # f4 = 4 byte, 32 bit float
        # maxfloat = 3.402823*10**38;
        # where the variable is based ona  single dimension, usually time, it is still expressed as a tuple ("time") and
        # needs to be kept that way, even though pylint complains
        intfill = -32768
        floatfill = 1E35

        # is it possible for delta_t to be none or an int.  Deal with that here
        if delta_t is None:
            delta_t = "none"

        if isinstance(delta_t, int):
            delta_t = str(delta_t)

        nens = gens[1] - gens[0] - 1
        print('creating netCDF file %s with %d records' % (fname, nens))

        cdf = Dataset(fname, "w", clobber=True, format="NETCDF4")

        # dimensions, in EPIC order
        cdf.createDimension('time', nens)
        cdf.createDimension('depth', ens.EnsembleData.NumBins)
        cdf.createDimension('lat', 1)
        cdf.createDimension('lon', 1)

        # write global attributes
        cdf.history = "translated to netCDF by rti_netcdf.py"
        cdf.sensor_type = "Rowe"
        cdf.serial_number = serial_number
        cdf.DELTA_T = delta_t
        cdf.sample_rate = ens_data['FLeader']['Time_Between_Ping Groups']

        self.write_dict_to_cdf_attributes(cdf, ens_data['FLeader'], "TRDI_")

        varobj = cdf.createVariable('Rec',              # Name
                                    'u4',               # Unsigned 32bit integer
                                    'time',             # Time Dimension created above
                                    fill_value=intfill)
        varobj.units = "count"
        varobj.long_name = "Ensemble Number"
        # the ensemble number is a two byte LSB and a one byte MSB (for the rollover)
        # varobj.valid_range = [0, 2**23]

        # it's not yet clear which way to go with this.  python tools like xarray
        # and panoply demand that time be a CF defined time.
        # USGS CMG MATLAB tools need time and time2
        # TODO - CF_time can come out as YYYY-M-D for dates with single digit months and days, check to see if this is ISO
        # and fix if it is not.  This is a better way:
        # d = datetime.datetime(2010, 7, 4, 12, 15, 58)
        # '{:%Y-%m-%d %H:%M:%S}'.format(d)
        if time_type == 'EPIC_with_CF':
            # we include time and time2 for EPIC compliance
            varobj = cdf.createVariable('time', 'u4', ('time',))
            varobj.units = "True Julian Day"
            varobj.epic_code = 624
            varobj.datum = "Time (UTC) in True Julian Days: 2440000 = 0000 h on May 23, 1968"
            varobj.NOTE = "Decimal Julian day [days] = time [days] + ( time2 [msec] / 86400000 [msec/day] )"
            varobj = cdf.createVariable('time2', 'u4', ('time',))
            varobj.units = "msec since 0:00 GMT"
            varobj.epic_code = 624
            varobj.datum = "Time (UTC) in True Julian Days: 2440000 = 0000 h on May 23, 1968"
            varobj.NOTE = "Decimal Julian day [days] = time [days] + ( time2 [msec] / 86400000 [msec/day] )"
            cf_units = ""
            # we include cf_time for cf compliance and use by python packages like xarray
            # if f8, 64 bit is not used, time is clipped
            # for ADCP fast sampled, single ping data, need millisecond resolution
            varobj = cdf.createVariable('cf_time', 'f8', 'time')
            # for cf convention, always assume UTC for now, and use the UNIX Epoch as the reference
            #varobj.units = "seconds since %d-%d-%d %d:%d:%f 0:00" % (ens_data['VLeader']['Year'],
            #                                                         ens_data['VLeader']['Month'],
            #                                                         ens_data['VLeader']['Day'],
            #                                                         ens_data['VLeader']['Hour'],
            #                                                         ens_data['VLeader']['Minute'],
            #                                                         ens_data['VLeader']['Second'] +
            #                                                         ens_data['VLeader']['Hundredths'] / 100)

            varobj.units = "seconds since %d-%d-%d %d:%d:%f 0:00" % (ens.EnsembleData.Year,
                                                                     ens.EnsembleData.Month,
                                                                     ens.EnsembleData.Day,
                                                                     ens.EnsembleData.Hour,
                                                                     ens.EnsembleData.Minute,
                                                                     ens.EnsembleData.Second +
                                                                     ens.EnsembleData.HSec / 100)

            varobj.standard_name = "time"
            varobj.axis = "T"
        elif time_type == "CF_with_EPIC":
            # cf_time for cf compliance and use by python packages like xarray
            # if f8, 64 bit is not used, time is clipped
            # for ADCP fast sampled, single ping data, need millisecond resolution
            varobj = cdf.createVariable('time', 'f8', ('time',))
            # for cf convention, always assume UTC for now, and use the UNIX Epoch as the reference
            #varobj.units = "seconds since %d-%d-%d %d:%d:%f 0:00" % (ens_data['VLeader']['Year'],
            #                                                         ens_data['VLeader']['Month'],
            #                                                         ens_data['VLeader']['Day'],
            #                                                         ens_data['VLeader']['Hour'],
            #                                                         ens_data['VLeader']['Minute'],
            #                                                         ens_data['VLeader']['Second'] +
            #                                                         ens_data['VLeader']['Hundredths'] / 100)

            varobj.units = "seconds since %d-%d-%d %d:%d:%f 0:00" % (ens.EnsembleData.Year,
                                                                     ens.EnsembleData.Month,
                                                                     ens.EnsembleData.Day,
                                                                     ens.EnsembleData.Hour,
                                                                     ens.EnsembleData.Minute,
                                                                     ens.EnsembleData.Second +
                                                                     ens.EnsembleData.HSec / 100)

            #cf_units = "seconds since %d-%d-%d %d:%d:%f 0:00" % (
            #ens_data['VLeader']['Year'], ens_data['VLeader']['Month'],
            #ens_data['VLeader']['Day'], ens_data['VLeader']['Hour'],
            #ens_data['VLeader']['Minute'],
            #ens_data['VLeader']['Second']
            #+ ens_data['VLeader']['Hundredths'] / 100)

            cf_units = "seconds since %d-%d-%d %d:%d:%f 0:00" % (
                ens.EnsembleData.Year,
                ens.EnsembleData.Month,
                ens.EnsembleData.Day,
                ens.EnsembleData.Hour,
                ens.EnsembleData.Minute,
                ens.EnsembleData.Second + ens.EnsembleData.HSec / 100)

            varobj.standard_name = "time"
            varobj.axis = "T"
            varobj.type = "UNEVEN"
            # we include time and time2 for EPIC compliance
            # this statement resulted in a fill value of -1??
            # varobj = cdf.createVariable('EPIC_time','u4',('time',))
            varobj = cdf.createVariable('EPIC_time', 'u4', ('time',), fill_value=False)
            varobj.units = "True Julian Day"
            varobj.epic_code = 624
            varobj.datum = "Time (UTC) in True Julian Days: 2440000 = 0000 h on May 23, 1968"
            varobj.NOTE = "Decimal Julian day [days] = time [days] + ( time2 [msec] / 86400000 [msec/day] )"
            # this statement resulted in a fill value of -1??
            # varobj = cdf.createVariable('EPIC_time2','u4',('time',))
            varobj = cdf.createVariable('EPIC_time2', 'u4', ('time',), fill_value=False)
            varobj.units = "msec since 0:00 GMT"
            varobj.epic_code = 624
            varobj.datum = "Time (UTC) in True Julian Days: 2440000 = 0000 h on May 23, 1968"
            varobj.NOTE = "Decimal Julian day [days] = time [days] + ( time2 [msec] / 86400000 [msec/day] )"
        elif time_type == "EPIC":
            varobj = cdf.createVariable('time', 'u4', ('time',))
            varobj.units = "True Julian Day"
            varobj.epic_code = 624
            varobj.datum = "Time (UTC) in True Julian Days: 2440000 = 0000 h on May 23, 1968"
            varobj.NOTE = "Decimal Julian day [days] = time [days] + ( time2 [msec] / 86400000 [msec/day] )"
            varobj = cdf.createVariable('time2', 'u4', ('time',))
            varobj.units = "msec since 0:00 GMT"
            varobj.epic_code = 624
            varobj.datum = "Time (UTC) in True Julian Days: 2440000 = 0000 h on May 23, 1968"
            varobj.NOTE = "Decimal Julian day [days] = time [days] + ( time2 [msec] / 86400000 [msec/day] )"
            cf_units = ""
        else:  # only CF time
            # this is best for use by python packages like xarray
            # if f8, 64 bit is not used, time is clipped
            # for ADCP fast sampled, single ping data, need millisecond resolution
            varobj = cdf.createVariable('time', 'f8', ('time',))
            # for cf convention, always assume UTC for now, and use the UNIX Epoch as the reference
            #varobj.units = "seconds since %d-%d-%d %d:%d:%f 0:00" % (ens_data['VLeader']['Year'],
            #                                                         ens_data['VLeader']['Month'],
            #                                                         ens_data['VLeader']['Day'],
            #                                                         ens_data['VLeader']['Hour'],
            #                                                         ens_data['VLeader']['Minute'],
            #                                                         ens_data['VLeader']['Second'] +
            #                                                         ens_data['VLeader']['Hundredths'] / 100)
            varobj.units = "seconds since %d-%d-%d %d:%d:%f 0:00" % (ens.EnsembleData.Year,
                                                                     ens.EnsembleData.Month,
                                                                     ens.EnsembleData.Day,
                                                                     ens.EnsembleData.Hour,
                                                                     ens.EnsembleData.Minute,
                                                                     ens.EnsembleData.Second + ens.EnsembleData.HSec / 100)


            #cf_units = "seconds since %d-%d-%d %d:%d:%f 0:00" % (
            #ens_data['VLeader']['Year'], ens_data['VLeader']['Month'],
            #ens_data['VLeader']['Day'], ens_data['VLeader']['Hour'],
            #ens_data['VLeader']['Minute'],
            #ens_data['VLeader']['Second']
            #+ ens_data['VLeader']['Hundredths'] / 100)
            cf_units = "seconds since %d-%d-%d %d:%d:%f 0:00" % (
                ens.EnsembleData.Year,
                ens.EnsembleData.Month,
                ens.EnsembleData.Day,
                ens.EnsembleData.Hour,
                ens.EnsembleData.Minute,
                ens.EnsembleData.Second + ens.EnsembleData.HSec / 100)
            varobj.standard_name = "time"
            varobj.axis = "T"
            varobj.type = "UNEVEN"

        varobj = cdf.createVariable('bindist', 'f4', ('depth',), fill_value=floatfill)
        # note name is one of the netcdf4 reserved attributes, use setncattr
        varobj.setncattr('name', "bindist")
        varobj.units = "m"
        varobj.long_name = "bin distance from instrument for slant beams"
        varobj.epic_code = 0
        # varobj.valid_range = [0 0]
        varobj.NOTE = "distance is calculated from center of bin 1 and bin size"
        bindist = []
        #for idx in range(ens_data['FLeader']['Number_of_Cells']):
        #    bindist.append(idx * (ens_data['FLeader']['Depth_Cell_Length_cm'] / 100) + ens_data['FLeader']['Bin_1_distance_cm'] / 100)
        for idx in range(ens.EnsembleData.NumBins):
            bindist.append(idx * (ens.AncillaryData.BinSize) + ens.AncillaryData.FirstBinRange)
        varobj[:] = bindist[:]

        varobj = cdf.createVariable('depth', 'f4', ('depth',))  # no fill for ordinates
        varobj.units = "m"
        varobj.long_name = "distance from transducer, depth placeholder"
        #varobj.center_first_bin_m = ens_data['FLeader']['Bin_1_distance_cm'] / 100
        varobj.center_first_bin_m = ens.AncillaryData.FirstBinRange
        varobj.blanking_distance_m = ens_data['FLeader']['Blank_after_Transmit_cm'] / 100
        #varobj.bin_size_m = ens_data['FLeader']['Depth_Cell_Length_cm'] / 100
        varobj.bin_size_m = ens.AncillaryData.BinSize
        #varobj.bin_count = ens_data['FLeader']['Number_of_Cells']
        varobj.bin_count = ens.EnsembleData.NumBins
        varobj[:] = bindist[:]

        varobj = cdf.createVariable('sv', 'f4', ('time',), fill_value=floatfill)
        varobj.units = "m s-1"
        varobj.long_name = "sound velocity (m s-1)"
        # varobj.valid_range = [1400, 1600]

        for i in range(4):
            varname = "vel%d" % (i + 1)
            varobj = cdf.createVariable(varname, 'f4', ('time', 'depth'), fill_value=floatfill)
            varobj.units = "mm s-1"
            varobj.long_name = "Beam %d velocity (mm s-1)" % (i + 1)
            varobj.epic_code = 1277 + i
            # varobj.valid_range = [-32767, 32767]

        for i in range(4):
            varname = "cor%d" % (i + 1)
            varobj = cdf.createVariable(varname, 'u2', ('time', 'depth'), fill_value=intfill)
            varobj.units = "counts"
            varobj.long_name = "Beam %d correlation" % (i + 1)
            varobj.epic_code = 1285 + i
            # varobj.valid_range = [0, 255]

        for i in range(4):
            varname = "att%d" % (i + 1)
            varobj = cdf.createVariable(varname, 'u2', ('time', 'depth'), fill_value=intfill)
            varobj.units = "counts"
            varobj.epic_code = 1281 + i
            varobj.long_name = "ADCP attenuation of beam %d" % (i + 1)
            # varobj.valid_range = [0, 255]

        if 'GData' in ens_data:
            for i in range(4):
                varname = "PGd%d" % (i + 1)
                varobj = cdf.createVariable(varname, 'u2', ('time', 'depth'), fill_value=intfill)
                varobj.units = "counts"
                varobj.long_name = "Percent Good Beam %d" % (i + 1)
                varobj.epic_code = 1241 + i
                # varobj.valid_range = [0, 100]

        varobj = cdf.createVariable('Hdg', 'f4', ('time',), fill_value=floatfill)
        varobj.units = "hundredths of degrees"
        varobj.long_name = "INST Heading"
        varobj.epic_code = 1215
        varobj.heading_alignment = ens_data['FLeader']['Heading_Alignment_Hundredths_of_Deg']
        varobj.heading_bias = ens_data['FLeader']['Heading_Bias_Hundredths_of_Deg']
        # varobj.valid_range = [0, 36000]
        if ens_data['FLeader']['Heading_Bias_Hundredths_of_Deg'] == 0:
            varobj.NOTE_9 = "no heading bias was applied by EB during deployment or by wavesmon"
        else:
            varobj.NOTE_9 = "a heading bias was applied by EB during deployment or by wavesmon"

        varobj = cdf.createVariable('Ptch', 'f4', ('time',), fill_value=floatfill)
        varobj.units = "hundredths of degrees"
        varobj.long_name = "INST Pitch"
        varobj.epic_code = 1216
        # varobj.valid_range = [-18000, 18000] # physical limit, not sensor limit

        varobj = cdf.createVariable('Roll', 'f4', ('time',), fill_value=floatfill)
        varobj.units = "hundredths of degrees"
        varobj.long_name = "INST Roll"
        varobj.epic_code = 1217
        # varobj.valid_range = [-18000, 18000] # physical limit, not sensor limit

        varobj = cdf.createVariable('HdgSTD', 'f4', ('time',), fill_value=floatfill)
        varobj.units = "degrees"
        varobj.long_name = "Heading Standard Deviation"

        varobj = cdf.createVariable('PtchSTD', 'f4', ('time',), fill_value=floatfill)
        varobj.units = "tenths of degrees"
        varobj.long_name = "Pitch Standard Deviation"

        varobj = cdf.createVariable('RollSTD', 'f4', ('time',), fill_value=floatfill)
        varobj.units = "tenths of degrees"
        varobj.long_name = "Roll Standard Deviation"

        varobj = cdf.createVariable('Tx', 'f4', ('time',), fill_value=floatfill)
        varobj.units = "hundredths of degrees"
        varobj.long_name = "ADCP Transducer Temperature"
        varobj.epic_code = 3017
        # varobj.valid_range = [-500, 4000]

        varobj = cdf.createVariable('S', 'f4', ('time',), fill_value=floatfill)
        varobj.units = "PPT"
        varobj.long_name = "SALINITY (PPT)"
        varobj.epic_code = 40
        # varobj.valid_range = [0, 40]

        varobj = cdf.createVariable('xmitc', 'f4', ('time',), fill_value=floatfill)
        varobj.units = "amps"
        varobj.long_name = "transmit current"

        varobj = cdf.createVariable('xmitv', 'f4', ('time',), fill_value=floatfill)
        varobj.units = "volts"
        varobj.long_name = "transmit voltage"

        varobj = cdf.createVariable('Ambient_Temp', 'i2', ('time',), fill_value=intfill)
        varobj.units = "C"
        varobj.long_name = "Ambient_Temp"

        varobj = cdf.createVariable('Pressure+', 'i2', ('time',), fill_value=intfill)
        varobj.units = "unknown"
        varobj.long_name = "Pressure+"

        varobj = cdf.createVariable('Pressure-', 'i2', ('time',), fill_value=intfill)
        varobj.units = "unknown"
        varobj.long_name = "Pressure-"

        varobj = cdf.createVariable('Attitude_Temp', 'i2', ('time',), fill_value=intfill)
        varobj.units = "C"
        varobj.long_name = "Attitude_Temp"

        for i in range(4):
            varname = "EWD%d" % (i + 1)
            varobj = cdf.createVariable(varname, 'u2', ('time',), fill_value=intfill)
            varobj.units = "binary flag"
            varobj.long_name = "Error Status Word %d" % (i + 1)

        if ens_data['FLeader']['Depth_sensor_available'] == 'Yes':
            varobj = cdf.createVariable('Pressure', 'f4', ('time',), fill_value=floatfill)
            varobj.units = "deca-pascals"
            varobj.long_name = "ADCP Transducer Pressure"
            varobj.epic_code = 4

            varobj = cdf.createVariable('PressVar', 'f4', ('time',), fill_value=floatfill)
            varobj.units = "deca-pascals"
            varobj.long_name = "ADCP Transducer Pressure Variance"

        if 'BTData' in ens_data:
            # write globals attributable to BT setup
            cdf.setncattr('TRDI_BT_pings_per_ensemble', ens_data['BTData']['Pings_per_ensemble'])
            cdf.setncattr('TRDI_BT_reacquire_delay', ens_data['BTData']['delay_before_reacquire'])
            cdf.setncattr('TRDI_BT_min_corr_mag', ens_data['BTData']['Corr_Mag_Min'])
            cdf.setncattr('TRDI_BT_min_eval_mag', ens_data['BTData']['Eval_Amp_Min'])
            cdf.setncattr('TRDI_BT_min_percent_good', ens_data['BTData']['PGd_Minimum'])
            cdf.setncattr('TRDI_BT_mode', ens_data['BTData']['Mode'])
            cdf.setncattr('TRDI_BT_max_err_vel', ens_data['BTData']['Err_Vel_Max'])
            # cdf.setncattr('TRDI_BT_max_tracking_depth',ens_data['BTData'][''])
            # cdf.setncattr('TRDI_BT_shallow_water_gain',ens_data['BTData'][''])

            for i in range(4):
                varname = "BTR%d" % (i + 1)
                varobj = cdf.createVariable(varname, 'u8', ('time',), fill_value=intfill)
                varobj.units = "cm"
                varobj.long_name = "BT Range %d" % (i + 1)

            for i in range(4):
                varnames = ('BTWe', 'BTWu', 'BTWv', 'BTWd')
                longnames = (
                'BT Error Velocity', 'BT Eastward Velocity', 'BT Northward Velocity', 'BT Vertical Velocity')
                if ens_data['FLeader']['Coord_Transform'] == 'EARTH':
                    varobj = cdf.createVariable(varnames[i + 1], 'i2', ('time',), fill_value=intfill)
                    varobj.units = "mm s-1"
                    varobj.long_name = "%s, mm s-1" % longnames[i + 1]
                else:
                    varname = "BTV%d" % (i + 1)
                    varobj = cdf.createVariable(varname, 'i2', ('time',), fill_value=intfill)
                    varobj.units = "mm s-1"
                    varobj.long_name = "BT velocity, mm s-1 %d" % (i + 1)

            for i in range(4):
                varname = "BTc%d" % (i + 1)
                varobj = cdf.createVariable(varname, 'u2', ('time',), fill_value=intfill)
                varobj.units = "counts"
                varobj.long_name = "BT correlation %d" % (i + 1)

            for i in range(4):
                varname = "BTe%d" % (i + 1)
                varobj = cdf.createVariable(varname, 'u2', ('time',), fill_value=intfill)
                varobj.units = "counts"
                varobj.long_name = "BT evaluation amplitude %d" % (i + 1)

            for i in range(4):
                varname = "BTp%d" % (i + 1)
                varobj = cdf.createVariable(varname, 'u2', ('time',), fill_value=intfill)
                varobj.units = "percent"
                varobj.long_name = "BT percent good %d" % (i + 1)
                # varobj.valid_range = [0, 100]

            for i in range(4):
                varname = "BTRSSI%d" % (i + 1)
                varobj = cdf.createVariable(varname, 'u2', ('time',), fill_value=intfill)
                varobj.units = "counts"
                varobj.long_name = "BT Receiver Signal Strength Indicator %d" % (i + 1)

            if ens_data['BTData']['Mode'] == 0:  # water reference layer was used
                varobj = cdf.createVariable('BTRmin', 'f4', ('time',), fill_value=floatfill)
                varobj.units = 'dm'
                varobj.long_name = "BT Ref. min"
                varobj = cdf.createVariable('BTRnear', 'f4', ('time',), fill_value=floatfill)
                varobj.units = 'dm'
                varobj.long_name = "BT Ref. near"
                varobj = cdf.createVariable('BTRfar', 'f4', ('time',), fill_value=floatfill)
                varobj.units = 'dm'
                varobj.long_name = "BT Ref. far"

                for i in range(4):
                    varname = "BTRv%d" % (i + 1)
                    varobj = cdf.createVariable(varname, 'i2', ('time',), fill_value=intfill)
                    varobj.units = "mm s-1"
                    varobj.long_name = "BT Ref. velocity, mm s-1 %d" % (i + 1)

                for i in range(4):
                    varname = "BTRc%d" % (i + 1)
                    varobj = cdf.createVariable(varname, 'u2', ('time',), fill_value=intfill)
                    varobj.units = "counts"
                    varobj.long_name = "BT Ref. correlation %d" % (i + 1)

                for i in range(4):
                    varname = "BTRi%d" % (i + 1)
                    varobj = cdf.createVariable(varname, 'u2', ('time',), fill_value=intfill)
                    varobj.units = "counts"
                    varobj.long_name = "BT Ref. intensity %d" % (i + 1)

                for i in range(4):
                    varname = "BTRp%d" % (i + 1)
                    varobj = cdf.createVariable(varname, 'u2', ('time',), fill_value=intfill)
                    varobj.units = "percent"
                    varobj.long_name = "BT Ref. percent good %d" % (i + 1)
                    varobj.epic_code = 1269 + i

        if 'VPingSetup' in ens_data:
            self.write_dict_to_cdf_attributes(cdf, ens_data['VPingSetup'], "TRDI_VBeam_")

        if 'VBeamLeader' in ens_data:
            self.write_dict_to_cdf_attributes(cdf, ens_data['VBeamLeader'], "TRDI_VBeam_")

        if 'VBeamVData' in ens_data:
            if ens_data['VBeamLeader']['Vertical_Depth_Cells'] == ens_data['FLeader']['Number_of_Cells']:
                varobj = cdf.createVariable("vel5", 'f4', ('time', 'depth'), fill_value=floatfill)
                varobj.units = "mm s-1"
                varobj.long_name = "Beam 5 velocity (mm s-1)"
                varobj = cdf.createVariable("cor5", 'u2', ('time', 'depth'), fill_value=intfill)
                varobj.units = "counts"
                varobj.long_name = "Beam 5 correlation"
                varobj = cdf.createVariable("att5", 'u2', ('time', 'depth'), fill_value=intfill)
                varobj.units = "counts"
                varobj.long_name = "ADCP attenuation of beam 5"
                if 'VBeamGData' in ens_data:
                    varobj = cdf.createVariable("PGd5", 'u2', ('time', 'depth'), fill_value=intfill)
                    varobj.units = "counts"
                    varobj.long_name = "Percent Good Beam 5"
                else:
                    cdf.TRDI_VBeam_note1 = 'Vertical beam data found without Percent Good'
            else:
                print("Vertical beam data found with different number of cells.")
                cdf.TRDI_VBeam_note = "Vertical beam data found with different number of cells. " + \
                                      "Vertical beam data not exported to netCDF"
                print("Vertical beam data not exported to netCDF")

        if 'WaveParams' in ens_data:
            # no units given for any of these in the TRDI docs
            varobj = cdf.createVariable("Hs", 'f4', ('time',), fill_value=floatfill)
            varobj.units = "m"
            varobj.long_name = "Significant Wave Height (m)"
            varobj = cdf.createVariable("Tp", 'f4', ('time',), fill_value=floatfill)
            varobj.units = "s"
            varobj.long_name = "Peak Wave Period (s)"
            varobj = cdf.createVariable("Dp", 'f4', ('time',), fill_value=floatfill)
            varobj.units = "Deg."
            varobj.long_name = "Peak Wave Direction (Deg.)"
            varobj = cdf.createVariable("Dm", 'f4', ('time',), fill_value=floatfill)
            varobj.units = "Deg."
            varobj.long_name = "Mea Peak Wave Direction (Deg.)"
            varobj = cdf.createVariable("SHmax", 'f4', ('time',), fill_value=floatfill)
            varobj.units = "m"
            varobj.long_name = "Maximum Wave Height (m)"
            varobj.note = "from zero crossing analysis of surface track time series"
            varobj = cdf.createVariable("SH13", 'f4', ('time',), fill_value=floatfill)
            varobj.units = "m"
            varobj.long_name = "Significant Wave Height of the largest 1/3 of the waves (m)"
            varobj.note = "in the field from zero crossing anaylsis of surface track time series"
            varobj = cdf.createVariable("SH10", 'f4', ('time',), fill_value=floatfill)
            varobj.units = "m"
            varobj.long_name = "Significant Wave Height of the largest 1/10 of the waves (m)"
            varobj.note = "in the field from zero crossing anaylsis of surface track time series"
            varobj = cdf.createVariable("STmax", 'f4', ('time',), fill_value=floatfill)
            varobj.units = "s"
            varobj.long_name = "Maximum Peak Wave Period (s)"
            varobj.note = "from zero crossing analysis of surface track time series"
            varobj = cdf.createVariable("ST13", 'f4', ('time',), fill_value=floatfill)
            varobj.units = "s"
            varobj.long_name = "Period associated with the peak wave height of the largest 1/3 of the waves (s)"
            varobj.note = "in the field from zero crossing analysis of surface track time series"
            varobj = cdf.createVariable("ST10", 'f4', ('time',), fill_value=floatfill)
            varobj.units = "s"
            varobj.long_name = "Period associated with the peak wave height of the largest 1/10 of the waves (s)"
            varobj.note = "in the field from zero crossing anaylsis of surface track time series"
            varobj = cdf.createVariable("T01", 'f4', ('time',), fill_value=floatfill)
            varobj.units = " "
            varobj = cdf.createVariable("Tz", 'f4', ('time',), fill_value=floatfill)
            varobj.units = " "
            varobj = cdf.createVariable("Tinv1", 'f4', ('time',), fill_value=floatfill)
            varobj.units = " "
            varobj = cdf.createVariable("S0", 'f4', ('time',), fill_value=floatfill)
            varobj.units = " "
            varobj = cdf.createVariable("Source", 'f4', ('time',), fill_value=floatfill)
            varobj.units = " "

        if 'WaveSeaSwell' in ens_data:
            # no units given for any of these in the TRDI docs
            varobj = cdf.createVariable("HsSea", 'f4', ('time',), fill_value=floatfill)
            varobj.units = "m"
            varobj.long_name = "Significant Wave Height (m)"
            varobj.note = "in the sea region of the power spectrum"
            varobj = cdf.createVariable("HsSwell", 'f4', ('time',), fill_value=floatfill)
            varobj.units = "m"
            varobj.long_name = "Significant Wave Height (m)"
            varobj.note = "in the swell region of the power spectrum"
            varobj = cdf.createVariable("TpSea", 'f4', ('time',), fill_value=floatfill)
            varobj.units = "s"
            varobj.long_name = "Peak Wave Period (s)"
            varobj.note = "in the sea region of the power spectrum"
            varobj = cdf.createVariable("TpSwell", 'f4', ('time',), fill_value=floatfill)
            varobj.units = "s"
            varobj.long_name = "Peak Wave Period (s)"
            varobj.note = "in the swell region of the power spectrum"
            varobj = cdf.createVariable("DpSea", 'f4', ('time',), fill_value=floatfill)
            varobj.units = "Deg."
            varobj.long_name = "Peak Wave Direction (Deg.)"
            varobj.note = "in the sea region of the power spectrum"
            varobj = cdf.createVariable("DpSwell", 'f4', ('time',), fill_value=floatfill)
            varobj.units = "Deg."
            varobj.long_name = "Peak Wave Direction (Deg.)"
            varobj.note = "in the swell region of the power spectrum"
            varobj = cdf.createVariable("SeaSwellPeriod", 'f4', ('time',), fill_value=floatfill)
            varobj.units = "s"
            varobj.long_name = "Transition Period between Sea and Swell (s)"

        return cdf, cf_units


    def add_ens_to_netcdf(self, ens: Ensemble, ens_error):

        nslantbeams = ens.EnsembleData.NumBeams

        if (ens_error is None) and (self.ensemble_count >= ens2process[0]):
            # write to netCDF
            if self.netcdf_index == 0:
                print('--- first ensembles read at %s and TRDI #%d' % (
                    ens_data['VLeader']['timestr'], ens.EnsembleData.EnsembleNumber))

            varobj = self.cdf_file.variables['Rec']
            try:
                varobj[self.netcdf_index] = ens.EnsembleData.EnsembleNumber
            except:
                # here we have reached the end of the netCDF file
                self.cdf_file.close()
                return

            # time calculations done when vleader is read
            if time_type == 'EPIC_with_CF':
                varobj = self.cdf_file.variables['time']
                varobj[self.netcdf_index] = ens_data['VLeader']['EPIC_time']
                varobj = self.cdf_file.variables['time2']
                varobj[self.netcdf_index] = ens_data['VLeader']['EPIC_time2']
                varobj = self.cdf_file.variables['cf_time']
                elapsed = ens_data['VLeader']['dtobj']-t0  # timedelta
                elapsed_sec = elapsed.total_seconds()
                varobj[self.netcdf_index] = elapsed_sec
            elif time_type == 'CF_with_EPIC':
                varobj = self.cdf_file.variables['time']
                elapsed = ens_data['VLeader']['dtobj'] - t0  # timedelta
                elapsed_sec = elapsed.total_seconds()
                if elapsed_sec == 0:
                    print('elapsed seconds from ensemble {} is {}'.format(self.ensemble_count, elapsed_sec))

                varobj[self.netcdf_index] = elapsed_sec
                t1, t2 = cftime2EPICtime(elapsed_sec, cf_units)
                varobj = self.cdf_file.variables['EPIC_time']
                varobj[self.netcdf_index] = t1
                varobj = self.cdf_file.variables['EPIC_time2']
                varobj[self.netcdf_index] = t2
            elif time_type == 'EPIC':
                varobj = self.cdf_file.variables['time']
                varobj[self.netcdf_index] = ens_data['VLeader']['EPIC_time']
                varobj = self.cdf_file.variables['time2']
                varobj[self.netcdf_index] = ens_data['VLeader']['EPIC_time2']
            else:  # only CF time, the default
                varobj = self.cdf_file.variables['time']
                elapsed = ens_data['VLeader']['dtobj']-t0  # timedelta
                elapsed_sec = elapsed.total_seconds()
                varobj[self.netcdf_index] = elapsed_sec

            # diagnostic
            if (ens2process[1]-ens2process[0]-1) < 100:
                print('%d %15.8f %s' % (ens.EnsembleData.EnsembleNumber,
                                        ens_data['VLeader']['julian_day_from_julian'],
                                        ens_data['VLeader']['timestr']))

            varobj = self.cdf_file.variables['sv']
            varobj[self.netcdf_index] = ens.AncillaryData.SpeedOfSound

            for i in range(nslantbeams):
                varname = "vel%d" % (i+1)
                varobj = self.cdf_file.variables[varname]
                varobj[self.netcdf_index, :] = ens_data['VData'][i, :]

            for i in range(nslantbeams):
                varname = "cor%d" % (i+1)
                varobj = self.cdf_file.variables[varname]
                varobj[self.netcdf_index, :] = ens_data['CData'][i, :]

            for i in range(nslantbeams):
                varname = "att%d" % (i+1)
                varobj = self.cdf_file.variables[varname]
                varobj[self.netcdf_index, :] = ens_data['IData'][i, :]

            if 'GData' in ens_data:
                for i in range(nslantbeams):
                    varname = "PGd%d" % (i+1)
                    varobj = self.cdf_file.variables[varname]
                    varobj[self.netcdf_index, :] = ens_data['GData'][i, :]

            varobj = self.cdf_file.variables['Rec']
            varobj[self.netcdf_index] = ens_data['VLeader']['Ensemble_Number']
            varobj = self.cdf_file.variables['Hdg']
            varobj[self.netcdf_index] = ens_data['VLeader']['Heading']
            varobj = self.cdf_file.variables['Ptch']
            varobj[self.netcdf_index] = ens_data['VLeader']['Pitch']
            varobj = self.cdf_file.variables['Roll']
            varobj[self.netcdf_index] = ens_data['VLeader']['Roll']
            varobj = self.cdf_file.variables['HdgSTD']
            varobj[self.netcdf_index] = ens_data['VLeader']['H/Hdg_Std_Dev']
            varobj = self.cdf_file.variables['PtchSTD']
            varobj[self.netcdf_index] = ens_data['VLeader']['P/Pitch_Std_Dev']
            varobj = self.cdf_file.variables['RollSTD']
            varobj[self.netcdf_index] = ens_data['VLeader']['R/Roll_Std_Dev']
            varobj = self.cdf_file.variables['Tx']
            varobj[self.netcdf_index] = ens_data['VLeader']['Temperature']
            varobj = self.cdf_file.variables['S']
            varobj[self.netcdf_index] = ens_data['VLeader']['Salinity']
            varobj = self.cdf_file.variables['xmitc']
            varobj[self.netcdf_index] = ens_data['VLeader']['Xmit_Current']
            varobj = self.cdf_file.variables['xmitv']
            varobj[self.netcdf_index] = ens_data['VLeader']['Xmit_Voltage']
            varobj = self.cdf_file.variables['Ambient_Temp']
            varobj[self.netcdf_index] = ens_data['VLeader']['Ambient_Temp']
            varobj = self.cdf_file.variables['Pressure+']
            varobj[self.netcdf_index] = ens_data['VLeader']['Pressure_(+)']
            varobj = self.cdf_file.variables['Pressure-']
            varobj[self.netcdf_index] = ens_data['VLeader']['Pressure_(-)']
            varobj = self.cdf_file.variables['Attitude_Temp']
            varobj[self.netcdf_index] = ens_data['VLeader']['Attitude_Temp']
            varobj = self.cdf_file.variables['EWD1']
            varobj[self.netcdf_index] = int(ens_data['VLeader']['Error_Status_Word_Low_16_bits_LSB'])
            varobj = self.cdf_file.variables['EWD2']
            varobj[self.netcdf_index] = int(ens_data['VLeader']['Error_Status_Word_Low_16_bits_MSB'])
            varobj = self.cdf_file.variables['EWD3']
            varobj[self.netcdf_index] = int(ens_data['VLeader']['Error_Status_Word_High_16_bits_LSB'])
            varobj = self.cdf_file.variables['EWD4']
            varobj[self.netcdf_index] = int(ens_data['VLeader']['Error_Status_Word_High_16_bits_MSB'])

            if ens_data['FLeader']['Depth_sensor_available'] == 'Yes':
                varobj = self.cdf_file.variables['Pressure']
                varobj[netcdf_index] = ens_data['VLeader']['Pressure_deca-pascals']
                varobj = self.cdf_file.variables['PressVar']
                varobj[netcdf_index] = ens_data['VLeader']['Pressure_variance_deca-pascals']

            # add bottom track data write to cdf here
            if 'BTData' in ens_data:
                if ens_data['BTData']['Mode'] == 0:
                    varobj = self.cdf_file.variables['BTRmin']
                    varobj[self.netcdf_index] = ens_data['BTData']['Ref_Layer_Min']
                    varobj = self.cdf_file.variables['BTRnear']
                    varobj[self.netcdf_index] = ens_data['BTData']['Ref_Layer_Near']
                    varobj = self.cdf_file.variables['BTRfar']
                    varobj[self.netcdf_index] = ens_data['BTData']['Ref_Layer_Far']

                varnames = ('BTWe', 'BTWu', 'BTWv', 'BTWd')
                for i in range(nslantbeams):
                    varname = "BTR%d" % (i+1)
                    varobj = self.cdf_file.variables[varname]
                    varobj[self.netcdf_index] = ens_data['BTData']['BT_Range'][i]
                    if ens_data['FLeader']['Coord_Transform'] == 'EARTH':
                        varobj = self.cdf_file.variables[varnames[i]]
                    else:
                        varname = "BTV%d" % (i+1)
                        varobj = self.cdf_file.variables[varname]

                    varobj[self.netcdf_index] = ens_data['BTData']['BT_Vel'][i]
                    varname = "BTc%d" % (i+1)
                    varobj = self.cdf_file.variables[varname]
                    varobj[self.netcdf_index] = ens_data['BTData']['BT_Corr'][i]
                    varname = "BTe%d" % (i+1)
                    varobj = self.cdf_file.variables[varname]
                    varobj[self.netcdf_index] = ens_data['BTData']['BT_Amp'][i]
                    varname = "BTp%d" % (i+1)
                    varobj = self.cdf_file.variables[varname]
                    varobj[self.netcdf_index] = ens_data['BTData']['BT_PGd'][i]
                    varname = "BTRSSI%d" % (i+1)
                    varobj = self.cdf_file.variables[varname]
                    varobj[self.netcdf_index] = ens_data['BTData']['RSSI_Amp'][i]

                    if ens_data['BTData']['Mode'] == 0:
                        varobj[self.netcdf_index] = ens_data['BTData']['Ref_Layer_Vel'][i]
                        varname = "BTRc%d" % (i+1)
                        varobj = self.cdf_file.variables[varname]
                        varobj[self.netcdf_index] = ens_data['BTData']['Ref_Layer_Corr'][i]
                        varname = "BTRi%d" % (i+1)
                        varobj = self.cdf_file.variables[varname]
                        varobj[self.netcdf_index] = ens_data['BTData']['Ref_Layer_Amp'][i]
                        varname = "BTRp%d" % (i+1)
                        varobj = self.cdf_file.variables[varname]
                        varobj[self.netcdf_index] = ens_data['BTData']['Ref_Layer_PGd'][i]

            if 'VBeamVData' in ens_data:
                if ens_data['VBeamLeader']['Vertical_Depth_Cells'] == ens_data['FLeader']['Number_of_Cells']:
                    varobj = self.cdf_file.variables['vel5']
                    varobj[self.netcdf_index, :] = ens_data['VBeamVData']
                    varobj = self.cdf_file.variables['cor5']
                    varobj[self.netcdf_index, :] = ens_data['VBeamCData']
                    varobj = self.cdf_file.variables['att5']
                    varobj[self.netcdf_index, :] = ens_data['VBeamIData']
                    if 'VBeamGData' in ens_data:
                        varobj = self.cdf_file.variables['PGd5']
                        varobj[self.netcdf_index, :] = ens_data['VBeamGData']

            if 'WaveParams' in ens_data:
                # we can get away with this because the key names and var names are the same
                for key in ens_data['WaveParams']:
                    varobj = self.cdf_file.variables[key]
                    varobj[self.netcdf_index] = ens_data['WaveParams'][key]

            if 'WaveSeaSwell' in ens_data:
                # we can get away with this because the key names and var names are the same
                for key in ens_data['WaveSeaSwell']:
                    varobj = self.cdf_file.variables[key]
                    varobj[self.netcdf_index] = ens_data['WaveSeaSwell'][key]

            self.netcdf_index += 1

        elif ens_error == 'no ID':
            print('Stopping because ID tracking lost')
            self.cdf_file.close()

        self.ensemble_count += 1

    def to_netcdf(ens_file: str, cdf_file: str, good_ens: [], serial_number: str, time_type: str, delta_t: int ):
        """
        convert from binary pd0 format to netcdf

        :param str pd0File: is path of raw PD0 format input file with current ensembles
        :param str cdfFile: is path of a netcdf4 EPIC compliant output file
        :param list good_ens: [start, end] ensembles to export.  end = -1 for all ensembles in file
        :param str serial_number: serial number of the instrument
        :param str time_type: "CF" for CF conventions, "EPIC" for EPIC conventions
        :param str delta_t: time between ensembles, in seconds.  15 min profiles would be 900
        :return: count of ensembles read, ending index of netCDF file, error type if file could not be read
        """

    def to_netcdf(pd0File, cdfFile, good_ens, serial_number, time_type, delta_t):
        """
        convert from binary pd0 format to netcdf

        :param str pd0File: is path of raw PD0 format input file with current ensembles
        :param str cdfFile: is path of a netcdf4 EPIC compliant output file
        :param list good_ens: [start, end] ensembles to export.  end = -1 for all ensembles in file
        :param str serial_number: serial number of the instrument
        :param str time_type: "CF" for CF conventions, "EPIC" for EPIC conventions
        :param str delta_t: time between ensembles, in seconds.  15 min profiles would be 900
        :return: count of ensembles read, ending index of netCDF file, error type if file could not be read
        """

        # TODO figure out a better way to handle this situation
        # need this check in case this function is used as a stand alone function
        # this is necessary so that this function does not change the value
        # in the calling function

        ens2process = good_ens[:]
        verbose = True  # diagnostic, True = turn on output, False = silent

        maxens, ens_len, ens_data, data_start_posn = analyzepd0file(pd0File, verbose)

        infile = open(pd0File, 'rb')

        infile.seek(data_start_posn)

        if (ens2process[1] < 0) or ens2process[1] == np.inf:
            ens2process[1] = maxens

        # we are good to go, get the output file ready
        print('Setting up netCDF file %s' % cdfFile)
        cdf, cf_units = setup_netcdf_file(cdfFile, ens_data, ens2process, serial_number, time_type, delta_t)
        # we want to save the time stamp from this ensemble since it is the
        # time from which all other times in the file will be relative to
        t0 = ens_data['VLeader']['dtobj']

        netcdf_index = 0
        ensemble_count = 0
        verbose = False  # diagnostic, True = turn on output, False = silent
        nslantbeams = 4

        # priming read - for the while loop
        # note that ensemble lengths can change in the middle of the file!
        # horribly inefficient, but here we go, one step backward, two forward...
        bookmark = infile.tell()  # save beginning of next ensemble
        # need to read the header from the file to know the ensemble size
        header = read_TRDI_header(infile)
        if header['sourceID'] != b'\x7f':
            print('non-currents ensemble found at %d' % bookmark)

        if ens_len != header['nbytesperens']+2:
            ens_len = header['nbytesperens']+2  # update to what we have

        # go back to where this ensemble started before we checked the header
        infile.seek(bookmark)
        ens = infile.read(ens_len)
        ens_error = None

        while len(ens) > 0:
            # print('-- ensemble %d length %g, file position %g' % (ensemble_count, len(ens), infile.tell()))
            # print(ens_data['header'])
            ens_data, ens_error = parse_TRDI_ensemble(ens, verbose)

            if (ens_error is None) and (ensemble_count >= ens2process[0]):
                # write to netCDF
                if netcdf_index == 0:
                    print('--- first ensembles read at %s and TRDI #%d' % (
                        ens_data['VLeader']['timestr'], ens_data['VLeader']['Ensemble_Number']))

                varobj = cdf.variables['Rec']
                try:
                    varobj[netcdf_index] = ens_data['VLeader']['Ensemble_Number']
                except:
                    # here we have reached the end of the netCDF file
                    cdf.close()
                    infile.close()
                    return

                # time calculations done when vleader is read
                if time_type == 'EPIC_with_CF':
                    varobj = cdf.variables['time']
                    varobj[netcdf_index] = ens_data['VLeader']['EPIC_time']
                    varobj = cdf.variables['time2']
                    varobj[netcdf_index] = ens_data['VLeader']['EPIC_time2']
                    varobj = cdf.variables['cf_time']
                    elapsed = ens_data['VLeader']['dtobj']-t0  # timedelta
                    elapsed_sec = elapsed.total_seconds()
                    varobj[netcdf_index] = elapsed_sec
                elif time_type == 'CF_with_EPIC':
                    varobj = cdf.variables['time']
                    elapsed = ens_data['VLeader']['dtobj'] - t0  # timedelta
                    elapsed_sec = elapsed.total_seconds()
                    if elapsed_sec == 0:
                        print('elapsed seconds from ensemble {} is {}'.format(ensemble_count, elapsed_sec))

                    varobj[netcdf_index] = elapsed_sec
                    t1, t2 = cftime2EPICtime(elapsed_sec, cf_units)
                    varobj = cdf.variables['EPIC_time']
                    varobj[netcdf_index] = t1
                    varobj = cdf.variables['EPIC_time2']
                    varobj[netcdf_index] = t2
                elif time_type == 'EPIC':
                    varobj = cdf.variables['time']
                    varobj[netcdf_index] = ens_data['VLeader']['EPIC_time']
                    varobj = cdf.variables['time2']
                    varobj[netcdf_index] = ens_data['VLeader']['EPIC_time2']
                else:  # only CF time, the default
                    varobj = cdf.variables['time']
                    elapsed = ens_data['VLeader']['dtobj']-t0  # timedelta
                    elapsed_sec = elapsed.total_seconds()
                    varobj[netcdf_index] = elapsed_sec

                # diagnostic
                if (ens2process[1]-ens2process[0]-1) < 100:
                    print('%d %15.8f %s' % (ens_data['VLeader']['Ensemble_Number'],
                                            ens_data['VLeader']['julian_day_from_julian'],
                                            ens_data['VLeader']['timestr']))

                varobj = cdf.variables['sv']
                varobj[netcdf_index] = ens_data['VLeader']['Speed_of_Sound']

                for i in range(nslantbeams):
                    varname = "vel%d" % (i+1)
                    varobj = cdf.variables[varname]
                    varobj[netcdf_index, :] = ens_data['VData'][i, :]

                for i in range(nslantbeams):
                    varname = "cor%d" % (i+1)
                    varobj = cdf.variables[varname]
                    varobj[netcdf_index, :] = ens_data['CData'][i, :]

                for i in range(nslantbeams):
                    varname = "att%d" % (i+1)
                    varobj = cdf.variables[varname]
                    varobj[netcdf_index, :] = ens_data['IData'][i, :]

                if 'GData' in ens_data:
                    for i in range(nslantbeams):
                        varname = "PGd%d" % (i+1)
                        varobj = cdf.variables[varname]
                        varobj[netcdf_index, :] = ens_data['GData'][i, :]

                varobj = cdf.variables['Rec']
                varobj[netcdf_index] = ens_data['VLeader']['Ensemble_Number']
                varobj = cdf.variables['Hdg']
                varobj[netcdf_index] = ens_data['VLeader']['Heading']
                varobj = cdf.variables['Ptch']
                varobj[netcdf_index] = ens_data['VLeader']['Pitch']
                varobj = cdf.variables['Roll']
                varobj[netcdf_index] = ens_data['VLeader']['Roll']
                varobj = cdf.variables['HdgSTD']
                varobj[netcdf_index] = ens_data['VLeader']['H/Hdg_Std_Dev']
                varobj = cdf.variables['PtchSTD']
                varobj[netcdf_index] = ens_data['VLeader']['P/Pitch_Std_Dev']
                varobj = cdf.variables['RollSTD']
                varobj[netcdf_index] = ens_data['VLeader']['R/Roll_Std_Dev']
                varobj = cdf.variables['Tx']
                varobj[netcdf_index] = ens_data['VLeader']['Temperature']
                varobj = cdf.variables['S']
                varobj[netcdf_index] = ens_data['VLeader']['Salinity']
                varobj = cdf.variables['xmitc']
                varobj[netcdf_index] = ens_data['VLeader']['Xmit_Current']
                varobj = cdf.variables['xmitv']
                varobj[netcdf_index] = ens_data['VLeader']['Xmit_Voltage']
                varobj = cdf.variables['Ambient_Temp']
                varobj[netcdf_index] = ens_data['VLeader']['Ambient_Temp']
                varobj = cdf.variables['Pressure+']
                varobj[netcdf_index] = ens_data['VLeader']['Pressure_(+)']
                varobj = cdf.variables['Pressure-']
                varobj[netcdf_index] = ens_data['VLeader']['Pressure_(-)']
                varobj = cdf.variables['Attitude_Temp']
                varobj[netcdf_index] = ens_data['VLeader']['Attitude_Temp']
                varobj = cdf.variables['EWD1']
                varobj[netcdf_index] = int(ens_data['VLeader']['Error_Status_Word_Low_16_bits_LSB'])
                varobj = cdf.variables['EWD2']
                varobj[netcdf_index] = int(ens_data['VLeader']['Error_Status_Word_Low_16_bits_MSB'])
                varobj = cdf.variables['EWD3']
                varobj[netcdf_index] = int(ens_data['VLeader']['Error_Status_Word_High_16_bits_LSB'])
                varobj = cdf.variables['EWD4']
                varobj[netcdf_index] = int(ens_data['VLeader']['Error_Status_Word_High_16_bits_MSB'])

                if ens_data['FLeader']['Depth_sensor_available'] == 'Yes':
                    varobj = cdf.variables['Pressure']
                    varobj[netcdf_index] = ens_data['VLeader']['Pressure_deca-pascals']
                    varobj = cdf.variables['PressVar']
                    varobj[netcdf_index] = ens_data['VLeader']['Pressure_variance_deca-pascals']

                # add bottom track data write to cdf here
                if 'BTData' in ens_data:
                    if ens_data['BTData']['Mode'] == 0:
                        varobj = cdf.variables['BTRmin']
                        varobj[netcdf_index] = ens_data['BTData']['Ref_Layer_Min']
                        varobj = cdf.variables['BTRnear']
                        varobj[netcdf_index] = ens_data['BTData']['Ref_Layer_Near']
                        varobj = cdf.variables['BTRfar']
                        varobj[netcdf_index] = ens_data['BTData']['Ref_Layer_Far']

                    varnames = ('BTWe', 'BTWu', 'BTWv', 'BTWd')
                    for i in range(nslantbeams):
                        varname = "BTR%d" % (i+1)
                        varobj = cdf.variables[varname]
                        varobj[netcdf_index] = ens_data['BTData']['BT_Range'][i]
                        if ens_data['FLeader']['Coord_Transform'] == 'EARTH':
                            varobj = cdf.variables[varnames[i]]
                        else:
                            varname = "BTV%d" % (i+1)
                            varobj = cdf.variables[varname]

                        varobj[netcdf_index] = ens_data['BTData']['BT_Vel'][i]
                        varname = "BTc%d" % (i+1)
                        varobj = cdf.variables[varname]
                        varobj[netcdf_index] = ens_data['BTData']['BT_Corr'][i]
                        varname = "BTe%d" % (i+1)
                        varobj = cdf.variables[varname]
                        varobj[netcdf_index] = ens_data['BTData']['BT_Amp'][i]
                        varname = "BTp%d" % (i+1)
                        varobj = cdf.variables[varname]
                        varobj[netcdf_index] = ens_data['BTData']['BT_PGd'][i]
                        varname = "BTRSSI%d" % (i+1)
                        varobj = cdf.variables[varname]
                        varobj[netcdf_index] = ens_data['BTData']['RSSI_Amp'][i]

                        if ens_data['BTData']['Mode'] == 0:
                            varobj[netcdf_index] = ens_data['BTData']['Ref_Layer_Vel'][i]
                            varname = "BTRc%d" % (i+1)
                            varobj = cdf.variables[varname]
                            varobj[netcdf_index] = ens_data['BTData']['Ref_Layer_Corr'][i]
                            varname = "BTRi%d" % (i+1)
                            varobj = cdf.variables[varname]
                            varobj[netcdf_index] = ens_data['BTData']['Ref_Layer_Amp'][i]
                            varname = "BTRp%d" % (i+1)
                            varobj = cdf.variables[varname]
                            varobj[netcdf_index] = ens_data['BTData']['Ref_Layer_PGd'][i]

                if 'VBeamVData' in ens_data:
                    if ens_data['VBeamLeader']['Vertical_Depth_Cells'] == ens_data['FLeader']['Number_of_Cells']:
                        varobj = cdf.variables['vel5']
                        varobj[netcdf_index, :] = ens_data['VBeamVData']
                        varobj = cdf.variables['cor5']
                        varobj[netcdf_index, :] = ens_data['VBeamCData']
                        varobj = cdf.variables['att5']
                        varobj[netcdf_index, :] = ens_data['VBeamIData']
                        if 'VBeamGData' in ens_data:
                            varobj = cdf.variables['PGd5']
                            varobj[netcdf_index, :] = ens_data['VBeamGData']

                if 'WaveParams' in ens_data:
                    # we can get away with this because the key names and var names are the same
                    for key in ens_data['WaveParams']:
                        varobj = cdf.variables[key]
                        varobj[netcdf_index] = ens_data['WaveParams'][key]

                if 'WaveSeaSwell' in ens_data:
                    # we can get away with this because the key names and var names are the same
                    for key in ens_data['WaveSeaSwell']:
                        varobj = cdf.variables[key]
                        varobj[netcdf_index] = ens_data['WaveSeaSwell'][key]

                netcdf_index += 1

            elif ens_error == 'no ID':
                print('Stopping because ID tracking lost')
                infile.close()
                cdf.close()
                sys.exit(1)

            ensemble_count += 1

            if ensemble_count > maxens:
                print('stopping at estimated end of file ensemble %d' % ens2process[1])
                break

            n = 10000

            ensf, ensi = math.modf(ensemble_count/n)
            if ensf == 0:
                print('%d ensembles read at %s and TRDI #%d' % (ensemble_count, ens_data['VLeader']['dtobj'],
                                                                ens_data['VLeader']['Ensemble_Number']))

            if ensemble_count >= ens2process[1]-1:
                print('stopping at requested ensemble %d' % ens2process[1])
                break

            # note that ensemble lengths can change in the middle of the file!
            # TODO - is there a faster way to do this??
            bookmark = infile.tell()  # save beginning of next ensemble
            # TODO - since we are jumping around, we should check here to see
            #   how close to the end of the file we are - if it is within one
            #   header length - we are done
            #   need to read the header from the file to know the ensemble size
            header = read_TRDI_header(infile)

            if header is None:
                # we presume this is the end of the file, since we don't have header info
                print('end of file reached with incomplete header')
                break

            if header['sourceID'] != b'\x7f':
                print('non-currents ensemble found at %d' % bookmark)

            if ens_len != header['nbytesperens']+2:
                ens_len = header['nbytesperens']+2  # update to what we have

            # TODO - fix this so that we aren't going back and forth, it is really slow
            # go back to where this ensemble started before we checked the header
            infile.seek(bookmark)
            ens = infile.read(ens_len)

        else:  # while len(ens) > 0:
            print('end of file reached')

        if ensemble_count < maxens:
            print('end of file reached after %d ensembles, less than estimated in the file' % ensemble_count)
        elif ensemble_count > maxens:
            print('end of file reached after %d ensembles, more than estimated in the file' % ensemble_count)

        infile.close()
        cdf.close()

        print('%d ensembles read, %d records written' % (ensemble_count, netcdf_index))

        return ensemble_count, netcdf_index, ens_error

    def write_dict_to_cdf_attributes(self, netcdf_object, d, tag):
        """
        write a dictionary to netCDF attributes
        :param netcdf_object: netcdf file object
        :param dict d: dictionary of attribute names and values
        :param str tag: an identifier to prepend to the attribute name
        :return: the dictionary d with any strings that can be changed to numbers, as numbers
        """
        i = 0
        # first, convert as many of the values in d to numbers as we can
        for key in iter(d):
            if type(d[key]) == str:
                try:
                    d[key] = float(d[key])
                except ValueError:
                    # we really don't need to print here,
                    # but python insists we do something
                    # print('   can\'t convert %s to float' % key)
                    i += 1

        for key in iter(d):
            newkey = tag + key
            try:
                netcdf_object.setncattr(newkey, d[key])
            except:
                print('can\'t set %s attribute' % key)

        return d