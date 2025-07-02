import numpy as np

def NewtonIterSat(T, P, q_v, q_c):
    """
    Use Newton's method to evaluate vapor mixing ratio and the energy balance equation.

    Parameters:
        T (float): initial absolute temperature
        P (float): pressure (constant)
        q_v (float): water vapor mixing ratio
        q_s (float): water vapor mixing ratio for fully saturated air at a given temperature

    Return:
        delta_T (float): the change in temperature
        delta_q_v (float): the change in vapor mixing ratio

    Notes:
        Defined in ERF/Source/Microphysics/SatAdj/ERF_SatAdj.H
    """
    

def erf_esatw_cc(T):
    """
    Find the saturation vapor pressure of water for the given temperature. Use the Magnus formula for the approximate solution to the Clausius-Clapeyron equation.
    Called from erf_esatw.

    Parameter:
        T (float): absolute temperature

    Return:
        esatw (float): saturation vapor pressure of water.

    Notes:
        Defined in ERF/Source/Utils/ERF_MicrophysicsUtils.H
    """

def erf_esatw(T):
    """
    Find the saturation vapor pressure of water for the given temperature. Use one of two approximations, depending on dt = T - 273.16, the difference between
    the input temperature and the triple-point of water. For -85 < dt < 70, use the eighth-order polynomial approximation due to Flatau et al. (1992). 
    Otherwise, use the Magnus approximation for the Clausius-Clapeyron equation.

    Parameter:
        T (float): temperature

    Return:
        esatw (float): saturation vapor pressure of water

    Notes:
        Defined in ERF/Source/Utils/ERF_MicrophysicsUtils.H
    """

def erf_dtesatw_cc(T):
    # TODO: Not sure if this is needed. Double check.
    return

def erf_dtesatw(T):
    # TODO: Not sure if this is needed. Double check.
    return

def erf_qsatw(T, P):
    """
    Find the vapor mixing ratio for water at given temperature and pressure.

    Parameters:
        T: temperature
        P: pressure

    Notes:
        Defined in ERF/Source/Utils/ERF_MicrophysicsUtils.H
    """

def erf_dtqsatw(T, P):
    """
    Find the time derivative of the vapor mixing ratio for water at given temperature and pressure.

    Parameters:
        T: temperature
        P: pressure

    Notes:
        Defined in ERF/Source/Utils/ERF_MicrophysicsUtils.H
    """
