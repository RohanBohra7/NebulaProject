import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  fetchSimulationScenarios,
  fetchScenarioDetails,
  createSimulation,
  runSimulation
} from '../services/api';
import { SimulationScenarioHeader, SimulationResult } from '../types/astronomy';
import { NBodyCanvas } from '../components/simulation/NBodyCanvas';
import { SimulationCharts } from '../components/simulation/SimulationCharts';
import { ScientificTransparencyPanel } from '../components/simulation/ScientificTransparencyPanel';
import {
  Atom,
  Play,
  RotateCcw,
  Sliders,
  AlertCircle,
  Activity,
  Layers,
  Zap,
  CheckCircle2,
  Users,
  Compass,
  SquareCheck,
  Square,
  Bot
} from 'lucide-react';

export const SimulationPage: React.FC = () => {
  const [scenarios, setScenarios] = useState<SimulationScenarioHeader[]>([]);
  const [selectedScenarioId, setSelectedScenarioId] = useState('sun_earth');
  const [scenarioDetail, setScenarioDetail] = useState<any | null>(null);

  // Selected body IDs for filtering
  const [selectedBodyIds, setSelectedBodyIds] = useState<string[]>([]);

  // Simulation Parameters
  const [integrator, setIntegrator] = useState('ias15');
  const [numSteps, setNumSteps] = useState(150);
  const [timeYears, setTimeYears] = useState(1.0);
  const [customTimestepDays, setCustomTimestepDays] = useState<number | null>(null);

  // Results & Execution state
  const [simulationResult, setSimulationResult] = useState<SimulationResult | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch scenarios on mount
  useEffect(() => {
    fetchSimulationScenarios().then((data) => {
      setScenarios(data);
      if (data.length > 0) {
        // Default to Sun + Earth or first scenario
        const defScen = data.find((s) => s.id === 'sun_earth') || data[0];
        loadScenario(defScen.id);
      }
    });
  }, []);

  const loadScenario = async (scenId: string) => {
    setSelectedScenarioId(scenId);
    setError(null);
    try {
      const detail = await fetchScenarioDetails(scenId);
      setScenarioDetail(detail);
      const bodies = detail.bodies || [];
      setSelectedBodyIds(bodies.map((b: any) => b.id));
      setTimeYears(detail.default_time_years || 1.0);
      setIntegrator(detail.recommended_integrator || 'ias15');

      // Auto-run simulation for the newly chosen scenario
      executeSimulation(
        scenId,
        detail.recommended_integrator || 'ias15',
        detail.default_time_years || 1.0,
        150,
        bodies.map((b: any) => b.id)
      );
    } catch (e: any) {
      setError(e.message || 'Failed to load scenario details');
    }
  };

  const handleScenarioChange = (scenId: string) => {
    loadScenario(scenId);
  };

  const toggleBodySelection = (bodyId: string) => {
    setSelectedBodyIds((prev) => {
      if (prev.includes(bodyId)) {
        if (prev.length <= 2) {
          setError('At least 2 bodies are required for an N-body gravitational simulation.');
          return prev;
        }
        setError(null);
        return prev.filter((id) => id !== bodyId);
      } else {
        setError(null);
        return [...prev, bodyId];
      }
    });
  };

  const selectAllBodies = () => {
    if (scenarioDetail?.bodies) {
      setSelectedBodyIds(scenarioDetail.bodies.map((b: any) => b.id));
      setError(null);
    }
  };

  const executeSimulation = async (
    scenId = selectedScenarioId,
    integ = integrator,
    tYears = timeYears,
    steps = numSteps,
    bIds = selectedBodyIds
  ) => {
    if (bIds.length < 2) {
      setError('Please select at least 2 bodies to simulate gravitational interaction.');
      return;
    }

    setIsRunning(true);
    setError(null);
    try {
      const timestepYears = customTimestepDays ? customTimestepDays / 365.25 : undefined;
      const res = await runSimulation({
        scenario_id: scenId,
        integrator: integ,
        duration: tYears,
        total_time_years: tYears,
        timestep: timestepYears,
        num_steps: steps,
        selected_bodies: bIds
      });
      setSimulationResult(res);
    } catch (e: any) {
      setError(e.message || 'Simulation execution failed.');
    } finally {
      setIsRunning(false);
    }
  };

  const currentScenario = scenarios.find((s) => s.id === selectedScenarioId) || scenarioDetail;

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-10">
      {/* Page Title & Mission Badge */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-purple-500/10 text-purple-300 border border-purple-400/20 text-xs font-mono mb-2">
            <Atom className="w-3.5 h-3.5" />
            <span>N-Body Gravitational Dynamics Engine • REBOUND IAS15 & Symplectic WHFast</span>
          </div>
          <h1 className="text-3xl font-extrabold text-white">
            N-Body Gravitational Simulation Laboratory
          </h1>
          <p className="text-sm text-slate-400 mt-1 max-w-3xl">
            Simulate mutual gravitational interactions, Keplerian orbits, multi-body resonances, and chaotic
            three-body systems with high-order Gauss-Radau and symplectic integrators.
          </p>
        </div>
      </div>

      {/* Scenario Chooser Grid */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-semibold text-slate-300 flex items-center space-x-2">
            <Layers className="w-4 h-4 text-sky-400" />
            <span>Select Scientific Scenario:</span>
          </h3>
          <span className="text-xs text-slate-400 font-mono">
            {scenarios.length} Preconfigured Scenarios
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
          {scenarios.map((scen) => (
            <button
              key={scen.id}
              onClick={() => handleScenarioChange(scen.id)}
              className={`p-4 rounded-2xl border text-left transition-all space-y-1.5 ${
                selectedScenarioId === scen.id
                  ? 'bg-sky-500/10 border-sky-400 shadow-md shadow-sky-500/15 ring-1 ring-sky-400/30'
                  : 'glass-panel border-white/5 hover:border-white/20'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-mono text-sky-400 uppercase tracking-wider">
                  {scen.mode_focus}
                </span>
                <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-white/5 text-slate-300">
                  {scen.body_count} Bodies
                </span>
              </div>
              <h4 className="text-xs font-bold text-white line-clamp-1">{scen.name}</h4>
              <p className="text-[11px] text-slate-400 line-clamp-2 leading-relaxed">
                {scen.description}
              </p>
            </button>
          ))}
        </div>
      </div>

      {/* Main Simulation Workbench */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Column: Integrator Controls & Body Selector */}
        <div className="lg:col-span-4 space-y-6">
          {/* Controls Panel */}
          <div className="p-6 rounded-3xl glass-panel border border-white/10 space-y-5">
            <h3 className="text-base font-bold text-white flex items-center space-x-2">
              <Sliders className="w-4 h-4 text-sky-400" />
              <span>Integration Parameters</span>
            </h3>

            {/* Integrator Algorithm */}
            <div className="space-y-1.5">
              <label className="text-xs text-slate-300 font-medium">Integration Method</label>
              <select
                value={integrator}
                onChange={(e) => setIntegrator(e.target.value)}
                className="w-full bg-space-900 border border-white/10 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-sky-400"
              >
                <option value="ias15">
                  REBOUND IAS15 (15th-Order Adaptive Gauss-Radau / High Precision)
                </option>
                <option value="whfast">
                  REBOUND WHFast (2nd-Order Symplectic Wisdom-Holman / Planetary)
                </option>
                <option value="leapfrog">
                  NumPy Symplectic Leapfrog (Velocity-Verlet / Phase Volume Conserving)
                </option>
              </select>
            </div>

            {/* Time Span Duration Slider */}
            <div className="space-y-1.5">
              <div className="flex justify-between text-xs text-slate-300">
                <span>Simulation Duration:</span>
                <span className="font-mono text-sky-400 font-bold">
                  {timeYears.toFixed(2)} years ({Math.round(timeYears * 365.25)} days)
                </span>
              </div>
              <input
                type="range"
                min="0.05"
                max="25.0"
                step="0.05"
                value={timeYears}
                onChange={(e) => setTimeYears(parseFloat(e.target.value))}
                className="w-full accent-sky-500"
              />
            </div>

            {/* Output Sampling Steps */}
            <div className="space-y-1.5">
              <div className="flex justify-between text-xs text-slate-300">
                <span>Output Sampling Steps:</span>
                <span className="font-mono text-sky-400 font-bold">{numSteps} snapshots</span>
              </div>
              <input
                type="range"
                min="20"
                max="500"
                step="10"
                value={numSteps}
                onChange={(e) => setNumSteps(parseInt(e.target.value, 10))}
                className="w-full accent-sky-500"
              />
            </div>

            {/* Body Selector Sub-Panel */}
            {scenarioDetail?.bodies && (
              <div className="space-y-2 pt-2 border-t border-white/10">
                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-300 font-medium flex items-center space-x-1.5">
                    <Users className="w-3.5 h-3.5 text-sky-400" />
                    <span>Select Bodies ({selectedBodyIds.length}/{scenarioDetail.bodies.length}):</span>
                  </span>
                  <button
                    onClick={selectAllBodies}
                    className="text-[11px] text-sky-400 hover:text-sky-300 underline font-mono"
                  >
                    Select All
                  </button>
                </div>

                <div className="grid grid-cols-1 gap-1.5 max-h-40 overflow-y-auto scrollbar-thin p-1 bg-space-950/60 rounded-xl border border-white/5">
                  {scenarioDetail.bodies.map((b: any) => {
                    const isSelected = selectedBodyIds.includes(b.id);
                    return (
                      <button
                        key={b.id}
                        type="button"
                        onClick={() => toggleBodySelection(b.id)}
                        className={`flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs transition-all ${
                          isSelected
                            ? 'bg-white/10 text-white font-medium'
                            : 'text-slate-500 hover:bg-white/5 hover:text-slate-300'
                        }`}
                      >
                        <div className="flex items-center space-x-2">
                          <span
                            className="w-2.5 h-2.5 rounded-full flex-shrink-0"
                            style={{ backgroundColor: b.color || '#38bdf8' }}
                          />
                          <span>{b.name}</span>
                        </div>
                        <div className="flex items-center space-x-2 font-mono text-[10px] text-slate-400">
                          <span>{Number(b.mass).toExponential(1)} M☉</span>
                          {isSelected ? (
                            <SquareCheck className="w-3.5 h-3.5 text-sky-400" />
                          ) : (
                            <Square className="w-3.5 h-3.5 text-slate-600" />
                          )}
                        </div>
                      </button>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Execute Button */}
            <button
              onClick={() => executeSimulation()}
              disabled={isRunning || selectedBodyIds.length < 2}
              className="w-full py-3 rounded-2xl bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-bold text-xs flex items-center justify-center space-x-2 shadow-lg shadow-sky-500/20 transition-all disabled:opacity-50"
            >
              <Zap className="w-4 h-4" />
              <span>{isRunning ? 'Integrating...' : 'Compute Trajectories'}</span>
            </button>

            {/* Telemetry Card */}
            {simulationResult && (
              <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-2 text-xs font-mono">
                <span className="text-[10px] text-slate-400 uppercase tracking-wider block font-sans">
                  Execution Telemetry:
                </span>
                <div className="flex justify-between text-slate-300">
                  <span>Solver Runtime:</span>
                  <span className="text-white font-bold">{simulationResult.runtime_ms} ms</span>
                </div>
                <div className="flex justify-between text-slate-300">
                  <span>Max Relative Energy Drift (ΔE/|E₀|):</span>
                  <span className="text-emerald-400 font-bold">
                    {simulationResult.max_energy_error.toExponential(3)}
                  </span>
                </div>
                <div className="flex justify-between text-slate-300">
                  <span>Bodies Simulated:</span>
                  <span className="text-white font-bold">{simulationResult.bodies.length}</span>
                </div>
                <div className="flex justify-between text-slate-300">
                  <span>Sampling Density:</span>
                  <span className="text-white font-bold">
                    {simulationResult.steps_computed} snapshots
                  </span>
                </div>

                <Link
                  to={`/ai?prompt=${encodeURIComponent(`What happened in this simulation (${simulationResult.scenario_name || scenarioDetail?.name || selectedScenarioId})? Explain this trajectory and its energy conservation.`)}`}
                  className="w-full mt-2 py-2 rounded-xl bg-purple-500/10 hover:bg-purple-500/20 text-purple-300 font-medium text-xs flex items-center justify-center space-x-1.5 border border-purple-400/30 transition-all font-sans"
                >
                  <Bot className="w-3.5 h-3.5 text-purple-400" />
                  <span>Ask Grounded AI to Interpret Run</span>
                </Link>
              </div>
            )}

            {/* Error Banner with Actionable Recovery */}
            {error && (
              <div className="p-3.5 rounded-2xl bg-rose-500/10 border border-rose-500/20 text-xs text-rose-300 space-y-1.5 animate-fadeIn">
                <div className="flex items-center space-x-2 font-semibold">
                  <AlertCircle className="w-4 h-4 flex-shrink-0 text-rose-400" />
                  <span>Simulation Parameter Notice</span>
                </div>
                <p className="text-[11px] text-slate-300">{error}</p>
                <div className="pt-1 flex items-center space-x-3">
                  <button
                    type="button"
                    onClick={selectAllBodies}
                    className="text-[11px] px-2.5 py-1 rounded-lg bg-rose-500/20 hover:bg-rose-500/30 text-rose-200 transition-colors font-mono"
                  >
                    Select All Bodies
                  </button>
                  <button
                    type="button"
                    onClick={() => setError(null)}
                    className="text-[11px] text-slate-400 hover:text-white underline font-mono"
                  >
                    Dismiss
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Right Column: 3D Visualization Canvas */}
        <div className="lg:col-span-8">
          <NBodyCanvas simulationData={simulationResult} isRunning={isRunning} />
        </div>
      </div>

      {/* Dynamic Telemetry Charts Section */}
      {simulationResult && (
        <div className="space-y-8">
          <SimulationCharts simulationData={simulationResult} />
        </div>
      )}

      {/* Scientific Transparency & Methodology Section */}
      <ScientificTransparencyPanel scenario={currentScenario} result={simulationResult} />
    </div>
  );
};
