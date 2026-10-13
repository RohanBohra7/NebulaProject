import React, { useState, useCallback, useRef } from 'react';
import { AstronomicalObject } from '../../types/astronomy';
import { ScaleMode } from '../../utils/orbitalMath';
import { AstronomyCanvas } from './AstronomyCanvas';
import { VisualizationHUD } from './VisualizationHUD';

interface SolarSystemCanvasProps {
  objects: AstronomicalObject[];
  selectedObjectId?: string | null;
  onSelectObject?: (obj: AstronomicalObject) => void;
  showHabitableZone?: boolean;
  className?: string;
  focusTrigger?: number;
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

export const SolarSystemCanvas: React.FC<SolarSystemCanvasProps> = ({
  objects,
  selectedObjectId,
  onSelectObject,
  showHabitableZone: initialShowHabitableZone = true,
  className = '',
  focusTrigger,
  onLiveStateUpdate,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);

  // Time simulation state
  const [isPlaying, setIsPlaying] = useState(true);
  const [simulationDays, setSimulationDays] = useState(0);
  const [speedMultiplier, setSpeedMultiplier] = useState(10);

  // Visual toggles
  const [scaleMode, setScaleMode] = useState<ScaleMode>('enhanced');
  const [showLabels, setShowLabels] = useState(true);
  const [showOrbits, setShowOrbits] = useState(true);
  const [showGrid, setShowGrid] = useState(true);
  const [showHabitableZone, setShowHabitableZone] = useState(initialShowHabitableZone);

  // Camera focus & reset triggers
  const [isFocusing, setIsFocusing] = useState(false);
  const [resetTrigger, setResetTrigger] = useState(0);
  const [isFullscreen, setIsFullscreen] = useState(false);

  // Respond to external focus triggers
  React.useEffect(() => {
    if (focusTrigger && focusTrigger > 0) {
      setIsFocusing(true);
    }
  }, [focusTrigger]);

  // Time progression handler
  const handleAdvanceTime = useCallback((deltaDays: number) => {
    setSimulationDays((prev) => prev + deltaDays);
  }, []);

  const handleResetTime = useCallback(() => {
    setSimulationDays(0);
  }, []);

  const handleStepTime = useCallback((days: number) => {
    setSimulationDays((prev) => Math.max(0, prev + days));
  }, []);

  const handleResetCamera = useCallback(() => {
    setIsFocusing(false);
    setResetTrigger((prev) => prev + 1);
  }, []);

  const handleFocusSelected = useCallback(() => {
    if (selectedObjectId) {
      setIsFocusing(true);
    }
  }, [selectedObjectId]);

  const handleSelectObject = useCallback(
    (obj: AstronomicalObject) => {
      onSelectObject?.(obj);
      setIsFocusing(true);
    },
    [onSelectObject]
  );

  const handleToggleFullscreen = useCallback(() => {
    if (!containerRef.current) return;
    if (!document.fullscreenElement) {
      containerRef.current.requestFullscreen().then(() => setIsFullscreen(true)).catch(() => {});
    } else {
      document.exitFullscreen().then(() => setIsFullscreen(false)).catch(() => {});
    }
  }, []);

  // Selected object name
  const selectedObj = objects.find((o) => o.id === selectedObjectId);

  return (
    <div
      ref={containerRef}
      className={`relative w-full h-full flex flex-col space-y-3 ${className}`}
    >
      {/* HUD Floating Controls Header */}
      <VisualizationHUD
        isPlaying={isPlaying}
        onTogglePlay={() => setIsPlaying(!isPlaying)}
        onResetTime={handleResetTime}
        onStepTime={handleStepTime}
        speedMultiplier={speedMultiplier}
        onChangeSpeed={setSpeedMultiplier}
        simulationDays={simulationDays}
        showLabels={showLabels}
        onToggleLabels={() => setShowLabels(!showLabels)}
        showOrbits={showOrbits}
        onToggleOrbits={() => setShowOrbits(!showOrbits)}
        showGrid={showGrid}
        onToggleGrid={() => setShowGrid(!showGrid)}
        showHabitableZone={showHabitableZone}
        onToggleHabitableZone={() => setShowHabitableZone(!showHabitableZone)}
        scaleMode={scaleMode}
        onToggleScaleMode={setScaleMode}
        onResetCamera={handleResetCamera}
        onFocusSelected={handleFocusSelected}
        selectedObjectName={selectedObj?.name}
        isFullscreen={isFullscreen}
        onToggleFullscreen={handleToggleFullscreen}
      />

      {/* R3F 3D Canvas */}
      <div className="flex-1 w-full min-h-[500px]">
        <AstronomyCanvas
          objects={objects}
          simulationDays={simulationDays}
          onAdvanceTime={handleAdvanceTime}
          isPlaying={isPlaying}
          speedMultiplier={speedMultiplier}
          scaleMode={scaleMode}
          showLabels={showLabels}
          showOrbits={showOrbits}
          showGrid={showGrid}
          showHabitableZone={showHabitableZone}
          selectedObjectId={selectedObjectId}
          onSelectObject={handleSelectObject}
          isFocusing={isFocusing}
          resetTrigger={resetTrigger}
          onLiveStateUpdate={onLiveStateUpdate}
        />
      </div>
    </div>
  );
};
