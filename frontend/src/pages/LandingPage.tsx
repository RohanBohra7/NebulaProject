import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useMode } from '../context/ModeContext';
import { fetchObjects } from '../services/api';
import { AstronomicalObject } from '../types/astronomy';
import {
  Orbit,
  Sparkles,
  GraduationCap,
  Cpu,
  Compass,
  Atom,
  BarChart3,
  ArrowRight,
  ShieldCheck,
  Database,
  Layers
} from 'lucide-react';

export const LandingPage: React.FC = () => {
  const { setMode } = useMode();
  const [objects, setObjects] = useState<AstronomicalObject[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchObjects()
      .then((data) => setObjects(data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  const planetCount = objects.filter((o) => o.category === 'Planet').length;
  const exoplanetCount = objects.filter((o) => o.category === 'Exoplanet').length;
  const starCount = objects.filter((o) => o.category === 'Star').length;
  const deepSkyCount = objects.filter((o) => o.category === 'Deep-Sky').length;

  return (
    <div className="space-y-20 pb-20">
      {/* Hero Section */}
      <section className="relative pt-12 lg:pt-20 px-4 text-center max-w-5xl mx-auto space-y-8">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-sky-500/10 border border-sky-400/20 text-sky-300 text-xs font-mono tracking-wide">
          <Sparkles className="w-3.5 h-3.5 animate-pulse" />
          <span>BTech CSE Research Project • Multi-Persona Astronomical Architecture</span>
        </div>

        <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight">
          Explore the Cosmos with{' '}
          <span className="cosmic-gradient-text">Adaptive Intelligence</span>
        </h1>

        <p className="text-lg sm:text-xl text-slate-300 max-w-3xl mx-auto leading-relaxed">
          NEBULA combines high-precision empirical astronomical datasets, symplectic N-body gravitational simulation,
          interactive 3D orbital dynamics, and grounded AI—tailored seamlessly for <strong>Researchers</strong>, <strong>Students</strong>, and <strong>Citizens</strong>.
        </p>

        {/* Action CTAs */}
        <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
          <Link
            to="/visualization"
            className="px-6 py-3 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-semibold flex items-center space-x-2 shadow-lg shadow-sky-500/25 transition-all"
          >
            <Orbit className="w-5 h-5" />
            <span>Launch 3D Solar System</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
          <Link
            to="/mode"
            className="px-6 py-3 rounded-xl glass-panel border border-white/10 hover:border-white/20 text-slate-200 font-medium flex items-center space-x-2 transition-all"
          >
            <Layers className="w-5 h-5 text-purple-400" />
            <span>Select Experience Mode</span>
          </Link>
        </div>

        {/* Live Empirical Stats Bar */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-10">
          <div className="p-4 rounded-xl glass-panel border border-white/10">
            <span className="text-2xl sm:text-3xl font-bold font-mono text-sky-400">
              {loading ? '...' : planetCount}
            </span>
            <p className="text-xs text-slate-400 mt-1 uppercase tracking-wider">Planets & Moons</p>
          </div>
          <div className="p-4 rounded-xl glass-panel border border-white/10">
            <span className="text-2xl sm:text-3xl font-bold font-mono text-purple-400">
              {loading ? '...' : exoplanetCount}
            </span>
            <p className="text-xs text-slate-400 mt-1 uppercase tracking-wider">Exoplanet Worlds</p>
          </div>
          <div className="p-4 rounded-xl glass-panel border border-white/10">
            <span className="text-2xl sm:text-3xl font-bold font-mono text-amber-400">
              {loading ? '...' : starCount}
            </span>
            <p className="text-xs text-slate-400 mt-1 uppercase tracking-wider">Stellar Targets</p>
          </div>
          <div className="p-4 rounded-xl glass-panel border border-white/10">
            <span className="text-2xl sm:text-3xl font-bold font-mono text-rose-400">
              {loading ? '...' : deepSkyCount}
            </span>
            <p className="text-xs text-slate-400 mt-1 uppercase tracking-wider">Deep-Sky Singularities</p>
          </div>
        </div>
      </section>

      {/* The 3 Adaptive Experience Modes */}
      <section className="max-w-7xl mx-auto px-4 space-y-8">
        <div className="text-center space-y-2">
          <h2 className="text-2xl sm:text-3xl font-bold text-white">Three Adaptive Personas, One Scientific Truth</h2>
          <p className="text-sm text-slate-400 max-w-2xl mx-auto">
            The core research contribution is evaluating how presentation, cognitive load, and AI grounding dynamically adapt across different user demographics.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Citizen Mode Card */}
          <div className="p-6 rounded-2xl glass-panel border border-purple-500/20 hover:border-purple-500/40 transition-all flex flex-col justify-between space-y-6">
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400">
                <Sparkles className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-bold text-white">Citizen Experience</h3>
              <p className="text-sm text-slate-300 leading-relaxed">
                Stargazers and curious explorers. Designed for cosmic wonder, high visual fidelity, plain-language explanations, and observation guides.
              </p>
              <ul className="text-xs text-slate-400 space-y-1.5 list-disc list-inside">
                <li>Everyday physical scale analogies</li>
                <li>Cinematic 3D planetary rendering</li>
                <li>Night sky viewing highlights</li>
                <li>Engaging cosmic trivia</li>
              </ul>
            </div>
            <Link
              to="/citizen"
              onClick={() => setMode('citizen')}
              className="w-full py-2.5 rounded-xl bg-purple-600/30 hover:bg-purple-600/50 text-purple-200 border border-purple-400/30 text-center text-xs font-semibold flex items-center justify-center space-x-1.5 transition-all"
            >
              <span>Enter Citizen Mode</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          {/* Student Mode Card */}
          <div className="p-6 rounded-2xl glass-panel border border-amber-500/20 hover:border-amber-500/40 transition-all flex flex-col justify-between space-y-6">
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400">
                <GraduationCap className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-bold text-white">Student Experience</h3>
              <p className="text-sm text-slate-300 leading-relaxed">
                Physics students and educators. Structured educational scaffolding, Kepler's laws sandboxes, interactive quizzes, and Socratic AI tutoring.
              </p>
              <ul className="text-xs text-slate-400 space-y-1.5 list-disc list-inside">
                <li>Kepler & Newton conceptual bridges</li>
                <li>Interactive orbital sandbox experiments</li>
                <li>Active learning comprehension checks</li>
                <li>Curated solar & exoplanet tours</li>
              </ul>
            </div>
            <Link
              to="/student"
              onClick={() => setMode('student')}
              className="w-full py-2.5 rounded-xl bg-amber-600/30 hover:bg-amber-600/50 text-amber-200 border border-amber-400/30 text-center text-xs font-semibold flex items-center justify-center space-x-1.5 transition-all"
            >
              <span>Enter Student Mode</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          {/* Researcher Mode Card */}
          <div className="p-6 rounded-2xl glass-panel border border-sky-500/20 hover:border-sky-500/40 transition-all flex flex-col justify-between space-y-6">
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-xl bg-sky-500/10 border border-sky-400/20 flex items-center justify-center text-sky-400">
                <Cpu className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-bold text-white">Researcher Experience</h3>
              <p className="text-sm text-slate-300 leading-relaxed">
                Astrophysicists and space science scholars. Comprehensive mathematical metadata, Hohmann delta-v solvers, REBOUND N-body integration, and LaTeX formulas.
              </p>
              <ul className="text-xs text-slate-400 space-y-1.5 list-disc list-inside">
                <li>Symplectic Hamiltonian energy error tracking</li>
                <li>Laplace resonance & Hill sphere solvers</li>
                <li>Empirical data citations & Gaia DR3 links</li>
                <li>CSV / JSON catalog telemetry export</li>
              </ul>
            </div>
            <Link
              to="/researcher"
              onClick={() => setMode('researcher')}
              className="w-full py-2.5 rounded-xl bg-sky-600/30 hover:bg-sky-600/50 text-sky-200 border border-sky-400/30 text-center text-xs font-semibold flex items-center justify-center space-x-1.5 transition-all"
            >
              <span>Enter Researcher Mode</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </section>

      {/* Research Contribution: System Architecture Visualization */}
      <section className="max-w-7xl mx-auto px-4 space-y-8">
        <div className="p-8 rounded-3xl glass-panel-glow border border-sky-500/20 space-y-6">
          <div className="max-w-3xl space-y-2">
            <span className="text-xs font-mono uppercase text-sky-400 tracking-wider">
              System Architecture & Research Contribution
            </span>
            <h3 className="text-2xl font-bold text-white">
              End-to-End Grounded Integration Pipeline
            </h3>
            <p className="text-sm text-slate-300 leading-relaxed">
              NEBULA proves that a single unified computational core can dynamically feed three drastically distinct cognitive levels without hallucination or loss of mathematical rigor.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 pt-4">
            <div className="p-4 rounded-xl bg-space-900 border border-white/10 space-y-2">
              <div className="flex items-center space-x-2 text-sky-400 font-mono text-xs font-bold">
                <Database className="w-4 h-4" />
                <span>1. Data Layer</span>
              </div>
              <p className="text-xs text-slate-400">
                NASA Horizons, JPL Dynamics, Gaia DR3, and local SQLite cache with verified physical constants.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-space-900 border border-white/10 space-y-2">
              <div className="flex items-center space-x-2 text-purple-400 font-mono text-xs font-bold">
                <Atom className="w-4 h-4" />
                <span>2. Physics Engine</span>
              </div>
              <p className="text-xs text-slate-400">
                REBOUND IAS15 + NumPy Symplectic Leapfrog, Kepler solvers, Hohmann transfers, and Hill spheres.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-space-900 border border-white/10 space-y-2">
              <div className="flex items-center space-x-2 text-emerald-400 font-mono text-xs font-bold">
                <ShieldCheck className="w-4 h-4" />
                <span>3. Grounded AI</span>
              </div>
              <p className="text-xs text-slate-400">
                Contextual prompt grounding injecting exact numerical figures, preventing hallucinations offline.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-space-900 border border-white/10 space-y-2">
              <div className="flex items-center space-x-2 text-amber-400 font-mono text-xs font-bold">
                <BarChart3 className="w-4 h-4" />
                <span>4. Evaluation Lab</span>
              </div>
              <p className="text-xs text-slate-400">
                Flesch-Kincaid grade level metrics, technical vocabulary density, and symplectic error verification.
              </p>
            </div>
          </div>

          <div className="pt-2 text-center">
            <Link
              to="/research"
              className="inline-flex items-center space-x-2 text-xs font-mono text-sky-400 hover:text-sky-300 underline underline-offset-4"
            >
              <span>View live evaluation benchmarks and comparative metrics</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};
