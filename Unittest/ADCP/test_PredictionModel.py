import ADCP.Predictor.Power
import ADCP.Predictor.Range
import ADCP.Predictor.MaxVelocity
import ADCP.Predictor.STD
import ADCP.Predictor.DataStorage
import ADCP.AdcpCommands
import pytest


def test_calculate_power():
    _CEI_ = 1
    _DeploymentDuration_ = 30
    _Beams_ = 4
    _SystemFrequency_ = 288000
    _CWPON_ = True
    _CWPBL_ = 1
    _CWPBS_ = 4
    _CWPBN_ = 30
    _CWPBB_LagLength_ = 1
    _CWPBB_TransmitPulseType_ = ADCP.AdcpCommands.eCWPBB_TransmitPulseType.BROADBAND.value
    _CWPP_ = 9
    _CWPTBP_ = 0.5
    _CBTON_ = True
    _CBTBB_TransmitPulseType_ = ADCP.AdcpCommands.eCBTBB_Mode.BROADBAND_CODED.value
    _BeamAngle_ = 20
    _SpeedOfSound_ = 1490
    _SystemBootPower_ = 1.80
    _SystemWakeupTime_ = 0.40
    _SystemInitPower_ = 2.80
    _SystemInitTime_ = 0.25
    _BroadbandPower_ = True
    _SystemSavePower_ = 1.80
    _SystemSaveTime_ = 0.15
    _SystemSleepPower_ = 0.024
    _BeamDiameter_ = 0.075
    _CyclesPerElement_ = 12
    _BatteryCapacity_ = 440.0
    _BatteryDerate_ = 0.85
    _BatterySelfDischarge_ = 0.05

    result = ADCP.Predictor.Power._calculate_power(_CEI_, _DeploymentDuration_, _Beams_, _SystemFrequency_,
                                _CWPON_, _CWPBL_, _CWPBS_, _CWPBN_,
                                _CWPBB_LagLength_, _CWPBB_TransmitPulseType_,
                                _CWPP_, _CWPTBP_,
                                _CBTON_, _CBTBB_TransmitPulseType_,
                                _BeamAngle_, _SpeedOfSound_,
                                _SystemBootPower_, _SystemWakeupTime_,
                                _SystemInitPower_, _SystemInitTime_,
                                _BroadbandPower_,
                                _SystemSavePower_, _SystemSaveTime_,
                                _SystemSleepPower_,
                                _BeamDiameter_, _CyclesPerElement_)

    assert result == pytest.approx(30743.46, 0.01)

    batts = ADCP.Predictor.Power._calculate_number_batteries(result, _DeploymentDuration_, _BatteryCapacity_, _BatteryDerate_, _BatterySelfDischarge_)

    assert batts == pytest.approx(82.203, 0.01)


def test_calculate_power_kwargs():
    _CEI_ = 1
    _DeploymentDuration_ = 30
    _Beams_ = 4
    _SystemFrequency_ = 288000
    _CWPON_ = True
    _CWPBL_ = 1
    _CWPBS_ = 4
    _CWPBN_ = 30
    _CWPBB_LagLength_ = 1
    _CWPBB_TransmitPulseType_ = ADCP.AdcpCommands.eCWPBB_TransmitPulseType.BROADBAND.value
    _CWPP_ = 9
    _CWPTBP_ = 0.5
    _CBTON_ = True
    _CBTBB_TransmitPulseType_ = ADCP.AdcpCommands.eCBTBB_Mode.BROADBAND_CODED.value
    _BeamAngle_ = 20
    _SpeedOfSound_ = 1490
    _SystemBootPower_ = 1.80
    _SystemWakeupTime_ = 0.40
    _SystemInitPower_ = 2.80
    _SystemInitTime_ = 0.25
    _BroadbandPower_ = True
    _SystemSavePower_ = 1.80
    _SystemSaveTime_ = 0.15
    _SystemSleepPower_ = 0.024
    _BeamDiameter_ = 0.075
    _CyclesPerElement_ = 12
    _BatteryCapacity_ = 440.0
    _BatteryDerate_ = 0.85
    _BatterySelfDischarge_ = 0.05

    result = ADCP.Predictor.Power.calculate_power(CEI=_CEI_, DeploymentDuration=_DeploymentDuration_, Beams=_Beams_, SystemFrequency=_SystemFrequency_,
                                CWPON=_CWPON_, CWPBL=_CWPBL_, CWPBS=_CWPBS_, CWPBN=_CWPBN_,
                                CWPBB_LagLength=_CWPBB_LagLength_, CWPBB=_CWPBB_TransmitPulseType_,
                                CWPP=_CWPP_, CWPTBP=_CWPTBP_,
                                CBTON=_CBTON_, CBTBB=_CBTBB_TransmitPulseType_,
                                BeamAngle=_BeamAngle_, SpeedOfSound=_SpeedOfSound_,
                                SystemBootPower=_SystemBootPower_, SystemWakeUpTime=_SystemWakeupTime_,
                                SystemInitPower=_SystemInitPower_, SystemInitTime=_SystemInitTime_,
                                BroadbandPower=_BroadbandPower_,
                                SystemSavePower=_SystemSavePower_, SystemSaveTime=_SystemSaveTime_,
                                SystemSleepPower=_SystemSleepPower_,
                                BeamDiameter=_BeamDiameter_, CyclesPerElement=_CyclesPerElement_)

    assert result == pytest.approx(30743.46, 0.01)

    batts = ADCP.Predictor.Power.calculate_number_batteries(PowerUsage=result, DeploymentDuration=_DeploymentDuration_)

    assert batts == pytest.approx(82.203, 0.01)


def test_calculate_power_burst():
    _CEI_ = 1
    _DeploymentDuration_ = 30
    _Beams_ = 4
    _SystemFrequency_ = 288000
    _CWPON_ = True
    _CWPBL_ = 1
    _CWPBS_ = 4
    _CWPBN_ = 30
    _CWPBB_LagLength_ = 1
    _CWPBB_TransmitPulseType_ = ADCP.AdcpCommands.eCWPBB_TransmitPulseType.BROADBAND.value
    _CWPP_ = 9
    _CWPTBP_ = 0.5
    _CBTON_ = True
    _CBTBB_TransmitPulseType_ = ADCP.AdcpCommands.eCBTBB_Mode.BROADBAND_CODED.value
    _BeamAngle_ = 20
    _SpeedOfSound_ = 1490
    _SystemBootPower_ = 1.80
    _SystemWakeupTime_ = 0.40
    _SystemInitPower_ = 2.80
    _SystemInitTime_ = 0.25
    _BroadbandPower_ = True
    _SystemSavePower_ = 1.80
    _SystemSaveTime_ = 0.15
    _SystemSleepPower_ = 0.024
    _BeamDiameter_ = 0.075
    _CyclesPerElement_ = 12
    _BatteryCapacity_ = 440.0
    _BatteryDerate_ = 0.85
    _BatterySelfDischarge_ = 0.05

    result = ADCP.Predictor.Power.calculate_burst_power(CEI=_CEI_, DeploymentDuration=_DeploymentDuration_, Beams=_Beams_, SystemFrequency=_SystemFrequency_,
                                CWPON=_CWPON_, CWPBL=_CWPBL_, CWPBS=_CWPBS_, CWPBN=_CWPBN_,
                                CWPBB_LagLength=_CWPBB_LagLength_, CWPBB=_CWPBB_TransmitPulseType_,
                                CWPP=_CWPP_, CWPTBP=_CWPTBP_,
                                CBTON=_CBTON_, CBTBB=_CBTBB_TransmitPulseType_,
                                BeamAngle=_BeamAngle_, SpeedOfSound=_SpeedOfSound_,
                                SystemBootPower=_SystemBootPower_, SystemWakeUpTime=_SystemWakeupTime_,
                                SystemInitPower=_SystemInitPower_, SystemInitTime=_SystemInitTime_,
                                BroadbandPower=_BroadbandPower_,
                                SystemSavePower=_SystemSavePower_, SystemSaveTime=_SystemSaveTime_,
                                SystemSleepPower=_SystemSleepPower_,
                                BeamDiameter=_BeamDiameter_, CyclesPerElement=_CyclesPerElement_, CBI=True, CBI_BurstInterval=3600, CBI_NumEns=2036)

    assert result == pytest.approx(17395.02, 0.01)

    batts = ADCP.Predictor.Power.calculate_number_batteries(PowerUsage=result, DeploymentDuration=_DeploymentDuration_)

    assert batts == pytest.approx(46.511, 0.01)


def test_calculate_power_kwargs1():
    _CEI_ = 1
    _DeploymentDuration_ = 30
    _Beams_ = 4
    _SystemFrequency_ = 288000
    _CWPON_ = True
    _CWPBL_ = 1
    _CWPBS_ = 4
    _CWPBN_ = 30
    _CWPBB_LagLength_ = 1
    _CWPBB_TransmitPulseType_ = ADCP.AdcpCommands.eCWPBB_TransmitPulseType.BROADBAND.value
    _CWPP_ = 9
    _CWPTBP_ = 0.5
    _CBTON_ = True
    _CBTBB_TransmitPulseType_ = ADCP.AdcpCommands.eCBTBB_Mode.BROADBAND_CODED.value
    _BeamAngle_ = 20
    _SpeedOfSound_ = 1490
    _SystemBootPower_ = 1.80
    _SystemWakeupTime_ = 0.40
    _SystemInitPower_ = 2.80
    _SystemInitTime_ = 0.25
    _BroadbandPower_ = True
    _SystemSavePower_ = 1.80
    _SystemSaveTime_ = 0.15
    _SystemSleepPower_ = 0.024
    _BeamDiameter_ = 0.075
    _CyclesPerElement_ = 12
    _BatteryCapacity_ = 440.0
    _BatteryDerate_ = 0.85
    _BatterySelfDischarge_ = 0.05

    result = ADCP.Predictor.Power.calculate_power(CEI=_CEI_, DeploymentDuration=_DeploymentDuration_, Beams=_Beams_, SystemFrequency=_SystemFrequency_,
                                CWPON=_CWPON_, CWPBL=_CWPBL_, CWPBS=_CWPBS_, CWPBN=_CWPBN_,
                                CWPBB_LagLength=_CWPBB_LagLength_, CWPBB=_CWPBB_TransmitPulseType_,
                                CWPP=_CWPP_, CWPTBP=_CWPTBP_,
                                CBTON=_CBTON_, CBTBB=_CBTBB_TransmitPulseType_)

    assert result == pytest.approx(30743.46, 0.01)

    batts = ADCP.Predictor.Power.calculate_number_batteries(PowerUsage=result, DeploymentDuration=_DeploymentDuration_)

    assert batts == pytest.approx(82.203, 0.01)


def test_calculate_range_kwargs():
    _CEI_ = 1
    _DeploymentDuration_ = 30
    _Beams_ = 4
    _SystemFrequency_ = 288000
    _CWPON_ = True
    _CWPBL_ = 1
    _CWPBS_ = 4
    _CWPBN_ = 30
    _CWPBB_LagLength_ = 1
    _CWPBB_TransmitPulseType_ = ADCP.AdcpCommands.eCWPBB_TransmitPulseType.BROADBAND.value
    _CWPP_ = 9
    _CWPTBP_ = 0.5
    _CBTON_ = True
    _CBTBB_TransmitPulseType_ = ADCP.AdcpCommands.eCBTBB_Mode.BROADBAND_CODED.value
    _BeamAngle_ = 20
    _SpeedOfSound_ = 1490
    _SystemBootPower_ = 1.80
    _SystemWakeupTime_ = 0.40
    _SystemInitPower_ = 2.80
    _SystemInitTime_ = 0.25
    _BroadbandPower_ = True
    _SystemSavePower_ = 1.80
    _SystemSaveTime_ = 0.15
    _SystemSleepPower_ = 0.024
    _BeamDiameter_ = 0.075
    _CyclesPerElement_ = 12
    _BatteryCapacity_ = 440.0
    _BatteryDerate_ = 0.85
    _BatterySelfDischarge_ = 0.05

    result = ADCP.Predictor.Range.calculate_predicted_range(SystemFrequency=_SystemFrequency_,
                                CWPON=_CWPON_, CWPBL=_CWPBL_, CWPBS=_CWPBS_, CWPBN=_CWPBN_,
                                CWPBB_LagLength=_CWPBB_LagLength_, CWPBB=_CWPBB_TransmitPulseType_,
                                CWPP=_CWPP_, CWPTBP=_CWPTBP_,
                                CBTON=_CBTON_, CBTBB=_CBTBB_TransmitPulseType_,
                                BeamAngle=_BeamAngle_, SpeedOfSound=_SpeedOfSound_,
                                BroadbandPower=_BroadbandPower_,
                                BeamDiameter=_BeamDiameter_, CyclesPerElement=_CyclesPerElement_)

    assert result[0] == pytest.approx(199, 0.01)    # BT
    assert result[1] == pytest.approx(100, 0.01)    # WP
    assert result[2] == pytest.approx(5.484, 0.01)  # First Bin
    assert result[3] == pytest.approx(121, 0.01)    # Configure Range


def test_calculate_range_kwargs1():
    _CEI_ = 1
    _DeploymentDuration_ = 30
    _Beams_ = 4
    _SystemFrequency_ = 288000
    _CWPON_ = True
    _CWPBL_ = 1
    _CWPBS_ = 4
    _CWPBN_ = 30
    _CWPBB_LagLength_ = 1
    _CWPBB_TransmitPulseType_ = ADCP.AdcpCommands.eCWPBB_TransmitPulseType.BROADBAND.value
    _CWPP_ = 9
    _CWPTBP_ = 0.5
    _CBTON_ = True
    _CBTBB_TransmitPulseType_ = ADCP.AdcpCommands.eCBTBB_Mode.BROADBAND_CODED.value
    _BeamAngle_ = 20
    _SpeedOfSound_ = 1490
    _SystemBootPower_ = 1.80
    _SystemWakeupTime_ = 0.40
    _SystemInitPower_ = 2.80
    _SystemInitTime_ = 0.25
    _BroadbandPower_ = True
    _SystemSavePower_ = 1.80
    _SystemSaveTime_ = 0.15
    _SystemSleepPower_ = 0.024
    _BeamDiameter_ = 0.075
    _CyclesPerElement_ = 12
    _BatteryCapacity_ = 440.0
    _BatteryDerate_ = 0.85
    _BatterySelfDischarge_ = 0.05

    result = ADCP.Predictor.Range.calculate_predicted_range(CWPON=_CWPON_, CWPBL=_CWPBL_, CWPBS=_CWPBS_, CWPBN=_CWPBN_,
                                                            CWPBB_LagLength=_CWPBB_LagLength_,
                                                            CWPBB=_CWPBB_TransmitPulseType_,
                                                            CWPP=_CWPP_, CWPTBP=_CWPTBP_,
                                                            CBTON=_CBTON_, CBTBB=_CBTBB_TransmitPulseType_,
                                                            SystemFrequency=_SystemFrequency_)

    assert result[0] == pytest.approx(199, 0.01)    # BT
    assert result[1] == pytest.approx(100, 0.01)    # WP
    assert result[2] == pytest.approx(5.484, 0.01)  # First Bin
    assert result[3] == pytest.approx(121, 0.01)    # Configure Range

def test_calculate_max_velocity():
    _CEI_ = 1
    _DeploymentDuration_ = 30
    _Beams_ = 4
    _SystemFrequency_ = 288000
    _CWPON_ = True
    _CWPBL_ = 1
    _CWPBS_ = 4
    _CWPBN_ = 30
    _CWPBB_LagLength_ = 1
    _CWPBB_TransmitPulseType_ = ADCP.AdcpCommands.eCWPBB_TransmitPulseType.BROADBAND.value
    _CWPP_ = 9
    _CWPTBP_ = 0.5
    _CBTON_ = True
    _CBTBB_TransmitPulseType_ = ADCP.AdcpCommands.eCBTBB_Mode.BROADBAND_CODED.value
    _BeamAngle_ = 20
    _SpeedOfSound_ = 1490
    _SystemBootPower_ = 1.80
    _SystemWakeupTime_ = 0.40
    _SystemInitPower_ = 2.80
    _SystemInitTime_ = 0.25
    _BroadbandPower_ = True
    _SystemSavePower_ = 1.80
    _SystemSaveTime_ = 0.15
    _SystemSleepPower_ = 0.024
    _BeamDiameter_ = 0.075
    _CyclesPerElement_ = 12
    _BatteryCapacity_ = 440.0
    _BatteryDerate_ = 0.85
    _BatterySelfDischarge_ = 0.05

    result = ADCP.Predictor.MaxVelocity._calculate_max_velocity(_CWPBB_LagLength_,
                                                               _BeamAngle_,
                                                               _SystemFrequency_,
                                                               _SpeedOfSound_,
                                                               _CyclesPerElement_)

    assert result == pytest.approx(2.669, 0.01)


def test_calculate_max_velocity_kwargs():
    _CEI_ = 1
    _DeploymentDuration_ = 30
    _Beams_ = 4
    _SystemFrequency_ = 288000
    _CWPON_ = True
    _CWPBL_ = 1
    _CWPBS_ = 4
    _CWPBN_ = 30
    _CWPBB_LagLength_ = 1
    _CWPBB_TransmitPulseType_ = ADCP.AdcpCommands.eCWPBB_TransmitPulseType.BROADBAND.value
    _CWPP_ = 9
    _CWPTBP_ = 0.5
    _CBTON_ = True
    _CBTBB_TransmitPulseType_ = ADCP.AdcpCommands.eCBTBB_Mode.BROADBAND_CODED.value
    _BeamAngle_ = 20
    _SpeedOfSound_ = 1490
    _SystemBootPower_ = 1.80
    _SystemWakeupTime_ = 0.40
    _SystemInitPower_ = 2.80
    _SystemInitTime_ = 0.25
    _BroadbandPower_ = True
    _SystemSavePower_ = 1.80
    _SystemSaveTime_ = 0.15
    _SystemSleepPower_ = 0.024
    _BeamDiameter_ = 0.075
    _CyclesPerElement_ = 12
    _BatteryCapacity_ = 440.0
    _BatteryDerate_ = 0.85
    _BatterySelfDischarge_ = 0.05

    result = ADCP.Predictor.MaxVelocity.calculate_max_velocity(CWPBB_LagLength=_CWPBB_LagLength_,
                                                               BeamAngle=_BeamAngle_,
                                                               SystemFrequency=_SystemFrequency_,
                                                               SpeedOfSound=_SpeedOfSound_,
                                                               CyclesPerElement=_CyclesPerElement_)

    assert result == pytest.approx(2.669, 0.01)


def test_calculate_std():
    _CEI_ = 1
    _DeploymentDuration_ = 30
    _Beams_ = 4
    _SystemFrequency_ = 288000
    _CWPON_ = True
    _CWPBL_ = 1
    _CWPBS_ = 4
    _CWPBN_ = 30
    _CWPBB_LagLength_ = 1
    _CWPBB_TransmitPulseType_ = ADCP.AdcpCommands.eCWPBB_TransmitPulseType.BROADBAND.value
    _CWPP_ = 9
    _CWPTBP_ = 0.5
    _CBTON_ = True
    _CBTBB_TransmitPulseType_ = ADCP.AdcpCommands.eCBTBB_Mode.BROADBAND_CODED.value
    _BeamAngle_ = 20
    _SpeedOfSound_ = 1490
    _SystemBootPower_ = 1.80
    _SystemWakeupTime_ = 0.40
    _SystemInitPower_ = 2.80
    _SystemInitTime_ = 0.25
    _BroadbandPower_ = True
    _SystemSavePower_ = 1.80
    _SystemSaveTime_ = 0.15
    _SystemSleepPower_ = 0.024
    _BeamDiameter_ = 0.075
    _CyclesPerElement_ = 12
    _BatteryCapacity_ = 440.0
    _BatteryDerate_ = 0.85
    _BatterySelfDischarge_ = 0.05
    _SNR_ = 30
    _Beta_ = 1.0
    _NbFudge_ = 1.4

    result = ADCP.Predictor.STD._calculate_std(_CWPP_, _CWPBS_, _CWPBB_LagLength_,
                                              _BeamAngle_, _CWPBB_TransmitPulseType_,
                                              _SystemFrequency_, _SpeedOfSound_,
                                              _CyclesPerElement_,
                                              _SNR_, _Beta_, _NbFudge_)

    assert result == pytest.approx(0.01, 0.1)


def test_calculate_max_velocity_kwargs():
    _CEI_ = 1
    _DeploymentDuration_ = 30
    _Beams_ = 4
    _SystemFrequency_ = 288000
    _CWPON_ = True
    _CWPBL_ = 1
    _CWPBS_ = 4
    _CWPBN_ = 30
    _CWPBB_LagLength_ = 1
    _CWPBB_TransmitPulseType_ = ADCP.AdcpCommands.eCWPBB_TransmitPulseType.BROADBAND.value
    _CWPP_ = 9
    _CWPTBP_ = 0.5
    _CBTON_ = True
    _CBTBB_TransmitPulseType_ = ADCP.AdcpCommands.eCBTBB_Mode.BROADBAND_CODED.value
    _BeamAngle_ = 20
    _SpeedOfSound_ = 1490
    _SystemBootPower_ = 1.80
    _SystemWakeupTime_ = 0.40
    _SystemInitPower_ = 2.80
    _SystemInitTime_ = 0.25
    _BroadbandPower_ = True
    _SystemSavePower_ = 1.80
    _SystemSaveTime_ = 0.15
    _SystemSleepPower_ = 0.024
    _BeamDiameter_ = 0.075
    _CyclesPerElement_ = 12
    _BatteryCapacity_ = 440.0
    _BatteryDerate_ = 0.85
    _BatterySelfDischarge_ = 0.05
    _SNR_ = 30
    _Beta_ = 1.0
    _NbFudge_ = 1.4

    result = ADCP.Predictor.STD.calculate_std(CWPP=_CWPP_,
                                              CWPBS=_CWPBS_,
                                              CWPBB_LagLength=_CWPBB_LagLength_,
                                              BeamAngle=_BeamAngle_,
                                              CWPBB=_CWPBB_TransmitPulseType_,
                                              SystemFrequency=_SystemFrequency_,
                                              SpeedOfSound=_SpeedOfSound_,
                                              CyclesPerElement=_CyclesPerElement_,
                                              SNR=_SNR_,
                                              Beta=_Beta_,
                                              NbFudge=_NbFudge_)

    assert result == pytest.approx(0.01, 0.1)

def test_calculate_storage_size():
    _CEI_ = 1
    _DeploymentDuration_ = 30
    _Beams_ = 4
    _SystemFrequency_ = 288000
    _CWPON_ = True
    _CWPBL_ = 1
    _CWPBS_ = 4
    _CWPBN_ = 30
    _CWPBB_LagLength_ = 1
    _CWPBB_TransmitPulseType_ = ADCP.AdcpCommands.eCWPBB_TransmitPulseType.BROADBAND.value
    _CWPP_ = 9
    _CWPTBP_ = 0.5
    _CBTON_ = True
    _CBTBB_TransmitPulseType_ = ADCP.AdcpCommands.eCBTBB_Mode.BROADBAND_CODED.value
    _BeamAngle_ = 20
    _SpeedOfSound_ = 1490
    _SystemBootPower_ = 1.80
    _SystemWakeupTime_ = 0.40
    _SystemInitPower_ = 2.80
    _SystemInitTime_ = 0.25
    _BroadbandPower_ = True
    _SystemSavePower_ = 1.80
    _SystemSaveTime_ = 0.15
    _SystemSleepPower_ = 0.024
    _BeamDiameter_ = 0.075
    _CyclesPerElement_ = 12
    _BatteryCapacity_ = 440.0
    _BatteryDerate_ = 0.85
    _BatterySelfDischarge_ = 0.05
    _SNR_ = 30
    _Beta_ = 1.0
    _NbFudge_ = 1.4
    IsE0000001 = True
    IsE0000002 = True
    IsE0000003 = True
    IsE0000004 = True
    IsE0000005 = True
    IsE0000006 = True
    IsE0000007 = True
    IsE0000008 = True
    IsE0000009 = True
    IsE0000010 = True
    IsE0000011 = True
    IsE0000012 = True
    IsE0000013 = True
    IsE0000014 = True
    IsE0000015 = True
    CBI_NumEns = 2036
    CBI_BurstInterval = 3600


    result = ADCP.Predictor.DataStorage._calculate_storage_amount(_CWPBN_, _Beams_, _DeploymentDuration_, _CEI_,
                                                                 IsE0000001,
                                                                 IsE0000002,
                                                                 IsE0000003,
                                                                 IsE0000004,
                                                                 IsE0000005,
                                                                 IsE0000006,
                                                                 IsE0000007,
                                                                 IsE0000008,
                                                                 IsE0000009,
                                                                 IsE0000010,
                                                                 IsE0000011,
                                                                 IsE0000012,
                                                                 IsE0000013,
                                                                 IsE0000014,
                                                                 IsE0000015)

    assert result == pytest.approx(12151.296 * 1000000, 0.1)


    burst = ADCP.Predictor.DataStorage._calculate_burst_storage_amount(CBI_NumEns, CBI_BurstInterval, _CWPBN_, _Beams_, _DeploymentDuration_,
                                                                 IsE0000001,
                                                                 IsE0000002,
                                                                 IsE0000003,
                                                                 IsE0000004,
                                                                 IsE0000005,
                                                                 IsE0000006,
                                                                 IsE0000007,
                                                                 IsE0000008,
                                                                 IsE0000009,
                                                                 IsE0000010,
                                                                 IsE0000011,
                                                                 IsE0000012,
                                                                 IsE0000013,
                                                                 IsE0000014,
                                                                 IsE0000015)

    assert burst == pytest.approx(6.872 * 1000000000, 0.1)

def test_calculate_storage_size_kwargs():
    _CEI_ = 1
    _DeploymentDuration_ = 30
    _Beams_ = 4
    _SystemFrequency_ = 288000
    _CWPON_ = True
    _CWPBL_ = 1
    _CWPBS_ = 4
    _CWPBN_ = 30
    _CWPBB_LagLength_ = 1
    _CWPBB_TransmitPulseType_ = ADCP.AdcpCommands.eCWPBB_TransmitPulseType.BROADBAND.value
    _CWPP_ = 9
    _CWPTBP_ = 0.5
    _CBTON_ = True
    _CBTBB_TransmitPulseType_ = ADCP.AdcpCommands.eCBTBB_Mode.BROADBAND_CODED.value
    _BeamAngle_ = 20
    _SpeedOfSound_ = 1490
    _SystemBootPower_ = 1.80
    _SystemWakeupTime_ = 0.40
    _SystemInitPower_ = 2.80
    _SystemInitTime_ = 0.25
    _BroadbandPower_ = True
    _SystemSavePower_ = 1.80
    _SystemSaveTime_ = 0.15
    _SystemSleepPower_ = 0.024
    _BeamDiameter_ = 0.075
    _CyclesPerElement_ = 12
    _BatteryCapacity_ = 440.0
    _BatteryDerate_ = 0.85
    _BatterySelfDischarge_ = 0.05
    _SNR_ = 30
    _Beta_ = 1.0
    _NbFudge_ = 1.4
    IsE0000001 = True
    IsE0000002 = True
    IsE0000003 = True
    IsE0000004 = True
    IsE0000005 = True
    IsE0000006 = True
    IsE0000007 = True
    IsE0000008 = True
    IsE0000009 = True
    IsE0000010 = True
    IsE0000011 = True
    IsE0000012 = True
    IsE0000013 = True
    IsE0000014 = True
    IsE0000015 = True

    result = ADCP.Predictor.DataStorage.calculate_storage_amount(CWPBN=_CWPBN_,
                                                                 Beams=_Beams_,
                                                                 DeploymentDuration=_DeploymentDuration_,
                                                                 CEI=_CEI_,
                                                                 IsE0000001=IsE0000001,
                                                                 IsE0000002=IsE0000002,
                                                                 IsE0000003=IsE0000003,
                                                                 IsE0000004=IsE0000004,
                                                                 IsE0000005=IsE0000005,
                                                                 IsE0000006=IsE0000006,
                                                                 IsE0000007=IsE0000007,
                                                                 IsE0000008=IsE0000008,
                                                                 IsE0000009=IsE0000009,
                                                                 IsE0000010=IsE0000010,
                                                                 IsE0000011=IsE0000011,
                                                                 IsE0000012=IsE0000012,
                                                                 IsE0000013=IsE0000013,
                                                                 IsE0000014=IsE0000014,
                                                                 IsE0000015=IsE0000015)

    assert result == pytest.approx(12151.296 * 1000000, 0.1)

    burst = ADCP.Predictor.DataStorage.calculate_burst_storage_amount(CBI_NumEns=2036,
                                                                       CBI_BurstInterval=3600,
                                                                CWPBN=_CWPBN_,
                                                                 Beams=_Beams_,
                                                                 DeploymentDuration=_DeploymentDuration_,
                                                                 IsE0000001=IsE0000001,
                                                                 IsE0000002=IsE0000002,
                                                                 IsE0000003=IsE0000003,
                                                                 IsE0000004=IsE0000004,
                                                                 IsE0000005=IsE0000005,
                                                                 IsE0000006=IsE0000006,
                                                                 IsE0000007=IsE0000007,
                                                                 IsE0000008=IsE0000008,
                                                                 IsE0000009=IsE0000009,
                                                                 IsE0000010=IsE0000010,
                                                                 IsE0000011=IsE0000011,
                                                                 IsE0000012=IsE0000012,
                                                                 IsE0000013=IsE0000013,
                                                                 IsE0000014=IsE0000014,
                                                                 IsE0000015=IsE0000015)

    assert burst == pytest.approx(6.872 * 1000000000, 0.1)



