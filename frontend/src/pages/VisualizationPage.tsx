import React, { useEffect, useState, useMemo, useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';
import { fetchObjects } from '../services/api';
import { AstronomicalObject } from '../types/astronomy';
import { useMode } from '../context/ModeContext';
import { SolarSystemCanvas } from '../components/visualization/SolarSystemCanvas';
import { ObjectInspectorPanel } from '../components/visualization/ObjectInspectorPanel';
import {
  Orbit,
  Sparkles,
  GraduationCap,
  Cpu,
  Compass,
  Info,
  CheckCircle2,
  Layers,
} from 'lucide-react';

export const VisualizationPage: React.FC = () => {
  const { mode } = useMode();
  const [searchParams, setSearchParams] = useSearchParams();
  const targetId = searchParams.get('target');

  const [objects, setObjects] = useState<AstronomicalObject[]>([]);
  const [systemFilter, setSystemFilter] = useState<'solar' | 'trappist'>('solar');
  const [selectedObject, setSelectedObject] = useState<AstronomicalObject | null>(null);
  const [loading, setLoading] = useState(true);

  // Live telemetry state from 3D animation loop
  const [liveState, setLiveState] = useState<{
    x: number;
    y: number;
    z: number;
    trueAnomalyDeg: number;
    currentDistanceAU: number;
    instantaneousVelocityKmS: number;
  } | null>(null);

  const [focusTrigger, setFocusTrigger] = useState(0);

  const handleFocusCamera = useCallback(() => {
    setFocusTrigger((prev) => prev + 1);
  }, []);

  useEffect(() => {
    setLoading(true);
    fetchObjects()
      .then((data) => {
        setObjects(data);
        if (targetId) {
          const targetObj = data.find((o) => o.id.toLowerCase() === targetId.toLowerCase());
          if (targetObj) {
            setSelectedObject(targetObj);
            if (targetObj.id.startsWith('trappist')) {
              setSystemFilter('trappist');
            } else {
              setSystemFilter('solar');
            }
            return;
          }
        }
        // Default selection to Earth
        const earth = data.find((o) => o.id === 'earth');
        if (earth) setSelectedObject(earth);
      })
      .finally(() => setLoading(false));
  }, [targetId]);

  // Handle system switch
  const handleSystemChange = (sys: 'solar' | 'trappist') => {
    setSystemFilter(sys);
    if (sys === 'solar') {
      const earth = objects.find((o) => o.id === 'earth');
      if (earth) setSelectedObject(earth);
    } else {
      const trapE = objects.find((o) => o.id === 'trappist-1e') || objects.find((o) => o.id.startsWith('trappist'));
      if (trapE) setSelectedObject(trapE);
    }
  };

  // Filter objects for the active planetary system
  const displayedObjects = useMemo(() => {
    if (systemFilter === 'trappist') {
      return objects.filter((o) => o.id.startsWith('trappist'));
    }
    // Solar System: Sun, Mercury, Venus, Earth, Moon, Mars, Jupiter, Saturn, Uranus, Neptune
    const solarIds = [
      'sun',
      'mercury',
      'venus',
      'earth',
      'moon',
      'mars',
      'jupiter',
      'saturn',
      'uranus',
      'neptune',
    ];
    return objects.filter(
      (o) => solarIds.includes(o.id) || (o.parent_body_id === 'sun' || o.parent_body_id === 'earth')
    );
  }, [objects, systemFilter]);

  // Core quick selector list
  const quickSelectorList = useMemo(() => {
    if (systemFilter === 'solar') {
      const order = ['sun', 'mercury', 'venus', 'earth', 'moon', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune'];
      return order
        .map((id) => displayedObjects.find((o) => o.id === id))
        .filter((o): o is AstronomicalObject => Boolean(o));
    }
    return displayedObjects;
  }, [displayedObjects, systemFilter]);

  const handleSelectObject = useCallback(
    (obj: AstronomicalObject) => {
      setSelectedObject(obj);
      setSearchParams({ target: obj.id });
    },
    [setSearchParams]
  );

  const handleLiveStateUpdate = useCallback(
    (
      objId: string,
      state: {
        x: number;
        y: number;
        z: number;
        trueAnomalyDeg: number;
        currentDistanceAU: number;
        instantaneousVelocityKmS: number;
      }
    ) => {
      if (selectedObject && selectedObject.id === objId) {
        setLiveState(state);
      }
    },
    [selectedObject]
  );

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-sky-500/10 text-sky-300 border border-sky-400/20 text-xs font-mono mb-2">
            <Orbit className="w-3.5 h-3.5" />
            <span>Interactive 3D Keplerian Visualizer • React Three Fiber & Drei Engine</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            3D Planetary Orbit Visualizer
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Simulate and explore true Keplerian orbital mechanics with non-linear scale adaptations.
          </p>
        </div>

        {/* System Switcher */}
        <div className="flex items-center space-x-2 bg-space-900 border border-white/10 rounded-2xl p-1 text-xs shadow-lg">
          <button
            onClick={() => handleSystemChange('solar')}
            className={`px-3.5 py-2 rounded-xl transition-all font-semibold flex items-center space-x-1.5 ${
              systemFilter === 'solar'
                ? 'bg-sky-500 text-white shadow-md shadow-sky-500/20'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <Compass className="w-3.5 h-3.5" />
            <span>Solar System (10 Worlds)</span>
          </button>
          <button
            onClick={() => handleSystemChange('trappist')}
            className={`px-3.5 py-2 rounded-xl transition-all font-semibold flex items-center space-x-1.5 ${
              systemFilter === 'trappist'
                ? 'bg-purple-600 text-white shadow-md shadow-purple-600/20'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <Orbit className="w-3.5 h-3.5" />
            <span>TRAPPIST-1 Resonant</span>
          </button>
        </div>
      </div>

      {/* Quick Celestial Body Selector Bar */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-thin">
        <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider flex-shrink-0 pl-1">
          Quick Target:
        </span>
        {quickSelectorList.map((obj) => {
          const isSel = selectedObject?.id === obj.id;
          return (
            <button
              key={obj.id}
              onClick={() => handleSelectObject(obj)}
              className={`px-3 py-1.5 rounded-xl border text-xs font-mono transition-all flex items-center space-x-1.5 flex-shrink-0 ${
                isSel
                  ? 'bg-sky-500/25 border-sky-400 text-white font-bold shadow-md shadow-sky-500/20 scale-105'
                  : 'bg-space-900/80 border-white/5 text-slate-300 hover:bg-white/10 hover:border-white/20'
              }`}
            >
              <span
                className="w-2 h-2 rounded-full"
                style={{ backgroundColor: obj.color_hex || '#38bdf8' }}
              />
              <span>{obj.name}</span>
            </button>
          );
        })}
      </div>

      {/* Primary 3D Viewport */}
      <div className="w-full h-[640px]">
        {loading ? (
          <div className="w-full h-full rounded-3xl glass-panel border border-white/10 flex flex-col items-center justify-center space-y-3">
            <div className="w-10 h-10 border-4 border-sky-500 border-t-transparent rounded-full animate-spin" />
            <p className="text-xs font-mono text-slate-400">Loading empirical astronomical telemetry...</p>
          </div>
        ) : (
          <SolarSystemCanvas
            objects={displayedObjects}
            selectedObjectId={selectedObject?.id}
            onSelectObject={handleSelectObject}
            focusTrigger={focusTrigger}
            onLiveStateUpdate={handleLiveStateUpdate}
          />
        )}
      </div>

      {/* Inspection & Mode Adaptive Telemetry Section */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Column: Mode-Adaptive Scientific Guidance */}
        <div className="lg:col-span-5 space-y-4">
          <div className="p-6 rounded-3xl glass-panel border border-white/10 space-y-4">
            <div className="flex items-center space-x-2">
              {mode === 'citizen' && <Sparkles className="w-5 h-5 text-purple-400" />}
              {mode === 'student' && <GraduationCap className="w-5 h-5 text-amber-400" />}
              {mode === 'researcher' && <Cpu className="w-5 h-5 text-sky-400" />}
              <h3 className="text-base font-bold text-white">
                {mode === 'citizen'
                  ? 'Cosmic Exploration Guide'
                  : mode === 'student'
                  ? "Kepler's Laws of Planetary Motion"
                  : 'Astrometric Reference Frame & Physics'}
              </h3>
            </div>

            {mode === 'citizen' && (
              <div className="space-y-3 text-xs text-slate-300 leading-relaxed font-sans">
                <p>
                  Welcome to the interactive Solar System visualizer! You can click any world to track it, scroll your mouse wheel to zoom into planetary rings, and drag to change your perspective.
                </p>
                <div className="p-3.5 rounded-2xl bg-purple-500/10 border border-purple-500/20 space-y-2">
                  <div className="font-semibold text-purple-200 flex items-center space-x-1.5">
                    <CheckCircle2 className="w-4 h-4 text-purple-400" />
                    <span>Citizen Stargazer Tip:</span>
                  </div>
                  <p className="text-slate-300 text-[11px]">
                    Use the <strong>Speed Multipliers (1x – 500x)</strong> to watch the inner planets race around the Sun while outer giants like Jupiter and Saturn glide majestically. Notice how the Moon faithfully orbits Earth!
                  </p>
                </div>
              </div>
            )}

            {mode === 'student' && (
              <div className="space-y-3 text-xs text-slate-300 leading-relaxed font-sans">
                <p>
                  Planets follow Johannes Kepler's three fundamental empirical laws of orbital motion:
                </p>
                <ul className="space-y-2 pl-2">
                  <li className="flex items-start space-x-2">
                    <span className="text-amber-400 font-bold font-mono">1.</span>
                    <span><strong>First Law:</strong> Planetary orbits are ellipses with the Sun at one focal point: <em>r = a(1 - e²) / (1 + e cos ν)</em>.</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-amber-400 font-bold font-mono">2.</span>
                    <span><strong>Second Law:</strong> A line segment joining a planet and the Sun sweeps out equal areas during equal intervals of time: <em>dA/dt = const</em>.</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-amber-400 font-bold font-mono">3.</span>
                    <span><strong>Third Law (Harmonic):</strong> The square of orbital period is proportional to the cube of semi-major axis: <em>P² ∝ a³</em>.</span>
                  </li>
                </ul>

                <div className="p-3.5 rounded-2xl bg-amber-500/10 border border-amber-500/20 text-[11px] text-amber-200 space-y-1">
                  <p className="font-semibold">Observation Activity:</p>
                  <p className="text-slate-300">
                    Switch between <strong>Mercury (88d)</strong> and <strong>Neptune (165yr)</strong>. Notice how orbital velocity drops from 47.4 km/s at 0.39 AU to 5.4 km/s at 30 AU!
                  </p>
                </div>
              </div>
            )}

            {mode === 'researcher' && (
              <div className="space-y-3 text-xs text-slate-300 leading-relaxed font-sans">
                <p>
                  Orbital states are parameterized via classical Keplerian orbital elements (a, e, i, Ω, ω, ν). Real-time state propagation integrates the mean anomaly M(t) = n(t - t₀) and numerically solves Kepler's transcendental equation:
                </p>
                <div className="p-3 rounded-xl bg-space-900 border border-white/5 font-mono text-[11px] text-sky-300 text-center">
                  {"M = E - e·sin(E)  ⟹  ν = 2·arctan(√((1+e)/(1-e))·tan(E/2))"}
                </div>
                <div className="p-3.5 rounded-2xl bg-sky-500/10 border border-sky-400/20 text-[11px] text-sky-200 space-y-1">
                  <p className="font-semibold">Vis-Viva Orbital Energy Conservation:</p>
                  <p className="text-slate-300 font-mono text-[10px]">
                    {"v(r) = √(μ·(2/r - 1/a)),  μ = GM_☉ ≈ 1.327 × 10¹¹ km³/s²"}
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Interactive Object Inspector Panel */}
        <div className="lg:col-span-7">
          <ObjectInspectorPanel
            object={selectedObject}
            mode={mode}
            onFocusCamera={handleFocusCamera}
            onClose={() => setSelectedObject(null)}
            liveState={liveState}
          />
        </div>
      </div>
    </div>
  );
};
