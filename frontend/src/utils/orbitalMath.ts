import { AstronomicalObject } from '../types/astronomy';

export interface KeplerianParams {
  semiMajorAxisAU: number;
  eccentricity: number;
  orbitalInclinationDeg: number;
  orbitalPeriodDays: number;
  meanOrbitalVelocityKmS?: number;
}

export type ScaleMode = 'enhanced' | 'scientific';

/**
 * Solves Kepler's equation M = E - e*sin(E) for Eccentric Anomaly E using Newton-Raphson iteration.
 */
export function solveKepler(meanAnomaly: number, eccentricity: number): number {
  let E = meanAnomaly;
  const e = Math.max(0, Math.min(0.99, eccentricity));
  for (let i = 0; i < 6; i++) {
    const f = E - e * Math.sin(E) - meanAnomaly;
    const fPrime = 1 - e * Math.cos(E);
    const delta = f / fPrime;
    E -= delta;
    if (Math.abs(delta) < 1e-7) break;
  }
  return E;
}

/**
 * Computes visual semi-major axis in 3D scene units based on selected scale mode.
 */
export function getVisualSemiMajorAxis(semiMajorAxisAU: number, scaleMode: ScaleMode): number {
  if (semiMajorAxisAU <= 0) return 0;

  if (scaleMode === 'enhanced') {
    // Non-linear power-law mapping: preserves orbital hierarchy while ensuring
    // Mercury is distinct from the Sun and Neptune remains comfortably in view.
    return 10.5 * Math.pow(semiMajorAxisAU, 0.52) + 3.2;
  } else {
    // Proportional / scientific mode: direct linear scaling (6 units per AU)
    return semiMajorAxisAU * 6.0;
  }
}

/**
 * Computes visual mesh radius for celestial spheres.
 */
export function getBodyVisualRadius(obj: AstronomicalObject, scaleMode: ScaleMode): number {
  if (obj.category === 'Star' || obj.id === 'sun') {
    return scaleMode === 'enhanced' ? 3.5 : 4.0;
  }

  if (obj.id === 'moon' || obj.category === 'Moon') {
    return scaleMode === 'enhanced' ? 0.25 : 0.12;
  }

  const rRel = obj.radius_earth_relative || 1.0;

  if (scaleMode === 'enhanced') {
    // Sub-linear expansion to keep terrestrial planets visible and gas giants prominent
    const base = 0.45 + 0.38 * Math.sqrt(rRel);
    return Math.max(0.35, Math.min(2.2, base));
  } else {
    // Proportional scale
    return Math.max(0.18, Math.min(2.5, rRel * 0.25));
  }
}

/**
 * Computes instantaneous position, true anomaly, distance, and velocity for a celestial body at time t (days).
 */
export function getKeplerianState(
  params: KeplerianParams,
  simulationDays: number,
  scaleMode: ScaleMode
): {
  x: number;
  y: number;
  z: number;
  trueAnomalyRad: number;
  trueAnomalyDeg: number;
  currentDistanceAU: number;
  instantaneousVelocityKmS: number;
} {
  const { semiMajorAxisAU, eccentricity, orbitalInclinationDeg, orbitalPeriodDays } = params;

  if (semiMajorAxisAU <= 0 || orbitalPeriodDays <= 0) {
    return {
      x: 0,
      y: 0,
      z: 0,
      trueAnomalyRad: 0,
      trueAnomalyDeg: 0,
      currentDistanceAU: 0,
      instantaneousVelocityKmS: 0,
    };
  }

  const e = Math.max(0, Math.min(0.99, eccentricity));
  const period = Math.max(0.1, orbitalPeriodDays);
  const meanMotion = (2 * Math.PI) / period;
  const meanAnomaly = ((simulationDays * meanMotion) % (2 * Math.PI) + 2 * Math.PI) % (2 * Math.PI);

  const E = solveKepler(meanAnomaly, e);

  // True Anomaly ν
  const sinNu = (Math.sqrt(1 - e * e) * Math.sin(E)) / (1 - e * Math.cos(E));
  const cosNu = (Math.cos(E) - e) / (1 - e * Math.cos(E));
  const nu = Math.atan2(sinNu, cosNu);

  // Real heliocentric distance (AU)
  const rAU = semiMajorAxisAU * (1 - e * Math.cos(E));

  // Visual distance
  const aVis = getVisualSemiMajorAxis(semiMajorAxisAU, scaleMode);
  const rVis = aVis * (1 - e * Math.cos(E));

  // 2D position in orbital plane
  const xOrb = rVis * Math.cos(nu);
  const zOrb = rVis * Math.sin(nu);

  // Inclination rotation around X-axis
  const incRad = (orbitalInclinationDeg * Math.PI) / 180;
  const x = xOrb;
  const y = zOrb * Math.sin(incRad);
  const z = zOrb * Math.cos(incRad);

  // Instantaneous velocity (vis-viva approximation)
  const baseV = params.meanOrbitalVelocityKmS || (29.78 / Math.sqrt(semiMajorAxisAU));
  const vInst = baseV * Math.sqrt(Math.max(0.1, (2 * semiMajorAxisAU) / rAU - 1));

  return {
    x,
    y,
    z,
    trueAnomalyRad: nu,
    trueAnomalyDeg: (nu * 180) / Math.PI,
    currentDistanceAU: rAU,
    instantaneousVelocityKmS: vInst,
  };
}

/**
 * Generates closed 3D polyline points for an elliptical orbit.
 */
export function generateOrbitPolyline(
  params: KeplerianParams,
  scaleMode: ScaleMode,
  segments = 120
): [number, number, number][] {
  const { semiMajorAxisAU, eccentricity, orbitalInclinationDeg } = params;
  if (semiMajorAxisAU <= 0) return [];

  const e = Math.max(0, Math.min(0.99, eccentricity));
  const aVis = getVisualSemiMajorAxis(semiMajorAxisAU, scaleMode);
  const incRad = (orbitalInclinationDeg * Math.PI) / 180;

  const points: [number, number, number][] = [];

  for (let i = 0; i <= segments; i++) {
    const E = (i / segments) * 2 * Math.PI;
    const rVis = aVis * (1 - e * Math.cos(E));

    const sinNu = (Math.sqrt(1 - e * e) * Math.sin(E)) / (1 - e * Math.cos(E));
    const cosNu = (Math.cos(E) - e) / (1 - e * Math.cos(E));
    const nu = Math.atan2(sinNu, cosNu);

    const xOrb = rVis * Math.cos(nu);
    const zOrb = rVis * Math.sin(nu);

    const x = xOrb;
    const y = zOrb * Math.sin(incRad);
    const z = zOrb * Math.cos(incRad);

    points.push([x, y, z]);
  }

  return points;
}

/**
 * Computes hierarchical natural satellite position relative to parent body (e.g. Moon around Earth).
 */
export function getSatelliteState(
  parentPos: { x: number; y: number; z: number },
  periodDays: number,
  simulationDays: number,
  scaleMode: ScaleMode,
  inclinationDeg = 5.145
): { x: number; y: number; z: number; relX: number; relY: number; relZ: number } {
  const visualOrbitRadius = scaleMode === 'enhanced' ? 1.6 : 0.9;
  const meanMotion = (2 * Math.PI) / periodDays;
  const angle = (simulationDays * meanMotion) % (2 * Math.PI);
  const incRad = (inclinationDeg * Math.PI) / 180;

  const relX = visualOrbitRadius * Math.cos(angle);
  const relZ = visualOrbitRadius * Math.sin(angle) * Math.cos(incRad);
  const relY = visualOrbitRadius * Math.sin(angle) * Math.sin(incRad);

  return {
    x: parentPos.x + relX,
    y: parentPos.y + relY,
    z: parentPos.z + relZ,
    relX,
    relY,
    relZ,
  };
}

/**
 * Generates relative orbit polyline for a satellite around its parent.
 */
export function generateSatelliteOrbitPolyline(
  scaleMode: ScaleMode,
  inclinationDeg = 5.145,
  segments = 64
): [number, number, number][] {
  const r = scaleMode === 'enhanced' ? 1.6 : 0.9;
  const incRad = (inclinationDeg * Math.PI) / 180;
  const points: [number, number, number][] = [];

  for (let i = 0; i <= segments; i++) {
    const angle = (i / segments) * 2 * Math.PI;
    const x = r * Math.cos(angle);
    const y = r * Math.sin(angle) * Math.sin(incRad);
    const z = r * Math.sin(angle) * Math.cos(incRad);
    points.push([x, y, z]);
  }

  return points;
}
