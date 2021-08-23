"""Module to access NASA ADS Database for research related to a source"""

# PSL modules
import webbrowser
import datetime
import csv
import os

# chandralc modules
from chandralc import convert
from chandralc import download


def _log(url):
    """Logs ADS queries."""

    # add record
    with open("./logs/ads.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.now(), url])


def search_ads(file, radius, browser=True):
    """Opens browser and queries NASA ADS for matches.

    Parameters
    ----------
    file: str
        filename of lightcurve
    radius: int
        search radius
    """

    # get coordinates from file path
    coords = convert.extract_coords(file).split()

    # get ra, dec
    ra = f"{coords[0]}h{coords[1]}m{coords[2]}s"
    dec = f"{coords[3][1:]}d{coords[4]}m{coords[5]}s"

    pm = "%2B" if "+" in file else "%2D"

    query = f"{ra} {pm}{dec}%3A{radius}"

    # url for query
    url = f'http://ui.adsabs.harvard.edu/search/q=object%3A"{query}"'

    # log query
    _log(url)

    if browser:
        webbrowser.open(url)
    return url
