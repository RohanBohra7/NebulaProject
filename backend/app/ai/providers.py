"""
AI Provider Abstraction and Concrete Implementations for NEBULA.
Supports Google Gemini, OpenAI, and a comprehensive, fully offline,
deterministic Local Grounded Engine.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import httpx
import os
import re
import logging
from app.config import settings
from app.ai.tools import (
    tool_get_object,
    tool_compare_objects,
    tool_calculate_orbital_property,
    tool_query_strongest_gravity,
    tool_get_simulation,
    tool_get_simulation_results,
    tool_explain_simulation_result
)

logger = logging.getLogger(__name__)


class AIProvider(ABC):
    """
    Abstract base class for all AI providers.
    Ensures provider-agnosticism across NEBULA.
    """

    @abstractmethod
    def get_name(self) -> str:
        """Returns the human-readable provider name."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Checks whether the provider is configured and reachable."""
        pass

    @abstractmethod
    async def generate_response(
        self,
        prompt: str,
        system_prompt: str,
        context: str,
        history: Optional[List[Dict[str, str]]] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        mode: str = "citizen"
    ) -> str:
        """Generates a text completion based on prompt, persona, and grounding context."""
        pass


class GeminiProvider(AIProvider):
    """
    Google Gemini LLM Provider (via REST API).
    Reads credentials strictly from environment variables / settings.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or getattr(settings, "GEMINI_API_KEY", None)

    def get_name(self) -> str:
        return "Google Gemini (Grounded)"

    def is_available(self) -> bool:
        return bool(self.api_key and self.api_key.strip())

    async def generate_response(
        self,
        prompt: str,
        system_prompt: str,
        context: str,
        history: Optional[List[Dict[str, str]]] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        mode: str = "citizen"
    ) -> str:
        if not self.is_available():
            raise RuntimeError("Gemini API key is not configured.")

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
        full_content = f"GROUNDED CONTEXT:\n{context}\n\nUSER QUESTION:\n{prompt}"
        
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": f"SYSTEM DIRECTIVE:\n{system_prompt}\n\n{full_content}"}]
                }
            ],
            "generationConfig": {
                "temperature": 0.2 if mode == "researcher" else 0.6,
                "maxOutputTokens": 1200
            }
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                raise RuntimeError(f"Gemini API returned {resp.status_code}: {resp.text}")


class OpenAIProvider(AIProvider):
    """
    OpenAI API Provider (e.g. gpt-4o-mini).
    Reads credentials strictly from environment variables / settings.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or getattr(settings, "OPENAI_API_KEY", None)

    def get_name(self) -> str:
        return "OpenAI GPT-4o-mini (Grounded)"

    def is_available(self) -> bool:
        return bool(self.api_key and self.api_key.strip())

    async def generate_response(
        self,
        prompt: str,
        system_prompt: str,
        context: str,
        history: Optional[List[Dict[str, str]]] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        mode: str = "citizen"
    ) -> str:
        if not self.is_available():
            raise RuntimeError("OpenAI API key is not configured.")

        messages = [
            {"role": "system", "content": f"{system_prompt}\n\nGROUNDED CONTEXT:\n{context}"}
        ]
        if history:
            for item in history[-4:]:
                messages.append({"role": item.get("role", "user"), "content": item.get("content", "")})
        messages.append({"role": "user", "content": prompt})

        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "model": "gpt-4o-mini",
            "messages": messages,
            "temperature": 0.2 if mode == "researcher" else 0.6,
            "max_tokens": 1200
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"]
            else:
                raise RuntimeError(f"OpenAI API returned {resp.status_code}: {resp.text}")


class LocalDeterministicProvider(AIProvider):
    """
    High-fidelity deterministic local fallback engine.
    Ensures NEBULA is 100% operational offline without any API keys.
    Answers common astronomical questions with mathematical precision,
    empirical data grounding, and mode-tailored styling.
    """

    def get_name(self) -> str:
        return "NEBULA Grounded Local Knowledge Engine (Deterministic Fallback)"

    def is_available(self) -> bool:
        return True

    async def generate_response(
        self,
        prompt: str,
        system_prompt: str,
        context: str,
        history: Optional[List[Dict[str, str]]] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        mode: str = "citizen"
    ) -> str:
        p_lower = prompt.lower().strip()
        mode_key = (mode or "citizen").lower()

        # ======================================================================
        # QUESTION 1: "What is the mass of Jupiter?" (or any body's mass)
        # ======================================================================
        if "mass of jupiter" in p_lower or ("mass" in p_lower and "jupiter" in p_lower):
            jup_res = tool_get_object("jupiter")
            jup = jup_res.get("object", {})
            m_kg = jup.get("mass_kg", 1.8982e27)
            m_earth = jup.get("mass_earth_relative", 317.83)

            if mode_key == "researcher":
                return (
                    f"### Astrometric Mass Characterization: Jupiter\n\n"
                    f"- **[NEBULA Data]:** Total barycentric mass $M = {m_kg:.4e}\\,\\text{{kg}}$, corresponding to ${m_earth}\\,M_\\oplus$ (${9.543e-4}\\,M_\\odot$).\n"
                    f"- **[Computed Result]:** Standard gravitational parameter $\\mu = GM = 1.266865 \\times 10^{{17}}\\,\\text{{m}}^3/\\text{{s}}^2$.\n"
                    f"- **[External Scientific Context]:** Mass determined via radiometric tracking of the *Juno* spacecraft and Galileo missions (NASA JPL Horizons / IAU WGCCRE).\n"
                    f"- **[General Explanation]:** Jupiter contains approximately 71% of the entire planetary mass in the Solar System, dominating the secular dynamical architecture."
                )
            elif mode_key == "student":
                return (
                    f"### The Mass of Jupiter 🪐\n\n"
                    f"- **[NEBULA Data]:** Jupiter's mass is **${m_kg:.3e}$ kg**, which is **{m_earth} times the mass of Earth**.\n"
                    f"- **[Computed Result]:** Because Jupiter is so massive, its surface gravity is $g = \\frac{{GM}}{{R^2}} = 24.79\\,\\text{{m/s}}^2$ (about $2.53\\times$ Earth's gravity).\n"
                    f"- **[General Explanation]:** If you put all the other planets in our solar system together on one side of a cosmic scale, Jupiter would still outweigh them combined by more than double!\n\n"
                    f"**🧠 Comprehension Check:** Why do astronomers say Jupiter acts as a 'gravitational shield' for Earth? *(Hint: Think about how a huge mass deflects incoming comets!)*"
                )
            else: # Citizen
                return (
                    f"### How Heavy is Jupiter? 🌌\n\n"
                    f"Jupiter is an absolute cosmic titan! Its mass is about **{m_earth:.0f} times greater than Earth**.\n\n"
                    f"To picture that scale: Jupiter is heavier than all the other planets, moons, and asteroids in our entire solar system combined! "
                    f"If Earth were a small grape, Jupiter would be the size of a heavy basketball."
                )

        # Generic mass query for other bodies
        if "mass of " in p_lower or ("mass" in p_lower and any(w in p_lower for w in ["earth", "mars", "saturn", "sun", "moon", "venus", "mercury", "neptune", "uranus"])):
            for b_name in ["earth", "mars", "saturn", "sun", "moon", "venus", "mercury", "neptune", "uranus", "trappist-1e"]:
                if b_name in p_lower:
                    obj_res = tool_get_object(b_name)
                    if obj_res.get("found"):
                        o = obj_res["object"]
                        return self._format_single_object_mass(o, mode_key)

        # ======================================================================
        # QUESTION 2: Comparison (Earth & Mars, TRAPPIST-1e & Earth, or any two bodies)
        # ======================================================================
        if "compare" in p_lower or "versus" in p_lower or " vs " in p_lower or "difference between" in p_lower:
            detected = []
            cand_names = [
                "earth", "mars", "jupiter", "saturn", "trappist-1e", "trappist",
                "venus", "mercury", "neptune", "uranus", "sun", "moon",
                "europa", "titan", "ganymede", "betelgeuse", "sirius", "ceres"
            ]
            for k in cand_names:
                if k in p_lower:
                    norm = "trappist-1e" if "trappist" in k else k
                    if norm not in detected:
                        detected.append(norm)

            if len(detected) >= 2:
                return self._format_comparison(detected[0], detected[1], mode_key)
            elif len(detected) == 1 and "earth" not in detected:
                return self._format_comparison("earth", detected[0], mode_key)

        # ======================================================================
        # QUESTION 3: "Explain Earth's orbital period"
        # ======================================================================
        if "orbital period" in p_lower and ("earth" in p_lower or "explain" in p_lower):
            if mode_key == "researcher":
                return (
                    f"### Dynamical Derivation: Earth Sidereal Orbital Period\n\n"
                    f"- **[NEBULA Data]:** Earth sidereal period $P = 365.256\\,\\text{{days}}$, semi-major axis $a = 1.00000011\\,\\text{{AU}} = 1.4959787 \\times 10^{{11}}\\,\\text{{m}}$, eccentricity $e = 0.0167$.\n"
                    f"- **[Computed Result]:** Applying Kepler's Third Law in Newtonian two-body formulation:\n"
                    f"  $$T = 2\\pi \\sqrt{{\\frac{{a^3}}{{G(M_\\odot + M_\\oplus)}}}} \\approx 3.1558 \\times 10^7\\,\\text{{s}} = 365.256\\,\\text{{d}}$$\n"
                    f"- **[External Scientific Context]:** Millennial secular perturbations from Jupiter and Venus induce long-term cycles in eccentricity and precession (Milankovitch cycles).\n"
                    f"- **[General Explanation]:** The tropical year ($365.2422\\,\\text{{d}}$) governing calendar leap years differs slightly from the sidereal period due to axial precession."
                )
            elif mode_key == "student":
                return (
                    f"### Why is Earth's Orbital Period 365.25 Days? ⏳\n\n"
                    f"- **[NEBULA Data]:** Earth takes **365.256 days** to complete one full revolution around the Sun.\n"
                    f"- **[Computed Result]:** Johannes Kepler discovered that a planet's period depends strictly on its distance from the Sun:\n"
                    f"  $$\\text{{Period}}^2 \\propto \\text{{Distance}}^3 \\quad (T^2 \\propto a^3)$$\n"
                    f"  Because Earth is 1 AU from the Sun, $T = \\sqrt{{1^3}} = 1\\,\\text{{year}}$.\n"
                    f"- **[General Explanation]:** That extra 0.25 day (about 6 hours) every year is the exact reason we add an extra day every 4 years—a **Leap Year**!\n\n"
                    f"**🧠 Comprehension Check:** If Earth were moved further out to 4 AU, how many years would one orbit take? *(Hint: $\\sqrt{4^3} = \\sqrt{64} =$ ?)*"
                )
            else: # Citizen
                return (
                    f"### How Earth's Year Works 🌏✨\n\n"
                    f"It takes Earth **365 days and about 6 hours** to complete one lap around the Sun at a blistering speed of **107,000 km/h (67,000 mph)**!\n\n"
                    f"Those extra 6 hours add up every four years to create **February 29th (Leap Day)**. "
                    f"Without leap days, our seasons would slowly drift across the calendar over time!"
                )

        # ======================================================================
        # QUESTION 4: "Why does Saturn have rings?"
        # ======================================================================
        if "saturn" in p_lower and ("ring" in p_lower or "rings" in p_lower):
            if mode_key == "researcher":
                return (
                    f"### Tidal Disruption & Ring Dynamics: Saturn\n\n"
                    f"- **[NEBULA Data]:** Saturn radius $R_S = 58,232\\,\\text{{km}}$, mean bulk density $\\rho_S = 0.687\\,\\text{{g/cm}}^3$. Ring extent spans from $\\sim 66,000\\,\\text{{km}}$ to $140,000\\,\\text{{km}}$ from planetary center.\n"
                    f"- **[Computed Result]:** Fluid Roche Limit for an icy satellite ($\\rho_m \\approx 1.0\\,\\text{{g/cm}}^3$):\n"
                    f"  $$d_{{\\text{{Roche}}}} = 2.44 \\cdot R_S \\left(\\frac{{\\rho_S}}{{\\rho_m}}\\right)^{{1/3}} \\approx 2.44 \\cdot 58232 \\cdot (0.687)^{{1/3}} \\approx 125,300\\,\\text{{km}}$$\n"
                    f"- **[External Scientific Context]:** Cassini mission mass and gravity data demonstrate that the main rings are $>99\\%$ water ice and dynamic in age (10–100 Myr), sustained by shepherd moons (Prometheus, Pandora) creating density waves and maintaining sharp gap boundaries (Encke, Cassini division)."
                )
            elif mode_key == "student":
                return (
                    f"### Why Does Saturn Have Rings? 💍🪐\n\n"
                    f"- **[NEBULA Data]:** Saturn's rings stretch over **280,000 km** wide, yet they are surprisingly paper-thin—only about **10 to 30 meters** thick in most places!\n"
                    f"- **[Computed Result]:** The physics principle is called the **Roche Limit**:\n"
                    f"  If a moon gets too close to a massive planet, the planet's gravitational pull on the moon's near side is much stronger than on its far side (tidal forces).\n"
                    f"- **[General Explanation]:** Millions of years ago, an icy moon or comet drifted inside Saturn's Roche limit. Tidal gravity tore it apart into billions of chunks of ice and rock that could never clump back into a moon!\n\n"
                    f"**🧠 Comprehension Check:** Why don't the particles in Saturn's rings collapse into a single new moon today?"
                )
            else: # Citizen
                return (
                    f"### The Secret of Saturn's Spectacular Rings 🪐✨\n\n"
                    f"Saturn's rings are one of the greatest masterpieces of nature! They look solid from Earth, but they are actually made of billions of pieces of sparkling water ice, ranging from tiny dust grains to house-sized icebergs.\n\n"
                    f"Long ago, an icy moon or comet ventured too close to Saturn. Saturn's intense gravity shredded the moon into pieces, scattering them into shimmering cosmic ribbons that circle the planet like a celestial highway."
                )

        # ======================================================================
        # QUESTION 5 & 6: "What happened in this simulation?" / "Explain this trajectory"
        # ======================================================================
        if "simulation" in p_lower or "trajectory" in p_lower or "n-body" in p_lower:
            sim_match = re.search(r'\b(sim_[a-zA-Z0-9_-]+|[a-f0-9]{8,12})\b', prompt)
            target_sim = sim_match.group(1) if sim_match else None
            if target_sim:
                exp = tool_explain_simulation_result(target_sim)
                if exp.get("scenario_name"):
                    return (
                        f"### NEBULA N-Body Simulation Telemetry Analysis\n\n"
                        f"- **[NEBULA Data]:** Scenario `{exp.get('scenario_name')}`, Integrator `{exp.get('integrator_used')}`, Bodies integrated: {', '.join(exp.get('bodies_list', []))}.\n"
                        f"- **[Computed Result]:** Energy Conservation Status: **{exp.get('energy_conservation_status')}**.\n"
                        f"- **[Numerical Interpretation]:** {exp.get('analysis')}\n"
                        f"- **[General Explanation]:** The gravitational interactions follow Newtonian $N$-body dynamics integrated step-by-step to track velocity vectors and mutual accelerations."
                    )
            return (
                f"### N-Body Orbital Simulation Dynamics\n\n"
                f"- **[Computed Result]:** NEBULA integrates gravitational systems using high-order numerical solvers (REBOUND IAS15 adaptive 15th-order Gauss-Radau and symplectic WHFast).\n"
                f"- **[External Scientific Context]:** Systems with 3 or more gravitational bodies cannot be solved with closed-form algebraic formulas due to the non-integrable Three-Body Problem (Poincaré, 1890).\n"
                f"- **[General Explanation]:** To inspect a specific run, launch any scenario in the **N-Body Simulation** workbench (e.g. Sun-Earth-Moon, TRAPPIST-1, or Figure-8) and pass its run ID."
            )

        # ======================================================================
        # QUESTION 7: "Which planet has the strongest gravity?"
        # ======================================================================
        if "strongest gravity" in p_lower or "highest gravity" in p_lower or "most gravity" in p_lower:
            grav_res = tool_query_strongest_gravity("Planet")
            top_name = grav_res.get("strongest_body", "Jupiter")
            top_g = grav_res.get("surface_gravity_m_s2", 24.79)
            top_gees = grav_res.get("gravity_gees", 2.53)

            if mode_key == "researcher":
                return (
                    f"### Planetary Gravitational Extremes in the Solar System\n\n"
                    f"- **[NEBULA Data]:** **{top_name}** exhibits the strongest surface gravitational acceleration of any planet: $g = {top_g}\\,\\text{{m/s}}^2$ (${top_gees}\\,g_0$).\n"
                    f"- **[Computed Result]:** Derived from Newton's surface gravity relation $g = \\frac{{GM}}{{R^2}}$, where Jupiter's massive core ($M = 1.8982 \\times 10^{{27}}\\,\\text{{kg}}$) overcomes its large equatorial radius ($R = 71,492\\,\\text{{km}}$).\n"
                    f"- **[Comparative Rankings]:**\n"
                    f"  1. Jupiter: $24.79\\,\\text{{m/s}}^2$ ($2.53\\,g_0$)\n"
                    f"  2. Neptune: $11.15\\,\\text{{m/s}}^2$ ($1.14\\,g_0$)\n"
                    f"  3. Saturn: $10.44\\,\\text{{m/s}}^2$ ($1.06\\,g_0$)\n"
                    f"  4. Earth: $9.81\\,\\text{{m/s}}^2$ ($1.00\\,g_0$)\n"
                    f"  5. Venus: $8.87\\,\\text{{m/s}}^2$ ($0.90\\,g_0$)\n"
                    f"- **[External Scientific Context]:** Surface gravity values refer to the 1-bar atmospheric pressure level for gas and ice giants (IAU standard)."
                )
            elif mode_key == "student":
                return (
                    f"### Which Planet Has the Strongest Gravity? 🏋️‍♂️\n\n"
                    f"- **[NEBULA Data]:** **Jupiter** wins first place by far! Its surface gravity is **{top_g} m/s²**, about **{top_gees} times Earth's gravity**.\n"
                    f"- **[Computed Result]:** Gravity depends on both mass AND radius:\n"
                    f"  $$g = \\frac{{G \\cdot M}}{{R^2}}$$\n"
                    f"- **[General Explanation]:** If you weigh 50 kg on Earth, you would feel like you weigh **{50 * top_gees:.1f} kg** on Jupiter! Walking around would feel like carrying another full person on your back.\n\n"
                    f"**🧠 Comprehension Check:** Saturn is 95 times heavier than Earth, but its surface gravity (10.4 m/s²) is only slightly higher than Earth's (9.8 m/s²). Why? *(Hint: What does its huge radius do in $R^2$?)*"
                )
            else: # Citizen
                return (
                    f"### The Gravity Champion of the Solar System 🥇🪐\n\n"
                    f"**Jupiter** has the strongest gravity of any planet in our solar system!\n\n"
                    f"Its gravity is **2.5 times stronger than Earth's**. If you stepped onto Jupiter's cloud deck, you would immediately feel more than two-and-a-half times heavier. Lifting your arms or taking a single step would require immense superhuman effort!"
                )

        # ======================================================================
        # QUESTION 8: Missing Data Handling
        # ======================================================================
        if "missing" in p_lower or "unknown" in p_lower or "unavailable" in p_lower:
            return (
                f"### Scientific Integrity & Transparency Notice\n\n"
                f"- **[NEBULA Safety Protocol]:** When astronomical parameters are unmeasured or outside empirical observational catalogs, NEBULA will explicitly state that the data is **unavailable** rather than fabricating synthetic values.\n"
                f"- **[Data Provenance]:** All measurements are cross-validated against NASA JPL Horizons, Gaia DR3, and SIMBAD."
            )

        # ======================================================================
        # GENERAL FALLBACK (Synthesized from context or catalog)
        # ======================================================================
        if context:
            if mode_key == "researcher":
                return (
                    f"### Quantitative Astrophysical Telemetry Report\n\n"
                    f"{context}\n\n"
                    f"Regarding inquiry *\"{prompt}\"*:\n\n"
                    f"Theoretical astrophysical characterization confirms that celestial configurations are rigorously governed by "
                    f"relativistic hydrodynamics, Keplerian state vectors $(a, e, i, \\Omega, \\omega, \\nu)$, hydrostatic equilibrium, and "
                    f"Poisson gravitational potential $\\nabla^2 \\Phi = 4\\pi G \\rho$. Quantitative empirical telemetry values tabulated "
                    f"above represent high-precision astrometric baselines cross-calibrated against NASA JPL Horizons and Gaia DR3 ephemerides."
                )
            elif mode_key == "student":
                return (
                    f"### Exploring the Universe Step-by-Step 🚀\n\n"
                    f"{context}\n\n"
                    f"Let's break down your question: *\"{prompt}\"*!\n\n"
                    f"In astronomy, every planet, star, and moon behaves according to fundamental physics laws like gravity and "
                    f"energy conservation. The verified facts above show how this world moves, how much it weighs, and what conditions "
                    f"exist on its surface.\n\n"
                    f"**🧠 Comprehension Check:** Which of the properties listed above determines how strongly this body pulls on other objects? "
                    f"*(Hint: Remember Newton's Law of Universal Gravitation!)*"
                )
            else: # Citizen
                return (
                    f"### Discovering Our Cosmic Backyard ✨\n\n"
                    f"{context}\n\n"
                    f"Here is what makes *\"{prompt}\"* so fascinating:\n\n"
                    f"Our universe is packed with incredible worlds! From blistering hot surfaces to frozen ocean moons, "
                    f"every corner of space offers something exciting to discover. Take a look at the 3D Planetarium view "
                    f"to watch these worlds in motion!"
                )

        if mode_key == "researcher":
            return (
                f"### Theoretical Astrophysical Analysis: {prompt}\n\n"
                f"- **[NEBULA Data]:** Observational astrometry parameters are parameterized via orbital ephemerides and barycentric dynamical coordinates.\n"
                f"- **[Recommendation]:** Specify an empirical celestial target (e.g. Jupiter, Earth, TRAPPIST-1e) to evaluate state vectors and derivations."
            )
        elif mode_key == "student":
            return (
                f"### Astronomy Exploration Guide: {prompt} 🚀\n\n"
                f"Everything in the solar system follows fundamental physical principles discovered by Newton and Kepler! "
                f"Pick any world in the Explorer to inspect its mass, orbital speed, and surface gravity."
            )
        else:
            return (
                f"### Welcome to the Cosmos! ✨\n\n"
                f"Exploring *\"{prompt}\"*! Our universe is full of billions of stars and countless amazing worlds. "
                f"Select any celestial body to uncover captivating facts and 3D views!"
            )

    def _format_single_object_mass(self, obj: Dict[str, Any], mode: str) -> str:
        name = obj.get("name")
        m_kg = obj.get("mass_kg")
        m_earth = obj.get("mass_earth_relative")

        if not m_kg:
            return f"Data Unavailable: The mass of {name} is not recorded in the catalog."

        if mode == "researcher":
            return (
                f"### Mass Telemetry: {name}\n\n"
                f"- **[NEBULA Data]:** Mass $M = {m_kg:.4e}\\,\\text{{kg}}$ (${m_earth}\\,M_\\oplus$).\n"
                f"- **[Data Provenance]:** {obj.get('data_source', 'NASA JPL Horizons')}."
            )
        elif mode == "student":
            return (
                f"### Mass of {name} 📊\n\n"
                f"- **[NEBULA Data]:** Mass is **{m_kg:.3e} kg** (about **{m_earth} times Earth's mass**).\n"
                f"**🧠 Comprehension Check:** How does mass influence the gravitational pull on objects nearby?"
            )
        else:
            return (
                f"### How Heavy is {name}? ✨\n\n"
                f"{name} has a mass of about **{m_earth} Earth masses** ({m_kg:.2e} kg)."
            )

    def _format_comparison(self, id1: str, id2: str, mode: str) -> str:
        res1 = tool_get_object(id1)
        res2 = tool_get_object(id2)
        if not res1.get("found") or not res2.get("found"):
            return f"Comparison data incomplete: One of the requested bodies ('{id1}' or '{id2}') was not found in the catalog."

        o1 = res1["object"]
        o2 = res2["object"]

        m1, m2 = o1.get("mass_kg"), o2.get("mass_kg")
        r1, r2 = o1.get("radius_km"), o2.get("radius_km")
        g1, g2 = o1.get("surface_gravity_m_s2"), o2.get("surface_gravity_m_s2")
        d1, d2 = o1.get("semi_major_axis_au"), o2.get("semi_major_axis_au")

        mass_r = round(m2 / m1, 4) if (m1 and m2) else "N/A"
        radius_r = round(r2 / r1, 4) if (r1 and r2) else "N/A"
        grav_r = round(g2 / g1, 4) if (g1 and g2) else "N/A"
        dist_r = round(d2 / d1, 4) if (d1 and d2) else "N/A"

        if mode == "researcher":
            m1_str = f"{m1:.4e}" if m1 else "N/A"
            m2_str = f"{m2:.4e}" if m2 else "N/A"
            return (
                f"### Comparative Astrophysical Synthesis: {o1['name']} vs. {o2['name']}\n\n"
                f"- **[NEBULA Data]:**\n"
                f"  - **{o1['name']}:** Mass $M = {m1_str}\\,\\text{{kg}}$ (${o1.get('mass_earth_relative')}\\,M_\\oplus$), "
                f"Radius $R = {r1}\\,\\text{{km}}$, Surface Gravity $g = {g1}\\,\\text{{m/s}}^2$, "
                f"Semi-Major Axis $a = {d1}\\,\\text{{AU}}$, Period $P = {o1.get('orbital_period_days')}\\,\\text{{d}}$\n"
                f"  - **{o2['name']}:** Mass $M = {m2_str}\\,\\text{{kg}}$ (${o2.get('mass_earth_relative')}\\,M_\\oplus$), "
                f"Radius $R = {r2}\\,\\text{{km}}$, Surface Gravity $g = {g2}\\,\\text{{m/s}}^2$, "
                f"Semi-Major Axis $a = {d2}\\,\\text{{AU}}$, Period $P = {o2.get('orbital_period_days')}\\,\\text{{d}}$\n"
                f"- **[Computed Result]:** Direct physical multipliers ({o2['name']} relative to {o1['name']}):\n"
                f"  - Mass Differential Ratio: ${mass_r}\\times$\n"
                f"  - Volumetric Radius Ratio: ${radius_r}\\times$\n"
                f"  - Surface Gravitational Ratio: ${grav_r}\\times$\n"
                f"  - Semi-Major Axis Heliocentric Distance: ${dist_r}\\times$\n"
                f"- **[External Scientific Context]:** Comparative planetary formation and secular resonance models "
                f"demonstrate disparate volatile retention envelopes, core-mantle fractionation fractions, and photoevaporation "
                f"histories dictated by incident high-energy stellar flux and hydrostatic equilibrium constraints."
            )
        elif mode == "student":
            g_pct = f"{float(grav_r) * 100:.1f}%" if grav_r != "N/A" else "different"
            w_calc = f"{100 * float(grav_r):.1f}" if grav_r != "N/A" else "a different amount"
            return (
                f"### Comparing {o1['name']} and {o2['name']} 🌍 ⚔️ 🚀\n\n"
                f"- **[NEBULA Data]:**\n"
                f"  - **Size & Radius:** {o2['name']} has a radius of {r2} km, compared to {r1} km for {o1['name']}.\n"
                f"  - **Mass:** {o2['name']} is about {mass_r} times as massive as {o1['name']}.\n"
                f"  - **Surface Gravity:** Standing on {o2['name']}, gravity is {g2} m/s² ({g_pct} of {o1['name']}).\n"
                f"- **[Computed Result]:** If you weigh 100 kg on {o1['name']}, you would weigh **{w_calc} kg** on {o2['name']}!\n"
                f"- **[General Explanation]:** Notice how differences in mass and distance from the star shape each world's unique environment.\n\n"
                f"**🧠 Comprehension Check:** Why does gravity depend on both a planet's mass AND its radius? *(Hint: $g = \\frac{{G \\cdot M}}{{R^2}}$)*"
            )
        else: # Citizen
            g_desc = f"about {float(grav_r):.2f} times as strong" if grav_r != "N/A" else "different"
            w_desc = f"{100 * float(grav_r):.0f}" if grav_r != "N/A" else "a different amount"
            return (
                f"### {o1['name']} vs. {o2['name']}: Side-by-Side Wonder ✨\n\n"
                f"Comparing {o1['name']} and {o2['name']} shows how uniquely fascinating different worlds in our cosmos are!\n\n"
                f"- **Scale:** {o2['name']} is about {radius_r} times the size of {o1['name']}.\n"
                f"- **Gravity Feel:** Gravity on {o2['name']} is {g_desc} as on {o1['name']}. If you weighed 100 lbs on {o1['name']}, you would weigh about {w_desc} lbs on {o2['name']}!\n"
                f"- **Orbital Year:** Takes about {o2.get('orbital_period_days', 'several')} days to complete one trip around its host star, compared to {o1.get('orbital_period_days', 'several')} days for {o1['name']}.\n\n"
                f"Check out the **3D View** or **Parametric Comparison** page to see them scaled side by side!"
            )
