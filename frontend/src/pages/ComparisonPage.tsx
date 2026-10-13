import React, { useEffect, useState } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { useMode } from '../context/ModeContext';
import { fetchObjects, compareObjects, chatAI } from '../services/api';
import { AstronomicalObject } from '../types/astronomy';
import {
  GitCompare,
  Plus,
  X,
  Sparkles,
  BarChart2,
  Send,
  Scale,
  Zap,
  ArrowRight,
  TrendingUp,
  Percent,
  CheckCircle,
  HelpCircle,
  Cpu,
  GraduationCap,
  Radar as RadarIcon,
  Bot
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis
} from 'recharts';
import { LoadingState, ErrorState, EmptyState } from '../components/ui';

export const ComparisonPage: React.FC = () => {
  const { mode } = useMode();
  const [searchParams, setSearchParams] = useSearchParams();
  const [allObjects, setAllObjects] = useState<AstronomicalObject[]>([]);
  const [selectedIds, setSelectedIds] = useState<string[]>(['earth', 'mars']);
  const [comparisonData, setComparisonData] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeChartTab, setActiveChartTab] = useState<'bar' | 'radar' | 'scale'>('bar');
  const [filterOnlyCommon, setFilterOnlyCommon] = useState(false);

  // AI comparative synthesis
  const [aiAnalysis, setAiAnalysis] = useState<string | null>(null);
  const [aiLoading, setAiLoading] = useState(false);

  // Initialize from searchParams (supports target, obj1/obj2, and comma-separated objects)
  useEffect(() => {
    fetchObjects().then((objs) => {
      setAllObjects(objs);
      const obj1 = searchParams.get('obj1');
      const obj2 = searchParams.get('obj2');
      const objectsParam = searchParams.get('objects');
      const targetParam = searchParams.get('target');

      if (obj1 && obj2 && objs.some((o) => o.id === obj1) && objs.some((o) => o.id === obj2)) {
        setSelectedIds([obj1, obj2]);
      } else if (objectsParam) {
        const parsed = objectsParam.split(',').map((s) => s.trim()).filter((id) => objs.some((o) => o.id === id));
        if (parsed.length >= 2) {
          setSelectedIds(parsed.slice(0, 6));
        }
      } else if (targetParam && objs.some((o) => o.id === targetParam)) {
        if (targetParam !== 'earth') {
          setSelectedIds(['earth', targetParam]);
        } else {
          setSelectedIds(['earth', 'mars']);
        }
      }
    });
  }, [searchParams]);

  useEffect(() => {
    if (selectedIds.length >= 2) {
      setLoading(true);
      setError(null);
      compareObjects(selectedIds, mode)
        .then((res) => {
          setComparisonData(res);
        })
        .catch((err) => {
          console.error(err);
          setError(err.message || 'Failed to compare celestial objects.');
        })
        .finally(() => setLoading(false));
    } else {
      setComparisonData(null);
    }
  }, [selectedIds, mode]);

  const handleSelectPreset = (ids: string[]) => {
    setSelectedIds(ids.slice(0, 4));
  };

  const handleAddObject = (id: string) => {
    if (selectedIds.includes(id) || selectedIds.length >= 4) return;
    setSelectedIds([...selectedIds, id]);
  };

  const handleRemoveObject = (id: string) => {
    if (selectedIds.length <= 2) return;
    setSelectedIds(selectedIds.filter((x) => x !== id));
  };

  const handleGenerateComparativeAI = async () => {
    if (!comparisonData) return;
    setAiLoading(true);
    const names = comparisonData.compared_objects.map((o: any) => o.name).join(' vs ');
    const prompt = `Provide a comprehensive comparative analysis contrasting ${names}. Compare their gravitational environments, atmospheric retention, and orbital mechanics from a ${mode} perspective.`;
    try {
      const res = await chatAI(prompt, mode);
      setAiAnalysis(res.response);
    } catch {
      setAiAnalysis("Comparative synthesis could not be generated.");
    } finally {
      setAiLoading(false);
    }
  };

  const presets = [
    { label: "Earth vs Mars", ids: ['earth', 'mars'] },
    { label: "Earth vs TRAPPIST-1e", ids: ['earth', 'trappist-1e'] },
    { label: "Earth vs Jupiter vs Saturn", ids: ['earth', 'jupiter', 'saturn'] },
    { label: "Sun vs Sirius A vs Betelgeuse", ids: ['sun', 'sirius-a', 'betelgeuse'] },
    { label: "Moon vs Europa vs Titan", ids: ['moon', 'europa', 'titan'] },
  ];

  // Colors for Radar Chart per object
  const palette = ['#38bdf8', '#f59e0b', '#ec4899', '#10b981'];

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-10 animate-fadeIn">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-sky-500/10 text-sky-300 border border-sky-400/20 text-xs font-mono mb-2">
            <GitCompare className="w-3.5 h-3.5" />
            <span>Multi-Target Parametric Comparison (2–4 Objects)</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Comparative Astronomical Analysis
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Evaluate physical dimensions, Keplerian orbital dynamics, and surface gravity differentials across celestial worlds.
          </p>
        </div>

        {/* Quick Presets */}
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-xs text-slate-400 font-mono">Curated Presets:</span>
          {presets.map((p, i) => (
            <button
              key={i}
              onClick={() => handleSelectPreset(p.ids)}
              className="px-2.5 py-1.5 rounded-xl bg-white/5 hover:bg-white/10 text-slate-300 border border-white/10 text-xs font-mono transition-all hover:text-white"
            >
              {p.label}
            </button>
          ))}
        </div>
      </div>

      {/* Target Selector Bar */}
      <div className="p-5 rounded-3xl glass-panel border border-white/10 space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex flex-wrap items-center gap-3">
            <span className="text-xs text-slate-400 font-mono uppercase font-bold tracking-wider">
              Selected Targets ({selectedIds.length}/4):
            </span>
            {selectedIds.map((id, idx) => {
              const obj = allObjects.find((o) => o.id === id);
              return (
                <span
                  key={id}
                  className="px-3.5 py-1.5 rounded-xl bg-space-900 border border-white/15 text-xs text-white flex items-center space-x-2 font-medium shadow-sm"
                >
                  <span
                    className="w-2.5 h-2.5 rounded-full"
                    style={{ backgroundColor: obj?.color_hex || palette[idx % palette.length] }}
                  />
                  <span>{obj?.name || id}</span>
                  {selectedIds.length > 2 && (
                    <button
                      onClick={() => handleRemoveObject(id)}
                      className="hover:text-rose-400 text-slate-400 transition-colors ml-1"
                      title="Remove object"
                    >
                      <X className="w-3.5 h-3.5" />
                    </button>
                  )}
                </span>
              );
            })}
          </div>

          {selectedIds.length < 4 && (
            <div className="flex items-center space-x-2">
              <select
                onChange={(e) => {
                  if (e.target.value) {
                    handleAddObject(e.target.value);
                    e.target.value = '';
                  }
                }}
                defaultValue=""
                className="bg-space-900 border border-white/20 rounded-xl px-3 py-1.5 text-xs text-slate-200 hover:text-white focus:outline-none focus:border-sky-400"
              >
                <option value="" disabled>+ Add Object to Compare...</option>
                {allObjects
                  .filter((o) => !selectedIds.includes(o.id))
                  .map((o) => (
                    <option key={o.id} value={o.id} className="bg-space-950 text-white">
                      {o.name} ({o.category})
                    </option>
                  ))}
              </select>
            </div>
          )}
        </div>

        {/* Mode-grounded comparative insight banner */}
        {comparisonData?.comparative_insights && (
          <div className="p-4 rounded-2xl bg-space-900/90 border border-sky-500/20 flex items-start space-x-3">
            <div className="mt-0.5">
              {mode === 'researcher' && <Cpu className="w-4 h-4 text-sky-400" />}
              {mode === 'student' && <GraduationCap className="w-4 h-4 text-amber-400" />}
              {mode === 'citizen' && <Sparkles className="w-4 h-4 text-purple-400" />}
            </div>
            <div className="space-y-1">
              <div className="flex items-center space-x-2">
                <span className="text-xs font-bold text-white capitalize">{mode} Perspective:</span>
                <span className="text-[10px] font-mono text-slate-400">Deterministic Scientific Synthesis</span>
              </div>
              <p className="text-xs text-slate-200 leading-relaxed font-sans">
                {comparisonData.comparative_insights[mode] || comparisonData.comparative_insights['citizen']}
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Main Side-by-Side Parametric Comparison Table */}
      {loading ? (
        <LoadingState message="Computing parametric comparative matrices and orbital differentials..." />
      ) : error ? (
        <ErrorState
          title="Comparative Analysis Failed"
          message={error}
          onRetry={() => {
            if (selectedIds.length >= 2) {
              setLoading(true);
              setError(null);
              compareObjects(selectedIds, mode)
                .then(setComparisonData)
                .catch((e) => setError(e.message))
                .finally(() => setLoading(false));
            }
          }}
        />
      ) : !comparisonData ? (
        <EmptyState
          title="Insufficient Celestial Targets Selected"
          description="Select at least 2 celestial objects from the dropdown or pick a curated preset above to compute side-by-side matrices."
        />
      ) : (
        <div className="p-6 sm:p-8 rounded-3xl glass-panel border border-white/10 space-y-6">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <h3 className="text-xl font-bold text-white flex items-center space-x-2">
              <Scale className="w-5 h-5 text-sky-400" />
              <span>Direct Parametric Comparison Matrix</span>
            </h3>
            <div className="flex flex-wrap items-center gap-3">
              <button
                onClick={() => setFilterOnlyCommon((prev) => !prev)}
                className={`px-3 py-1.5 rounded-xl text-xs font-mono border transition-all ${
                  filterOnlyCommon
                    ? 'bg-sky-500/20 border-sky-400 text-sky-300 font-semibold'
                    : 'bg-white/5 border-white/10 text-slate-400 hover:text-white'
                }`}
                title="Filter metrics to only show rows where all selected objects have data"
              >
                {filterOnlyCommon ? '✓ Common Properties Only' : 'Show All Properties'}
              </button>
              <span className="text-xs font-mono text-slate-400">
                Primary Reference: <strong className="text-white">{comparisonData.primary_reference}</strong>
              </span>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead className="bg-white/5 text-slate-300 border-b border-white/10">
                <tr>
                  <th className="p-3.5 font-sans font-semibold">Physical / Orbital Metric</th>
                  {comparisonData.compared_objects.map((obj: any, idx: number) => (
                    <th key={obj.id} className="p-3.5">
                      <div className="flex items-center space-x-2">
                        <span
                          className="w-2.5 h-2.5 rounded-full"
                          style={{ backgroundColor: obj.color_hex || palette[idx % palette.length] }}
                        />
                        <Link to={`/object/${obj.id}`} className="text-white font-bold hover:text-sky-300 underline">
                          {obj.name}
                        </Link>
                        {idx === 0 && (
                          <span className="text-[9px] px-1.5 py-0.2 rounded bg-sky-500/20 text-sky-300 font-normal">
                            Reference
                          </span>
                        )}
                      </div>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                <tr>
                  <td className="p-3.5 text-slate-400 font-sans">Classification</td>
                  {comparisonData.compared_objects.map((obj: any) => (
                    <td key={obj.id} className="p-3.5 text-slate-200">{obj.category}</td>
                  ))}
                </tr>
                {(!filterOnlyCommon || comparisonData.compared_objects.every((o: any) => o.mass_earth_relative != null || o.mass_kg != null)) && (
                  <tr>
                    <td className="p-3.5 text-slate-400 font-sans">Mass ($M_\oplus$ / kg)</td>
                    {comparisonData.compared_objects.map((obj: any) => (
                      <td key={obj.id} className="p-3.5 text-white font-bold">
                        {obj.mass_earth_relative !== null && obj.mass_earth_relative !== undefined
                          ? `${obj.mass_earth_relative} M⊕`
                          : obj.mass_kg ? `${obj.mass_kg.toExponential(2)} kg` : '—'}
                      </td>
                    ))}
                  </tr>
                )}
                {(!filterOnlyCommon || comparisonData.compared_objects.every((o: any) => o.radius_km != null)) && (
                  <tr>
                    <td className="p-3.5 text-slate-400 font-sans">Volumetric Mean Radius (km)</td>
                    {comparisonData.compared_objects.map((obj: any) => (
                      <td key={obj.id} className="p-3.5 text-slate-200">
                        {obj.radius_km ? `${obj.radius_km.toLocaleString()} km` : '—'}
                      </td>
                    ))}
                  </tr>
                )}
                {(!filterOnlyCommon || comparisonData.compared_objects.every((o: any) => o.surface_gravity_m_s2 != null)) && (
                  <tr>
                    <td className="p-3.5 text-slate-400 font-sans">Surface Gravity ($g$)</td>
                    {comparisonData.compared_objects.map((obj: any) => (
                      <td key={obj.id} className="p-3.5 text-slate-200">
                        {obj.surface_gravity_m_s2 ? `${obj.surface_gravity_m_s2} m/s²` : '—'}
                      </td>
                    ))}
                  </tr>
                )}
                {(!filterOnlyCommon || comparisonData.compared_objects.every((o: any) => (o.semi_major_axis_au ?? o.distance_from_sun) != null)) && (
                  <tr>
                    <td className="p-3.5 text-slate-400 font-sans">Distance from Sun / Semi-Major ($a$)</td>
                    {comparisonData.compared_objects.map((obj: any) => {
                      const dist = obj.semi_major_axis_au ?? obj.distance_from_sun;
                      return (
                        <td key={obj.id} className="p-3.5 text-slate-200">
                          {dist !== null && dist !== undefined ? `${dist} AU` : '—'}
                        </td>
                      );
                    })}
                  </tr>
                )}
                {(!filterOnlyCommon || comparisonData.compared_objects.every((o: any) => (o.orbital_period_days ?? o.orbital_period) != null)) && (
                  <tr>
                    <td className="p-3.5 text-slate-400 font-sans">Orbital Period ($P$)</td>
                    {comparisonData.compared_objects.map((obj: any) => {
                      const per = obj.orbital_period_days ?? obj.orbital_period;
                      return (
                        <td key={obj.id} className="p-3.5 text-slate-200">
                          {per ? `${per.toLocaleString()} d` : '—'}
                        </td>
                      );
                    })}
                  </tr>
                )}
                {(!filterOnlyCommon || comparisonData.compared_objects.every((o: any) => (o.surface_temperature_k ?? o.temperature) != null)) && (
                  <tr>
                    <td className="p-3.5 text-slate-400 font-sans">Surface Temperature ($T$)</td>
                    {comparisonData.compared_objects.map((obj: any) => {
                      const temp = obj.surface_temperature_k ?? obj.temperature;
                      return (
                        <td key={obj.id} className="p-3.5 text-slate-200">
                          {temp ? `${temp} K (${Math.round(temp - 273.15)} °C)` : '—'}
                        </td>
                      );
                    })}
                  </tr>
                )}
                {(!filterOnlyCommon || comparisonData.compared_objects.every((o: any) => (o.mean_orbital_velocity_km_s ?? o.orbital_velocity) != null)) && (
                  <tr>
                    <td className="p-3.5 text-slate-400 font-sans">Mean Orbital Velocity (v_orb)</td>
                    {comparisonData.compared_objects.map((obj: any) => {
                      const vel = obj.mean_orbital_velocity_km_s ?? obj.orbital_velocity;
                      return (
                        <td key={obj.id} className="p-3.5 text-slate-200">
                          {vel !== null && vel !== undefined ? `${vel} km/s` : '—'}
                        </td>
                      );
                    })}
                  </tr>
                )}
                {(!filterOnlyCommon || comparisonData.compared_objects.every((o: any) => o.mean_density_g_cm3 != null)) && (
                  <tr>
                    <td className="p-3.5 text-slate-400 font-sans">Mean Density ($\rho$)</td>
                    {comparisonData.compared_objects.map((obj: any) => (
                      <td key={obj.id} className="p-3.5 text-slate-200">
                        {obj.mean_density_g_cm3 ? `${obj.mean_density_g_cm3} g/cm³` : '—'}
                      </td>
                    ))}
                  </tr>
                )}
                {(!filterOnlyCommon || comparisonData.compared_objects.every((o: any) => o.escape_velocity_km_s != null)) && (
                  <tr>
                    <td className="p-3.5 text-slate-400 font-sans">Escape Velocity (v_esc)</td>
                    {comparisonData.compared_objects.map((obj: any) => (
                      <td key={obj.id} className="p-3.5 text-slate-200">
                        {obj.escape_velocity_km_s ? `${obj.escape_velocity_km_s} km/s` : '—'}
                      </td>
                    ))}
                  </tr>
                )}
                {(!filterOnlyCommon || comparisonData.compared_objects.every((o: any) => o.eccentricity != null)) && (
                  <tr>
                    <td className="p-3.5 text-slate-400 font-sans">Orbital Eccentricity ($e$)</td>
                    {comparisonData.compared_objects.map((obj: any) => (
                      <td key={obj.id} className="p-3.5 text-slate-200">
                        {obj.eccentricity !== null && obj.eccentricity !== undefined ? obj.eccentricity : '—'}
                      </td>
                    ))}
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Calculated Physical Ratios & Absolute Differences */}
      {comparisonData && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Calculated Relative Ratios */}
          <div className="p-6 rounded-3xl glass-panel border border-white/10 space-y-4">
            <div className="flex items-center space-x-2 text-sky-400">
              <TrendingUp className="w-5 h-5" />
              <h3 className="text-lg font-bold text-white">Calculated Multiplier Ratios</h3>
            </div>
            <p className="text-xs text-slate-400 font-mono">
              Direct physical multipliers computed relative to {comparisonData.primary_reference}:
            </p>

            {comparisonData.calculated_ratios?.length === 0 ? (
              <p className="text-xs text-slate-500 font-mono">No ratio multipliers computed.</p>
            ) : (
              <div className="space-y-4">
                {comparisonData.calculated_ratios.map((r: any, idx: number) => (
                  <div key={idx} className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-2.5">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-white font-mono">
                        {r.target_name} / {r.relative_to}
                      </span>
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-sky-500/10 text-sky-300">
                        Relative Ratio
                      </span>
                    </div>

                    <div className="grid grid-cols-2 gap-2 text-xs font-mono">
                      <div className="p-2 rounded-xl bg-white/5 flex justify-between">
                        <span className="text-slate-400">Mass:</span>
                        <span className="text-sky-300 font-bold">{r.mass_ratio !== null ? `${r.mass_ratio}x` : '—'}</span>
                      </div>
                      <div className="p-2 rounded-xl bg-white/5 flex justify-between">
                        <span className="text-slate-400">Radius:</span>
                        <span className="text-sky-300 font-bold">{r.radius_ratio !== null ? `${r.radius_ratio}x` : '—'}</span>
                      </div>
                      <div className="p-2 rounded-xl bg-white/5 flex justify-between">
                        <span className="text-slate-400">Gravity:</span>
                        <span className="text-sky-300 font-bold">{r.gravity_ratio !== null ? `${r.gravity_ratio}x` : '—'}</span>
                      </div>
                      <div className="p-2 rounded-xl bg-white/5 flex justify-between">
                        <span className="text-slate-400">Density:</span>
                        <span className="text-sky-300 font-bold">{r.density_ratio !== null ? `${r.density_ratio}x` : '—'}</span>
                      </div>
                      <div className="p-2 rounded-xl bg-white/5 flex justify-between">
                        <span className="text-slate-400">Period:</span>
                        <span className="text-sky-300 font-bold">{r.period_ratio !== null ? `${r.period_ratio}x` : '—'}</span>
                      </div>
                      <div className="p-2 rounded-xl bg-white/5 flex justify-between">
                        <span className="text-slate-400">Temp:</span>
                        <span className="text-sky-300 font-bold">{r.temperature_ratio !== null ? `${r.temperature_ratio}x` : '—'}</span>
                      </div>
                      <div className="p-2 rounded-xl bg-white/5 flex justify-between">
                        <span className="text-slate-400">Distance:</span>
                        <span className="text-sky-300 font-bold">{r.distance_ratio !== null && r.distance_ratio !== undefined ? `${r.distance_ratio}x` : '—'}</span>
                      </div>
                      <div className="p-2 rounded-xl bg-white/5 flex justify-between">
                        <span className="text-slate-400">Velocity:</span>
                        <span className="text-sky-300 font-bold">{r.velocity_ratio !== null && r.velocity_ratio !== undefined ? `${r.velocity_ratio}x` : '—'}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Absolute & Percentage Differences */}
          <div className="p-6 rounded-3xl glass-panel border border-white/10 space-y-4">
            <div className="flex items-center space-x-2 text-indigo-400">
              <Percent className="w-5 h-5" />
              <h3 className="text-lg font-bold text-white">Absolute & Percentage Deltas</h3>
            </div>
            <p className="text-xs text-slate-400 font-mono">
              Parametric divergence relative to {comparisonData.primary_reference}:
            </p>

            {comparisonData.absolute_differences?.length === 0 ? (
              <p className="text-xs text-slate-500 font-mono">No differential deltas computed.</p>
            ) : (
              <div className="space-y-4">
                {comparisonData.absolute_differences.map((delta: any, idx: number) => (
                  <div key={idx} className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-2.5">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-white font-mono">
                        Δ ({delta.target_name} − {delta.relative_to})
                      </span>
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-300">
                        Differential Variance
                      </span>
                    </div>

                    <div className="space-y-1.5 text-xs font-mono">
                      {delta.mass_diff_earth !== null && delta.mass_diff_earth !== undefined && (
                        <div className="p-2 rounded-xl bg-white/5 flex items-center justify-between">
                          <span className="text-slate-400">Mass Δ:</span>
                          <div className="space-x-2">
                            <span className="text-white font-bold">
                              {delta.mass_diff_earth > 0 ? '+' : ''}{delta.mass_diff_earth} M⊕
                            </span>
                            {delta.mass_diff_percent !== null && delta.mass_diff_percent !== undefined && (
                              <span className={`text-[10px] px-1.5 py-0.5 rounded ${
                                delta.mass_diff_percent >= 0 ? 'bg-emerald-500/20 text-emerald-300' : 'bg-rose-500/20 text-rose-300'
                              }`}>
                                {delta.mass_diff_percent > 0 ? '+' : ''}{delta.mass_diff_percent}%
                              </span>
                            )}
                          </div>
                        </div>
                      )}

                      <div className="p-2 rounded-xl bg-white/5 flex items-center justify-between">
                        <span className="text-slate-400">Radius Δ:</span>
                        <div className="space-x-2">
                          <span className="text-white font-bold">
                            {delta.radius_diff_km !== null ? `${delta.radius_diff_km > 0 ? '+' : ''}${delta.radius_diff_km.toLocaleString()} km` : '—'}
                          </span>
                          {delta.radius_diff_percent !== null && (
                            <span className={`text-[10px] px-1.5 py-0.5 rounded ${
                              delta.radius_diff_percent >= 0 ? 'bg-emerald-500/20 text-emerald-300' : 'bg-rose-500/20 text-rose-300'
                            }`}>
                              {delta.radius_diff_percent > 0 ? '+' : ''}{delta.radius_diff_percent}%
                            </span>
                          )}
                        </div>
                      </div>

                      <div className="p-2 rounded-xl bg-white/5 flex items-center justify-between">
                        <span className="text-slate-400">Gravity Δ:</span>
                        <div className="space-x-2">
                          <span className="text-white font-bold">
                            {delta.gravity_diff_m_s2 !== null ? `${delta.gravity_diff_m_s2 > 0 ? '+' : ''}${delta.gravity_diff_m_s2} m/s²` : '—'}
                          </span>
                          {delta.gravity_diff_percent !== null && (
                            <span className={`text-[10px] px-1.5 py-0.5 rounded ${
                              delta.gravity_diff_percent >= 0 ? 'bg-emerald-500/20 text-emerald-300' : 'bg-rose-500/20 text-rose-300'
                            }`}>
                              {delta.gravity_diff_percent > 0 ? '+' : ''}{delta.gravity_diff_percent}%
                            </span>
                          )}
                        </div>
                      </div>

                      <div className="p-2 rounded-xl bg-white/5 flex items-center justify-between">
                        <span className="text-slate-400">Temperature Δ:</span>
                        <div className="space-x-2">
                          <span className="text-white font-bold">
                            {delta.temperature_diff_k !== null ? `${delta.temperature_diff_k > 0 ? '+' : ''}${delta.temperature_diff_k} K` : '—'}
                          </span>
                          {delta.temperature_diff_percent !== null && (
                            <span className={`text-[10px] px-1.5 py-0.5 rounded ${
                              delta.temperature_diff_percent >= 0 ? 'bg-amber-500/20 text-amber-300' : 'bg-blue-500/20 text-blue-300'
                            }`}>
                              {delta.temperature_diff_percent > 0 ? '+' : ''}{delta.temperature_diff_percent}%
                            </span>
                          )}
                        </div>
                      </div>

                      {delta.distance_diff_au !== null && delta.distance_diff_au !== undefined && (
                        <div className="p-2 rounded-xl bg-white/5 flex items-center justify-between">
                          <span className="text-slate-400">Distance Δ:</span>
                          <div className="space-x-2">
                            <span className="text-white font-bold">
                              {delta.distance_diff_au > 0 ? '+' : ''}{delta.distance_diff_au} AU
                            </span>
                            {delta.distance_diff_percent !== null && delta.distance_diff_percent !== undefined && (
                              <span className={`text-[10px] px-1.5 py-0.5 rounded ${
                                delta.distance_diff_percent >= 0 ? 'bg-emerald-500/20 text-emerald-300' : 'bg-rose-500/20 text-rose-300'
                              }`}>
                                {delta.distance_diff_percent > 0 ? '+' : ''}{delta.distance_diff_percent}%
                              </span>
                            )}
                          </div>
                        </div>
                      )}

                      {delta.orbital_velocity_diff_km_s !== null && delta.orbital_velocity_diff_km_s !== undefined && (
                        <div className="p-2 rounded-xl bg-white/5 flex items-center justify-between">
                          <span className="text-slate-400">Orbital Velocity Δ:</span>
                          <div className="space-x-2">
                            <span className="text-white font-bold">
                              {delta.orbital_velocity_diff_km_s > 0 ? '+' : ''}{delta.orbital_velocity_diff_km_s} km/s
                            </span>
                            {delta.orbital_velocity_diff_percent !== null && delta.orbital_velocity_diff_percent !== undefined && (
                              <span className={`text-[10px] px-1.5 py-0.5 rounded ${
                                delta.orbital_velocity_diff_percent >= 0 ? 'bg-emerald-500/20 text-emerald-300' : 'bg-rose-500/20 text-rose-300'
                              }`}>
                                {delta.orbital_velocity_diff_percent > 0 ? '+' : ''}{delta.orbital_velocity_diff_percent}%
                              </span>
                            )}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Visual Analytics / Charts Section */}
      {comparisonData && (
        <div className="p-6 sm:p-8 rounded-3xl glass-panel border border-white/10 space-y-6">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center space-x-2 text-purple-400">
              <BarChart2 className="w-5 h-5" />
              <h3 className="text-xl font-bold text-white">Visual Parametric Analytics</h3>
            </div>

            <div className="flex items-center space-x-2 bg-space-900 p-1 rounded-xl border border-white/10 text-xs font-mono">
              <button
                onClick={() => setActiveChartTab('bar')}
                className={`px-3 py-1 rounded-lg transition-all ${
                  activeChartTab === 'bar' ? 'bg-sky-500 text-space-950 font-bold' : 'text-slate-400 hover:text-white'
                }`}
              >
                Bar Comparison
              </button>
              <button
                onClick={() => setActiveChartTab('radar')}
                className={`px-3 py-1 rounded-lg transition-all ${
                  activeChartTab === 'radar' ? 'bg-sky-500 text-space-950 font-bold' : 'text-slate-400 hover:text-white'
                }`}
              >
                Radar Profile
              </button>
              <button
                onClick={() => setActiveChartTab('scale')}
                className={`px-3 py-1 rounded-lg transition-all ${
                  activeChartTab === 'scale' ? 'bg-sky-500 text-space-950 font-bold' : 'text-slate-400 hover:text-white'
                }`}
              >
                Scale Diagram
              </button>
            </div>
          </div>

          {/* TAB 1: Bar Chart */}
          {activeChartTab === 'bar' && comparisonData.radar_chart_metrics?.length > 0 && (
            <div className="h-80 w-full pt-4">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={comparisonData.radar_chart_metrics}>
                  <XAxis dataKey="metric" stroke="#64748b" fontSize={11} />
                  <YAxis stroke="#64748b" fontSize={11} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '11px' }}
                  />
                  <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
                  {comparisonData.compared_objects.map((obj: any, idx: number) => (
                    <Bar
                      key={obj.name}
                      dataKey={obj.name}
                      fill={obj.color_hex || palette[idx % palette.length]}
                      radius={[6, 6, 0, 0]}
                    />
                  ))}
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* TAB 2: Radar Chart */}
          {activeChartTab === 'radar' && comparisonData.radar_chart_metrics?.length > 0 && (
            <div className="h-80 w-full pt-4">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart data={comparisonData.radar_chart_metrics}>
                  <PolarGrid stroke="#334155" />
                  <PolarAngleAxis dataKey="metric" stroke="#94a3b8" fontSize={11} />
                  <PolarRadiusAxis stroke="#475569" fontSize={9} />
                  {comparisonData.compared_objects.map((obj: any, idx: number) => (
                    <Radar
                      key={obj.name}
                      name={obj.name}
                      dataKey={obj.name}
                      stroke={obj.color_hex || palette[idx % palette.length]}
                      fill={obj.color_hex || palette[idx % palette.length]}
                      fillOpacity={0.3}
                    />
                  ))}
                  <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '11px' }}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* TAB 3: Proportional Scale Diagram */}
          {activeChartTab === 'scale' && (
            <div className="p-6 rounded-2xl bg-space-900 border border-white/5 space-y-4 text-center">
              <span className="text-xs font-mono text-slate-400 block">
                Visual Volumetric Radius Comparison (Scaled Proportions)
              </span>

              <div className="flex flex-wrap items-end justify-center gap-12 py-8 min-h-[220px]">
                {comparisonData.compared_objects.map((obj: any, idx: number) => {
                  // Normalize radius relative to the max radius among compared objects
                  const maxRadius = Math.max(...comparisonData.compared_objects.map((o: any) => o.radius_km || 1000));
                  const normalizedPx = Math.max(28, Math.min(180, Math.round(((obj.radius_km || 1000) / maxRadius) * 160)));
                  return (
                    <div key={obj.id} className="flex flex-col items-center space-y-2">
                      <div
                        className="rounded-full flex items-center justify-center transition-all shadow-lg hover:scale-105"
                        style={{
                          width: `${normalizedPx}px`,
                          height: `${normalizedPx}px`,
                          backgroundColor: obj.color_hex || palette[idx % palette.length],
                          boxShadow: `0 0 20px ${obj.color_hex || palette[idx % palette.length]}40`
                        }}
                      />
                      <span className="text-xs font-bold text-white font-mono mt-1">{obj.name}</span>
                      <span className="text-[10px] text-slate-400 font-mono">
                        {obj.radius_km ? `${obj.radius_km.toLocaleString()} km` : '—'}
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Comparative AI Synthesis Engine */}
      <div className="p-6 sm:p-8 rounded-3xl glass-panel border border-sky-500/20 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Sparkles className="w-5 h-5 text-sky-400" />
            <h3 className="text-xl font-bold text-white">Generate Grounded Comparative AI Synthesis</h3>
          </div>
          <span className="text-xs font-mono text-slate-400 capitalize">
            Persona: <strong className="text-white">{mode}</strong>
          </span>
        </div>

        <p className="text-xs text-slate-300">
          Click below to generate a grounded astrophysical report contrasting planetary evolution, atmosphere retention, and orbital mechanics across these targets.
        </p>

        <div className="flex flex-wrap items-center gap-3">
          <button
            onClick={handleGenerateComparativeAI}
            disabled={aiLoading}
            className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-semibold text-xs flex items-center space-x-2 transition-all shadow-md shadow-sky-500/20 disabled:opacity-50"
          >
            <Zap className="w-4 h-4" />
            <span>{aiLoading ? 'Synthesizing Analysis...' : 'Generate Comparative Report'}</span>
          </button>
          <Link
            to={`/ai?compare=${selectedIds.join(',')}&prompt=${encodeURIComponent(`Compare ${selectedIds.join(' and ')}.`)}`}
            className="px-5 py-2.5 rounded-xl bg-white/10 hover:bg-white/20 text-slate-200 font-semibold text-xs flex items-center space-x-2 transition-all border border-white/10"
          >
            <Bot className="w-4 h-4 text-sky-400" />
            <span>Open in AI Assistant</span>
          </Link>
        </div>

        {aiAnalysis && (
          <div className="mt-4 p-5 rounded-2xl bg-space-900/90 border border-sky-500/20 text-xs text-slate-200 leading-relaxed whitespace-pre-wrap animate-fadeIn">
            {aiAnalysis}
          </div>
        )}
      </div>
    </div>
  );
};
