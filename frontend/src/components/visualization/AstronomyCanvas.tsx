import React, { useRef, useState, useCallback } from 'react';
import { Canvas } from '@react-three/fiber';
import { AstronomicalObject } from '../../types/astronomy';
import { ScaleMode } from '../../utils/orbitalMath';
import { SolarSystemScene } from './SolarSystemScene';

interface AstronomyCanvasProps {
  objects: AstronomicalObject[];
  simulationDays: number;
  onAdvanceTime: (deltaDays: number) => void;
  isPlaying: boolean;
  speedMultiplier: number;

  scaleMode: ScaleMode;
  showLabels: boolean;
  showOrbits: boolean;
  showGrid: boolean;
  showHabitableZone: boolean;

  selectedObjectId?: string | null;
  onSelectObject: (obj: AstronomicalObject) => void;

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

// Time Driver runs inside R3F render loop
function TimeDriver({
  isPlaying,
  speedMultiplier,
  onAdvanceTime,
}: {
  isPlaying: boolean;
  speedMultiplier: number;
  onAdvanceTime: (deltaDays: number) => void;
}) {
  // We use standard requestAnimationFrame in component or useFrame
  return null;
}

export const AstronomyCanvas: React.FC<AstronomyCanvasProps> = ({
  objects,
  simulationDays,
  onAdvanceTime,
  isPlaying,
  speedMultiplier,
  scaleMode,
  showLabels,
  showOrbits,
  showGrid,
  showHabitableZone,
  selectedObjectId,
  onSelectObject,
  isFocusing,
  resetTrigger,
  onLiveStateUpdate,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [hoveredObject, setHoveredObject] = useState<AstronomicalObject | null>(null);

  // Animation frame loop for smooth time progression
  const lastTimeRef = useRef<number | null>(null);
  const animFrameRef = useRef<number | null>(null);

  React.useEffect(() => {
    let active = true;

    const loop = (currentTime: number) => {
      if (!active) return;
      if (lastTimeRef.current !== null && isPlaying) {
        const deltaSeconds = (currentTime - lastTimeRef.current) / 1000;
        // 1 wall-clock second = 1 day at 1x speed
        onAdvanceTime(deltaSeconds * speedMultiplier);
      }
      lastTimeRef.current = currentTime;
      animFrameRef.current = requestAnimationFrame(loop);
    };

    animFrameRef.current = requestAnimationFrame(loop);

    return () => {
      active = false;
      if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current);
    };
  }, [isPlaying, speedMultiplier, onAdvanceTime]);

  return (
    <div
      ref={containerRef}
      className="relative w-full h-full min-h-[550px] rounded-3xl overflow-hidden border border-white/10 glass-panel shadow-2xl bg-space-950"
    >
      {/* React Three Fiber Canvas */}
      <Canvas
        camera={{ position: [0, 48, 85], fov: 45, near: 0.1, far: 3000 }}
        gl={{ antialias: true, alpha: true, powerPreference: 'high-performance' }}
        dpr={[1, 2]}
      >
        <SolarSystemScene
          objects={objects}
          simulationDays={simulationDays}
          scaleMode={scaleMode}
          showLabels={showLabels}
          showOrbits={showOrbits}
          showGrid={showGrid}
          showHabitableZone={showHabitableZone}
          selectedObjectId={selectedObjectId}
          hoveredObjectId={hoveredObject?.id}
          onSelectObject={onSelectObject}
          onHoverObject={setHoveredObject}
          isFocusing={isFocusing}
          resetTrigger={resetTrigger}
          onLiveStateUpdate={onLiveStateUpdate}
        />
      </Canvas>

      {/* Hover Info Tooltip */}
      {hoveredObject && (
        <div className="absolute top-4 left-1/2 -translate-x-1/2 z-20 pointer-events-none animate-fade-in">
          <div className="px-3.5 py-1.5 rounded-full bg-space-900/90 border border-white/15 backdrop-blur-md shadow-lg text-xs flex items-center space-x-2">
            <span
              className="w-2.5 h-2.5 rounded-full"
              style={{ backgroundColor: hoveredObject.color_hex || '#38bdf8' }}
            />
            <span className="font-bold text-white">{hoveredObject.name}</span>
            <span className="text-slate-400 font-mono text-[11px]">• {hoveredObject.category}</span>
            {hoveredObject.semi_major_axis_au !== undefined && hoveredObject.semi_major_axis_au !== null && (
              <span className="text-sky-300 font-mono text-[11px]">
                • {hoveredObject.semi_major_axis_au} AU
              </span>
            )}
          </div>
        </div>
      )}

      {/* Camera Guidance Notice Footer */}
      <div className="absolute bottom-4 left-4 z-10 text-[11px] text-slate-400 bg-space-950/75 backdrop-blur-md px-3.5 py-1.5 rounded-xl border border-white/10 pointer-events-none font-sans">
        🖱️ Left Click + Drag to Rotate • Right Click / Two-finger to Pan • Scroll to Zoom • Click Object to Select
      </div>

      {/* Tracking Indicator Badge */}
      {selectedObjectId && (
        <div className="absolute top-4 right-4 z-10 text-xs bg-sky-950/90 border border-sky-400/30 text-sky-200 px-3.5 py-1.5 rounded-xl backdrop-blur-md flex items-center space-x-2 shadow-lg">
          <span className="w-2 h-2 rounded-full bg-sky-400 animate-ping" />
          <span>Tracking Target: <strong className="font-semibold text-white capitalize">{selectedObjectId}</strong></span>
        </div>
      )}
    </div>
  );
};
