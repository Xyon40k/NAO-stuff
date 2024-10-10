# NAO-stuff
Repo to store all the development and setup files needed to use NAO with the Python SDK

This repo is meant to collect all the needed files and links to start developing with your NAO with the python SDK without complications.<br>
This was motivated by our difficulties in finding appropriate examples, tutorials, or the documentation itself at first, and by the lack of maintenance and support that Aldebaran Robotics offers.
Our hope is for someone experiencing the same things we did to be saved by this repo.

In the _Redist directory you can find a python 2.7.18 installer, and a corrected Visual c++ 2013 installer.<br>
When just installed from the installer, Choregraphe may tell you that VCOMP120.dll is missing. The c++ installer provided in this repo is meant to fix this.

To properly "install" the naoqi library for Python, rename the downloaded .zip file (as windows cannot extract it if the filename is too long), unzip it and move the `pynaoqi-python2.7-2.8.6.23-win64-vs2015-20191127_152649` directory found within inside `<python2.7 installation path>/Python27/Lib/site-packages` (on windows this is by default `C:/Python27/Lib/site-packages`). Then, edit your environment variables to add the path to the `lib` subdirectory to your PYTHONPATH variable, or create it if you don't have it. Now you should be able to use `import naoqi` in any python file to import the library.

Note that we were using a NAO v6 with Windows and this wasn't tested at all with other models/OSs.
Also forgive us for the spaghetti code (and the italian mixed in) as we did this after school while we were still learning programming.

Link to the official download site for the programs: https://www.aldebaran.com/en/support/nao-6/downloads-softwares (Warning: at the time of writing some links are broken or mislabeled. Double check the downloaded files.)<br>
Link to the official documentation: http://doc.aldebaran.com/2-8/naoqi/index.html
