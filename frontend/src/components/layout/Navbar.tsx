import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useMode } from '../../context/ModeContext';
import { UserMode } from '../../types/astronomy';
import {
  Compass,
  Orbit,
  Sparkles,
  GitCompare,
  Cpu,
  Database,
  BarChart3,
  Settings,
  Layers,
  GraduationCap,
  Globe2,
  Atom,
  BookOpen
} from 'lucide-react';

export const Navbar: React.FC = () => {
  const { mode, setMode } = useMode();
  const location = useLocation();

  // Mode-adaptive navigation items
  const getNavLinks = () => {
    switch (mode) {
      case 'researcher':
        return [
          { to: '/', label: 'Overview', icon: Globe2 },
          { to: '/explorer', label: 'Data Catalog', icon: Compass },
          { to: '/visualization', label: 'Ephemeris 3D', icon: Orbit },
          { to: '/simulation', label: 'N-Body Solver', icon: Atom },
          { to: '/compare', label: 'Parametric Matrix', icon: GitCompare },
          { to: '/ai', label: 'Astrophysics AI', icon: Sparkles },
          { to: '/data', label: 'Provenance', icon: Database },
          { to: '/research', label: 'Evaluation', icon: BarChart3 }
        ];
      case 'student':
        return [
          { to: '/', label: 'Overview', icon: Globe2 },
          { to: '/student', label: 'Learn Concepts', icon: BookOpen },
          { to: '/explorer', label: 'Explore Objects', icon: Compass },
          { to: '/visualization', label: 'Interactive 3D', icon: Orbit },
          { to: '/simulation', label: 'Guided Simulations', icon: Atom },
          { to: '/compare', label: 'Compare Objects', icon: GitCompare },
          { to: '/ai', label: 'AI Tutor', icon: Sparkles }
        ];
      case 'citizen':
      default:
        return [
          { to: '/', label: 'Overview', icon: Globe2 },
          { to: '/explorer', label: 'Discover Worlds', icon: Compass },
          { to: '/visualization', label: '3D Planetarium', icon: Orbit },
          { to: '/simulation', label: 'Gravity Playground', icon: Atom },
          { to: '/compare', label: 'Side-by-Side', icon: GitCompare },
          { to: '/ai', label: 'Cosmic Assistant', icon: Sparkles }
        ];
    }
  };

  const getDashboardInfo = () => {
    switch (mode) {
      case 'researcher':
        return { path: '/researcher', label: 'Research Station', icon: Cpu, badgeColor: 'text-sky-400 border-sky-400/30 bg-sky-500/10' };
      case 'student':
        return { path: '/student', label: 'Student Classroom', icon: GraduationCap, badgeColor: 'text-amber-400 border-amber-400/30 bg-amber-500/10' };
      case 'citizen':
        return { path: '/citizen', label: 'Cosmic Backyard', icon: Sparkles, badgeColor: 'text-purple-400 border-purple-400/30 bg-purple-500/10' };
    }
  };

  const dashboardInfo = getDashboardInfo();
  const navLinks = getNavLinks();

  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-white/10 px-4 lg:px-8 py-3" role="banner">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        {/* Brand Logo */}
        <Link
          to="/"
          className="flex items-center space-x-3 group focus:outline-none focus:ring-2 focus:ring-sky-400 rounded-xl"
          aria-label="NEBULA Home"
        >
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-500 via-indigo-600 to-purple-600 flex items-center justify-center shadow-lg shadow-sky-500/20 group-hover:shadow-sky-500/40 transition-all duration-300">
            <Orbit className="w-6 h-6 text-white animate-spin-slow" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-xl font-bold tracking-wider font-mono bg-gradient-to-r from-sky-400 via-purple-300 to-rose-400 bg-clip-text text-transparent">
                NEBULA
              </span>
              <span className="text-xs px-2 py-0.5 rounded-full bg-white/10 text-slate-300 border border-white/10 uppercase tracking-widest font-mono">
                {mode}
              </span>
            </div>
            <span className="text-[10px] text-slate-400 hidden sm:block">
              Astronomical Visualization & Research Platform
            </span>
          </div>
        </Link>

        {/* Central Nav Links (Mode-Adaptive) */}
        <nav
          className="hidden md:flex items-center space-x-1 lg:space-x-2"
          role="navigation"
          aria-label="Main Navigation"
        >
          {/* Active Mode Dashboard Link */}
          <Link
            to={dashboardInfo.path}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center space-x-1.5 transition-all ${
              location.pathname === dashboardInfo.path
                ? 'bg-gradient-to-r from-sky-500/20 via-indigo-500/20 to-purple-500/20 text-white border border-white/20 shadow-md'
                : 'text-slate-300 hover:text-white hover:bg-white/5'
            }`}
            aria-current={location.pathname === dashboardInfo.path ? 'page' : undefined}
          >
            <dashboardInfo.icon className="w-3.5 h-3.5" />
            <span>{dashboardInfo.label}</span>
          </Link>

          {navLinks.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.to;
            return (
              <Link
                key={item.to}
                to={item.to}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center space-x-1.5 transition-all ${
                  isActive
                    ? 'bg-sky-500/10 text-sky-400 border border-sky-500/30'
                    : 'text-slate-300 hover:text-white hover:bg-white/5'
                }`}
                aria-current={isActive ? 'page' : undefined}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>

        {/* Persona Mode Switcher and Settings */}
        <div className="flex items-center space-x-3">
          {/* Persona Mode Switcher */}
          <div
            className="flex items-center bg-space-900 border border-white/10 rounded-xl p-1 text-xs shadow-inner"
            role="group"
            aria-label="Select User Persona"
          >
            <button
              onClick={() => setMode('citizen')}
              className={`px-2.5 py-1 rounded-lg transition-all flex items-center space-x-1 ${
                mode === 'citizen'
                  ? 'bg-purple-600 text-white shadow-md shadow-purple-600/30 font-semibold'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
              title="Citizen Mode: Plain language, wonder-focused 3D visual exploration"
              aria-label="Switch to Citizen Mode"
              aria-pressed={mode === 'citizen'}
            >
              <Sparkles className="w-3 h-3" />
              <span className="hidden sm:inline">Citizen</span>
            </button>
            <button
              onClick={() => setMode('student')}
              className={`px-2.5 py-1 rounded-lg transition-all flex items-center space-x-1 ${
                mode === 'student'
                  ? 'bg-amber-600 text-white shadow-md shadow-amber-600/30 font-semibold'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
              title="Student Mode: Educational scaffolding, guided simulations, AI tutor"
              aria-label="Switch to Student Mode"
              aria-pressed={mode === 'student'}
            >
              <GraduationCap className="w-3 h-3" />
              <span className="hidden sm:inline">Student</span>
            </button>
            <button
              onClick={() => setMode('researcher')}
              className={`px-2.5 py-1 rounded-lg transition-all flex items-center space-x-1 ${
                mode === 'researcher'
                  ? 'bg-sky-600 text-white shadow-md shadow-sky-600/30 font-semibold'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
              title="Researcher Mode: Astrophysical metadata, N-body conservation, orbital analysis"
              aria-label="Switch to Researcher Mode"
              aria-pressed={mode === 'researcher'}
            >
              <Cpu className="w-3 h-3" />
              <span className="hidden sm:inline">Researcher</span>
            </button>
          </div>

          {/* Mode Hub link */}
          <Link
            to="/mode"
            className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-white/5 transition-all"
            title="Persona Guide & Matrix"
            aria-label="View Persona Guide"
          >
            <Layers className="w-4 h-4" />
          </Link>

          {/* Settings */}
          <Link
            to="/settings"
            className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-white/5 transition-all"
            title="Settings & Application Config"
            aria-label="Settings"
          >
            <Settings className="w-4 h-4" />
          </Link>
        </div>
      </div>
    </header>
  );
};
