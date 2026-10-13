"""
Conservation laws and stability metrics for N-body gravitational simulations.
Calculates Hamiltonian total mechanical energy E = T + V,
Angular Momentum vector L, Center of Mass, and relative energy drift.
"""
import numpy as np
from typing import Dict, Any, List, Tuple


def compute_kinetic_energy(velocities: np.ndarray, masses: np.ndarray) -> float:
    """
    Computes total kinetic energy:
    T = 0.5 * sum_i (m_i * ||v_i||^2)
    """
    speeds_sq = np.sum(velocities ** 2, axis=1)
    return float(0.5 * np.sum(masses * speeds_sq))


def compute_potential_energy(positions: np.ndarray, masses: np.ndarray, G_const: float = 1.0) -> float:
    """
    Computes total gravitational potential energy:
    V = - sum_{i < j} (G * m_i * m_j / ||r_i - r_j||)
    """
    potential = 0.0
    n = len(masses)
    for i in range(n):
        for j in range(i + 1, n):
            r = float(np.linalg.norm(positions[i] - positions[j]))
            if r > 1e-12:
                potential -= G_const * masses[i] * masses[j] / r
    return float(potential)


def compute_total_energy(
    positions: np.ndarray,
    velocities: np.ndarray,
    masses: np.ndarray,
    G_const: float = 1.0
) -> float:
    """
    Computes total Hamiltonian mechanical energy E = T + V.
    """
    t = compute_kinetic_energy(velocities, masses)
    v = compute_potential_energy(positions, masses, G_const)
    return float(t + v)


def compute_angular_momentum(
    positions: np.ndarray,
    velocities: np.ndarray,
    masses: np.ndarray
) -> np.ndarray:
    """
    Computes total angular momentum vector:
    L = sum_i (m_i * (r_i x v_i))
    """
    l_vec = np.zeros(3, dtype=np.float64)
    for i in range(len(masses)):
        l_vec += masses[i] * np.cross(positions[i], velocities[i])
    return l_vec


def compute_center_of_mass(
    positions: np.ndarray,
    masses: np.ndarray
) -> Tuple[np.ndarray, float]:
    """
    Computes center of mass coordinate R_cm and total mass M_total.
    """
    m_total = float(np.sum(masses))
    if m_total <= 0:
        return np.zeros(3), 0.0
    r_cm = np.sum(positions * masses[:, np.newaxis], axis=0) / m_total
    return r_cm, m_total


def compute_energy_drift(initial_energy: float, current_energy: float) -> float:
    """
    Computes relative energy error: Delta E / |E_0|.
    Returns 0.0 if initial energy is approximately zero.
    """
    if abs(initial_energy) < 1e-14:
        return 0.0
    return float(abs(current_energy - initial_energy) / abs(initial_energy))
