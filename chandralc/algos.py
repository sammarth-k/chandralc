"""Algorithms for eclipse and flare detection."""

# Dependencies
import numpy as np
from chandralc import analysis, ml


def flare_detect(lc, binsize=10, sigma=3, threshold=0.3):
    """Detects potential flares in lightcurves.

    Parameters
    ----------
    lc : ChandraLightcurve
        ChandraLightcurve object
    binsize : int
        Size of bin, by default 10
    sigma : float
        No. of std. deviations of slope above mean of slopes of all bins, by default 3
    threshold : float
        Threshold of clustering of bins which could be part of a flare from 0 to 1, by default 0.3

    Returns
    -------
    bool
        Whether flare(s) is/are detected or not
    """

    # binsize arrays of times and cumulative counts
    binned_time_arrays = analysis.bin_toarrays(lc.time_array, binsize)
    binned_count_arrays = analysis.bin_toarrays(lc.cumulative_counts, binsize)

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
    """Checks for eclipses in files.

    Parameters
    ----------
    lc : ChandraLightcurve
        ChandraLightcurve object
    binsize : int
        Size of bin, by default 300

    Returns
    -------
    list
        2D array of eclipse timestamps
    """

    # binsize arrays of times and cumulative counts
    binned_time_arrays = analysis.bin_toarrays(lc.time_array, binsize)
    binned_count_arrays = analysis.bin_toarrays(lc.cumulative_counts, binsize)

    # Array of slopes of each bin from regression line
    slopes = [
        ml.regression_equation(x, y)[0]
        for x, y in zip(binned_time_arrays, binned_count_arrays)
    ]  # [(i[-1] - i[0])/binsize*3241 for i in binned_count_arrays]

    # Replacing nan with 0
    for i in range(len(slopes)):
        if np.isnan(slopes[i]):
            slopes[i] = 0

    # finding clusters of eclipse candidates
    potential_eclipses = [[]]
    eclipse = True
    index = 0

    for i in range(len(slopes)):

        if slopes[i] <= 1:

            if eclipse == False:
                index += 1
                potential_eclipses.append([])

            potential_eclipses[index].append(i * binsize * lc.chandra_bin)
            eclipse = True

        else:
            eclipse = False

    return [cluster for cluster in potential_eclipses if len(cluster) > 1]
