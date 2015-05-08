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

    def __init__(self, teff, logg, monh, turbvel):
        self.fn = ld_dir+'data/Claret2014MOST_ATLAS.tsv'

        self.teff = teff
        self.monh = monh
        self.logg = logg
        self.turbvel = turbvel
        self.round_values()

    def round_values(self):
        """
        PURPOSE:
        To round the input parameters for lookup in the Claret table.
        """
        self.rteff = np.round(self.teff/250) * 250
        self.rmonh = np.round(self.monh/0.1) * 0.1
        self.rlogg = np.round(self.logg/0.5) * 0.5

    def get_data(self):
        """
        PURPOSE:
        Restore the data from file and return them as a pandas DataFrame.
        """
        return pd.read_csv(self.fn, sep='\s*\s*', engine='python', header=70)[2:]

    def get_ldcs(self):
        """
        PURPOSE:
        This function will extract and return the limb darkening coefficients
        from the Claret table.
        """
        ldcs = np.zeros(4)
        coeffNames = ['a1', 'a2', 'a3', 'a4']
        idx = 0
        lddf = self.get_data()
        for cNm in coeffNames:
            ldcs[idx] = lddf[((lddf['Teff'] == '{:n}'.format(self.rteff)) &
                             (lddf['logg'] == '{:.2f}'.format(self.rlogg)) &
                             (lddf['logZ'] == '{:.1f}'.format(self.rmonh)))][cNm].values[0]
            idx += 1
        return ldcs

    def claret_model(self, ldcs):

        def limb_darkening_function(theta):
            mu = np.cos(theta)
            limbdark = 1. - \
                ldcs[0] * (1. - mu**0.5) - \
                ldcs[1] * (1. - mu**1.0) - \
                ldcs[2] * (1. - mu**1.5) - \
                ldcs[3] * (1. - mu**2.0)
            return limbdark
        return limb_darkening_function


def claret14_limb_darkening_coeffs(teff, monh, logg, turbvel):
    """
    PURPOSE:
    To round the input values in order to extract the limb darkening
    coefficients from the Claret et al. (2014) table.

    :param teff:
    The stellar effective temperature in Kelvin

    :param monh:
    The stellar metalicity

    :param logg:
    The log of the stellar surface gravity

    :param turbvel:
    The stellar turbulent velocity

    See the Claret et al. (2014) paper for more details.
    """

    assert teff >= 3000, 'teff should be greater than 3000: {}'.format(teff)
    assert teff <= 50000, 'teff should be less than 50000: {}'.format(teff)
    assert monh >= -5.0, 'monh should be greater than -5.0: {}'.format(monh)
    assert monh <= 1.0, 'monh should be greater than 1.0: {}'.format(monh)
    assert logg >= 0.0, 'logg should be greater than 0.0: {}'.format(logg)
    assert logg <= 5.0, 'logg should be less than 5.0: {}'.format(logg)
    assert turbvel <= 8.0, 'turbvel should be less than 8.0: {}'.format(turbvel)
    assert turbvel >= 0.0, 'turbvel should be greater than 0.0: {}'.format(turbvel)

    ldo = LimbDarkening(teff, monh, logg, turbvel)
    print(ldo.get_ldcs())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='argparse object.')
    parser.add_argument(
        'teff',
        help='The stellar effective temperature.')
    parser.add_argument(
        'monh',
        help='The stellar metalicity')
    parser.add_argument(
        'logg',
        help='The log of the stellar surface gravity')
    parser.add_argument(
        'turbvel',
        help='The stellar turbulent velocity')

    args = parser.parse_args()

    claret14_limb_darkening_coeffs(int(args.teff), float(args.monh),
                                   float(args.logg), float(args.turbvel))
 