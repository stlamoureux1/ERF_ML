import NewtonIterSat
import ERF_Constants as const
import numpy as np


def AdvanceSatAdj(T, P, qv, qc):
    """
    Calculate temperature and moisture mixing ratio adjustments. This functions applies
    some conditional logic depending on available moisture.

    Parameters:
        T: absolute temperature
        P: pressure
        qv: vapor mixing ratio
        qc: cloud mixing ratio

    Return:
        T, qv, qc

    Notes:
        Defined in ERF/Source/Microphysics/SatAdj/ERF_SatAdj.cpp
    """

    # Assign these values so that they can be adjusted inside the conditionals 
    # and return outside of them.
    T_new, qv_new, qc_new = 0., 0., 0.

    # Use constant d_fac_cond as in NewtonIterSat.py
    d_fac_cond = const.L_v / const.Cp_d
    rdOcp = const.R_d / const.Cp_d

    qc = max(0.0, qc)

    qsat = NewtonIterSat.erf_qsatw(T, P)

    if qv + qc > qsat:
        T_new, qv_new, qc_new = NewtonIterSat.NewtonIterSat(T, P, qv, qc)

    else:
        delta_qc = qc
        qv += qc
        qc = 0.0

        T_new = T - d_fac_cond * delta_qc

        qsat = NewtonIterSat.erf_qsatw(T, P)

        if qv > qsat:
            T_new, qv_new, qc_new = NewtonIterSat.NewtonIterSat(T, qv, qc)

        else:
            qv_new, qc_new = qv, qc

    return T_new, qv_new, qc_new
