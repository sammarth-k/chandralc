"""This module contains functions to download data from the online locations."""

# Python Standard Library Modules
import os
import csv
import time
import requests
import inspect
import concurrent.futures
import json

# chandralc modules
from chandralc import convert

# ----------------------------------------------------------

clc_path = os.path.dirname(inspect.getfile(convert))
# Downloading databases

# list of galaxies with extracted lightcurves
if "file_dbs" not in os.listdir(clc_path):
    os.mkdir(clc_path + "/file_dbs")

# updating local copy of dbs.json
db_data = requests.get(
    "https://raw.githubusercontent.com/sammarth-k/chandralc/main/file_dbs/dbs.json"
).text

with open(f"{clc_path}/file_dbs/dbs.json", "w+") as f:
    f.write(db_data)
    f.flush()
    f.seek(0)
    json_data = json.load(f)

# data variables
dbs = []
for db in json_data:
    exec(f"{db} = json_data[db]")
    dbs += [db]

repos = list(json_data.values())[:-1]


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

                with open(
                    f"{clc_path}/file_dbs/{db}.csv", "w", encoding="utf-8"
                ) as file:
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

                    with open(
                        f"{clc_path}/file_dbs/{db}.csv", "w", encoding="utf-8"
                    ) as file:
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


def coordinate_search(coordinates, radius):
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

    # converting radius from arcseconds to degrees
    radius = radius * 0.000277778

    for file in files:

        # extracting file coordinates in degrees from filename
        file_ra, file_dec = convert.to_deg(convert.extract_coords(file))

        # add file if within search radius
        ra_check = file_ra - radius <= search_ra <= file_ra + radius
        dec_check = file_dec - radius <= search_dec <= file_dec + radius

        if ra_check and dec_check:
            matching_files.append(file)

        print(f"{count+1} of {len(files)} searched", end="\r")
        count += 1

    # returns list of files with coordinates within the search radius
    return matching_files


# ----------------------------------------------------------


# downloading lightcurves from GitHub repository
def download_lcs_unthreaded(filenames, directory="."):
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

        # skip files which have been downloaded
        if filename in os.listdir():
            continue

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
                f"    Progress: {count} of {len(filenames)} downloaded | Total Size: {round(size/1048576,2)} MB | Time Elapsed: {round(t,2)} seconds | Speed: {round(size/(1048576*t),2)}                  ",
                end="\r",
            )

            count += 1

        except requests.exceptions.HTTPError:
            print(
                f"{filename}: Error 404: Page Not Found. Please make sure you have used the correct filename"
            )


# ----------------------------------------------------------


def download_lc(file):
    galaxy = get_galaxy(file)

    # getting repo number
    repo_num = 0
    for i in range(len(repos)):
        if galaxy in repos[i]:
            repo_num = i + 1
            break

    # url of lightcurve
    url = f"https://raw.githubusercontent.com/sammarth-k/CXO-lightcurves{repo_num}/main/{galaxy}/textfiles/{file}"

    data = requests.get(url).text
    all_data["files"] += 1
    with open(f"{file}", "w", encoding="utf-8") as f:
        f.write(data)

    print(
        f"Downloaded {all_data['files']} of {download_total} | Time Elapsed: {round(time.time() - download_start,2)}s | Rate: {round((all_data['files'])/(time.time() - download_start),2)} files/s                  ",
        end="\r",
    )


def download_lcs(files, directory=".", threads=3):

    print("Your download will begin shortly...     ", end="\r")

    # creating global variables
    global download_start, all_data, download_total

    # download start time
    download_start = time.time()

    # data storage list
    all_data = {"files": 0}

    # total number of files
    download_total = len(files)

    print(f"Creating directory {directory}...          ", end="\r")

    try:
        os.mkdir(directory)
    except:
        pass
    finally:
        os.chdir(directory)

    print(f"Starting Download...                                       ", end="\r")

    # multithread processing
    with concurrent.futures.ThreadPoolExecutor(threads) as executor:

        # mapping function over files
        executor.map(download_lc, files)

    # delete `all_data` list
    del all_data


def galaxy_download(galaxy, directory=None, threads=3):
    directory = galaxy if directory is None else directory
    download_lcs(get_files(galaxy), directory, threads)
