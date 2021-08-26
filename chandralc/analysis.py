"""This module contains functions for lightcurve analysis."""

# dependencies
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np

# chandralc modules
from chandralc import ml


def psd(lightcurve, save=False, directory=".", show=True):
    """Plots power spectral density for lightcurve.

    Parameters
    ----------
    lc: ChandraLightcurve
        ChandraLightcurve object
    save : bool, optional
        Save figure or not, by default False
    directory : str, optional
        Directory to save figure in, by default "."
    show : bool, optional
        Show plot or not, by default True
    Returns
    -------
    float
        Time period of frequency with maximum amplitude
    """

    frequency, power = signal.periodogram(lightcurve.raw_phot)
    plt.semilogx(frequency, power)
    plt.xlabel("frequency [Hz]")
    plt.ylabel("PSD [V**2/Hz]")

    if save:
        figure = plt.gcf()
        figure.savefig(
            f"{directory}/chandralc_psd_{lightcurve.coords}_{lightcurve.obsid}.jpg",
            bbox_inches="tight",
        )

    if show:
        plt.show()

    plt.close()

    return (1 / frequency[list(power).index(max(power))]) * 3.241


def bin_lc(lightcurve, binsize):
    """Bins photon counts.

    Parameters
    ----------
    lc: ChandraLightcurve
        ChandraLightcurve object
    binsize : int
        Size of bin

    Returns
    -------
    list
        Array of net counts per bin.
    """
    binned_photons = []

    # range: total number of df points over included bins --> temp3 of intervals
    for j in range(0, len(lightcurve) // binsize):
        bin_count = 0
        j *= binsize
        for k in range(binsize):
            # sum of all photons within one interval
            bin_count = bin_count + lightcurve[j + k]

        # appends that sum to a list
        binned_photons.append(bin_count)

    return binned_photons


def bin_toarrays(lightcurve, binsize):
    """Bins photon counts.

    Parameters
    ----------
    lc: ChandraLightcurve
        ChandraLightcurve object
    binsize : int
        Size of bin

    Returns
    -------
    list
        Array of bins.
    """
    binned_photons = []
    # binned_time = []

    # range: total number of df points over included bins --> temp3 of intervals
    for j in range(0, len(lightcurve) // binsize):
        temp1 = []
        temp2 = 0
        j *= binsize
        for k in range(binsize):
            # sum of all photons within one interval
            temp2 = lightcurve[j + k]
            temp1.append(temp2)

        # appends that sum to a list
        binned_photons.append(temp1)

    return binned_photons

# modified version of lightcurve function
def raw_binned_lightcurve(lc, binning=1000.0, rate=True):
    """Returns raw binned lightcurve."""

    bins = []

    group_size = int(binning / lc.chandra_bin)

    # range: total number of df points over included bins --> temp3 of intervals
    for j in range(len(lc.raw_phot) // group_size):

        # len(temp1) of intervals total_time temp3 of bins in that interval
        j = j * group_size
        temp2 = 0

        for k in range(group_size):
            # sum of all photons within one interval
            temp2 = temp2 + lc.raw_phot[j + k]

        # appends that sum to a list
        bins.append(temp2)

    bins = np.array(bins) / (lc.chandra_bin * group_size) if rate else bins

    # getting NumPy array length of the array and increasing values by 1
    time_array = np.array(range(len(bins))) * lc.chandra_bin / 1000 * group_size

    return time_array, bins

def running_average(
    lc,
    plusminus=2,
    binning=1000.0,
    figsize=(15, 9),
    rate=True,
    fontsize=25,
    family="sans serif",
    save=False,
    directory=".",
    show=True,
):
    """Plots running average over binned lightcurve.

    Parameters
    ----------
    lc: ChandraLightcurve
        ChandraLightcurve object
    plusminus: int
        Number of bins before and after current bin
    binning : float, optional
        Binning in seconds, by default 1000.0
    figsize : tuple, optional
        Size of figure in inches (length, breadth), by default (15, 9)
    rate : bool, optional
        Choose whether to plot count rate or net counts per bin on y-axis, by default True
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

    # getting initial data from binned lightcurve
    data = raw_binned_lightcurve(lc, binning=binning)
    phot_plot = data[1]
    time = data[0]

    # calculating running averages
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        running_avgs = [
            np.mean(data[1][i - plusminus : i + plusminus + 1])
            for i in range(len(phot_plot))
        ]

    # plotting code
    plt.figure(figsize=figsize)

    # binned lightcurve as scatterplot
    plt.scatter(time, phot_plot, color="blue", alpha=0.4)

    # running averages
    plt.plot(time, running_avgs, color="red")

    if rate:
        plt.ylabel("Count Rate (c/s)", fontsize=fontsize)
    else:
        plt.ylabel("Photon Count", fontsize=fontsize)

    plt.xlabel("Time (ks)", fontsize=fontsize)
    plt.title(
        "Running Average Plot Computed Over $\pm$ 2ks, On Top of 1ks Binned Lightcurve"
    )

    plt.rc("text", usetex=False)
    plt.rc("font", family=family)

    if save:
        figure = plt.gcf()
        figure.savefig(
            f"{directory}/chandralc_running_average_{lc.coords}_{lc.obsid}.jpg",
            bbox_inches="tight",
        )

    if show:
        plt.show()

    plt.close()
