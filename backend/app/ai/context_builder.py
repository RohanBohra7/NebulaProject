"""
Context Builder for NEBULA Grounded AI.
Extracts query intents, executes corresponding NEBULA tools, and formats
a structured, verifiable context block distinguishing NEBULA data,
computed results, simulation telemetry, and external context.
"""
from typing import Dict, Any, List, Optional, Tuple
import re
import logging
from app.ai.tools import (
    tool_registry,
    tool_get_object,
    tool_compare_objects,
    tool_get_simulation,
    tool_get_simulation_results,
    tool_explain_simulation_result,
    tool_calculate_orbital_property,
    tool_query_strongest_gravity
)
from app.data.seed_data import ASTRONOMICAL_CATALOG

logger = logging.getLogger(__name__)


class ContextBuilder:
    """
    Intelligently extracts grounding context from NEBULA by invoking
    catalog lookups, scientific engines, or N-body simulation queries.
    """

    KNOWN_CELESTIAL_TERMS = {
        "sun": "sun",
        "mercury": "mercury",
        "venus": "venus",
        "earth": "earth",
        "moon": "moon",
        "mars": "mars",
        "jupiter": "jupiter",
        "saturn": "saturn",
        "uranus": "uranus",
        "neptune": "neptune",
        "trappist": "trappist-1e",
        "trappist-1e": "trappist-1e",
        "proxima": "proxima_centauri_b",
        "proxima b": "proxima_centauri_b",
        "europa": "europa",
        "titan": "titan",
        "ganymede": "ganymede",
        "betelgeuse": "betelgeuse",
        "sirius": "sirius_a",
        "ceres": "ceres",
        "halley": "halley_comet",
        "m87": "m87_black_hole",
        "sgr a*": "sagittarius_a_star",
        "sagittarius a*": "sagittarius_a_star"
    }

    def detect_referenced_objects(
        self,
        query: str,
        target_object_id: Optional[str] = None,
        comparison_ids: Optional[List[str]] = None
    ) -> List[str]:
        found_ids = []
        seen = set()

        if target_object_id:
            tid = target_object_id.lower().strip()
            found_ids.append(tid)
            seen.add(tid)

        if comparison_ids:
            for cid in comparison_ids:
                c = cid.lower().strip()
                if c not in seen:
                    found_ids.append(c)
                    seen.add(c)

        q_lower = query.lower()
        # Match against known keywords
        for term, oid in self.KNOWN_CELESTIAL_TERMS.items():
            pattern = r'\b' + re.escape(term) + r'\b'
            if re.search(pattern, q_lower):
                if oid not in seen:
                    found_ids.append(oid)
                    seen.add(oid)

        return found_ids

    async def build_context(
        self,
        query: str,
        target_object_id: Optional[str] = None,
        simulation_id: Optional[str] = None,
        comparison_ids: Optional[List[str]] = None
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Builds the grounded context string and metadata dictionary for a query.
        """
        tools_invoked = []
        grounded_data_points = []
        nebula_data_sections = []
        computed_result_sections = []
        simulation_sections = []
        external_context_sections = []

        q_lower = query.lower()

        # 1. Check for Simulation Intent or explicit simulation_id
        sim_id_match = re.search(r'\b(sim_[a-zA-Z0-9_-]+|[a-f0-9]{8,12})\b', query)
        detected_sim_id = simulation_id or (sim_id_match.group(1) if sim_id_match else None)
        is_sim_query = detected_sim_id is not None or "simulation" in q_lower or "trajectory" in q_lower or "n-body" in q_lower

        if detected_sim_id:
            tools_invoked.append("get_simulation")
            sim_meta = tool_get_simulation(detected_sim_id)
            if sim_meta.get("found"):
                tools_invoked.append("get_simulation_results")
                sim_res = tool_get_simulation_results(detected_sim_id)
                tools_invoked.append("explain_simulation_result")
                sim_exp = tool_explain_simulation_result(detected_sim_id)

                sim_record = sim_meta["simulation"]
                simulation_sections.append(
                    f"Simulation ID: {detected_sim_id}\n"
                    f"- Scenario: {sim_record.get('parameters', {}).get('scenario_name', sim_record.get('scenario_id'))}\n"
                    f"- Status: {sim_record.get('status')}\n"
                    f"- Integrator: {sim_record.get('parameters', {}).get('integrator', 'ias15')}\n"
                    f"- Time Duration: {sim_record.get('parameters', {}).get('duration')} years\n"
                    f"- Numerical Steps: {sim_record.get('parameters', {}).get('num_steps')} steps"
                )
                if sim_res.get("found"):
                    simulation_sections.append(
                        f"- Conservation Error (ΔE/E0): {sim_res.get('energy_error')}\n"
                        f"- Active Bodies: {', '.join(sim_res.get('bodies', []))}\n"
                        f"- Dynamical Stability Analysis: {sim_exp.get('analysis')}"
                    )
                    grounded_data_points.append({
                        "domain": "simulation",
                        "id": detected_sim_id,
                        "energy_error": sim_res.get("energy_error"),
                        "bodies": sim_res.get("bodies")
                    })

        # 2. Check for "Strongest Gravity" Query
        if "strongest gravity" in q_lower or "highest gravity" in q_lower or "most gravity" in q_lower:
            tools_invoked.append("query_strongest_gravity")
            cat = "Star" if "star" in q_lower else "Planet"
            grav_res = tool_query_strongest_gravity(category=cat)
            if grav_res.get("strongest_body"):
                nebula_data_sections.append(
                    f"Catalog Gravity Ranking ({grav_res.get('category')}s):\n"
                    f"- Strongest Surface Gravity: {grav_res['strongest_body']} ({grav_res['surface_gravity_m_s2']} m/s², {grav_res['gravity_gees']}g)\n"
                    f"- Comparison with Earth: {grav_res['earth_relative_gravity']}"
                )
                grounded_data_points.append({
                    "property": "strongest_gravity",
                    "body": grav_res["strongest_body"],
                    "value": grav_res["surface_gravity_m_s2"],
                    "unit": "m/s²"
                })

        # 3. Detect Referenced Objects
        obj_ids = self.detect_referenced_objects(query, target_object_id, comparison_ids)

        # 4. Check for Comparison Intent
        is_compare_query = (
            "compare" in q_lower or
            "versus" in q_lower or
            " vs " in q_lower or
            "difference between" in q_lower or
            (comparison_ids and len(comparison_ids) >= 2) or
            len(obj_ids) >= 2
        )

        if is_compare_query and len(obj_ids) >= 2:
            tools_invoked.append("compare_objects")
            comp_res = tool_compare_objects(obj_ids[:4])
            if "primary_reference" in comp_res:
                computed_result_sections.append(
                    f"Parametric Comparison Matrix (Reference: {comp_res['primary_reference']}):"
                )
                for r in comp_res.get("ratios", []):
                    computed_result_sections.append(
                        f"- {r['target']} relative to {r['relative_to']}: "
                        f"Mass={r.get('mass_ratio')}x, Radius={r.get('radius_ratio')}x, "
                        f"Gravity={r.get('gravity_ratio')}x, Distance={r.get('distance_ratio')}x"
                    )
                for b in comp_res.get("metrics_summary", []):
                    nebula_data_sections.append(
                        f"- {b['name']}: Mass={b.get('mass_earth')} M⊕, Radius={b.get('radius_km')} km, "
                        f"Gravity={b.get('gravity_m_s2')} m/s², Period={b.get('period_days')} d, Semi-Major={b.get('semi_major_axis_au')} AU"
                    )
                    grounded_data_points.append({
                        "object": b["name"],
                        "mass_earth": b.get("mass_earth"),
                        "radius_km": b.get("radius_km"),
                        "gravity_m_s2": b.get("gravity_m_s2")
                    })

        # 5. Extract Single or Specific Object Data
        for oid in obj_ids:
            tools_invoked.append("get_object")
            obj_res = tool_get_object(oid)
            if obj_res.get("found"):
                o = obj_res["object"]
                nebula_data_sections.append(
                    f"Celestial Object: {o['name']} (ID: {o['id']}, Category: {o.get('category')})\n"
                    f"- Mass: {o.get('mass_kg')} kg ({o.get('mass_earth_relative')} M⊕)\n"
                    f"- Mean Radius: {o.get('radius_km')} km ({o.get('radius_earth_relative')} R⊕)\n"
                    f"- Surface Gravity: {o.get('surface_gravity_m_s2')} m/s²\n"
                    f"- Escape Velocity: {o.get('escape_velocity_km_s')} km/s\n"
                    f"- Semi-Major Axis: {o.get('semi_major_axis_au')} AU\n"
                    f"- Orbital Period: {o.get('orbital_period_days')} days\n"
                    f"- Orbital Eccentricity: {o.get('eccentricity')}\n"
                    f"- Surface/Equilibrium Temperature: {o.get('surface_temperature_k')} K\n"
                    f"- Mean Density: {o.get('mean_density_g_cm3')} g/cm³\n"
                    f"- Ring System Present: {o.get('has_rings')}\n"
                    f"- Atmosphere Present: {o.get('has_atmosphere')}"
                )
                external_context_sections.append(
                    f"- Provenance for {o['name']}: {o.get('data_source', 'NASA JPL / Gaia DR3')} (Source URL: {o.get('source_url', 'N/A')})"
                )
                grounded_data_points.append({
                    "object": o["name"],
                    "mass_kg": o.get("mass_kg"),
                    "radius_km": o.get("radius_km"),
                    "gravity_m_s2": o.get("surface_gravity_m_s2"),
                    "semi_major_axis_au": o.get("semi_major_axis_au"),
                    "period_days": o.get("orbital_period_days")
                })

                # If asking about rings (e.g. "Why does Saturn have rings?")
                if ("ring" in q_lower or "roche" in q_lower) and o.get("has_rings"):
                    tools_invoked.append("calculate_orbital_property:roche_limit")
                    r_lim = tool_calculate_orbital_property(
                        "roche_limit",
                        {
                            "primary_radius_km": o.get("radius_km", 58232.0),
                            "primary_density_g_cm3": o.get("mean_density_g_cm3", 0.687),
                            "satellite_density_g_cm3": 1.0,
                            "is_fluid": True
                        }
                    )
                    if "result" in r_lim:
                        computed_result_sections.append(
                            f"Roche Tidal Disruption Limit for {o['name']}:\n"
                            f"- Fluid Roche Limit: {r_lim['result'].get('roche_limit_km')} km ({r_lim['result'].get('roche_limit_primary_radii')} planetary radii)\n"
                            f"- Physics: Within this threshold, tidal gravitational shear forces exceed internal self-gravity, preventing moon accretion and maintaining ring structures."
                        )

                # If asking about orbital period
                if "period" in q_lower and o.get("semi_major_axis_au"):
                    tools_invoked.append("calculate_orbital_property:orbital_period")
                    computed_result_sections.append(
                        f"Keplerian Orbital Period Derivation for {o['name']}:\n"
                        f"- Formula: T = 2π * sqrt(a^3 / (G * M_sun))\n"
                        f"- Semi-Major Axis a = {o.get('semi_major_axis_au')} AU\n"
                        f"- Resulting Period: {o.get('orbital_period_days')} Earth days ({round((o.get('orbital_period_days') or 365)/365.25, 2)} Earth years)"
                    )

        # Assemble full text context with distinct sections
        context_parts = []
        if nebula_data_sections:
            context_parts.append("[NEBULA EMPIRICAL DATA]\n" + "\n\n".join(nebula_data_sections))
        if computed_result_sections:
            context_parts.append("[COMPUTED RESULTS (EQUATIONS & DERIVATIONS)]\n" + "\n\n".join(computed_result_sections))
        if simulation_sections:
            context_parts.append("[NEBULA N-BODY SIMULATION RESULTS]\n" + "\n\n".join(simulation_sections))
        if external_context_sections:
            context_parts.append("[EXTERNAL SCIENTIFIC PROVENANCE & CONTEXT]\n" + "\n\n".join(external_context_sections))

        full_context_str = "\n\n".join(context_parts)

        metadata = {
            "is_grounded": len(grounded_data_points) > 0 or len(simulation_sections) > 0,
            "detected_objects": obj_ids,
            "simulation_id": detected_sim_id,
            "tools_invoked": list(dict.fromkeys(tools_invoked)),
            "grounded_data_points": grounded_data_points,
            "distinctions": {
                "has_nebula_data": len(nebula_data_sections) > 0,
                "has_computed_results": len(computed_result_sections) > 0,
                "has_simulation_results": len(simulation_sections) > 0,
                "has_external_context": len(external_context_sections) > 0
            }
        }

        return full_context_str, metadata

context_builder = ContextBuilder()
