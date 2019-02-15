import pytest
import os
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
    codec = wfc.WaveForceCodec()
    codec.init(3, "", 32.0, 118.0, 3, 4, 5, 30, 4)

    # Create Ensembles
    ancillary_data = AncillaryData.AncillaryData(17, 1)
    ancillary_data.Heading = 22.0
    ancillary_data.Pitch = 10.0
    ancillary_data.Roll = 1.0
    ancillary_data.TransducerDepth = 30.2
    ancillary_data.WaterTemp = 23.5

    ensemble_data = EnsembleData.EnsembleData(19, 1)
    ensemble_data.EnsembleNumber = 1
    ensemble_data.NumBeams = 4
    ensemble_data.NumBins = 10

    ensemble = Ensemble.Ensemble()
    ensemble.AddAncillaryData(ancillary_data)
    ensemble.AddEnsembleData(ensemble_data)


    codec.add(ensemble)