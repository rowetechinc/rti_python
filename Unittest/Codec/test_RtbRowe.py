import pytest
from rti_python.Codecs.RtbRowe import RtbRowe


def test_RtbRowe():
    file_path = r"C:\Users\rico\Documents\data\Vault\01200000000000000000000000000857\RTI_20191101112241_00857.bin"
    rowe = RtbRowe(file_name=file_path)
    assert len(rowe.ens) == 233


def test_RtbRowe_pd0():
    file_path = r"C:\Users\rico\Documents\data\Vault\01200000000000000000000000000857\RTI_20191101112241_00857.bin"
    rowe = RtbRowe(file_name=file_path, use_pd0_format=True)
    assert len(rowe.ens) == 233

