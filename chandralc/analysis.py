"""This module contains functions for lightcurve analysis."""

# chandralc modules
from chandralc import ml

# dependencies
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np


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
