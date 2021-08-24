"""The future of CXO Lightcurve Analysis."""

# PSL modules
import os
import inspect

# chandralc modules
from chandralc import download

clc_path = os.path.dirname(inspect.getfile(download))

# config files
try:
    os.mkdir(clc_path + "/config")
except:
    pass

from chandralc.chandra_lightcurve import *

# Download Database Indices
download.download_db()
