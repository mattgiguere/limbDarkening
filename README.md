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

####object-oriented example

To create a limb darkening object within the python environment:

    from limbDarkening.code import claret_most_limb_darkening as cld
    ldo = cld.LimbDarkening(5084, 4.3, -0.1, 2.0)

To get the four-parameter non-linear limb darkening coefficients:

    ldo.get_ldcs()
    array([ 0.5989, -0.548 ,  1.3669, -0.5722])

To return the full ATLAS table as a pandas DataFrame:

    lddf = ldo.get_data()
    lddf.head(3)

And to return the intensity as a function of $\gamma$, the angle between the line of sight and the outward surface normal

    ldfunc = ldo.claret_model(ldo.get_ldcs())

To plot this function over a range of $\gamma$:

    plt.rcParams['font.size']=20.
    gamma = np.linspace(-np.pi/2., np.pi/2., 1e2)
    ldfunc = ldo.claret_model(ldo.get_ldcs())
    intens = ldfunc(gamma)
    fig, ax = plt.subplots(1, 1)
    ax.plot(gamma, intens)
    ax.set_xlabel(r'$\gamma$ [radians]')
    ax.set_ylabel(r'$I(\mu)/I_0$')
    ax.set_ylim([0, 1.1])
    plt.subplots_adjust(left=0.15, right=0.9, top=0.9, bottom=0.2)
    nbins = 6
    ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=nbins, prune='both'))
    ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=nbins, prune='both'))

![Limb Darkening Function](figures/MOST_Limb_Darkening.png)