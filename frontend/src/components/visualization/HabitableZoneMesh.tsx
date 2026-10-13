import React, { useMemo } from 'react';
import * as THREE from 'three';
import { ScaleMode, getVisualSemiMajorAxis } from '../../utils/orbitalMath';

interface HabitableZoneMeshProps {
  scaleMode: ScaleMode;
  visible?: boolean;
}

export const HabitableZoneMesh: React.FC<HabitableZoneMeshProps> = ({ scaleMode, visible = true }) => {
  // Solar System habitable zone boundaries: ~0.95 AU (inner) to ~1.67 AU (outer)
  const innerRadius = useMemo(() => getVisualSemiMajorAxis(0.95, scaleMode), [scaleMode]);
  const outerRadius = useMemo(() => getVisualSemiMajorAxis(1.67, scaleMode), [scaleMode]);

  const geometry = useMemo(() => {
    return new THREE.RingGeometry(innerRadius, outerRadius, 96);
  }, [innerRadius, outerRadius]);

  if (!visible) return null;

  return (
    <group rotation={[-Math.PI / 2, 0, 0]}>
      {/* Translucent Green Disk */}
      <mesh geometry={geometry}>
        <meshBasicMaterial
          color="#10b981"
          transparent
          opacity={0.07}
          side={THREE.DoubleSide}
          depthWrite={false}
        />
      </mesh>

      {/* Inner Boundary Line */}
      <mesh>
        <ringGeometry args={[innerRadius - 0.05, innerRadius + 0.05, 96]} />
        <meshBasicMaterial
          color="#10b981"
          transparent
          opacity={0.25}
          side={THREE.DoubleSide}
          depthWrite={false}
        />
      </mesh>

      {/* Outer Boundary Line */}
      <mesh>
        <ringGeometry args={[outerRadius - 0.05, outerRadius + 0.05, 96]} />
        <meshBasicMaterial
          color="#10b981"
          transparent
          opacity={0.2}
          side={THREE.DoubleSide}
          depthWrite={false}
        />
      </mesh>
    </group>
  );
};
