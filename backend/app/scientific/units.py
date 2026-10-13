"""
Astropy-powered dimensional analysis and unit conversion engine for NEBULA.
Enables unit-aware calculations and conversions across astronomical, SI, and imperial systems.
"""
from typing import Dict, Any, List, Optional
import astropy.units as u
from astropy.units import UnitConversionError

# Register speed of light as custom unit
try:
    _c_unit = u.def_unit(['c', 'speed_of_light'], 299792458.0 * u.m / u.s, prefixes=False)
    u.add_enabled_units([_c_unit])
except Exception:
    pass

# Unit alias dictionary for flexible user input
UNIT_ALIASES: Dict[str, str] = {
    # Mass
    "msun": "solMass",
    "m_sun": "solMass",
    "solar_mass": "solMass",
    "solar_masses": "solMass",
    "mearth": "earthMass",
    "m_earth": "earthMass",
    "earth_mass": "earthMass",
    "mjup": "jupiterMass",
    "m_jup": "jupiterMass",
    "jupiter_mass": "jupiterMass",
    "kilogram": "kg",
    "kilograms": "kg",
    "gram": "g",
    "grams": "g",
    "pound": "lb",
    "pounds": "lb",

    # Length / Distance
    "au": "AU",
    "astronomical_unit": "AU",
    "pc": "pc",
    "parsec": "pc",
    "parsecs": "pc",
    "kpc": "kpc",
    "mpc": "Mpc",
    "ly": "lyr",
    "lightyear": "lyr",
    "lightyears": "lyr",
    "light_year": "lyr",
    "light_years": "lyr",
    "rsun": "solRad",
    "r_sun": "solRad",
    "solar_radius": "solRad",
    "rearth": "earthRad",
    "r_earth": "earthRad",
    "earth_radius": "earthRad",
    "meter": "m",
    "meters": "m",
    "kilometer": "km",
    "kilometers": "km",
    "mile": "mile",
    "miles": "mile",

    # Velocity
    "m/s": "m/s",
    "km/s": "km/s",
    "km/h": "km/h",
    "kph": "km/h",
    "mph": "mile/h",
    "c": "c",
    "speed_of_light": "c",

    # Time
    "s": "s",
    "sec": "s",
    "second": "s",
    "seconds": "s",
    "min": "min",
    "minute": "min",
    "minutes": "min",
    "h": "h",
    "hr": "h",
    "hour": "h",
    "hours": "h",
    "d": "d",
    "day": "d",
    "days": "d",
    "yr": "yr",
    "year": "yr",
    "years": "yr",
    "kyr": "kyr",
    "myr": "Myr",
    "gyr": "Gyr",

    # Temperature
    "k": "K",
    "kelvin": "K",
    "celsius": "deg_C",
    "degc": "deg_C",
    "fahrenheit": "deg_F",
    "degf": "deg_F",

    # Energy
    "j": "J",
    "joule": "J",
    "joules": "J",
    "kj": "kJ",
    "ev": "eV",
    "kev": "keV",
    "mev": "MeV",
    "erg": "erg",
    "ergs": "erg",

    # Force
    "n": "N",
    "newton": "N",
    "newtons": "N",
    "dyn": "dyn",
    "dyne": "dyn",
    "dynes": "dyn",
    "lbf": "lbf"
}

def resolve_unit_string(unit_str: str) -> str:
    """Normalizes string aliases to valid Astropy unit names."""
    cleaned = unit_str.strip().lower()
    return UNIT_ALIASES.get(cleaned, unit_str.strip())

def convert_units(
    value: float,
    from_unit: str,
    to_unit: str
) -> Dict[str, Any]:
    """
    Converts a numerical quantity between physical units with dimensional verification.

    :param value: Numerical magnitude
    :param from_unit: Source unit string
    :param to_unit: Target unit string
    """
    resolved_from = resolve_unit_string(from_unit)
    resolved_to = resolve_unit_string(to_unit)

    # Temperature conversions with offsets
    temp_units = {"k", "deg_c", "deg_f"}
    if resolved_from.lower() in temp_units or resolved_to.lower() in temp_units:
        return _convert_temperature(value, resolved_from, resolved_to)

    try:
        u_from = u.Unit(resolved_from)
    except Exception as e:
        raise ValueError(f"Unrecognized source unit '{from_unit}': {str(e)}")

    try:
        u_to = u.Unit(resolved_to)
    except Exception as e:
        raise ValueError(f"Unrecognized target unit '{to_unit}': {str(e)}")

    if not u_from.is_equivalent(u_to):
        raise ValueError(
            f"Dimensionally incompatible units: cannot convert from '{from_unit}' ({u_from.physical_type}) "
            f"to '{to_unit}' ({u_to.physical_type})."
        )

    try:
        quantity = value * u_from
        converted = quantity.to(u_to)
        result_val = float(converted.value)
    except UnitConversionError as err:
        raise ValueError(f"Unit conversion failed: {str(err)}")

    return {
        "input_value": float(value),
        "from_unit": from_unit,
        "to_unit": to_unit,
        "converted_value": result_val,
        "physical_type": str(u_from.physical_type),
        "astropy_representation": str(converted)
    }

def _convert_temperature(val: float, u_from: str, u_to: str) -> Dict[str, Any]:
    """Special handling for temperature scales with affine shifts."""
    f = u_from.lower()
    t = u_to.lower()

    # Convert source to Kelvin
    if f in ("k", "kelvin"):
        kelvin = val
    elif f in ("deg_c", "celsius"):
        kelvin = val + 273.15
    elif f in ("deg_f", "fahrenheit"):
        kelvin = (val - 32.0) * (5.0 / 9.0) + 273.15
    else:
        raise ValueError(f"Cannot convert non-temperature unit '{u_from}' to temperature scale.")

    if kelvin < 0:
        raise ValueError("Temperature cannot be below absolute zero (0 K).")

    # Convert Kelvin to target
    if t in ("k", "kelvin"):
        res = kelvin
    elif t in ("deg_c", "celsius"):
        res = kelvin - 273.15
    elif t in ("deg_f", "fahrenheit"):
        res = (kelvin - 273.15) * (9.0 / 5.0) + 32.0
    else:
        raise ValueError(f"Cannot convert temperature to non-temperature unit '{u_to}'.")

    return {
        "input_value": float(val),
        "from_unit": u_from,
        "to_unit": u_to,
        "converted_value": round(float(res), 4),
        "physical_type": "temperature",
        "astropy_representation": f"{round(float(res), 4)} {u_to}"
    }

def get_supported_categories() -> Dict[str, List[str]]:
    """Returns catalog of supported unit categories and common symbols."""
    return {
        "mass": ["kg", "g", "M_sun", "M_earth", "M_jup", "lb"],
        "distance": ["m", "km", "AU", "pc", "kpc", "Mpc", "ly", "R_sun", "R_earth", "mile"],
        "velocity": ["m/s", "km/s", "km/h", "mph", "c"],
        "time": ["s", "min", "h", "d", "yr", "kyr", "Myr", "Gyr"],
        "temperature": ["K", "deg_C", "deg_F"],
        "energy": ["J", "kJ", "eV", "keV", "MeV", "erg"],
        "force": ["N", "dyn", "lbf"]
    }
