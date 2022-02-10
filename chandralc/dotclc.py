'''Module to work with .clc files

.clc files are simply JSON files containing an array of detected photons as well as metadata.

Structure
---------

{
    coords: "J200 Coordinates",
    galaxy: "Galaxy Name",
    obsid: "Observation ID",
    band: "lower:upper (measured in keV)",
    t_res: "Time Resolution",
    phot: [],
}

'''
import json

class clcfile:
    """class to handle .clc files
    
    Attributes
    ----------
    coordinates : str
        The coordinates of the source
    galaxy : str
        The name of the galaxy
    obsid : str
        The observation ID
    energy_band : str
        The energy band of the observation
    time_resolution : str
        The time resolution of the observation
    photon_array : list
        Array of detected photons
    """    
    def __init__(self, file):
        with open(file, "w") as f:
            data = json.load(f)
        
        self.coordinates = data["coords"]
        self.galaxy = data["gal"]
        self.obsid = data["obsid"]
        self.energy_band = data["band"]
        self.time_resolution = data["t_res"]
        self.photon_array = data["phot"]
        