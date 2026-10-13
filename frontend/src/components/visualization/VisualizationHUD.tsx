import React from 'react';
import {
  Play,
  Pause,
  RotateCcw,
  StepForward,
  StepBack,
  Eye,
  Orbit,
  Grid,
  Shield,
  Maximize2,
  Minimize2,
  Crosshair,
  Compass,
} from 'lucide-react';
import { ScaleMode } from '../../utils/orbitalMath';
import { ScaleNotice } from './ScaleNotice';

interface VisualizationHUDProps {
  isPlaying: boolean;
  onTogglePlay: () => void;
  onResetTime: () => void;
  onStepTime: (days: number) => void;
  speedMultiplier: number;
  onChangeSpeed: (speed: number) => void;
  simulationDays: number;

  showLabels: boolean;
  onToggleLabels: () => void;
  showOrbits: boolean;
  onToggleOrbits: () => void;
  showGrid: boolean;
  onToggleGrid: () => void;
  showHabitableZone: boolean;
  onToggleHabitableZone: () => void;

  scaleMode: ScaleMode;
  onToggleScaleMode: (mode: ScaleMode) => void;

  onResetCamera: () => void;
  onFocusSelected: () => void;
  selectedObjectName?: string | null;

  isFullscreen: boolean;
  onToggleFullscreen: () => void;
}

export const VisualizationHUD: React.FC<VisualizationHUDProps> = ({
  isPlaying,
  onTogglePlay,
  onResetTime,
  onStepTime,
  speedMultiplier,
  onChangeSpeed,
  simulationDays,

  showLabels,
  onToggleLabels,
  showOrbits,
  onToggleOrbits,
  showGrid,
  onToggleGrid,
  showHabitableZone,
  onToggleHabitableZone,

  scaleMode,
  onToggleScaleMode,

  onResetCamera,
  onFocusSelected,
  selectedObjectName,

  isFullscreen,
  onToggleFullscreen,
}) => {
  const speeds = [0.1, 1, 5, 20, 100, 500];
  const earthYears = (simulationDays / 365.25).toFixed(2);

  return (
    <div className="flex flex-wrap items-center justify-between gap-3 p-3 bg-space-950/85 backdrop-blur-md rounded-2xl border border-white/10 shadow-xl text-xs">
      {/* 1. Time Control Cluster */}
      <div className="flex items-center space-x-1.5">
        {/* Play/Pause */}
        <button
          onClick={onTogglePlay}
          className={`p-2 rounded-xl transition-all flex items-center space-x-1.5 font-semibold ${
            isPlaying
              ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30 hover:bg-amber-500/30'
              : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 hover:bg-emerald-500/30'
          }`}
          title={isPlaying ? 'Pause Simulation' : 'Resume Simulation'}
        >
          {isPlaying ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
          <span>{isPlaying ? 'Pause' : 'Play'}</span>
        </button>

        {/* Step Backward */}
        <button
          onClick={() => onStepTime(-10)}
          className="p-2 rounded-xl bg-white/5 border border-white/10 text-slate-300 hover:bg-white/10 hover:text-white transition-all"
          title="Step Backward -10 Days"
        >
          <StepBack className="w-3.5 h-3.5" />
        </button>

        {/* Step Forward */}
        <button
          onClick={() => onStepTime(10)}
          className="p-2 rounded-xl bg-white/5 border border-white/10 text-slate-300 hover:bg-white/10 hover:text-white transition-all"
          title="Step Forward +10 Days"
        >
          <StepForward className="w-3.5 h-3.5" />
        </button>

        {/* Reset Time */}
        <button
          onClick={onResetTime}
          className="p-2 rounded-xl bg-white/5 border border-white/10 text-slate-300 hover:bg-white/10 hover:text-white transition-all"
          title="Reset Simulation Time (t = 0)"
        >
          <RotateCcw className="w-3.5 h-3.5" />
        </button>

        {/* Simulation Days Display */}
        <div className="px-3 py-1 rounded-xl bg-space-900 border border-white/5 font-mono text-[11px] text-slate-300">
          <span className="text-sky-400 font-bold">{Math.round(simulationDays)}d</span>
          <span className="text-slate-500 mx-1">•</span>
          <span className="text-slate-400">{earthYears} yr</span>
        </div>

        {/* Speed Multipliers */}
        <div className="hidden sm:flex items-center space-x-1 pl-1">
          {speeds.map((s) => (
            <button
              key={s}
              onClick={() => onChangeSpeed(s)}
              className={`px-2 py-1 rounded-lg text-[10px] font-mono transition-all ${
                speedMultiplier === s
                  ? 'bg-sky-500 text-white font-bold shadow-md shadow-sky-500/20'
                  : 'bg-white/5 text-slate-400 hover:bg-white/10 hover:text-slate-200'
              }`}
            >
              {s}x
            </button>
          ))}
        </div>
      </div>

      {/* 2. Visual Layer Toggles */}
      <div className="flex items-center space-x-1.5">
        {/* Toggle Orbits */}
        <button
          onClick={onToggleOrbits}
          className={`p-2 rounded-xl border transition-all flex items-center space-x-1 ${
            showOrbits
              ? 'bg-purple-500/20 border-purple-400/40 text-purple-300'
              : 'bg-white/5 border-white/10 text-slate-400'
          }`}
          title="Toggle Orbit Trajectories"
        >
          <Orbit className="w-3.5 h-3.5" />
          <span className="hidden md:inline text-[11px]">Orbits</span>
        </button>

        {/* Toggle Labels */}
        <button
          onClick={onToggleLabels}
          className={`p-2 rounded-xl border transition-all flex items-center space-x-1 ${
            showLabels
              ? 'bg-sky-500/20 border-sky-400/40 text-sky-300'
              : 'bg-white/5 border-white/10 text-slate-400'
          }`}
          title="Toggle Planet Labels"
        >
          <Eye className="w-3.5 h-3.5" />
          <span className="hidden md:inline text-[11px]">Labels</span>
        </button>

        {/* Toggle Grid */}
        <button
          onClick={onToggleGrid}
          className={`p-2 rounded-xl border transition-all flex items-center space-x-1 ${
            showGrid
              ? 'bg-indigo-500/20 border-indigo-400/40 text-indigo-300'
              : 'bg-white/5 border-white/10 text-slate-400'
          }`}
          title="Toggle Ecliptic Plane Grid"
        >
          <Grid className="w-3.5 h-3.5" />
          <span className="hidden md:inline text-[11px]">Grid</span>
        </button>

        {/* Toggle Habitable Zone */}
        <button
          onClick={onToggleHabitableZone}
          className={`p-2 rounded-xl border transition-all flex items-center space-x-1 ${
            showHabitableZone
              ? 'bg-emerald-500/20 border-emerald-400/40 text-emerald-300'
              : 'bg-white/5 border-white/10 text-slate-400'
          }`}
          title="Toggle Circumstellar Habitable Zone"
        >
          <Shield className="w-3.5 h-3.5" />
          <span className="hidden md:inline text-[11px]">Hab Zone</span>
        </button>

        {/* Scale Notice & Toggle */}
        <ScaleNotice scaleMode={scaleMode} onToggleScaleMode={onToggleScaleMode} />
      </div>

      {/* 3. Camera & Viewport Actions */}
      <div className="flex items-center space-x-1.5">
        {/* Reset Camera */}
        <button
          onClick={onResetCamera}
          className="px-2.5 py-1.5 rounded-xl bg-white/5 border border-white/10 text-slate-300 hover:bg-white/10 hover:text-white transition-all flex items-center space-x-1"
          title="Reset Camera to Overview"
        >
          <Compass className="w-3.5 h-3.5 text-sky-400" />
          <span className="text-[11px]">Overview</span>
        </button>

        {/* Focus on Selected Target */}
        {selectedObjectName && (
          <button
            onClick={onFocusSelected}
            className="px-2.5 py-1.5 rounded-xl bg-sky-500/20 border border-sky-400/40 text-sky-300 hover:bg-sky-500/30 transition-all flex items-center space-x-1"
            title={`Focus Camera on ${selectedObjectName}`}
          >
            <Crosshair className="w-3.5 h-3.5" />
            <span className="text-[11px]">Focus {selectedObjectName}</span>
          </button>
        )}

        {/* Fullscreen Toggle */}
        <button
          onClick={onToggleFullscreen}
          className="p-2 rounded-xl bg-white/5 border border-white/10 text-slate-300 hover:bg-white/10 hover:text-white transition-all"
          title={isFullscreen ? 'Exit Fullscreen' : 'Enter Fullscreen'}
        >
          {isFullscreen ? <Minimize2 className="w-3.5 h-3.5" /> : <Maximize2 className="w-3.5 h-3.5" />}
        </button>
      </div>
    </div>
  );
};
