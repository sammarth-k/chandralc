"""Create configuration files."""

# PSL modules
import os
import inspect

# chandralc modules
from chandralc import convert
clc_path = os.path.dirname(inspect.getfile(convert))

def mpl_backend(switch=False):
    """Switches between agg and default matplotlib backend.
    
    Parameters
    ----------
    switch: bool
        Turn agg on or off, by default False
    """
    
    with open(clc_path + "/config/mpl_backend.chandralc", "w") as f:
        if switch is False:
            f.write("False")
        else:
            f.write("True")
