# dependencies

# External Modules
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

# User made modules
from chandralc import download, convert

class ChandraLightcurve(object):
    """Class for lightcurve plotting and analysis.

    Attributes
    ----------
    path: str
        Filepath
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

        chandra_bin = 3.241039999999654

        self.cumulative_count_arr = []

        count = 0

        # Creating counts array
        for index, row in self.df.iterrows():
            if self.df['EXPOSURE'][index] > 0:
                count += self.df.COUNTS[index]
            elif self.df['EXPOSURE'][index] == 0:
                count += 0

            self.cumulative_count_arr.append(count)

        # array for timestamps
        self.time_array = [chandra_bin / 1000 *
                           i for i in range(1, len(self.cumulative_count_arr) + 1)]

        # Lightcurve stats
        self.time = round(self.time_array[-1], 3)
        self.count = count
        self.rate_ks = round(self.count / self.time, 3)
        self.rate_s = round(self.count / (self.time * 1000), 5)

        # Source information
        file = file.split("_lc.fits")[0].split("_")
        file = file.split("/")[-1] if "/" in file else file
        self.obsid = file[1]
        self.coords = convert.extract_coords(self.path)

        # raw data
        self.raw_phot = [self.df.COUNTS[i] if self.df.EXPOSURE[i]
                         > 0 else 0 for i in range(len(self.df))]


    def lightcurve(self, binning=500.0, figsize=(15, 9), rate=True, color="blue", fontsize=25, family="sans serif", save=False):
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
        """
        chandra_bin = 3.241039999999654

        photons_in_group = []

        group_size = int(binning / chandra_bin)

        temp1 = [self.df.COUNTS[i] if self.df.EXPOSURE[i] > 0 else 0 for i in range(
            len(self.df.COUNTS)) if self.df.EXPOSURE[i] > 0]

        # range: total number of df points over included bins --> temp3 of intervals
        for j in range(len(temp1) // group_size):

            # len(temp1) of intervals total_time temp3 of bins in that interval
            j = j * group_size
            temp2 = 0
            for k in range(group_size):
                # sum of all photons within one interval
                temp2 = temp2 + temp1[j+k]

            # appends that sum to a list
            photons_in_group.append(temp2)

        avg_phot = np.array(photons_in_group) / (chandra_bin *
                                                 group_size) if rate else photons_in_group

        avg = [i for i in avg_phot for j in range(group_size)]

        # getting NumPy array length of the array and increasing values by 1
        f = np.array(range(len(avg)))

        # adjusting for kiloseconds and multiplying each value in the array by the exposure time
        f = f*chandra_bin/1000

        # customizing the plot
        plt.figure(figsize=figsize)
        plt.rc('text', usetex=False)
        plt.rc('font', family=family)
        plt.xlabel(r'Time (ks)', fontsize=fontsize)
        if rate:
            plt.ylabel(r'Count Rate (c/s)', fontsize=fontsize)
        else:
            plt.ylabel(r'Photon Counts', fontsize=fontsize)
        plt.rc('xtick', labelsize=30)
        plt.rc('ytick', labelsize=22)
        plt.title(
            f"{binning}s Binned Lightcurve for {self.coords} ObsID {self.obsid}")
        plt.plot(f, avg, color=color)

        # adjusting the scale of axis
        upper = np.max(avg)

        if rate == False:
            plt.yticks(np.arange(0, upper+1, 3))

        if save:
            f = plt.gcf()
            f.savefig(
                f"chandralc_lightcurve_{self.coords}_{self.obsid}_{binning}.jpg", bbox_inches='tight')

        plt.show()

    def cumulative(self, figsize=(15, 9), color="blue", fontsize=25, family='sans serif', save=False):
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
        """

        # plotting
        plt.figure(figsize=figsize)
        plt.plot(self.time_array, self.cumulative_count_arr, color=color)
        plt.xlabel("Time (ks)")
        plt.ylabel("Net Photon Counts")
        plt.title(
            f"Cumulative Photon Count v/s Time Plot for {self.coords} ObsID {self.obsid}")
        plt.rc('text', usetex=False)
        plt.rc('font', family=family)
        plt.xlabel(r'Time (ks)', fontsize=fontsize)
        plt.ylabel(r'Photon Count', fontsize=fontsize)
        plt.rc('xtick', labelsize=30)
        plt.rc('ytick', labelsize=22)

        if save:
            f = plt.gcf()
            f.savefig(
                f"chandralc_cumulative_{self.coords}_{self.obsid}.jpg", bbox_inches='tight')

        plt.show()

    def psd(self):
        """Plots power spectral density for lightcurve.

        Returns
        -------
        float
            Time period of frequency with maximum amplitude
        """

        f, Pxx_den = signal.periodogram(self.raw_phot)
        plt.semilogx(f, Pxx_den)
        plt.xlabel('frequency [Hz]')
        plt.ylabel('PSD [V**2/Hz]')
        plt.show()

        return (1/f[list(Pxx_den).index(max(Pxx_den))])*3.241

    # signature detection algorithms
    def bin(self, binsize):
        """Bins photon counts.

        Parameters
        ----------
        binsize : int
            Size of bin

        Returns
        -------
        list
            Array of bins
        """
        binned_photons = []

        # range: total number of df points over included bins --> temp3 of intervals
        for j in range(0, len(self.df.COUNTS)//binsize):
            temp2 = 0
            j *= binsize
            for k in range(binsize):
                # sum of all photons within one interval
                temp2 = temp2 + self.df.COUNTS[j+k]

            # appends that sum to a list
            binned_photons.append(temp2)

        return binned_photons