import React, { useMemo } from 'react';
import * as THREE from 'three';
import {
  KeplerianParams,
  ScaleMode,
  generateOrbitPolyline,
  generateSatelliteOrbitPolyline,
} from '../../utils/orbitalMath';

interface OrbitalTrajectoryProps {
  params: KeplerianParams;
  colorHex?: string;
  scaleMode: ScaleMode;
  visible?: boolean;
  isSatellite?: boolean;
  parentPosition?: [number, number, number];
  opacity?: number;
}

export const OrbitalTrajectory: React.FC<OrbitalTrajectoryProps> = ({
  params,
  colorHex = '#38bdf8',
  scaleMode,
  visible = true,
  isSatellite = false,
  parentPosition,
  opacity = 0.28,
}) => {
  const points = useMemo(() => {
    if (isSatellite) {
      return generateSatelliteOrbitPolyline(scaleMode, params.orbitalInclinationDeg || 5.145, 64);
    }
    return generateOrbitPolyline(params, scaleMode, 128);
  }, [params, scaleMode, isSatellite]);

  const lineGeometry = useMemo(() => {
    if (points.length === 0) return null;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(points.length * 3);

    for (let i = 0; i < points.length; i++) {
      positions[i * 3] = points[i][0];
      positions[i * 3 + 1] = points[i][1];
      positions[i * 3 + 2] = points[i][2];
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    return geometry;
  }, [points]);

  const colorVal = useMemo(() => {
    return parseInt((colorHex || '#38bdf8').replace('#', '0x'), 16);
  }, [colorHex]);

  const lineMesh = useMemo(() => {
    if (!lineGeometry) return null;
    const mat = new THREE.LineBasicMaterial({
      color: colorVal,
      transparent: true,
      opacity: isSatellite ? opacity * 0.75 : opacity,
      depthWrite: false,
    });
    return new THREE.Line(lineGeometry, mat);
  }, [lineGeometry, colorVal, isSatellite, opacity]);

  if (!visible || !lineMesh) return null;

  const groupPos: [number, number, number] = isSatellite && parentPosition ? parentPosition : [0, 0, 0];

  return (
    <group position={groupPos}>
      <primitive object={lineMesh} />
    </group>
  );
};
