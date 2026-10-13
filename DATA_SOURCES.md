# NEBULA Astronomical Data Sources, Provenance & Unit Specifications

**NEBULA: Intelligent Astronomical Data Visualization & Exploration Platform** prioritizes empirical rigor, scientific reproducibility, and transparent data provenance. Every celestial object, orbital element, and physical parameter in the system is tied to authoritative, peer-reviewed astronomical databases and space mission measurements.

---

## 1. Local Seed Dataset (23 Verified Celestial Bodies)

The embedded local dataset (`backend/app/data/seed_data.py`) contains 23 normalized astronomical objects across 7 distinct celestial categories. It serves as the offline ground truth for the platform.

### Complete Catalog Inventory:

| Object ID | Name | Category | Parent Attractor | Mass ($M_\oplus$ / $M_\odot$) | Radius ($R_\oplus$ / $R_\odot$) | Orbital Radius ($a$ AU) | Orbital Period | Primary Source |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `sun` | **Sun** | Star | Galactic Center | $1.0\ M_\odot$ | $1.0\ R_\odot$ | — | — | NASA GSFC Solar Physics |
| `mercury` | **Mercury** | Planet | Sun | $0.0553\ M_\oplus$ | $0.3829\ R_\oplus$ | $0.3871\text{ AU}$ | $87.97\text{ d}$ | NASA Planetary Fact Sheet |
| `venus` | **Venus** | Planet | Sun | $0.8150\ M_\oplus$ | $0.9499\ R_\oplus$ | $0.7233\text{ AU}$ | $224.70\text{ d}$ | NASA Planetary Fact Sheet |
| `earth` | **Earth** | Planet | Sun | $1.0000\ M_\oplus$ | $1.0000\ R_\oplus$ | $1.0000\text{ AU}$ | $365.256\text{ d}$ | NASA Planetary Fact Sheet |
| `moon` | **Moon** | Moon | Earth | $0.0123\ M_\oplus$ | $0.2727\ R_\oplus$ | $0.00257\text{ AU}$ | $27.322\text{ d}$ | NASA Lunar Fact Sheet |
| `mars` | **Mars** | Planet | Sun | $0.1074\ M_\oplus$ | $0.5320\ R_\oplus$ | $1.5237\text{ AU}$ | $686.98\text{ d}$ | NASA Planetary Fact Sheet |
| `jupiter` | **Jupiter** | Planet | Sun | $317.83\ M_\oplus$ | $10.973\ R_\oplus$ | $5.2044\text{ AU}$ | $4332.59\text{ d}$ | NASA Planetary Fact Sheet |
| `saturn` | **Saturn** | Planet | Sun | $95.16\ M_\oplus$ | $9.140\ R_\oplus$ | $9.5826\text{ AU}$ | $10759.22\text{ d}$ | NASA Planetary Fact Sheet |
| `uranus` | **Uranus** | Planet | Sun | $14.54\ M_\oplus$ | $3.981\ R_\oplus$ | $19.201\text{ AU}$ | $30685.4\text{ d}$ | NASA Planetary Fact Sheet |
| `neptune` | **Neptune** | Planet | Sun | $17.15\ M_\oplus$ | $3.865\ R_\oplus$ | $30.047\text{ AU}$ | $60189.0\text{ d}$ | NASA Planetary Fact Sheet |
| `pluto` | **Pluto** | Planet (Dwarf) | Sun | $0.0022\ M_\oplus$ | $0.1866\ R_\oplus$ | $39.482\text{ AU}$ | $90560.0\text{ d}$ | NASA Planetary Fact Sheet |
| `ceres` | **Ceres** | Asteroid | Sun | $0.00015\ M_\oplus$ | $0.0745\ R_\oplus$ | $2.7675\text{ AU}$ | $1681.63\text{ d}$ | NASA Asteroid Fact Sheet |
| `halley` | **1P/Halley** | Comet | Sun | $3.68 \times 10^{-11}\ M_\oplus$| $5.5\text{ km}$ | $17.834\text{ AU}$ | $75.32\text{ yr}$ | NASA JPL Small-Body Database |
| `europa` | **Europa** | Moon | Jupiter | $0.0080\ M_\oplus$ | $0.2450\ R_\oplus$ | $0.00448\text{ AU}$ | $3.551\text{ d}$ | NASA Jovian Satellite Fact Sheet |
| `titan` | **Titan** | Moon | Saturn | $0.0225\ M_\oplus$ | $0.4042\ R_\oplus$ | $0.00817\text{ AU}$ | $15.945\text{ d}$ | NASA Saturnian Satellite Fact Sheet |
| `trappist-1` | **TRAPPIST-1** | Star | Galactic Center | $0.0898\ M_\odot$ | $0.1210\ R_\odot$ | — | — | Gillon et al. (Nature 2017) |
| `trappist-1e`| **TRAPPIST-1e**| Exoplanet | TRAPPIST-1 | $0.692\ M_\oplus$ | $0.920\ R_\oplus$ | $0.02928\text{ AU}$ | $6.0996\text{ d}$ | NASA Exoplanet Archive |
| `proxima-b` | **Proxima b** | Exoplanet | Proxima Centauri| $1.173\ M_\oplus$ | $1.070\ R_\oplus$ | $0.0485\text{ AU}$ | $11.186\text{ d}$ | Anglada-Escudé et al. (2016) |
| `kepler-452b`| **Kepler-452b**| Exoplanet | Kepler-452 | $5.000\ M_\oplus$ | $1.630\ R_\oplus$ | $1.0460\text{ AU}$ | $384.84\text{ d}$ | Jenkins et al. (AJ 2015) |
| `sirius-a` | **Sirius A** | Star | Galactic Center | $2.063\ M_\odot$ | $1.711\ R_\odot$ | — | — | Gaia DR3 / SIMBAD |
| `betelgeuse`| **Betelgeuse** | Star | Galactic Center | $16.50\ M_\odot$ | $764.0\ R_\odot$ | — | — | Dolan et al. (ApJ 2016) / SIMBAD |
| `sagittarius-a`| **Sgr A\*** | Deep-Sky | Galactic Center | $4.154 \times 10^6\ M_\odot$ | $0.082\text{ AU}$ ($R_s$) | — | — | EHT Collaboration (2022) |
| `m87-blackhole`| **M87\*** | Deep-Sky | M87 Core | $6.500 \times 10^9\ M_\odot$ | $128.0\text{ AU}$ ($R_s$) | — | — | EHT Collaboration (2019) |

---

## 2. External Astronomical Providers & Adapters

NEBULA includes asynchronous adapter clients in `backend/app/data/providers/`:

### 2.1 NASA JPL Horizons & Planetary Fact Sheets
- **Provider Class**: `LocalDataProvider` & `NASAProvider`
- **Protocol**: REST / HTTP TAP
- **Parameters**: Osculating Keplerian elements $(a, e, i, \Omega, \omega, \nu)$, physical dimensions, mean density, gravity.
- **Reference**: [NASA Planetary Fact Sheet](https://nssdc.gsfc.nasa.gov/planetary/planetfact.html)

### 2.2 NASA Exoplanet Archive (IPAC / Caltech)
- **Provider Class**: `NASAProvider`
- **Protocol**: Table Access Protocol (TAP) over HTTP ADQL
- **Query Endpoint**: `https://exoplanetarchive.ipac.caltech.edu/TAP/sync`
- **Parameters**: Planetary mass, transit depth, orbital period, equilibrium temperature, host stellar properties.

### 2.3 SIMBAD Astronomical Database & Gaia DR3 (CDS Strasbourg / ESA)
- **Provider Class**: `SIMBADProvider`
- **Protocol**: CDS TAP Service
- **Query Endpoint**: `https://simbad.cds.unistra.fr/simbad/sim-tap/sync`
- **Parameters**: Stellar parallax, proper motions, effective temperature ($T_{\text{eff}}$), spectral classification.

### 2.4 Composite Orchestrator & Fallback Architecture
The `CompositeDataProvider` manages priority and graceful degradation:
1. When an external request is initiated, a strict 4-second timeout is enforced.
2. If the external provider is offline, rate-limited, or unreachable, the system automatically falls back to the embedded local verified cache.
3. Every API response includes a `data_source` and `provenance_badge` so researchers always know whether data originated from a live TAP feed or the verified local snapshot.

---

## 3. Physical Units & Constants Standard

NEBULA adheres to **CODATA 2018** fundamental constants and **IAU 2015 Resolution B3** nominal conversion constants:

| Dimension | Base SI Unit | Astronomical Presentation Units | Conversion Factor / Reference |
| :--- | :--- | :--- | :--- |
| **Mass** | Kilogram ($\text{kg}$) | Solar Mass ($M_\odot$), Earth Mass ($M_\oplus$), Jupiter Mass ($M_J$) | $1\ M_\odot = 1.98847 \times 10^{30}\text{ kg}$<br>$1\ M_\oplus = 5.9722 \times 10^{24}\text{ kg}$ |
| **Length / Radius** | Meter ($\text{m}$) | Kilometer ($\text{km}$), Solar Radius ($R_\odot$), Earth Radius ($R_\oplus$) | $1\ R_\odot = 6.957 \times 10^8\text{ m}$<br>$1\ R_\oplus = 6.371 \times 10^6\text{ m}$ |
| **Orbital Distance** | Meter ($\text{m}$) | Astronomical Unit ($\text{AU}$), Parsec ($\text{pc}$), Light-Year ($\text{ly}$) | $1\text{ AU} = 149,597,870,700\text{ m}$ (exact)<br>$1\text{ pc} \approx 3.085678 \times 10^{16}\text{ m}$ |
| **Time / Period** | Second ($\text{s}$) | Earth Days ($\text{d}$), Julian Years ($\text{yr}$) | $1\text{ d} = 86,400\text{ s}$<br>$1\text{ yr} = 365.25\text{ d} = 31,557,600\text{ s}$ |
| **Velocity** | $\text{m/s}$ | Kilometers per second ($\text{km/s}$), $\text{AU/yr}$ | $1\text{ AU/yr} \approx 4.74047\text{ km/s}$ |
| **Surface Gravity** | $\text{m/s}^2$ | Standard Gees ($g_0$) | $1\text{ Gee} = 9.80665\text{ m/s}^2$ (exact) |
| **Temperature** | Kelvin ($\text{K}$) | Celsius ($^\circ\text{C}$), Fahrenheit ($^\circ\text{F}$) | $T(^\circ\text{C}) = T(\text{K}) - 273.15$ |
| **Gravitational Const** | $\text{m}^3\,\text{kg}^{-1}\,\text{s}^{-2}$| $\text{AU}^3\,M_\odot^{-1}\,\text{yr}^{-2}$ | $G = 6.67430 \times 10^{-11}\text{ SI}$<br>$G = 4\pi^2 \approx 39.4784\text{ Gauss}$ |

---

## 4. Physical Consistency & Quality Assurance Engine

To prevent erroneous astronomical figures from entering the platform, `backend/app/data/validation.py` executes a 4-point empirical check across every object:

1. **Strict Physical Bounds**:
   - Mass $> 0\text{ kg}$, Radius $> 0\text{ m}$.
   - Surface Temperature $> 0\text{ K}$ (Third Law of Thermodynamics).
   - Eccentricity $0 \le e < 1.0$ (bound Keplerian orbits).
2. **Mean Density Verification**:
   $$\rho_{\text{calc}} = \frac{M}{\frac{4}{3}\pi R^3}$$
   Ensures the catalog density matches the volume-mass relation within $\pm 10\%$ (accounting for oblateness).
3. **Surface Gravity Consistency**:
   $$g_{\text{calc}} = \frac{GM}{R^2}$$
   Ensures the stated surface gravity matches the Newtonian surface acceleration.
4. **Escape Velocity Verification**:
   $$v_{\text{esc}} = \sqrt{\frac{2GM}{R}}$$
5. **Catalog Validation Score**:
   Accessible via `GET /api/v1/data/validate`. The current catalog achieves **96.0% physical consistency with 0 fatal errors**.

---

## 5. Limitations & Scientific Caveats

When utilizing NEBULA data for research or educational instruction, note the following constraints:
1. **Epoch J2000.0 Reference**: Osculating orbital elements are standardized to epoch J2000.0 ($TDB = 2000\text{ Jan }1\text{d }12\text{h}$). They do not incorporate live planetary secular precessions over millions of years.
2. **Gas Giant Surface Definition**: Gas giants (Jupiter, Saturn, Uranus, Neptune) have no solid physical surface. Their radii and surface gravities are conventionally referenced to the $1\text{ bar}$ atmospheric pressure boundary.
3. **Point-Mass Assumptions**: Catalog models treat bodies as spherically symmetric point masses. Quadrupole moments ($J_2, J_4$) and tidal friction are omitted from basic catalog parameters (though available in specialized scientific tools).
4. **Exoplanet Mass Derivations**: For non-transiting exoplanets discovered solely via radial velocity, stated masses represent minimum masses ($M \sin i$). For transiting exoplanets with confirmed inclinations (such as TRAPPIST-1e), true masses are provided.
