import ERF_Constants as const
import pandas as pd
import numpy as np
import argparse

from AdvanceSatAdj import AdvanceSatAdj
from NewtonIterSat import erf_qsatw, NewtonIterSat

parser = argparse.ArgumentParser()
parser.add_argument(
    "-N",
    "--num-samples",
    help="Number of samples to draw. Default is 1e4.",
    default=1e4,
)
parser.add_argument(
    "-v",
    "--verbose",
    help="Display summary statistics for output variables.",
    action="store_true",
)
parser.add_argument(
    "-f",
    "--file-name",
    help="Name of file to save (csv format). Default is 'samples.csv'",
    default="newton_samples.csv",
)

args = parser.parse_args()

# number of samples to generate
N = int(args.num_samples)

# Lower and upper bounds for absolute temperature and air pressure.
# Pressure does not take into account hydrostatic balance at present.
temp_range = (190, 323)
pres_range = (1e3, 1e5)

# We generate samples for vapor mixing ratio based on a multiple
# of the saturation mixing ratio, itself a function of temperature and pressure.
qv_multiplier_range = (0, 1.5)

# Lower and upper bounds for cloud mixing ratio
qc_range = (0, 5e-3)

# Use constant latent and specific heat for now
latent_heat = const.L_v
specific_heat = const.Cp_d

# Independent input variables
temp_in = np.random.uniform(temp_range[0], temp_range[1], N)
pres_in = np.random.uniform(pres_range[0], pres_range[1], N)
qc_in = np.random.uniform(qc_range[0], qc_range[1], N)

# Derived input variable(s)
# Set qv based on temperature and pressure
# Needs to use a loop b/c erf_qsatw contains conditional
# logic that isn't straightforward to vectorize.
qv_in = np.empty(N)
for i in range(N):
    qv_in[i] = np.random.uniform(
        qv_multiplier_range[0], qv_multiplier_range[1]
    ) * erf_qsatw(temp_in[i], pres_in[i])

# Constant input variables
latent_heat_samples = np.full(N, latent_heat)
specific_heat_samples = np.full(N, specific_heat)


# Initialize arrays for output variables
temp_out = np.empty(N)
qv_out = np.empty(N)
qc_out = np.empty(N)

for i in range(N):
    res = NewtonIterSat(temp_in[i], pres_in[i], qv_in[i], qc_in[i])
    temp_out[i] = res[0]
    qv_out[i] = res[1]
    qc_out[i] = res[2]

# Calculate deltas to report stats
delta_T = temp_in - temp_out
delta_qv = qv_in - qv_out
delta_qc = qc_in - qc_out

samples = np.column_stack(
    [
        temp_in,
        pres_in,
        qv_in,
        qc_in,
        latent_heat_samples,
        specific_heat_samples,
        temp_out,
        qv_out,
        qc_out,
        delta_T,
        delta_qv,
        delta_qc,
    ]
)

file_name = args.file_name

# Assemble data frame
col_names = [
    "T_in",
    "pres_in",
    "qv_in",
    "qc_in",
    "L",
    "Cp",
    "T_out",
    "qv_out",
    "qc_out",
    "delta T",
    "delta qv",
    "delta qc",
]
df = pd.DataFrame(samples, columns=col_names)

# Write to csv
df.to_csv(file_name, index=False)

if args.verbose:
    # Display stats for deltas
    print("Summary stats")
    print("\tmean delta T:", delta_T.mean())
    print("\tvariance in delta T:", delta_T.var())
    print("\tmax delta T:", delta_T.max())
    print("\tmin delta T:", delta_T.min())
    print("\tmin |delta T|:", np.abs(delta_T).min(), "\n")

    print("\tmean delta qv:", delta_qv.mean())
    print("\tvariance in delta qv:", delta_qv.var())
    print("\tmax delta qv:", delta_qv.var())
    print("\tmin delta qv:", delta_qv.min())
    print("\tmin |delta qv|:", np.abs(delta_qv).min(), "\n")

    print("\tmean delta qc:", delta_qc.mean())
    print("\tvariance in delta qc:", delta_qc.var())
    print("\tmax delta qc:", delta_qc.max())
    print("\tmin delta qc:", delta_qc.min())
    print("\tmin |delta qc|:", np.abs(delta_qc).min())
