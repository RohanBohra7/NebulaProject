# NEBULA Scientific Methods & Astrophysical Formulations

This document provides a comprehensive, rigorous reference for the mathematical, astronomical, and physical formulations implemented across the **NEBULA Scientific Computation Engine** (`backend/app/scientific/`).

All calculations are implemented in pure Python using **NumPy**, **SciPy**, and **Astropy**, with strictly documented physical units and error bounds.

---

## 1. Fundamental Constants (SI & Astronomical Units)

Physical constants are grounded in **CODATA 2018** recommendations and **IAU 2015/2012** resolution values, cross-verified with `astropy.constants` and `astropy.units`.

| Constant | Symbol | Numerical Value | SI / IAU Units | Origin / Standard |
| :--- | :--- | :--- | :--- | :--- |
| **Newtonian Gravitational Constant** | $G$ | $6.67430 \times 10^{-11}$ | $\text{m}^3\,\text{kg}^{-1}\,\text{s}^{-2}$ | CODATA 2018 |
| **Speed of Light in Vacuum** | $c$ | $299,792,458$ | $\text{m/s}$ | Exact SI definition |
| **Standard Solar Mass** | $M_\odot$ | $1.98847 \times 10^{30}$ | $\text{kg}$ | IAU 2015 Resolution B3 |
| **Standard Earth Mass** | $M_\oplus$ | $5.9722 \times 10^{24}$ | $\text{kg}$ | IAU 2015 Resolution B3 |
| **Standard Jupiter Mass** | $M_J$ | $1.89813 \times 10^{27}$ | $\text{kg}$ | IAU 2015 Resolution B3 |
| **Nominal Solar Radius** | $R_\odot$ | $6.95700 \times 10^{8}$ | $\text{m}$ | IAU 2015 Resolution B3 |
| **Nominal Equatorial Earth Radius** | $R_\oplus$ | $6.378137 \times 10^{6}$ | $\text{m}$ | IAU 2015 Resolution B3 |
| **Volumetric Mean Earth Radius** | $R_{\oplus,\text{mean}}$ | $6.3710 \times 10^{6}$ | $\text{m}$ | IUGG Reference |
| **Nominal Jupiter Equatorial Radius** | $R_J$ | $7.1492 \times 10^{7}$ | $\text{m}$ | IAU 2015 Resolution B3 |
| **Astronomical Unit** | $\text{AU}$ | $149,597,870,700$ | $\text{m}$ | IAU 2012 exact definition |
| **Parsec** | $\text{pc}$ | $\approx 3.085677581 \times 10^{16}$ | $\text{m}$ | Exact $\frac{180 \times 3600}{\pi}\,\text{AU}$ |
| **Julian Light-Year** | $\text{ly}$ | $\approx 9.460730472 \times 10^{15}$ | $\text{m}$ | $c \times 365.25 \times 86400\,\text{s}$ |
| **Standard Acceleration of Gravity** | $g_0$ | $9.80665$ | $\text{m/s}^2$ | 3rd CGPM (1901) |
| **Nominal Solar Luminosity** | $L_\odot$ | $3.828 \times 10^{26}$ | $\text{W}$ | IAU 2015 Resolution B3 |
| **Stefan-Boltzmann Constant** | $\sigma$ | $5.670374 \times 10^{-8}$ | $\text{W}\,\text{m}^{-2}\,\text{K}^{-4}$ | CODATA 2018 |
| **Mean J2000.0 Ecliptic Obliquity** | $\epsilon$ | $23.43929111^\circ$ | Degrees | IAU J2000.0 Reference |

---

## 2. Gravitational Physics (`backend/app/scientific/gravity.py`)

### 2.1 Universal Law of Gravitation
For two idealized point masses $m_1$ and $m_2$ separated by center-to-center distance $r$:
$$F = G \frac{m_1 m_2}{r^2}$$

In 3D Cartesian space, the vector force $\mathbf{F}_{12}$ exerted on body 1 by body 2 at position vectors $\mathbf{r}_1$ and $\mathbf{r}_2$:
$$\mathbf{r}_{12} = \mathbf{r}_2 - \mathbf{r}_1, \quad r = \|\mathbf{r}_{12}\|$$
$$\mathbf{F}_{12} = G \frac{m_1 m_2}{r^3} \mathbf{r}_{12} = G \frac{m_1 m_2}{r^2} \hat{\mathbf{r}}_{12}$$

- **Assumptions**: Point-mass approximation, non-relativistic weak gravitational regime.
- **Units**: Mass in $\text{kg}$, distance in $\text{m}$, force in Newtons ($\text{N} = \text{kg}\,\text{m}\,\text{s}^{-2}$).
- **Limitations**: Excludes relativistic frame dragging and quadrupole non-spherical mass perturbations.

### 2.2 Surface Gravity & Gravitational Acceleration
The local gravitational acceleration at radial distance $R$ from a spherically symmetric body of mass $M$:
$$g = \frac{G M}{R^2}$$
Relative surface gravity normalized to Earth standard gravity:
$$g_{\text{gees}} = \frac{g}{g_0} = \frac{G M / R^2}{9.80665\,\text{m/s}^2}$$

### 2.3 Gravitational Potential & Potential Energy
The specific gravitational potential $\Phi(r)$ and two-body potential energy $U(r)$ with reference $\Phi(\infty) = 0$:
$$\Phi(r) = -\frac{G M}{r} \quad [\text{J/kg} = \text{m}^2/\text{s}^2]$$
$$U(r) = -\frac{G M m}{r} \quad [\text{Joules}]$$

### 2.4 Tidal Acceleration
Differential gravitational pull across the finite diameter $2 R_2$ of a secondary body orbiting a primary mass $M_1$ at distance $r$:
$$a_{\text{tidal}} = \left|\frac{\partial g}{\partial r}\right| \cdot R_2 \approx \frac{2 G M_1 R_2}{r^3} \quad [\text{m/s}^2]$$
This differential strain drives oceanic tides, tidal locking, orbital circularization, and Roche disruption.

---

## 3. Orbital Velocities & Energy (`backend/app/scientific/orbital.py`)

### 3.1 Circular Orbital Velocity
For a circular orbit of radius $r$ around standard gravitational parameter $\mu = G(M + m) \approx G M$:
$$v_c = \sqrt{\frac{\mu}{r}}$$

### 3.2 Vis-Viva Instantaneous Velocity
For any bound Keplerian orbit with semi-major axis $a$, the instantaneous orbital velocity at radial distance $r$ satisfies conservation of specific mechanical energy:
$$\epsilon = \frac{v^2}{2} - \frac{\mu}{r} = -\frac{\mu}{2a}$$
Solving for $v(r)$ yields the **Vis-Viva equation**:
$$v(r) = \sqrt{\mu \left(\frac{2}{r} - \frac{1}{a}\right)}$$

- **Apsidal Velocities**:
  - **Periapsis** ($r_p = a(1 - e)$):
    $$v_{\text{peri}} = \sqrt{\frac{\mu}{a} \left(\frac{1 + e}{1 - e}\right)}$$
  - **Apoapsis** ($r_a = a(1 + e)$):
    $$v_{\text{apo}} = \sqrt{\frac{\mu}{a} \left(\frac{1 - e}{1 + e}\right)}$$
  - **Apsidal Ratio**: $\frac{v_{\text{peri}}}{v_{\text{apo}}} = \frac{1 + e}{1 - e}$.

### 3.3 Escape Velocity
The parabolic speed required for a projectile to reach infinite distance with zero residual kinetic energy:
$$v_{\text{esc}} = \sqrt{\frac{2 \mu}{r}} = \sqrt{2} \cdot v_c$$

---

## 4. Orbital Periods & Resonance (`backend/app/scientific/orbital.py`)

### 4.1 Kepler's Third Law (Harmonic Law)
The sidereal orbital period of two bodies under mutual gravitational attraction:
$$P = 2\pi \sqrt{\frac{a^3}{G (M_1 + M_2)}}$$
When $M_1 = M_\odot \gg M_2$ and $a$ is measured in $\text{AU}$, the period simplifies to:
$$P^2 \approx a^3 \quad (P \text{ in years, } a \text{ in AU})$$

### 4.2 Synodic Period
The recurrence interval between identical relative celestial configurations (e.g. oppositions or conjunctions) as viewed from the primary host:
$$\frac{1}{P_{\text{syn}}} = \left|\frac{1}{P_1} - \frac{1}{P_2}\right| \implies P_{\text{syn}} = \frac{P_1 P_2}{|P_1 - P_2|}$$

### 4.3 Mean-Motion Orbital Resonance
Two bodies are in mean-motion orbital resonance when their orbital periods satisfy a near-integer ratio $p:q$:
$$\frac{P_2}{P_1} \approx \frac{p}{q}, \quad p, q \in \mathbb{N}$$
Resonances stabilize orbits through periodic gravitational phasing (e.g. Neptune-Pluto 3:2, TRAPPIST-1 Laplace chain 8:5:3:2).

---

## 5. Keplerian Orbital Geometry (`backend/app/scientific/orbital.py`)

An elliptical orbit is characterized by semi-major axis $a$ and eccentricity $e \in [0, 1)$:

| Geometric Metric | Formulation | Physical Meaning |
| :--- | :--- | :--- |
| **Semi-Minor Axis** | $b = a\sqrt{1 - e^2}$ | Perpendicular transverse axis radius |
| **Semi-Latus Rectum** | $p = a(1 - e^2)$ | Radial distance at true anomaly $\nu = \pm 90^\circ$ |
| **Linear Eccentricity** | $c = a \cdot e$ | Distance from ellipse center to focal point |
| **Periapsis Distance** | $r_p = a(1 - e)$ | Closest orbital distance |
| **Apoapsis Distance** | $r_a = a(1 + e)$ | Furthest orbital distance |
| **Specific Mechanical Energy** | $\epsilon = -\frac{\mu}{2a}$ | Conserved sum of kinetic + potential energy per unit mass |
| **Specific Angular Momentum** | $h = \sqrt{\mu p} = \sqrt{\mu a(1 - e^2)}$ | Conserved orbital angular momentum vector magnitude |

### 5.1 Kepler's Equation & Anomaly Transformations
The mean anomaly $M(t)$ advances linearly with time:
$$M(t) = n (t - t_0) = \frac{2\pi}{P} (t - t_0)$$
The eccentric anomaly $E$ satisfies Kepler's transcendental equation:
$$M = E - e \sin E$$

NEBULA solves for $E$ using Newton-Raphson iteration with convergence threshold $\epsilon < 10^{-12}$:
$$E_{k+1} = E_k - \frac{E_k - e\sin E_k - M}{1 - e\cos E_k}$$

The true anomaly $\nu$ is subsequently determined via:
$$\tan\left(\frac{\nu}{2}\right) = \sqrt{\frac{1+e}{1-e}} \tan\left(\frac{E}{2}\right)$$

---

## 6. Trajectories & Stability Boundaries

### 6.1 Hohmann Transfer Orbit
The minimum-energy coplanar transfer between two concentric circular orbits of radii $r_1$ and $r_2$:
$$a_{\text{trans}} = \frac{r_1 + r_2}{2}$$
$$\Delta v_1 = \left|\sqrt{\mu \left(\frac{2}{r_1} - \frac{1}{a_{\text{trans}}}\right)} - \sqrt{\frac{\mu}{r_1}}\right|$$
$$\Delta v_2 = \left|\sqrt{\frac{\mu}{r_2}} - \sqrt{\mu \left(\frac{2}{r_2} - \frac{1}{a_{\text{trans}}}\right)}\right|$$
$$\Delta v_{\text{total}} = \Delta v_1 + \Delta v_2$$
$$T_{\text{trans}} = \pi \sqrt{\frac{a_{\text{trans}}^3}{\mu}}$$

### 6.2 Hill Sphere Radius
The approximate gravitational sphere of influence of a secondary mass $m$ orbiting a dominant primary $M$:
$$r_H \approx a (1 - e) \sqrt[3]{\frac{m}{3 M}}$$

### 6.3 Roche Limit (Tidal Disruption)
The critical distance inside which tidal forces overcome self-gravity:
- **Rigid satellite**:
  $$d_{\text{rigid}} = R_M \left(2 \frac{\rho_M}{\rho_m}\right)^{1/3}$$
- **Fluid satellite (hydrostatic equilibrium)**:
  $$d_{\text{fluid}} \approx 2.44 R_M \left(\frac{\rho_M}{\rho_m}\right)^{1/3}$$

### 6.4 Lagrange Equilibrium Points
In the circular restricted three-body problem with normalized mass parameter $\mu = \frac{m_2}{m_1 + m_2}$:
- **$L_1$**: Collinear between masses at $r_{L1} \approx r \sqrt[3]{\mu / 3}$ inside $m_2$.
- **$L_2$**: Collinear beyond $m_2$ at $r_{L2} \approx r \sqrt[3]{\mu / 3}$ outside $m_2$.
- **$L_3$**: Collinear opposite $m_2$ at $x_{L3} \approx -r (1 + 7\mu / 12)$.
- **$L_4, L_5$**: Equilateral triangular vertices leading and trailing $m_2$ by $\pm 60^\circ$ in the orbital plane. Stable under Coriolis trapping when $\frac{m_1}{m_2} > \frac{27 + \sqrt{621}}{2} \approx 24.96$.

---

## 7. Distance Metrics & Light Propagation (`backend/app/scientific/distances.py`)

### 7.1 Euclidean 3D Separation
$$d = \|\mathbf{r}_2 - \mathbf{r}_1\| = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2 + (z_2 - z_1)^2}$$

### 7.2 Light Travel Time
$$t_{\text{light}} = \frac{d}{c}$$
- Earth to Sun ($1\text{ AU}$): $499.005\,\text{s} \approx 8.317\,\text{min}$.
- Earth to Moon ($384,400\,\text{km}$): $1.282\,\text{s}$.

### 7.3 Apparent Angular Diameter
$$\theta = 2 \arctan\left(\frac{D}{2 d}\right)$$
For $d \gg D$, the small-angle approximation yields:
$$\theta \approx \frac{D}{d} \quad [\text{radians}]$$

### 7.4 Photometric Distance Modulus
Relating apparent magnitude $m$, absolute magnitude $M$, and distance in parsecs $d_{\text{pc}}$:
$$\mu = m - M = 5 \log_{10}(d_{\text{pc}}) - 5 = 5 \log_{10}\left(\frac{d_{\text{pc}}}{10\,\text{pc}}\right)$$
$$d_{\text{pc}} = 10^{(\mu + 5) / 5}$$

---

## 8. Coordinate Transformations (`backend/app/scientific/coordinates.py`)

### 8.1 Cartesian $\leftrightarrow$ Spherical Polar
$$(x, y, z) \longrightarrow (r, \theta, \phi):$$
$$r = \sqrt{x^2 + y^2 + z^2}, \quad \theta = \arccos\left(\frac{z}{r}\right), \quad \phi = \text{atan2}(y, x)$$

### 8.2 Ecliptic $\leftrightarrow$ Equatorial Reference Frames
Transforming between Ecliptic coordinates $(\lambda, \beta)$ and Equatorial coordinates $(\alpha, \delta)$ using Earth's J2000.0 axial obliquity $\epsilon \approx 23.43929111^\circ$:
$$\sin \delta = \sin \beta \cos \epsilon + \cos \beta \sin \epsilon \sin \lambda$$
$$\tan \alpha = \frac{\sin \lambda \cos \epsilon - \tan \beta \sin \epsilon}{\cos \lambda}$$

Inverse transformation:
$$\sin \beta = \sin \delta \cos \epsilon - \cos \delta \sin \epsilon \sin \alpha$$
$$\tan \lambda = \frac{\sin \alpha \cos \epsilon + \tan \delta \sin \epsilon}{\cos \alpha}$$

---

## 9. Astropy Unit Engine & Dimensional Integrity (`backend/app/scientific/units.py`)

NEBULA verifies physical dimensional compatibility before executing any conversions:
- **Mass**: $\text{kg}, \text{g}, \text{lb}, M_\odot, M_\oplus, M_J$.
- **Length**: $\text{m}, \text{km}, \text{mile}, \text{AU}, \text{pc}, \text{kpc}, \text{Mpc}, \text{ly}, R_\odot, R_\oplus, R_J$.
- **Velocity**: $\text{m/s}, \text{km/s}, \text{km/h}, \text{mph}, c$.
- **Time**: $\text{s}, \text{min}, \text{h}, \text{d}, \text{yr}, \text{kyr}, \text{Myr}, \text{Gyr}$.
- **Temperature**: $\text{K}, ^\circ\text{C}, ^\circ\text{F}$ via affine shifting ($T_K = T_C + 273.15$).
- **Energy**: $\text{J}, \text{kJ}, \text{eV}, \text{keV}, \text{MeV}, \text{erg}$.
- **Force**: $\text{N}, \text{dyn}, \text{lbf}$.

If a user requests a conversion across differing physical dimensions (e.g. $\text{kg} \to \text{AU}$), the engine rejects the request with an explicit `ValueError` identifying the incompatible physical types.

---

## 10. Assumptions, Approximations, and Physical Limitations

1. **Two-Body Approximation**:
   Analytical orbital equations assume isolated two-body Keplerian motion. N-body gravitational perturbations (e.g. Jupiter perturbing Asteroid belt) are addressed in the numerical simulation engine rather than the analytical solver.
2. **Point-Mass Assumption**:
   Bodies are modeled as spherically symmetric point masses. Quadrupole mass moments ($J_2$) and gravitational harmonics are neglected in primary Keplerian orbits.
3. **Classical Non-Relativistic Regime**:
   Calculations assume Newtonian gravity ($v \ll c$, weak field). Relativistic corrections (such as Mercury's perihelion precession of $42.98''/\text{century}$) are omitted in classical 2-body analytical equations.
4. **Coplanar Circular Hohmann Transfers**:
   Hohmann transfer formulations assume initial and final orbits are circular and coplanar. True interplanetary trajectories require Lambert targeting and bi-elliptic or patched-conic corrections.
5. **Rigid vs Fluid Roche Disruption**:
   The rigid Roche limit assumes the satellite maintains shape until disruption; the fluid limit assumes hydrostatic tidal distortion into a prolate ellipsoid prior to disintegration. Real celestial bodies behave between these limits depending on internal tensile strength and mantle elasticity.
