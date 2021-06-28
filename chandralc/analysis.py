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
        f = plt.gcf()
        f.savefig(
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
    binned_time = []

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


def flare_detect(lc, binsize=10, sigma=3, threshold=0.3):
    """Detects potential flares in lightcurves.

    Parameters
    ----------
    lc : ChandraLightcurve
        ChandraLightcurve object
    binsize : int
        Size of bin, by default 10
    sigma : float
        Number of standard deviations of regression slope above mean of regression slopes of all bins, by default 3
    threshold : float
        Threshold of clustering of bins which could be part of a flare from 0 to 1, by default 0.3

    Returns
    -------
    bool
        Whether flare(s) is/are detected or not
    """

    # binsize arrays of times and cumulative counts
    binned_time_arrays = bin_toarrays(lc.time_array, binsize)
    binned_count_arrays = bin_toarrays(lc.cumulative_counts, binsize)

    # Array of slopes of each bin from regression line
    slopes = [
        ml.regression_equation(x, y)[0]
        for x, y in zip(binned_time_arrays, binned_count_arrays)
    ]

    # Replacing nan with 0
    for i in range(len(slopes)):
        if np.isnan(slopes[i]):
            slopes[i] = 0

    # array of potential flares
    potential_flares = [
        i * binsize * lc.chandra_bin
        if ml.sigma_check(slopes, slopes[i], sigma=sigma)
        else 0
        for i in range(len(slopes))
    ]

    if (
        len(ml.check_cluster(potential_flares, binsize=binsize, threshold=threshold))
        > 0
    ):
        return True

    return False

def eclipse_detect(lc, binsize=300):
    """Detects potential eclipses in lightcurves.
       
    Parameters
    ----------
    lc : ChandraLightcurve
        ChandraLightcurve object
    binsize : int
        Size of bin, by default 300
    
    Returns
    -------
    list
        Array of eclipse timestamps
    """
    # binsize arrays of times and cumulative counts
    binned_time_arrays = analysis.bin_toarrays(lc.time_array, binsize)
    binned_count_arrays = analysis.bin_toarrays(lc.cumulative_counts, binsize)

    # Array of slopes of each bin from regression line
    slopes = [0 if np.isnan(ml.regression_equation(x,y)[0]) else ml.regression_equation(x,y)[0] for x,y in zip(binned_time_arrays, binned_count_arrays)]
    
    
    potential_eclipses = [[]] # to store timestamps of eclipse
    eclipse = True # to check whether an eclipse has been detected
    index = 0 # to keep track of position in potential_eclipses
    
    for i in range(len(slopes)):
        
        if slopes[i] <= int(np.mean(slopes) - lc.rate_ks//5) * np.std(slopes):
            
            if eclipse == False:
                index += 1
                potential_eclipses.append([])
                
            potential_eclipses[index].append(((i+1) * binsize * lc.chandra_bin))
            eclipse = True
            
        else:
            eclipse = False 
            
    return [cluster for cluster in potential_eclipses if len(cluster) > 1]