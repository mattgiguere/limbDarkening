# limbDarkening
Create limb darkening models using the Claret (2000), Claret et al. (2013), or Claret et al. (2014) models

# code

All code is contained within the `code` subdirectory. Below is a description of the files in that directory, and how to use them:

##claret_most_limb_darkening.py

`claret_most_limb_darkening.py` is a routine that uses the Claret, Dragomir, Matthews (2014) MOST limb darkening model. If you use this code, please cite that paper, which can be found [here](http://adsabs.harvard.edu/abs/2014A%26A...567A...3C).

###example

`claret_most_limb_darkening` can be used either via the command line, or by creating an object using the `LimbDarkening` class.

####command line example
    cd limbDarkening/code

To see usage help, use the --help argument:

    ./claret_most_limb_darkening --help
    usage: claret_most_limb_darkening.py [-h] teff monh logg turbvel    

    argparse object.    

    positional arguments:
      teff        The stellar effective temperature.
      monh        The stellar metalicity
      logg        The log of the stellar surface gravity
      turbvel     The stellar turbulent velocity    

    optional arguments:
      -h, --help  show this help message and exit

To get the four-parameter non-linear limb darkening coefficients:

    ./claret_most_limb_darkening 5084 -0.1 4.3 2.0
    [ 0.5989 -0.548   1.3669 -0.5722]