#!/usr/bin/env python

"""
PURPOSE:

To return the theoretical Limb Darkening coefficients and/or model
for observations taken with the MOST Satellite given the input
parameters.

This code makes use of the Claret, Dragomir, and Matthews (2014) A&A 567, A3
paper, which should be cited if you use this code:

http://adsabs.harvard.edu/abs/2014A%26A...567A...3C

Created on 2015-05-08T10:26:38
"""

from __future__ import division, print_function
import sys
import argparse

try:
    import numpy as np
except ImportError:
    print('You need numpy installed')
    sys.exit(1)

import pandas as pd
import limbDarkening
ld_dir = '/'.join(limbDarkening.__file__.split('/')[:-1])+'/'

__author__ = "Matt Giguere (github: @mattgiguere)"
__license__ = "MIT"
__version__ = '0.0.1'
__maintainer__ = "Matt Giguere"
__email__ = "matthew.giguere@yale.edu"
__status__ = " Development NOT(Prototype or Production)"


class LimbDarkening:
    """
    The main class that creates a limb darkening object.

    :param teff:
        The effective temperature in Kelvin

    :param logg:
        The log of the surface gravity
    """


################################################################
# USE THE CLARET LIMB DARKENING MODEL
################################################################
def getMOSTLDC(ld14fnm, monh, logg, teff, turbvel, passband):
    """This function will extract the limb darkening coefficients
    from the Claret table."""
    ldcs = np.zeros(4)
    coeffNames = ['a1', 'a2', 'a3', 'a4']
    idx = 0
    lddf = pd.read_csv(ld14fnm, sep='\s*\s*', engine='python', header=70)[2:]
    for cNm in coeffNames:
        ldcs[idx] = lddf[((lddf['Teff'] == '{:n}'.format(teff)) &
                         (lddf['logg'] == '{:.2f}'.format(logg)) &
                         (lddf['logZ'] == '{:.1f}'.format(monh)))][cNm].values[0]
        idx += 1
    return ldcs


def claret14_limb_darkening_coeffs():
    ld14fnm = ld_dir+'data/Claret2014MOST_ATLAS.tsv'

    teff = 5084.

    # specify the metalicity for the Claret Models (log [M/H]):
    monh = -0.13

    # specify the surface gravity:
    logg = 4.3

    # Turbulent Velocity for Claret Limn Dark Models (km/s):
    turbvel = 2.0

    # Round the setllar parameters for tabular lookup from
    # the Claret models for Limb Darkening:
    rteff = np.round(teff/250) * 250
    rmonh = np.round(monh/0.1) * 0.1
    rlogg = np.round(logg/0.5) * 0.5

    ldcs = getMOSTLDC(ld14fnm, rmonh, rlogg, rteff, turbvel, passband)
    return ldcs


def claret_model(ldcs):

    def limb_darkening_function(theta):
        mu = np.cos(theta)
        limbdark = 1. - ldcs[0] * (1. - mu**0.5)
        -  ldcs[1] * (1. - mu**1.0)
        -  ldcs[2] * (1. - mu**1.5)
        -  ldcs[3] * (1. - mu**2.0)
        return limbdark
    return limb_darkening_function

ldcs = claret14_limb_darkening_coeffs()
ld14func = claret_model(ldcs)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='argparse object.')
    parser.add_argument(
        'arg1',
        help='This argument does something.')
    parser.add_argument(
        'arg2',
        help='This argument does something else. By specifying ' +
             'the "nargs=>" makes this argument not required.',
             nargs='?')
    if len(sys.argv) > 3:
        print('use the command')
        print('python filename.py tablenum columnnum')
        sys.exit(2)

    args = parser.parse_args()

    claret_most_limb_darkening(int(args.arg1), args.arg2)
 