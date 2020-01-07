import math
import datetime
import numpy as np
from enum import Enum
from rti_python.Ensemble.Ensemble import Ensemble


class EnsembleFlowInfo:

    def __init__(self):
        self.top_flow = 0.0
        self.bottom_flow = 0.0
        self.measured_flow = 0.0
        self.valid = False
        self.measured_bin_info = []

class MeasuredBinInfo:

    def __init__(self):
        self.depth = 0.0
        self.flow = 0.0
        self.valid = False

class FlowMode(Enum):
    """
    TRDI restricts the constant
    method to use of the top depth cell only and the power-law
    estimate to using all of the available depth cells, but provides
    an additional 3-point slope method to fit situations where wind
    significantly affects the velocity at the water surface.
    """

    # This constant extrapolation method is often used where there
    # is an upstream wind or an irregular velocity profile through the
    # measured portion of the water column.
    Constants = 1

    # A method using
    # a one-sixth power law (Chen, 1989) eventually was chosen
    # because of its robust noise rejection capability during most
    # streamflow conditions.
    # The power-law estimation scheme is an approximation only
    # and emulates a Manning-like vertical distribution of horizontal
    # water velocities. Different power coefficients can be used to
    # adjust the shape of the curve fit to emulate profiles measured
    # in an estuarine environment or in areas that have bedforms that
    # produce nonstandard hydrologic conditions.
    PowerFunction = 2

    # 3-point slope method to fit situations where wind
    # significantly affects the velocity at the water surface
    Slope = 3


class Slope:

    def __init__(self):
        self.a = 0.0
        self.b = 0.0
        self.c = 0.0

    def setXYs(self, x_list: [], y_list: []):
        if len(x_list) != len(y_list) and len(x_list) > 0:
            return

        accum_x = 0.0
        accum_y = 0.0
        accum_xx = 0.0
        accum_xy = 0.0

        list_length = len(x_list)

        for index in range(x_list):
            accum_x += x_list[index]
            accum_y += y_list[index]
            accum_xx += (x_list[index] * x_list[index])
            accum_xy += (x_list[index] * y_list[index])

        avg_x = accum_x / list_length
        avg_y = accum_y / list_length
        val = list_length * accum_xx - accum_x * accum_x

        if val == 0.0:
            self.b = 0.0
            self.a = 1.0
            self.c = -avg_x
        else:
            val8 = (list_length * accum_xy - accum_x * accum_y) / val
            val9 = (accum_y * accum_xx - accum_x * accum_xy) / val
            self.b = 1.0
            self.a = -val8
            self.c = -val9

    def cal_x(self, y: float) -> float:
        if self.a == 0.0:
            return 0.0

        return 0.0 - (self.b * y + self.c) / self.a

    def cal_y(self, x: float) -> float:
        if self.b == 0.0:
            return 0.0

        return 0.0 - (self.a * x * self.c) / self.b


class CalcDischarge:

    # One-sixth power law common value
    ONE_SIXTH_POWER_LAW = 1/6

    def __init__(self):


    def calculate_ensemble_flow(self,
                                ens: Ensemble,
                                boat_draft: float,
                                beam_angle: float,
                                pulse_length: float,
                                pulse_lag: float,
                                bt_east: float,
                                bt_north: float,
                                bt_vert: float,
                                delta_time: float,
                                top_flow_mode: FlowMode=FlowMode.Constants,
                                top_pwr_func_exponent: float=ONE_SIXTH_POWER_LAW,
                                bottom_flow_mode: FlowMode=FlowMode.PowerFunction,
                                bottom_pwr_func_exponent: float=ONE_SIXTH_POWER_LAW) -> EnsembleFlowInfo:

        # Initialize the values
        ensemble_flow_info = EnsembleFlowInfo()
        ensemble_flow_info.valid = False

        # Check vessel velocity
        if abs(bt_east) > 80.0 or abs(bt_north) > 80.0:
            return ensemble_flow_info

        # Check for bad cell size
        if ens.IsAncillaryData and ens.AncillaryData.BinSize < 1E-06:
            return ensemble_flow_info

        # Get the average bottom track range
        # num2
        avg_depth = 0.0
        if ens.IsBottomTrack:
            # num4
            avg_depth = ens.BottomTrack.avg_range()

        if avg_depth <= 0.0:
            return ensemble_flow_info

        # Maximum depth of all the ranges
        max_depth = max(ens.BottomTrack.Range)

        # num5
        depth_angle = max_depth * math.cos(beam_angle / 180.0 * math.pi) + boat_draft - max((pulse_length + pulse_lag) / 2.0, ens.AncillaryData.BinSize / 2.0)

        # Average depth and the boat draft
        # num6
        overall_depth = avg_depth + boat_draft

        measured_bin_info_top = None
        measured_bin_info_bottom = None

        # First Bin Position
        # num7
        first_bin_pos = ens.AncillaryData.FirstBinRange + boat_draft

        # List of bins
        measured_bin_info_list = []
        bin_list = []
        bin_index = 0
        # num8
        accum_flow = 0.0
        # num9
        accum_east_vel = 0.0
        # num10
        accum_north_vel = 0.0
        # num11
        accum_bins = 0
        bt_vel = [bt_east, bt_north]
        bin_depth_index = first_bin_pos
        for bin_index in range(ens.EnsembleData.NumBins):
            if first_bin_pos < depth_angle and ens.EnsembleData.NumBeams >= 2:

                # num3
                earth_vel = [ens.EarthVelocity.Velocities[bin_index, 0], ens.EarthVelocity.Velocities[bin_index, 1]]
                cross_prod_bin = np.cross(earth_vel, bt_vel)

                # Store the bin info
                # Equation A16
                # Calculate the total flow of a bin with the cross product of the accumulated velocities * dt * dz
                # Qbin = (Vw X Vb)*dt*dz
                # Cross product of water velocity and boat velocity
                # dt is delta time
                # dz is change in bin size
                measured_bin_info = MeasuredBinInfo()
                measured_bin_info.depth = bin_depth_index                                                 # Bin Depth
                measured_bin_info.flow = cross_prod_bin[0] * delta_time * ens.AncillaryData.BinSize       # Flow for bin
                measured_bin_info.valid = True                                                            # Valid bin
                measured_bin_info_list.append(measured_bin_info)

                # Set the top most bin
                if measured_bin_info.valid and not measured_bin_info_top:
                    measured_bin_info_top = measured_bin_info

                # Set the bottom most bin
                if measured_bin_info.valid:
                    measured_bin_info_bottom = measured_bin_info

                # Accumulate flow
                accum_flow += measured_bin_info.flow

                # Accumulate East Velocity
                accum_east_vel += ens.EarthVelocity.Velocities[bin_index, 0]

                # Accumulate North Velocity
                accum_north_vel += ens.EarthVelocity.Velocities[bin_index, 1]

                # Accumulate good bins
                accum_bins += 1

                # Accumulate the list of bins
                bin_list.append(bin_index)

                # Increment the bin position
                bin_depth_index += ens.AncillaryData.BinSize

        # Store the bin info
        ensemble_flow_info.measured_bin_info = measured_bin_info_list

        if not measured_bin_info_top.valid:
            ensemble_flow_info

        # Get the depths
        depth1 = measured_bin_info_top.depth
        depth2 = measured_bin_info_bottom.depth
        x1 = overall_depth
        x2 = overall_depth - depth1 + ens.AncillaryData.BinSize / 2.0
        x3 = overall_depth - depth2 - ens.AncillaryData.BinSize / 2.0

        # Accumulate the overall velocity and take the cross product
        # to get the overall discharge
        # Equation A16
        # Calculate the total flow of a bin with the cross product of the accumulated velocities * dt * dz
        # Qbin = (Vw X Vb)*dt*dz
        # Cross product of water velocity and boat velocity
        # dt is delta time
        # dz is change in bin size
        vel_accum = [accum_east_vel / accum_bins, accum_north_vel / accum_bins]
        cross_prod_accum_vel = np.cross(vel_accum, bt_vel)
        ensemble_flow_info.measured_flow = cross_prod_accum_vel * delta_time * (x2 - x3)

        # Calculate the top flow based on the mode selected
        if top_flow_mode == FlowMode.Constants:
            # Use the flow from the top most bin only (TRDI)
            ensemble_flow_info.top_flow = measured_bin_info_top.flow / ens.AncillaryData.BinSize * (x1 - x2)
        elif top_flow_mode == FlowMode.PowerFunction:
            y1 = top_pwr_func_exponent + 1.0
            ensemble_flow_info.top_flow = accum_flow * (math.pow(x1, y1) - math.pow(x2, y1)) / (math.pow(x2, y1) - math.pow(x3, y1))
        elif top_flow_mode == FlowMode.Slope:
            if len(bin_list) < 6:
                ensemble_flow_info.top_flow = measured_bin_info_top.flow / ens.AncillaryData.BinSize * (x1 - x2)

            # Accumulate the velocities and bin depths
            # for the second and third good bins, skipping the first bin
            depth_list = []
            east_vel_list = []
            north_vel_list = []
            for bin_slope_index in range(2):
                # Get the next bin in the list of good bins
                # Add 1 to skip the first bin
                index_bin = bin_list[bin_slope_index+1]

                # Calculate the depth of the bin
                depth_bin = ens.AncillaryData.FirstBinRange + boat_draft + (index_bin * ens.AncillaryData.BinSize)

                # Get the east and north velocity
                east_vel_bin = ens.EarthVelocity.Velocities[index_bin][0]
                north_vel_bin = ens.EarthVelocity.Velocities[index_bin][1]

                # Add it to the list
                depth_list.append(depth_bin)
                east_vel_list.append(east_vel_bin)
                north_vel_list.append(north_vel_bin)

            x4 = (x1 - x2) / 2.0
            slope_vel_east = Slope()
            slope_vel_east.setXYs(earth_vel, depth_list)
            slope_vel_north = Slope()
            slope_vel_north.setXYs(north_vel_list, depth_list)
            if (depth_list[1] - depth_list[0]) != 0:
                slope_vel_east = slope_vel_east.cal_y(x4)
                slope_vel_north = slope_vel_north.cal_y(x4)
            else:
                ensemble_flow_info.top_flow = measured_bin_info.flow / ens.AncillaryData.BinSize * (x1 - x2)

            # Calculate the cross product of the slope of the top bins
            top_vel_accum = [slope_vel_east, slope_vel_north]
            cross_prod_top_accum_vel = np.cross(top_vel_accum, bt_vel)
            ensemble_flow_info.top_flow = delta_time * (x1-x2) * cross_prod_top_accum_vel

        # Set the Bottom Flow
        if bottom_flow_mode == FlowMode.PowerFunction:
            y2 = top_pwr_func_exponent + 1.0
            ensemble_flow_info.bottom_flow = accum_flow * math.pow(x3, y2) / (math.pow(x2, y2) - math.pow(x3, y2))
        elif bottom_flow_mode == FlowMode.Constants:
            ensemble_flow_info.bottom_flow = measured_bin_info_bottom.flow / ens.AncillaryData.BinSize * x3
