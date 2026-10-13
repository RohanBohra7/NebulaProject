"""
High-precision astronomical reference catalog for NEBULA.
Grounded in empirical datasets from NASA Planetary Fact Sheet, JPL Horizons,
NASA Exoplanet Archive, SIMBAD Astronomical Database, and Gaia DR3.
"""

ASTRONOMICAL_CATALOG = [
    # ==================== SUN & SOLAR SYSTEM PLANETS ====================
    {
        "id": "sun",
        "name": "Sun (Sol)",
        "category": "Star",
        "parent_body_id": None,
        "mass_kg": 1.98847e30,
        "mass_earth_relative": 332946.0,
        "radius_km": 696340.0,
        "radius_earth_relative": 109.2,
        "mean_density_g_cm3": 1.408,
        "surface_gravity_m_s2": 274.0,
        "escape_velocity_km_s": 617.5,
        "surface_temperature_k": 5778.0,
        "luminosity_solar": 1.0,
        "spectral_type": "G2V",
        "apparent_magnitude": -26.74,
        "absolute_magnitude": 4.83,
        "semi_major_axis_au": 0.0,
        "eccentricity": 0.0,
        "orbital_inclination_deg": 0.0,
        "orbital_period_days": 0.0,
        "perihelion_au": 0.0,
        "aphelion_au": 0.0,
        "mean_orbital_velocity_km_s": 0.0,
        "color_hex": "#f59e0b",
        "texture_preset": "sun",
        "has_rings": False,
        "has_atmosphere": True,
        "description_citizen": "The glowing heart of our solar system! A giant nuclear furnace that provides the light, warmth, and gravity keeping all planets in their cosmic dance.",
        "description_student": "The Sun is a middle-aged yellow dwarf main-sequence star (G2V). It fuses 600 million tons of hydrogen into helium every second in its core via the proton-proton chain reaction, maintaining hydrostatic equilibrium against gravitational collapse.",
        "description_researcher": "G2V spectral type main-sequence star ($M_\\odot = 1.98847 \\times 10^{30}\\,\\text{kg}$, $R_\\odot = 6.9634 \\times 10^{8}\\,\\text{m}$, $T_{\\text{eff}} = 5778\\,\\text{K}$). Core proton-proton (p-p I) thermonuclear fusion sustains a radiative zone ($0.25 - 0.70\\,R_\\odot$) and an outer convective zone generating an active solar dynamo with an approximately 11-year magnetic Schwabe cycle.",
        "educational_facts": [
            "The Sun contains 99.86% of all mass in the entire solar system.",
            "Light takes approximately 8 minutes and 20 seconds to travel from the Sun to Earth.",
            "About 1.3 million Earths could fit inside the volume of the Sun."
        ],
        "research_notes": {
            "metallicity_fe_h": "+0.00",
            "age_gyr": 4.603,
            "core_temperature_k": 1.57e7,
            "solar_wind_mass_loss_rate_kg_s": 1.4e9
        },
        "data_source": "NASA Planetary Fact Sheet / JPL Solar System Dynamics",
        "data_confidence": "High"
    },
    {
        "id": "mercury",
        "name": "Mercury",
        "category": "Planet",
        "parent_body_id": "sun",
        "mass_kg": 3.3011e23,
        "mass_earth_relative": 0.0553,
        "radius_km": 2439.7,
        "radius_earth_relative": 0.383,
        "mean_density_g_cm3": 5.427,
        "surface_gravity_m_s2": 3.7,
        "escape_velocity_km_s": 4.25,
        "surface_temperature_k": 440.0,
        "luminosity_solar": 0.0,
        "spectral_type": None,
        "apparent_magnitude": -0.42,
        "absolute_magnitude": None,
        "semi_major_axis_au": 0.3871,
        "eccentricity": 0.2056,
        "orbital_inclination_deg": 7.005,
        "orbital_period_days": 87.97,
        "perihelion_au": 0.3075,
        "aphelion_au": 0.4667,
        "mean_orbital_velocity_km_s": 47.36,
        "color_hex": "#9ca3af",
        "texture_preset": "mercury",
        "has_rings": False,
        "has_atmosphere": False,
        "description_citizen": "The fastest world in the solar system! Mercury speeds around the Sun in just 88 days, experiencing extreme temperature swings between scorching days and freezing nights.",
        "description_student": "Mercury is the smallest planet and closest to the Sun. It has a high orbital eccentricity (0.206) and a 3:2 spin-orbit resonance, meaning it rotates on its axis three times for every two orbits around the Sun.",
        "description_researcher": "Innermost terrestrial planet exhibiting significant relativistic perihelion precession (42.98 arcsec/century anomalous precession, confirming Einstein's General Relativity). Features a large metallic core (~70% radius) and a 3:2 spin-orbit resonance ($P_{\\text{orb}} = 87.97\\,\\text{d}$, $P_{\\text{rot}} = 58.65\\,\\text{d}$).",
        "educational_facts": [
            "A day-night cycle on Mercury takes 176 Earth days, twice as long as its year!",
            "Its surface temperature ranges from -180°C at night to 430°C in direct sunlight.",
            "Water ice exists permanently inside deep craters at Mercury's polar regions."
        ],
        "research_notes": {
            "perihelion_advance_arcsec_century": 42.98,
            "core_radius_fraction": 0.75,
            "surface_magnetic_field_gauss": 0.003
        },
        "data_source": "NASA Planetary Fact Sheet / MESSENGER Mission Data",
        "data_confidence": "High"
    },
    {
        "id": "venus",
        "name": "Venus",
        "category": "Planet",
        "parent_body_id": "sun",
        "mass_kg": 4.8675e24,
        "mass_earth_relative": 0.815,
        "radius_km": 6051.8,
        "radius_earth_relative": 0.949,
        "mean_density_g_cm3": 5.243,
        "surface_gravity_m_s2": 8.87,
        "escape_velocity_km_s": 10.36,
        "surface_temperature_k": 737.0,
        "luminosity_solar": 0.0,
        "spectral_type": None,
        "apparent_magnitude": -4.40,
        "absolute_magnitude": None,
        "semi_major_axis_au": 0.7233,
        "eccentricity": 0.0067,
        "orbital_inclination_deg": 3.394,
        "orbital_period_days": 224.7,
        "perihelion_au": 0.7184,
        "aphelion_au": 0.7282,
        "mean_orbital_velocity_km_s": 35.02,
        "color_hex": "#eab308",
        "texture_preset": "venus",
        "has_rings": False,
        "has_atmosphere": True,
        "description_citizen": "Often called Earth's twin due to its similar size, Venus is actually an intense greenhouse inferno shrouded in dense, reflective sulfuric acid clouds.",
        "description_student": "Venus has a runaway greenhouse effect caused by a dense CO2 atmosphere (96.5%) with surface pressures 92 times that of Earth. It rotates backwards (retrograde rotation) extremely slowly.",
        "description_researcher": "Terrestrial planet with retrograde rotation ($P_{\\text{rot}} = -243.02\\,\\text{d}$) and near-circular orbit ($e = 0.0067$). Thick atmosphere ($P_{\\text{surf}} \\approx 9.2\\,\\text{MPa}$, 96.5% $\\text{CO}_2$) exhibits atmospheric super-rotation with wind speeds reaching $100\\,\\text{m/s}$ at cloud tops.",
        "educational_facts": [
            "Venus is hotter than Mercury despite being nearly twice as far from the Sun.",
            "The Sun rises in the west and sets in the east on Venus.",
            "Surface pressure is equivalent to being 900 meters deep in Earth's ocean."
        ],
        "research_notes": {
            "surface_pressure_bar": 92.0,
            "greenhouse_warming_k": 450.0,
            "retrograde_obliquity_deg": 177.36
        },
        "data_source": "NASA Planetary Fact Sheet / Magellan Radar",
        "data_confidence": "High"
    },
    {
        "id": "earth",
        "name": "Earth",
        "category": "Planet",
        "parent_body_id": "sun",
        "mass_kg": 5.9722e24,
        "mass_earth_relative": 1.0,
        "radius_km": 6371.0,
        "radius_earth_relative": 1.0,
        "mean_density_g_cm3": 5.514,
        "surface_gravity_m_s2": 9.807,
        "escape_velocity_km_s": 11.186,
        "surface_temperature_k": 288.0,
        "luminosity_solar": 0.0,
        "spectral_type": None,
        "apparent_magnitude": None,
        "absolute_magnitude": None,
        "semi_major_axis_au": 1.0,
        "eccentricity": 0.0167,
        "orbital_inclination_deg": 0.0,
        "orbital_period_days": 365.256,
        "perihelion_au": 0.9833,
        "aphelion_au": 1.0167,
        "mean_orbital_velocity_km_s": 29.78,
        "color_hex": "#38bdf8",
        "texture_preset": "earth",
        "has_rings": False,
        "has_atmosphere": True,
        "description_citizen": "Our home harbor in the cosmic ocean! The only known world with liquid surface oceans, a protective atmosphere, and thriving biodiversity.",
        "description_student": "Earth resides precisely in the circumstellar habitable zone ('Goldilocks zone'), allowing liquid water to exist stably. Its liquid iron-nickel outer core generates a magnetosphere that shields surface life from solar radiation.",
        "description_researcher": "Reference terrestrial body ($1.0\\,\\text{AU}$, $1.0\\,M_\\oplus$). Possesses active plate tectonics, oxygen-nitrogen atmosphere ($78\\%\\,\\text{N}_2, 21\\%\\,\\text{O}_2$), dipolar geodynamo ($B_{\\text{surf}} \\approx 30-60\\,\\mu\\text{T}$), and a dynamically stabilizing large natural satellite ($M_{\\text{moon}}/M_\\oplus \\approx 1/81.3$).",
        "educational_facts": [
            "Over 71% of Earth's surface is covered with liquid water.",
            "Earth's magnetic shield deflects high-energy charged particles from solar storms.",
            "Our atmosphere is the only known planetary atmosphere with free diatomic oxygen."
        ],
        "research_notes": {
            "albedo_bond": 0.306,
            "geoid_j2": 1.08263e-3,
            "axial_tilt_obliquity_deg": 23.44,
            "solar_constant_w_m2": 1361.0
        },
        "data_source": "NASA Planetary Fact Sheet / IERS Conventions",
        "data_confidence": "High"
    },
    {
        "id": "moon",
        "name": "Moon (Luna)",
        "category": "Moon",
        "parent_body_id": "earth",
        "mass_kg": 7.342e22,
        "mass_earth_relative": 0.0123,
        "radius_km": 1737.4,
        "radius_earth_relative": 0.2727,
        "mean_density_g_cm3": 3.344,
        "surface_gravity_m_s2": 1.62,
        "escape_velocity_km_s": 2.38,
        "surface_temperature_k": 220.0,
        "luminosity_solar": 0.0,
        "spectral_type": None,
        "apparent_magnitude": -12.74,
        "absolute_magnitude": None,
        "semi_major_axis_au": 0.00257, # 384,400 km
        "eccentricity": 0.0549,
        "orbital_inclination_deg": 5.145,
        "orbital_period_days": 27.322,
        "perihelion_au": 0.00242,
        "aphelion_au": 0.00271,
        "mean_orbital_velocity_km_s": 1.022,
        "color_hex": "#cbd5e1",
        "texture_preset": "moon",
        "has_rings": False,
        "has_atmosphere": False,
        "description_citizen": "Earth's loyal companion! Tidal locking keeps its same luminous face pointed toward us every night as it guides oceanic tides.",
        "description_student": "The Moon is tidally locked to Earth with a 1:1 synchronous rotation. It formed approximately 4.5 billion years ago likely through the Giant Impact hypothesis (Theia collision).",
        "description_researcher": "Tidally locked natural satellite in a 5.14° inclined orbit to the ecliptic. Semi-major axis $a = 384,400\\,\\text{km}$ ($0.00257\\,\\text{AU}$) receding at $3.82\\,\\text{cm/yr}$ due to tidal dissipation torque transfer. Anorthositic lunar highlands and basaltic maria crust.",
        "educational_facts": [
            "The Moon is gradually moving away from Earth at about 3.8 cm per year.",
            "Footprints left by Apollo astronauts will remain for millions of years due to no wind or water erosion.",
            "The Moon is the fifth largest natural satellite in the solar system."
        ],
        "research_notes": {
            "tidal_recession_rate_cm_yr": 3.82,
            "synchronous_rotation": True,
            "surface_regolith_depth_m": 4.5
        },
        "data_source": "NASA Lunar Reconnaissance Orbiter / Apollo Seismic Data",
        "data_confidence": "High"
    },
    {
        "id": "mars",
        "name": "Mars",
        "category": "Planet",
        "parent_body_id": "sun",
        "mass_kg": 6.4171e23,
        "mass_earth_relative": 0.107,
        "radius_km": 3389.5,
        "radius_earth_relative": 0.532,
        "mean_density_g_cm3": 3.933,
        "surface_gravity_m_s2": 3.72,
        "escape_velocity_km_s": 5.03,
        "surface_temperature_k": 210.0,
        "luminosity_solar": 0.0,
        "spectral_type": None,
        "apparent_magnitude": -2.94,
        "absolute_magnitude": None,
        "semi_major_axis_au": 1.524,
        "eccentricity": 0.0934,
        "orbital_inclination_deg": 1.85,
        "orbital_period_days": 686.98,
        "perihelion_au": 1.3814,
        "aphelion_au": 1.6660,
        "mean_orbital_velocity_km_s": 24.07,
        "color_hex": "#ef4444",
        "texture_preset": "mars",
        "has_rings": False,
        "has_atmosphere": True,
        "description_citizen": "The Red Planet! A rust-colored desert world home to towering extinct volcanoes, vast canyons, and ancient dried river valleys.",
        "description_student": "Mars features the largest volcano in the solar system, Olympus Mons (21.9 km tall), and Valles Marineris canyon. Its thin CO2 atmosphere and lack of a global magnetic field allowed solar winds to strip away ancient surface water.",
        "description_researcher": "Outer terrestrial planet with significant orbital eccentricity ($e = 0.0934$). Low surface atmospheric pressure ($P \\approx 610\\,\\text{Pa}$, 95% $\\text{CO}_2$). Crustal remanent magnetic fields indicate an ancient dynamo ceased $\\sim 4.0\\,\\text{Ga}$. Subsurface water ice reservoirs identified via SHARAD radar sounder.",
        "educational_facts": [
            "Olympus Mons on Mars is three times taller than Mount Everest.",
            "Sunsets on Mars appear blue due to dust particles scattering reddish light.",
            "A Martian day (called a sol) is 24 hours, 39 minutes, and 35 seconds."
        ],
        "research_notes": {
            "crustal_magnetic_anomalies": True,
            "atmospheric_scale_height_km": 11.1,
            "valles_marineris_length_km": 4000.0
        },
        "data_source": "NASA Mars Exploration Program / MAVEN & MRO",
        "data_confidence": "High"
    },
    {
        "id": "jupiter",
        "name": "Jupiter",
        "category": "Planet",
        "parent_body_id": "sun",
        "mass_kg": 1.8982e27,
        "mass_earth_relative": 317.8,
        "radius_km": 69911.0,
        "radius_earth_relative": 10.97,
        "mean_density_g_cm3": 1.326,
        "surface_gravity_m_s2": 24.79,
        "escape_velocity_km_s": 59.5,
        "surface_temperature_k": 165.0,
        "luminosity_solar": 0.0,
        "spectral_type": None,
        "apparent_magnitude": -2.94,
        "absolute_magnitude": None,
        "semi_major_axis_au": 5.2044,
        "eccentricity": 0.0489,
        "orbital_inclination_deg": 1.303,
        "orbital_period_days": 4332.59,
        "perihelion_au": 4.9504,
        "aphelion_au": 5.4584,
        "mean_orbital_velocity_km_s": 13.07,
        "color_hex": "#d97706",
        "texture_preset": "jupiter",
        "has_rings": True,
        "has_atmosphere": True,
        "description_citizen": "The colossus of our solar system! A swirling giant of hydrogen and helium with a storm bigger than Earth called the Great Red Spot.",
        "description_student": "Jupiter is the most massive planet, containing more than double the mass of all other planets combined. It acts as a cosmic shield, clearing cometary debris with its enormous gravitational field.",
        "description_researcher": "Gas giant planet ($M = 317.8\\,M_\\oplus$, $1.8982 \\times 10^{27}\\,\\text{kg}$) composed predominantly of $\\text{H}$ (~90% mole fraction) and $\\text{He}$ (~10%). Possesses an extensive magnetosphere driven by a metallic hydrogen mantle dynamo with equatorial magnetic field $\\sim 4.28\\,\\text{Gauss}$. Strong influence on solar system architecture via orbital resonances (Kirkwood gaps).",
        "educational_facts": [
            "Jupiter rotates faster than any other planet, completing a full turn in under 10 hours.",
            "The Great Red Spot is a persistent anticyclonic storm that has raged for at least 350 years.",
            "Jupiter has 95 officially recognized moons, including the four massive Galilean moons."
        ],
        "research_notes": {
            "juno_gravity_j2": 1.4697e-2,
            "metallic_hydrogen_transition_mbar": 2.0,
            "trojan_asteroid_cloud_l4_l5": True
        },
        "data_source": "NASA Juno Mission / JPL Planetary Data",
        "data_confidence": "High"
    },
    {
        "id": "saturn",
        "name": "Saturn",
        "category": "Planet",
        "parent_body_id": "sun",
        "mass_kg": 5.6834e26,
        "mass_earth_relative": 95.16,
        "radius_km": 58232.0,
        "radius_earth_relative": 9.14,
        "mean_density_g_cm3": 0.687,
        "surface_gravity_m_s2": 10.44,
        "escape_velocity_km_s": 35.5,
        "surface_temperature_k": 134.0,
        "luminosity_solar": 0.0,
        "spectral_type": None,
        "apparent_magnitude": 0.46,
        "absolute_magnitude": None,
        "semi_major_axis_au": 9.582,
        "eccentricity": 0.0565,
        "orbital_inclination_deg": 2.485,
        "orbital_period_days": 10759.22,
        "perihelion_au": 9.0412,
        "aphelion_au": 10.1238,
        "mean_orbital_velocity_km_s": 9.68,
        "color_hex": "#fde047",
        "texture_preset": "saturn",
        "has_rings": True,
        "has_atmosphere": True,
        "description_citizen": "The crowned jewel of the night sky! Famous for its breathtaking, dazzling system of icy rings stretching hundreds of thousands of kilometers.",
        "description_student": "Saturn is the least dense planet in the solar system—at 0.687 g/cm³, it would float in a giant bathtub of water! Its spectacular rings consist of 99% pure water ice particles.",
        "description_researcher": "Gas giant planet with lowest mean bulk density ($0.687\\,\\text{g/cm}^3$) in the solar system. Ring system spans $7,000$ to $80,000\\,\\text{km}$ above equator with optical depth $\\tau$ up to 5, sustained by shepherd moons (Prometheus, Pandora) and Enceladus cryovolcanic replenishment. Highly aligned magnetic dipole axis ($< 0.005^\\circ$ tilt from rotational axis).",
        "educational_facts": [
            "Saturn's rings are up to 282,000 km across, but typically only 10 to 30 meters thick!",
            "Saturn is the only planet in the solar system with an average density lower than liquid water.",
            "The Cassini spacecraft discovered geysers of water shooting from Saturn's moon Enceladus."
        ],
        "research_notes": {
            "ring_mass_kg": 1.54e19,
            "cassini_division_width_km": 4800,
            "hexagonal_polar_jet_velocity_m_s": 100.0
        },
        "data_source": "NASA Cassini-Huygens Mission / JPL Planetary Data",
        "data_confidence": "High"
    },
    {
        "id": "uranus",
        "name": "Uranus",
        "category": "Planet",
        "parent_body_id": "sun",
        "mass_kg": 8.6810e25,
        "mass_earth_relative": 14.54,
        "radius_km": 25362.0,
        "radius_earth_relative": 3.98,
        "mean_density_g_cm3": 1.270,
        "surface_gravity_m_s2": 8.69,
        "escape_velocity_km_s": 21.3,
        "surface_temperature_k": 76.0,
        "luminosity_solar": 0.0,
        "spectral_type": None,
        "apparent_magnitude": 5.68,
        "absolute_magnitude": None,
        "semi_major_axis_au": 19.201,
        "eccentricity": 0.0463,
        "orbital_inclination_deg": 0.773,
        "orbital_period_days": 30685.4,
        "perihelion_au": 18.33,
        "aphelion_au": 20.06,
        "mean_orbital_velocity_km_s": 6.80,
        "color_hex": "#67e8f9",
        "texture_preset": "uranus",
        "has_rings": True,
        "has_atmosphere": True,
        "description_citizen": "An icy cyan realm rolling on its side like a bowling ball through the cold depths of the outer solar system.",
        "description_student": "Uranus is an ice giant with an extreme axial tilt of 97.77°, meaning its north and south poles take turns pointing almost directly at the Sun during its 84-year orbit.",
        "description_researcher": "Ice giant planet with retrograde rotation and severe obliquity (axial tilt $97.77^\\circ$). Interior composition dominated by 'ices' (water, methane, ammonia high-pressure phases) rather than hydrogen gas. Highly tilted ($59^\\circ$) and offset ($0.33\\,R_U$) non-dipolar magnetic field.",
        "educational_facts": [
            "Uranus was the first planet discovered with a telescope, by William Herschel in 1781.",
            "Its atmospheric methane absorbs red light, giving the planet its distinctive cyan color.",
            "Uranus has 28 known moons, all named after characters by William Shakespeare and Alexander Pope."
        ],
        "research_notes": {
            "axial_tilt_deg": 97.77,
            "magnetic_dipole_tilt_deg": 59.0,
            "internal_heat_flux_anomaly": "Unusually low intrinsic thermal emission"
        },
        "data_source": "NASA Voyager 2 / Hubble Space Telescope",
        "data_confidence": "High"
    },
    {
        "id": "neptune",
        "name": "Neptune",
        "category": "Planet",
        "parent_body_id": "sun",
        "mass_kg": 1.02413e26,
        "mass_earth_relative": 17.15,
        "radius_km": 24622.0,
        "radius_earth_relative": 3.86,
        "mean_density_g_cm3": 1.638,
        "surface_gravity_m_s2": 11.15,
        "escape_velocity_km_s": 23.5,
        "surface_temperature_k": 72.0,
        "luminosity_solar": 0.0,
        "spectral_type": None,
        "apparent_magnitude": 7.78,
        "absolute_magnitude": None,
        "semi_major_axis_au": 30.07,
        "eccentricity": 0.0095,
        "orbital_inclination_deg": 1.768,
        "orbital_period_days": 60189.0,
        "perihelion_au": 29.81,
        "aphelion_au": 30.33,
        "mean_orbital_velocity_km_s": 5.43,
        "color_hex": "#3b82f6",
        "texture_preset": "neptune",
        "has_rings": True,
        "has_atmosphere": True,
        "description_citizen": "A deep-azure ice giant where supersonic winds whip across stormy clouds at the edge of our planetary neighborhood.",
        "description_student": "Neptune was the first planet located via mathematical prediction rather than direct observation. It experiences the fastest winds in the solar system, clocking up to 2,100 km/h.",
        "description_researcher": "Ice giant planet ($17.15\\,M_\\oplus$) exhibiting 3:2 mean-motion resonance with Pluto and Plutinos. Internal heat engine radiates 2.61 times the solar energy it absorbs, fueling supersonic atmospheric zonal jets reaching $v > 600\\,\\text{m/s}$. Dynamic magnetosphere inclined at $47^\\circ$.",
        "educational_facts": [
            "Predicted mathematically by Urbain Le Verrier before Johann Galle observed it in 1846.",
            "Neptune's moon Triton orbits backwards (retrograde) and is likely a captured Kuiper Belt object.",
            "One year on Neptune lasts nearly 165 Earth years."
        ],
        "research_notes": {
            "internal_heat_ratio": 2.61,
            "maximum_wind_speed_km_h": 2160,
            "kuiper_belt_resonance_stabilizer": True
        },
        "data_source": "NASA Voyager 2 / Keck Observatory",
        "data_confidence": "High"
    },
    {
        "id": "pluto",
        "name": "Pluto",
        "category": "Planet", # Dwarf Planet
        "parent_body_id": "sun",
        "mass_kg": 1.303e22,
        "mass_earth_relative": 0.00218,
        "radius_km": 1188.3,
        "radius_earth_relative": 0.186,
        "mean_density_g_cm3": 1.854,
        "surface_gravity_m_s2": 0.62,
        "escape_velocity_km_s": 1.21,
        "surface_temperature_k": 44.0,
        "luminosity_solar": 0.0,
        "spectral_type": None,
        "apparent_magnitude": 15.1,
        "absolute_magnitude": None,
        "semi_major_axis_au": 39.48,
        "eccentricity": 0.2488,
        "orbital_inclination_deg": 17.16,
        "orbital_period_days": 90560.0,
        "perihelion_au": 29.66,
        "aphelion_au": 49.31,
        "mean_orbital_velocity_km_s": 4.67,
        "color_hex": "#a8a29e",
        "texture_preset": "pluto",
        "has_rings": False,
        "has_atmosphere": True,
        "description_citizen": "The beloved outpost of the Kuiper Belt! A frosty world featuring nitrogen ice glaciers shaped into a famous heart named Tombaugh Regio.",
        "description_student": "Pluto is classified as a dwarf planet because it has not cleared the neighborhood around its orbit. It shares a binary system relationship with its large moon Charon, orbiting a common center of mass outside Pluto itself.",
        "description_researcher": "Archetypal Plutino in a stable 2:3 mean-motion resonance with Neptune. Features a high inclination ($17.16^\\circ$) and eccentricity ($0.2488$). Mutual tidal locking with Charon ($P = 6.387\\,\\text{d}$) with system barycenter located $1.83\\,R_{\\text{Pluto}}$ above Pluto's surface. Sputnik Planitia displays active convection in solid nitrogen-methane-CO ice.",
        "educational_facts": [
            "Pluto is smaller in surface area than Russia, yet possesses towering water-ice mountains.",
            "Because Pluto and Charon orbit a point in space between them, they are effectively a double-planet system.",
            "New Horizons flew past Pluto in July 2015 at 49,600 km/h, sending back high-resolution images."
        ],
        "research_notes": {
            "barycenter_above_surface_km": 960,
            "nitrogen_ice_convection_cell_depth_km": 10.0,
            "neptune_resonance": "2:3"
        },
        "data_source": "NASA New Horizons Mission / JPL Horizons",
        "data_confidence": "High"
    },

    # ==================== GALILEAN & SATURNIAN MOONS ====================
    {
        "id": "europa",
        "name": "Europa",
        "category": "Moon",
        "parent_body_id": "jupiter",
        "mass_kg": 4.8e22,
        "mass_earth_relative": 0.008,
        "radius_km": 1560.8,
        "radius_earth_relative": 0.245,
        "mean_density_g_cm3": 3.013,
        "surface_gravity_m_s2": 1.315,
        "escape_velocity_km_s": 2.025,
        "surface_temperature_k": 102.0,
        "luminosity_solar": 0.0,
        "spectral_type": None,
        "apparent_magnitude": 5.29,
        "absolute_magnitude": None,
        "semi_major_axis_au": 0.00448, # 670,900 km
        "eccentricity": 0.009,
        "orbital_inclination_deg": 0.47,
        "orbital_period_days": 3.551,
        "perihelion_au": 0.00444,
        "aphelion_au": 0.00452,
        "mean_orbital_velocity_km_s": 13.74,
        "color_hex": "#e2e8f0",
        "texture_preset": "europa",
        "has_rings": False,
        "has_atmosphere": True,
        "description_citizen": "An icy beacon for the search for extraterrestrial life! Beneath its crisscrossed crust lies a vast global saltwater ocean.",
        "description_student": "Europa's smooth, fractured ice shell conceals a liquid water ocean containing more water than all of Earth's oceans combined. Tidal flexing from Jupiter and sibling moons provides the internal heat keeping the water liquid.",
        "description_researcher": "Galilean satellite participating in the 4:2:1 Laplace orbital resonance with Io and Ganymede. Subsurface liquid water ocean ($d \\sim 100\\,\\text{km}$) sustained by tidal dissipation heating ($Q_{\\text{tide}} \\sim 10^{12}\\,\\text{W}$). Induced magnetic dipole moment detected by Galileo magnetometer confirms conductive liquid layer.",
        "educational_facts": [
            "Europa holds an estimated 2 to 3 times more liquid water than Earth.",
            "Its surface is one of the smoothest in the solar system, with very few impact craters.",
            "NASA's Europa Clipper mission is on its way to investigate its habitability."
        ],
        "research_notes": {
            "ocean_depth_km": 100,
            "ice_shell_thickness_km": 20,
            "laplace_resonance_partner": "Io (1:2) & Ganymede (2:1)"
        },
        "data_source": "NASA Galileo Orbiter / Europa Clipper Science Objectives",
        "data_confidence": "High"
    },
    {
        "id": "titan",
        "name": "Titan",
        "category": "Moon",
        "parent_body_id": "saturn",
        "mass_kg": 1.3452e23,
        "mass_earth_relative": 0.0225,
        "radius_km": 2574.7,
        "radius_earth_relative": 0.404,
        "mean_density_g_cm3": 1.88,
        "surface_gravity_m_s2": 1.352,
        "escape_velocity_km_s": 2.639,
        "surface_temperature_k": 94.0,
        "luminosity_solar": 0.0,
        "spectral_type": None,
        "apparent_magnitude": 8.28,
        "absolute_magnitude": None,
        "semi_major_axis_au": 0.00817, # 1,221,870 km
        "eccentricity": 0.0288,
        "orbital_inclination_deg": 0.3485,
        "orbital_period_days": 15.945,
        "perihelion_au": 0.00793,
        "aphelion_au": 0.00840,
        "mean_orbital_velocity_km_s": 5.57,
        "color_hex": "#f59e0b",
        "texture_preset": "titan",
        "has_rings": False,
        "has_atmosphere": True,
        "description_citizen": "The only moon in the solar system with a dense atmosphere, complete with clouds, rain, rivers, and lakes of liquid methane and ethane!",
        "description_student": "Titan has an active hydrological cycle, but instead of water, the liquid raining down and filling lakes like Kraken Mare is liquid natural gas. Its atmosphere is 95% nitrogen and 1.5 times thicker than Earth's.",
        "description_researcher": "Second-largest satellite in solar system ($R = 2574.7\\,\\text{km}$, larger than Mercury). Features a substantial nitrogen atmosphere ($P_{\\text{surf}} = 146.7\\,\\text{kPa}$, 95% $\\text{N}_2$, 5% $\\text{CH}_4$). Methane acts as a condensable volatile driving hydrocarbon precipitation, fluvial valley networks, and liquid hydrocarbon seas (Kraken Mare, Ligeia Mare).",
        "educational_facts": [
            "You could strap on artificial wings and fly on Titan using human muscle power due to dense air and low gravity!",
            "ESA's Huygens probe landed on Titan in 2005, transmitting sound and photos of rounded river stones.",
            "Titan is larger than the planet Mercury."
        ],
        "research_notes": {
            "surface_pressure_kpa": 146.7,
            "kraken_mare_area_km2": 400000,
            "photochemical_tholin_haze": True
        },
        "data_source": "NASA/ESA Cassini-Huygens Mission Data",
        "data_confidence": "High"
    },

    # ==================== EXOPLANET SYSTEMS ====================
    {
        "id": "trappist-1",
        "name": "TRAPPIST-1",
        "category": "Star",
        "parent_body_id": None,
        "mass_kg": 1.785e29,
        "mass_earth_relative": 29888.0,
        "radius_km": 84180.0,
        "radius_earth_relative": 13.2,
        "mean_density_g_cm3": 71.3,
        "surface_gravity_m_s2": 612.0,
        "escape_velocity_km_s": 752.0,
        "surface_temperature_k": 2566.0,
        "luminosity_solar": 0.000553,
        "spectral_type": "M8V",
        "apparent_magnitude": 18.8,
        "absolute_magnitude": 18.4,
        "semi_major_axis_au": 0.0,
        "eccentricity": 0.0,
        "orbital_inclination_deg": 0.0,
        "orbital_period_days": 0.0,
        "perihelion_au": 0.0,
        "aphelion_au": 0.0,
        "mean_orbital_velocity_km_s": 0.0,
        "color_hex": "#dc2626",
        "texture_preset": "red_dwarf",
        "has_rings": False,
        "has_atmosphere": True,
        "description_citizen": "An ultra-cool red dwarf star located 40 light-years away, famous for hosting seven Earth-sized worlds packed closely around it.",
        "description_student": "TRAPPIST-1 is barely larger than Jupiter in radius, but about 90 times more massive. Because it burns its fuel very slowly, it can shine for over 10 trillion years—hundreds of times longer than the current age of the universe!",
        "description_researcher": "Ultra-cool red dwarf star ($M = 0.0898\\,M_\\odot$, $R = 0.121\\,R_\\odot$, $T_{\\text{eff}} = 2566\\,\\text{K}$, spectral type M8V) hosting an extraordinary resonant chain of 7 transiting terrestrial exoplanets within $0.06\\,\\text{AU}$. Distance $12.1\\,\\text{pc}$ (39.5 ly).",
        "educational_facts": [
            "All seven of TRAPPIST-1's planets orbit closer to their star than Mercury does to the Sun.",
            "From the surface of one planet, neighboring worlds would appear larger than the full Moon in our sky.",
            "The star is so cool that its light is emitted mostly in the infrared."
        ],
        "research_notes": {
            "distance_pc": 12.14,
            "metallicity_fe_h": "+0.04",
            "age_gyr": 7.6,
            "flaring_activity": "Active chromospheric flare emissions"
        },
        "data_source": "NASA Exoplanet Archive / Gillon et al. (Nature 2017)",
        "data_confidence": "High"
    },
    {
        "id": "trappist-1e",
        "name": "TRAPPIST-1e",
        "category": "Exoplanet",
        "parent_body_id": "trappist-1",
        "mass_kg": 4.13e24,
        "mass_earth_relative": 0.692,
        "radius_km": 5861.0,
        "radius_earth_relative": 0.920,
        "mean_density_g_cm3": 5.65,
        "surface_gravity_m_s2": 9.12,
        "escape_velocity_km_s": 9.69,
        "surface_temperature_k": 251.0,
        "luminosity_solar": 0.0,
        "spectral_type": None,
        "apparent_magnitude": None,
        "absolute_magnitude": None,
        "semi_major_axis_au": 0.02925,
        "eccentricity": 0.0051,
        "orbital_inclination_deg": 89.86,
        "orbital_period_days": 6.0996,
        "perihelion_au": 0.0291,
        "aphelion_au": 0.0294,
        "mean_orbital_velocity_km_s": 52.6,
        "color_hex": "#38bdf8",
        "texture_preset": "exoplanet_habitable",
        "has_rings": False,
        "has_atmosphere": True,
        "description_citizen": "One of the most promising candidates for an Earth-like world outside our solar system, sitting comfortably in its star's habitable zone.",
        "description_student": "TRAPPIST-1e receives about 66% of the stellar energy that Earth receives from the Sun, making its estimated equilibrium temperature very close to Earth's. It orbits its host star in just 6.1 days.",
        "description_researcher": "Habitable zone terrestrial exoplanet ($M = 0.692\\,M_\\oplus$, $R = 0.920\\,R_\\oplus$, $\\rho = 5.65\\,\\text{g/cm}^3$) in Laplace-like resonance chain. Equilibrium temperature $T_{\\text{eq}} = 251\\,\\text{K}$ (Earth equivalent $255\\,\\text{K}$). High Earth Similarity Index ($ESI = 0.85$). JWST NIRSpec/MIRI transmission spectroscopy candidate.",
        "educational_facts": [
            "TRAPPIST-1e is considered one of the top targets for NASA's James Webb Space Telescope to search for atmospheric biosignatures.",
            "The planet is likely tidally locked, meaning one hemisphere faces perpetual day and the other perpetual night.",
            "Its year is only 6.1 Earth days long!"
        ],
        "research_notes": {
            "esi_index": 0.85,
            "stellar_flux_ratio_earth": 0.662,
            "transit_depth_ppm": 4820,
            "resonance_ratio": "4:3 with 1d, 3:2 with 1f"
        },
        "data_source": "NASA Exoplanet Archive / Grimm et al. (A&A 2018)",
        "data_confidence": "High"
    },
    {
        "id": "proxima-b",
        "name": "Proxima Centauri b",
        "category": "Exoplanet",
        "parent_body_id": "sun", # Orbiting Proxima Centauri
        "mass_kg": 6.98e24,
        "mass_earth_relative": 1.173,
        "radius_km": 6817.0,
        "radius_earth_relative": 1.07,
        "mean_density_g_cm3": 5.4,
        "surface_gravity_m_s2": 10.0,
        "escape_velocity_km_s": 11.7,
        "surface_temperature_k": 234.0,
        "luminosity_solar": 0.0,
        "spectral_type": None,
        "apparent_magnitude": None,
        "absolute_magnitude": None,
        "semi_major_axis_au": 0.0485,
        "eccentricity": 0.109,
        "orbital_inclination_deg": 61.0,
        "orbital_period_days": 11.186,
        "perihelion_au": 0.0432,
        "aphelion_au": 0.0538,
        "mean_orbital_velocity_km_s": 47.3,
        "color_hex": "#0284c7",
        "texture_preset": "exoplanet_habitable",
        "has_rings": False,
        "has_atmosphere": True,
        "description_citizen": "Our closest exoplanetary neighbor, orbiting the nearest star to our solar system just 4.24 light-years away in the Alpha Centauri system.",
        "description_student": "Proxima Centauri b orbits in the habitable zone of an M-dwarf star, completing an orbit every 11.2 days. However, its host star releases violent coronal flares that may strip its atmosphere.",
        "description_researcher": "Terrestrial exoplanet detected via radial velocity ($M \\sin i = 1.173\\,M_\\oplus$, $P = 11.186\\,\\text{d}$) around the closest star ($d = 1.30\\,\\text{pc}$). Incident bolometric flux $S = 0.65\\,S_\\oplus$. Host star flare frequency poses severe atmospheric erosion challenges via extreme UV/X-ray photoevaporation.",
        "educational_facts": [
            "At 4.24 light-years away, Proxima b is the nearest known exoplanet to Earth.",
            "It would take about 75,000 years for modern chemical rockets to reach Proxima b.",
            "The Breakthrough Starshot project proposes sending laser-propelled nanocrafts to photograph it in under 25 years."
        ],
        "research_notes": {
            "radial_velocity_amplitude_m_s": 1.38,
            "distance_light_years": 4.246,
            "x_ray_flux_multiplier_earth": 250.0
        },
        "data_source": "ESO / Anglada-Escudé et al. (Nature 2016)",
        "data_confidence": "High"
    },
    {
        "id": "kepler-452b",
        "name": "Kepler-452b",
        "category": "Exoplanet",
        "parent_body_id": "sun",
        "mass_kg": 2.98e25,
        "mass_earth_relative": 5.0,
        "radius_km": 10385.0,
        "radius_earth_relative": 1.63,
        "mean_density_g_cm3": 4.9,
        "surface_gravity_m_s2": 18.4,
        "escape_velocity_km_s": 19.6,
        "surface_temperature_k": 265.0,
        "luminosity_solar": 0.0,
        "spectral_type": None,
        "apparent_magnitude": None,
        "absolute_magnitude": None,
        "semi_major_axis_au": 1.046,
        "eccentricity": 0.035,
        "orbital_inclination_deg": 89.8,
        "orbital_period_days": 384.84,
        "perihelion_au": 1.01,
        "aphelion_au": 1.08,
        "mean_orbital_velocity_km_s": 29.1,
        "color_hex": "#10b981",
        "texture_preset": "super_earth",
        "has_rings": False,
        "has_atmosphere": True,
        "description_citizen": "Nicknamed 'Earth's Older Cousin'! A super-Earth orbiting a star very similar to our Sun in an orbit lasting almost exactly one Earth year.",
        "description_student": "Kepler-452b is about 60% larger than Earth in diameter. It orbits a G2-type star that is 1.5 billion years older than our Sun, offering scientists a glimpse into Earth's possible future climate as our Sun ages.",
        "description_researcher": "Super-Earth transiting exoplanet ($R = 1.63\\,R_\\oplus$, estimated $M \\sim 5\\,M_\\oplus$) orbiting a solar analog ($G2V, T_{\\text{eff}} = 5757\\,\\text{K}, 6.0\\,\\text{Gyr}$). Period $P = 384.84\\,\\text{d}$ and semi-major axis $a = 1.046\\,\\text{AU}$. Lies near the Fulton gap ($1.5-2.0\\,R_\\oplus$), bridging rocky super-Earths and volatile-rich sub-Neptunes.",
        "educational_facts": [
            "Kepler-452b takes 385 days to orbit its star, remarkably close to Earth's 365 days.",
            "Its host star is 20% brighter and 10% larger in diameter than our Sun.",
            "Located approximately 1,400 light-years away in the constellation Cygnus."
        ],
        "research_notes": {
            "distance_pc": 430.0,
            "fulton_gap_status": "Upper boundary rocky/sub-Neptune transition",
            "insolation_flux_earth_ratio": 1.10
        },
        "data_source": "NASA Kepler Mission / Jenkins et al. (AJ 2015)",
        "data_confidence": "High"
    },

    # ==================== FAMOUS STARS ====================
    {
        "id": "sirius-a",
        "name": "Sirius A (Alpha Canis Majoris)",
        "category": "Star",
        "parent_body_id": None,
        "mass_kg": 4.10e30,
        "mass_earth_relative": 686000.0,
        "radius_km": 1190000.0,
        "radius_earth_relative": 186.8,
        "mean_density_g_cm3": 0.58,
        "surface_gravity_m_s2": 192.0,
        "escape_velocity_km_s": 678.0,
        "surface_temperature_k": 9940.0,
        "luminosity_solar": 25.4,
        "spectral_type": "A1V",
        "apparent_magnitude": -1.46,
        "absolute_magnitude": 1.42,
        "semi_major_axis_au": 0.0,
        "eccentricity": 0.0,
        "orbital_inclination_deg": 0.0,
        "orbital_period_days": 0.0,
        "perihelion_au": 0.0,
        "aphelion_au": 0.0,
        "mean_orbital_velocity_km_s": 0.0,
        "color_hex": "#60a5fa",
        "texture_preset": "blue_star",
        "has_rings": False,
        "has_atmosphere": True,
        "description_citizen": "The Dog Star! The brightest star visible from Earth, shining with an icy blue-white brilliance in the winter constellation Canis Major.",
        "description_student": "Sirius appears so bright in our night sky because it is both 25 times more luminous than our Sun and relatively close to us—only 8.6 light-years away. It has a tiny white dwarf companion named Sirius B.",
        "description_researcher": "A1V main-sequence primary of a binary system ($d = 2.64\\,\\text{pc}$, $8.6\\,\\text{ly}$). Mass $M = 2.063\\,M_\\odot$, radius $R = 1.711\\,R_\\odot$, $T_{\\text{eff}} = 9940\\,\\text{K}$. Gravitationally bound to white dwarf Sirius B with a 50.1-year orbital period ($e = 0.591$).",
        "educational_facts": [
            "Sirius is the brightest star in the night sky with an apparent magnitude of -1.46.",
            "Ancient Egyptians timed their agricultural calendar to the heliacal rising of Sirius, which marked the annual flooding of the Nile.",
            "Its white dwarf companion, Sirius B, was the first white dwarf star ever discovered."
        ],
        "research_notes": {
            "distance_pc": 2.64,
            "binary_companion": "Sirius B (DA2 white dwarf)",
            "binary_period_years": 50.13,
            "binary_eccentricity": 0.5914
        },
        "data_source": "SIMBAD / Gaia DR3 / Hipparcos",
        "data_confidence": "High"
    },
    {
        "id": "betelgeuse",
        "name": "Betelgeuse (Alpha Orionis)",
        "category": "Star",
        "parent_body_id": None,
        "mass_kg": 3.28e31,
        "mass_earth_relative": 5490000.0,
        "radius_km": 530000000.0, # ~764 R_sun
        "radius_earth_relative": 83000.0,
        "mean_density_g_cm3": 1.2e-8,
        "surface_gravity_m_s2": 0.003,
        "escape_velocity_km_s": 91.0,
        "surface_temperature_k": 3600.0,
        "luminosity_solar": 126000.0,
        "spectral_type": "M1-M2Ia-ab",
        "apparent_magnitude": 0.50,
        "absolute_magnitude": -5.85,
        "semi_major_axis_au": 0.0,
        "eccentricity": 0.0,
        "orbital_inclination_deg": 0.0,
        "orbital_period_days": 0.0,
        "perihelion_au": 0.0,
        "aphelion_au": 0.0,
        "mean_orbital_velocity_km_s": 0.0,
        "color_hex": "#f97316",
        "texture_preset": "red_supergiant",
        "has_rings": False,
        "has_atmosphere": True,
        "description_citizen": "A colossal red supergiant pulsating at Orion's right shoulder! If placed in our solar system, its surface would engulf the orbits of Mars and Jupiter.",
        "description_student": "Betelgeuse is near the end of its stellar life. It has burned through its core hydrogen and will eventually explode in a catastrophic core-collapse supernova (Type II), shining as bright as the full Moon for months.",
        "description_researcher": "Semi-regular pulsating red supergiant ($M \\sim 16.5-19\\,M_\\odot$, $R \\sim 764\\,R_\\odot$, $L \\sim 1.26 \\times 10^5\\,L_\\odot$, $T_{\\text{eff}} \\sim 3600\\,\\text{K}$). Distance $168\\,\\text{pc}$ ($548\\,\\text{ly}$). Underwent the 'Great Dimming' in late 2019 caused by large episodic convective surface mass ejection condensing into an obscuring dust cloud.",
        "educational_facts": [
            "If Betelgeuse were at the center of our solar system, its outer surface would extend beyond the orbit of Mars!",
            "When Betelgeuse explodes as a supernova, it will be visible during broad daylight.",
            "In 2019, Betelgeuse mysteriously dimmed by more than a full magnitude, sparking worldwide scientific attention."
        ],
        "research_notes": {
            "distance_pc": 168.0,
            "supernova_progenitor_type": "Type II-P",
            "pulsation_period_days": 420,
            "mass_loss_rate_m_sun_yr": 2e-6
        },
        "data_source": "ESO VLT / SPHERE / ALMA / SIMBAD",
        "data_confidence": "High"
    },

    # ==================== DEEP SKY OBJECTS ====================
    {
        "id": "m31-andromeda",
        "name": "Messier 31 (Andromeda Galaxy)",
        "category": "Deep-Sky",
        "parent_body_id": None,
        "mass_kg": 3.0e42, # ~1.5e12 M_sun
        "mass_earth_relative": 5.0e17,
        "radius_km": 1.04e18, # ~110,000 light years radius
        "radius_earth_relative": 1.6e14,
        "mean_density_g_cm3": 1e-24,
        "surface_gravity_m_s2": 0.0,
        "escape_velocity_km_s": 500.0,
        "surface_temperature_k": None,
        "luminosity_solar": 2.6e10,
        "spectral_type": "SA(s)b",
        "apparent_magnitude": 3.44,
        "absolute_magnitude": -21.5,
        "semi_major_axis_au": 0.0,
        "eccentricity": 0.0,
        "orbital_inclination_deg": 77.0,
        "orbital_period_days": 0.0,
        "perihelion_au": 0.0,
        "aphelion_au": 0.0,
        "mean_orbital_velocity_km_s": -301.0, # Approaching Milky Way
        "color_hex": "#818cf8",
        "texture_preset": "spiral_galaxy",
        "has_rings": False,
        "has_atmosphere": False,
        "description_citizen": "Our grand neighboring spiral island of a trillion stars! The most distant object you can see with the naked eye on a clear, dark night.",
        "description_student": "Andromeda is approximately 2.5 million light-years away from Earth. It and our Milky Way are gravitationally attracted to each other and will collide in about 4.5 billion years to form a giant elliptical galaxy ('Milkomeda').",
        "description_researcher": "Barred spiral galaxy (Hubble classification SA(s)b) and dominant member of the Local Group alongside the Milky Way. Total virial mass $M_{\\text{vir}} \\sim 1.5 \\times 10^{12}\\,M_\\odot$ including dark matter halo. Distance $765\\,\\text{kpc}$ ($2.5\\,\\text{Mly}$). Radial velocity $v_{\\text{rad}} = -301\\,\\text{km/s}$ approaching Milky Way barycenter.",
        "educational_facts": [
            "Andromeda contains approximately one trillion stars, more than double the Milky Way.",
            "Light you see tonight from Andromeda started its journey when early hominids were first crafting stone tools.",
            "The collision between Andromeda and the Milky Way will not destroy stars because interstellar distances are vast."
        ],
        "research_notes": {
            "distance_kpc": 765.0,
            "dark_matter_fraction": 0.90,
            "supermassive_black_hole_mass_m_sun": 1.4e8,
            "local_group_virial_mass": "Dominant"
        },
        "data_source": "Hubble Space Telescope / Gaia Collaboration / NED",
        "data_confidence": "High"
    },
    {
        "id": "sagittarius-a-star",
        "name": "Sagittarius A*",
        "category": "Deep-Sky",
        "parent_body_id": None,
        "mass_kg": 8.26e36, # ~4.15 million M_sun
        "mass_earth_relative": 1.38e12,
        "radius_km": 12000000.0, # Schwarzschild radius ~12 million km (0.08 AU)
        "radius_earth_relative": 1880.0,
        "mean_density_g_cm3": 1e6,
        "surface_gravity_m_s2": 3.8e8,
        "escape_velocity_km_s": 299792.0, # Speed of light
        "surface_temperature_k": None,
        "luminosity_solar": 100.0,
        "spectral_type": "SMBH",
        "apparent_magnitude": None,
        "absolute_magnitude": None,
        "semi_major_axis_au": 0.0,
        "eccentricity": 0.0,
        "orbital_inclination_deg": 0.0,
        "orbital_period_days": 0.0,
        "perihelion_au": 0.0,
        "aphelion_au": 0.0,
        "mean_orbital_velocity_km_s": 0.0,
        "color_hex": "#1e1b4b",
        "texture_preset": "black_hole",
        "has_rings": True, # Accretion disk
        "has_atmosphere": False,
        "description_citizen": "The supermassive black hole at the gravitational anchor of our Milky Way galaxy! A dark singularity with the mass of four million Suns.",
        "description_student": "Sagittarius A* is located 26,000 light-years away at the galactic center. In 2022, the Event Horizon Telescope captured the first direct silhouette of its glowing orange radio ring warped by extreme gravity.",
        "description_researcher": "Supermassive black hole ($M = 4.154 \\pm 0.014 \\times 10^6\\,M_\\odot$) at the dynamical center of the Milky Way ($d = 8.178\\,\\text{kpc}$). Gravitational radius $r_g = GM/c^2 \\approx 6.13 \\times 10^9\\,\\text{m}$; Schwarzschild event horizon radius $R_s = 2r_g \\approx 1.23 \\times 10^{10}\\,\\text{m}$ ($0.082\\,\\text{AU}$). Event Horizon Telescope resolved shadow diameter of $51.8\\,\\mu\\text{as}$.",
        "educational_facts": [
            "Stars near Sagittarius A*, like S2, orbit it at dizzying speeds exceeding 7,000 km per second!",
            "Its event horizon has an angular size on sky equivalent to a donut placed on the surface of the Moon.",
            "Andrea Ghez and Reinhard Genzel won the 2020 Nobel Prize in Physics for tracking stars around Sgr A*."
        ],
        "research_notes": {
            "distance_kpc": 8.178,
            "schwarzschild_radius_au": 0.082,
            "eht_shadow_diameter_microarcsec": 51.8,
            "s2_star_pericenter_speed_c": 0.0255
        },
        "data_source": "Event Horizon Telescope (ApJL 2022) / GRAVITY Collaboration",
        "data_confidence": "High"
    },

    # ==================== SMALL BODIES & COMETS ====================
    {
        "id": "1p-halley",
        "name": "1P/Halley",
        "category": "Comet",
        "parent_body_id": "sun",
        "mass_kg": 2.2e14,
        "mass_earth_relative": 3.7e-11,
        "radius_km": 5.5,
        "radius_earth_relative": 0.00086,
        "mean_density_g_cm3": 0.6,
        "surface_gravity_m_s2": 0.002,
        "escape_velocity_km_s": 0.003,
        "surface_temperature_k": 200.0,
        "luminosity_solar": 0.0,
        "spectral_type": None,
        "apparent_magnitude": 28.2, # Near aphelion
        "absolute_magnitude": 5.5,
        "semi_major_axis_au": 17.834,
        "eccentricity": 0.9671,
        "orbital_inclination_deg": 162.26,
        "orbital_period_days": 27500.0, # ~75.3 years
        "perihelion_au": 0.586,
        "aphelion_au": 35.08,
        "mean_orbital_velocity_km_s": 54.5, # High at perihelion
        "color_hex": "#64748b",
        "texture_preset": "comet",
        "has_rings": False,
        "has_atmosphere": True, # Coma & tail
        "description_citizen": "History's most legendary comet! Every 75-76 years, it dives inwards from beyond Neptune to grace our night skies with a luminous glowing dust tail.",
        "description_student": "Halley's Comet has a highly eccentric orbit ($e = 0.967$) and orbits backward (retrograde inclination of 162°). It produces two annual meteor showers on Earth: the Eta Aquariids and Orionids.",
        "description_researcher": "Periodic comet with highly eccentric retrograde orbit ($a = 17.834\\,\\text{AU}$, $e = 0.9671$, $i = 162.26^\\circ$, $P = 75.3\\,\\text{yr}$). Nucleus dimensions $15 \\times 8 \\times 8\\,\\text{km}$ with low albedo ($p_v = 0.04$) determined by ESA Giotto flyby. Sublimating volatile inventory dominated by $\\text{H}_2\\text{O}$ (~80%), $\\text{CO}$ (~10-15%), and $\\text{CO}_2$ (~3%).",
        "educational_facts": [
            "Next perihelion passage is calculated to occur on July 28, 2061.",
            "Halley was depicted in the historic 1066 Bayeux Tapestry before the Battle of Hastings.",
            "Edmond Halley used Isaac Newton's newly formulated laws of gravitation to predict its return in 1758."
        ],
        "research_notes": {
            "nucleus_albedo": 0.04,
            "next_perihelion_year": 2061,
            "giotto_flyby_distance_km": 596
        },
        "data_source": "ESA Giotto Mission / JPL Small-Body Database",
        "data_confidence": "High"
    },
    {
        "id": "ceres",
        "name": "1 Ceres",
        "category": "Asteroid",
        "parent_body_id": "sun",
        "mass_kg": 9.3835e20,
        "mass_earth_relative": 0.000157,
        "radius_km": 473.0,
        "radius_earth_relative": 0.0742,
        "mean_density_g_cm3": 2.161,
        "surface_gravity_m_s2": 0.284,
        "escape_velocity_km_s": 0.516,
        "surface_temperature_k": 168.0,
        "luminosity_solar": 0.0,
        "spectral_type": "C-type",
        "apparent_magnitude": 6.65,
        "absolute_magnitude": 3.34,
        "semi_major_axis_au": 2.767,
        "eccentricity": 0.0758,
        "orbital_inclination_deg": 10.59,
        "orbital_period_days": 1682.0,
        "perihelion_au": 2.557,
        "aphelion_au": 2.977,
        "mean_orbital_velocity_km_s": 17.9,
        "color_hex": "#94a3b8",
        "texture_preset": "asteroid",
        "has_rings": False,
        "has_atmosphere": False,
        "description_citizen": "The monarch of the asteroid belt! The largest object between Mars and Jupiter, containing one-third of the total mass of the asteroid belt.",
        "description_student": "Ceres is classified as both an asteroid and a dwarf planet because its gravity is strong enough to pull it into a round spherical shape (hydrostatic equilibrium). NASA's Dawn mission discovered bright sodium carbonate salt deposits in Occator Crater.",
        "description_researcher": "Dwarf planet and largest body in the main asteroid belt ($a = 2.767\\,\\text{AU}$, $e = 0.0758$, $i = 10.59^\\circ$). Differentiated body exhibiting hydrostatic equilibrium ($R_{\\text{mean}} = 473.0\\,\\text{km}$). Hydrothermally altered clay-carbonate mineralogy. Transient water vapor exosphere detected via Herschel Space Observatory.",
        "educational_facts": [
            "Ceres contains about one-third of the entire mass in the main asteroid belt.",
            "Bright white spots inside Occator Crater are salt deposits left behind after briny subsurface water erupted and evaporated.",
            "Discovered on January 1, 1801, by Italian astronomer Giuseppe Piazzi."
        ],
        "research_notes": {
            "dawn_gravity_j2": 0.016,
            "occator_faculae_composition": "Sodium carbonate / ammonium salts",
            "ice_rich_mantle_fraction": 0.25
        },
        "data_source": "NASA Dawn Mission / JPL Horizons",
        "data_confidence": "High"
    }
]

# =====================================================================
# PHASE 2 DATA LAYER NORMALIZATION & METADATA ENRICHMENT
# =====================================================================

ROTATION_PERIODS_HOURS = {
    "sun": 609.12,          # 25.38 days equatorial
    "mercury": 1407.6,      # 58.65 days
    "venus": -5832.5,       # -243.02 days retrograde
    "earth": 23.934,        # 0.997 days
    "moon": 655.72,         # 27.32 days synchronous
    "mars": 24.623,         # 1.026 days
    "jupiter": 9.925,       # 0.414 days
    "saturn": 10.656,       # 0.444 days
    "uranus": -17.24,       # -0.718 days retrograde
    "neptune": 16.11,       # 0.671 days
    "pluto": -153.29,       # -6.387 days retrograde
    "europa": 85.23,        # 3.55 days synchronous
    "titan": 382.68,        # 15.945 days synchronous
    "ceres": 9.074,
    "1p-halley": 52.8,
    "sirius-a": 132.0,
    "betelgeuse": 87600.0,
    "trappist-1": 79.2
}

DISCOVERY_METADATA = {
    "sun": {"discoverer": "Prehistoric", "discovery_year": "Antiquity", "discovery_method": "Naked Eye"},
    "mercury": {"discoverer": "Prehistoric", "discovery_year": "Antiquity", "discovery_method": "Naked Eye"},
    "venus": {"discoverer": "Prehistoric", "discovery_year": "Antiquity", "discovery_method": "Naked Eye"},
    "earth": {"discoverer": "Origin of Humanity", "discovery_year": "Prehistoric", "discovery_method": "Native Habitat"},
    "moon": {"discoverer": "Prehistoric", "discovery_year": "Antiquity", "discovery_method": "Naked Eye"},
    "mars": {"discoverer": "Prehistoric", "discovery_year": "Antiquity", "discovery_method": "Naked Eye"},
    "jupiter": {"discoverer": "Prehistoric", "discovery_year": "Antiquity", "discovery_method": "Naked Eye"},
    "saturn": {"discoverer": "Prehistoric", "discovery_year": "Antiquity", "discovery_method": "Naked Eye"},
    "uranus": {"discoverer": "William Herschel", "discovery_year": "1781", "discovery_method": "Telescopic"},
    "neptune": {"discoverer": "Urbain Le Verrier & Johann Galle", "discovery_year": "1846", "discovery_method": "Mathematical Prediction"},
    "pluto": {"discoverer": "Clyde Tombaugh", "discovery_year": "1930", "discovery_method": "Photographic Comparison"},
    "europa": {"discoverer": "Galileo Galilei", "discovery_year": "1610", "discovery_method": "Telescopic"},
    "titan": {"discoverer": "Christiaan Huygens", "discovery_year": "1655", "discovery_method": "Telescopic"},
    "ceres": {"discoverer": "Giuseppe Piazzi", "discovery_year": "1801", "discovery_method": "Telescopic"},
    "1p-halley": {"discoverer": "Edmond Halley", "discovery_year": "1705", "discovery_method": "Periodic Orbit Computation"},
    "sirius-a": {"discoverer": "Prehistoric", "discovery_year": "Antiquity", "discovery_method": "Naked Eye"},
    "betelgeuse": {"discoverer": "Prehistoric", "discovery_year": "Antiquity", "discovery_method": "Naked Eye"},
    "m31-andromeda": {"discoverer": "Abd al-Rahman al-Sufi", "discovery_year": "964", "discovery_method": "Naked Eye Observation"},
    "sagittarius-a-star": {"discoverer": "Bruce Balick & Robert Brown", "discovery_year": "1974", "discovery_method": "Radio Interferometry"},
    "trappist-1": {"discoverer": "Michaël Gillon et al.", "discovery_year": "1999", "discovery_method": "Photometric Sky Survey"},
    "trappist-1e": {"discoverer": "Michaël Gillon et al. / Spitzer", "discovery_year": "2017", "discovery_method": "Transit Photometry"},
    "proxima-b": {"discoverer": "Guillem Anglada-Escudé et al. / HARPS", "discovery_year": "2016", "discovery_method": "Radial Velocity"},
    "kepler-452b": {"discoverer": "NASA Kepler Science Team", "discovery_year": "2015", "discovery_method": "Transit Photometry"}
}

SOURCE_REFERENCE_URLS = {
    "sun": "https://nssdc.gsfc.nasa.gov/planetary/factsheet/sunfact.html",
    "mercury": "https://nssdc.gsfc.nasa.gov/planetary/factsheet/mercuryfact.html",
    "venus": "https://nssdc.gsfc.nasa.gov/planetary/factsheet/venusfact.html",
    "earth": "https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html",
    "moon": "https://nssdc.gsfc.nasa.gov/planetary/factsheet/moonfact.html",
    "mars": "https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html",
    "jupiter": "https://nssdc.gsfc.nasa.gov/planetary/factsheet/jupiterfact.html",
    "saturn": "https://nssdc.gsfc.nasa.gov/planetary/factsheet/saturnfact.html",
    "uranus": "https://nssdc.gsfc.nasa.gov/planetary/factsheet/uranusfact.html",
    "neptune": "https://nssdc.gsfc.nasa.gov/planetary/factsheet/neptunefact.html",
    "pluto": "https://nssdc.gsfc.nasa.gov/planetary/factsheet/plutofact.html",
    "europa": "https://solarsystem.nasa.gov/moons/jupiter-moons/europa/in-depth/",
    "titan": "https://solarsystem.nasa.gov/moons/saturn-moons/titan/in-depth/",
    "ceres": "https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html#/?sstr=1",
    "1p-halley": "https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html#/?sstr=1P",
    "sirius-a": "https://simbad.cds.unistra.fr/simbad/sim-id?Ident=Sirius",
    "betelgeuse": "https://simbad.cds.unistra.fr/simbad/sim-id?Ident=Betelgeuse",
    "m31-andromeda": "https://simbad.cds.unistra.fr/simbad/sim-id?Ident=M31",
    "sagittarius-a-star": "https://eventhorizontelescope.org/",
    "trappist-1": "https://exoplanetarchive.ipac.caltech.edu/",
    "trappist-1e": "https://exoplanetarchive.ipac.caltech.edu/overview/TRAPPIST-1e",
    "proxima-b": "https://exoplanetarchive.ipac.caltech.edu/overview/Proxima%20Cen%20b",
    "kepler-452b": "https://exoplanetarchive.ipac.caltech.edu/overview/Kepler-452%20b"
}

STANDARD_UNITS = {
    "mass": "kg",
    "radius": "km",
    "gravity": "m/s²",
    "distance_from_sun": "AU",
    "orbital_period": "days",
    "rotation_period": "hours",
    "orbital_velocity": "km/s",
    "temperature": "K"
}

# Apply enrichment pass
for _item in ASTRONOMICAL_CATALOG:
    _oid = _item["id"]
    _item["object_type"] = _item.get("category", "Generic")
    _item["description"] = _item.get("description_citizen") or _item.get("description_student") or f"{_item.get('name')} is a celestial body."
    _item["mass"] = _item.get("mass_kg")
    _item["radius"] = _item.get("radius_km")
    _item["gravity"] = _item.get("surface_gravity_m_s2")
    _item["distance_from_sun"] = _item.get("semi_major_axis_au")
    _item["orbital_period"] = _item.get("orbital_period_days")
    _item["rotation_period"] = ROTATION_PERIODS_HOURS.get(_oid)
    _item["orbital_velocity"] = _item.get("mean_orbital_velocity_km_s")
    _item["temperature"] = _item.get("surface_temperature_k")
    _item["parent_object"] = _item.get("parent_body_id")
    _item["orbital_parameters"] = {
        "semi_major_axis_au": _item.get("semi_major_axis_au"),
        "eccentricity": _item.get("eccentricity"),
        "orbital_inclination_deg": _item.get("orbital_inclination_deg"),
        "perihelion_au": _item.get("perihelion_au"),
        "aphelion_au": _item.get("aphelion_au")
    }
    _item["discovery_information"] = DISCOVERY_METADATA.get(_oid, {})
    _item["source"] = _item.get("data_source", "NASA Planetary Fact Sheet / JPL Solar System Dynamics")
    _item["source_url"] = SOURCE_REFERENCE_URLS.get(_oid, "https://nssdc.gsfc.nasa.gov/planetary/factsheet/")
    _item["is_demo_seed"] = True
    _item["units"] = dict(STANDARD_UNITS)
    _item["metadata"] = _item.get("research_notes", {})

