import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { AstronomicalObject } from '../../types/astronomy';

interface Object3DViewerProps {
  object?: AstronomicalObject;
  colorHex?: string;
  hasRings?: boolean;
  hasAtmosphere?: boolean;
  category?: string;
  size?: number;
}

export const Object3DViewer: React.FC<Object3DViewerProps> = ({
  object,
  colorHex,
  hasRings,
  hasAtmosphere,
  category,
  size = 320
}) => {
  const mountRef = useRef<HTMLDivElement>(null);

  const effectiveColor = object?.color_hex || colorHex || '#38bdf8';
  const effectiveHasRings = object?.has_rings ?? hasRings ?? false;
  const effectiveCategory = object?.category || category || 'Planet';
  const effectiveHasAtmosphere = object?.has_atmosphere ?? hasAtmosphere ?? (effectiveCategory === 'Star');

  useEffect(() => {
    const mount = mountRef.current;
    if (!mount) return;

    const width = mount.clientWidth || size;
    const height = size;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x070b19);

    const camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 100);
    camera.position.set(0, 0, 5.5);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    mount.appendChild(renderer.domElement);

    // Lights
    const ambient = new THREE.AmbientLight(0xffffff, 0.4);
    scene.add(ambient);

    const dirLight = new THREE.DirectionalLight(0xffffff, 2.5);
    dirLight.position.set(5, 3, 5);
    scene.add(dirLight);

    // Object Mesh
    const colorVal = parseInt(effectiveColor.replace('#', '0x'), 16);
    const geom = new THREE.SphereGeometry(1.6, 48, 48);
    const isStar = effectiveCategory === 'Star';

    const mat = isStar
      ? new THREE.MeshBasicMaterial({ color: colorVal })
      : new THREE.MeshStandardMaterial({
          color: colorVal,
          roughness: 0.5,
          metalness: 0.1
        });

    const mesh = new THREE.Mesh(geom, mat);
    scene.add(mesh);

    // Rings
    if (effectiveHasRings) {
      const ringGeom = new THREE.RingGeometry(2.1, 3.4, 64);
      const ringMat = new THREE.MeshBasicMaterial({
        color: 0xfde047,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.75
      });
      const ringMesh = new THREE.Mesh(ringGeom, ringMat);
      ringMesh.rotation.x = Math.PI / 2.5;
      mesh.add(ringMesh);
    }

    // Atmosphere Glow
    if (effectiveHasAtmosphere || isStar) {
      const glowGeom = new THREE.SphereGeometry(1.75, 32, 32);
      const glowMat = new THREE.MeshBasicMaterial({
        color: colorVal,
        transparent: true,
        opacity: 0.2
      });
      const glowMesh = new THREE.Mesh(glowGeom, glowMat);
      scene.add(glowMesh);
    }

    let animId: number;
    const animate = () => {
      animId = requestAnimationFrame(animate);
      mesh.rotation.y += 0.005;
      renderer.render(scene, camera);
    };
    animate();

    return () => {
      cancelAnimationFrame(animId);
      if (mount && renderer.domElement.parentNode === mount) {
        mount.removeChild(renderer.domElement);
      }
      renderer.dispose();
    };
  }, [effectiveColor, effectiveHasRings, effectiveCategory, effectiveHasAtmosphere, size]);

  return (
    <div
      ref={mountRef}
      className="w-full rounded-2xl overflow-hidden glass-panel border border-white/10 shadow-xl flex items-center justify-center relative"
      style={{ height: `${size}px` }}
    >
      <div className="absolute bottom-2 right-3 text-[10px] text-slate-400 font-mono pointer-events-none">
        3D Simulation View
      </div>
    </div>
  );
};
