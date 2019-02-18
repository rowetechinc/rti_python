import pytest
import os
import scipy.io as sio
import rti_python.Codecs.WaveForceCodec as wfc
import rti_python.Ensemble.AncillaryData as AncillaryData
import rti_python.Ensemble.EnsembleData as EnsembleData
import rti_python.Ensemble.RangeTracking as RangeTracking
import rti_python.Ensemble.Ensemble as Ensemble


def test_constructor():
    codec = wfc.WaveForceCodec()

    assert codec.height_source == pytest.approx(4, 0, False)
    assert codec.Bin1 == pytest.approx(3, 0, False)
    assert codec.Bin2 == pytest.approx(4, 0, False)
    assert codec.Bin3 == pytest.approx(5, 0, False)
    assert codec.PressureSensorDepth == pytest.approx(30, 0, False)
    assert codec.EnsInBurst == pytest.approx(2048, 0, False)
    assert len(codec.selected_bin) == pytest.approx(0, 0, False)
    assert codec.CorrThreshold == pytest.approx(0.25, 0.0, False)
    assert codec.PressureOffset == pytest.approx(0.0, 0.0, False)


def test_init():
    codec = wfc.WaveForceCodec()
    codec.init()

    assert codec.EnsInBurst == pytest.approx(2048, 0, False)
    assert codec.FilePath == os.path.expanduser('~')
    assert codec.Lat == pytest.approx(0.0, 0.1, False)
    assert codec.Lon == pytest.approx(0.0, 0.1, False)
    assert codec.height_source == pytest.approx(4, 0, False)
    assert codec.Bin1 == pytest.approx(3, 0, False)
    assert codec.Bin2 == pytest.approx(4, 0, False)
    assert codec.Bin3 == pytest.approx(5, 0, False)
    assert codec.CorrThreshold == pytest.approx(0.25, 0.0, False)
    assert codec.PressureOffset == pytest.approx(0.0, 0.0, False)
    assert codec.PressureSensorDepth == pytest.approx(30, 0, False)
    assert codec.EnsInBurst == pytest.approx(2048, 0, False)
    assert len(codec.selected_bin) == pytest.approx(3, 0, False)


def test_init_1():
    codec = wfc.WaveForceCodec()
    codec.init(1024, os.path.expanduser('~'), 31.0, 118.5, 5, 6, 7, 22, 1, 0.84, 1.3)

    assert codec.EnsInBurst == pytest.approx(1024, 0, False)
    assert codec.FilePath == os.path.expanduser('~')
    assert codec.Lat == pytest.approx(31.0, 0.1, False)
    assert codec.Lon == pytest.approx(118.5, 0.1, False)
    assert codec.height_source == pytest.approx(1, 0, False)
    assert codec.Bin1 == pytest.approx(5, 0, False)
    assert codec.Bin2 == pytest.approx(6, 0, False)
    assert codec.Bin3 == pytest.approx(7, 0, False)
    assert codec.CorrThreshold == pytest.approx(0.84, 0.0, False)
    assert codec.PressureOffset == pytest.approx(1.3, 0.0, False)
    assert codec.PressureSensorDepth == pytest.approx(22, 0, False)
    assert len(codec.selected_bin) == pytest.approx(3, 0, False)


def test_update():
    codec = wfc.WaveForceCodec()
    codec.update_settings(1024, os.path.expanduser('~'), 31.0, 118.5, 5, 6, 7, 22, 1, 0.84, 1.3)

    assert codec.EnsInBurst == pytest.approx(1024, 0, False)
    assert codec.FilePath == os.path.expanduser('~')
    assert codec.Lat == pytest.approx(31.0, 0.1, False)
    assert codec.Lon == pytest.approx(118.5, 0.1, False)
    assert codec.height_source == pytest.approx(1, 0, False)
    assert codec.height_source == pytest.approx(1, 0, False)
    assert codec.Bin1 == pytest.approx(5, 0, False)
    assert codec.Bin2 == pytest.approx(6, 0, False)
    assert codec.Bin3 == pytest.approx(7, 0, False)
    assert codec.CorrThreshold == pytest.approx(0.84, 0.0, False)
    assert codec.PressureOffset == pytest.approx(1.3, 0.0, False)
    assert codec.PressureSensorDepth == pytest.approx(22, 0, False)
    assert len(codec.selected_bin) == pytest.approx(3, 0, False)


def test_add_ens():
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    num_ens_in_burst = 3

    codec = wfc.WaveForceCodec()
    codec.init(num_ens_in_burst, curr_dir, 32.0, 118.0, 3, 4, 5, 30, 4)
    codec.process_data_event += waves_rcv

    # Create Ensembles
    ancillary_data1 = AncillaryData.AncillaryData(17, 1)
    ancillary_data1.Heading = 22.0
    ancillary_data1.Pitch = 10.0
    ancillary_data1.Roll = 1.0
    ancillary_data1.TransducerDepth = 30.2
    ancillary_data1.WaterTemp = 23.5
    ancillary_data1.BinSize = 1
    ancillary_data1.FirstBinRange = 3

    ancillary_data2 = AncillaryData.AncillaryData(17, 1)
    ancillary_data2.Heading = 23.0
    ancillary_data2.Pitch = 13.0
    ancillary_data2.Roll = 3.0
    ancillary_data2.TransducerDepth = 33.2
    ancillary_data2.WaterTemp = 26.5
    ancillary_data2.BinSize = 1
    ancillary_data2.FirstBinRange = 3

    ancillary_data3 = AncillaryData.AncillaryData(17, 1)
    ancillary_data3.Heading = 24.0
    ancillary_data3.Pitch = 14.0
    ancillary_data3.Roll = 4.0
    ancillary_data3.TransducerDepth = 34.2
    ancillary_data3.WaterTemp = 27.5
    ancillary_data3.BinSize = 1
    ancillary_data3.FirstBinRange = 3

    ensemble_data1 = EnsembleData.EnsembleData(19, 1)
    ensemble_data1.EnsembleNumber = 1
    ensemble_data1.NumBeams = 4
    ensemble_data1.NumBins = 10
    ensemble_data1.Year = 2019
    ensemble_data1.Month = 2
    ensemble_data1.Day = 19
    ensemble_data1.Hour = 10
    ensemble_data1.Minute = 22
    ensemble_data1.Second = 39
    ensemble_data1.HSec = 10

    ensemble_data2 = EnsembleData.EnsembleData(19, 1)
    ensemble_data2.EnsembleNumber = 1
    ensemble_data2.NumBeams = 4
    ensemble_data2.NumBins = 10
    ensemble_data2.Year = 2019
    ensemble_data2.Month = 2
    ensemble_data2.Day = 19
    ensemble_data2.Hour = 10
    ensemble_data2.Minute = 23
    ensemble_data2.Second = 39
    ensemble_data2.HSec = 10

    ensemble_data3 = EnsembleData.EnsembleData(19, 1)
    ensemble_data3.EnsembleNumber = 1
    ensemble_data3.NumBeams = 4
    ensemble_data3.NumBins = 10
    ensemble_data3.Year = 2019
    ensemble_data3.Month = 2
    ensemble_data3.Day = 19
    ensemble_data3.Hour = 10
    ensemble_data3.Minute = 24
    ensemble_data3.Second = 39
    ensemble_data3.HSec = 10

    range_track1 = RangeTracking.RangeTracking()
    range_track1.NumBeams = 4
    range_track1.Range.append(38.0)
    range_track1.Range.append(39.0)
    range_track1.Range.append(40.0)
    range_track1.Range.append(41.0)

    range_track2 = RangeTracking.RangeTracking()
    range_track2.NumBeams = 4
    range_track2.Range.append(20.5)
    range_track2.Range.append(21.6)
    range_track2.Range.append(22.7)
    range_track2.Range.append(23.8)

    range_track3 = RangeTracking.RangeTracking()
    range_track3.NumBeams = 4
    range_track3.Range.append(33.1)
    range_track3.Range.append(34.2)
    range_track3.Range.append(35.3)
    range_track3.Range.append(36.4)


    ensemble1 = Ensemble.Ensemble()
    ensemble1.AddAncillaryData(ancillary_data1)
    ensemble1.AddEnsembleData(ensemble_data1)
    ensemble1.AddRangeTracking(range_track1)

    ensemble2 = Ensemble.Ensemble()
    ensemble2.AddAncillaryData(ancillary_data2)
    ensemble2.AddEnsembleData(ensemble_data2)
    ensemble2.AddRangeTracking(range_track2)

    ensemble3 = Ensemble.Ensemble()
    ensemble3.AddAncillaryData(ancillary_data3)
    ensemble3.AddEnsembleData(ensemble_data3)
    ensemble3.AddRangeTracking(range_track3)

    codec.add(ensemble1)
    codec.add(ensemble2)
    codec.add(ensemble3)


def waves_rcv(self, file_name):

    assert True == os.path.isfile(file_name)

    # Read in the MATLAB file
    mat_data = sio.loadmat(file_name)

    # Lat and Lon
    assert 32.0 == mat_data['lat'][0][0]
    assert 118.0 == mat_data['lon'][0][0]

    # Wave Cell Depths
    assert 6.0 == mat_data['whv'][0][0]
    assert 7.0 == mat_data['whv'][0][1]
    assert 8.0 == mat_data['whv'][0][2]

    # First Ensemble Time
    assert 212353954335.1 == mat_data['wft'][0][0]

    # Time between Ensembles
    assert 60.0 == mat_data['wdt'][0][0]

    # Pressure Sensor Height
    assert 30 == mat_data['whp'][0][0]

    # Heading
    assert 22.0 == mat_data['whg'][0][0]
    assert 23.0 == mat_data['whg'][1][0]
    assert 24.0 == mat_data['whg'][2][0]

    # Pitch
    assert 10.0 == mat_data['wph'][0][0]
    assert 13.0 == mat_data['wph'][1][0]
    assert 14.0 == mat_data['wph'][2][0]

    # Roll
    assert 1.0 == mat_data['wrl'][0][0]
    assert 3.0 == mat_data['wrl'][1][0]
    assert 4.0 == mat_data['wrl'][2][0]

    # Pressure
    assert 30.2 == pytest.approx(mat_data['wps'][0][0], 0.1)
    assert 33.2 == pytest.approx(mat_data['wps'][1][0], 0.1)
    assert 34.2 == pytest.approx(mat_data['wps'][2][0], 0.1)

    # Water Temp
    assert 23.5 == pytest.approx(mat_data['wts'][0][0], 0.1)
    assert 26.5 == pytest.approx(mat_data['wts'][1][0], 0.1)
    assert 27.5 == pytest.approx(mat_data['wts'][2][0], 0.1)

    # Average Range and Pressure
    assert 37.64 == pytest.approx(mat_data['wah'][0][0], 0.1)
    assert 24.36 == pytest.approx(mat_data['wah'][1][0], 0.1)
    assert 34.64 == pytest.approx(mat_data['wah'][2][0], 0.1)


