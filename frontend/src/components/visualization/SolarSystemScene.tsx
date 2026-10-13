import React, { useRef, useMemo, useEffect } from 'react';
import * as THREE from 'three';
import { useThree, useFrame } from '@react-three/fiber';
import { OrbitControls, Stars } from '@react-three/drei';
import { AstronomicalObject } from '../../types/astronomy';
import {
  ScaleMode,
  getKeplerianState,
  getSatelliteState,
  getBodyVisualRadius,
} from '../../utils/orbitalMath';
import { CelestialBodyMesh } from './CelestialBodyMesh';
import { OrbitalTrajectory } from './OrbitalTrajectory';
import { HabitableZoneMesh } from './HabitableZoneMesh';
import { EclipticGrid } from './EclipticGrid';

interface SolarSystemSceneProps {
  objects: AstronomicalObject[];
  simulationDays: number;
  scaleMode: ScaleMode;
  showLabels: boolean;
  showOrbits: boolean;
  showGrid: boolean;
  showHabitableZone: boolean;
  selectedObjectId?: string | null;
  hoveredObjectId?: string | null;
  onSelectObject: (obj: AstronomicalObject) => void;
  onHoverObject: (obj: AstronomicalObject | null) => void;
  isFocusing: boolean;
  resetTrigger: number;
  onLiveStateUpdate?: (
    objId: string,
    state: {
      x: number;
      y: number;
      z: number;
      trueAnomalyDeg: number;
      currentDistanceAU: number;
      instantaneousVelocityKmS: number;
    }
  ) => void;
}

function CameraRig({
  focusPosition,
  isFocusing,
  resetTrigger,
}: {
  focusPosition: [number, number, number] | null;
  isFocusing: boolean;
  resetTrigger: number;
}) {
  const { camera } = useThree();
  const controlsRef = useRef<any>(null);
  const targetVec = useRef(new THREE.Vector3(0, 0, 0));

  useEffect(() => {
    if (controlsRef.current) {
      targetVec.current.set(0, 0, 0);
      controlsRef.current.target.set(0, 0, 0);
      camera.position.set(0, 48, 85);
      controlsRef.current.update();
    }
  }, [resetTrigger, camera]);

  useFrame((_, delta) => {
    if (isFocusing && focusPosition && controlsRef.current) {
      targetVec.current.set(focusPosition[0], focusPosition[1], focusPosition[2]);
      controlsRef.current.target.lerp(targetVec.current, Math.min(1, delta * 3.5));
      controlsRef.current.update();
    }
  });

  return (
    <OrbitControls
      ref={controlsRef}
      makeDefault
      enableDamping
      dampingFactor={0.05}
      minDistance={3}
      maxDistance={450}
    />
  );
}

export const SolarSystemScene: React.FC<SolarSystemSceneProps> = ({
  objects,
  simulationDays,
  scaleMode,
  showLabels,
  showOrbits,
  showGrid,
  showHabitableZone,
  selectedObjectId,
  hoveredObjectId,
  onSelectObject,
  onHoverObject,
  isFocusing,
  resetTrigger,
  onLiveStateUpdate,
}) => {
  // Separate central star, planets, and natural satellites (moons)
  const { star, planets, moons } = useMemo<{
    star: AstronomicalObject | null;
    planets: AstronomicalObject[];
    moons: AstronomicalObject[];
  }>(() => {
    let s: AstronomicalObject | null = null;
    const p: AstronomicalObject[] = [];
    const m: AstronomicalObject[] = [];

    objects.forEach((obj) => {
      if (obj.category === 'Star' || obj.id === 'sun') {
        s = obj;
      } else if (obj.category === 'Moon' || obj.parent_body_id === 'earth') {
        m.push(obj);
      } else if (obj.semi_major_axis_au !== undefined && obj.semi_major_axis_au !== null) {
        p.push(obj);
      }
    });

    return { star: s, planets: p, moons: m };
  }, [objects]);

  // Map to store current 3D position of each body
  const positionsMap = useMemo(() => new Map<string, [number, number, number]>(), []);

  // Compute position for central star
  const starRadius = useMemo(() => {
    return star ? getBodyVisualRadius(star, scaleMode) : 3.5;
  }, [star, scaleMode]);

  positionsMap.set(star?.id || 'sun', [0, 0, 0]);

  // Compute positions of planets
  const planetPositions = useMemo(() => {
    return planets.map((planet) => {
      const state = getKeplerianState(
        {
          semiMajorAxisAU: planet.semi_major_axis_au || 1.0,
          eccentricity: planet.eccentricity || 0.0,
          orbitalInclinationDeg: planet.orbital_inclination_deg || 0.0,
          orbitalPeriodDays: planet.orbital_period_days || 365.25,
          meanOrbitalVelocityKmS: planet.mean_orbital_velocity_km_s || undefined,
        },
        simulationDays,
        scaleMode
      );

      const pos: [number, number, number] = [state.x, state.y, state.z];
      positionsMap.set(planet.id, pos);

      if (planet.id === selectedObjectId && onLiveStateUpdate) {
        onLiveStateUpdate(planet.id, state);
      }

      const visualRadius = getBodyVisualRadius(planet, scaleMode);

      return {
        planet,
        position: pos,
        visualRadius,
        state,
      };
    });
  }, [planets, simulationDays, scaleMode, selectedObjectId, onLiveStateUpdate, positionsMap]);

  // Compute positions for natural satellites (e.g. Moon around Earth)
  const moonPositions = useMemo(() => {
    return moons.map((moon) => {
      const parentId = moon.parent_body_id || 'earth';
      const parentPos = positionsMap.get(parentId) || [0, 0, 0];

      const satState = getSatelliteState(
        { x: parentPos[0], y: parentPos[1], z: parentPos[2] },
        moon.orbital_period_days || 27.322,
        simulationDays,
        scaleMode,
        moon.orbital_inclination_deg || 5.145
      );

      const pos: [number, number, number] = [satState.x, satState.y, satState.z];
      positionsMap.set(moon.id, pos);

      if (moon.id === selectedObjectId && onLiveStateUpdate) {
        onLiveStateUpdate(moon.id, {
          x: satState.x,
          y: satState.y,
          z: satState.z,
          trueAnomalyDeg: ((simulationDays / (moon.orbital_period_days || 27.322)) * 360) % 360,
          currentDistanceAU: moon.semi_major_axis_au || 0.00257,
          instantaneousVelocityKmS: moon.mean_orbital_velocity_km_s || 1.022,
        });
      }

      const visualRadius = getBodyVisualRadius(moon, scaleMode);

      return {
        moon,
        position: pos,
        parentPosition: parentPos,
        visualRadius,
      };
    });
  }, [moons, simulationDays, scaleMode, selectedObjectId, onLiveStateUpdate, positionsMap]);

  // Determine focus target position
  const focusPosition = useMemo(() => {
    if (!selectedObjectId) return null;
    return positionsMap.get(selectedObjectId) || null;
  }, [selectedObjectId, positionsMap]);

  return (
    <>
      {/* Dynamic Camera Rig with OrbitControls & Lerp Focus */}
      <CameraRig
        focusPosition={focusPosition}
        isFocusing={isFocusing}
        resetTrigger={resetTrigger}
      />

      {/* Lighting */}
      <ambientLight intensity={0.25} />
      <pointLight position={[0, 0, 0]} intensity={3.5} color="#fff7ed" distance={1200} decay={0.5} />

      {/* High-Fidelity Starfield */}
      <Stars radius={300} depth={80} count={3500} factor={4} saturation={0.2} fade speed={0.4} />

      {/* Ecliptic Reference Plane Grid */}
      <EclipticGrid scaleMode={scaleMode} visible={showGrid} />

      {/* Circumstellar Habitable Zone */}
      <HabitableZoneMesh scaleMode={scaleMode} visible={showHabitableZone} />

      {/* Central Star (Sun) */}
      {star && (
        <CelestialBodyMesh
          object={star}
          position={[0, 0, 0]}
          visualRadius={starRadius}
          isSelected={selectedObjectId === star.id}
          isHovered={hoveredObjectId === star.id}
          showLabel={showLabels}
          onSelect={() => onSelectObject(star)}
          onHover={(hovered) => onHoverObject(hovered ? star : null)}
        />
      )}

      {/* Planetary Orbit Trajectories & Meshes */}
      {planetPositions.map(({ planet, position, visualRadius }) => (
        <React.Fragment key={planet.id}>
          {/* Keplerian Orbit Line */}
          <OrbitalTrajectory
            params={{
              semiMajorAxisAU: planet.semi_major_axis_au || 1.0,
              eccentricity: planet.eccentricity || 0.0,
              orbitalInclinationDeg: planet.orbital_inclination_deg || 0.0,
              orbitalPeriodDays: planet.orbital_period_days || 365.25,
            }}
            colorHex={planet.color_hex || '#38bdf8'}
            scaleMode={scaleMode}
            visible={showOrbits}
          />

          {/* Planetary Sphere */}
          <CelestialBodyMesh
            object={planet}
            position={position}
            visualRadius={visualRadius}
            isSelected={selectedObjectId === planet.id}
            isHovered={hoveredObjectId === planet.id}
            showLabel={showLabels}
            onSelect={() => onSelectObject(planet)}
            onHover={(hovered) => onHoverObject(hovered ? planet : null)}
          />
        </React.Fragment>
      ))}

      {/* Natural Satellites (e.g. Moon orbiting Earth) */}
      {moonPositions.map(({ moon, position, parentPosition, visualRadius }) => (
        <React.Fragment key={moon.id}>
          {/* Moon's Orbit Line around Earth */}
          <OrbitalTrajectory
            params={{
              semiMajorAxisAU: moon.semi_major_axis_au || 0.00257,
              eccentricity: moon.eccentricity || 0.0549,
              orbitalInclinationDeg: moon.orbital_inclination_deg || 5.145,
              orbitalPeriodDays: moon.orbital_period_days || 27.322,
            }}
            colorHex="#cbd5e1"
            scaleMode={scaleMode}
            visible={showOrbits}
            isSatellite={true}
            parentPosition={parentPosition}
            opacity={0.35}
          />

          {/* Moon Sphere */}
          <CelestialBodyMesh
            object={moon}
            position={position}
            visualRadius={visualRadius}
            isSelected={selectedObjectId === moon.id}
            isHovered={hoveredObjectId === moon.id}
            showLabel={showLabels}
            onSelect={() => onSelectObject(moon)}
            onHover={(hovered) => onHoverObject(hovered ? moon : null)}
          />
        </React.Fragment>
      ))}
    </>
  );
};
