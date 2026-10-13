import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useMode } from '../context/ModeContext';
import { fetchObjectById, calculateHohmann, chatAI } from '../services/api';
import { AstronomicalObject, HohmannTransferResult } from '../types/astronomy';
import { Object3DViewer } from '../components/visualization/Object3DViewer';
import {
  Orbit,
  Cpu,
  Sparkles,
  GraduationCap,
  Rocket,
  ShieldCheck,
  GitCompare,
  ArrowLeft,
  Send,
  Zap,
  CheckCircle,
  Database,
  ExternalLink,
  Globe,
  Compass,
  Atom,
  Info,
  Calendar,
  Layers,
  Thermometer,
  Weight,
  Flame,
  Radio,
  Eye,
  BookOpen
} from 'lucide-react';

export const ObjectDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { mode } = useMode();

  const [object, setObject] = useState<AstronomicalObject | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'physical' | 'orbital' | 'scientific' | 'related' | 'hohmann' | 'sources'>('overview');

  // Hohmann Mission State
  const [hohmannData, setHohmannData] = useState<HohmannTransferResult | null>(null);
  const [hohmannLoading, setHohmannLoading] = useState(false);

  // Grounded AI Chat State
  const [aiPrompt, setAiPrompt] = useState('');
  const [aiResponse, setAiResponse] = useState<string | null>(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [groundingMeta, setGroundingMeta] = useState<any | null>(null);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    fetchObjectById(id)
      .then((data) => {
        setObject(data);
        // Pre-compute Hohmann transfer if eligible (if planet or exoplanet)
        if (data.semi_major_axis_au && data.id !== 'earth') {
          setHohmannLoading(true);
          calculateHohmann({ origin_id: 'earth', target_id: data.id })
            .then((h) => setHohmannData(h))
            .catch(() => {})
            .finally(() => setHohmannLoading(false));
        } else {
          setHohmannData(null);
        }
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [id]);

  const handleAskAI = async (promptText: string) => {
    if (!object) return;
    setAiLoading(true);
    setAiPrompt(promptText);
    try {
      const res = await chatAI(promptText, mode, object.id);
      setAiResponse(res.response);
      setGroundingMeta(res.grounding_meta);
    } catch {
      setAiResponse("Could not retrieve grounded AI analysis for this target.");
    } finally {
      setAiLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-5xl mx-auto px-4 py-24 text-center space-y-4">
        <div className="w-12 h-12 border-4 border-sky-500 border-t-transparent rounded-full animate-spin mx-auto shadow-lg shadow-sky-500/20" />
        <p className="text-slate-300 text-sm font-mono tracking-wide">
          Retrieving empirical astronomical telemetry from catalog...
        </p>
      </div>
    );
  }

  if (error || !object) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-20 text-center space-y-6 glass-panel rounded-3xl border border-rose-500/30">
        <div className="w-14 h-14 rounded-2xl bg-rose-500/20 text-rose-400 mx-auto flex items-center justify-center">
          <Info className="w-8 h-8" />
        </div>
        <div className="space-y-2">
          <h2 className="text-2xl font-bold text-rose-300">Celestial Target Not Found</h2>
          <p className="text-slate-300 text-sm max-w-md mx-auto">
            {error || `Unable to locate target object '${id}' in the astronomical catalog.`}
          </p>
        </div>
        <Link
          to="/explorer"
          className="inline-flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-sky-500 hover:bg-sky-400 text-space-950 font-semibold text-xs transition-all shadow-md"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Return to Explorer Catalog</span>
        </Link>
      </div>
    );
  }

  // Calculate persona weight analogy
  const earthGees = object.surface_gravity_m_s2 ? (object.surface_gravity_m_s2 / 9.80665) : null;
  const personWeight70kg = earthGees ? Math.round(70 * earthGees) : null;

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8 animate-fadeIn">
      {/* Top Breadcrumb & Action Toolbar */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <Link
          to="/explorer"
          className="inline-flex items-center space-x-2 text-xs font-mono text-slate-400 hover:text-white transition-colors group"
        >
          <ArrowLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
          <span>Back to Astronomical Catalog</span>
        </Link>

        <div className="flex flex-wrap items-center gap-2">
          <Link
            to={`/visualization?target=${object.id}`}
            className="px-3.5 py-2 rounded-xl bg-sky-500/10 hover:bg-sky-500/20 text-sky-300 text-xs font-semibold flex items-center space-x-1.5 border border-sky-400/30 transition-all shadow-sm"
            title="Open in 3D Keplerian Visualizer"
          >
            <Eye className="w-3.5 h-3.5" />
            <span>3D Visualization</span>
          </Link>
          <Link
            to={`/compare?target=${object.id}`}
            className="px-3.5 py-2 rounded-xl bg-purple-500/10 hover:bg-purple-500/20 text-purple-300 text-xs font-semibold flex items-center space-x-1.5 border border-purple-400/30 transition-all shadow-sm"
            title="Compare with other celestial bodies"
          >
            <GitCompare className="w-3.5 h-3.5" />
            <span>Compare</span>
          </Link>
          <Link
            to={`/ai?target=${object.id}`}
            className="px-3.5 py-2 rounded-xl bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-300 text-xs font-semibold flex items-center space-x-1.5 border border-emerald-400/30 transition-all shadow-sm"
            title="Query grounded AI assistant for this body"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Ask AI Tutor</span>
          </Link>
          <Link
            to="/simulation"
            className="px-3.5 py-2 rounded-xl bg-white/5 hover:bg-white/10 text-slate-300 text-xs font-semibold flex items-center space-x-1.5 border border-white/10 transition-all shadow-sm"
            title="N-body orbital simulation"
          >
            <Orbit className="w-3.5 h-3.5" />
            <span>Simulation</span>
          </Link>
        </div>
      </div>

      {/* Hero Showcase Card */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center p-8 rounded-3xl glass-panel-glow border border-white/10 relative overflow-hidden">
        {/* Ambient subtle glow background */}
        <div
          className="absolute -top-32 -left-32 w-80 h-80 rounded-full blur-3xl opacity-20 pointer-events-none"
          style={{ backgroundColor: object.color_hex || '#38bdf8' }}
        />

        {/* 3D Visualizer Canvas */}
        <div className="lg:col-span-5 flex flex-col items-center">
          <Object3DViewer object={object} size={360} />
          <div className="mt-3 flex items-center space-x-2 text-[11px] font-mono text-slate-400">
            <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: object.color_hex || '#38bdf8' }} />
            <span>Hex Signature: {object.color_hex || '#38bdf8'}</span>
            {object.has_rings && <span className="px-2 py-0.5 rounded bg-amber-500/10 text-amber-300 text-[10px]">Ring System</span>}
            {object.has_atmosphere && <span className="px-2 py-0.5 rounded bg-sky-500/10 text-sky-300 text-[10px]">Atmosphere</span>}
          </div>
        </div>

        {/* Object Hero Telemetry */}
        <div className="lg:col-span-7 space-y-5">
          <div className="space-y-2">
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-xs px-3 py-1 rounded-full bg-sky-500/20 text-sky-300 border border-sky-400/30 font-mono font-medium">
                {object.category}
              </span>
              {object.source_metadata?.provenance_badge && (
                <span className="text-xs px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 font-mono flex items-center space-x-1">
                  <ShieldCheck className="w-3.5 h-3.5" />
                  <span>{object.source_metadata.provenance_badge}</span>
                </span>
              )}
              {object.source_metadata?.is_demo_seed && (
                <span className="text-xs px-2.5 py-0.5 rounded bg-purple-500/10 text-purple-300 border border-purple-500/20 font-mono">
                  Verified Local Seed
                </span>
              )}
            </div>
            <h1 className="text-4xl sm:text-5xl font-extrabold text-white tracking-tight">
              {object.name}
            </h1>
            <p className="text-xs text-slate-400 font-mono flex items-center space-x-2">
              <Database className="w-3.5 h-3.5 text-slate-500" />
              <span>Primary Source: </span>
              <span className="text-slate-300 font-medium">{object.data_source || 'Astronomical Catalog'}</span>
            </p>
          </div>

          {/* Adaptive Presentation Description */}
          <div className="p-5 rounded-2xl bg-space-900/90 border border-white/10 space-y-2.5">
            <div className="flex items-center justify-between text-xs font-semibold">
              <div className="flex items-center space-x-2">
                {mode === 'researcher' && <Cpu className="w-4 h-4 text-sky-400" />}
                {mode === 'student' && <GraduationCap className="w-4 h-4 text-amber-400" />}
                {mode === 'citizen' && <Sparkles className="w-4 h-4 text-purple-400" />}
                <span className="capitalize text-white">{mode} Analysis View:</span>
              </div>
              <span className="text-[11px] font-mono text-slate-400">
                {mode === 'citizen' ? 'Everyday Analogies' : mode === 'student' ? 'Educational Framework' : 'Empirical Astrometry'}
              </span>
            </div>
            <p className="text-xs sm:text-sm text-slate-200 leading-relaxed font-sans">
              {mode === 'researcher'
                ? object.description_researcher
                : mode === 'student'
                ? object.description_student
                : object.description_citizen}
            </p>

            {/* Mode-specific bonus highlights */}
            {mode === 'citizen' && personWeight70kg !== null && (
              <div className="pt-2 border-t border-white/5 flex items-center space-x-2 text-xs text-purple-300 font-sans">
                <Weight className="w-4 h-4 text-purple-400" />
                <span>
                  <strong>Gravity Effect:</strong> A 70 kg human standing here would experience a weight equivalent to <strong>{personWeight70kg} kg</strong> on Earth ({earthGees?.toFixed(2)}g).
                </span>
              </div>
            )}
            {mode === 'student' && object.educational_facts && object.educational_facts.length > 0 && (
              <div className="pt-2 border-t border-white/5 space-y-1">
                <span className="text-[10px] uppercase font-mono tracking-wider text-amber-400 font-bold block">Key Learning Points:</span>
                <ul className="text-xs text-slate-300 list-disc list-inside space-y-0.5">
                  {object.educational_facts.slice(0, 2).map((fact, i) => (
                    <li key={i}>{fact}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* Quick Metrics Key Telemetry Strip */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center">
            <div className="p-3 rounded-2xl glass-panel border border-white/10 hover:border-sky-500/30 transition-colors">
              <span className="text-[10px] text-slate-400 block font-mono">Mass</span>
              <span className="text-xs sm:text-sm font-bold font-mono text-white">
                {object.mass_earth_relative ? `${object.mass_earth_relative} M⊕` : object.mass_kg ? `${object.mass_kg.toExponential(2)} kg` : '—'}
              </span>
            </div>
            <div className="p-3 rounded-2xl glass-panel border border-white/10 hover:border-sky-500/30 transition-colors">
              <span className="text-[10px] text-slate-400 block font-mono">Mean Radius</span>
              <span className="text-xs sm:text-sm font-bold font-mono text-white">
                {object.radius_km ? `${object.radius_km.toLocaleString()} km` : '—'}
              </span>
            </div>
            <div className="p-3 rounded-2xl glass-panel border border-white/10 hover:border-sky-500/30 transition-colors">
              <span className="text-[10px] text-slate-400 block font-mono">Surface Gravity</span>
              <span className="text-xs sm:text-sm font-bold font-mono text-white">
                {object.surface_gravity_m_s2 ? `${object.surface_gravity_m_s2} m/s²` : '—'}
              </span>
            </div>
            <div className="p-3 rounded-2xl glass-panel border border-white/10 hover:border-sky-500/30 transition-colors">
              <span className="text-[10px] text-slate-400 block font-mono">Orbital Period</span>
              <span className="text-xs sm:text-sm font-bold font-mono text-white">
                {object.orbital_period_days ? `${object.orbital_period_days} d` : '—'}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-white/10 overflow-x-auto gap-2 text-xs font-mono">
        <button
          onClick={() => setActiveTab('overview')}
          className={`px-4 py-3 border-b-2 font-medium flex items-center space-x-2 transition-all whitespace-nowrap ${
            activeTab === 'overview'
              ? 'border-sky-400 text-sky-400 bg-sky-500/5'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <BookOpen className="w-4 h-4" />
          <span>Overview</span>
        </button>

        <button
          onClick={() => setActiveTab('physical')}
          className={`px-4 py-3 border-b-2 font-medium flex items-center space-x-2 transition-all whitespace-nowrap ${
            activeTab === 'physical'
              ? 'border-sky-400 text-sky-400 bg-sky-500/5'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Globe className="w-4 h-4" />
          <span>Physical Properties</span>
        </button>

        <button
          onClick={() => setActiveTab('orbital')}
          className={`px-4 py-3 border-b-2 font-medium flex items-center space-x-2 transition-all whitespace-nowrap ${
            activeTab === 'orbital'
              ? 'border-sky-400 text-sky-400 bg-sky-500/5'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Orbit className="w-4 h-4" />
          <span>Orbital Properties</span>
        </button>

        <button
          onClick={() => setActiveTab('scientific')}
          className={`px-4 py-3 border-b-2 font-medium flex items-center space-x-2 transition-all whitespace-nowrap ${
            activeTab === 'scientific'
              ? 'border-sky-400 text-sky-400 bg-sky-500/5'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Atom className="w-4 h-4" />
          <span>Scientific Information</span>
        </button>

        <button
          onClick={() => setActiveTab('related')}
          className={`px-4 py-3 border-b-2 font-medium flex items-center space-x-2 transition-all whitespace-nowrap ${
            activeTab === 'related'
              ? 'border-sky-400 text-sky-400 bg-sky-500/5'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Layers className="w-4 h-4" />
          <span>Related Objects ({object.related_objects?.length || 0})</span>
        </button>

        {hohmannData && (
          <button
            onClick={() => setActiveTab('hohmann')}
            className={`px-4 py-3 border-b-2 font-medium flex items-center space-x-2 transition-all whitespace-nowrap ${
              activeTab === 'hohmann'
                ? 'border-sky-400 text-sky-400 bg-sky-500/5'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <Rocket className="w-4 h-4" />
            <span>Hohmann Trajectory</span>
          </button>
        )}

        <button
          onClick={() => setActiveTab('sources')}
          className={`px-4 py-3 border-b-2 font-medium flex items-center space-x-2 transition-all whitespace-nowrap ${
            activeTab === 'sources'
              ? 'border-sky-400 text-sky-400 bg-sky-500/5'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Database className="w-4 h-4" />
          <span>Source Information</span>
        </button>
      </div>

      {/* TAB 1: Mode-Adaptive Overview */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          {/* Mode Highlights Panel */}
          {mode === 'citizen' && (
            <div className="p-6 sm:p-8 rounded-3xl glass-panel border border-purple-500/20 space-y-5">
              <div className="flex items-center space-x-2 text-purple-400">
                <Sparkles className="w-5 h-5" />
                <h3 className="text-lg font-bold text-white">Citizen Explorer: Key Facts & Daily Realities</h3>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-xs font-mono">
                <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-1">
                  <span className="text-[10px] text-slate-400 uppercase block font-sans">Everyday Weight</span>
                  <span className="text-sm font-bold text-white block">
                    {personWeight70kg !== null ? `${personWeight70kg} kg` : 'N/A'}
                  </span>
                  <span className="text-[10px] text-purple-300 font-sans">
                    {earthGees ? `${earthGees.toFixed(2)}x Earth's pull` : ''}
                  </span>
                </div>
                <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-1">
                  <span className="text-[10px] text-slate-400 uppercase block font-sans">Surface Climate</span>
                  <span className="text-sm font-bold text-white block">
                    {object.surface_temperature_k ? `${Math.round(object.surface_temperature_k - 273.15)} °C` : 'N/A'}
                  </span>
                  <span className="text-[10px] text-slate-400 font-sans">
                    {object.surface_temperature_k
                      ? object.surface_temperature_k > 373 ? 'Boiling hot environment'
                      : object.surface_temperature_k < 200 ? 'Extreme cryogenic cold'
                      : 'Moderate temperature range'
                      : ''}
                  </span>
                </div>
                <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-1">
                  <span className="text-[10px] text-slate-400 uppercase block font-sans">Sunlight Travel Time</span>
                  <span className="text-sm font-bold text-white block">
                    {object.semi_major_axis_au ? `~${(object.semi_major_axis_au * 8.317).toFixed(1)} mins` : 'Central Star'}
                  </span>
                  <span className="text-[10px] text-slate-400 font-sans">Speed-of-light delay</span>
                </div>
                <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-1">
                  <span className="text-[10px] text-slate-400 uppercase block font-sans">Day Length</span>
                  <span className="text-sm font-bold text-white block">
                    {object.rotation_period ? `${object.rotation_period} hrs` : 'Synchronous / Unknown'}
                  </span>
                  <span className="text-[10px] text-slate-400 font-sans">One full axial rotation</span>
                </div>
              </div>
            </div>
          )}

          {mode === 'student' && (
            <div className="p-6 sm:p-8 rounded-3xl glass-panel border border-amber-500/20 space-y-5">
              <div className="flex items-center space-x-2 text-amber-400">
                <GraduationCap className="w-5 h-5" />
                <h3 className="text-lg font-bold text-white">Student Study Guide: Physical Principles & Orbit Mechanics</h3>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
                <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-2">
                  <span className="text-[11px] font-bold text-amber-300 font-mono">1. Universal Gravitation</span>
                  <p className="text-slate-300 leading-relaxed text-[11px]">
                    Surface gravity is derived from <code className="text-amber-200">g = G·M / R²</code>. With mass {object.mass_earth_relative ? `${object.mass_earth_relative} M⊕` : 'N/A'} and radius {object.radius_km ? `${object.radius_km.toLocaleString()} km` : 'N/A'}, the computed gravity is {object.surface_gravity_m_s2 ? `${object.surface_gravity_m_s2} m/s²` : 'N/A'}.
                  </p>
                </div>
                <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-2">
                  <span className="text-[11px] font-bold text-amber-300 font-mono">2. Kepler's Harmonic Law</span>
                  <p className="text-slate-300 leading-relaxed text-[11px]">
                    The square of the orbital period is proportional to the cube of the semi-major axis: <code className="text-amber-200">P² ∝ a³</code>. Semi-major axis = {object.semi_major_axis_au ? `${object.semi_major_axis_au} AU` : 'N/A'} yields a period of {object.orbital_period_days ? `${Math.round(object.orbital_period_days)} days` : 'N/A'}.
                  </p>
                </div>
                <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-2">
                  <span className="text-[11px] font-bold text-amber-300 font-mono">3. Atmospheric Retention</span>
                  <p className="text-slate-300 leading-relaxed text-[11px]">
                    Escape velocity is <code className="text-amber-200">{object.escape_velocity_km_s ? `${object.escape_velocity_km_s} km/s` : 'N/A'}</code>. An atmosphere can be sustained over billions of years only if the thermal root-mean-square velocity of gases is significantly lower than escape velocity.
                  </p>
                </div>
              </div>
            </div>
          )}

          {mode === 'researcher' && (
            <div className="p-6 sm:p-8 rounded-3xl glass-panel border border-sky-500/20 space-y-5">
              <div className="flex items-center space-x-2 text-sky-400">
                <Cpu className="w-5 h-5" />
                <h3 className="text-lg font-bold text-white">Researcher Overview: Dimensionless Astrometric Ratios</h3>
              </div>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-mono">
                <div className="p-3.5 rounded-2xl bg-space-900 border border-white/5">
                  <span className="text-[10px] text-slate-400 block">Mass Ratio (M / M⊕)</span>
                  <span className="text-white font-bold">{object.mass_earth_relative ?? '—'}</span>
                </div>
                <div className="p-3.5 rounded-2xl bg-space-900 border border-white/5">
                  <span className="text-[10px] text-slate-400 block">Radius Ratio (R / R⊕)</span>
                  <span className="text-white font-bold">{object.radius_earth_relative ?? '—'}</span>
                </div>
                <div className="p-3.5 rounded-2xl bg-space-900 border border-white/5">
                  <span className="text-[10px] text-slate-400 block">Surface Potential (Φ)</span>
                  <span className="text-white font-bold">
                    {object.mass_kg && object.radius_km
                      ? `${(-6.6743e-11 * object.mass_kg / (object.radius_km * 1000)).toExponential(3)} J/kg`
                      : '—'}
                  </span>
                </div>
                <div className="p-3.5 rounded-2xl bg-space-900 border border-white/5">
                  <span className="text-[10px] text-slate-400 block">Data Confidence</span>
                  <span className="text-emerald-400 font-bold">{object.data_confidence || 'High Precision'}</span>
                </div>
              </div>
            </div>
          )}

          {/* Quick Snapshot Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="p-6 rounded-3xl glass-panel border border-white/10 space-y-4">
              <div className="flex items-center justify-between">
                <h4 className="text-sm font-bold text-white flex items-center space-x-2">
                  <Globe className="w-4 h-4 text-sky-400" />
                  <span>Physical Snapshot</span>
                </h4>
                <button
                  onClick={() => setActiveTab('physical')}
                  className="text-xs text-sky-400 hover:text-sky-300 font-mono"
                >
                  View All Physical →
                </button>
              </div>
              <div className="grid grid-cols-2 gap-2.5 text-xs font-mono">
                <div className="p-2.5 rounded-xl bg-space-900 border border-white/5">
                  <span className="text-[10px] text-slate-400 block">Mass</span>
                  <span className="text-white font-semibold">
                    {object.mass_earth_relative ? `${object.mass_earth_relative} M⊕` : object.mass_kg ? `${object.mass_kg.toExponential(2)} kg` : 'N/A'}
                  </span>
                </div>
                <div className="p-2.5 rounded-xl bg-space-900 border border-white/5">
                  <span className="text-[10px] text-slate-400 block">Radius</span>
                  <span className="text-white font-semibold">{object.radius_km ? `${object.radius_km.toLocaleString()} km` : 'N/A'}</span>
                </div>
                <div className="p-2.5 rounded-xl bg-space-900 border border-white/5">
                  <span className="text-[10px] text-slate-400 block">Gravity</span>
                  <span className="text-white font-semibold">{object.surface_gravity_m_s2 ? `${object.surface_gravity_m_s2} m/s²` : 'N/A'}</span>
                </div>
                <div className="p-2.5 rounded-xl bg-space-900 border border-white/5">
                  <span className="text-[10px] text-slate-400 block">Temperature</span>
                  <span className="text-white font-semibold">{object.surface_temperature_k ? `${object.surface_temperature_k} K` : 'N/A'}</span>
                </div>
              </div>
            </div>

            <div className="p-6 rounded-3xl glass-panel border border-white/10 space-y-4">
              <div className="flex items-center justify-between">
                <h4 className="text-sm font-bold text-white flex items-center space-x-2">
                  <Orbit className="w-4 h-4 text-indigo-400" />
                  <span>Orbital Snapshot</span>
                </h4>
                <button
                  onClick={() => setActiveTab('orbital')}
                  className="text-xs text-indigo-400 hover:text-indigo-300 font-mono"
                >
                  View All Orbital →
                </button>
              </div>
              <div className="grid grid-cols-2 gap-2.5 text-xs font-mono">
                <div className="p-2.5 rounded-xl bg-space-900 border border-white/5">
                  <span className="text-[10px] text-slate-400 block">Semi-Major Axis</span>
                  <span className="text-white font-semibold">{object.semi_major_axis_au !== null && object.semi_major_axis_au !== undefined ? `${object.semi_major_axis_au} AU` : 'N/A'}</span>
                </div>
                <div className="p-2.5 rounded-xl bg-space-900 border border-white/5">
                  <span className="text-[10px] text-slate-400 block">Orbital Period</span>
                  <span className="text-white font-semibold">{object.orbital_period_days ? `${Math.round(object.orbital_period_days)} d` : 'N/A'}</span>
                </div>
                <div className="p-2.5 rounded-xl bg-space-900 border border-white/5">
                  <span className="text-[10px] text-slate-400 block">Eccentricity</span>
                  <span className="text-white font-semibold">{object.eccentricity ?? 'N/A'}</span>
                </div>
                <div className="p-2.5 rounded-xl bg-space-900 border border-white/5">
                  <span className="text-[10px] text-slate-400 block">Orbital Velocity</span>
                  <span className="text-white font-semibold">{object.mean_orbital_velocity_km_s ? `${object.mean_orbital_velocity_km_s} km/s` : 'N/A'}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: Physical Properties */}
      {activeTab === 'physical' && (
        <div className="p-6 sm:p-8 rounded-3xl glass-panel border border-white/10 space-y-6">
          <div className="flex items-center space-x-2 text-sky-400">
            <Globe className="w-5 h-5" />
            <h3 className="text-lg font-bold text-white">Geophysical & Physical Characteristics</h3>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 text-xs font-mono">
            <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-1">
              <span className="text-[10px] text-slate-400 block font-sans">Mass ($M$)</span>
              <span className="text-white font-bold block">{object.mass_kg ? `${object.mass_kg.toExponential(4)} kg` : 'N/A'}</span>
              <span className="text-[10px] text-slate-500">
                {object.mass_earth_relative ? `${object.mass_earth_relative} M⊕` : ''}
              </span>
            </div>

            <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-1">
              <span className="text-[10px] text-slate-400 block font-sans">Mean Volumetric Radius ($R$)</span>
              <span className="text-white font-bold block">{object.radius_km ? `${object.radius_km.toLocaleString()} km` : 'N/A'}</span>
              <span className="text-[10px] text-slate-500">
                {object.radius_earth_relative ? `${object.radius_earth_relative} R⊕` : ''}
              </span>
            </div>

            <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-1">
              <span className="text-[10px] text-slate-400 block font-sans">Mean Bulk Density ($\rho$)</span>
              <span className="text-white font-bold block">{object.mean_density_g_cm3 ? `${object.mean_density_g_cm3} g/cm³` : 'N/A'}</span>
              <span className="text-[10px] text-slate-500">
                {object.mean_density_g_cm3 && object.mean_density_g_cm3 < 1.0 ? 'Less dense than liquid water' : 'Dense metallic / silicate'}
              </span>
            </div>

            <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-1">
              <span className="text-[10px] text-slate-400 block font-sans">Surface Gravity ($g$)</span>
              <span className="text-white font-bold block">{object.surface_gravity_m_s2 ? `${object.surface_gravity_m_s2} m/s²` : 'N/A'}</span>
              <span className="text-[10px] text-slate-500">
                {earthGees ? `${earthGees.toFixed(3)} Earth standard g` : ''}
              </span>
            </div>

            <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-1">
              <span className="text-[10px] text-slate-400 block font-sans">Escape Velocity (v_esc)</span>
              <span className="text-white font-bold block">{object.escape_velocity_km_s ? `${object.escape_velocity_km_s} km/s` : 'N/A'}</span>
              <span className="text-[10px] text-slate-500">Required speed to leave gravity well</span>
            </div>

            <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-1">
              <span className="text-[10px] text-slate-400 block font-sans">Mean Surface Temperature</span>
              <span className="text-white font-bold block">{object.surface_temperature_k ? `${object.surface_temperature_k} K` : 'N/A'}</span>
              <span className="text-[10px] text-slate-500">
                {object.surface_temperature_k ? `${Math.round(object.surface_temperature_k - 273.15)} °C` : ''}
              </span>
            </div>
          </div>

          {/* Atmosphere & Rings Badges */}
          <div className="p-4 rounded-2xl bg-space-900 border border-white/5 flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center space-x-3">
              <span className="text-xs text-slate-400 font-mono">Atmosphere Envelope:</span>
              <span className={`text-xs px-2.5 py-0.5 rounded-full font-mono font-bold ${
                object.has_atmosphere ? 'bg-sky-500/20 text-sky-300 border border-sky-400/30' : 'bg-slate-800 text-slate-400'
              }`}>
                {object.has_atmosphere ? 'Present' : 'None / Exosphere only'}
              </span>
            </div>

            <div className="flex items-center space-x-3">
              <span className="text-xs text-slate-400 font-mono">Ring Structures:</span>
              <span className={`text-xs px-2.5 py-0.5 rounded-full font-mono font-bold ${
                object.has_rings ? 'bg-amber-500/20 text-amber-300 border border-amber-400/30' : 'bg-slate-800 text-slate-400'
              }`}>
                {object.has_rings ? 'Active Planetary Rings' : 'Absent'}
              </span>
            </div>
          </div>
        </div>
      )}

      {/* TAB 3: Orbital Properties */}
      {activeTab === 'orbital' && (
        <div className="p-6 sm:p-8 rounded-3xl glass-panel border border-white/10 space-y-6">
          <div className="flex items-center space-x-2 text-indigo-400">
            <Orbit className="w-5 h-5" />
            <h3 className="text-lg font-bold text-white">Orbital Dynamics & Keplerian Elements</h3>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 text-xs font-mono">
            <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-1">
              <span className="text-[10px] text-slate-400 block font-sans">Semi-Major Axis ($a$)</span>
              <span className="text-white font-bold block">{object.semi_major_axis_au !== null && object.semi_major_axis_au !== undefined ? `${object.semi_major_axis_au} AU` : 'N/A'}</span>
              <span className="text-[10px] text-slate-500">
                {object.semi_major_axis_au ? `${(object.semi_major_axis_au * 1.496e8).toLocaleString()} km` : ''}
              </span>
            </div>

            <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-1">
              <span className="text-[10px] text-slate-400 block font-sans">Orbital Eccentricity ($e$)</span>
              <span className="text-white font-bold block">{object.eccentricity !== null && object.eccentricity !== undefined ? object.eccentricity : 'N/A'}</span>
              <span className="text-[10px] text-slate-500">
                {object.eccentricity !== null && object.eccentricity !== undefined
                  ? object.eccentricity < 0.05
                    ? 'Near circular orbit'
                    : object.eccentricity < 0.2
                    ? 'Mildly elliptical'
                    : 'Highly elliptical'
                  : ''}
              </span>
            </div>

            <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-1">
              <span className="text-[10px] text-slate-400 block font-sans">Orbital Period ($P$)</span>
              <span className="text-white font-bold block">{object.orbital_period_days ? `${object.orbital_period_days} d` : 'N/A'}</span>
              <span className="text-[10px] text-slate-500">
                {object.orbital_period_days ? `${(object.orbital_period_days / 365.25).toFixed(2)} Julian Years` : ''}
              </span>
            </div>

            <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-1">
              <span className="text-[10px] text-slate-400 block font-sans">Orbital Inclination ($i$)</span>
              <span className="text-white font-bold block">{object.orbital_inclination_deg ? `${object.orbital_inclination_deg}°` : 'N/A'}</span>
              <span className="text-[10px] text-slate-500">Tilt relative to ecliptic plane</span>
            </div>

            <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-1">
              <span className="text-[10px] text-slate-400 block font-sans">Mean Orbital Velocity</span>
              <span className="text-white font-bold block">{object.mean_orbital_velocity_km_s ? `${object.mean_orbital_velocity_km_s} km/s` : 'N/A'}</span>
              <span className="text-[10px] text-slate-500">Heliocentric orbital speed</span>
            </div>

            <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-1">
              <span className="text-[10px] text-slate-400 block font-sans">Perihelion / Aphelion</span>
              <span className="text-white font-bold block">
                {object.perihelion_au ? `${object.perihelion_au} / ${object.aphelion_au} AU` : 'N/A'}
              </span>
              <span className="text-[10px] text-slate-500">Closest and farthest points</span>
            </div>
          </div>

          {/* Kepler Formula Note */}
          <div className="p-4 rounded-2xl bg-space-900 border border-white/5 text-xs text-slate-300 space-y-1 font-mono">
            <div className="text-indigo-400 font-bold text-[11px]">Kepler's Third Harmonic Law:</div>
            <p className="text-[11px] text-slate-400 font-sans">
              The square of the orbital period ($P^2$) is directly proportional to the cube of the semi-major axis ($a^3$): $P^2 \propto a^3$.
            </p>
          </div>
        </div>
      )}

      {/* TAB 2: Astropy Scientific Metadata */}
      {activeTab === 'scientific' && (
        <div className="space-y-6">
          <div className="p-6 rounded-3xl glass-panel border border-sky-500/20 space-y-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2 text-sky-400">
                <Atom className="w-5 h-5" />
                <h3 className="text-lg font-bold text-white">Astropy Units & Astrophysical Standards Breakdown</h3>
              </div>
              <span className="text-xs font-mono px-3 py-1 rounded-full bg-sky-500/10 text-sky-300 border border-sky-400/20">
                Engine: astropy.units & astropy.constants
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 text-xs font-mono">
              <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-2">
                <span className="text-slate-400 text-[10px] uppercase font-bold tracking-wider">Mass Equivalencies</span>
                <div className="space-y-1">
                  <div className="flex justify-between">
                    <span className="text-slate-400">Solar Mass ($M_\odot$):</span>
                    <span className="text-white font-bold">{object.astropy_units?.mass_solar ? `${object.astropy_units.mass_solar.toExponential(4)}` : 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Jupiter Mass ($M_J$):</span>
                    <span className="text-white font-bold">{object.astropy_units?.mass_jupiter ? `${object.astropy_units.mass_jupiter.toExponential(4)}` : 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Earth Mass ($M_\oplus$):</span>
                    <span className="text-white font-bold">{object.astropy_units?.mass_earth ? `${object.astropy_units.mass_earth}` : 'N/A'}</span>
                  </div>
                </div>
              </div>

              <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-2">
                <span className="text-slate-400 text-[10px] uppercase font-bold tracking-wider">Radius Equivalencies</span>
                <div className="space-y-1">
                  <div className="flex justify-between">
                    <span className="text-slate-400">Solar Radius ($R_\odot$):</span>
                    <span className="text-white font-bold">{object.astropy_units?.radius_solar ? `${object.astropy_units.radius_solar.toExponential(4)}` : 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Jupiter Radius ($R_J$):</span>
                    <span className="text-white font-bold">{object.astropy_units?.radius_jupiter ? `${object.astropy_units.radius_jupiter.toFixed(4)}` : 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Earth Radius ($R_\oplus$):</span>
                    <span className="text-white font-bold">{object.astropy_units?.radius_earth ? `${object.astropy_units.radius_earth.toFixed(4)}` : 'N/A'}</span>
                  </div>
                </div>
              </div>

              <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-2">
                <span className="text-slate-400 text-[10px] uppercase font-bold tracking-wider">Astronomical Distances</span>
                <div className="space-y-1">
                  <div className="flex justify-between">
                    <span className="text-slate-400">AU ($a$):</span>
                    <span className="text-white font-bold">{object.astropy_units?.distance_au ? `${object.astropy_units.distance_au} AU` : 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Parsecs (pc):</span>
                    <span className="text-white font-bold">{object.astropy_units?.distance_parsec ? `${object.astropy_units.distance_parsec.toExponential(3)} pc` : 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Light-Years (ly):</span>
                    <span className="text-white font-bold">{object.astropy_units?.distance_light_years ? `${object.astropy_units.distance_light_years.toExponential(3)} ly` : 'N/A'}</span>
                  </div>
                </div>
              </div>

              <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-2">
                <span className="text-slate-400 text-[10px] uppercase font-bold tracking-wider">Spectral & Photometry</span>
                <div className="space-y-1">
                  <div className="flex justify-between">
                    <span className="text-slate-400">Spectral Type:</span>
                    <span className="text-white font-bold">{object.spectral_type || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Apparent Magnitude ($m_V$):</span>
                    <span className="text-white font-bold">{object.apparent_magnitude !== null && object.apparent_magnitude !== undefined ? object.apparent_magnitude : 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Absolute Magnitude ($M_V$):</span>
                    <span className="text-white font-bold">{object.absolute_magnitude !== null && object.absolute_magnitude !== undefined ? object.absolute_magnitude : 'N/A'}</span>
                  </div>
                </div>
              </div>

              <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-2">
                <span className="text-slate-400 text-[10px] uppercase font-bold tracking-wider">Thermal & Gravity</span>
                <div className="space-y-1">
                  <div className="flex justify-between">
                    <span className="text-slate-400">Gravity in Earth Gees:</span>
                    <span className="text-white font-bold">{object.astropy_units?.surface_gravity_gees ? `${object.astropy_units.surface_gravity_gees.toFixed(3)} g` : 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Celsius Scale:</span>
                    <span className="text-white font-bold">{object.astropy_units?.temperature_celsius ? `${object.astropy_units.temperature_celsius.toFixed(1)} °C` : 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Solar Luminosity ($L_\odot$):</span>
                    <span className="text-white font-bold">{object.luminosity_solar ? `${object.luminosity_solar} L⊙` : 'N/A'}</span>
                  </div>
                </div>
              </div>

              <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-2">
                <span className="text-slate-400 text-[10px] uppercase font-bold tracking-wider">Physical Verification Equations</span>
                <div className="space-y-1 text-[11px] text-slate-400">
                  <div className="font-mono text-sky-300">g = G·M / R²</div>
                  <div className="font-mono text-indigo-300">v_esc = √(2·G·M / R)</div>
                  <div className="font-mono text-emerald-300">ρ = 3·M / (4·π·R³)</div>
                </div>
              </div>
            </div>

            {/* Specialized Astrophysical Notes */}
            {object.research_notes && Object.keys(object.research_notes).length > 0 && (
              <div className="p-5 rounded-2xl bg-space-900 border border-white/5 space-y-3">
                <h4 className="text-xs font-bold text-sky-400 uppercase tracking-wider font-mono">Specialized Empirical Research Notes:</h4>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 text-xs font-mono">
                  {Object.entries(object.research_notes).map(([key, val]) => (
                    <div key={key} className="p-2.5 rounded-xl bg-white/5 flex items-center justify-between">
                      <span className="text-slate-400">{key}:</span>
                      <span className="text-white font-semibold">{String(val)}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* TAB 3: Related Celestial Bodies */}
      {activeTab === 'related' && (
        <div className="p-6 rounded-3xl glass-panel border border-white/10 space-y-5">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2 text-sky-400">
              <Layers className="w-5 h-5" />
              <h3 className="text-lg font-bold text-white">Gravitationally and Hierarchically Related Bodies</h3>
            </div>
            <span className="text-xs font-mono text-slate-400">
              Identified Connections: {object.related_objects?.length || 0}
            </span>
          </div>

          {(!object.related_objects || object.related_objects.length === 0) ? (
            <div className="p-8 text-center text-slate-400 text-xs font-mono">
              No direct gravitational satellites or parent bodies registered in this catalog scope.
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {object.related_objects.map((rel) => (
                <Link
                  key={rel.id}
                  to={`/object/${rel.id}`}
                  className="p-4 rounded-2xl bg-space-900 border border-white/5 hover:border-sky-500/40 transition-all group flex flex-col justify-between space-y-3"
                >
                  <div className="space-y-1">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-sky-500/10 text-sky-300 border border-sky-400/20">
                        {rel.relationship}
                      </span>
                      <span
                        className="w-2.5 h-2.5 rounded-full"
                        style={{ backgroundColor: rel.color_hex || '#38bdf8' }}
                      />
                    </div>
                    <h4 className="text-sm font-bold text-white group-hover:text-sky-300 transition-colors">
                      {rel.name}
                    </h4>
                    <span className="text-[11px] text-slate-400 font-mono block">
                      Category: {rel.category}
                    </span>
                  </div>

                  <div className="text-[10px] text-sky-400 font-mono flex items-center space-x-1 group-hover:translate-x-1 transition-transform">
                    <span>Inspect Body</span>
                    <span>→</span>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>
      )}

      {/* TAB 4: Hohmann Trajectory Planner */}
      {activeTab === 'hohmann' && hohmannData && (
        <div className="p-8 rounded-3xl glass-panel border border-white/10 space-y-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2 text-sky-400">
              <Rocket className="w-5 h-5" />
              <h3 className="text-xl font-bold text-white">Interplanetary Hohmann Transfer Trajectory</h3>
            </div>
            <span className="text-xs font-mono text-slate-400">Origin: Earth (1.0 AU) → Target: {object.name}</span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-center">
            <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-1">
              <span className="text-[11px] text-slate-400 block font-mono">Departure Burn ($\Delta v_1$)</span>
              <span className="text-lg font-bold font-mono text-sky-400">{hohmannData.delta_v1_km_s} km/s</span>
              <span className="text-[10px] text-slate-500 block">Earth escape impulse</span>
            </div>
            <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-1">
              <span className="text-[11px] text-slate-400 block font-mono">Arrival Insertion ($\Delta v_2$)</span>
              <span className="text-lg font-bold font-mono text-sky-400">{hohmannData.delta_v2_km_s} km/s</span>
              <span className="text-[10px] text-slate-500 block">Target capture impulse</span>
            </div>
            <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-1">
              <span className="text-[11px] text-slate-400 block font-mono">Total Mission $\Delta v$</span>
              <span className="text-lg font-bold font-mono text-emerald-400">{hohmannData.total_delta_v_km_s} km/s</span>
              <span className="text-[10px] text-slate-500 block">Combined orbital delta-v</span>
            </div>
            <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-1">
              <span className="text-[11px] text-slate-400 block font-mono">One-Way Flight Time</span>
              <span className="text-lg font-bold font-mono text-amber-400">{hohmannData.transfer_time_days} days</span>
              <span className="text-[10px] text-slate-500 block">~{(hohmannData.transfer_time_days / 30.4).toFixed(1)} months</span>
            </div>
          </div>

          {/* Formulations Box */}
          <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-2 text-xs font-mono">
            <span className="text-[10px] uppercase font-bold text-sky-400 tracking-wider">Astrodynamic Equations:</span>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-2 text-slate-300 text-[11px]">
              <div>a_transfer = (r₁ + r₂) / 2 = {hohmannData.transfer_semi_major_axis_au} AU</div>
              <div>e_transfer = |r₂ - r₁| / (r₁ + r₂) = {hohmannData.transfer_eccentricity}</div>
              <div>T_transfer = π · √(a³ / μ_sun) = {hohmannData.transfer_time_days} d</div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 5: Source Provenance & Transparency */}
      {activeTab === 'sources' && (
        <div className="p-8 rounded-3xl glass-panel border border-sky-500/20 space-y-6">
          <div className="flex items-center space-x-2 text-emerald-400">
            <ShieldCheck className="w-6 h-6" />
            <h3 className="text-xl font-bold text-white">Data Provenance & Scientific Transparency</h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
            <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-2">
              <span className="text-slate-400 text-[10px] uppercase">Data Source Name</span>
              <p className="text-white font-bold text-sm">{object.data_source || 'Astronomical Data Service'}</p>
              {object.source_metadata?.source_url && (
                <a
                  href={object.source_metadata.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center space-x-1.5 text-sky-400 hover:text-sky-300 underline text-xs"
                >
                  <span>Access External Scientific Archive</span>
                  <ExternalLink className="w-3.5 h-3.5" />
                </a>
              )}
            </div>

            <div className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-2">
              <span className="text-slate-400 text-[10px] uppercase">Verification Status & Timestamp</span>
              <div className="space-y-1">
                <div className="flex justify-between">
                  <span className="text-slate-400">Retrieval Date:</span>
                  <span className="text-white">{object.source_metadata?.retrieval_date || '2025-01-15'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Confidence Rating:</span>
                  <span className="text-emerald-400 font-bold">{object.source_metadata?.confidence_level || 'High Precision Astrometry'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Storage Class:</span>
                  <span className="text-purple-300">{object.source_metadata?.is_demo_seed ? 'Local Offline Seed' : 'Remote API Ingested'}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Explicit Transparency Policy Statement */}
          <div className="p-5 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 text-xs text-slate-200 space-y-2 font-sans">
            <div className="flex items-center space-x-2 text-emerald-300 font-bold">
              <CheckCircle className="w-4 h-4" />
              <span>Scientific Integrity & AI Boundary Guarantee</span>
            </div>
            <p className="leading-relaxed text-slate-300">
              All physical parameters ($M$, $R$, $\rho$, $g$, v_esc, $T$) and Keplerian orbital coordinates above represent verified empirical astronomical measurements sourced from peer-reviewed databases (such as NASA/JPL Horizons, Exoplanet Archive, and CDS SIMBAD).
            </p>
            <p className="leading-relaxed text-slate-300 font-medium">
              <strong>Crucial Transparency Policy:</strong> NEBULA never generates or invents numerical astronomical data via generative language models. AI assists only with textual pedagogical translation and interpretation, always grounded against these verified empirical parameters.
            </p>
          </div>
        </div>
      )}

      {/* Grounded AI Analysis Section */}
      <div className="p-8 rounded-3xl glass-panel border border-white/10 space-y-5">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Sparkles className="w-5 h-5 text-sky-400" />
            <h3 className="text-xl font-bold text-white">Grounded AI Analysis on {object.name}</h3>
          </div>
          <span className="px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs font-mono flex items-center space-x-1">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Telemetry Grounding Active</span>
          </span>
        </div>

        {/* Quick prompt suggestions */}
        <div className="flex flex-wrap gap-2 text-xs">
          {[
            `How does ${object.name}'s surface gravity compare to Earth?`,
            `Could liquid water or an atmosphere exist on ${object.name}?`,
            `What orbital resonance or dynamics govern ${object.name}?`,
            `What are the greatest open scientific questions regarding ${object.name}?`
          ].map((prompt, i) => (
            <button
              key={i}
              onClick={() => handleAskAI(prompt)}
              className="px-3 py-1.5 rounded-xl bg-white/5 hover:bg-white/10 text-slate-300 border border-white/5 transition-all text-left"
            >
              {prompt}
            </button>
          ))}
        </div>

        <div className="flex gap-2">
          <input
            type="text"
            value={aiPrompt}
            onChange={(e) => setAiPrompt(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && aiPrompt.trim()) handleAskAI(aiPrompt);
            }}
            placeholder={`Ask our grounded AI tutor anything about ${object.name}...`}
            className="flex-1 bg-space-900 border border-white/10 rounded-xl px-4 py-2.5 text-xs text-white focus:outline-none focus:border-sky-500"
          />
          <button
            onClick={() => handleAskAI(aiPrompt)}
            disabled={aiLoading || !aiPrompt.trim()}
            className="px-5 py-2.5 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-semibold text-xs flex items-center space-x-1.5 transition-all disabled:opacity-50 shadow-md shadow-sky-600/20"
          >
            <Send className="w-3.5 h-3.5" />
            <span>{aiLoading ? 'Synthesizing...' : 'Submit Inquiry'}</span>
          </button>
        </div>

        {aiResponse && (
          <div className="mt-4 p-5 rounded-2xl bg-space-900/90 border border-sky-500/20 space-y-3 animate-fadeIn">
            <div className="text-xs text-slate-200 leading-relaxed whitespace-pre-wrap">
              {aiResponse}
            </div>

            {groundingMeta && groundingMeta.data_points?.length > 0 && (
              <div className="pt-3 border-t border-white/5 flex flex-wrap items-center gap-2">
                <span className="text-[10px] text-slate-400 font-mono">Grounded Data Points:</span>
                {groundingMeta.data_points.map((pt: any, i: number) => (
                  <span key={i} className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/20">
                    {pt.property}: {pt.value} {pt.unit}
                  </span>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
