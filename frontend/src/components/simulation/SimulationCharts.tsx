import React, { useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
  ScatterChart,
  Scatter,
  ZAxis
} from 'recharts';
import { SimulationResult } from '../../types/astronomy';
import { Activity, Gauge, TrendingUp, Shuffle, Compass } from 'lucide-react';

interface SimulationChartsProps {
  simulationData: SimulationResult;
}

export const SimulationCharts: React.FC<SimulationChartsProps> = ({ simulationData }) => {
  const [activeTab, setActiveTab] = useState<'energy' | 'position' | 'velocity' | 'distance' | 'trajectory'>('energy');

  // Format data for Position vs Time
  const positionTimeData = (simulationData.times || []).map((t, idx) => {
    const entry: Record<string, any> = { time: t };
    simulationData.bodies.forEach((b) => {
      const dist = b.distances_from_center ? b.distances_from_center[idx] : null;
      if (dist !== null && dist !== undefined) {
        entry[b.name] = dist;
      }
    });
    return entry;
  });

  // Format data for Velocity vs Time
  const velocityTimeData = (simulationData.times || []).map((t, idx) => {
    const entry: Record<string, any> = { time: t };
    simulationData.bodies.forEach((b) => {
      const spd = b.speeds ? b.speeds[idx] : null;
      if (spd !== null && spd !== undefined) {
        entry[b.name] = spd;
      }
    });
    return entry;
  });

  // Pairwise distance options
  const pairwiseList = simulationData.pairwise_distances || [];
  const [selectedPairIndex, setSelectedPairIndex] = useState(0);
  const currentPair = pairwiseList[selectedPairIndex] || null;

  return (
    <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-6">
      {/* Header & Tabs */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-white/10 pb-4">
        <div>
          <h3 className="text-base font-bold text-white flex items-center space-x-2">
            <TrendingUp className="w-5 h-5 text-sky-400" />
            <span>Astrophysical Telemetry & Numerical Dynamics</span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Real-time quantitative analysis derived from {simulationData.engine_used}
          </p>
        </div>

        {/* Tab Buttons */}
        <div className="flex flex-wrap items-center gap-1.5 p-1 rounded-2xl bg-space-950/80 border border-white/10">
          <button
            onClick={() => setActiveTab('energy')}
            className={`px-3 py-1.5 rounded-xl text-xs font-medium flex items-center space-x-1.5 transition-all ${
              activeTab === 'energy'
                ? 'bg-sky-500 text-white font-bold shadow-md shadow-sky-500/20'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Activity className="w-3.5 h-3.5" />
            <span>Energy Drift</span>
          </button>

          <button
            onClick={() => setActiveTab('position')}
            className={`px-3 py-1.5 rounded-xl text-xs font-medium flex items-center space-x-1.5 transition-all ${
              activeTab === 'position'
                ? 'bg-sky-500 text-white font-bold shadow-md shadow-sky-500/20'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Compass className="w-3.5 h-3.5" />
            <span>Position r(t)</span>
          </button>

          <button
            onClick={() => setActiveTab('velocity')}
            className={`px-3 py-1.5 rounded-xl text-xs font-medium flex items-center space-x-1.5 transition-all ${
              activeTab === 'velocity'
                ? 'bg-sky-500 text-white font-bold shadow-md shadow-sky-500/20'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Gauge className="w-3.5 h-3.5" />
            <span>Velocity v(t)</span>
          </button>

          {pairwiseList.length > 0 && (
            <button
              onClick={() => setActiveTab('distance')}
              className={`px-3 py-1.5 rounded-xl text-xs font-medium flex items-center space-x-1.5 transition-all ${
                activeTab === 'distance'
                  ? 'bg-sky-500 text-white font-bold shadow-md shadow-sky-500/20'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Shuffle className="w-3.5 h-3.5" />
              <span>Inter-Body Distance</span>
            </button>
          )}

          <button
            onClick={() => setActiveTab('trajectory')}
            className={`px-3 py-1.5 rounded-xl text-xs font-medium flex items-center space-x-1.5 transition-all ${
              activeTab === 'trajectory'
                ? 'bg-sky-500 text-white font-bold shadow-md shadow-sky-500/20'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <span>2D Orbit Plan</span>
          </button>
        </div>
      </div>

      {/* Tab 1: Energy Drift & Conservation */}
      {activeTab === 'energy' && (
        <div className="space-y-3">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between text-xs text-slate-300 gap-2">
            <div>
              <span>Hamiltonian Total Mechanical Energy Conservation: </span>
              <strong className="text-emerald-400 font-mono">
                ΔE / |E₀| ≤ {simulationData.max_energy_error.toExponential(3)}
              </strong>
            </div>
            <div className="flex items-center space-x-4 font-mono text-[11px] text-slate-400">
              <span>E₀: {simulationData.initial_energy.toFixed(6)}</span>
              <span>Ef: {simulationData.final_energy.toFixed(6)}</span>
            </div>
          </div>

          <div className="h-64 w-full bg-space-950/40 rounded-2xl p-2 border border-white/5">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={simulationData.energy_drift_series}>
                <XAxis dataKey="time" stroke="#64748b" fontSize={11} tickFormatter={(v) => `${Number(v).toFixed(2)}y`} />
                <YAxis
                  stroke="#64748b"
                  fontSize={11}
                  domain={['auto', 'auto']}
                  tickFormatter={(v) => Number(v).toExponential(1)}
                />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '12px' }}
                  labelFormatter={(v) => `Time: ${Number(v).toFixed(4)} years`}
                  formatter={(val: any) => [`${Number(val).toExponential(4)}`, 'Relative Error (ΔE/E₀)']}
                />
                <Legend wrapperStyle={{ fontSize: '11px' }} />
                <Line type="monotone" name="Energy Error (ΔE/|E₀|)" dataKey="energy_error" stroke="#10b981" dot={false} strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Tab 2: Position vs Time */}
      {activeTab === 'position' && (
        <div className="space-y-3">
          <div className="text-xs text-slate-300">
            <span>Radial separation from primary central body / coordinate origin over time (in AU or normalized units):</span>
          </div>

          <div className="h-64 w-full bg-space-950/40 rounded-2xl p-2 border border-white/5">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={positionTimeData}>
                <XAxis dataKey="time" stroke="#64748b" fontSize={11} tickFormatter={(v) => `${Number(v).toFixed(2)}y`} />
                <YAxis stroke="#64748b" fontSize={11} tickFormatter={(v) => `${Number(v).toFixed(2)} AU`} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '12px' }}
                  labelFormatter={(v) => `Time: ${Number(v).toFixed(4)} years`}
                />
                <Legend wrapperStyle={{ fontSize: '11px' }} />
                {simulationData.bodies.map((b) => (
                  <Line
                    key={b.id}
                    type="monotone"
                    name={`${b.name} (r)`}
                    dataKey={b.name}
                    stroke={b.color || '#38bdf8'}
                    dot={false}
                    strokeWidth={1.8}
                  />
                ))}
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Tab 3: Velocity vs Time */}
      {activeTab === 'velocity' && (
        <div className="space-y-3">
          <div className="text-xs text-slate-300">
            <span>Instantaneous orbital speed ||v(t)|| over time (in AU/year or normalized units):</span>
          </div>

          <div className="h-64 w-full bg-space-950/40 rounded-2xl p-2 border border-white/5">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={velocityTimeData}>
                <XAxis dataKey="time" stroke="#64748b" fontSize={11} tickFormatter={(v) => `${Number(v).toFixed(2)}y`} />
                <YAxis stroke="#64748b" fontSize={11} tickFormatter={(v) => `${Number(v).toFixed(2)} AU/yr`} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '12px' }}
                  labelFormatter={(v) => `Time: ${Number(v).toFixed(4)} years`}
                />
                <Legend wrapperStyle={{ fontSize: '11px' }} />
                {simulationData.bodies.map((b) => (
                  <Line
                    key={b.id}
                    type="monotone"
                    name={`${b.name} (Speed)`}
                    dataKey={b.name}
                    stroke={b.color || '#38bdf8'}
                    dot={false}
                    strokeWidth={1.8}
                  />
                ))}
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Tab 4: Pairwise Inter-Body Distances */}
      {activeTab === 'distance' && currentPair && (
        <div className="space-y-3">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs text-slate-300">
            <div className="flex items-center space-x-2">
              <span>Select Inter-Body Pair:</span>
              <select
                value={selectedPairIndex}
                onChange={(e) => setSelectedPairIndex(parseInt(e.target.value, 10))}
                className="bg-space-900 border border-white/10 rounded-xl px-3 py-1 text-xs text-white"
              >
                {pairwiseList.map((pair, idx) => (
                  <option key={pair.pair_id} value={idx}>
                    {pair.pair_name}
                  </option>
                ))}
              </select>
            </div>
            <div className="flex items-center space-x-4 font-mono text-[11px] text-slate-400">
              <span>Min: <strong className="text-sky-400">{currentPair.min_distance.toFixed(5)} AU</strong></span>
              <span>Max: <strong className="text-amber-400">{currentPair.max_distance.toFixed(5)} AU</strong></span>
            </div>
          </div>

          <div className="h-64 w-full bg-space-950/40 rounded-2xl p-2 border border-white/5">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={currentPair.series}>
                <XAxis dataKey="time" stroke="#64748b" fontSize={11} tickFormatter={(v) => `${Number(v).toFixed(2)}y`} />
                <YAxis stroke="#64748b" fontSize={11} tickFormatter={(v) => `${Number(v).toFixed(3)} AU`} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '12px' }}
                  labelFormatter={(v) => `Time: ${Number(v).toFixed(4)} years`}
                  formatter={(val: any) => [`${Number(val).toFixed(5)} AU`, currentPair.pair_name]}
                />
                <Line type="monotone" name={currentPair.pair_name} dataKey="distance" stroke="#38bdf8" dot={false} strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Tab 5: 2D Orbit Plan Projection (X vs Y) */}
      {activeTab === 'trajectory' && (
        <div className="space-y-3">
          <div className="text-xs text-slate-300">
            <span>2D Orbital Plane Projection (X vs Y in AU or normalized coordinates):</span>
          </div>

          <div className="h-64 w-full bg-space-950/40 rounded-2xl p-2 border border-white/5">
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart margin={{ top: 10, right: 10, bottom: 10, left: 10 }}>
                <XAxis
                  type="number"
                  dataKey="x"
                  name="X"
                  stroke="#64748b"
                  fontSize={11}
                  tickFormatter={(v) => `${v.toFixed(1)}`}
                />
                <YAxis
                  type="number"
                  dataKey="y"
                  name="Y"
                  stroke="#64748b"
                  fontSize={11}
                  tickFormatter={(v) => `${v.toFixed(1)}`}
                />
                <ZAxis range={[15, 15]} />
                <Tooltip
                  cursor={{ strokeDasharray: '3 3' }}
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '12px' }}
                  formatter={(val: any, name: any) => [`${Number(val).toFixed(4)}`, name]}
                />
                <Legend wrapperStyle={{ fontSize: '11px' }} />
                {simulationData.bodies.map((b) => {
                  const pts = (b.trajectory || []).map((pt) => ({ x: pt[0], y: pt[1] }));
                  return (
                    <Scatter
                      key={b.id}
                      name={b.name}
                      data={pts}
                      fill={b.color || '#38bdf8'}
                      line={{ stroke: b.color || '#38bdf8', strokeWidth: 1.5 }}
                      shape="circle"
                    />
                  );
                })}
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  );
};
