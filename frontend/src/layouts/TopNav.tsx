import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useMode } from '../context/ModeContext';
import {
  Orbit,
  Sparkles,
  GraduationCap,
  Cpu,
  Layers,
  Settings,
  Menu,
  X,
  Search,
  Activity,
  ChevronRight
} from 'lucide-react';
import { Modal } from '../components/ui/Modal';
import { Button } from '../components/ui/Button';

interface TopNavProps {
  onToggleSidebar?: () => void;
  isSidebarOpen?: boolean;
}

export const TopNav: React.FC<TopNavProps> = ({ onToggleSidebar, isSidebarOpen }) => {
  const { mode, setMode } = useMode();
  const location = useLocation();
  const [isBackendHealthy, setIsBackendHealthy] = useState<boolean | null>(null);
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  // Check backend health periodically
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch('/api/health');
        if (res.ok) {
          setIsBackendHealthy(true);
        } else {
          setIsBackendHealthy(false);
        }
      } catch (e) {
        setIsBackendHealthy(false);
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  // Quick navigation shortcuts for the search modal
  const searchShortcuts = [
    { title: 'Astronomical Object Explorer', path: '/explorer', category: 'Catalog' },
    { title: 'Interactive 3D Keplerian Orbits', path: '/visualization', category: 'Visualization' },
    { title: 'N-Body Gravitational Laboratory', path: '/simulation', category: 'Physics Lab' },
    { title: 'Multi-Object Comparative Analysis', path: '/compare', category: 'Analysis' },
    { title: 'Grounded AI Astronomical Assistant', path: '/ai', category: 'Intelligence' },
    { title: 'Multi-Persona Research Evaluation', path: '/research', category: 'Evaluation' },
    { title: 'Scientific Data & Provenance', path: '/data', category: 'Datasets' },
    { title: 'Researcher Workspace', path: '/researcher', category: 'Dashboards' },
    { title: 'Student Learning Hub', path: '/student', category: 'Dashboards' },
    { title: 'Citizen Visual Experience', path: '/citizen', category: 'Dashboards' },
  ];

  const filteredShortcuts = searchShortcuts.filter((item) =>
    item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    item.category.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <>
      <header className="sticky top-0 z-40 bg-space-950/80 backdrop-blur-xl border-b border-white/10 px-4 sm:px-6 py-2.5 transition-all">
        <div className="flex items-center justify-between">
          {/* Left: Sidebar Toggle & Brand */}
          <div className="flex items-center space-x-3">
            <button
              onClick={onToggleSidebar}
              className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-white/5 transition-colors focus:outline-none"
              aria-label="Toggle navigation sidebar"
            >
              {isSidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>

            <Link to="/" className="flex items-center space-x-2.5 group">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-sky-500 via-indigo-600 to-purple-600 flex items-center justify-center shadow-md shadow-sky-500/20 group-hover:shadow-sky-500/40 transition-all">
                <Orbit className="w-4 h-4 text-white animate-spin-slow" />
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-base font-bold tracking-wider font-mono bg-gradient-to-r from-sky-400 via-purple-300 to-rose-400 bg-clip-text text-transparent">
                  NEBULA
                </span>
                <span className="hidden sm:inline-block text-[10px] font-mono uppercase px-1.5 py-0.5 rounded bg-white/10 text-slate-300 border border-white/10">
                  v1.0
                </span>
              </div>
            </Link>
          </div>

          {/* Center: Command Palette / Search Trigger */}
          <div className="hidden md:flex items-center">
            <button
              onClick={() => setIsSearchOpen(true)}
              className="flex items-center space-x-3 px-3 py-1.5 rounded-lg bg-white/[0.04] hover:bg-white/[0.08] border border-white/10 text-slate-400 hover:text-slate-200 text-xs transition-all w-64 lg:w-80 justify-between group shadow-inner"
            >
              <div className="flex items-center space-x-2">
                <Search className="w-3.5 h-3.5 text-slate-400 group-hover:text-sky-400 transition-colors" />
                <span>Search objects, simulations...</span>
              </div>
              <kbd className="px-1.5 py-0.5 text-[10px] font-mono bg-space-900 border border-white/10 rounded text-slate-400">
                ⌘K
              </kbd>
            </button>
          </div>

          {/* Right: Mode Switcher & Status */}
          <div className="flex items-center space-x-2 sm:space-x-3">
            {/* Backend Health Indicator */}
            <div
              className={`hidden sm:flex items-center space-x-1.5 px-2.5 py-1 rounded-full text-[11px] font-mono border ${
                isBackendHealthy === true
                  ? 'bg-emerald-950/40 border-emerald-500/30 text-emerald-400'
                  : isBackendHealthy === false
                  ? 'bg-rose-950/40 border-rose-500/30 text-rose-400'
                  : 'bg-slate-900/60 border-white/10 text-slate-400'
              }`}
              title={isBackendHealthy ? 'Backend API: Online (/api/v1)' : 'Backend API: Offline'}
            >
              <span
                className={`w-1.5 h-1.5 rounded-full ${
                  isBackendHealthy === true ? 'bg-emerald-400 animate-pulse' : 'bg-rose-400'
                }`}
              />
              <span className="hidden lg:inline">{isBackendHealthy ? 'REBOUND/FastAPI' : 'Offline'}</span>
            </div>

            {/* Persistent Persona Mode Switcher */}
            <div className="flex items-center bg-space-900/90 border border-white/10 rounded-lg p-0.5 text-xs shadow-inner">
              <button
                onClick={() => setMode('citizen')}
                className={`px-2 py-1 rounded-md transition-all flex items-center space-x-1 ${
                  mode === 'citizen'
                    ? 'bg-purple-600 text-white shadow font-medium'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
                title="Citizen Mode"
              >
                <Sparkles className="w-3 h-3" />
                <span className="hidden sm:inline">Citizen</span>
              </button>
              <button
                onClick={() => setMode('student')}
                className={`px-2 py-1 rounded-md transition-all flex items-center space-x-1 ${
                  mode === 'student'
                    ? 'bg-amber-600 text-white shadow font-medium'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
                title="Student Mode"
              >
                <GraduationCap className="w-3 h-3" />
                <span className="hidden sm:inline">Student</span>
              </button>
              <button
                onClick={() => setMode('researcher')}
                className={`px-2 py-1 rounded-md transition-all flex items-center space-x-1 ${
                  mode === 'researcher'
                    ? 'bg-sky-600 text-white shadow font-medium'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
                title="Researcher Mode"
              >
                <Cpu className="w-3 h-3" />
                <span className="hidden sm:inline">Researcher</span>
              </button>
            </div>

            {/* Mode selection page link */}
            <Link
              to="/mode"
              className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/5 transition-colors"
              title="Compare Personas"
            >
              <Layers className="w-4 h-4" />
            </Link>

            {/* Settings Link */}
            <Link
              to="/settings"
              className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/5 transition-colors"
              title="Settings"
            >
              <Settings className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </header>

      {/* Quick Search & Command Modal */}
      <Modal
        isOpen={isSearchOpen}
        onClose={() => {
          setIsSearchOpen(false);
          setSearchQuery('');
        }}
        title="NEBULA Quick Navigator"
        description="Search platform modules, scientific simulations, or astronomical tools"
        size="lg"
      >
        <div className="space-y-4">
          <div className="relative">
            <Search className="absolute left-3.5 top-3 w-4 h-4 text-slate-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search or jump to module..."
              className="w-full bg-space-950 border border-white/10 rounded-xl pl-10 pr-4 py-2.5 text-sm text-white focus:outline-none focus:border-sky-500 font-mono"
              autoFocus
            />
          </div>

          <div className="space-y-1 max-h-72 overflow-y-auto">
            {filteredShortcuts.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                onClick={() => {
                  setIsSearchOpen(false);
                  setSearchQuery('');
                }}
                className="flex items-center justify-between p-3 rounded-lg hover:bg-white/[0.06] transition-colors group"
              >
                <div className="flex items-center space-x-3">
                  <span className="text-xs px-2 py-0.5 rounded bg-white/5 text-slate-400 font-mono border border-white/5">
                    {item.category}
                  </span>
                  <span className="text-sm text-slate-200 group-hover:text-white font-medium">
                    {item.title}
                  </span>
                </div>
                <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-sky-400 transition-colors" />
              </Link>
            ))}
            {filteredShortcuts.length === 0 && (
              <div className="text-center py-6 text-xs text-slate-500 font-mono">
                No matching tools or pages found.
              </div>
            )}
          </div>
        </div>
      </Modal>
    </>
  );
};
