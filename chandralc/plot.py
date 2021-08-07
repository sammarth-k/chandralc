"""This module contains functions to plot lightcurves in different ways."""

# Dependencies
import matplotlib.pyplot as plt
import numpy as np
import warnings


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
    timespan: bool/tuple
        range of x axis (kiloseconds), by default False
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
        plt.yticks(np.arange(0, upper + 1, 3))

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
