"""This module contains functions for machine learning."""

import numpy as np
np.seterr(divide='ignore', invalid='ignore')

def pmf(mu, k):
    """Probability mass function.

    Parameters
    ----------
    mu : float
        Mean of data
    k : float
        Number of occurences

    Returns
    -------
    float
        [description]
    """
    return ((mu**k) * (np.e**(-mu)))/np.math.factorial(k)


def to_standard_units(array):
    """Converts values to standard units.

    Parameters
    ----------
    array : numpy.ndarray
        Array of values in original units.

    Returns
    -------
    numpy.ndarray
        Array of values in standard units.
    """
    
    return (array - np.mean(array)) / np.std(array)


def calculate_r(x, y):
    """Calculates coefficient of correlation.

    Parameters
    ----------
    x : numpy.ndarray
        x-axis values
    y : numpy.ndarray
        y-axis values

    Returns
    -------
    float
        Coefficient of correlation
    """

    return np.mean(to_standard_units(x)*to_standard_units(y))


def linear_reg(x, y):
    """Creates a regression line.

    Parameters
    ----------
    x : numpy.ndarray
        x-axis values
    y : numpy.ndarray
        y-axis values

    Returns
    -------
    tuple
        x-axis and y-axis values as NumPy Arrays (x,y)
    """
    # calculating r
    r = calculate_r(x, y)

    # regression line
    std = np.std(y)
    mean = np.mean(y)

    y = to_standard_units(x) * r * std + mean

    return x, y


def rmse(actual, predicted):
    """Calculates root mean square error.

    Parameters
    ----------
    actual : numpy.ndarray
        Array of actual y values
    predicted : numpy.ndarray
        Array of actual x values

    Returns
    -------
    float
        Root mean square error
    """
    return np.sqrt(np.mean(actual - predicted)**2)

# creating function to return b0 and b1
def regression_equation(x,y):
    x,y = np.array(x), np.array(y)
    r = calculate_r(x,y)
    
    # regression line
    std = np.std(y)
    mean = np.mean(y)
    
    y = to_standard_units(x) * r * std + mean
    
    x,y = list(x),list(y)
    
    delta_y = y[1] - y[0]
    delta_x = x[1] - x[0]
    
    m = delta_y/delta_x
    c = y[0] - m * x[0]
        
    return m,c

def sigma_check(array, value, sigma=3):
     """Checks whether a value is greater than or equal to x standard deviations above the mean.
     
    Parameters
    ----------
    array : list
        Array of numbers
    value : float
        Value to check
    sigma : float
        Number of standard deviations above mean, by default 3
        
    Returns
    -------
    bool
        Wheter values is greater than or equal to or not
    """
    
    mean = np.mean(array)
    std = np.std(array)
    
    # checking
    if value >= mean + sigma * std:
        return True
    
    return False

def check_cluster(array, binsize=10, threshold=0.3):
    """Looks for clustering in in array.
    
    Parameters
    ----------
    array : list
        Array of numbers
    binsize : int
        Items per bin, by default 10
    threshold : float
        Threshold of clustering from 0 to 1, by default 0.3
        
    Returns
    -------
    list
        Array of timestamps with clustering of potential flares
    """
    
    bins = analysis.bin_toarrays(array, binsize)
    
    # assigns 0 or 1 to s     
    slope_clusters = [[1 if bins[i][j] > 0 else 0 for j in range(binsize)] for i in range(len(bins))]
    
    # adds timestamps if bin meets or exceeds threshold
    clusters = [array[i*binsize] for i in range(len(bins)) if np.sum(slope_clusters[i])/binsize >= threshold]
            
    return clusters
