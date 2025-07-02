import numpy as np
import ERF_Constants as const


def NewtonIterSat(T, P, qv, qc):
    """
    Use Newton's method to evaluate vapor mixing ratio and the energy balance equation.

    Parameters:
        T (float): initial absolute temperature
        P (float): pressure (constant)
        qv (float): water vapor mixing ratio
        q_s (float): water vapor mixing ratio for fully saturated air at a given temperature

    Return:
        delta_T (float): the change in temperature
        delta_qv (float): the change in vapor mixing ratio

    Notes:
        Defined in ERF/Source/Microphysics/SatAdj/ERF_SatAdj.H
    """
    # For now, use constant fac_cond.
    # Ratio of latent heat to specific heat, used in calculation of q_s
    fac_cond = const.L_v / const.Cp_d

    # Solution tolerance
    tol = 1.0e-8

    # Initial guess for temperature.
    # Will be updated as part of balance calculation.
    T_new = T

    # Newton iteration vars
    niter = 0
    dT = 1

    # ==================================================
    # Newton iteration to qv=qsat (cloud phase only)
    # ==================================================

    # Emulate do-while loop in original using break stmt.
    while True:
        # Saturation moisture fractions
        qsat = erf_qsatw(T, P)
        dqsat = erf_dtqsatw(T, P)

        # Function for root finding:
        # 0 = -T_new + T_old + L_eff/C_p * (qv - qsat)
        fff = -T_new + T + fac_cond * (qv - qsat)

        # Derivative of function (T_new iterated on)
        dfff = -1.0 - fac_cond * dqsat

        # Update the temperature
        dT = -fff / dfff
        T_new += dT

        # Update iteration
        niter += 1

        print(qsat)
        print(T_new)

        if np.abs(dT) < tol or niter > 20:
            break

    # Update qsat from last iteration (dq = dq/dt * dt)
    qsat += dqsat * dT

    delta_qv = qv - qsat

    # NOTE: not sure what these are used for, if at all in this case
    qv = qsat
    qc += delta_qv

    delta_T = T_new - T

    return delta_T, delta_qv


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
    svp1 = 0.6112
    svp2 = 17.67
    svp3 = 29.65
    svpt0 = 273.15
    esatw = 10.0 * svp1 * np.exp(svp2 * (T - svpt0) / (T - svp3))
    return esatw


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
    a0 = 6.11239921
    a1 = 0.443987641
    a2 = 0.142986287e-1
    a3 = 0.264847430e-3
    a4 = 0.302950461e-5
    a5 = 0.206739458e-7
    a6 = 0.640689451e-10
    a7 = -0.952447341e-13
    a8 = -0.976195544e-15

    dtt = T - 273.16
    if dtt > -85 and dtt < 70.0:
        esatw = a0 + dtt * (
            a1
            + dtt
            * (
                a2
                + dtt
                * (a3 + dtt * (a4 + dtt * (a5 + dtt * (a6 + dtt * (a7 + a8 * dtt)))))
            )
        )
    else:
        esatw = erf_esatw_cc(T)
    return esatw


def erf_dtesatw_cc(T):
    svp1 = 0.6112
    svp2 = 17.67
    svp3 = 29.65
    svpt0 = 273.15
    dtesatw = (
        10.0
        * svp1
        * svp2
        * np.exp(svp2 * (T - svpt0) / (T - svp3))
        * (svpt0 - svp3)
        / ((T - svp3) * (T - svp3))
    )
    return dtesatw


def erf_dtesatw(T):
    a0 = 0.443956472
    a1 = 0.285976452e-1
    a2 = 0.794747212e-3
    a3 = 0.121167162e-4
    a4 = 0.103167413e-6
    a5 = 0.385208005e-9
    a6 = -0.604119582e-12
    a7 = -0.792933209e-14
    a8 = -0.599634321e-17

    dtt = T - 273.16  # Goff-Gratch
    if dtt > -85.0 and dtt < 70.0:
        dtesatw = a0 + dtt * (
            a1
            + dtt
            * (
                a2
                + dtt
                * (a3 + dtt * (a4 + dtt * (a5 + dtt * (a6 + dtt * (a7 + a8 * dtt)))))
            )
        )
    else:
        dtesatw = erf_dtesatw_cc(T)
    return dtesatw


def erf_qsatw(T, P):
    """
    Find the vapor mixing ratio for water at given temperature and pressure.

    Parameters:
        T: temperature
        P: pressure

    Notes:
        Defined in ERF/Source/Utils/ERF_MicrophysicsUtils.H
    """
    esatw = erf_esatw(T)
    qsatw = const.Rd_on_Rv * esatw / max(esatw, P - esatw)
    return qsatw


def erf_dtqsatw(T, P):
    """
    Find the time derivative of the vapor mixing ratio for water at given temperature and pressure.

    Parameters:
        T: temperature
        P: pressure

    Notes:
        Defined in ERF/Source/Utils/ERF_MicrophysicsUtils.H
    """
    esatw = erf_esatw(T)
    dtesatw = erf_dtesatw(T)
    denom = P - esatw
    dtqsatw = const.Rd_on_Rv * dtesatw * P / (denom * denom)
    return dtqsatw
