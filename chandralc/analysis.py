# dependencies
import matplotlib.pyplot as plt
from scipy import signal

def psd(lc):
    """Plots power spectral density for lightcurve.

    Parameters
    ----------
    lc: ChandraLightcurve
        ChandraLightcurve object
    Returns
    -------
    float
        Time period of frequency with maximum amplitude
    """

    f, Pxx_den = signal.periodogram(lc.raw_phot)
    plt.semilogx(f, Pxx_den)
    plt.xlabel('frequency [Hz]')
    plt.ylabel('PSD [V**2/Hz]')
    plt.show()

    return (1/f[list(Pxx_den).index(max(Pxx_den))])*3.241

def bin(lc, binsize):
    """Bins photon counts.

    Parameters
    ----------
    lc: ChandraLightcurve
        ChandraLightcurve object
    binsize : int
        Size of bin

    Returns
    -------
    list
        Array of bins
    """
    binned_photons = []

    # range: total number of df points over included bins --> temp3 of intervals
    for j in range(0, len(lc.raw_phot)//binsize):
        temp2 = 0
        j *= binsize
        for k in range(binsize):
            # sum of all photons within one interval
            temp2 = temp2 + lc.raw_phot[j+k]

        # appends that sum to a list
        binned_photons.append(temp2)

    return binned_photons