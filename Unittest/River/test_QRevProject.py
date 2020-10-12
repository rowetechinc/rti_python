import os
from rti_python.River.QRevProject import QRevRtiProject
from rti_python.River.QRevTransect import QRevRtiTransect

def test_constructor():
    project_name = "TestProject1"
    project = QRevRtiProject(project_name)
    project.path = 'C:\\RTI_Capture\\imperial\\Imperal Valley_20170816_095301\\'

    assert project.project is not None
    assert type(project.project) is dict
    assert 'Name' in project.project
    assert project.project['Name'] == project_name


def test_transect():
    project_name = "TestProject1"
    project = QRevRtiProject(project_name)
    project.path = 'C:\\RTI_Capture\\imperial\\Imperal Valley_20170816_095301\\'

    transect = QRevRtiTransect()
    file_name1 = 'Imperal Valley_20170816_095301_0_1.2 MHz 4 beam 20 degree piston_pd0.pd0'
    transect.add_transect_file(file_name1)
    project.add_transect(transect)

    assert len(project.transects) == 1
    assert len(project.transects[0].Files) == 1
    assert project.transects[0].Files[0] == file_name1


def test_write_file():
    project_name = "TestProject1"
    project = QRevRtiProject(project_name)
    project.path = 'C:\\RTI_Capture\\test_qrev_project'

    transect = QRevRtiTransect()
    file_name1 = 'Imperal Valley_20170816_095301_0_1.2 MHz 4 beam 20 degree piston_pd0.pd0'
    transect.add_transect_file(file_name1)
    project.add_transect(transect)

    # Write the project file
    project.write_json_file()

    assert os.path.exists(project.path)
    assert os.path.exists(os.path.join(project.path, project_name + QRevRtiProject.FILE_EXTENSION))


def test_write_file_multi_transect():
    project_name = "TestProject1"
    project = QRevRtiProject(project_name)
    project.path = 'C:\\RTI_Capture\\test_qrev_project'

    transect = QRevRtiTransect()
    file_name1 = 'Imperal Valley_20170816_095301_0_1.2 MHz 4 beam 20 degree piston_pd0.pd0'
    file_name2 = 'Imperal Valley_20170816_095301_0_1.2 MHz 4 beam 20 degree piston_pd0_1.pd0'
    transect.add_transect_file(file_name1)
    transect.add_transect_file(file_name2)
    project.add_transect(transect)

    # Write the project file
    project.write_json_file()

    assert os.path.exists(project.path)
    assert os.path.exists(os.path.join(project.path, project_name + QRevRtiProject.FILE_EXTENSION))


def test_read_file():
    project_name = "TestProject1"
    project = QRevRtiProject(project_name)
    project.path = 'C:\\RTI_Capture\\test_qrev_project'

    transect = QRevRtiTransect()
    file_name1 = 'Imperal Valley_20170816_095301_0_1.2 MHz 4 beam 20 degree piston_pd0.pd0'
    file_name2 = 'Imperal Valley_20170816_095301_0_1.2 MHz 4 beam 20 degree piston_pd0_1.pd0'
    transect.add_transect_file(file_name1)
    transect.add_transect_file(file_name2)
    project.add_transect(transect)

    # Verify the file exist before we read it in
    assert os.path.exists(project.path)
    assert os.path.exists(os.path.join(project.path, project_name + QRevRtiProject.FILE_EXTENSION))

    # Read the project file
    project_read = QRevRtiProject("")
    project_read.read_json_file(os.path.join(project.path, project_name + QRevRtiProject.FILE_EXTENSION))

    assert project_read.project['Name'] == project_name
    assert len(project_read.transects) == 1
    assert len(project_read.transects[0].Files) == 2

