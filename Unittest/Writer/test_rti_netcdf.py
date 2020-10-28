from rti_python.Writer.rti_netcdf import RtiNetcdf


def test_netcdf():
    file_paths = [r"C:\Users\rico\Documents\data\Waves_5_beam\B0000006.ENS"]

    net_cdf = RtiNetcdf()
    net_cdf.write(file_paths)