from __future__ import division

import itertools
import operator

import numpy as np
from astropy.modeling import models, fitting


__all__ = ['fitmodels', 'fitmodels_simple']


def fitmodels(spectrum, model_initial_conds, fitmodels_type='simple',
               window=None, weights=None, *args, **kwargs):
    """
    Entry point for fitting using the ``astropy.modeling.fitting``
    machinery.

    Parameters
    ----------
    spectrum : Spectrum1D
        The spectrum object overwhich the equivalent width will be calculated.
    model_initial_conds : list of ``astropy.modeling.models``
        The list of models that contain the initial guess.
    fitmodels_type: str
        String representation of fit method to use as defined by the dict fitmodels_types.
    window : tuple of wavelengths  (NOT IMPLEMENTED YET)
        Start and end wavelengths used for fitting.
    weights : list  (NOT IMPLEMENTED YET)
        List of weights to define importance of fitting regions.

    Returns
    -------
    models : list of ``astropy.modeling.models``
        The list of models that contain the fitted model parmeters.

    """

    #
    #  Define the fit line methods that are available.
    #     str description  ->  fit method
    #

    fitmodels_types = {
        'simple': fitmodels_simple
    }

    if fitmodels_type in fitmodels_types.keys():
        return fitmodels_types[fitmodels_type](spectrum, model_initial_conds, 
                                                 *args, **kwargs)
    else:
        raise ValueError('Fit line type {} is not one of implmented {}'.format(
            fitmodels_type, fitmodels_types.keys()))


def fitmodels_simple(spectrum, model_initial_conds, fitter=fitting.SLSQPLSQFitter, window=None, weights=None):
    """
    Basic fitting of the input spectrum based on the initial conditions defined as a list
    of models with the initial conditions and bounds set.

    Parameters
    ----------
    spectrum : Spectrum1D
        The spectrum object overwhich the equivalent width will be calculated.
    models : list of ``astropy.modeling.models``
        The list of models that contain the initial guess.
    window : tuple of wavelengths  (NOT IMPLEMENTED YET)
        Start and end wavelengths used for fitting.
    weights : list  (NOT IMPLEMENTED YET)
        List of weights to define importance of fitting regions.

    Returns
    -------
    models : Compound model of ``astropy.modeling.models``
        A compound model of models with fitted parameters.

    Notes
    -----
       * Could add functionality to set the bounds in 
         `model_initial_conds`` if they are not set.
       * The models in the list of `model_initial_conds` are added
          together and passed as a compound model to the 
          ``astropy.modeling.fitter`` class instance.

    """

    #
    # Now to fit the data create a new superposition with initial
    # guesses for the parameters:
    #

    *_, compound_model = itertools.accumulate(model_initial_conds, operator.add)

    #
    # Do the fitting of spectrum to the model.
    #

    fitter_func = fitter()
    fitted_models = fitter_func(compound_model, spectrum.wavelength.value, spectrum.flux.value)

    #
    # Split up the combined model in the component form.
    #

    return fitted_models
