import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { SimulationResult } from '../../types/astronomy';
import {
  Play,
  Pause,
  RotateCcw,
  Activity,
  Eye,
  Maximize2,
  Clock,
  Focus,
  Sliders
} from 'lucide-react';

interface NBodyCanvasProps {
  simulationData: SimulationResult | null;
  isRunning: boolean;
}

export const NBodyCanvas: React.FC<NBodyCanvasProps> = ({ simulationData, isRunning }) => {
  const mountRef = useRef<HTMLDivElement>(null);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(true);
  const [playbackSpeed, setPlaybackSpeed] = useState<number>(1);
  const [showTrails, setShowTrails] = useState(true);
  const [showFullOrbits, setShowFullOrbits] = useState(false);
  const [showLabels, setShowLabels] = useState(true);
  const [trailLength, setTrailLength] = useState(80);
  const [focusedBodyIndex, setFocusedBodyIndex] = useState<number | 'center'>('center');

  const sceneRef = useRef<THREE.Scene | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const particleMeshesRef = useRef<THREE.Mesh[]>([]);
  const trailLinesRef = useRef<THREE.Line[]>([]);
  const fullOrbitLinesRef = useRef<THREE.Line[]>([]);
  const labelsContainerRef = useRef<HTMLDivElement>(null);
  const animationFrameId = useRef<number | null>(null);

  // Camera spherical coordinates
  const sphericalRef = useRef({ radius: 16, theta: 0.6, phi: 1.1 });
  const centerTargetRef = useRef(new THREE.Vector3(0, 0, 0));

  const totalSteps = simulationData?.steps_computed || 0;
  const currentTimestamp = simulationData?.times ? simulationData.times[currentStepIndex] || 0 : 0;
  const currentDays = Math.round(currentTimestamp * 365.25);

  // Initialize Three.js scene
  useEffect(() => {
    const mount = mountRef.current;
    if (!mount) return;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x030712);
    sceneRef.current = scene;

    const camera = new THREE.PerspectiveCamera(50, mount.clientWidth / mount.clientHeight, 0.01, 2000);
    cameraRef.current = camera;

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(mount.clientWidth, mount.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    mount.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    // Ambient and directional lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.9);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
    dirLight.position.set(10, 20, 15);
    scene.add(dirLight);

    // Ecliptic reference grid
    const grid = new THREE.GridHelper(30, 30, 0x334155, 0x1e293b);
    grid.position.y = -0.01;
    scene.add(grid);

    const updateCamera = () => {
      const sph = sphericalRef.current;
      const target = centerTargetRef.current;
      camera.position.x = target.x + sph.radius * Math.sin(sph.phi) * Math.sin(sph.theta);
      camera.position.y = target.y + sph.radius * Math.cos(sph.phi);
      camera.position.z = target.z + sph.radius * Math.sin(sph.phi) * Math.cos(sph.theta);
      camera.lookAt(target);
    };
    updateCamera();

    // Mouse drag rotation & wheel zoom
    let isDragging = false;
    let prevMouse = { x: 0, y: 0 };

    const onMouseDown = (e: MouseEvent) => {
      isDragging = true;
      prevMouse = { x: e.clientX, y: e.clientY };
    };

    const onMouseMove = (e: MouseEvent) => {
      if (!isDragging) return;
      const dx = e.clientX - prevMouse.x;
      const dy = e.clientY - prevMouse.y;
      sphericalRef.current.theta -= dx * 0.007;
      sphericalRef.current.phi = Math.max(0.05, Math.min(Math.PI / 2.05, sphericalRef.current.phi - dy * 0.007));
      prevMouse = { x: e.clientX, y: e.clientY };
      updateCamera();
    };

    const onMouseUp = () => {
      isDragging = false;
    };

    const onWheel = (e: WheelEvent) => {
      e.preventDefault();
      sphericalRef.current.radius = Math.max(1.5, Math.min(200, sphericalRef.current.radius + e.deltaY * 0.02));
      updateCamera();
    };

    const dom = renderer.domElement;
    dom.addEventListener('mousedown', onMouseDown);
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
    dom.addEventListener('wheel', onWheel, { passive: false });

    const handleResize = () => {
      if (!mount) return;
      camera.aspect = mount.clientWidth / mount.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(mount.clientWidth, mount.clientHeight);
    };
    window.addEventListener('resize', handleResize);

    const renderLoop = () => {
      animationFrameId.current = requestAnimationFrame(renderLoop);
      updateCamera();
      renderer.render(scene, camera);
    };
    renderLoop();

    return () => {
      if (animationFrameId.current) cancelAnimationFrame(animationFrameId.current);
      window.removeEventListener('resize', handleResize);
      dom.removeEventListener('mousedown', onMouseDown);
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
      dom.removeEventListener('wheel', onWheel);
      if (mount && dom.parentNode === mount) mount.removeChild(dom);
      renderer.dispose();
    };
  }, []);

  // Reset or adjust scene when simulation data changes
  useEffect(() => {
    if (!sceneRef.current || !simulationData) return;
    const scene = sceneRef.current;

    // Clean up old meshes and trails
    particleMeshesRef.current.forEach((m) => scene.remove(m));
    trailLinesRef.current.forEach((l) => scene.remove(l));
    fullOrbitLinesRef.current.forEach((l) => scene.remove(l));
    particleMeshesRef.current = [];
    trailLinesRef.current = [];
    fullOrbitLinesRef.current = [];

    const newMeshes: THREE.Mesh[] = [];
    const newTrails: THREE.Line[] = [];
    const newFullOrbits: THREE.Line[] = [];

    // Scale scene camera based on max coordinate
    let maxCoord = 2.0;
    simulationData.bodies.forEach((b) => {
      (b.trajectory || []).forEach((pt) => {
        maxCoord = Math.max(maxCoord, Math.abs(pt[0]), Math.abs(pt[1]), Math.abs(pt[2]));
      });
    });
    sphericalRef.current.radius = Math.max(6, Math.min(100, maxCoord * 3.0));

    simulationData.bodies.forEach((body) => {
      const colorVal = parseInt(body.color.replace('#', '0x'), 16) || 0x38bdf8;
      const baseRadius = (body.radius_display || 1.0) * 0.22;

      // Particle Mesh (sphere + glow point)
      const geom = new THREE.SphereGeometry(baseRadius, 24, 24);
      const mat = new THREE.MeshStandardMaterial({
        color: colorVal,
        roughness: 0.3,
        metalness: 0.2,
        emissive: colorVal,
        emissiveIntensity: body.mass >= 0.5 ? 0.7 : 0.15
      });
      const mesh = new THREE.Mesh(geom, mat);
      scene.add(mesh);
      newMeshes.push(mesh);

      // Trajectory ribbon trail line
      const maxPts = body.trajectory.length;
      const trailPositions = new Float32Array(maxPts * 3);
      const trailGeom = new THREE.BufferGeometry();
      trailGeom.setAttribute('position', new THREE.BufferAttribute(trailPositions, 3));
      const trailMat = new THREE.LineBasicMaterial({
        color: colorVal,
        transparent: true,
        opacity: 0.75,
        linewidth: 2
      });
      const trailLine = new THREE.Line(trailGeom, trailMat);
      scene.add(trailLine);
      newTrails.push(trailLine);

      // Full complete orbit line (faint background path)
      const fullPositions = new Float32Array(maxPts * 3);
      body.trajectory.forEach((p, idx) => {
        fullPositions[idx * 3] = p[0];
        fullPositions[idx * 3 + 1] = p[1];
        fullPositions[idx * 3 + 2] = p[2];
      });
      const fullGeom = new THREE.BufferGeometry();
      fullGeom.setAttribute('position', new THREE.BufferAttribute(fullPositions, 3));
      const fullMat = new THREE.LineBasicMaterial({
        color: colorVal,
        transparent: true,
        opacity: 0.2,
        linewidth: 1
      });
      const fullLine = new THREE.Line(fullGeom, fullMat);
      fullLine.visible = showFullOrbits;
      scene.add(fullLine);
      newFullOrbits.push(fullLine);
    });

    particleMeshesRef.current = newMeshes;
    trailLinesRef.current = newTrails;
    fullOrbitLinesRef.current = newFullOrbits;
    setCurrentStepIndex(0);
  }, [simulationData]);

  // Toggle full orbits visibility
  useEffect(() => {
    fullOrbitLinesRef.current.forEach((l) => {
      l.visible = showFullOrbits;
    });
  }, [showFullOrbits]);

  // Toggle trails visibility
  useEffect(() => {
    trailLinesRef.current.forEach((l) => {
      l.visible = showTrails;
    });
  }, [showTrails]);

  // Animation playback interval
  useEffect(() => {
    if (!isPlaying || !simulationData || totalSteps === 0) return;

    const msPerStep = Math.max(16, Math.round(50 / playbackSpeed));
    const interval = setInterval(() => {
      setCurrentStepIndex((prev) => {
        if (prev >= totalSteps) {
          return 0; // Loop playback
        }
        return prev + 1;
      });
    }, msPerStep);

    return () => clearInterval(interval);
  }, [isPlaying, simulationData, totalSteps, playbackSpeed]);

  // Update particle positions and camera tracking at current step
  useEffect(() => {
    if (!simulationData || particleMeshesRef.current.length === 0) return;

    simulationData.bodies.forEach((body, idx) => {
      const mesh = particleMeshesRef.current[idx];
      const trail = trailLinesRef.current[idx];
      if (!mesh || !trail) return;

      const pt = body.trajectory[currentStepIndex] || [0, 0, 0];
      mesh.position.set(pt[0], pt[1], pt[2]);

      // If camera is focused on this body, update camera center target
      if (focusedBodyIndex === idx) {
        centerTargetRef.current.set(pt[0], pt[1], pt[2]);
      }

      // Update dynamic trail
      if (showTrails) {
        const startIdx = Math.max(0, currentStepIndex - trailLength);
        const visiblePts = body.trajectory.slice(startIdx, currentStepIndex + 1);
        const positions = new Float32Array(visiblePts.length * 3);
        visiblePts.forEach((p, i) => {
          positions[i * 3] = p[0];
          positions[i * 3 + 1] = p[1];
          positions[i * 3 + 2] = p[2];
        });
        trail.geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        trail.geometry.attributes.position.needsUpdate = true;
      }
    });

    if (focusedBodyIndex === 'center') {
      centerTargetRef.current.set(0, 0, 0);
    }
  }, [currentStepIndex, simulationData, trailLength, showTrails, focusedBodyIndex]);

  const handleResetCamera = () => {
    sphericalRef.current = { radius: 16, theta: 0.6, phi: 1.1 };
    centerTargetRef.current.set(0, 0, 0);
    setFocusedBodyIndex('center');
  };

  return (
    <div className="flex flex-col space-y-4">
      {/* 3D Simulation Canvas Container */}
      <div className="relative w-full h-[460px] rounded-3xl overflow-hidden border border-white/10 glass-panel shadow-2xl">
        <div ref={mountRef} className="w-full h-full cursor-grab active:cursor-grabbing" />

        {/* Top-Left Engine & Scientific Method HUD */}
        <div className="absolute top-4 left-4 z-10 flex flex-col space-y-1">
          <div className="flex items-center space-x-2 bg-space-950/85 backdrop-blur-md px-3 py-1.5 rounded-xl border border-white/10 text-xs">
            <Activity className="w-4 h-4 text-sky-400" />
            <span className="text-slate-300">
              Integrator:{' '}
              <strong className="text-white font-mono">{simulationData?.engine_used || 'Initializing...'}</strong>
            </span>
          </div>

          <div className="flex items-center space-x-2 bg-space-950/85 backdrop-blur-md px-3 py-1.5 rounded-xl border border-white/10 text-xs text-slate-300 font-mono">
            <Clock className="w-3.5 h-3.5 text-indigo-400" />
            <span>Time: </span>
            <strong className="text-sky-400 font-bold">{currentTimestamp.toFixed(3)} yr</strong>
            <span className="text-slate-400">({currentDays} days)</span>
          </div>
        </div>

        {/* Top-Right Step HUD & View Controls */}
        <div className="absolute top-4 right-4 z-10 flex items-center space-x-2">
          {/* Focus Selector */}
          {simulationData && simulationData.bodies.length > 0 && (
            <div className="flex items-center space-x-1.5 bg-space-950/85 backdrop-blur-md px-2.5 py-1.5 rounded-xl border border-white/10 text-xs">
              <Focus className="w-3.5 h-3.5 text-sky-400" />
              <select
                value={focusedBodyIndex}
                onChange={(e) => {
                  const val = e.target.value;
                  setFocusedBodyIndex(val === 'center' ? 'center' : parseInt(val, 10));
                }}
                className="bg-transparent border-0 text-xs text-slate-200 focus:outline-none"
              >
                <option value="center" className="bg-space-900">Focus: System Center</option>
                {simulationData.bodies.map((b, idx) => (
                  <option key={b.id} value={idx} className="bg-space-900">
                    Focus: {b.name}
                  </option>
                ))}
              </select>
            </div>
          )}

          {/* Reset Camera */}
          <button
            onClick={handleResetCamera}
            className="p-2 rounded-xl bg-space-950/85 backdrop-blur-md border border-white/10 text-slate-300 hover:text-white transition-all"
            title="Reset Camera View"
          >
            <Maximize2 className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Dynamic 2D Labels Overlay */}
        {showLabels && simulationData && (
          <div ref={labelsContainerRef} className="absolute inset-0 pointer-events-none z-10">
            {simulationData.bodies.map((b, idx) => {
              const pt = b.trajectory[currentStepIndex] || [0, 0, 0];
              const cam = cameraRef.current;
              const mount = mountRef.current;
              if (!cam || !mount) return null;

              const v = new THREE.Vector3(pt[0], pt[1], pt[2]);
              v.project(cam);

              // Check if in front of camera
              if (v.z > 1.0) return null;

              const x = ((v.x + 1) * mount.clientWidth) / 2;
              const y = ((-v.y + 1) * mount.clientHeight) / 2;

              return (
                <div
                  key={b.id}
                  style={{
                    transform: `translate(${x + 8}px, ${y - 12}px)`
                  }}
                  className="absolute text-[10px] font-mono px-1.5 py-0.5 rounded bg-space-950/80 backdrop-blur-sm border border-white/10 text-slate-200 flex items-center space-x-1"
                >
                  <span className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: b.color }} />
                  <span>{b.name}</span>
                </div>
              );
            })}
          </div>
        )}

        {/* Bottom Playback & Scrubber Controls Bar */}
        <div className="absolute bottom-4 left-4 right-4 z-20 flex flex-col space-y-2 bg-space-950/90 backdrop-blur-md p-3 rounded-2xl border border-white/10">
          <div className="flex items-center justify-between text-xs">
            {/* Play, Pause, Reset */}
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setIsPlaying(!isPlaying)}
                className="p-2 rounded-xl bg-sky-500/20 text-sky-400 hover:bg-sky-500/30 transition-all"
                title={isPlaying ? 'Pause' : 'Play'}
              >
                {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
              </button>
              <button
                onClick={() => setCurrentStepIndex(0)}
                className="p-2 rounded-xl bg-white/5 text-slate-300 hover:bg-white/10 transition-all"
                title="Reset to Step 0"
              >
                <RotateCcw className="w-4 h-4" />
              </button>
            </div>

            {/* Scrubber Range Input */}
            <div className="flex-1 mx-4 flex items-center space-x-3">
              <span className="text-[11px] font-mono text-slate-400">Step:</span>
              <input
                type="range"
                min={0}
                max={Math.max(1, totalSteps)}
                value={currentStepIndex}
                onChange={(e) => setCurrentStepIndex(parseInt(e.target.value, 10))}
                className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-sky-500"
              />
              <span className="text-[11px] font-mono text-sky-400 font-bold min-w-[60px] text-right">
                {currentStepIndex} / {totalSteps}
              </span>
            </div>

            {/* Playback Speed Selectors */}
            <div className="flex items-center space-x-1">
              <span className="text-slate-400 text-[11px] mr-1">Speed:</span>
              {[0.25, 0.5, 1, 2, 5].map((spd) => (
                <button
                  key={spd}
                  onClick={() => setPlaybackSpeed(spd)}
                  className={`px-2 py-0.5 rounded text-[11px] font-mono transition-all ${
                    playbackSpeed === spd
                      ? 'bg-sky-500 text-white font-bold'
                      : 'bg-white/5 text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {spd}x
                </button>
              ))}
            </div>
          </div>

          {/* Secondary Controls Bar (Toggles) */}
          <div className="flex items-center justify-between text-[11px] pt-1 border-t border-white/5 text-slate-400">
            <div className="flex items-center space-x-4">
              <label className="flex items-center space-x-1.5 cursor-pointer hover:text-slate-200">
                <input
                  type="checkbox"
                  checked={showTrails}
                  onChange={(e) => setShowTrails(e.target.checked)}
                  className="rounded accent-sky-500"
                />
                <span>Motion Trails</span>
              </label>

              <label className="flex items-center space-x-1.5 cursor-pointer hover:text-slate-200">
                <input
                  type="checkbox"
                  checked={showFullOrbits}
                  onChange={(e) => setShowFullOrbits(e.target.checked)}
                  className="rounded accent-sky-500"
                />
                <span>Full Orbit Paths</span>
              </label>

              <label className="flex items-center space-x-1.5 cursor-pointer hover:text-slate-200">
                <input
                  type="checkbox"
                  checked={showLabels}
                  onChange={(e) => setShowLabels(e.target.checked)}
                  className="rounded accent-sky-500"
                />
                <span>Body Labels</span>
              </label>
            </div>

            <div className="flex items-center space-x-2">
              <span>Trail Length:</span>
              <input
                type="range"
                min={20}
                max={200}
                step={10}
                value={trailLength}
                onChange={(e) => setTrailLength(parseInt(e.target.value, 10))}
                className="w-16 h-1 bg-slate-800 rounded accent-sky-500"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
