import React, { useMemo } from 'react';
import * as THREE from 'three';
import { ScaleMode, getVisualSemiMajorAxis } from '../../utils/orbitalMath';

interface EclipticGridProps {
  scaleMode: ScaleMode;
  visible?: boolean;
}

export const EclipticGrid: React.FC<EclipticGridProps> = ({ scaleMode, visible = true }) => {
  // Key distance markers in AU
  const distanceAUs = [1.0, 5.0, 10.0, 20.0, 30.0];

  const ringGeometries = useMemo(() => {
    return distanceAUs.map((au) => {
      const radius = getVisualSemiMajorAxis(au, scaleMode);
      return {
        au,
        radius,
        geometry: new THREE.RingGeometry(radius - 0.04, radius + 0.04, 128),
      };
    });
  }, [scaleMode]);

  if (!visible) return null;

  return (
    <group rotation={[-Math.PI / 2, 0, 0]}>
      {/* Plane Grid Helper */}
      <gridHelper args={[160, 32, '#38bdf8', '#1e293b']} rotation={[Math.PI / 2, 0, 0]} />

      {/* Concentric Astronomical Unit Guidance Rings */}
      {ringGeometries.map(({ au, geometry }) => (
        <mesh key={au} geometry={geometry}>
          <meshBasicMaterial
            color="#64748b"
            transparent
            opacity={0.18}
            side={THREE.DoubleSide}
            depthWrite={false}
          />
        </mesh>
      ))}
    </group>
  );
};
