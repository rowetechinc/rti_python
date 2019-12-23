

class Transect:

    def __init__(self, index):
        self.transect_index = index
        self.name = ""
        self.station_name = ""
        self.station_info = ""
        self.cross_section_loc = ""
        self.comments = ""
        self.drafts = ""
        self.declination = ""
        self.measured_water_temp = ""
        self.left_edge_shape = ""
        self.right_edge_shape = ""
        self.left_edge_distance = 0.0
        self.right_edge_distance = 0.0
        self.manual_speed_of_sound = 0.0
        self.transect_identification = ""
        self.time_of_day_start_transect = ""
        self.elasped_time = 0.0
        self.mean_vel_boat = 0.0
        self.mean_vel_water = 0.0
        self.total_width = 0.0
        self.sys_test_result = ""
        self.list_ens = []
        self.bottom_extrap = 0.0
        self.top_extrap = 0.0
        self.left_extrap = 0.0
        self.right_extrap = 0.0
        self.q_bottom = 0.0
        self.q_top = 0.0
        self.q_right = 0.0
        self.q_left = 0.0
        self.total_discharge = 0.0

    def get_name(self) -> str:
        return "Transect_" + str(self.transect_index)

