# NEBULA Astronomical Data Sources, Provenance & Data Layer Specification

NEBULA prioritizes empirical scientific rigor, strict data provenance, and 100% offline autonomy. All celestial bodies in the platform are grounded in peer-reviewed astronomical databases, space mission telemetry, and international observational archives.

---

## 1. Datasets & Repositories

### 1.1 NASA Planetary Fact Sheets & JPL Solar System Dynamics
- **Curating Institution**: NASA Goddard Space Flight Center / NASA Jet Propulsion Laboratory (JPL)
- **Objects Covered**: Sun, Mercury, Venus, Earth, Moon, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Ceres, 1P/Halley.
- **Data Extracted**:
  - Gravitational & Bulk: Mass ($M$), volumetric mean radius ($R$), mean density ($\rho$), surface gravity ($g$), escape velocity ($v_{\text{esc}}$).
  - Orbital & Dynamical: Semi-major axis ($a$), orbital period ($P$), sidereal rotation period, mean orbital velocity, eccentricity ($e$), inclination ($i$), perihelion, aphelion.
  - Thermal & Atmospheric: Effective temperature ($T$), surface atmospheric pressure, atmospheric envelope presence, ring structure existence.
- **Reference URL**: [NASA Planetary Fact Sheet](https://nssdc.gsfc.nasa.gov/planetary/planetfact.html)

### 1.2 NASA Exoplanet Archive (IPAC / Caltech)
- **Curating Institution**: NASA Exoplanet Science Institute / California Institute of Technology (IPAC)
- **Objects Covered**: TRAPPIST-1 system (Star + TRAPPIST-1e), Proxima Centauri b, Kepler-452b.
- **Data Extracted**:
  - Host star parentage, planetary mass ($M \sin i$ / dynamical TTV mass), planetary radius ($R_p$), orbital period ($P$), semi-major axis ($a$), equilibrium temperature ($T_{\text{eq}}$).
  - Discovery telemetry: Discovery method (Transit Photometry, Doppler Radial Velocity), discovery year, discovering observatory/facility.
- **Reference URL**: [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/)

### 1.3 SIMBAD Astronomical Database & Gaia DR3 (CDS Strasbourg / ESA)
- **Curating Institution**: Centre de Données astronomiques de Strasbourg (CDS) & European Space Agency (ESA)
- **Objects Covered**: Sirius A, Betelgeuse (Alpha Orionis), M31 Andromeda Galaxy.
- **Data Extracted**:
  - Spectral classification (Morgan-Keenan class), apparent magnitude ($V$), absolute magnitude ($M_V$), effective temperature ($T_{\text{eff}}$), bolometric luminosity ($L_\odot$), equatorial rotation velocity/period.
- **Reference URL**: [CDS SIMBAD](https://simbad.u-strasbg.fr/simbad/)

### 1.4 Event Horizon Telescope Collaboration & GRAVITY
- **Curating Institution**: EHT Collaboration / Max Planck Institute for Extraterrestrial Physics
- **Objects Covered**: Sagittarius A* (Supermassive Black Hole at the Galactic Center)
- **Data Extracted**:
  - Virial dynamical mass ($4.154 \pm 0.014 \times 10^6\,M_\odot$), gravitational radius ($R_g$), Schwarzschild radius ($R_s \approx 0.082\,\text{AU}$), shadow angular diameter ($51.8\,\mu\text{as}$).
- **Citations**: EHT Collaboration (ApJL 2022); GRAVITY Collaboration (A&A 2018).

---

## 2. Normalized Data Model Specification

NEBULA provides normalized models that represent astronomical bodies accurately without forcing irrelevant properties onto incompatible entities:

### 2.1 Core Normalized Attributes
| Field | Type | Description | Unit |
| :--- | :--- | :--- | :--- |
| `id` | `str` | Unique URL-safe lowercase slug (e.g. `'earth'`, `'jupiter'`) | — |
| `name` | `str` | Common astronomical name | — |
| `object_type` | `str` | Celestial classification: Planet, Moon, Star, Exoplanet, Asteroid, Comet, Generic | — |
| `description` | `str` | Comprehensive descriptive text | — |
| `mass` | `float` | Gravitational body mass | $\text{kg}$ |
| `radius` | `float` | Volumetric mean radius | $\text{km}$ |
| `gravity` | `float` | Surface gravitational acceleration | $\text{m/s}^2$ |
| `distance_from_sun` | `float` | Heliocentric semi-major axis (orbiting solar bodies) | $\text{AU}$ |
| `orbital_period` | `float` | Sidereal orbital period | $\text{days}$ |
| `rotation_period` | `float` | Sidereal axial rotation period | $\text{hours}$ |
| `orbital_velocity` | `float` | Mean orbital velocity | $\text{km/s}$ |
| `temperature` | `float` | Surface or effective temperature | $\text{K}$ |
| `parent_object` | `str` | Host body identifier (`'sun'` for planets, host planet for moons, host star for exoplanets) | — |
| `orbital_parameters` | `dict` | Keplerian coordinates: eccentricity, inclination, perihelion, aphelion | $\text{AU}, ^\circ$ |
| `discovery_information` | `dict` | Discoverer name, discovery year, discovery method | — |
| `source` | `str` | Canonical astronomical catalog citation | — |
| `source_url` | `str` | Authoritative external documentation URL | — |
| `units` | `dict` | Key-value dictionary documenting the unit of each field | — |
| `metadata` | `dict` | Additional astrophysical telemetry (albedo, magnetic field, research notes) | — |

### 2.2 Specialized Model Hierarchy
- **`Star`**: Focuses on spectral class, luminosity ($L_\odot$), effective temperature ($T_{\text{eff}}$), and stellar rotation. Does not force `distance_from_sun` or `parent_object`.
- **`Planet`**: Captures heliocentric semi-major axis, orbital period, orbital velocity, Keplerian orbital parameters, atmosphere, and rings. Parent object defaults to the Sun.
- **`Moon`**: Explicitly requires `parent_object` (host planet). Defines orbital period and velocity around parent world.
- **`Exoplanet`**: Requires `parent_object` (host star). Focuses on stellar distance, transit/RV parameters, and discovery method.
- **`Asteroid`**: Captures main belt or trojan orbital coordinates, rotation period, and small-body dimensions.
- **`Comet`**: Captures high-eccentricity orbital elements, perihelion, aphelion, and apparition period.
- **`GenericCelestialObject`**: Supports deep-sky structures, galaxies, and black holes without forced planetary mechanics.

---

## 3. Measurement Units Standard

NEBULA documents and validates units across all numeric fields using standard IAU and SI conventions:
- **Mass**: $\text{kg}$ (with secondary conversions to Earth masses $M_\oplus$, Solar masses $M_\odot$, and Jupiter masses $M_J$ via Astropy).
- **Radius**: $\text{km}$ (with secondary conversions to Earth radii $R_\oplus$ and Solar radii $R_\odot$).
- **Surface Gravity**: $\text{m/s}^2$ (standard Earth gravitational acceleration $g_0 = 9.80665\,\text{m/s}^2$).
- **Distances**: $\text{AU}$ for interplanetary and exoplanetary separations; $\text{pc}$ and $\text{ly}$ for interstellar bodies.
- **Time**: $\text{days}$ for orbital periods; $\text{hours}$ for rotational periods.
- **Velocities**: $\text{km/s}$ for orbital and escape speeds.
- **Thermal State**: $\text{Kelvin}$ ($\text{K}$) with automatic conversion to Celsius ($^\circ\text{C} = \text{K} - 273.15$).

---

## 4. Scientific Limitations & Approximations

1. **Mean Spherical Approximation**: Volumetric mean radius ($R = (a^2 b)^{1/3}$ or spherical equivalent) is used for density and surface gravity calculations. Highly oblate worlds (Saturn oblateness $\approx 0.098$, Jupiter $\approx 0.065$) exhibit pole-to-equator gravity variations not captured by single-value mean surface gravity.
2. **Mean Keplerian Elements**: Heliocentric orbital elements are referenced to the J2000 epoch and represent mean secular orbits. Planetary orbits in nature undergo osculating gravitational perturbations from other planetary masses.
3. **Exoplanet Temperature Estimates**: Exoplanet surface temperatures reflect calculated radiative equilibrium temperatures assuming an Earth-like Bond albedo ($A_B = 0.3$) and uniform heat redistribution, in absence of direct spectroscopic atmospheric profile data.
4. **Relativistic Gravitational Corrections**: Newtonian formulas are employed for surface gravity and escape velocity. For Sagittarius A*, relativistic Schwarzschild coordinates are explicitly annotated in `metadata`.

---

## 5. Local Fallback & Offline Resilience

NEBULA is architected with an offline-first mandate:
1. **Zero Mandatory Network Access**: Core functionality, catalog browsing, parametric filtering, search, and validation run entirely against the embedded `LocalDataProvider`.
2. **Deterministic Seed Catalog**: All 23 core astronomical objects (including Sun, Mercury, Venus, Earth, Moon, Mars, Jupiter, Saturn, Uranus, Neptune) are pre-loaded in memory and persistent in SQLite (`nebula.db`).
3. **Transparent Provenance Flagging**: Local seed objects are permanently marked with `"is_demo_seed": true` and `"confidence_level": "High (Empirically Verified)"`.
4. **External Provider Isolation**: If remote TAP/ADQL endpoints (NASA Exoplanet Archive, SIMBAD) are enabled in future expansions, connection failures will immediately and gracefully fall back to local seed data without user disruption.
