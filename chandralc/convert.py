# dependencies
from astropy.coordinates import SkyCoord
from astropy.table import Table
from astropy.io import fits
from astropy import units as u
import pandas as pd


def to_deg(coordinates):
    """Convert J2000 coordinates to degrees.

    Parameters
    ----------
    coordinates : str
        J2000 coordinates

    Returns
    -------
    tuple
        (ra, dec) in degrees
    """

    # using SkyCoord function from astropy to convert HMS to degrees
    c = SkyCoord(coordinates, unit=(u.hourangle, u.deg))

    # using string manipulation to extract coordinates from SkyCoord object
    coordinates = tuple(map(float, str(c).split(
        "deg")[1].strip(">,\n, ),(").split(", ")))
    return coordinates


def extract_coords(filename):
    """Extract J2000 coordinates from filename or filepath

    Parameters
    ----------
    filename : str
        name or path of file

    Returns
    -------
    str
        J2000 coordinates
    """

    # in case path is entered as argument
    filename = filename.split("/")[-1] if "/" in filename else filename
    # to check whether declination is positive or negative
    plus_minus = "+" if "+" in filename else "-"

    # extracting right acesnsion (ra) and declination(dec) from filename
    filename = filename.split("_")[0].strip("J").split(plus_minus)
    ra = ["".join(filename[0][0:2]), "".join(
        filename[0][2:4]), "".join(filename[0][4:])]
    dec = ["".join(filename[1][0:2]), "".join(
        filename[1][2:4]), "".join(filename[1][4:])]

    coordinates = " ".join(ra) + " " + plus_minus + " ".join(dec)

    # return coordinates as a string in HH MM SS.SSS format
    return coordinates


def header_check(file):
    """Checks whether the file has a header or not.

    Parameters
    ----------
    file : str
        Filename or filepath of file to check

    Returns
    -------
    int
        1 if header is present 0 if not
    """
    file = open(file, "r", encoding="utf-8")
    result = file.read(1).isalpha()
    file.close()
    return int(result)


def txt_to_df(file, header):
    """Converts TXT lightcurve file to Pandas DataFrame.

    Parameters
    ----------
    file : str
        Filename or filepath
    header : int
        To skip header if present.

    Returns
    -------
    pandas.core.frame.DataFrame
        Lightcurve as a DataFrame
    """

    cols = ['TIME_BIN', 'TIME_MIN', 'TIME', 'TIME_MAX', 'COUNTS',
            'STAT_ERR', 'AREA', 'EXPOSURE', 'COUNT_RATE', 'COUNT_RATE_ERR']

    df = pd.read_csv(file, skiprows=header, names=cols, sep=" ")
    return df


def fits_to_df(file, header):
    """Converts FITS lightcurve file to Pandas DataFrame.

    Parameters
    ----------
    file : str
        Filename or filepath
    header : int
        To skip header if present

    Returns
    -------
    pandas.core.frame.DataFrame
        Lightcurve as a DataFrame
    """

    # list of columns
    cols = "TIME_BIN TIME_MIN TIME TIME_MAX COUNTS STAT_ERR AREA EXPOSURE COUNT_RATE COUNT_RATE_ERR"
    cols = cols.split(" ")

    # accessing fits data
    hdu_list = fits.open(file, memmap=True)
    evt_data = Table(hdu_list[1].data)

    # initialising DataFrame
    df = pd.DataFrame()

    # writing to dataframe
    for col in cols:
        exec(f"df['{col}']=list(evt_data['{col}'])")

    return df