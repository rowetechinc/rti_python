import pytest
import os
import scipy.io as sio
import rti_python.Codecs.WaveForceCodec as wfc
import rti_python.Ensemble.AncillaryData as AncillaryData
import rti_python.Ensemble.EnsembleData as EnsembleData
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
    ancillary_data = AncillaryData.AncillaryData(17, 1)
    ancillary_data.Heading = 22.0
    ancillary_data.Pitch = 10.0
    ancillary_data.Roll = 1.0
    ancillary_data.TransducerDepth = 30.2
    ancillary_data.WaterTemp = 23.5
    ancillary_data.BinSize = 1
    ancillary_data.FirstBinRange = 3

    ensemble_data = EnsembleData.EnsembleData(19, 1)
    ensemble_data.EnsembleNumber = 1
    ensemble_data.NumBeams = 4
    ensemble_data.NumBins = 10
    ensemble_data.Year = 2019
    ensemble_data.Month = 2
    ensemble_data.Day = 19
    ensemble_data.Hour = 10
    ensemble_data.Minute = 22
    ensemble_data.Second = 39
    ensemble_data.HSec = 10

    ensemble = Ensemble.Ensemble()
    ensemble.AddAncillaryData(ancillary_data)
    ensemble.AddEnsembleData(ensemble_data)

    for ens_cnt in range(num_ens_in_burst):
        codec.add(ensemble)


def waves_rcv(self, file_name):

    assert True == os.path.isfile(file_name)

    # Read in the MATLAB file
    mat_data = sio.loadmat(file_name)

    assert 32.0 == mat_data['lat'][0][0]
    assert 118.0 == mat_data['lon'][0][0]

    assert 6.0 == mat_data['whv'][0][0]
    assert 7.0 == mat_data['whv'][0][1]
    assert 8.0 == mat_data['whv'][0][2]

    assert 212353954335.1 == mat_data['wft'][0][0]