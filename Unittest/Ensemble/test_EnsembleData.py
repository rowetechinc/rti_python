import pytest
import datetime
import re
from rti_python.Ensemble.Ensemble import Ensemble
from rti_python.Ensemble.EnsembleData import EnsembleData


def test_generate_header():

    value_type = 20             # Int
    num_elements = 19           # 19 elements
    element_multiplier = 1      # no multiplier
    imag = 0                    # NOT USED
    name_length = 8             # Length of name
    name = "E000008\0"          # Ensemble Dataset name

    header = Ensemble.generate_header(value_type,
                                      num_elements,
                                      element_multiplier,
                                      imag,
                                      name_length,
                                      name)

    # Value type
    assert 0x14 == header[0]
    assert 0x0 == header[1]
    assert 0x0 == header[2]
    assert 0x0 == header[3]

    # Num Elements
    assert 0x13 == header[4]
    assert 0x0 == header[5]
    assert 0x0 == header[6]
    assert 0x0 == header[7]

    # Element Multiplier
    assert 0x1 == header[8]
    assert 0x0 == header[9]
    assert 0x0 == header[10]
    assert 0x0 == header[11]

    # Imag
    assert 0x0 == header[12]
    assert 0x0 == header[13]
    assert 0x0 == header[14]
    assert 0x0 == header[15]

    # Name Length
    assert 0x8 == header[16]
    assert 0x0 == header[17]
    assert 0x0 == header[18]
    assert 0x0 == header[19]

    # Name
    assert ord('E') == header[20]
    assert ord('0') == header[21]
    assert ord('0') == header[22]
    assert ord('0') == header[23]
    assert ord('0') == header[24]
    assert ord('0') == header[25]
    assert ord('8') == header[26]
    assert ord('\0') == header[27]


def test_ensembledata():
    ens = EnsembleData()
    ens.EnsembleNumber = 2668
    ens.NumBins = 37
    ens.NumBeams = 4
    ens.DesiredPingCount = 45
    ens.ActualPingCount = 46
    ens.SerialNumber = "01H00000000000000000000000999999"
    ens.SysFirmwareMajor = 2
    ens.SysFirmwareMinor = 11
    ens.SysFirmwareRevision = 5
    ens.SysFirmwareSubsystemCode = "A"
    ens.SubsystemConfig = 3
    ens.Status = 0x0120
    ens.Year = 2019
    ens.Month = 3
    ens.Day = 9
    ens.Hour = 12
    ens.Minute = 23
    ens.Second = 24
    ens.HSec = 33

    # Populate data

    result = ens.encode()

    # Value type
    assert 0x14 == result[0]
    assert 0x0 == result[1]
    assert 0x0 == result[2]
    assert 0x0 == result[3]

    # Num Elements
    assert 0x13 == result[4]
    assert 0x0 == result[5]
    assert 0x0 == result[6]
    assert 0x0 == result[7]

    # Element Multiplier
    assert 0x1 == result[8]
    assert 0x0 == result[9]
    assert 0x0 == result[10]
    assert 0x0 == result[11]

    # Imag
    assert 0x0 == result[12]
    assert 0x0 == result[13]
    assert 0x0 == result[14]
    assert 0x0 == result[15]

    # Name Length
    assert 0x8 == result[16]
    assert 0x0 == result[17]
    assert 0x0 == result[18]
    assert 0x0 == result[19]

    # Name
    assert ord('E') == result[20]
    assert ord('0') == result[21]
    assert ord('0') == result[22]
    assert ord('0') == result[23]
    assert ord('0') == result[24]
    assert ord('0') == result[25]
    assert ord('8') == result[26]
    assert ord('\0') == result[27]

    # Length
    assert len(result) == (23 * Ensemble.BytesInInt32) + 28

    # Data
    # Ensemble Number
    assert Ensemble.int32_to_bytes(2668)[0] == result[28]
    assert Ensemble.int32_to_bytes(2668)[1] == result[29]
    assert Ensemble.int32_to_bytes(2668)[2] == result[30]
    assert Ensemble.int32_to_bytes(2668)[3] == result[31]

    # Num Bins
    assert Ensemble.int32_to_bytes(37)[0] == result[32]
    assert Ensemble.int32_to_bytes(37)[1] == result[33]
    assert Ensemble.int32_to_bytes(37)[2] == result[34]
    assert Ensemble.int32_to_bytes(37)[3] == result[35]

    # Num Beams
    assert Ensemble.int32_to_bytes(4)[0] == result[36]
    assert Ensemble.int32_to_bytes(4)[1] == result[37]
    assert Ensemble.int32_to_bytes(4)[2] == result[38]
    assert Ensemble.int32_to_bytes(4)[3] == result[39]

    # Desired Ping Count
    assert Ensemble.int32_to_bytes(45)[0] == result[40]
    assert Ensemble.int32_to_bytes(45)[1] == result[41]
    assert Ensemble.int32_to_bytes(45)[2] == result[42]
    assert Ensemble.int32_to_bytes(45)[3] == result[43]

    # Actual Ping Count
    assert Ensemble.int32_to_bytes(46)[0] == result[44]
    assert Ensemble.int32_to_bytes(46)[1] == result[45]
    assert Ensemble.int32_to_bytes(46)[2] == result[46]
    assert Ensemble.int32_to_bytes(46)[3] == result[47]

    # Serial Number
    serial = ens.SerialNumber.encode()
    assert serial[0] == result[48]
    assert serial[1] == result[49]
    assert serial[2] == result[50]
    assert serial[3] == result[51]
    assert serial[4] == result[52]
    assert serial[5] == result[53]
    assert serial[6] == result[54]
    assert serial[7] == result[55]
    assert serial[8] == result[56]
    assert serial[9] == result[57]
    assert serial[10] == result[58]
    assert serial[11] == result[59]
    assert serial[12] == result[60]
    assert serial[13] == result[61]
    assert serial[14] == result[62]
    assert serial[15] == result[63]
    assert serial[16] == result[64]
    assert serial[17] == result[65]
    assert serial[18] == result[66]
    assert serial[19] == result[67]
    assert serial[20] == result[68]
    assert serial[21] == result[69]
    assert serial[22] == result[70]
    assert serial[23] == result[71]
    assert serial[24] == result[72]
    assert serial[25] == result[73]
    assert serial[26] == result[74]
    assert serial[27] == result[75]
    assert serial[28] == result[76]
    assert serial[29] == result[77]
    assert serial[30] == result[78]
    assert serial[31] == result[79]
    #assert "01H00000000000000000000000999999" == str(result[48:79], "UTF-8")

    # Firmware Major
    assert 2 == result[80]
    assert 11 == result[81]
    assert 5 == result[82]
    assert 65 == result[83]
    #assert "A" == str(result[83], "UTF-8")

    # Subsystem Config
    assert 0 == result[84]
    assert 0 == result[85]
    assert 0 == result[86]
    assert 3 == result[87]

    # Status
    assert Ensemble.int32_to_bytes(288)[0] == result[88]
    assert Ensemble.int32_to_bytes(288)[1] == result[89]
    assert Ensemble.int32_to_bytes(288)[2] == result[90]
    assert Ensemble.int32_to_bytes(288)[3] == result[91]

    # Year
    assert Ensemble.int32_to_bytes(2019)[0] == result[92]
    assert Ensemble.int32_to_bytes(2019)[1] == result[93]
    assert Ensemble.int32_to_bytes(2019)[2] == result[94]
    assert Ensemble.int32_to_bytes(2019)[3] == result[95]

    # Month
    assert Ensemble.int32_to_bytes(3)[0] == result[96]
    assert Ensemble.int32_to_bytes(3)[1] == result[97]
    assert Ensemble.int32_to_bytes(3)[2] == result[98]
    assert Ensemble.int32_to_bytes(3)[3] == result[99]

    # Day
    assert Ensemble.int32_to_bytes(9)[0] == result[100]
    assert Ensemble.int32_to_bytes(9)[1] == result[101]
    assert Ensemble.int32_to_bytes(9)[2] == result[102]
    assert Ensemble.int32_to_bytes(9)[3] == result[103]

    # Hour
    assert Ensemble.int32_to_bytes(12)[0] == result[104]
    assert Ensemble.int32_to_bytes(12)[1] == result[105]
    assert Ensemble.int32_to_bytes(12)[2] == result[106]
    assert Ensemble.int32_to_bytes(12)[3] == result[107]

    # Minute
    assert Ensemble.int32_to_bytes(23)[0] == result[108]
    assert Ensemble.int32_to_bytes(23)[1] == result[109]
    assert Ensemble.int32_to_bytes(23)[2] == result[110]
    assert Ensemble.int32_to_bytes(23)[3] == result[111]

    # Second
    assert Ensemble.int32_to_bytes(24)[0] == result[112]
    assert Ensemble.int32_to_bytes(24)[1] == result[113]
    assert Ensemble.int32_to_bytes(24)[2] == result[114]
    assert Ensemble.int32_to_bytes(24)[3] == result[115]

    # HSecond
    assert Ensemble.int32_to_bytes(33)[0] == result[116]
    assert Ensemble.int32_to_bytes(33)[1] == result[117]
    assert Ensemble.int32_to_bytes(33)[2] == result[118]
    assert Ensemble.int32_to_bytes(33)[3] == result[119]


def test_encode_csv():

    ens = EnsembleData()
    ens.EnsembleNumber = 2668
    ens.NumBins = 37
    ens.NumBeams = 4
    ens.DesiredPingCount = 45
    ens.ActualPingCount = 46
    ens.SerialNumber = 386
    ens.SysFirmwareMajor = 2
    ens.SysFirmwareMinor = 11
    ens.SysFirmwareRevision = 5
    ens.SysFirmwareSubsystemCode = 'A'
    ens.SubsystemConfig = 1
    ens.Status = 0x0120
    ens.Year = 2019
    ens.Month = 3
    ens.Day = 9
    ens.Hour = 12
    ens.Minute = 23
    ens.Second = 24
    ens.HSec = 33

    # Populate data

    dt = datetime.datetime.now()

    # Create CSV lines
    result = ens.encode_csv(dt, 'A', 1)

    # Check the csv data
    for line in result:
        if Ensemble.CSV_STATUS in line:
            assert bool(re.search(str(288), line))
            assert bool(re.search(str(0), line))
