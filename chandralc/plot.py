"""This module contains functions to plot lightcurves in different ways."""

# PSL modules
import os
import inspect

# Dependencies
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import warnings

# chandralc modules
from chandralc import convert

clc_path = os.path.dirname(inspect.getfile(convert))

with open(clc_path + "/config/mpl_backend.chandralc", "r") as f:

    if "True" in f.read():
        matplotlib.use("agg")
        plt.ioff()
        print("Using agg backend for plotting")
        
def lightcurve(
    lc,
    binning=500.0,
    figsize=(15, 9),
    rate=True,
    color="blue",
    fontsize=25,
    family="sans serif",
    save=False,
    directory=".",
    show=True,
    timespan=False,
    ymax=None
):
    """Plot binned lightcurves over time.

    Parameters
    ----------
    lc: ChandraLightcurve
        ChandraLightcurve object
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
    timespan : bool/tuple
        range of x axis (kiloseconds), by default False
    ymax : float, optional
        Maximum y-axis value, by default None
    """

    photons_in_group = []

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
        photons_in_group.append(temp2)

    avg_phot = (
        np.array(photons_in_group) / (lc.chandra_bin * group_size)
        if rate
        else photons_in_group
    )

    avg = [i for i in avg_phot for j in range(group_size)]

    # getting NumPy array length of the array and increasing values by 1
    time_array = np.array(range(len(avg))) * lc.chandra_bin / 1000

    # customizing the plot
    plt.figure(figsize=figsize)
    plt.rc("text", usetex=False)
    plt.rc("font", family=family)
    plt.xlabel(r"Time (ks)", fontsize=fontsize)

    if rate:
        plt.ylabel(r"Count Rate (c/s)", fontsize=fontsize)
    else:
        plt.ylabel(r"Photon Counts", fontsize=fontsize)

    plt.rc("xtick", labelsize=30)
    plt.rc("ytick", labelsize=22)
    plt.title(f"{binning}s Binned Lightcurve for {lc.coords} ObsID {lc.obsid}")
    plt.plot(time_array, avg, color=color)

    # adjusting the scale of axis
    upper = np.max(avg)

    if not rate:
        if ymax == None:
            plt.yticks(np.arange(0, upper + 1, 3))
        else:
            plt.yticks(np.arange(0, ymax + 1, 3))

    if timespan is not False:
        plt.xlim(timespan[0], timespan[1])

    if save:
        figure = plt.gcf()
        figure.savefig(
            f"{directory}/chandralc_lightcurve_{lc.coords}_{lc.obsid}_{binning}.jpg",
            bbox_inches="tight",
        )
    if show:
        plt.show()

    plt.close()


def cumulative(
    lc,
    figsize=(15, 9),
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
    lc: ChandraLightcurve
        ChandraLightcurve object
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

    # plotting
    plt.figure(figsize=figsize)
    plt.plot(lc.time_array, lc.cumulative_counts, color=color)
    plt.xlabel("Time (ks)")
    plt.ylabel("Net Photon Counts")
    plt.title(f"Cumulative Photon Count v/s Time Plot for {lc.coords} ObsID {lc.obsid}")
    plt.rc("text", usetex=False)
    plt.rc("font", family=family)
    plt.xlabel(r"Time (ks)", fontsize=fontsize)
    plt.ylabel(r"Photon Count", fontsize=fontsize)
    plt.rc("xtick", labelsize=30)
    plt.rc("ytick", labelsize=22)

    if save:
        figure = plt.gcf()
        figure.savefig(
            f"{directory}/chandralc_cumulative_{lc.coords}_{lc.obsid}.jpg",
            bbox_inches="tight",
        )

    if show:
        plt.show()

    plt.close()


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
