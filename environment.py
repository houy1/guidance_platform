# -*- coding: UTF-8 -*-
import numpy as np
from scipy import interpolate

def atmoscoesa(height):
    ''' Use 1976 COESA model. 1976 U.S Standard Atmosphere Interpolation.
    Args:
        geomAlt : geopotential heights, in meters. : float

    Returns:
        T : temperatures, in kelvin.
        a : speeds of sound, in meters per second.
        P :  pressures, in pascal.
        Rou : densities, in kilograms per meter cubed.
    '''
    # TODO : different from matlab atmoscoesa
    # Values Tabulated by Geomeyric Altitude
    # real value
    Z = np.array([-1000., 0., 1000., 2000., 3000., 4000., 5000., 6000., 7000., 8000., 9000., 10000., 15000., 20000., 25000., 30000., 
        40000., 50000., 60000., 70000., 80000.])
    # pressure
    r_ppo = np.array([1.139e+01, 1.013e+01, 8.988e+00, 7.950e+00, 7.012e+00, 6.166e+00,
        5.405e+00, 4.722e+00, 4.111e+00, 3.565e+00, 3.080e+00, 2.650e+00,
        1.211e+00, 5.529e-01, 2.549e-01, 1.197e-01, 2.870e-02, 7.978e-03,
        2.196e-03, 5.200e-04, 1.100e-04])
    # density
    r_rro = np.array([1.347e+00, 1.225e+00, 1.112e+00, 1.007e+00, 9.093e-01, 8.194e-01,
        7.364e-01, 6.601e-01, 5.900e-01, 5.258e-01, 4.671e-01, 4.135e-01,
        1.948e-01, 8.891e-02, 4.008e-02, 1.841e-02, 3.996e-03, 1.027e-03,
        3.097e-04, 8.283e-05, 1.846e-05])
    # temperature
    r_T = np.array([21.5, 15., 8.5, 2., -4.49, -10.98, -17.47, -23.96, -30.45, -36.94, -43.42, -49.9, -56.5, -56.5, -51.6, -46.64,
        -22.8, -2.5, -26.13, -53.57, -74.51])
    r_T = r_T + 273.15
    # soundspeed
    r_a = np.array([344.1108, 340.2941, 336.4341, 332.5293, 328.5780, 324.5787, 320.5295, 316.4285, 312.2736, 308.0627, 303.7934,
        299.4633, 295.0696, 295.0696, 298.4551, 301.8026, 317.6327, 329.7988, 314.0701, 295.6139, 281.1202])
    
    geopAlt = np.array([height])

    # Linear Interpolation in Geopotential  Altitude
    # for Temperature and Speed of Sound
    f_T = interpolate.interp1d(Z,r_T, fill_value='extrapolate')
    T = f_T(geopAlt)[0]
    f_a = interpolate.interp1d(Z,r_a, fill_value='extrapolate')
    a = f_a(geopAlt)[0]
    f_ppo = interpolate.interp1d(Z,r_ppo, fill_value='extrapolate')
    P = f_ppo(geopAlt)[0]
    f_rro = interpolate.interp1d(Z,r_rro, fill_value='extrapolate')
    Rou = f_rro(geopAlt)[0]

    return T, a, P, Rou


if __name__ == '__main__':
    data = np.loadtxt('Air_properties.txt')
    print(data)
    print(data.shape)
