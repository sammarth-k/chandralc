"""This module contains functions to download data from the online locations."""

# Python Standard Library Modules
import os
import csv
import time
import requests
import inspect

# chandralc modules
from chandralc import convert

# ----------------------------------------------------------

clc_path = os.path.dirname(inspect.getfile(convert))
# Downloading databases

# list of galaxies with extracted lightcurves
dbs1 = [
    "M101",
    "M104",
    "M31",
    "M49",
    "M74",
    "M81",
    "M83",
    "M84",
    "M87",
    "NGC1399",
    "NGC5128",
    "NGC6946",
    "LMC",
    "SMC",
]
dbs2 = ["M51", "NGC4736", "NGC1313", "M82", "M33"]
dbs = dbs1 + dbs2
repos = [dbs1, dbs2]


def download_db():
    """Download database index."""
    if "file_dbs" not in os.listdir(clc_path):
        os.mkdir(clc_path + "/file_dbs")
    
        count = 1
        total_time = 0
        size = 0

        for repo in repos:

            for db in repo:

                start = time.time()

                url = f"https://raw.githubusercontent.com/sammarth-k/Chandra-Lightcurve-Download/main/file_dbs/{db}.csv"
                data = requests.get(url)

                with open(f"{clc_path}/file_dbs/{db}.csv", "w", encoding="utf-8") as file:
                    file.write(data.text)

                size += len(data.text)

                end = time.time()

                total_time += end - start

                print(
                    f"Progress: {count} of {len([db for repo in repos for db in repo])} downloaded | Total Size: {round(size/1024,2)} KB | Time Elapsed: {round(total_time,2)} seconds",
                    end="\r",
                )

                count += 1
            
    elif "file_dbs" in os.listdir():
        count = 1
        total_time = 0
        size = 0

        for repo in repos:

            for db in repo:
                
                if f"{db}.csv" not in os.listdir(clc_path + "/file_dbs"):

                    start = time.time()

                    url = f"https://raw.githubusercontent.com/sammarth-k/Chandra-Lightcurve-Download/main/file_dbs/{db}.csv"
                    data = requests.get(url)

                    with open(f"{clc_path}/file_dbs/{db}.csv", "w", encoding="utf-8") as file:
                        file.write(data.text)

                    size += len(data.text)

                    end = time.time()

                    total_time += end - start

                    print(
                        f"Progress: {count} of {len(dbs)} downloaded | Total Download Size: {round(size/1024,2)} KB | Time Elapsed: {round(total_time,2)} seconds",
                        end="\r",
                    )

                count += 1

        return


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
    with open(f"{clc_path}/file_dbs/{galaxy}.csv", "r") as fnames:
        files = [file[0] for file in csv.reader(fnames)]

    # returns array of all files
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
    for repo in repos:
        for db in repo:
            # create a list of all available extracted lightcurves
            files += get_files(db)

    # returns a list of all available extracted lightcurves
    return files


def get_galaxy(filename):
    """Get name of galaxy a file belongs to.

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

    for repo in repos:

        for db in repo:

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
    search_ra, search_dec = convert.to_deg(coordinates)

    matching_files = []

    # counter variable
    count = 0

    for file in files:

        # extracting file coordinates in degrees from filename
        file_ra, file_dec = convert.to_deg(convert.extract_coords(file))

        # add file if within search radius
        ra_check = file_ra * 0.999995 <= search_ra <= file_ra * 1.000005
        dec_check = file_dec * 0.999995 <= search_dec <= file_dec * 1.000005

        if ra_check and dec_check:
            matching_files.append(file)

        print(f"{count+1} of {len(files)} searched", end="\r")
        count += 1

    # returns list of files with coordinates within the search radius
    return matching_files


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

        # getting repo number
        repo_num = 0
        for i in range(len(repos)):
            if galaxy in repos[i]:
                repo_num = i + 1
                break

        # url of lightcurve
        url = f"https://raw.githubusercontent.com/sammarth-k/CXO-lightcurves{repo_num}/main/{galaxy}/textfiles/{filename}"

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
            t += end - start

            print(
                f"    Progress: {count} of {len(filenames)} downloaded | Total Size: {round(size/1048576,2)} MB | Time Elapsed: {round(t,2)} seconds",
                end="\r",
            )

            count += 1

        except requests.exceptions.HTTPError:
            print(
                f"{filename}: Error 404: Page Not Found. Please make sure you have used the correct filename"
            )
