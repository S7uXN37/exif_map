
# exif_map
Supply a folder of images with geo locations and this python script will put them on a map

Runs on Python3

## Dependencies ##
This script depends on the third-party modules:
* exifread ([installation](https://pypi.org/project/ExifRead/))
  - You'll need PIP installed ([installation](https://pip.pypa.io/en/stable/installing/))
* cartopy ([installation](https://scitools.org.uk/cartopy/docs/v0.16/installing.html))
  - Either using [conda](https://conda.io/docs/user-guide/install/index.html) or by building from source with these dependencies:
  - Cython ("pip isntall Cython")
  - NumPy (using pip, but probably pre-installed)
  - GEOS ("pip install GEOS")
  - Proj.4 ([installation](https://proj4.org/install.html#install))
* requests ([installation](http://docs.python-requests.org/en/master/user/install/))
  - Or just "pip install requests" if pip is installed

And on the built-in modules:
* PIL
* argparse
* matplotlib
* glob
* os
* numpy

## Usage ##
Just execute the script using:
> python3 generate.py

Usage info and possible arguments can be shown with:
> python3 generate.py -h

## General info ##
All commands in quotes above should be run in a command prompt:
- cmd.exe on Windows (search for "Command Prompt")
- Terminal on MacOS and Linux (search for "Terminal")
