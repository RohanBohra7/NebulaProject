import React from 'react';
import { SimulationResult, SimulationScenarioHeader } from '../../types/astronomy';
import { ShieldCheck, Info, Cpu, AlertTriangle, BookOpen, Clock, Hash } from 'lucide-react';

interface ScientificTransparencyPanelProps {
  scenario: SimulationScenarioHeader | null;
  result: SimulationResult | null;
}

export const ScientificTransparencyPanel: React.FC<ScientificTransparencyPanelProps> = ({
  scenario,
  result
}) => {
  const reproducibility = result?.reproducibility;
  const assumptions = reproducibility?.assumptions || scenario?.assumptions || [
    'Point-mass Newtonian universal gravitation.',
    'Isolated N-body gravitational interaction without external drag.',
    'Non-relativistic kinematics (post-Newtonian corrections omitted).'
  ];
  const units = reproducibility?.units || scenario?.units || {
    distance: 'AU (Astronomical Units)',
    mass: 'M_sun (Solar Masses)',
    time: 'years',
    velocity: 'AU/year'
  };

  const initialConditions = reproducibility?.initial_conditions || [];

  return (
    <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-white/10 pb-4">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 rounded-2xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white">Scientific Transparency & Methodology</h3>
            <p className="text-xs text-slate-400">
              Rigorous physical assumptions, integrator specifications, and reproducibility metadata
            </p>
          </div>
        </div>
        <span className="text-[11px] font-mono px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-300 border border-emerald-500/20">
          Open Science Telemetry
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
        {/* Left Column: Integrator Specs & Physical Assumptions */}
        <div className="space-y-4">
          {/* Integrator Method Card */}
          <div className="p-4 rounded-2xl bg-space-950/60 border border-white/5 space-y-2">
            <div className="flex items-center space-x-2 text-xs font-semibold text-sky-400">
              <Cpu className="w-4 h-4" />
              <span>Numerical Integration Engine</span>
            </div>
            <div className="space-y-1.5 text-xs text-slate-300">
              <div className="flex justify-between">
                <span className="text-slate-400">Engine / Solver:</span>
                <span className="font-mono text-white font-bold">{result?.engine_used || 'REBOUND IAS15 / WHFast'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Integrator Algorithm:</span>
                <span className="font-mono text-indigo-300 uppercase">{result?.integrator || 'IAS15'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Output Sampling Steps:</span>
                <span className="font-mono text-white">{result?.steps_computed || 150} snapshots</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Effective Timestep (Δt):</span>
                <span className="font-mono text-sky-400">
                  {reproducibility?.parameters?.timestep
                    ? `${Number(reproducibility.parameters.timestep).toFixed(5)} ${reproducibility.parameters.timestep_unit}`
                    : 'Adaptive (IAS15 Gauss-Radau)'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Total Duration (ΔT):</span>
                <span className="font-mono text-white">
                  {result?.total_time_years} {reproducibility?.parameters?.duration_unit || 'years'}
                </span>
              </div>
            </div>
          </div>

          {/* Physical Assumptions List */}
          <div className="p-4 rounded-2xl bg-space-950/60 border border-white/5 space-y-2">
            <div className="flex items-center space-x-2 text-xs font-semibold text-amber-400">
              <BookOpen className="w-4 h-4" />
              <span>Physical Assumptions</span>
            </div>
            <ul className="space-y-1.5 text-xs text-slate-300">
              {assumptions.map((assump, idx) => (
                <li key={idx} className="flex items-start space-x-2">
                  <span className="text-sky-400 mt-0.5">•</span>
                  <span className="leading-relaxed">{assump}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Units System */}
          <div className="p-4 rounded-2xl bg-space-950/60 border border-white/5 space-y-2">
            <div className="flex items-center space-x-2 text-xs font-semibold text-purple-400">
              <Hash className="w-4 h-4" />
              <span>Astronomical Units Convention</span>
            </div>
            <div className="grid grid-cols-2 gap-2 text-xs font-mono">
              {Object.entries(units).map(([key, val]) => (
                <div key={key} className="p-2 rounded-xl bg-white/5">
                  <span className="text-slate-400 block capitalize text-[10px]">{key}</span>
                  <span className="text-slate-200">{val}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column: Initial Conditions Table & Scientific Limitations */}
        <div className="space-y-4">
          {/* Initial Conditions Snapshot */}
          <div className="p-4 rounded-2xl bg-space-950/60 border border-white/5 space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2 text-xs font-semibold text-emerald-400">
                <Clock className="w-4 h-4" />
                <span>Initial Conditions Snapshot (t = 0)</span>
              </div>
              <span className="text-[10px] font-mono text-slate-400">Cartesian State Vectors</span>
            </div>

            <div className="overflow-x-auto max-h-48 scrollbar-thin">
              <table className="w-full text-[11px] text-left border-collapse">
                <thead>
                  <tr className="border-b border-white/10 text-slate-400 font-mono">
                    <th className="py-1 px-2">Body</th>
                    <th className="py-1 px-2">Mass (M☉)</th>
                    <th className="py-1 px-2">r₀ (x, y, z) [AU]</th>
                    <th className="py-1 px-2">v₀ (vx, vy, vz) [AU/yr]</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5 font-mono text-slate-300">
                  {(initialConditions.length > 0 ? initialConditions : scenario?.bodies || []).map((b: any) => {
                    const pos = b.position || [b.x, b.y, b.z];
                    const vel = b.velocity || [b.vx, b.vy, b.vz];
                    return (
                      <tr key={b.id} className="hover:bg-white/5">
                        <td className="py-1 px-2 text-white font-semibold font-sans">{b.name}</td>
                        <td className="py-1 px-2 text-sky-400">{Number(b.mass).toExponential(3)}</td>
                        <td className="py-1 px-2 text-slate-300">
                          [{pos[0]?.toFixed(2)}, {pos[1]?.toFixed(2)}, {pos[2]?.toFixed(2)}]
                        </td>
                        <td className="py-1 px-2 text-slate-300">
                          [{vel[0]?.toFixed(2)}, {vel[1]?.toFixed(2)}, {vel[2]?.toFixed(2)}]
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>

          {/* Scientific Limitations & Disclaimer Card */}
          <div className="p-4 rounded-2xl bg-rose-500/10 border border-rose-500/20 space-y-2">
            <div className="flex items-center space-x-2 text-xs font-bold text-rose-300">
              <AlertTriangle className="w-4 h-4 flex-shrink-0" />
              <span>Scientific Limitations & Lyapunov Chaos Horizon</span>
            </div>
            <p className="text-xs text-rose-200/90 leading-relaxed">
              <strong>Never claim that the simulation perfectly reproduces reality:</strong> Classical N-body
              gravitational simulations are subject to machine-precision floating-point roundoff errors, numerical
              integrator discretization drift, and physical chaos horizons (positive Lyapunov exponents in multi-body
              interactions). Small uncertainties in initial conditions exponentially diverge over orbital timescales.
            </p>
          </div>

          {/* Reproducibility Hash & Software Versions */}
          {reproducibility?.software_version && (
            <div className="p-3 rounded-2xl bg-space-950/60 border border-white/5 flex flex-wrap items-center justify-between gap-2 text-[11px] font-mono text-slate-400">
              <span>REBOUND: <strong className="text-white">{reproducibility.software_version.rebound}</strong></span>
              <span>NumPy: <strong className="text-white">{reproducibility.software_version.numpy}</strong></span>
              <span>Python: <strong className="text-white">{reproducibility.software_version.python}</strong></span>
              <span>Timestamp: <strong className="text-sky-400">{reproducibility.timestamp.slice(0, 19)}Z</strong></span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
