# rti_python
RTI Library in Python


Rowe Technologies Inc. Python library

There is currently no main file to run.  This library contains core library files to create a python application.


# Dependencies
Must use Python version 3.5

OSX and Linux
```javascript
pip3 install -r requirements.txt -UI --user
```
 
 
Windows
```javascript
set-executionpolicy RemotedSigned
/venv/Scripts/activate.ps1
python -m pip install -r requirements.txt -UI --user
```


### Upgrade Dependcies to Latest Version
```term
pip install -r requirements.txt --upgrade
```

## ADCP
All the available commands and subsystem types.  This also contains the prediction model

## Codecs
Decode the ADCP data from different formats.

## Ensemble
Ensemble data formats

## Unittest
All the unittests.


## Waves
Waves MATLAB formats

## Writer
Write the ensemble data to a file format.

## Logging
Edit the log.py file to turn on or off some logging options.

## Read in a File and decode the data
```python
from rti_python.Utilities.read_binary_file import ReadBinaryFile

    def process_ens_func(sender, ens):
        """
        Receive the data from the file.  It will process the file.
        When an ensemble is found, it will call this function with the
        complete ensemble.
        :param ens: Ensemble to process.
        :return:
        """
        if ens.IsEnsembleData:
            print(str(ens.EnsembleData.EnsembleNumber))

# Create the file reader to read the binary file
read_binary = ReadBinaryFile()
read_binary.ensemble_event += process_ens_func

# Just define the file path
file_path = "/path/to/file/ensembles.ens"

# Pass the file path to the reader
read_binary.playback(file_path)
```


## Check for Bad Velocity in data
```python
if Ensemble.is_bad_velocity(vel_value):
    print("Bad Velocity Value")
else:
    print("Good Velocity Value")
```