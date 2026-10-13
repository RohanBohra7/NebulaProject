"""
Tool Registry and Execution Engine for NEBULA Grounded AI.
Provides typed, validated tools that interface directly with NEBULA's
astronomical catalog, scientific calculation engine, and N-body simulation solver.
"""
from typing import Dict, Any, List, Optional, Callable
import math
import logging
from app.db.database import SessionLocal
from app.data.catalog import get_all_objects, get_object_by_id
from app.data.seed_data import ASTRONOMICAL_CATALOG
from app.scientific import (
    calculate_gravitational_force,
    calculate_circular_velocity,
    calculate_orbital_period,
    calculate_escape_velocity,
    calculate_hohmann_transfer,
    calculate_hill_sphere,
    calculate_roche_limit,
    find_orbital_resonances
)
from app.simulation.manager import simulation_manager

logger = logging.getLogger(__name__)


class ToolDefinition:
    def __init__(
        self,
        name: str,
        description: str,
        parameters: Dict[str, Any],
        func: Callable,
        category: str = "general"
    ):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.func = func
        self.category = category

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
            "category": self.category
        }


class ToolRegistry:
    """
    Central registry for AI tools/functions.
    Enforces that the AI retrieves verifiable empirical data and calculated
    results rather than inventing or hallucinating values.
    """
    def __init__(self):
        self._tools: Dict[str, ToolDefinition] = {}
        self._register_default_tools()

    def register(
        self,
        name: str,
        description: str,
        parameters: Dict[str, Any],
        func: Callable,
        category: str = "general"
    ):
        self._tools[name] = ToolDefinition(
            name=name,
            description=description,
            parameters=parameters,
            func=func,
            category=category
        )

    def get_tool(self, name: str) -> Optional[ToolDefinition]:
        return self._tools.get(name)

    def list_tools(self) -> List[Dict[str, Any]]:
        return [t.to_dict() for t in self._tools.values()]

    async def execute(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        tool = self.get_tool(name)
        if not tool:
            return {
                "status": "error",
                "message": f"Tool '{name}' is not registered in ToolRegistry.",
                "tool_name": name
            }
        try:
            res = tool.func(**arguments)
            if hasattr(res, "__await__"):
                res = await res
            return {
                "status": "success",
                "tool_name": name,
                "result": res
            }
        except Exception as e:
            logger.exception(f"Error executing tool {name} with args {arguments}: {e}")
            return {
                "status": "error",
                "tool_name": name,
                "message": str(e)
            }

    def _register_default_tools(self):
        # 1. get_object
        self.register(
            name="get_object",
            description="Retrieves the complete empirical record for a celestial object by ID or name.",
            parameters={
                "type": "object",
                "properties": {
                    "object_id": {
                        "type": "string",
                        "description": "Unique identifier of the celestial object (e.g. 'jupiter', 'earth', 'mars', 'sun')"
                    }
                },
                "required": ["object_id"]
            },
            func=tool_get_object,
            category="catalog"
        )

        # 2. search_objects
        self.register(
            name="search_objects",
            description="Searches the NEBULA catalog by keyword, name, or celestial category.",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search term (e.g. 'ring', 'habitable', 'giant', 'ice')"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 5)"
                    }
                },
                "required": ["query"]
            },
            func=tool_search_objects,
            category="catalog"
        )

        # 3. compare_objects
        self.register(
            name="compare_objects",
            description="Computes a parametric comparison matrix, physical ratios, and deltas between 2 to 6 celestial objects.",
            parameters={
                "type": "object",
                "properties": {
                    "object_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of 2 to 6 celestial object IDs (e.g. ['earth', 'mars'])"
                    }
                },
                "required": ["object_ids"]
            },
            func=tool_compare_objects,
            category="comparison"
        )

        # 4. get_object_properties
        self.register(
            name="get_object_properties",
            description="Extracts specific empirical properties for a celestial object. Explicitly notes if requested properties are unavailable.",
            parameters={
                "type": "object",
                "properties": {
                    "object_id": {
                        "type": "string",
                        "description": "ID of the target object"
                    },
                    "properties": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Property names to retrieve (e.g. ['mass_kg', 'radius_km', 'surface_gravity_m_s2'])"
                    }
                },
                "required": ["object_id", "properties"]
            },
            func=tool_get_object_properties,
            category="catalog"
        )

        # 5. calculate_orbital_property
        self.register(
            name="calculate_orbital_property",
            description="Executes rigorous astronomical equations (gravity force, orbital velocity, orbital period, escape velocity, Hohmann transfer, Hill sphere, Roche limit).",
            parameters={
                "type": "object",
                "properties": {
                    "property_name": {
                        "type": "string",
                        "enum": [
                            "gravitational_force",
                            "orbital_velocity",
                            "orbital_period",
                            "escape_velocity",
                            "hohmann_transfer",
                            "hill_sphere",
                            "roche_limit"
                        ],
                        "description": "The scientific calculation to perform"
                    },
                    "params": {
                        "type": "object",
                        "description": "Key-value parameters required for the chosen calculation"
                    }
                },
                "required": ["property_name", "params"]
            },
            func=tool_calculate_orbital_property,
            category="scientific"
        )

        # 6. get_simulation
        self.register(
            name="get_simulation",
            description="Retrieves metadata, status, parameters, and scenario definition for an N-body simulation run.",
            parameters={
                "type": "object",
                "properties": {
                    "simulation_id": {
                        "type": "string",
                        "description": "Simulation run ID"
                    }
                },
                "required": ["simulation_id"]
            },
            func=tool_get_simulation,
            category="simulation"
        )

        # 7. get_simulation_results
        self.register(
            name="get_simulation_results",
            description="Retrieves the numerical results of an N-body simulation including energy error, conservation metrics, and trajectories.",
            parameters={
                "type": "object",
                "properties": {
                    "simulation_id": {
                        "type": "string",
                        "description": "Simulation run ID"
                    }
                },
                "required": ["simulation_id"]
            },
            func=tool_get_simulation_results,
            category="simulation"
        )

        # 8. explain_simulation_result
        self.register(
            name="explain_simulation_result",
            description="Analyzes and explains the numerical stability, energy conservation, and dynamical physics of an N-body simulation.",
            parameters={
                "type": "object",
                "properties": {
                    "simulation_id": {
                        "type": "string",
                        "description": "Simulation run ID"
                    }
                },
                "required": ["simulation_id"]
            },
            func=tool_explain_simulation_result,
            category="simulation"
        )

        # 9. query_strongest_gravity
        self.register(
            name="query_strongest_gravity",
            description="Queries the NEBULA catalog to identify the body with the highest surface gravity, ranking candidates.",
            parameters={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Optional category filter (e.g. 'Planet', 'Star', or 'All')"
                    }
                }
            },
            func=tool_query_strongest_gravity,
            category="catalog"
        )


# ==============================================================================
# TOOL FUNCTION IMPLEMENTATIONS
# ==============================================================================

def _normalize_id(oid: str) -> str:
    cleaned = oid.strip().lower()
    # Map common aliases
    alias_map = {
        "jupiter": "jupiter",
        "earth": "earth",
        "mars": "mars",
        "venus": "venus",
        "mercury": "mercury",
        "saturn": "saturn",
        "uranus": "uranus",
        "neptune": "neptune",
        "sun": "sun",
        "moon": "moon",
        "trappist-1e": "trappist-1e",
        "trappist 1e": "trappist-1e",
        "trappist": "trappist-1e",
        "proxima b": "proxima_centauri_b",
        "proxima centauri b": "proxima_centauri_b",
        "europa": "europa",
        "titan": "titan",
        "ganymede": "ganymede",
        "betelgeuse": "betelgeuse",
        "sirius": "sirius_a",
        "sirius a": "sirius_a",
        "ceres": "ceres",
        "halley": "halley_comet",
        "halleys comet": "halley_comet",
        "m87": "m87_black_hole",
        "m87*": "m87_black_hole",
        "sagittarius a*": "sagittarius_a_star",
        "sgr a*": "sagittarius_a_star",
    }
    return alias_map.get(cleaned, cleaned)


def tool_get_object(object_id: str) -> Dict[str, Any]:
    target_id = _normalize_id(object_id)
    # Check DB
    db = SessionLocal()
    try:
        obj = get_object_by_id(db, target_id)
    except Exception:
        obj = None
    finally:
        db.close()

    # Fallback to seed catalog if needed
    if not obj:
        for seed_obj in ASTRONOMICAL_CATALOG:
            if seed_obj["id"] == target_id or seed_obj["name"].lower() == object_id.lower():
                obj = dict(seed_obj)
                break

    if not obj:
        return {
            "found": False,
            "message": f"Celestial object '{object_id}' was not found in the NEBULA catalog.",
            "source": "NEBULA Catalog"
        }

    return {
        "found": True,
        "object": obj,
        "source": "NEBULA Catalog",
        "provenance": obj.get("data_source", "NASA / JPL Horizons / Gaia DR3")
    }


def tool_search_objects(query: str, limit: int = 5) -> Dict[str, Any]:
    q_lower = query.lower().strip()
    db = SessionLocal()
    try:
        all_objs = get_all_objects(db)
    except Exception:
        all_objs = ASTRONOMICAL_CATALOG
    finally:
        db.close()

    matches = []
    for obj in all_objs:
        score = 0
        name = obj.get("name", "").lower()
        cat = obj.get("category", "").lower()
        desc = (obj.get("description_citizen") or "").lower()
        
        if q_lower == name or q_lower == obj.get("id"):
            score += 10
        elif q_lower in name:
            score += 5
        if q_lower in cat:
            score += 3
        if q_lower in desc:
            score += 2

        if score > 0:
            matches.append((score, obj))

    matches.sort(key=lambda x: x[0], reverse=True)
    selected = [m[1] for m in matches[:limit]]

    return {
        "query": query,
        "count": len(selected),
        "results": [
            {
                "id": o.get("id"),
                "name": o.get("name"),
                "category": o.get("category"),
                "mass_earth_relative": o.get("mass_earth_relative"),
                "radius_km": o.get("radius_km"),
                "semi_major_axis_au": o.get("semi_major_axis_au")
            }
            for o in selected
        ],
        "source": "NEBULA Catalog"
    }


def tool_compare_objects(object_ids: List[str]) -> Dict[str, Any]:
    if len(object_ids) < 2:
        return {
            "error": "Comparison requires at least 2 celestial bodies.",
            "source": "NEBULA Comparison Engine"
        }

    resolved = []
    for oid in object_ids[:6]:
        res = tool_get_object(oid)
        if res.get("found"):
            resolved.append(res["object"])

    if len(resolved) < 2:
        return {
            "error": f"Could not find at least 2 valid objects from provided IDs: {object_ids}",
            "source": "NEBULA Comparison Engine"
        }

    primary = resolved[0]
    ratios = []
    for target in resolved[1:]:
        mass_r = (target.get("mass_kg") / primary.get("mass_kg")) if (target.get("mass_kg") and primary.get("mass_kg")) else None
        radius_r = (target.get("radius_km") / primary.get("radius_km")) if (target.get("radius_km") and primary.get("radius_km")) else None
        grav_r = (target.get("surface_gravity_m_s2") / primary.get("surface_gravity_m_s2")) if (target.get("surface_gravity_m_s2") and primary.get("surface_gravity_m_s2")) else None
        dist_r = (target.get("semi_major_axis_au") / primary.get("semi_major_axis_au")) if (target.get("semi_major_axis_au") and primary.get("semi_major_axis_au")) else None
        period_r = (target.get("orbital_period_days") / primary.get("orbital_period_days")) if (target.get("orbital_period_days") and primary.get("orbital_period_days")) else None

        ratios.append({
            "target": target["name"],
            "relative_to": primary["name"],
            "mass_ratio": round(mass_r, 4) if mass_r else None,
            "radius_ratio": round(radius_r, 4) if radius_r else None,
            "gravity_ratio": round(grav_r, 4) if grav_r else None,
            "distance_ratio": round(dist_r, 4) if dist_r else None,
            "period_ratio": round(period_r, 4) if period_r else None,
        })

    return {
        "primary_reference": primary["name"],
        "compared_bodies": [o["name"] for o in resolved],
        "ratios": ratios,
        "metrics_summary": [
            {
                "name": o["name"],
                "category": o.get("category"),
                "mass_earth": o.get("mass_earth_relative"),
                "radius_km": o.get("radius_km"),
                "gravity_m_s2": o.get("surface_gravity_m_s2"),
                "semi_major_axis_au": o.get("semi_major_axis_au"),
                "period_days": o.get("orbital_period_days")
            }
            for o in resolved
        ],
        "source": "NEBULA Comparison Engine"
    }


def tool_get_object_properties(object_id: str, properties: List[str]) -> Dict[str, Any]:
    obj_res = tool_get_object(object_id)
    if not obj_res.get("found"):
        return {
            "found": False,
            "object_id": object_id,
            "message": f"Celestial object '{object_id}' not found.",
            "source": "NEBULA Catalog"
        }

    obj = obj_res["object"]
    available_data = {}
    unavailable_data = []

    for prop in properties:
        val = obj.get(prop)
        if val is not None:
            available_data[prop] = val
        else:
            unavailable_data.append(prop)

    return {
        "object_id": obj["id"],
        "object_name": obj["name"],
        "available_properties": available_data,
        "unavailable_properties": unavailable_data,
        "source": "NEBULA Catalog",
        "provenance": obj.get("data_source", "NASA JPL")
    }


def tool_calculate_orbital_property(property_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    try:
        if property_name == "gravitational_force":
            m1 = float(params.get("m1_kg") or params.get("mass1", 5.972e24))
            m2 = float(params.get("m2_kg") or params.get("mass2", 1.989e30))
            r = float(params.get("distance_m") or params.get("distance", 1.496e11))
            res = calculate_gravitational_force(m1, m2, r)
            return {
                "calculation": "Newtonian Universal Gravitation Force",
                "formula": "F = G * (m1 * m2) / r^2",
                "result": res,
                "source": "NEBULA Scientific Engine (Astropy-verified)"
            }

        elif property_name == "orbital_velocity":
            m_central = float(params.get("central_mass_kg") or params.get("mass", 1.989e30))
            r = float(params.get("semi_major_axis_m") or params.get("radius_m") or params.get("distance_m", 1.496e11))
            res = calculate_circular_velocity(m_central, r)
            return {
                "calculation": "Circular Orbital Velocity",
                "formula": "v_circ = sqrt(G * M / r)",
                "result": res,
                "source": "NEBULA Scientific Engine"
            }

        elif property_name == "orbital_period":
            a = float(params.get("semi_major_axis_m") or params.get("distance_m", 1.496e11))
            m_central = float(params.get("central_mass_kg") or params.get("mass", 1.989e30))
            res = calculate_orbital_period(a, m_central)
            return {
                "calculation": "Keplerian Orbital Period",
                "formula": "T = 2 * pi * sqrt(a^3 / (G * M))",
                "result": res,
                "source": "NEBULA Scientific Engine"
            }

        elif property_name == "escape_velocity":
            m = float(params.get("mass_kg", 5.972e24))
            r = float(params.get("radius_m", 6.371e6))
            res = calculate_escape_velocity(m, r)
            return {
                "calculation": "Escape Velocity",
                "formula": "v_esc = sqrt(2 * G * M / R)",
                "result": res,
                "source": "NEBULA Scientific Engine"
            }

        elif property_name == "hohmann_transfer":
            r1_au = float(params.get("r1_au", 1.0))
            r2_au = float(params.get("r2_au", 1.524))
            res = calculate_hohmann_transfer(r1_au, r2_au)
            return {
                "calculation": "Hohmann Transfer Trajectory",
                "result": res,
                "source": "NEBULA Orbital Mechanics Engine"
            }

        elif property_name == "hill_sphere":
            a_au = float(params.get("semi_major_axis_au", 1.0))
            e = float(params.get("eccentricity", 0.0167))
            m_body = float(params.get("body_mass_kg", 5.972e24))
            m_star = float(params.get("star_mass_kg", 1.989e30))
            res = calculate_hill_sphere(a_au, e, m_body, m_star)
            return {
                "calculation": "Hill Sphere Gravitational Dominance Radius",
                "formula": "r_H = a * (1 - e) * (m / (3 * M))^(1/3)",
                "result": res,
                "source": "NEBULA Scientific Engine"
            }

        elif property_name == "roche_limit":
            r_prim = float(params.get("primary_radius_km", 58232.0))
            rho_prim = float(params.get("primary_density_g_cm3", 0.687))
            rho_sat = float(params.get("satellite_density_g_cm3", 1.0))
            is_fluid = bool(params.get("is_fluid", True))
            res = calculate_roche_limit(r_prim, rho_prim, rho_sat, is_fluid)
            return {
                "calculation": "Roche Tidal Disruption Limit",
                "formula": "d = C * R_M * (rho_M / rho_m)^(1/3)",
                "result": res,
                "source": "NEBULA Scientific Engine"
            }

        else:
            return {
                "error": f"Unknown orbital property calculation: '{property_name}'",
                "supported": [
                    "gravitational_force",
                    "orbital_velocity",
                    "orbital_period",
                    "escape_velocity",
                    "hohmann_transfer",
                    "hill_sphere",
                    "roche_limit"
                ]
            }
    except Exception as e:
        return {"error": f"Calculation failed: {str(e)}"}


def tool_get_simulation(simulation_id: str) -> Dict[str, Any]:
    record = simulation_manager.get_simulation(simulation_id)
    if not record:
        return {
            "found": False,
            "simulation_id": simulation_id,
            "message": f"Simulation job '{simulation_id}' not found.",
            "source": "NEBULA N-Body Solver"
        }
    return {
        "found": True,
        "simulation": record,
        "source": "NEBULA N-Body Solver"
    }


def tool_get_simulation_results(simulation_id: str) -> Dict[str, Any]:
    results = simulation_manager.get_simulation_results(simulation_id)
    if not results:
        record = simulation_manager.get_simulation(simulation_id)
        status_msg = record.get("status") if record else "not found"
        return {
            "found": False,
            "simulation_id": simulation_id,
            "message": f"Simulation results not available (current status: {status_msg}).",
            "source": "NEBULA N-Body Solver"
        }

    return {
        "found": True,
        "simulation_id": simulation_id,
        "scenario": results.get("scenario_name"),
        "integrator": results.get("integrator"),
        "total_time_years": results.get("total_time_years"),
        "num_steps": results.get("num_steps"),
        "conservation_metrics": results.get("conservation_metrics", {}),
        "bodies": [b.get("name") for b in results.get("bodies", [])],
        "energy_error": results.get("conservation_metrics", {}).get("relative_energy_error"),
        "source": "NEBULA N-Body Numerical Engine"
    }


def tool_explain_simulation_result(simulation_id: str) -> Dict[str, Any]:
    res = tool_get_simulation_results(simulation_id)
    if not res.get("found"):
        return res

    scenario = res.get("scenario", "Custom N-body run")
    integrator = res.get("integrator", "IAS15")
    energy_err = res.get("energy_error")
    bodies = res.get("bodies", [])

    is_stable = True
    stability_notes = []

    if energy_err is not None:
        if abs(energy_err) < 1e-6:
            stability_notes.append(
                f"High-fidelity energy conservation (relative energy error ΔE/E0 = {energy_err:.2e}), indicating numerical stability."
            )
        elif abs(energy_err) < 1e-3:
            stability_notes.append(
                f"Acceptable energy conservation for medium-duration integration (ΔE/E0 = {energy_err:.2e})."
            )
        else:
            is_stable = False
            stability_notes.append(
                f"Elevated numerical energy divergence (ΔE/E0 = {energy_err:.2e}); consider decreasing timestep."
            )

    explanation = {
        "scenario_name": scenario,
        "integrator_used": integrator,
        "particles_integrated": len(bodies),
        "bodies_list": bodies,
        "energy_conservation_status": "Strictly Conserved" if is_stable else "Divergence Warning",
        "analysis": " ".join(stability_notes),
        "source": "NEBULA N-Body Scientific Interpreter"
    }
    return explanation


def tool_query_strongest_gravity(category: Optional[str] = "Planet") -> Dict[str, Any]:
    db = SessionLocal()
    try:
        objs = get_all_objects(db)
    except Exception:
        objs = ASTRONOMICAL_CATALOG
    finally:
        db.close()

    cat_filter = category.lower() if (category and category.lower() != "all") else None
    ranked = []
    for o in objs:
        if cat_filter and o.get("category", "").lower() != cat_filter:
            continue
        g = o.get("surface_gravity_m_s2")
        if g is not None:
            ranked.append((g, o))

    ranked.sort(key=lambda x: x[0], reverse=True)
    if not ranked:
        return {
            "found": False,
            "message": f"No celestial bodies with recorded surface gravity found in category '{category}'."
        }

    top_g, top_obj = ranked[0]
    comparison_summary = [
        {
            "rank": idx + 1,
            "name": obj["name"],
            "category": obj.get("category"),
            "surface_gravity_m_s2": g,
            "gravity_gees": round(g / 9.80665, 2)
        }
        for idx, (g, obj) in enumerate(ranked[:5])
    ]

    return {
        "strongest_body": top_obj["name"],
        "category": top_obj.get("category"),
        "surface_gravity_m_s2": top_g,
        "gravity_gees": round(top_g / 9.80665, 2),
        "earth_relative_gravity": f"{round(top_g / 9.80665, 2)}x Earth gravity",
        "top_rankings": comparison_summary,
        "source": "NEBULA Empirical Catalog"
    }


# Global tool registry singleton
tool_registry = ToolRegistry()
