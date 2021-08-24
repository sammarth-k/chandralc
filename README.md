<div align="center"> <img src="github.com/sammarth-k/chandralc/images/chandralc.png" width="100%"></div>

# chandralc: The Future of Chandra Lightcurve Analysis 

<p align="left">
 <a href="LICENSE.txt"><img src = "https://img.shields.io/github/license/sammarth-k/chandralc?logo=MIT"></a> <a herfF="https://python.org" target="_blank"><img src="https://img.shields.io/badge/Made%20with-Python-306998.svg"></a> <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

``chandralc`` is a Python package for processing Chandra X-ray Observatory (``CXO``) lightcurves and includes several functions and modules to download, plot and analyse data, It also contains algorithms to detect flares, eclipses and periodicities, and has **automation** tools to find events in a large dataset

To see ``chandralc`` in action, check out <a href="https://github.com/sammarth-k/chandralc/blob/main/demo.ipynb">the demo</a>.

### Features:

#### Downloads:

- Large database of over 100,000 files
- Downloading extracted lightcurves from 13+ galaxies.
- Search for lightcurves with J2000 coordinates
- Retrieve galaxy from lightcurve file names

#### Analysis:

##### Observation Details
- Total counts
- Observation time
- Count rate (kilosecond, seconds)
- Source coordinates
- ObsID
- Galaxy (Messier or NGC)
	
#### Plots
- Cumulative Count plots over time to view net counts over time
- Lightcurves with custom binning to view data in the form of count rate per bin or net counts per bin over time.
- Power Spectral Density (PSD) to identify periodicity and their time periods/frequencies.
- Running Averages

#### Feature Detection
- Flares
- Eclipses

##### Upcoming features:

- Integration with <a href="https://github.com/sammarth-k/galaXy.lc"> galaXy.lc </a>
- VizeR and NASA ADS connection

### Installation

1. Install dependencies via requirements.txt file:
   ```pip install requirements.txt```

##### Cite chandralc

If you use ``chandralc`` in your research, please cite it as follows:

```tex
@MISC{chandralc,
	author = {{Kumar}, Sammarth},
	title = "{chandralc: Python Package for CXO Lightcurve Analysis}",
	keywords = {Software, Chandra, CXO, lightcurves },
	url = {https://github.com/sammarth-k/chandralc},
	publisher = {\url{{https://github.com/sammarth-k/chandralc}}},
	year = {2021},
	month = {May},
}
```
