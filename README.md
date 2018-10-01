# rti-python
RTI Library in Python


Rowe Technologies Inc. Python library

There is currently no main file to run.  This library contains a variety
of utility applications.

The Utilities and tests folder contain python applications to test different features and also used for examples.

#Dependicencies
Must use Python version 3.5

OSX and Linux
```javascript
pip3 install -r requirements.txt -UI --user
```
 
 
Windows
```javascript
python -m pip install -r requirements.txt -UI --user
```

#WAMP Application to run

```javascript
cd crossbar
crossbar start
```

This will start the WAMP server, the serial port and GUI





#Create PredictR application
OSX
```javascript
pyinstaller Predictr_installer_OSX.spec
```

Windows

You will need to install MSVC 2015 redistribution.


Then add C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64 to environment PATH. Then the warning message about api-ms-win-crt-***.dll will disappear and all works correctly.

```javascript
C:\Users\XXX\AppData\Local\Programs\Python\Python35\Scripts\pyinstaller.exe Predictr_installer_WIN.spec
```

This will create a dist and build folder.  The exe in is the dist folder.


#To create a new Pyinstaller spec file
OSX
```javascript
pyinstaller /path/to/mainwindow.py --windowed --onefile
```

Windows
```javascript
C:\Users\XXX\AppData\Local\Programs\Python\Python35\Scripts\pyinstaller.exe  --windowed --onefile --paths C:\Users\XXX\AppData\Roaming\Python\Python35\site-packages\PyQt5\Qt\bin /path/to/mainwindow.py
```

You will need to add the predictor.json to the data=[] in the spec file.
Use the spec files as an example for the data=[] settings.

Windows must include the path to PyQT5 DLL files.


#Compile QT5 .UI files
OSX
```javascript
pyuic5 -x file.ui -o file.py
```

Windows
```javascript
python -m PyQt5.uic.pyuic -x filename.ui -o filename.py

C:\Users\XXX\AppData\Local\Programs\Python\Python35\Scripts\pyuic5.exe -x file.ui -o file.py
```

#Compile QT5 .qrc files
Add all the images included in the .qrc file.  Then compile it.
Also add the images to the spec file.

OSX
```javascript
pyrcc4 -o images.qrc images_qr.py
```

#Install Virtualenv in Windows
```python
pip install virtualenv
pip install virtualenvwrapper-win
```



#Run Utilties Apps
OSX and Linux
```javascript
export PYTHONPATH=$PYTHONPATH:/path/to/rti_python

python3 Utilities/EnsembleFileReport.py -i file -v
```

Windows
```javascript
set PYTHONPATH=%PYTHONPATH%;/path/to/rti_python
```

#AWS DynamoDB
Install AWS CLI

```javascript
pip3 install awscli
```

Setup a configuration

```javascript
aws configure
```

Add a User to IAM in AWS Console

Create Access key and Secret key and add to 'aws configure'


-------------
#install pyside2

#To Compile pyside2 from source for OSX

##Download and install QT5.6
```
curl -O https://raw.githubusercontent.com/Homebrew/homebrew-core/fdfc724dd532345f5c6cdf47dc43e99654e6a5fd/Formula/qt5.rb
```
```
brew install ./qt5.rb
```
##Download pyside2
```
git clone --recursive http://code.qt.io/cgit/pyside/pyside-setup.git/
```

##Install pyside3 with python3 and QT5.6
```
python3 setup.py install ---ignore-git --build-tests --qmake=/usr/local/Cellar/qt5/5.6.1-1/bin/qmake --cmake=/usr/local/bin/cmake --openssl=/usr/bin/openssl
```
