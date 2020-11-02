# -*- coding: UTF-8 -*-
import numpy as np
from scipy import interpolate

def atmoscoesa(geomAlt):
    ''' Use 1976 COESA model. 1976 U.S Standard Atmosphere Interpolation.
    Args:
        geomAlt : geometric Altitude, in meters : float

    Returns:
        T : temperatures, in kelvin.
        a : speeds of sound, in meters per second.
        P :  pressures, in pascal.
        Rou : densities, in kilograms per meter cubed.
    '''
    # TODO : different from matlab atmoscoesa
    # Values Tabulated by Geomeyric Altitude
    # real value
    Z = np.array([-10,0, 2500,5000, 10000, 11100, 15000, 20000, 47400, 51000])
    H = np.array([-10, 0,2499,4996,9984,11081,14965,19937,47049,50594])
    # pressure
    r_ppo = np.array([1,1,0.737,0.533,0.262,0.221,0.12,0.055,0.0011,0.0007])
    # density
    r_rro = np.array([1,1,0.781,0.601,0.338,0.293,0.159,0.073,0.0011,0.0007])
    # temperature
    r_T = np.array([288.15,288.15,271.906,255.676,223.252,216.65,216.65,216.65,270.65,270.65])
    # soundspeed
    r_a = np.array([340.294,340.294,330.563,320.545,299.532,295.069,295.069,295.069,329.799,329.799])
    
    R = 6367435
    Dens = 1.225
    Pres = 101325
    # Geopotential Altitude,m
    # geopAlt = R * geomAlt / (R + geomAlt)
    geopAlt = geomAlt
    geopAlt = np.array([geopAlt])

    if geopAlt < 1:
        geopAlt = np.array([1])

    # initial value
    P = 0
    Rou = 0
    # Linear Interpolation in Geopotential  Altitude
    # for Temperature and Speed of Sound
    f_T = interpolate.interp1d(Z,r_T, fill_value='extrapolate')
    T = f_T(geopAlt)[0]
    f_a = interpolate.interp1d(Z,r_a, fill_value='extrapolate')
    a = f_a(geopAlt)[0]
    # Exponential Interpolation in Geometric Altitude for Air Density and
    # Pressure
    for k in range(1, 10):
        if geomAlt <= Z[k]:
            betap = np.log(r_ppo[k] / r_ppo[k-1]) / (Z[k]-Z[k-1])
            betar = np.log(r_rro[k] / r_rro[k-1]) / (Z[k]-Z[k-1])
            P = Pres * r_ppo[k - 1] * np.exp(betap * (geomAlt - Z[k - 1]))
            Rou = Dens * r_rro[k - 1] * np.exp(betar * (geomAlt - Z[k - 1]))
            break
    
    return T, a, P, Rou
    # for k=2:10
    #     if geomAlt<=Z(k)
    #         betap=log(ppo(k)/ppo(k-1))/(Z(k)-Z(k-1));
    #         betar=log(rro(k)/rro(k-1))/(Z(k)-Z(k-1));
    #         P=Pres*ppo(k-1)*exp(betap*(geomAlt-Z(k-1)));
    #         Rou=Dens*rro(k-1)*exp(betar*(geomAlt-Z(k-1)));
    #         break
    #     end
    # end


if __name__ == '__main__':
    f = open('test_atmos.txt', 'w+')
    for i in range(100000):
        T, a, P, Rou = atmoscoesa(i)
        out_stream = ' '
        seq = (str(i), str(T), str(a), str(P), str(Rou))
        out_stream = out_stream.join(seq)
        print(out_stream)
        f.write(out_stream + '\n')
        # print(T, a, P, Rou)
    f.close()


