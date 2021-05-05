# dependencies

# Python Standard Library Modules
import os
import requests
import time

# External Modules
from astropy.coordinates import SkyCoord
from astropy.table import Table
from astropy.io import fits
from astropy import units as u
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


# ----------------------------------------------------------


# Downloading databases

# list of galaxies with extracted lightcurves
dbs = ["M101", "M104", "M81", "M84", "M74"]


def download_db():
    """Download database index."""

    print("    Downloading File Databases...", end="\r")

    if "file_dbs" in os.listdir():
        return

    os.mkdir("./file_dbs")

    count = 1
    t = 0
    size = 0

    for db in dbs:
        start = time.time()

        url = f"https://raw.githubusercontent.com/sammarth-k/Chandra-Lightcurve-Download/main/file_dbs/{db}.csv"
        data = requests.get(url)

        file = open(f"./file_dbs/{db}.csv", "w", encoding="utf-8")
        file.write(data.text)
        file.close()

        size += len(data.text)

        end = time.time()

        t += (end-start)

        print(
            f"    Progress: {count} of {len(dbs)} downloaded | Total Size: {round(size/1024,2)} KB | Time Elapsed: {round(t,2)} seconds", end="\r")

        count += 1


download_db()


# ----------------------------------------------------------


# functions to extract and convert coordinates
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


# ----------------------------------------------------------


# functions to get filenames of extracted lightcurves


def get_files(galaxy):
    """Get a list of all files within a galaxy.

    Parameters
    ----------
    galaxy : str
        Messier object eg. M81

    Returns
    -------
    list
        List of all files in galaxy
    """

    # opening database of filenames for the particular galaxy
    filenames = open(f"./file_dbs/{galaxy}.csv", "r")

    # returns list of filenames
    files = [filename.strip("\n") for filename in filenames.readlines()]
    filenames.close()
    return files


def get_all_files():
    """Get the filenames of all available extracted lightcurves.

    Returns
    -------
    list
        List of all files in database
    """

    files = []

    # iterate through list of galaxies
    for db in dbs:

        # create a list of all available extracted lightcurves
        files += get_files(db)

    # returns a list of all available extracted lightcurves
    return files


# ----------------------------------------------------------


# Get name of galaxy containing the particular file
def get_galaxy(filename):
    """Get name of galaxy a file belongs to.j

    Parameters
    ----------
    filename : str
        Filename or filepath 

    Returns
    -------
    str
        Galaxy Messier name
    """
    # in case path is entered as argument
    filename = filename.split("/")[-1] if "/" in filename else filename

    for db in dbs:

        filenames = get_files(db)

        if filename in filenames:
            return db

    print("File not present in available extracted lightcurves")


# ----------------------------------------------------------


def coordinate_search(coordinates):
    """Search for files close to the given coordinates.

    Parameters
    ----------
    coordinates : str
        J2000 coordinates

    Returns
    -------
    list
        List of files near coordinates.
    """

    # get all filenames
    files = get_all_files()

    # getting ra and dec of search coordinates in degrees
    search_ra, search_dec = to_deg(coordinates)

    matching_files = []

    # counter variable
    count = 0

    for file in files:

        # extracting file coordinates in degrees from filename
        file_ra, file_dec = to_deg(extract_coords(file))

        # add file if within search radius
        ra_check = (file_ra*0.999995 <= search_ra <= file_ra*1.000005)
        dec_check = (file_dec*0.999995 <= search_dec <= file_dec*1.000005)

        if ra_check and dec_check:
            matching_files.append(file)

        print(f"{count+1} of {len(files)} searched", end="\r")
        count += 1

    # returns list of files with coordinates within the search radius
    return(matching_files)


# ----------------------------------------------------------


# downloading lightcurves from GitHub repository
def download_lcs(filenames, directory="."):
    """Download raw ligtcurves from database.

    Parameters
    ----------
    filenames : list
        List of filenames to download
    directory : str, optional
        Output directory of downloaded files, by default "."
    """

    import requests
    import time

    # variables for time and size
    t = 0
    size = 0

    # counter variable
    count = 1

    try:
        os.mkdir(directory)
    except:
        pass

    for filename in filenames:

        # timer
        start = time.time()

        # to get galaxy of file
        galaxy = get_galaxy(filename)

        # url of lightcurve
        url = f"https://raw.githubusercontent.com/sammarth-k/CXO-lightcurves/main/{galaxy}/textfiles/{filename}"

        # using a GET request to download lightcurve
        try:
            data = requests.get(url)

            # Exception in case of Error 404
            data.raise_for_status()

            # file size
            size += len(data.text)

            # saving to file
            file = open(directory + "/" + filename, "w", encoding="utf-8")
            file.write(data.text)
            file.close()

            # progress meter
            end = time.time()
            t += (end-start)

            print(
                f"    Progress: {count} of {len(filenames)} downloaded | Total Size: {round(size/1048576,2)} MB | Time Elapsed: {round(t,2)} seconds", end="\r")

            count += 1

        except requests.exceptions.HTTPError:
            print(
                f"{filename}: Error 404: Page Not Found. Please make sure you have used the correct filename")


# ----------------------------------------------------------


# to plot lightcurves

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
# ----------------------------------------------------------


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
            self.df = txt_to_df(file, header_check(file))
        elif "fits" in file:
            self.df = fits_to_df(file, header_check(file))

        chandra_bin = 3.241039999999654

        self.count_array = []

        count = 0

        # Creating counts array
        for index, row in self.df.iterrows():
            if self.df['EXPOSURE'][index] > 0:
                count += self.df.COUNTS[index]
            elif self.df['EXPOSURE'][index] == 0:
                count += 0

            self.count_array.append(count)

        # array for timestamps
        self.time_array = [chandra_bin / 1000 *
                           i for i in range(1, len(self.count_array) + 1)]

        # Lightcurve stats
        self.time = round(self.time_array[-1], 3)
        self.count = count
        self.rate_ks = round(self.count / self.time, 3)
        self.rate_s = round(self.count / (self.time * 1000), 5)

        # Source information
        file = file.split("_lc.fits")[0].split("_")
        self.obsid = file[1]
        self.coords = extract_coords(self.path)

        # raw data
        self.raw_phot = [self.df.COUNTS[i] if self.df.EXPOSURE[i] > 0 else 0 for i in range(len(self.df))]

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
        plt.plot(self.time_array, self.count_array, color=color)
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