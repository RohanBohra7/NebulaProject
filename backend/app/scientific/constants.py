"""
Fundamental physical and astronomical constants for the NEBULA scientific computation engine.
Directly grounded in CODATA 2018 and IAU 2015/2012 recommended values, verified via Astropy.
"""
import astropy.constants as const
import astropy.units as u

# Gravitational Constant (m^3 kg^-1 s^-2)
G_CONST = float(const.G.value)  # 6.67430e-11
G = G_CONST

# Speed of light in vacuum (m/s)
SPEED_OF_LIGHT = float(const.c.value)  # 299792458.0
C_CONST = SPEED_OF_LIGHT

# Standard Astronomical Masses (kg)
M_SUN = float(const.M_sun.value)    # ~1.98847e30 kg
M_EARTH = float(const.M_earth.value)  # ~5.9722e24 kg
M_JUPITER = float(const.M_jup.value)  # ~1.89813e27 kg
M_MOON = 7.342e22                   # ~7.342e22 kg

# Standard Astronomical Radii (m)
R_SUN = float(const.R_sun.value)    # ~6.957e8 m
R_EARTH = float(const.R_earth.value)  # ~6.378137e6 m (equatorial)
R_EARTH_MEAN = 6.371e6              # Mean volumetric Earth radius (m)
R_JUPITER = float(const.R_jup.value)  # ~7.1492e7 m
R_MOON = 1.7374e6                   # ~1.7374e6 m

# Standard Astronomical Distances (m)
AU_METERS = float(const.au.value)   # 149597870700.0 m
PC_METERS = float(const.pc.value)   # ~3.08567758e16 m
LY_METERS = float((1.0 * u.lyr).to(u.m).value)  # ~9.46073e15 m

# Time Constants (seconds)
DAY_SECONDS = 86400.0               # Standard SI day
JULIAN_YEAR_DAYS = 365.25           # IAU Julian year in days
JULIAN_YEAR_SECONDS = JULIAN_YEAR_DAYS * DAY_SECONDS  # 31,557,600 s

# Standard Acceleration of Gravity at Earth's Surface (m/s^2)
G_EARTH_SURFACE = float(const.g0.value)  # 9.80665 m/s^2

# Solar Luminosity (Watts)
L_SUN = float(const.L_sun.value)    # 3.828e26 W

# Stefan-Boltzmann Constant (W m^-2 K^-4)
STEFAN_BOLTZMANN = float(const.sigma_sb.value)  # 5.670374e-8

# Earth's Mean Obliquity of the Ecliptic (J2000.0) in degrees
EARTH_OBLIQUITY_J2000_DEG = 23.43929111
