import pytest
import os
from rti_python.Utilities.config import RtiConfig
from rti_python.River.RiverProjectManager import RiverProjectManager
from rti_python.River.Transect import Transect

rti_config = RtiConfig()
rti_config.init_river_project_config()


def setup_test():
    # Delete all the hdf5 files
    for file in os.listdir("./"):
        if file.endswith(".hdf5"):
            os.remove(os.path.join("./", file))


def test_constructor():

    # FIRST TEST RUN SO RUN SETUP
    setup_test()

    rvr_prj_mgr = RiverProjectManager(rti_config)


def test_create_project():
    rvr_prj_mgr = RiverProjectManager(rti_config)
    project_file = rvr_prj_mgr.create_project("Project1")

    if project_file is not None:
        assert True
    else:
        assert False

    if 'Name' in project_file.attrs:
        assert True
    else:
        assert False

    assert "Project1" == project_file.attrs["Name"]


def test_get_project_list():
    rvr_prj_mgr = RiverProjectManager(rti_config)

    project_file = rvr_prj_mgr.create_project("Project2")

    prjs_list = rvr_prj_mgr.get_project_list()
    assert len(prjs_list) >= 1

    assert True == ("Project2" in prjs_list)

    assert "Project2" == project_file.attrs["Name"]


def test_create_project_exist():
    rvr_prj_mgr = RiverProjectManager(rti_config)
    project_file = rvr_prj_mgr.create_project("Project3")
    project_file1 = rvr_prj_mgr.create_project("Project3")      # Duplicate

    prjs_list = rvr_prj_mgr.get_project_list()
    assert len(prjs_list) >= 2

    assert True == ("Project3_0" in prjs_list)

    assert "Project3" == project_file.attrs["Name"]
    assert "Project3_0" == project_file1.attrs["Name"]


def test_add_project():
    rvr_prj_mgr = RiverProjectManager(rti_config)

    project_file = rvr_prj_mgr.add_project("Project22", os.path.join("./", "Project1.hdf5"))

    project_list = rvr_prj_mgr.get_project_list()

    # Project name in list matches list entry
    assert True == ("Project22" in project_list)
    # Project Name in file matches file
    assert "Project1" == project_file.attrs["Name"]


def test_get_project():
    rvr_prj_mgr = RiverProjectManager(rti_config)

    project_file_path = rvr_prj_mgr.get_project("Project2")

    # Project Name in file matches file
    assert os.path.join(os.getcwd(), "Project2.hdf5") == project_file_path


def test_add_project_file_not_exist():
    rvr_prj_mgr = RiverProjectManager(rti_config)

    # File path should not exist so project file will be none
    project_file = rvr_prj_mgr.add_project("Project23", os.path.join("./", "Project77.hdf5"))

    project_list = rvr_prj_mgr.get_project_list()

    assert False == ("Project23" in project_list)
    if project_file is None:
        assert True
    else:
        assert False


def test_add_transect():
    rvr_prj_mgr = RiverProjectManager(rti_config)
    #transect = Transect(33)
    #assert transect.transect_index == 33

    #rvr_prj_mgr.create_transect(transect)




