import numpy as np
import matplotlib.pyplot as plt

def pmf(mu,k):
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

# creating a function to convert values to standard units
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
    return (array - np.average(array)) / np.std(array)

# creating function to calculate r
def calculate_r(x,y):
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
    
    return np.average(to_standard_units(x), to_standard_units(y))

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
    r = calculate_r(x,y)
    
    # regression line
    std = np.std(y)
    mean = np.mean(y)
    
    y = to_standard_units(x)* r * std + mean

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