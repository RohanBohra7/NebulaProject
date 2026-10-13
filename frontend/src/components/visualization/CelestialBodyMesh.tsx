import React, { useRef, useMemo } from 'react';
import * as THREE from 'three';
import { useFrame } from '@react-three/fiber';
import { Html } from '@react-three/drei';
import { AstronomicalObject } from '../../types/astronomy';

interface CelestialBodyMeshProps {
  object: AstronomicalObject;
  position: [number, number, number];
  visualRadius: number;
  isSelected?: boolean;
  isHovered?: boolean;
  showLabel?: boolean;
  onSelect?: () => void;
  onHover?: (hovered: boolean) => void;
}

export const CelestialBodyMesh: React.FC<CelestialBodyMeshProps> = ({
  object,
  position,
  visualRadius,
  isSelected = false,
  isHovered = false,
  showLabel = true,
  onSelect,
  onHover,
}) => {
  const meshRef = useRef<THREE.Mesh>(null);
  const glowRef = useRef<THREE.Mesh>(null);
  const selectionRingRef = useRef<THREE.Mesh>(null);

  const isStar = object.category === 'Star' || object.id === 'sun';
  const colorHex = object.color_hex || '#38bdf8';
  const colorVal = useMemo(() => parseInt(colorHex.replace('#', '0x'), 16), [colorHex]);

  // Axial rotation in animation loop
  useFrame((_, delta) => {
    if (meshRef.current) {
      // Rotate planet on its axis
      meshRef.current.rotation.y += delta * (isStar ? 0.2 : 0.8);
    }
    if (glowRef.current) {
      glowRef.current.rotation.y += delta * 0.1;
    }
    if (selectionRingRef.current) {
      selectionRingRef.current.rotation.z += delta * 1.5;
    }
  });

  return (
    <group position={position}>
      {/* Central Celestial Sphere */}
      <mesh
        ref={meshRef}
        onClick={(e) => {
          e.stopPropagation();
          onSelect?.();
        }}
        onPointerOver={(e) => {
          e.stopPropagation();
          onHover?.(true);
        }}
        onPointerOut={(e) => {
          e.stopPropagation();
          onHover?.(false);
        }}
        scale={isHovered ? 1.08 : 1.0}
      >
        <sphereGeometry args={[visualRadius, 36, 36]} />
        {isStar ? (
          <meshBasicMaterial color={colorVal} />
        ) : (
          <meshStandardMaterial
            color={colorVal}
            roughness={0.6}
            metalness={0.15}
          />
        )}
      </mesh>

      {/* Stellar / Atmosphere Outer Glow */}
      {(isStar || object.has_atmosphere) && (
        <mesh ref={glowRef}>
          <sphereGeometry args={[visualRadius * (isStar ? 1.3 : 1.1), 32, 32]} />
          <meshBasicMaterial
            color={colorVal}
            transparent
            opacity={isStar ? 0.25 : 0.12}
            side={THREE.BackSide}
            depthWrite={false}
          />
        </mesh>
      )}

      {/* Ring System (Saturn, Uranus) */}
      {object.has_rings && (
        <mesh rotation={[Math.PI / 2.3, 0, 0]}>
          <ringGeometry args={[visualRadius * 1.45, visualRadius * 2.4, 48]} />
          <meshBasicMaterial
            color={object.id === 'saturn' ? '#fde047' : '#93c5fd'}
            side={THREE.DoubleSide}
            transparent
            opacity={0.65}
            depthWrite={false}
          />
        </mesh>
      )}

      {/* Selected Target Highlight Ring */}
      {isSelected && (
        <mesh ref={selectionRingRef} rotation={[-Math.PI / 2, 0, 0]}>
          <ringGeometry args={[visualRadius * 1.55, visualRadius * 1.75, 48]} />
          <meshBasicMaterial
            color="#38bdf8"
            side={THREE.DoubleSide}
            transparent
            opacity={0.85}
            depthWrite={false}
          />
        </mesh>
      )}

      {/* Hover Pulse Ring */}
      {isHovered && !isSelected && (
        <mesh rotation={[-Math.PI / 2, 0, 0]}>
          <ringGeometry args={[visualRadius * 1.4, visualRadius * 1.52, 32]} />
          <meshBasicMaterial
            color="#a78bfa"
            side={THREE.DoubleSide}
            transparent
            opacity={0.6}
            depthWrite={false}
          />
        </mesh>
      )}

      {/* 2D/3D Label Overlay */}
      {showLabel && (
        <Html
          position={[0, visualRadius + (visualRadius > 2 ? 1.4 : 0.9), 0]}
          center
          distanceFactor={55}
          style={{
            pointerEvents: 'none',
            userSelect: 'none',
            whiteSpace: 'nowrap',
          }}
        >
          <div
            className={`px-2 py-0.5 rounded-full text-[10px] font-mono tracking-tight transition-all duration-200 backdrop-blur-md border ${
              isSelected
                ? 'bg-sky-500/90 text-white border-sky-300 shadow-lg shadow-sky-500/30 font-bold scale-110'
                : isHovered
                ? 'bg-purple-900/90 text-purple-200 border-purple-400 font-semibold scale-105'
                : 'bg-space-950/75 text-slate-300 border-white/10'
            }`}
          >
            <div className="flex items-center space-x-1">
              <span
                className="w-1.5 h-1.5 rounded-full"
                style={{ backgroundColor: colorHex }}
              />
              <span>{object.name}</span>
            </div>
          </div>
        </Html>
      )}
    </group>
  );
};
