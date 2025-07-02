"""
Constants defined in ERF/Source/ERF_Constants.H
"""

PI           = 3.14159265358979323846264338327950288;
PIoTwo       = PI/2.0;

# Physical Constants
R_d          = 287.0;    # dry air constant for dry air [J/(kg-K)]
R_v          = 461.505;  # water vapor constant for water vapor [J/(kg-K)]
Cp_d         = 1004.5;   # We have set this so that with qv=0 we get identically gamma = 1.4
Cp_v         = 1859.0;
Cp_l         = 4200.0;

L_v          = 2.5e6;    # latent heat of vaporization (J / kg)

p_0          = 1.0e5;    # reference surface pressure [Pa]
Gamma        = 1.4;      # c_p / c_v [-]
KAPPA        = 0.41;     # von Karman constant
CONST_GRAV   = 9.81;

# Derived Constants
ip_0         = 1./p_0;
iR_d         = 1./R_d;
iGamma       = 1./Gamma;

rhor         = 1000.; # Density of water, kg/m3
rhos         = 100.;  # Density of snow, kg/m3
rhog         = 400.;  # Density of graupel, kg/m3
tbgmin       = 253.16;    # Minimum temperature for cloud water., K
tbgmax       = 273.16;    # Maximum temperature for cloud ice, K
tprmin       = 268.16;    # Minimum temperature for rain, K
tprmax       = 283.16;    # Maximum temperature for snow+graupel, K
tgrmin       = 223.16;    # Minimum temperature for graupel, K
tgrmax       = 283.16;    # Maximum temperature for graupel, K

a_rain       = 842.;   # Coeff.for rain term vel
b_rain       = 0.8;    # Fall speed exponent for rain
a_snow       = 4.84;   # Coeff.for snow term vel
b_snow       = 0.25;   # Fall speed exponent for snow
a_grau       = 94.5;   # Lin (1983) (rhog=400)
b_grau       = 0.5;    # Fall speed exponent for graupel

# Autoconversion
qcw0         = 1.e-3;  # Threshold for water autoconversion, g/g
qci0         = 1.e-4;  # Threshold for ice autoconversion, g/g
alphaelq     = 1.e-3;  # autoconversion of cloud water rate coef
betaelq      = 1.e-3;  # autoconversion of cloud ice rate coef

erccoef      = 1.0;    # Rain/Cloud water collection efficiency
esccoef      = 1.0;    # Snow/Cloud water collection efficiency
esicoef      = 0.1;    # Snow/cloud ice collection efficiency
egccoef      = 1.0;    # Graupel/Cloud water collection efficiency
egicoef      = 0.1;    # Graupel/Cloud ice collection efficiency

nzeror       = 8.e6;   # Intercept coeff. for rain
nzeros       = 3.e6;   # Intersept coeff. for snow
nzerog       = 4.e6;   # Intersept coeff. for graupel
qp_threshold = 1.e-8;  # minimal rain/snow water content

boltz    = 1.38065e-23;
avogadro = 6.02214e26;
mwdair   = 28.966;
mwwv     = 18.016;
lcond    = 2.501e6;
lfus     = 2.11727e3;
lsub     = lcond+lfus;
rair     = boltz*avogadro/mwdair;
rh20     = rair/mwwv;
rga      = 1.0/CONST_GRAV;

diffelq = 2.21e-05;     # Diffusivity of water vapor, m2/s
therco  = 2.40e-02;     # Thermal conductivity of air, J/m/s/K
muelq   = 1.717e-05;    # Dynamic viscosity of air

a_bg = 1.0/(tbgmax-tbgmin);
a_pr = 1.0/(tprmax-tprmin);
a_gr = 1.0/(tgrmax-tgrmin);

crain = b_rain / 4.0;
csnow = b_snow / 4.0;
cgrau = b_grau / 4.0;

lat_vap  = 2.5e6;     # Latent heat of vaporization (J/kg)
lat_ice  = 3.337e5;   # latent heat of fusion (J/kg)
Rd_on_Rv = R_d/R_v;
tmelt    = 273.15;  # melting temp.
h2otrip  = 273.15;  # Triple point temperature of water (K)
tboil    = 373.16;  # Boiling point of water at 1 atm (K)
ttrice   = 20.00;   # transition range from es over H2O to es over ice
epsilo   = Rd_on_Rv;
omeps    = 1. - epsilo;
rhoh2o   = 1.000e3;  # density of liquid water

ORB_UNDEF_INT  = 2000000000;  # undefined int
