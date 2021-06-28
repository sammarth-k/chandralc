"""This module contains the ChandraLightcurve class."""

# dependencies

# External Modules
import numpy as np

# User made modules
from chandralc import convert, analysis, plot, ml
from chandralc.download import get_galaxy


class ChandraLightcurve:
    """Class for lightcurve plotting and analysis.

    Attributes
    ----------
    path: str
        File path
    df: pandas.core.frame.DataFrame
        DataFrame of lightcurve
    time: float
        Total observation time
    count: float
        Net photon counts of observation
    rate_ks: float
        Net count rate in kiloseconds
    rate_s: float
        Net count rate in seconds
    obsid: str
        Observation ID
    coords: str
        Source coordinates in J2000 format
    raw_phot: list
        Array of photons
    cumulative_counts: numpy.ndarray
        Array of cumulative photon counts
    time_array : list

    """

    def __init__(self, file):
        """Inits ChandraLightcurve class.

        Parameters
        ----------
        file : str
            Filename or filepath of raw lightcurve
        """

        self.path = file

        if "txt" in file:
            self.df = convert.txt_to_df(file, convert.header_check(file))
        elif "fits" in file:
            self.df = convert.fits_to_df(file, convert.header_check(file))

        self.chandra_bin = 3.241039999999654

        self.raw_phot = np.array(self.df[self.df.EXPOSURE > 0].COUNTS)

        # will count net counts
        self.count = 0

        self.cumulative_counts = []

        for raw_phot in self.raw_phot:
            self.count += raw_phot
            self.cumulative_counts.append(self.count)

        self.cumulative_counts = np.array(self.cumulative_counts).astype(int)

        # array for timestamps
        self.time_array = np.arange(1, len(self.raw_phot) + 1) * self.chandra_bin / 1000
                
        # np.array([self.chandra_bin / 1000 *
        #                           i for i in range(1, len(self.raw_phot) + 1)])

        # Lightcurve stats
        try:
            self.time = round(self.time_array[-1], 3)
        except:
            self.time = 0.0000001
        self.rate_ks = round(self.count / self.time, 3)
        self.rate_s = self.rate_ks/1000

        # Source information
        file = file.split("_lc.fits")[0].split("_")
        file = file.split("/")[-1] if "/" in file else file
        self.obsid = file[1]
        self.coords = convert.extract_coords(self.path)
        self.galaxy = get_galaxy(self.path)

    def lightcurve(
        self,
        binning=500.0,
        figsize=(15, 9),
        rate=True,
        color="blue",
        fontsize=25,
        family="sans serif",
        save=False,
        directory=".",
        show=True,
    ):
        """Plots cumulative photon counts over time.

        Parameters
        ----------
        figsize : tuple, optional
            Size of figure in inches (length, breadth), by default (15, 9)
        color : str, optional
            Color of plotted data, by default "blue"
        fontsize : int, optional
            Fontsize of tick labels, by default 25
        family : str, optional
            Font family for text, by default 'sans serif'
        save : bool, optional
            Save figure or not, by default False
        directory : str, optional
            Directory to save figure in, by default "."
        show : bool, optional
            Show plot or not, by default True
        """

        plot.lightcurve(
            self,
            binning=binning,
            figsize=figsize,
            rate=rate,
            color=color,
            fontsize=fontsize,
            family=family,
            save=save,
            directory=directory,
            show=show,
        )

    def cumulative(
        self,
        figsize=(15, 9),
        color="blue",
        fontsize=25,
        family="sans serif",
        save=False,
        directory=".",
        show=True,
    ):
        """Plot binned lightcurves over time.

        Parameters
        ----------
        binning : float, optional
            Binning in seconds, by default 500.0
        figsize : tuple, optional
            Size of figure in inches (length, breadth), by default (15, 9)
        rate : bool, optional
            Choose whether to plot count rate or net counts per bin on y-axis, by default True
        color : str, optional
            Color of plotted data, by default "blue"
        fontsize : int, optional
            Fontsize of tick labels, by default 25
        family : str, optional
            Font family for text, by default 'sans serif'
        save : bool, optional
            Save figure or not, by default False
        directory : str, optional
            Directory to save figure in, by default "."
        show : bool, optional
            Show plot or not, by default True
        """

        plot.cumulative(
            self,
            figsize=figsize,
            color=color,
            fontsize=fontsize,
            family=family,
            save=save,
            directory=directory,
            show=show,
        )

    def psd(self, save=False, directory=".", show=True):
        """Plots power spectral density for lightcurve.

        Returns
        -------
        float
            Time period of frequency with maximum amplitude
        """

        return analysis.psd(self, save=save, directory=directory, show=show)

    def bin_lc(self, binsize):
        """Bins photon counts and returns an array of net counts per bin.

        Parameters
        ----------
        binsize : int
            Size of bin

        Returns
        -------
        list
            Array of net counts per bin.
        """

        return analysis.bin_lc(self.raw_phot, binsize)

    def bin_toarrays(self, binsize=10):
        """Bins photon counts and returns an array with each bin.

        Parameters
        ----------
        binsize : int
            Size of bin

        Returns
        -------
        list
            Array of bins.
        """
        return analysis.bin_toarrays(self.raw_phot, binsize)

    def flare_detect(self, binsize=5, sigma=3, threshold=0.3):
        """Detects potential flares in lightcurves.

        Parameters
        ----------
        binsize : int
            Items per bin, by default 10
        sigma : float
            Number of standard deviations of regression slope above mean of regression slopes of all bins, by default 3
        threshold : float
            Threshold of clustering of bins which could be part of a flare from 0 to 1, by default 0.3

        Returns
        -------
        bool
            Whether flare(s) is/are detected or not
        """
        if ml.calculate_r(self.time_array, self.cumulative_counts) ** 2 <= 0.998:
            return analysis.flare_detect(
                self, binsize=binsize, sigma=sigma, threshold=threshold
            )

        return False
