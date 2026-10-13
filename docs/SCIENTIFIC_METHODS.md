# NEBULA Scientific Methods & Astrophysical Formulations

This document details the mathematical and physical foundations implemented in the NEBULA computation engine.

---

## 1. Fundamental Constants (SI & Astronomical Units)

| Constant | Symbol | Value | Units |
| :--- | :--- | :--- | :--- |
| **Gravitational Constant** | $G$ | $6.67430 \times 10^{-11}$ | $\text{m}^3\,\text{kg}^{-1}\,\text{s}^{-2}$ |
| **Solar Mass** | $M_\odot$ | $1.98847 \times 10^{30}$ | $\text{kg}$ |
| **Earth Mass** | $M_\oplus$ | $5.9722 \times 10^{24}$ | $\text{kg}$ |
| **Solar Radius** | $R_\odot$ | $6.9634 \times 10^{8}$ | $\text{m}$ |
| **Earth Radius** | $R_\oplus$ | $6.3710 \times 10^{6}$ | $\text{m}$ |
| **Astronomical Unit** | $\text{AU}$ | $1.495978707 \times 10^{11}$ | $\text{m}$ |
| **Speed of Light** | $c$ | $2.99792458 \times 10^{8}$ | $\text{m/s}$ |
| **Normalized Gravitational Parameter** | $G_{\text{AU}}$ | $4\pi^2 \approx 39.4784$ | $\text{AU}^3\,M_\odot^{-1}\,\text{yr}^{-2}$ |

---

## 2. Keplerian Orbital Mechanics

### 2.1 Kepler's Equation Solver
The relationship between mean anomaly $M$ (proportional to time) and eccentric anomaly $E$ is transcendental:
$$M = E - e \sin E$$

NEBULA solves for $E$ using the Newton-Raphson method with convergence threshold $\epsilon < 10^{-12}$:
$$f(E) = E - e \sin E - M$$
$$f'(E) = 1 - e \cos E$$
$$E_{n+1} = E_n - \frac{f(E_n)}{f'(E_n)}$$

The true anomaly $\nu$ (actual angular position in the orbital plane) is then obtained via the half-angle tangent relation:
$$\tan\left(\frac{\nu}{2}\right) = \sqrt{\frac{1+e}{1-e}} \tan\left(\frac{E}{2}\right)$$

### 2.2 Keplerian Elements to Cartesian State Vectors
From semi-major axis $a$, eccentricity $e$, inclination $i$, longitude of ascending node $\Omega$, argument of periapsis $\omega$, and true anomaly $\nu$:

1. Orbital radius:
   $$r = \frac{a(1 - e^2)}{1 + e \cos \nu}$$
2. Perifocal coordinates:
   $$\mathbf{r}_{\text{peri}} = \begin{bmatrix} r \cos \nu \\ r \sin \nu \\ 0 \end{bmatrix}, \quad \mathbf{v}_{\text{peri}} = \begin{bmatrix} -\sqrt{\mu / p} \sin \nu \\ \sqrt{\mu / p} (e + \cos \nu) \\ 0 \end{bmatrix}$$
   where $p = a(1 - e^2)$ is the semi-latus rectum and $\mu = G(M_1 + M_2)$.
3. 3D Rotation from perifocal to heliocentric ecliptic coordinates:
   $$\mathbf{r}_{\text{ecl}} = R_z(-\Omega) R_x(-i) R_z(-\omega) \mathbf{r}_{\text{peri}}$$

---

## 3. Mission Planning: Hohmann Transfer Orbits

A Hohmann transfer orbit is an elliptical orbit used to transfer a spacecraft between two coplanar circular orbits of radii $r_1$ and $r_2$:

1. **Semi-Major Axis of Transfer Ellipse**:
   $$a_{\text{trans}} = \frac{r_1 + r_2}{2}$$
2. **Circular Orbit Velocities**:
   $$v_1 = \sqrt{\frac{\mu}{r_1}}, \quad v_2 = \sqrt{\frac{\mu}{r_2}}$$
3. **Transfer Ellipse Velocities (Vis-Viva Equation)**:
   $$v_{t1} = \sqrt{\mu \left(\frac{2}{r_1} - \frac{1}{a_{\text{trans}}}\right)}, \quad v_{t2} = \sqrt{\mu \left(\frac{2}{r_2} - \frac{1}{a_{\text{trans}}}\right)}$$
4. **Impulsive Velocity Changes ($\Delta v$)**:
   $$\Delta v_1 = |v_{t1} - v_1|, \quad \Delta v_2 = |v_2 - v_{t2}|$$
   $$\Delta v_{\text{total}} = \Delta v_1 + \Delta v_2$$
5. **Transfer Duration ($\tau$)**:
   $$\tau = \pi \sqrt{\frac{a_{\text{trans}}^3}{\mu}}$$

---

## 4. Gravitational Boundaries: Hill Sphere & Roche Limit

### 4.1 Hill Sphere Radius
The region where an astronomical body dominates the attraction of satellites against the tidal pull of a more massive primary body:
$$r_H \approx a (1 - e) \sqrt[3]{\frac{m}{3M_{\text{primary}}}}$$

### 4.2 Roche Limit (Tidal Disruption Boundary)
The minimum distance a celestial body held together only by gravity can approach a second body without being torn apart by tidal forces:
- **Rigid Satellite**:
  $$d_{\text{rigid}} = R_M \left(2 \frac{\rho_M}{\rho_m}\right)^{1/3}$$
- **Fluid Satellite**:
  $$d_{\text{fluid}} \approx 2.44 R_M \left(\frac{\rho_M}{\rho_m}\right)^{1/3}$$

---

## 5. N-Body Hamiltonian Dynamics & Conservation Laws

For a system of $N$ point masses with positions $\mathbf{r}_i$ and velocities $\mathbf{v}_i$:

### 5.1 Hamiltonian Energy
$$E = T + V = \sum_{i=1}^N \frac{1}{2} m_i \|\mathbf{v}_i\|^2 - \sum_{i=1}^N \sum_{j > i}^N \frac{G m_i m_j}{\|\mathbf{r}_i - \mathbf{r}_j\|}$$

### 5.2 Relative Energy Conservation Drift
$$\text{Relative Energy Error} = \frac{|E(t) - E(0)|}{|E(0)|}$$

### 5.3 Angular Momentum Vector
$$\mathbf{L} = \sum_{i=1}^N m_i (\mathbf{r}_i \times \mathbf{v}_i)$$

### 5.4 Symplectic Integration Property
Standard integrators (e.g. RK4) suffer from secular energy dissipation over long timespans. Symplectic integrators (e.g. Leapfrog Velocity-Verlet, WHFast) preserve the symplectic 2-form $d\mathbf{p} \wedge d\mathbf{q}$ in phase space, ensuring that energy error oscillates within a strictly bounded envelope without secular dissipation.
