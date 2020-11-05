import pytest
from rti_python.Codecs.RtbRowe import RtbRowe


def test_RtbRowe():
    file_path = r"RTI_20191101112241_00857.bin"
    rowe = RtbRowe(file_name=file_path)
    assert len(rowe.ens) == 233


def test_RtbRowe_pd0():
    file_path = r"RTI_20191101112241_00857.bin"
    rowe = RtbRowe(file_name=file_path, use_pd0_format=True)
    assert len(rowe.ens) == 233


def test_RtbRowe_Cfg():
    file_path = r"RTI_20191101112241_00857.bin"
    rowe = RtbRowe(file_name=file_path)
    assert rowe.ens[-1].Cfg.ens_num == 267
    assert rowe.ens[-1].Cfg.actual_ping_count == 1
    assert rowe.ens[-1].Cfg.bin_size == 1.0
    assert rowe.ens[-1].Cfg.blank == pytest.approx(1.5, 0.1)
    assert rowe.ens[-1].Cfg.bt_actual_ping_count == 1
    assert rowe.ens[-1].Cfg.bt_beam_mux == 2.0
    assert rowe.ens[-1].Cfg.bt_broadband == 7.0
    assert rowe.ens[-1].Cfg.bt_cpce == 10604
    assert rowe.ens[-1].Cfg.bt_first_ping_time == 267
    assert rowe.ens[-1].Cfg.bt_lag_length == 0.0
    assert rowe.ens[-1].Cfg.bt_last_ping_time == 267
    assert rowe.ens[-1].Cfg.bt_lag_length == 0.0
    assert rowe.ens[-1].Cfg.bt_narrowband == 20
    assert rowe.ens[-1].Cfg.bt_nce == 1.0
    assert rowe.ens[-1].Cfg.bt_num_beams == 4
    assert rowe.ens[-1].Cfg.bt_repeat_n == 1.0
    assert rowe.ens[-1].Cfg.bt_samples_per_second == 96000
    assert rowe.ens[-1].Cfg.bt_speed_of_sound == pytest.approx(1484.20, 0.1)
    assert rowe.ens[-1].Cfg.bt_status == 16
    assert rowe.ens[-1].Cfg.bt_system_freq_hz == 1152000
    assert rowe.ens[-1].Cfg.day == 1
    assert rowe.ens[-1].Cfg.desired_ping_count == 1
    assert rowe.ens[-1].Cfg.firm_major == 0
    assert rowe.ens[-1].Cfg.firm_minor == 2
    assert rowe.ens[-1].Cfg.firm_rev == 133
    assert rowe.ens[-1].Cfg.first_ping_time == pytest.approx(267.519, 0.001)
    assert rowe.ens[-1].Cfg.hour == 11
    assert rowe.ens[-1].Cfg.hsec == 0
    assert rowe.ens[-1].Cfg.last_ping_time == pytest.approx(267.5199, 0.001)
    assert rowe.ens[-1].Cfg.minute == 26
    assert rowe.ens[-1].Cfg.month == 11
    assert rowe.ens[-1].Cfg.num_beams == 4
    assert rowe.ens[-1].Cfg.salinity == 0.0
    assert rowe.ens[-1].Cfg.second == 26
    assert rowe.ens[-1].Cfg.serial_num == '01200000000000000000000000000857'
    assert rowe.ens[-1].Cfg.speed_of_sound == pytest.approx(1484.1315, 0.01)
    assert rowe.ens[-1].Cfg.status == 0
    assert rowe.ens[-1].Cfg.subsystem_code == '2'
    assert rowe.ens[-1].Cfg.subsystem_config == 0
    assert rowe.ens[-1].Cfg.transmit_boost_neg_volt == pytest.approx(-18.044, 0.01)
    assert rowe.ens[-1].Cfg.voltage == pytest.approx(24.3934, 0.01)
    assert rowe.ens[-1].Cfg.wp_beam_mux == 2.0
    assert rowe.ens[-1].Cfg.wp_broadband == 1.0
    assert rowe.ens[-1].Cfg.wp_cpce == 12.0
    assert rowe.ens[-1].Cfg.wp_lag_length == pytest.approx(0.20, 0.01)
    assert rowe.ens[-1].Cfg.wp_lag_samples == 28
    assert rowe.ens[-1].Cfg.wp_nce == 28
    assert rowe.ens[-1].Cfg.wp_receive_bandwidth == 0.0
    assert rowe.ens[-1].Cfg.wp_repeat_n == 5.0
    assert rowe.ens[-1].Cfg.wp_samples_per_second == 96000
    assert rowe.ens[-1].Cfg.wp_system_freq_hz == 1152000
    assert rowe.ens[-1].Cfg.wp_transmit_bandwidth == 0.0
    assert rowe.ens[-1].Cfg.xmt_voltage == pytest.approx(17.8573, 0.01)
    assert rowe.ens[-1].Cfg.year == 2019

