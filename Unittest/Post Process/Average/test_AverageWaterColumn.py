import pytest
from rti_python.Ensemble.Ensemble import Ensemble
from rti_python.Ensemble.EnsembleData import EnsembleData
from rti_python.Ensemble.BeamVelocity import BeamVelocity
from rti_python.Ensemble.InstrumentVelocity import InstrumentVelocity
from rti_python.Ensemble.EarthVelocity import EarthVelocity
from rti_python.Post_Process.Average.AverageWaterColumn import AverageWaterColumn

def test_AWC_1ens():

    ens = Ensemble()
    ensDS = EnsembleData()
    ensDS.SysFirmwareSubsystemCode = '3'
    ensDS.SubsystemConfig = '1'
    ensDS.NumBeams = 4
    ensDS.NumBins = 3
    ens.AddEnsembleData(ensDS)

    beamVel = BeamVelocity(ensDS.NumBins, ensDS.NumBeams)
    beamVel.Velocities[0][0] = 1.0
    beamVel.Velocities[0][1] = 2.0
    beamVel.Velocities[0][2] = 3.0
    beamVel.Velocities[0][3] = 4.0
    beamVel.Velocities[1][0] = 1.0
    beamVel.Velocities[1][1] = 2.0
    beamVel.Velocities[1][2] = 3.0
    beamVel.Velocities[1][3] = 4.0
    beamVel.Velocities[2][0] = 1.0
    beamVel.Velocities[2][1] = 2.0
    beamVel.Velocities[2][2] = 3.0
    beamVel.Velocities[2][3] = 4.0
    ens.AddBeamVelocity(beamVel)

    instrVel = InstrumentVelocity(ensDS.NumBins, ensDS.NumBeams)
    instrVel.Velocities[0][0] = 1.0
    instrVel.Velocities[0][1] = 2.0
    instrVel.Velocities[0][2] = 3.0
    instrVel.Velocities[0][3] = 4.0
    instrVel.Velocities[1][0] = 1.0
    instrVel.Velocities[1][1] = 2.0
    instrVel.Velocities[1][2] = 3.0
    instrVel.Velocities[1][3] = 4.0
    instrVel.Velocities[2][0] = 1.0
    instrVel.Velocities[2][1] = 2.0
    instrVel.Velocities[2][2] = 3.0
    instrVel.Velocities[2][3] = 4.0
    ens.AddInstrumentVelocity(instrVel)

    earthVel = EarthVelocity(ensDS.NumBins, ensDS.NumBeams)
    earthVel.Velocities[0][0] = 1.0
    earthVel.Velocities[0][1] = 2.0
    earthVel.Velocities[0][2] = 3.0
    earthVel.Velocities[0][3] = 4.0
    earthVel.Velocities[1][0] = 1.0
    earthVel.Velocities[1][1] = 2.0
    earthVel.Velocities[1][2] = 3.0
    earthVel.Velocities[1][3] = 4.0
    earthVel.Velocities[2][0] = 1.0
    earthVel.Velocities[2][1] = 2.0
    earthVel.Velocities[2][2] = 3.0
    earthVel.Velocities[2][3] = 4.0
    ens.AddEarthVelocity(earthVel)

    awc = AverageWaterColumn(3, '3', '1')
    awc.add_ens(ens)
    result = awc.average()

    # verify empty list
    assert not result[0]
    assert not result[1]
    assert not result[2]

def test_AWC_2ens():

    ens = Ensemble()
    ensDS = EnsembleData()
    ensDS.SysFirmwareSubsystemCode = '3'
    ensDS.SubsystemConfig = '1'
    ensDS.NumBeams = 4
    ensDS.NumBins = 3
    ens.AddEnsembleData(ensDS)

    beamVel = BeamVelocity(ensDS.NumBins, ensDS.NumBeams)
    beamVel.Velocities[0][0] = 1.0
    beamVel.Velocities[0][1] = 2.0
    beamVel.Velocities[0][2] = 3.0
    beamVel.Velocities[0][3] = 4.0
    beamVel.Velocities[1][0] = 1.0
    beamVel.Velocities[1][1] = 2.0
    beamVel.Velocities[1][2] = 3.0
    beamVel.Velocities[1][3] = 4.0
    beamVel.Velocities[2][0] = 1.0
    beamVel.Velocities[2][1] = 2.0
    beamVel.Velocities[2][2] = 3.0
    beamVel.Velocities[2][3] = 4.0
    ens.AddBeamVelocity(beamVel)

    instrVel = InstrumentVelocity(ensDS.NumBins, ensDS.NumBeams)
    instrVel.Velocities[0][0] = 1.0
    instrVel.Velocities[0][1] = 2.0
    instrVel.Velocities[0][2] = 3.0
    instrVel.Velocities[0][3] = 4.0
    instrVel.Velocities[1][0] = 1.0
    instrVel.Velocities[1][1] = 2.0
    instrVel.Velocities[1][2] = 3.0
    instrVel.Velocities[1][3] = 4.0
    instrVel.Velocities[2][0] = 1.0
    instrVel.Velocities[2][1] = 2.0
    instrVel.Velocities[2][2] = 3.0
    instrVel.Velocities[2][3] = 4.0
    ens.AddInstrumentVelocity(instrVel)

    earthVel = EarthVelocity(ensDS.NumBins, ensDS.NumBeams)
    earthVel.Velocities[0][0] = 1.0
    earthVel.Velocities[0][1] = 2.0
    earthVel.Velocities[0][2] = 3.0
    earthVel.Velocities[0][3] = 4.0
    earthVel.Velocities[1][0] = 1.0
    earthVel.Velocities[1][1] = 2.0
    earthVel.Velocities[1][2] = 3.0
    earthVel.Velocities[1][3] = 4.0
    earthVel.Velocities[2][0] = 1.0
    earthVel.Velocities[2][1] = 2.0
    earthVel.Velocities[2][2] = 3.0
    earthVel.Velocities[2][3] = 4.0
    ens.AddEarthVelocity(earthVel)

    awc = AverageWaterColumn(3, '3', '1')
    awc.add_ens(ens)
    awc.add_ens(ens)
    result = awc.average()

    # verify empty list
    assert not result[0]
    assert not result[1]
    assert not result[2]

def test_AWC_3ens():

    ens = Ensemble()
    ensDS = EnsembleData()
    ensDS.SysFirmwareSubsystemCode = '3'
    ensDS.SubsystemConfig = '1'
    ensDS.NumBeams = 4
    ensDS.NumBins = 3
    ens.AddEnsembleData(ensDS)

    beamVel = BeamVelocity(ensDS.NumBins, ensDS.NumBeams)
    beamVel.Velocities[0][0] = 1.0
    beamVel.Velocities[0][1] = 2.0
    beamVel.Velocities[0][2] = 3.0
    beamVel.Velocities[0][3] = 4.0
    beamVel.Velocities[1][0] = 1.0
    beamVel.Velocities[1][1] = 2.0
    beamVel.Velocities[1][2] = 3.0
    beamVel.Velocities[1][3] = 4.0
    beamVel.Velocities[2][0] = 1.0
    beamVel.Velocities[2][1] = 2.0
    beamVel.Velocities[2][2] = 3.0
    beamVel.Velocities[2][3] = 4.0
    ens.AddBeamVelocity(beamVel)

    instrVel = InstrumentVelocity(ensDS.NumBins, ensDS.NumBeams)
    instrVel.Velocities[0][0] = 1.0
    instrVel.Velocities[0][1] = 2.0
    instrVel.Velocities[0][2] = 3.0
    instrVel.Velocities[0][3] = 4.0
    instrVel.Velocities[1][0] = 1.0
    instrVel.Velocities[1][1] = 2.0
    instrVel.Velocities[1][2] = 3.0
    instrVel.Velocities[1][3] = 4.0
    instrVel.Velocities[2][0] = 1.0
    instrVel.Velocities[2][1] = 2.0
    instrVel.Velocities[2][2] = 3.0
    instrVel.Velocities[2][3] = 4.0
    ens.AddInstrumentVelocity(instrVel)

    earthVel = EarthVelocity(ensDS.NumBins, ensDS.NumBeams)
    earthVel.Velocities[0][0] = 1.0
    earthVel.Velocities[0][1] = 2.0
    earthVel.Velocities[0][2] = 3.0
    earthVel.Velocities[0][3] = 4.0
    earthVel.Velocities[1][0] = 1.0
    earthVel.Velocities[1][1] = 2.0
    earthVel.Velocities[1][2] = 3.0
    earthVel.Velocities[1][3] = 4.0
    earthVel.Velocities[2][0] = 1.0
    earthVel.Velocities[2][1] = 2.0
    earthVel.Velocities[2][2] = 3.0
    earthVel.Velocities[2][3] = 4.0
    ens.AddEarthVelocity(earthVel)

    awc = AverageWaterColumn(3, '3', '1')
    awc.add_ens(ens)
    awc.add_ens(ens)
    awc.add_ens(ens)
    result = awc.average()

    # verify empty list
    assert result[0]
    assert result[1]
    assert result[2]

    # Beam Results
    assert result[0][0][0] == 1.0
    assert result[0][0][1] == 2.0
    assert result[0][0][2] == 3.0
    assert result[0][0][3] == 4.0

    # Instrument Results
    assert result[1][0][0] == 1.0
    assert result[1][0][1] == 2.0
    assert result[1][0][2] == 3.0
    assert result[1][0][3] == 4.0

    # Earth Results
    assert result[2][0][0] == 1.0
    assert result[2][0][1] == 2.0
    assert result[2][0][2] == 3.0
    assert result[2][0][3] == 4.0

def test_AWC_data():

    ens = Ensemble()
    ensDS = EnsembleData()
    ensDS.SysFirmwareSubsystemCode = '3'
    ensDS.SubsystemConfig = '1'
    ensDS.NumBeams = 4
    ensDS.NumBins = 3
    ens.AddEnsembleData(ensDS)

    beamVel = BeamVelocity(ensDS.NumBins, ensDS.NumBeams)
    beamVel.Velocities[0][0] = 1.0
    beamVel.Velocities[0][1] = 2.0
    beamVel.Velocities[0][2] = 3.0
    beamVel.Velocities[0][3] = 4.0
    beamVel.Velocities[1][0] = 1.0
    beamVel.Velocities[1][1] = 2.0
    beamVel.Velocities[1][2] = 3.0
    beamVel.Velocities[1][3] = 4.0
    beamVel.Velocities[2][0] = 1.0
    beamVel.Velocities[2][1] = 2.0
    beamVel.Velocities[2][2] = 3.0
    beamVel.Velocities[2][3] = 4.0
    ens.AddBeamVelocity(beamVel)

    instrVel = InstrumentVelocity(ensDS.NumBins, ensDS.NumBeams)
    instrVel.Velocities[0][0] = 5.0
    instrVel.Velocities[0][1] = 6.0
    instrVel.Velocities[0][2] = 7.0
    instrVel.Velocities[0][3] = 8.0
    instrVel.Velocities[1][0] = 5.0
    instrVel.Velocities[1][1] = 6.0
    instrVel.Velocities[1][2] = 7.0
    instrVel.Velocities[1][3] = 8.0
    instrVel.Velocities[2][0] = 5.0
    instrVel.Velocities[2][1] = 6.0
    instrVel.Velocities[2][2] = 7.0
    instrVel.Velocities[2][3] = 8.0
    ens.AddInstrumentVelocity(instrVel)

    earthVel = EarthVelocity(ensDS.NumBins, ensDS.NumBeams)
    earthVel.Velocities[0][0] = 9.0
    earthVel.Velocities[0][1] = 10.0
    earthVel.Velocities[0][2] = 11.0
    earthVel.Velocities[0][3] = 12.0
    earthVel.Velocities[1][0] = 9.0
    earthVel.Velocities[1][1] = 10.0
    earthVel.Velocities[1][2] = 11.0
    earthVel.Velocities[1][3] = 12.0
    earthVel.Velocities[2][0] = 9.0
    earthVel.Velocities[2][1] = 10.0
    earthVel.Velocities[2][2] = 11.0
    earthVel.Velocities[2][3] = 12.0
    ens.AddEarthVelocity(earthVel)

    awc = AverageWaterColumn(3, '3', '1')
    awc.add_ens(ens)
    awc.add_ens(ens)
    awc.add_ens(ens)
    result = awc.average()

    # verify empty list
    assert result[0]
    assert result[1]
    assert result[2]

    # Beam Results
    assert result[0][0][0] == 1.0
    assert result[0][0][1] == 2.0
    assert result[0][0][2] == 3.0
    assert result[0][0][3] == 4.0

    # Instrument Results
    assert result[1][0][0] == 5.0
    assert result[1][0][1] == 6.0
    assert result[1][0][2] == 7.0
    assert result[1][0][3] == 8.0

    # Earth Results
    assert result[2][0][0] == 9.0
    assert result[2][0][1] == 10.0
    assert result[2][0][2] == 11.0
    assert result[2][0][3] == 12.0

def test_AWC_4ens():

    ens = Ensemble()
    ensDS = EnsembleData()
    ensDS.SysFirmwareSubsystemCode = '3'
    ensDS.SubsystemConfig = '1'
    ensDS.NumBeams = 4
    ensDS.NumBins = 3
    ens.AddEnsembleData(ensDS)

    beamVel = BeamVelocity(ensDS.NumBins, ensDS.NumBeams)
    beamVel.Velocities[0][0] = 1.0
    beamVel.Velocities[0][1] = 2.0
    beamVel.Velocities[0][2] = 3.0
    beamVel.Velocities[0][3] = 4.0
    beamVel.Velocities[1][0] = 1.0
    beamVel.Velocities[1][1] = 2.0
    beamVel.Velocities[1][2] = 3.0
    beamVel.Velocities[1][3] = 4.0
    beamVel.Velocities[2][0] = 1.0
    beamVel.Velocities[2][1] = 2.0
    beamVel.Velocities[2][2] = 3.0
    beamVel.Velocities[2][3] = 4.0
    ens.AddBeamVelocity(beamVel)

    instrVel = InstrumentVelocity(ensDS.NumBins, ensDS.NumBeams)
    instrVel.Velocities[0][0] = 5.0
    instrVel.Velocities[0][1] = 6.0
    instrVel.Velocities[0][2] = 7.0
    instrVel.Velocities[0][3] = 8.0
    instrVel.Velocities[1][0] = 5.0
    instrVel.Velocities[1][1] = 6.0
    instrVel.Velocities[1][2] = 7.0
    instrVel.Velocities[1][3] = 8.0
    instrVel.Velocities[2][0] = 5.0
    instrVel.Velocities[2][1] = 6.0
    instrVel.Velocities[2][2] = 7.0
    instrVel.Velocities[2][3] = 8.0
    ens.AddInstrumentVelocity(instrVel)

    earthVel = EarthVelocity(ensDS.NumBins, ensDS.NumBeams)
    earthVel.Velocities[0][0] = 9.0
    earthVel.Velocities[0][1] = 10.0
    earthVel.Velocities[0][2] = 11.0
    earthVel.Velocities[0][3] = 12.0
    earthVel.Velocities[1][0] = 9.0
    earthVel.Velocities[1][1] = 10.0
    earthVel.Velocities[1][2] = 11.0
    earthVel.Velocities[1][3] = 12.0
    earthVel.Velocities[2][0] = 9.0
    earthVel.Velocities[2][1] = 10.0
    earthVel.Velocities[2][2] = 11.0
    earthVel.Velocities[2][3] = 12.0
    ens.AddEarthVelocity(earthVel)

    ens1 = Ensemble()
    ens1DS = EnsembleData()
    ens1DS.SysFirmwareSubsystemCode = '3'
    ens1DS.SubsystemConfig = '1'
    ens1DS.NumBeams = 4
    ens1DS.NumBins = 3
    ens1.AddEnsembleData(ens1DS)

    beamVel1 = BeamVelocity(ens1DS.NumBins, ens1DS.NumBeams)
    beamVel1.Velocities[0][0] = 1.0
    beamVel1.Velocities[0][1] = 2.0
    beamVel1.Velocities[0][2] = 3.0
    beamVel1.Velocities[0][3] = 4.0
    beamVel1.Velocities[1][0] = 1.0
    beamVel1.Velocities[1][1] = 2.0
    beamVel1.Velocities[1][2] = 3.0
    beamVel1.Velocities[1][3] = 4.0
    beamVel1.Velocities[2][0] = 1.0
    beamVel1.Velocities[2][1] = 2.0
    beamVel1.Velocities[2][2] = 3.0
    beamVel1.Velocities[2][3] = 4.0
    ens1.AddBeamVelocity(beamVel1)

    instrVel1 = InstrumentVelocity(ens1DS.NumBins, ens1DS.NumBeams)
    instrVel1.Velocities[0][0] = 5.0
    instrVel1.Velocities[0][1] = 6.0
    instrVel1.Velocities[0][2] = 7.0
    instrVel1.Velocities[0][3] = 8.0
    instrVel1.Velocities[1][0] = 5.0
    instrVel1.Velocities[1][1] = 6.0
    instrVel1.Velocities[1][2] = 7.0
    instrVel1.Velocities[1][3] = 8.0
    instrVel1.Velocities[2][0] = 5.0
    instrVel1.Velocities[2][1] = 6.0
    instrVel1.Velocities[2][2] = 7.0
    instrVel1.Velocities[2][3] = 8.0
    ens1.AddInstrumentVelocity(instrVel1)

    earthVel1 = EarthVelocity(ens1DS.NumBins, ens1DS.NumBeams)
    earthVel1.Velocities[0][0] = 9.0
    earthVel1.Velocities[0][1] = 10.0
    earthVel1.Velocities[0][2] = 11.0
    earthVel1.Velocities[0][3] = 12.0
    earthVel1.Velocities[1][0] = 9.0
    earthVel1.Velocities[1][1] = 10.0
    earthVel1.Velocities[1][2] = 11.0
    earthVel1.Velocities[1][3] = 12.0
    earthVel1.Velocities[2][0] = 9.0
    earthVel1.Velocities[2][1] = 10.0
    earthVel1.Velocities[2][2] = 11.0
    earthVel1.Velocities[2][3] = 12.0
    ens1.AddEarthVelocity(earthVel1)

    awc = AverageWaterColumn(3, '3', '1')
    awc.add_ens(ens)
    awc.add_ens(ens)
    awc.add_ens(ens)
    awc.add_ens(ens1)
    result = awc.average()

    # verify not empty list
    assert result[0]
    assert result[1]
    assert result[2]

    # Beam Results
    assert result[0][0][0] == 1.0
    assert result[0][0][1] == 2.0
    assert result[0][0][2] == 3.0
    assert result[0][0][3] == 4.0

    # Instrument Results
    assert result[1][0][0] == 5.0
    assert result[1][0][1] == 6.0
    assert result[1][0][2] == 7.0
    assert result[1][0][3] == 8.0

    # Earth Results
    assert result[2][0][0] == 9.0
    assert result[2][0][1] == 10.0
    assert result[2][0][2] == 11.0
    assert result[2][0][3] == 12.0

def test_AWC_4ens_new_data():

    ens = Ensemble()
    ensDS = EnsembleData()
    ensDS.SysFirmwareSubsystemCode = '3'
    ensDS.SubsystemConfig = '1'
    ensDS.NumBeams = 4
    ensDS.NumBins = 3
    ens.AddEnsembleData(ensDS)

    beamVel = BeamVelocity(ensDS.NumBins, ensDS.NumBeams)
    beamVel.Velocities[0][0] = 1.0
    beamVel.Velocities[0][1] = 2.0
    beamVel.Velocities[0][2] = 3.0
    beamVel.Velocities[0][3] = 4.0
    beamVel.Velocities[1][0] = 1.0
    beamVel.Velocities[1][1] = 2.0
    beamVel.Velocities[1][2] = 3.0
    beamVel.Velocities[1][3] = 4.0
    beamVel.Velocities[2][0] = 1.0
    beamVel.Velocities[2][1] = 2.0
    beamVel.Velocities[2][2] = 3.0
    beamVel.Velocities[2][3] = 4.0
    ens.AddBeamVelocity(beamVel)

    instrVel = InstrumentVelocity(ensDS.NumBins, ensDS.NumBeams)
    instrVel.Velocities[0][0] = 5.0
    instrVel.Velocities[0][1] = 6.0
    instrVel.Velocities[0][2] = 7.0
    instrVel.Velocities[0][3] = 8.0
    instrVel.Velocities[1][0] = 5.0
    instrVel.Velocities[1][1] = 6.0
    instrVel.Velocities[1][2] = 7.0
    instrVel.Velocities[1][3] = 8.0
    instrVel.Velocities[2][0] = 5.0
    instrVel.Velocities[2][1] = 6.0
    instrVel.Velocities[2][2] = 7.0
    instrVel.Velocities[2][3] = 8.0
    ens.AddInstrumentVelocity(instrVel)

    earthVel = EarthVelocity(ensDS.NumBins, ensDS.NumBeams)
    earthVel.Velocities[0][0] = 9.0
    earthVel.Velocities[0][1] = 10.0
    earthVel.Velocities[0][2] = 11.0
    earthVel.Velocities[0][3] = 12.0
    earthVel.Velocities[1][0] = 9.0
    earthVel.Velocities[1][1] = 10.0
    earthVel.Velocities[1][2] = 11.0
    earthVel.Velocities[1][3] = 12.0
    earthVel.Velocities[2][0] = 9.0
    earthVel.Velocities[2][1] = 10.0
    earthVel.Velocities[2][2] = 11.0
    earthVel.Velocities[2][3] = 12.0
    ens.AddEarthVelocity(earthVel)

    ens1 = Ensemble()
    ens1DS = EnsembleData()
    ens1DS.SysFirmwareSubsystemCode = '3'
    ens1DS.SubsystemConfig = '1'
    ens1DS.NumBeams = 4
    ens1DS.NumBins = 3
    ens1.AddEnsembleData(ens1DS)

    beamVel1 = BeamVelocity(ens1DS.NumBins, ens1DS.NumBeams)
    beamVel1.Velocities[0][0] = 11.0
    beamVel1.Velocities[0][1] = 21.0
    beamVel1.Velocities[0][2] = 31.0
    beamVel1.Velocities[0][3] = 41.0
    beamVel1.Velocities[1][0] = 11.0
    beamVel1.Velocities[1][1] = 21.0
    beamVel1.Velocities[1][2] = 31.0
    beamVel1.Velocities[1][3] = 41.0
    beamVel1.Velocities[2][0] = 11.0
    beamVel1.Velocities[2][1] = 21.0
    beamVel1.Velocities[2][2] = 31.0
    beamVel1.Velocities[2][3] = 41.0
    ens1.AddBeamVelocity(beamVel1)

    instrVel1 = InstrumentVelocity(ens1DS.NumBins, ens1DS.NumBeams)
    instrVel1.Velocities[0][0] = 51.0
    instrVel1.Velocities[0][1] = 61.0
    instrVel1.Velocities[0][2] = 71.0
    instrVel1.Velocities[0][3] = 81.0
    instrVel1.Velocities[1][0] = 51.0
    instrVel1.Velocities[1][1] = 61.0
    instrVel1.Velocities[1][2] = 71.0
    instrVel1.Velocities[1][3] = 81.0
    instrVel1.Velocities[2][0] = 51.0
    instrVel1.Velocities[2][1] = 61.0
    instrVel1.Velocities[2][2] = 71.0
    instrVel1.Velocities[2][3] = 81.0
    ens1.AddInstrumentVelocity(instrVel1)

    earthVel1 = EarthVelocity(ens1DS.NumBins, ens1DS.NumBeams)
    earthVel1.Velocities[0][0] = 91.0
    earthVel1.Velocities[0][1] = 101.0
    earthVel1.Velocities[0][2] = 111.0
    earthVel1.Velocities[0][3] = 121.0
    earthVel1.Velocities[1][0] = 91.0
    earthVel1.Velocities[1][1] = 101.0
    earthVel1.Velocities[1][2] = 111.0
    earthVel1.Velocities[1][3] = 121.0
    earthVel1.Velocities[2][0] = 91.0
    earthVel1.Velocities[2][1] = 101.0
    earthVel1.Velocities[2][2] = 111.0
    earthVel1.Velocities[2][3] = 121.0
    ens1.AddEarthVelocity(earthVel1)

    awc = AverageWaterColumn(3, '3', '1')
    awc.add_ens(ens)
    awc.add_ens(ens)
    awc.add_ens(ens)
    awc.add_ens(ens1)
    result = awc.average()

    # verify not empty list
    assert result[0]
    assert result[1]
    assert result[2]

    # Beam Results
    assert result[0][0][0] == pytest.approx(4.33, 0.01)
    assert result[0][0][1] == pytest.approx(8.33, 0.01)
    assert result[0][0][2] == pytest.approx(12.33, 0.01)
    assert result[0][0][3] == pytest.approx(16.33, 0.01)

    # Instrument Results
    assert result[1][0][0] == pytest.approx(16.5, 0.01)
    assert result[1][0][1] == pytest.approx(19.75, 0.01)
    assert result[1][0][2] == pytest.approx(23.0, 0.01)
    assert result[1][0][3] == pytest.approx(26.25, 0.01)

    # Earth Results
    assert result[2][0][0] == pytest.approx(29.5, 0.01)
    assert result[2][0][1] == pytest.approx(32.75, 0.01)
    assert result[2][0][2] == pytest.approx(36.0, 0.01)
    assert result[2][0][3] == pytest.approx(39.25, 0.01)

def test_AWC_change_beam():

    ens = Ensemble()
    ensDS = EnsembleData()
    ensDS.SysFirmwareSubsystemCode = '3'
    ensDS.SubsystemConfig = '1'
    ensDS.NumBeams = 4
    ensDS.NumBins = 3
    ens.AddEnsembleData(ensDS)

    beamVel = BeamVelocity(ensDS.NumBins, ensDS.NumBeams)
    beamVel.Velocities[0][0] = 1.0
    beamVel.Velocities[0][1] = 2.0
    beamVel.Velocities[0][2] = 3.0
    beamVel.Velocities[0][3] = 4.0
    beamVel.Velocities[1][0] = 1.0
    beamVel.Velocities[1][1] = 2.0
    beamVel.Velocities[1][2] = 3.0
    beamVel.Velocities[1][3] = 4.0
    beamVel.Velocities[2][0] = 1.0
    beamVel.Velocities[2][1] = 2.0
    beamVel.Velocities[2][2] = 3.0
    beamVel.Velocities[2][3] = 4.0
    ens.AddBeamVelocity(beamVel)

    instrVel = InstrumentVelocity(ensDS.NumBins, ensDS.NumBeams)
    instrVel.Velocities[0][0] = 5.0
    instrVel.Velocities[0][1] = 6.0
    instrVel.Velocities[0][2] = 7.0
    instrVel.Velocities[0][3] = 8.0
    instrVel.Velocities[1][0] = 5.0
    instrVel.Velocities[1][1] = 6.0
    instrVel.Velocities[1][2] = 7.0
    instrVel.Velocities[1][3] = 8.0
    instrVel.Velocities[2][0] = 5.0
    instrVel.Velocities[2][1] = 6.0
    instrVel.Velocities[2][2] = 7.0
    instrVel.Velocities[2][3] = 8.0
    ens.AddInstrumentVelocity(instrVel)

    earthVel = EarthVelocity(ensDS.NumBins, ensDS.NumBeams)
    earthVel.Velocities[0][0] = 9.0
    earthVel.Velocities[0][1] = 10.0
    earthVel.Velocities[0][2] = 11.0
    earthVel.Velocities[0][3] = 12.0
    earthVel.Velocities[1][0] = 9.0
    earthVel.Velocities[1][1] = 10.0
    earthVel.Velocities[1][2] = 11.0
    earthVel.Velocities[1][3] = 12.0
    earthVel.Velocities[2][0] = 9.0
    earthVel.Velocities[2][1] = 10.0
    earthVel.Velocities[2][2] = 11.0
    earthVel.Velocities[2][3] = 12.0
    ens.AddEarthVelocity(earthVel)

    ens1 = Ensemble()
    ens1DS = EnsembleData()
    ens1DS.SysFirmwareSubsystemCode = '3'
    ens1DS.SubsystemConfig = '1'
    ens1DS.NumBeams = 1
    ens1DS.NumBins = 3
    ens1.AddEnsembleData(ens1DS)

    beamVel1 = BeamVelocity(ens1DS.NumBins, ens1DS.NumBeams)
    beamVel1.Velocities[0][0] = 11.0
    beamVel1.Velocities[1][0] = 11.0
    beamVel1.Velocities[2][0] = 11.0
    ens1.AddBeamVelocity(beamVel1)

    instrVel1 = InstrumentVelocity(ens1DS.NumBins, ens1DS.NumBeams)
    instrVel1.Velocities[0][0] = 51.0
    instrVel1.Velocities[1][0] = 51.0
    instrVel1.Velocities[2][0] = 51.0
    ens1.AddInstrumentVelocity(instrVel1)

    earthVel1 = EarthVelocity(ens1DS.NumBins, ens1DS.NumBeams)
    earthVel1.Velocities[0][0] = 91.0
    earthVel1.Velocities[1][0] = 91.0
    earthVel1.Velocities[2][0] = 91.0
    ens1.AddEarthVelocity(earthVel1)

    awc = AverageWaterColumn(3, '3', '1')
    awc.add_ens(ens)
    awc.add_ens(ens)
    awc.add_ens(ens)
    awc.add_ens(ens1)
    result = awc.average()

    # verify empty list
    assert not result[0]
    assert not result[1]
    assert not result[2]

def test_AWC_change_ss_code():

    ens = Ensemble()
    ensDS = EnsembleData()
    ensDS.SysFirmwareSubsystemCode = '3'
    ensDS.SubsystemConfig = '1'
    ensDS.NumBeams = 4
    ensDS.NumBins = 3
    ens.AddEnsembleData(ensDS)

    beamVel = BeamVelocity(ensDS.NumBins, ensDS.NumBeams)
    beamVel.Velocities[0][0] = 1.0
    beamVel.Velocities[0][1] = 2.0
    beamVel.Velocities[0][2] = 3.0
    beamVel.Velocities[0][3] = 4.0
    beamVel.Velocities[1][0] = 1.0
    beamVel.Velocities[1][1] = 2.0
    beamVel.Velocities[1][2] = 3.0
    beamVel.Velocities[1][3] = 4.0
    beamVel.Velocities[2][0] = 1.0
    beamVel.Velocities[2][1] = 2.0
    beamVel.Velocities[2][2] = 3.0
    beamVel.Velocities[2][3] = 4.0
    ens.AddBeamVelocity(beamVel)

    instrVel = InstrumentVelocity(ensDS.NumBins, ensDS.NumBeams)
    instrVel.Velocities[0][0] = 5.0
    instrVel.Velocities[0][1] = 6.0
    instrVel.Velocities[0][2] = 7.0
    instrVel.Velocities[0][3] = 8.0
    instrVel.Velocities[1][0] = 5.0
    instrVel.Velocities[1][1] = 6.0
    instrVel.Velocities[1][2] = 7.0
    instrVel.Velocities[1][3] = 8.0
    instrVel.Velocities[2][0] = 5.0
    instrVel.Velocities[2][1] = 6.0
    instrVel.Velocities[2][2] = 7.0
    instrVel.Velocities[2][3] = 8.0
    ens.AddInstrumentVelocity(instrVel)

    earthVel = EarthVelocity(ensDS.NumBins, ensDS.NumBeams)
    earthVel.Velocities[0][0] = 9.0
    earthVel.Velocities[0][1] = 10.0
    earthVel.Velocities[0][2] = 11.0
    earthVel.Velocities[0][3] = 12.0
    earthVel.Velocities[1][0] = 9.0
    earthVel.Velocities[1][1] = 10.0
    earthVel.Velocities[1][2] = 11.0
    earthVel.Velocities[1][3] = 12.0
    earthVel.Velocities[2][0] = 9.0
    earthVel.Velocities[2][1] = 10.0
    earthVel.Velocities[2][2] = 11.0
    earthVel.Velocities[2][3] = 12.0
    ens.AddEarthVelocity(earthVel)

    ens1 = Ensemble()
    ens1DS = EnsembleData()
    ens1DS.SysFirmwareSubsystemCode = '3'
    ens1DS.SubsystemConfig = '2'
    ens1DS.NumBeams = 4
    ens1DS.NumBins = 3
    ens1.AddEnsembleData(ens1DS)

    beamVel1 = BeamVelocity(ens1DS.NumBins, ens1DS.NumBeams)
    beamVel1.Velocities[0][0] = 11.0
    beamVel1.Velocities[0][1] = 21.0
    beamVel1.Velocities[0][2] = 31.0
    beamVel1.Velocities[0][3] = 41.0
    beamVel1.Velocities[1][0] = 11.0
    beamVel1.Velocities[1][1] = 21.0
    beamVel1.Velocities[1][2] = 31.0
    beamVel1.Velocities[1][3] = 41.0
    beamVel1.Velocities[2][0] = 11.0
    beamVel1.Velocities[2][1] = 21.0
    beamVel1.Velocities[2][2] = 31.0
    beamVel1.Velocities[2][3] = 41.0
    ens1.AddBeamVelocity(beamVel1)

    instrVel1 = InstrumentVelocity(ens1DS.NumBins, ens1DS.NumBeams)
    instrVel1.Velocities[0][0] = 51.0
    instrVel1.Velocities[0][1] = 61.0
    instrVel1.Velocities[0][2] = 71.0
    instrVel1.Velocities[0][3] = 81.0
    instrVel1.Velocities[1][0] = 51.0
    instrVel1.Velocities[1][1] = 61.0
    instrVel1.Velocities[1][2] = 71.0
    instrVel1.Velocities[1][3] = 81.0
    instrVel1.Velocities[2][0] = 51.0
    instrVel1.Velocities[2][1] = 61.0
    instrVel1.Velocities[2][2] = 71.0
    instrVel1.Velocities[2][3] = 81.0
    ens1.AddInstrumentVelocity(instrVel1)

    earthVel1 = EarthVelocity(ens1DS.NumBins, ens1DS.NumBeams)
    earthVel1.Velocities[0][0] = 91.0
    earthVel1.Velocities[0][1] = 101.0
    earthVel1.Velocities[0][2] = 111.0
    earthVel1.Velocities[0][3] = 121.0
    earthVel1.Velocities[1][0] = 91.0
    earthVel1.Velocities[1][1] = 101.0
    earthVel1.Velocities[1][2] = 111.0
    earthVel1.Velocities[1][3] = 121.0
    earthVel1.Velocities[2][0] = 91.0
    earthVel1.Velocities[2][1] = 101.0
    earthVel1.Velocities[2][2] = 111.0
    earthVel1.Velocities[2][3] = 121.0
    ens1.AddEarthVelocity(earthVel1)

    awc = AverageWaterColumn(3, '3', '1')
    awc.add_ens(ens)
    awc.add_ens(ens)
    awc.add_ens(ens)
    awc.add_ens(ens1)
    result = awc.average()

    # verify not empty list
    assert result[0]
    assert result[1]
    assert result[2]

    # Beam Results
    assert result[0][0][0] == 1.0
    assert result[0][0][1] == 2.0
    assert result[0][0][2] == 3.0
    assert result[0][0][3] == 4.0

    # Instrument Results
    assert result[1][0][0] == 5.0
    assert result[1][0][1] == 6.0
    assert result[1][0][2] == 7.0
    assert result[1][0][3] == 8.0

    # Earth Results
    assert result[2][0][0] == 9.0
    assert result[2][0][1] == 10.0
    assert result[2][0][2] == 11.0
    assert result[2][0][3] == 12.0

def test_AWC_change_ss_config():

    ens = Ensemble()
    ensDS = EnsembleData()
    ensDS.SysFirmwareSubsystemCode = '3'
    ensDS.SubsystemConfig = '1'
    ensDS.NumBeams = 4
    ensDS.NumBins = 3
    ens.AddEnsembleData(ensDS)

    beamVel = BeamVelocity(ensDS.NumBins, ensDS.NumBeams)
    beamVel.Velocities[0][0] = 1.0
    beamVel.Velocities[0][1] = 2.0
    beamVel.Velocities[0][2] = 3.0
    beamVel.Velocities[0][3] = 4.0
    beamVel.Velocities[1][0] = 1.0
    beamVel.Velocities[1][1] = 2.0
    beamVel.Velocities[1][2] = 3.0
    beamVel.Velocities[1][3] = 4.0
    beamVel.Velocities[2][0] = 1.0
    beamVel.Velocities[2][1] = 2.0
    beamVel.Velocities[2][2] = 3.0
    beamVel.Velocities[2][3] = 4.0
    ens.AddBeamVelocity(beamVel)

    instrVel = InstrumentVelocity(ensDS.NumBins, ensDS.NumBeams)
    instrVel.Velocities[0][0] = 5.0
    instrVel.Velocities[0][1] = 6.0
    instrVel.Velocities[0][2] = 7.0
    instrVel.Velocities[0][3] = 8.0
    instrVel.Velocities[1][0] = 5.0
    instrVel.Velocities[1][1] = 6.0
    instrVel.Velocities[1][2] = 7.0
    instrVel.Velocities[1][3] = 8.0
    instrVel.Velocities[2][0] = 5.0
    instrVel.Velocities[2][1] = 6.0
    instrVel.Velocities[2][2] = 7.0
    instrVel.Velocities[2][3] = 8.0
    ens.AddInstrumentVelocity(instrVel)

    earthVel = EarthVelocity(ensDS.NumBins, ensDS.NumBeams)
    earthVel.Velocities[0][0] = 9.0
    earthVel.Velocities[0][1] = 10.0
    earthVel.Velocities[0][2] = 11.0
    earthVel.Velocities[0][3] = 12.0
    earthVel.Velocities[1][0] = 9.0
    earthVel.Velocities[1][1] = 10.0
    earthVel.Velocities[1][2] = 11.0
    earthVel.Velocities[1][3] = 12.0
    earthVel.Velocities[2][0] = 9.0
    earthVel.Velocities[2][1] = 10.0
    earthVel.Velocities[2][2] = 11.0
    earthVel.Velocities[2][3] = 12.0
    ens.AddEarthVelocity(earthVel)

    ens1 = Ensemble()
    ens1DS = EnsembleData()
    ens1DS.SysFirmwareSubsystemCode = '4'
    ens1DS.SubsystemConfig = '1'
    ens1DS.NumBeams = 4
    ens1DS.NumBins = 3
    ens1.AddEnsembleData(ens1DS)

    beamVel1 = BeamVelocity(ens1DS.NumBins, ens1DS.NumBeams)
    beamVel1.Velocities[0][0] = 11.0
    beamVel1.Velocities[0][1] = 21.0
    beamVel1.Velocities[0][2] = 31.0
    beamVel1.Velocities[0][3] = 41.0
    beamVel1.Velocities[1][0] = 11.0
    beamVel1.Velocities[1][1] = 21.0
    beamVel1.Velocities[1][2] = 31.0
    beamVel1.Velocities[1][3] = 41.0
    beamVel1.Velocities[2][0] = 11.0
    beamVel1.Velocities[2][1] = 21.0
    beamVel1.Velocities[2][2] = 31.0
    beamVel1.Velocities[2][3] = 41.0
    ens1.AddBeamVelocity(beamVel1)

    instrVel1 = InstrumentVelocity(ens1DS.NumBins, ens1DS.NumBeams)
    instrVel1.Velocities[0][0] = 51.0
    instrVel1.Velocities[0][1] = 61.0
    instrVel1.Velocities[0][2] = 71.0
    instrVel1.Velocities[0][3] = 81.0
    instrVel1.Velocities[1][0] = 51.0
    instrVel1.Velocities[1][1] = 61.0
    instrVel1.Velocities[1][2] = 71.0
    instrVel1.Velocities[1][3] = 81.0
    instrVel1.Velocities[2][0] = 51.0
    instrVel1.Velocities[2][1] = 61.0
    instrVel1.Velocities[2][2] = 71.0
    instrVel1.Velocities[2][3] = 81.0
    ens1.AddInstrumentVelocity(instrVel1)

    earthVel1 = EarthVelocity(ens1DS.NumBins, ens1DS.NumBeams)
    earthVel1.Velocities[0][0] = 91.0
    earthVel1.Velocities[0][1] = 101.0
    earthVel1.Velocities[0][2] = 111.0
    earthVel1.Velocities[0][3] = 121.0
    earthVel1.Velocities[1][0] = 91.0
    earthVel1.Velocities[1][1] = 101.0
    earthVel1.Velocities[1][2] = 111.0
    earthVel1.Velocities[1][3] = 121.0
    earthVel1.Velocities[2][0] = 91.0
    earthVel1.Velocities[2][1] = 101.0
    earthVel1.Velocities[2][2] = 111.0
    earthVel1.Velocities[2][3] = 121.0
    ens1.AddEarthVelocity(earthVel1)

    awc = AverageWaterColumn(3, '3', '1')
    awc.add_ens(ens)
    awc.add_ens(ens)
    awc.add_ens(ens)
    awc.add_ens(ens1)
    result = awc.average()

    # verify not empty list
    assert result[0]
    assert result[1]
    assert result[2]

    # Beam Results
    assert result[0][0][0] == 1.0
    assert result[0][0][1] == 2.0
    assert result[0][0][2] == 3.0
    assert result[0][0][3] == 4.0

    # Instrument Results
    assert result[1][0][0] == 5.0
    assert result[1][0][1] == 6.0
    assert result[1][0][2] == 7.0
    assert result[1][0][3] == 8.0

    # Earth Results
    assert result[2][0][0] == 9.0
    assert result[2][0][1] == 10.0
    assert result[2][0][2] == 11.0
    assert result[2][0][3] == 12.0




