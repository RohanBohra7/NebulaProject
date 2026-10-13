import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  fetchObjects,
  calculateHohmann,
  calculateResonance,
  calculateGravityForce,
  calculateSurfaceGravity,
  calculateOrbitalVelocity,
  fetchSimulationsHistory,
  chatAI
} from '../services/api';
import { AstronomicalObject, HohmannTransferResult } from '../types/astronomy';
import { Object3DViewer } from '../components/visualization/Object3DViewer';
import {
  Cpu,
  Calculator,
  Search,
  Download,
  Send,
  Zap,
  ArrowRight,
  ShieldCheck,
  Radio,
  FileSpreadsheet,
  Atom,
  Clock,
  ExternalLink,
  Layers,
  Sparkles,
  GitCompare,
  TrendingUp,
  Activity,
  CheckCircle2,
  Eye,
  X
} from 'lucide-react';

export const ResearcherDashboard: React.FC = () => {
  const navigate = useNavigate();
  const [objects, setObjects] = useState<AstronomicalObject[]>([]);
  const [filterCat, setFilterCat] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [massFilter, setMassFilter] = useState('All');
  const [sortBy, setSortBy] = useState<'name' | 'mass' | 'radius' | 'period' | 'gravity'>('name');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');

  // 3D Preview Modal State
  const [previewObject, setPreviewObject] = useState<AstronomicalObject | null>(null);

  // Quick Compare Selector State
  const [compareTarget1, setCompareTarget1] = useState('earth');
  const [compareTarget2, setCompareTarget2] = useState('mars');

  // Active Calculation Tool Tab
  const [calcTab, setCalcTab] = useState<'gravity' | 'surface' | 'hohmann' | 'resonance'>('gravity');

  // Scientific Calculation State: Universal Gravitation Force
  const [gravObj1, setGravObj1] = useState('sun');
  const [gravObj2, setGravObj2] = useState('earth');
  const [gravResult, setGravResult] = useState<any | null>(null);
  const [gravLoading, setGravLoading] = useState(false);

  // Scientific Calculation State: Surface Gravity & Escape Velocity
  const [surfaceObj, setSurfaceObj] = useState('earth');
  const [surfaceResult, setSurfaceResult] = useState<any | null>(null);
  const [surfaceLoading, setSurfaceLoading] = useState(false);

  // Hohmann Calculator State
  const [originId, setOriginId] = useState('earth');
  const [targetId, setTargetId] = useState('mars');
  const [hohmannResult, setHohmannResult] = useState<HohmannTransferResult | null>(null);
  const [hohmannLoading, setHohmannLoading] = useState(false);

  // Resonance Scanner State
  const [resObj1, setResObj1] = useState('neptune');
  const [resObj2, setResObj2] = useState('pluto');
  const [resonanceResult, setResonanceResult] = useState<any | null>(null);
  const [resonanceLoading, setResonanceLoading] = useState(false);

  // Simulation Runs History State
  const [simHistory, setSimHistory] = useState<any[]>([]);
  const [simHistoryLoading, setSimHistoryLoading] = useState(false);

  // Researcher AI Assistant State
  const [aiPrompt, setAiPrompt] = useState('');
  const [aiResponse, setAiResponse] = useState<string | null>(null);
  const [aiLoading, setAiLoading] = useState(false);

  useEffect(() => {
    fetchObjects().then((data) => {
      setObjects(data);
      // Run initial surface gravity
      calculateSurfaceGravity({ object_id: 'earth' }).then((res) => setSurfaceResult(res));
      // Run initial gravity force between Sun and Earth
      calculateGravityForce({ object1_id: 'sun', object2_id: 'earth' }).then((res) => setGravResult(res));
    });

    // Run initial Hohmann transfer
    calculateHohmann({ origin_id: 'earth', target_id: 'mars' }).then((res) => setHohmannResult(res));

    // Run initial resonance check
    calculateResonance(60189.0, 90560.0).then((res) => setResonanceResult(res));

    // Load recent simulation runs
    loadSimHistory();
  }, []);

  const loadSimHistory = async () => {
    setSimHistoryLoading(true);
    try {
      const runs = await fetchSimulationsHistory();
      setSimHistory(runs.slice(0, 5));
    } catch {
      // Fallback if none yet
    } finally {
      setSimHistoryLoading(false);
    }
  };

  const handleComputeGravity = async () => {
    setGravLoading(true);
    try {
      const res = await calculateGravityForce({ object1_id: gravObj1, object2_id: gravObj2 });
      setGravResult(res);
    } catch (e) {
      console.error(e);
    } finally {
      setGravLoading(false);
    }
  };

  const handleComputeSurface = async () => {
    setSurfaceLoading(true);
    try {
      const res = await calculateSurfaceGravity({ object_id: surfaceObj });
      setSurfaceResult(res);
    } catch (e) {
      console.error(e);
    } finally {
      setSurfaceLoading(false);
    }
  };

  const handleComputeHohmann = async () => {
    setHohmannLoading(true);
    try {
      const res = await calculateHohmann({ origin_id: originId, target_id: targetId });
      setHohmannResult(res);
    } catch (e) {
      console.error(e);
    } finally {
      setHohmannLoading(false);
    }
  };

  const handleComputeResonance = async () => {
    const o1 = objects.find((o) => o.id === resObj1);
    const o2 = objects.find((o) => o.id === resObj2);
    if (!o1?.orbital_period_days || !o2?.orbital_period_days) return;

    setResonanceLoading(true);
    try {
      const res = await calculateResonance(o1.orbital_period_days, o2.orbital_period_days);
      setResonanceResult({ ...res, body1: o1.name, body2: o2.name });
    } catch (e) {
      console.error(e);
    } finally {
      setResonanceLoading(false);
    }
  };

  const handleAskResearcherAI = async (promptText: string) => {
    setAiLoading(true);
    setAiPrompt(promptText);
    try {
      const res = await chatAI(promptText, 'researcher');
      setAiResponse(res.response);
    } catch {
      setAiResponse('Astrophysical derivation service momentarily unavailable.');
    } finally {
      setAiLoading(false);
    }
  };

  const handleLaunchCompare = () => {
    navigate(`/compare?obj1=${compareTarget1}&obj2=${compareTarget2}`);
  };

  // Filter and sort catalog
  const filteredObjects = objects
    .filter((o) => {
      const matchesCat = filterCat === 'All' || o.category.toLowerCase() === filterCat.toLowerCase();
      const matchesSearch =
        o.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        o.id.includes(searchQuery.toLowerCase()) ||
        o.category.toLowerCase().includes(searchQuery.toLowerCase());

      let matchesMass = true;
      if (massFilter === 'terrestrial') matchesMass = (o.mass_earth_relative || 0) <= 2.0;
      else if (massFilter === 'giant') matchesMass = (o.mass_earth_relative || 0) > 2.0 && (o.mass_earth_relative || 0) < 500.0;
      else if (massFilter === 'stellar') matchesMass = (o.mass_earth_relative || 0) >= 500.0;

      return matchesCat && matchesSearch && matchesMass;
    })
    .sort((a, b) => {
      let valA: any = a.name;
      let valB: any = b.name;
      if (sortBy === 'mass') {
        valA = a.mass_earth_relative || 0;
        valB = b.mass_earth_relative || 0;
      } else if (sortBy === 'radius') {
        valA = a.radius_km || 0;
        valB = b.radius_km || 0;
      } else if (sortBy === 'period') {
        valA = a.orbital_period_days || 0;
        valB = b.orbital_period_days || 0;
      } else if (sortBy === 'gravity') {
        valA = a.surface_gravity_m_s2 || 0;
        valB = b.surface_gravity_m_s2 || 0;
      }
      if (valA < valB) return sortOrder === 'asc' ? -1 : 1;
      if (valA > valB) return sortOrder === 'asc' ? 1 : -1;
      return 0;
    });

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-12">
      {/* Researcher Banner */}
      <div className="p-8 rounded-3xl glass-panel-glow border border-sky-500/20 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-2">
            <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-sky-500/10 text-sky-300 border border-sky-400/20 text-xs font-mono">
              <Cpu className="w-3.5 h-3.5" />
              <span>Researcher Perspective • Quantitative Astrophysics & Orbital Telemetry</span>
            </div>
            <h1 className="text-3xl sm:text-4xl font-extrabold text-white">
              Astrophysics & Orbital Analysis Workstation
            </h1>
          </div>
          <div className="flex items-center space-x-2">
            <a
              href="/api/data/export?format=csv"
              download
              className="px-3.5 py-2 rounded-xl bg-sky-600/30 hover:bg-sky-600/50 border border-sky-400/30 text-sky-200 text-xs font-mono flex items-center space-x-1.5 transition-all"
            >
              <FileSpreadsheet className="w-3.5 h-3.5" />
              <span>Export CSV</span>
            </a>
            <a
              href="/api/data/export?format=json"
              download
              className="px-3.5 py-2 rounded-xl bg-white/10 hover:bg-white/20 border border-white/10 text-white text-xs font-mono flex items-center space-x-1.5 transition-all"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Export JSON</span>
            </a>
          </div>
        </div>
        <p className="text-sm text-slate-300 max-w-3xl leading-relaxed">
          Access empirical astrometric parameters sourced from NASA JPL Horizons, Gaia DR3, SIMBAD, and the NASA
          Exoplanet Archive. Perform high-precision orbital transfers, gravitational force calculations, and Hamiltonian
          N-body simulations.
        </p>
      </div>

      {/* Quick Launch & Workstation Toolbar */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Quick Comparator Card */}
        <div className="p-5 rounded-2xl glass-panel border border-white/10 space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2 text-sky-400">
              <GitCompare className="w-4 h-4" />
              <h4 className="text-sm font-bold text-white">Parametric Comparator</h4>
            </div>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-sky-500/10 text-sky-300">Quick Diff</span>
          </div>
          <p className="text-xs text-slate-400">Compare physical, orbital, and Astropy parameters side-by-side.</p>
          <div className="grid grid-cols-2 gap-2">
            <select
              value={compareTarget1}
              onChange={(e) => setCompareTarget1(e.target.value)}
              className="bg-space-900 border border-white/10 rounded-xl px-2.5 py-1.5 text-xs text-white"
            >
              {objects.map((o) => (
                <option key={o.id} value={o.id}>{o.name}</option>
              ))}
            </select>
            <select
              value={compareTarget2}
              onChange={(e) => setCompareTarget2(e.target.value)}
              className="bg-space-900 border border-white/10 rounded-xl px-2.5 py-1.5 text-xs text-white"
            >
              {objects.map((o) => (
                <option key={o.id} value={o.id}>{o.name}</option>
              ))}
            </select>
          </div>
          <button
            onClick={handleLaunchCompare}
            className="w-full py-2 rounded-xl bg-sky-600/30 hover:bg-sky-600/50 border border-sky-400/30 text-sky-200 text-xs font-semibold flex items-center justify-center space-x-1.5 transition-all"
          >
            <span>Launch Comparison Matrix</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* N-Body Simulation Launcher */}
        <div className="p-5 rounded-2xl glass-panel border border-white/10 space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2 text-purple-400">
              <Atom className="w-4 h-4" />
              <h4 className="text-sm font-bold text-white">N-Body Gravitational Engine</h4>
            </div>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-500/10 text-purple-300">REBOUND</span>
          </div>
          <p className="text-xs text-slate-400">
            Launch multi-body orbits with Gauss-Radau (IAS15) or Symplectic Wisdom-Holman (WHFast).
          </p>
          <div className="flex items-center space-x-2">
            <Link
              to="/simulation"
              className="flex-1 py-2 rounded-xl bg-purple-600/30 hover:bg-purple-600/50 border border-purple-400/30 text-purple-200 text-xs font-semibold flex items-center justify-center space-x-1.5 transition-all"
            >
              <span>Open Simulation Lab</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>

        {/* 3D Ephemeris Visualizer */}
        <div className="p-5 rounded-2xl glass-panel border border-white/10 space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2 text-emerald-400">
              <Activity className="w-4 h-4" />
              <h4 className="text-sm font-bold text-white">3D Solar System Ephemeris</h4>
            </div>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300">WebGL</span>
          </div>
          <p className="text-xs text-slate-400">
            Render 3D planetary orbits with real relative inclination and scientific scaling.
          </p>
          <div className="flex items-center space-x-2">
            <Link
              to="/visualization"
              className="flex-1 py-2 rounded-xl bg-emerald-600/30 hover:bg-emerald-600/50 border border-emerald-400/30 text-emerald-200 text-xs font-semibold flex items-center justify-center space-x-1.5 transition-all"
            >
              <span>Launch 3D Ephemeris</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </div>

      {/* Scientific Calculations Workbench */}
      <div className="p-6 sm:p-8 rounded-3xl glass-panel border border-sky-500/20 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-white/10 pb-4">
          <div>
            <div className="flex items-center space-x-2 text-sky-400">
              <Calculator className="w-5 h-5" />
              <h3 className="text-lg font-bold text-white">Scientific Calculation & Orbital Mechanics Engine</h3>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">
              Exact solutions utilizing NumPy, SciPy, and Astropy dimensional units.
            </p>
          </div>

          {/* Calculator Tab Switcher */}
          <div className="flex flex-wrap items-center gap-1 p-1 bg-space-900 border border-white/10 rounded-2xl text-xs">
            <button
              onClick={() => setCalcTab('gravity')}
              className={`px-3 py-1.5 rounded-xl font-medium transition-all ${
                calcTab === 'gravity' ? 'bg-sky-500 text-white font-bold' : 'text-slate-400 hover:text-white'
              }`}
            >
              Gravitational Force
            </button>
            <button
              onClick={() => setCalcTab('surface')}
              className={`px-3 py-1.5 rounded-xl font-medium transition-all ${
                calcTab === 'surface' ? 'bg-sky-500 text-white font-bold' : 'text-slate-400 hover:text-white'
              }`}
            >
              Surface Gravity & v_esc
            </button>
            <button
              onClick={() => setCalcTab('hohmann')}
              className={`px-3 py-1.5 rounded-xl font-medium transition-all ${
                calcTab === 'hohmann' ? 'bg-sky-500 text-white font-bold' : 'text-slate-400 hover:text-white'
              }`}
            >
              Hohmann Δv Solver
            </button>
            <button
              onClick={() => setCalcTab('resonance')}
              className={`px-3 py-1.5 rounded-xl font-medium transition-all ${
                calcTab === 'resonance' ? 'bg-sky-500 text-white font-bold' : 'text-slate-400 hover:text-white'
              }`}
            >
              Resonance Scanner
            </button>
          </div>
        </div>

        {/* Tab 1: Universal Gravitation Force */}
        {calcTab === 'gravity' && (
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-[11px] text-slate-400 block mb-1">Body 1 (Primary Attractor)</label>
                <select
                  value={gravObj1}
                  onChange={(e) => setGravObj1(e.target.value)}
                  className="w-full bg-space-900 border border-white/10 rounded-xl px-3 py-2 text-xs text-white"
                >
                  {objects.map((o) => (
                    <option key={o.id} value={o.id}>{o.name} ({o.mass_earth_relative || 1} M⊕)</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="text-[11px] text-slate-400 block mb-1">Body 2 (Secondary Attractor)</label>
                <select
                  value={gravObj2}
                  onChange={(e) => setGravObj2(e.target.value)}
                  className="w-full bg-space-900 border border-white/10 rounded-xl px-3 py-2 text-xs text-white"
                >
                  {objects.map((o) => (
                    <option key={o.id} value={o.id}>{o.name} ({o.mass_earth_relative || 1} M⊕)</option>
                  ))}
                </select>
              </div>
            </div>

            <button
              onClick={handleComputeGravity}
              disabled={gravLoading}
              className="py-2.5 px-6 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-semibold text-xs flex items-center space-x-2 transition-all disabled:opacity-50"
            >
              <Zap className="w-3.5 h-3.5" />
              <span>{gravLoading ? 'Calculating...' : 'Compute Gravitational Force'}</span>
            </button>

            {gravResult && (
              <div className="p-4 rounded-2xl bg-space-900 border border-sky-500/20 space-y-2 text-xs font-mono">
                <div className="flex justify-between text-slate-300">
                  <span>Scalar Gravitational Force (F = G m1 m2 / r²):</span>
                  <strong className="text-sky-400 font-bold">{Number(gravResult.force_newtons).toExponential(4)} N</strong>
                </div>
                <div className="flex justify-between text-slate-400 text-[11px]">
                  <span>Radial Separation (r):</span>
                  <span>{gravResult.distance_m?.toExponential(3)} m ({gravResult.distance_au?.toFixed(4)} AU)</span>
                </div>
                <div className="flex justify-between text-slate-400 text-[11px]">
                  <span>Formula Applied:</span>
                  <span className="text-slate-300 font-sans">{gravResult.formula}</span>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Tab 2: Surface Gravity & Escape Velocity */}
        {calcTab === 'surface' && (
          <div className="space-y-4">
            <div className="max-w-md">
              <label className="text-[11px] text-slate-400 block mb-1">Target Celestial Object</label>
              <select
                value={surfaceObj}
                onChange={(e) => setSurfaceObj(e.target.value)}
                className="w-full bg-space-900 border border-white/10 rounded-xl px-3 py-2 text-xs text-white"
              >
                {objects.map((o) => (
                  <option key={o.id} value={o.id}>{o.name}</option>
                ))}
              </select>
            </div>

            <button
              onClick={handleComputeSurface}
              disabled={surfaceLoading}
              className="py-2.5 px-6 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-semibold text-xs flex items-center space-x-2 transition-all disabled:opacity-50"
            >
              <Zap className="w-3.5 h-3.5" />
              <span>{surfaceLoading ? 'Calculating...' : 'Compute Surface Gravity'}</span>
            </button>

            {surfaceResult && (
              <div className="p-4 rounded-2xl bg-space-900 border border-sky-500/20 grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs font-mono text-center">
                <div className="p-3 rounded-xl bg-white/5">
                  <span className="text-[10px] text-slate-400 block font-sans">Surface Gravity (g)</span>
                  <span className="text-base font-bold text-sky-400">{surfaceResult.surface_gravity_m_s2?.toFixed(3)} m/s²</span>
                </div>
                <div className="p-3 rounded-xl bg-white/5">
                  <span className="text-[10px] text-slate-400 block font-sans">Earth Gees Ratio</span>
                  <span className="text-base font-bold text-emerald-400">{surfaceResult.surface_gravity_gees?.toFixed(3)} g</span>
                </div>
                <div className="p-3 rounded-xl bg-white/5">
                  <span className="text-[10px] text-slate-400 block font-sans">Escape Velocity</span>
                  <span className="text-base font-bold text-amber-400">{surfaceResult.escape_velocity_km_s?.toFixed(2)} km/s</span>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Tab 3: Hohmann Transfer */}
        {calcTab === 'hohmann' && (
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-[11px] text-slate-400 block mb-1">Departure Orbit</label>
                <select
                  value={originId}
                  onChange={(e) => setOriginId(e.target.value)}
                  className="w-full bg-space-900 border border-white/10 rounded-xl px-3 py-2 text-xs text-white"
                >
                  {objects.filter((o) => o.semi_major_axis_au).map((o) => (
                    <option key={o.id} value={o.id}>{o.name} ({o.semi_major_axis_au} AU)</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="text-[11px] text-slate-400 block mb-1">Target Arrival Orbit</label>
                <select
                  value={targetId}
                  onChange={(e) => setTargetId(e.target.value)}
                  className="w-full bg-space-900 border border-white/10 rounded-xl px-3 py-2 text-xs text-white"
                >
                  {objects.filter((o) => o.semi_major_axis_au).map((o) => (
                    <option key={o.id} value={o.id}>{o.name} ({o.semi_major_axis_au} AU)</option>
                  ))}
                </select>
              </div>
            </div>

            <button
              onClick={handleComputeHohmann}
              disabled={hohmannLoading || originId === targetId}
              className="py-2.5 px-6 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-semibold text-xs flex items-center space-x-2 transition-all disabled:opacity-50"
            >
              <Zap className="w-3.5 h-3.5" />
              <span>{hohmannLoading ? 'Integrating...' : 'Compute Transfer Trajectory'}</span>
            </button>

            {hohmannResult && (
              <div className="p-4 rounded-2xl bg-space-900 border border-sky-500/20 space-y-3">
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-center">
                  <div className="p-2.5 rounded-xl bg-white/5">
                    <span className="text-[10px] text-slate-400 block">Burn 1 (Δv1)</span>
                    <span className="text-sm font-bold font-mono text-sky-400">{hohmannResult.delta_v1_km_s} km/s</span>
                  </div>
                  <div className="p-2.5 rounded-xl bg-white/5">
                    <span className="text-[10px] text-slate-400 block">Burn 2 (Δv2)</span>
                    <span className="text-sm font-bold font-mono text-sky-400">{hohmannResult.delta_v2_km_s} km/s</span>
                  </div>
                  <div className="p-2.5 rounded-xl bg-white/5">
                    <span className="text-[10px] text-slate-400 block">Total Impulse</span>
                    <span className="text-sm font-bold font-mono text-emerald-400">{hohmannResult.total_delta_v_km_s} km/s</span>
                  </div>
                  <div className="p-2.5 rounded-xl bg-white/5">
                    <span className="text-[10px] text-slate-400 block">Flight Duration</span>
                    <span className="text-sm font-bold font-mono text-amber-400">{hohmannResult.transfer_time_days} days</span>
                  </div>
                </div>
                <div className="text-[10px] text-slate-400 font-mono space-y-0.5">
                  <div>Transfer semi-major axis: a = {hohmannResult.transfer_semi_major_axis_au?.toFixed(4)} AU</div>
                  <div>Transfer orbit eccentricity: e = {hohmannResult.transfer_eccentricity?.toFixed(4)}</div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Tab 4: Resonance Scanner */}
        {calcTab === 'resonance' && (
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-[11px] text-slate-400 block mb-1">Body 1</label>
                <select
                  value={resObj1}
                  onChange={(e) => setResObj1(e.target.value)}
                  className="w-full bg-space-900 border border-white/10 rounded-xl px-3 py-2 text-xs text-white"
                >
                  {objects.filter((o) => o.orbital_period_days).map((o) => (
                    <option key={o.id} value={o.id}>{o.name} ({o.orbital_period_days} d)</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="text-[11px] text-slate-400 block mb-1">Body 2</label>
                <select
                  value={resObj2}
                  onChange={(e) => setResObj2(e.target.value)}
                  className="w-full bg-space-900 border border-white/10 rounded-xl px-3 py-2 text-xs text-white"
                >
                  {objects.filter((o) => o.orbital_period_days).map((o) => (
                    <option key={o.id} value={o.id}>{o.name} ({o.orbital_period_days} d)</option>
                  ))}
                </select>
              </div>
            </div>

            <button
              onClick={handleComputeResonance}
              disabled={resonanceLoading || resObj1 === resObj2}
              className="py-2.5 px-6 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-semibold text-xs flex items-center space-x-2 transition-all disabled:opacity-50"
            >
              <Radio className="w-3.5 h-3.5" />
              <span>{resonanceLoading ? 'Scanning...' : 'Scan Commensurability'}</span>
            </button>

            {resonanceResult && (
              <div className="p-4 rounded-2xl bg-space-900 border border-purple-500/20 space-y-2 text-xs font-mono">
                <div className="flex justify-between text-slate-300">
                  <span>Period Ratio:</span>
                  <strong>{(resonanceResult.period_2_days / resonanceResult.period_1_days).toFixed(4)}</strong>
                </div>
                {resonanceResult.resonances_found?.map((r: any, i: number) => (
                  <div key={i} className="flex justify-between p-2 rounded-lg bg-white/5 text-purple-300">
                    <span>{r.ratio_str} Commensurability</span>
                    <span className="text-slate-400 text-[11px]">Discrepancy: {r.discrepancy_percent}%</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Recent Simulation Runs History */}
      <div className="p-6 rounded-3xl glass-panel border border-white/10 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2 text-purple-400">
            <Clock className="w-4 h-4" />
            <h3 className="text-base font-bold text-white">N-Body Numerical Simulation Run History</h3>
          </div>
          <Link to="/simulation" className="text-xs text-sky-400 hover:text-sky-300 font-mono flex items-center space-x-1">
            <span>Configure & Run New Simulation</span>
            <ArrowRight className="w-3 h-3" />
          </Link>
        </div>

        {simHistory.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left">
              <thead className="bg-white/5 text-slate-400 font-mono border-b border-white/10">
                <tr>
                  <th className="p-2.5">Run ID</th>
                  <th className="p-2.5">Scenario</th>
                  <th className="p-2.5">Status</th>
                  <th className="p-2.5">Integrator</th>
                  <th className="p-2.5">Duration</th>
                  <th className="p-2.5">Steps</th>
                  <th className="p-2.5">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5 font-mono text-slate-300">
                {simHistory.map((run) => (
                  <tr key={run.id} className="hover:bg-white/5">
                    <td className="p-2.5 text-sky-400 font-bold">{run.id}</td>
                    <td className="p-2.5 text-white font-sans">{run.parameters?.scenario_name || run.scenario_id}</td>
                    <td className="p-2.5">
                      <span className="px-2 py-0.5 rounded text-[10px] bg-emerald-500/10 text-emerald-300 border border-emerald-500/20">
                        {run.status}
                      </span>
                    </td>
                    <td className="p-2.5 uppercase text-indigo-300">{run.parameters?.integrator || 'IAS15'}</td>
                    <td className="p-2.5">{run.parameters?.duration} yr</td>
                    <td className="p-2.5">{run.parameters?.num_steps}</td>
                    <td className="p-2.5">
                      <Link
                        to={`/simulation`}
                        className="text-xs text-sky-400 hover:text-white underline font-sans"
                      >
                        Inspect
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="p-6 text-center text-xs text-slate-400 font-mono">
            No active runs cached in current session. Execute a run in the <Link to="/simulation" className="text-sky-400 underline">Simulation Lab</Link>.
          </div>
        )}
      </div>

      {/* Advanced Empirical Astrometric Catalog */}
      <div className="p-6 sm:p-8 rounded-3xl glass-panel border border-white/10 space-y-6">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <h3 className="text-lg font-bold text-white">Empirical Astrometric Catalog</h3>
            <p className="text-xs text-slate-400">
              Complete physical and orbital elements across all 23 targets with direct 3D preview and telemetry.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            {/* Search */}
            <div className="relative">
              <Search className="w-3.5 h-3.5 absolute left-3 top-3 text-slate-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search catalog..."
                className="bg-space-900 border border-white/10 rounded-xl pl-9 pr-3 py-1.5 text-xs text-white focus:outline-none focus:border-sky-500"
              />
            </div>

            {/* Category Filter */}
            <select
              value={filterCat}
              onChange={(e) => setFilterCat(e.target.value)}
              className="bg-space-900 border border-white/10 rounded-xl px-3 py-1.5 text-xs text-white"
            >
              <option value="All">All Categories</option>
              <option value="Planet">Planets</option>
              <option value="Moon">Moons</option>
              <option value="Exoplanet">Exoplanets</option>
              <option value="Star">Stars</option>
              <option value="Deep-Sky">Deep-Sky</option>
              <option value="Comet">Comets / Asteroids</option>
            </select>

            {/* Mass Filter */}
            <select
              value={massFilter}
              onChange={(e) => setMassFilter(e.target.value)}
              className="bg-space-900 border border-white/10 rounded-xl px-3 py-1.5 text-xs text-white"
            >
              <option value="All">All Masses</option>
              <option value="terrestrial">Terrestrial (≤ 2 M⊕)</option>
              <option value="giant">Giant (2–500 M⊕)</option>
              <option value="stellar">Stellar (&gt; 500 M⊕)</option>
            </select>

            {/* Sort Metric */}
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as any)}
              className="bg-space-900 border border-white/10 rounded-xl px-3 py-1.5 text-xs text-white"
            >
              <option value="name">Sort: Name</option>
              <option value="mass">Sort: Mass</option>
              <option value="radius">Sort: Radius</option>
              <option value="period">Sort: Period</option>
              <option value="gravity">Sort: Gravity</option>
            </select>

            {/* Sort Order Toggle */}
            <button
              onClick={() => setSortOrder((prev) => (prev === 'asc' ? 'desc' : 'asc'))}
              className="px-2.5 py-1.5 rounded-xl bg-space-900 border border-white/10 text-xs text-slate-300 font-mono"
            >
              {sortOrder.toUpperCase()}
            </button>
          </div>
        </div>

        {/* Catalog Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-white/5 text-slate-400 border-b border-white/10 font-mono">
              <tr>
                <th className="p-3">Object</th>
                <th className="p-3">Category</th>
                <th className="p-3">Mass (M⊕)</th>
                <th className="p-3">Radius (km)</th>
                <th className="p-3">Semi-Major (a)</th>
                <th className="p-3">Period (P)</th>
                <th className="p-3">Eccentricity (e)</th>
                <th className="p-3">Gravity (g)</th>
                <th className="p-3">Data Provenance</th>
                <th className="p-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {filteredObjects.map((obj) => (
                <tr key={obj.id} className="hover:bg-white/5 transition-all">
                  <td className="p-3 font-semibold text-white flex items-center space-x-2">
                    <span className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ backgroundColor: obj.color_hex || '#38bdf8' }} />
                    <Link to={`/object/${obj.id}`} className="hover:text-sky-400 underline">
                      {obj.name}
                    </Link>
                  </td>
                  <td className="p-3 text-slate-300 font-mono">{obj.category}</td>
                  <td className="p-3 text-slate-300 font-mono">{obj.mass_earth_relative ?? '—'}</td>
                  <td className="p-3 text-slate-300 font-mono">{obj.radius_km ? obj.radius_km.toLocaleString() : '—'}</td>
                  <td className="p-3 text-slate-300 font-mono">{obj.semi_major_axis_au !== null ? `${obj.semi_major_axis_au} AU` : '—'}</td>
                  <td className="p-3 text-slate-300 font-mono">{obj.orbital_period_days ? `${obj.orbital_period_days} d` : '—'}</td>
                  <td className="p-3 text-slate-300 font-mono">{obj.eccentricity ?? '—'}</td>
                  <td className="p-3 text-slate-300 font-mono">{obj.surface_gravity_m_s2 ? `${obj.surface_gravity_m_s2} m/s²` : '—'}</td>
                  <td className="p-3 text-slate-400 font-mono text-[10px] truncate max-w-[140px]">{obj.data_source}</td>
                  <td className="p-3 text-right space-x-2 font-mono">
                    <button
                      onClick={() => setPreviewObject(obj)}
                      className="px-2 py-1 rounded bg-white/5 hover:bg-white/10 text-sky-400 hover:text-sky-300 transition-all text-[11px]"
                      title="Quick 3D Inspection"
                    >
                      <Eye className="w-3.5 h-3.5 inline mr-1" />
                      <span>3D</span>
                    </button>
                    <Link
                      to={`/object/${obj.id}`}
                      className="px-2 py-1 rounded bg-sky-500/10 hover:bg-sky-500/20 text-sky-300 transition-all text-[11px]"
                    >
                      Telemetry
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Quantitative AI Assistant */}
      <div className="p-6 rounded-3xl glass-panel border border-sky-500/20 space-y-4">
        <div className="flex items-center space-x-2">
          <Cpu className="w-5 h-5 text-sky-400" />
          <h3 className="text-lg font-bold text-white">Astrophysical Inquiry Assistant</h3>
        </div>
        <p className="text-xs text-slate-300">
          Formulate queries requiring quantitative derivations, secular stability analysis, or observational spectroscopy constraints.
        </p>

        <div className="flex flex-wrap gap-2 text-xs">
          {[
            'Derive the Hill sphere radius for TRAPPIST-1e.',
            'Explain relativistic perihelion advance of Mercury using General Relativity.',
            'Compare the tidal dissipation factor Q for Europa versus Io.',
            'Detail the Chandrasekhar mass limit for Sirius B.'
          ].map((q, i) => (
            <button
              key={i}
              onClick={() => handleAskResearcherAI(q)}
              className="px-3 py-1 rounded-lg bg-white/5 hover:bg-white/10 text-slate-300 border border-white/5 transition-all text-left"
            >
              {q}
            </button>
          ))}
        </div>

        <div className="flex gap-2 pt-2">
          <input
            type="text"
            value={aiPrompt}
            onChange={(e) => setAiPrompt(e.target.value)}
            placeholder="Ask formal astrophysical derivation or parameter verification query..."
            className="flex-1 bg-space-900 border border-white/10 rounded-xl px-4 py-2.5 text-xs text-white focus:outline-none focus:border-sky-500"
          />
          <button
            onClick={() => handleAskResearcherAI(aiPrompt)}
            disabled={aiLoading || !aiPrompt.trim()}
            className="px-5 py-2.5 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-semibold text-xs flex items-center space-x-1.5 transition-all disabled:opacity-50"
          >
            <Send className="w-3.5 h-3.5" />
            <span>{aiLoading ? 'Deriving...' : 'Analyze'}</span>
          </button>
        </div>

        {aiResponse && (
          <div className="mt-4 p-5 rounded-2xl bg-space-900/95 border border-sky-500/30 text-xs text-slate-200 leading-relaxed font-sans whitespace-pre-wrap">
            {aiResponse}
          </div>
        )}
      </div>

      {/* 3D Preview Modal */}
      {previewObject && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-space-950/80 backdrop-blur-md">
          <div className="relative w-full max-w-xl p-6 rounded-3xl glass-panel border border-white/10 space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-bold text-white">{previewObject.name}</h3>
                <span className="text-xs text-sky-400 font-mono">{previewObject.category}</span>
              </div>
              <button
                onClick={() => setPreviewObject(null)}
                className="p-1.5 rounded-xl bg-white/5 hover:bg-white/10 text-slate-400 hover:text-white"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="h-72 w-full">
              <Object3DViewer object={previewObject} size={280} />
            </div>

            <div className="grid grid-cols-3 gap-2 text-center text-xs font-mono">
              <div className="p-2 rounded-xl bg-white/5">
                <span className="text-[10px] text-slate-400 block font-sans">Mass</span>
                <span className="text-white font-bold">{previewObject.mass_earth_relative || '—'} M⊕</span>
              </div>
              <div className="p-2 rounded-xl bg-white/5">
                <span className="text-[10px] text-slate-400 block font-sans">Radius</span>
                <span className="text-white font-bold">{previewObject.radius_km?.toLocaleString()} km</span>
              </div>
              <div className="p-2 rounded-xl bg-white/5">
                <span className="text-[10px] text-slate-400 block font-sans">Surface g</span>
                <span className="text-white font-bold">{previewObject.surface_gravity_m_s2 || '—'} m/s²</span>
              </div>
            </div>

            <div className="flex justify-end space-x-2 pt-2">
              <Link
                to={`/object/${previewObject.id}`}
                className="px-4 py-2 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-semibold text-xs flex items-center space-x-1"
              >
                <span>Full Astrometric Profile</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
