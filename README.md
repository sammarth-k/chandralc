# chandralc
<p align="center">
 <a href="LICENSE.txt"><img src = "https://img.shields.io/github/license/sammarth-k/chandralc?logo=MIT"></a>
 
</p>
```chandralc``` is a Python package aimed at easing access to Chandra X-ray Observatory lightcurves and promoting citizen science. It includes several tools for accessing and analysing data.

To see ```chandralc``` in action, check out <a href="https://github.com/sammarth-k/chandralc/blob/main/demo.ipynb">the demo</a>.

### Features:

##### Downloads:

- Large database of over 75,000 files
- Downloading extracted lightcurves from multiple galaxies.
- Search for lightcurves with J2000 coordinates
- Retrieve galaxy from lightcurve file names

##### Analysis:

- Observation details: Source coordinates, ObsID, total counts, observation time, count rate
- Cumulative Count plots over time to view net counts over time
- Lightcurves with custom binning to view data in the form of count rate per bin or net counts per bin over time.
- Retrieve raw data in the form of a Pandas DataFrame or arrays.
- Power Spectral Density (PSD) to identify . periodicity and their time periods/frequencies

##### Upcoming features:

- Integration with <a href="https://github.com/sammarth-k/galaXy.lc"> galaXy.lc</a>
