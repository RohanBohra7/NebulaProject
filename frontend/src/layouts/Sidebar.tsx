import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useMode } from '../context/ModeContext';
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
  Atom,
  Home,
  Info,
  ChevronLeft,
  ChevronRight,
  ExternalLink
} from 'lucide-react';
import { cn } from '../utils/cn';

interface NavItem {
  to: string;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  badge?: string;
}

interface SidebarProps {
  isOpen: boolean;
  onToggle: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ isOpen, onToggle }) => {
  const { mode } = useMode();
  const location = useLocation();

  // Mode-aware primary dashboard link
  const getDashboardLink = (): NavItem => {
    switch (mode) {
      case 'researcher':
        return { to: '/researcher', label: 'Researcher Workspace', icon: Cpu, badge: 'Astrophysics' };
      case 'student':
        return { to: '/student', label: 'Student Hub', icon: GraduationCap, badge: 'Learning' };
      case 'citizen':
        return { to: '/citizen', label: 'Citizen Space', icon: Sparkles, badge: 'Discovery' };
    }
  };

  const dashboardItem = getDashboardLink();

  // Navigation items
  const navSections: { title: string; items: NavItem[] }[] = [
    {
      title: 'CORE PLATFORM',
      items: [
        { to: '/', label: 'Platform Overview', icon: Home },
        dashboardItem,
        { to: '/explorer', label: 'Celestial Explorer', icon: Compass, badge: '23 Objects' },
      ],
    },
    {
      title: 'PHYSICS & SIMULATION',
      items: [
        { to: '/visualization', label: '3D Orbit Viewer', icon: Orbit, badge: 'Keplerian' },
        { to: '/simulation', label: 'N-Body Laboratory', icon: Atom, badge: 'REBOUND' },
        { to: '/compare', label: 'Object Comparison', icon: GitCompare },
      ],
    },
    {
      title: 'INTELLIGENCE & DATA',
      items: [
        { to: '/ai', label: 'Grounded AI Assistant', icon: Sparkles },
        { to: '/research', label: 'Research Evaluation', icon: BarChart3, badge: 'FKGL & Ease' },
        { to: '/data', label: 'Data Management', icon: Database, badge: 'Provenance' },
      ],
    },
  ];

  const modeBadge = {
    researcher: {
      title: 'Researcher Persona',
      description: 'High scientific density & N-body telemetry',
      color: 'bg-sky-500/10 border-sky-500/30 text-sky-400',
    },
    student: {
      title: 'Student Persona',
      description: 'Guided physics scaffolding & AI tutor',
      color: 'bg-amber-500/10 border-amber-500/30 text-amber-400',
    },
    citizen: {
      title: 'Citizen Persona',
      description: 'Visual 3D discovery & plain language',
      color: 'bg-purple-500/10 border-purple-500/30 text-purple-400',
    },
  }[mode];

  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-space-950/70 backdrop-blur-sm z-30 lg:hidden"
          onClick={onToggle}
        />
      )}

      {/* Sidebar container */}
      <aside
        className={cn(
          'fixed lg:sticky top-0 lg:top-[57px] left-0 z-30 h-screen lg:h-[calc(100vh-57px)] bg-space-950/95 backdrop-blur-2xl border-r border-white/10 flex flex-col transition-all duration-300 select-none overflow-hidden',
          isOpen ? 'w-64 translate-x-0' : 'w-0 lg:w-16 -translate-x-full lg:translate-x-0'
        )}
      >
        {/* Active Persona Banner */}
        {isOpen && (
          <div className="p-4 border-b border-white/10 bg-white/[0.02]">
            <div className={cn('p-3 rounded-xl border flex flex-col space-y-1', modeBadge.color)}>
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-bold tracking-wider font-mono uppercase">
                  {modeBadge.title}
                </span>
                <Link
                  to="/mode"
                  className="text-[10px] text-slate-400 hover:text-white underline font-mono"
                  title="Switch Persona Mode"
                >
                  Change
                </Link>
              </div>
              <p className="text-[10px] text-slate-400 leading-snug font-sans">
                {modeBadge.description}
              </p>
            </div>
          </div>
        )}

        {/* Navigation Sections */}
        <div className="flex-1 overflow-y-auto px-3 py-4 space-y-6 custom-scrollbar">
          {navSections.map((section, idx) => (
            <div key={idx} className="space-y-1.5">
              {isOpen && (
                <div className="px-3 text-[10px] font-mono uppercase tracking-wider text-slate-400 font-semibold">
                  {section.title}
                </div>
              )}
              <div className="space-y-0.5">
                {section.items.map((item) => {
                  const Icon = item.icon;
                  const isActive = location.pathname === item.to;
                  return (
                    <Link
                      key={item.to}
                      to={item.to}
                      title={!isOpen ? item.label : undefined}
                      className={cn(
                        'flex items-center rounded-xl text-xs font-medium transition-all group',
                        isOpen ? 'px-3 py-2 space-x-3' : 'p-3 justify-center',
                        isActive
                          ? 'bg-sky-500/15 text-white border border-sky-500/30 shadow-md shadow-sky-500/10'
                          : 'text-slate-400 hover:text-white hover:bg-white/5'
                      )}
                    >
                      <Icon
                        className={cn(
                          'w-4 h-4 shrink-0 transition-transform group-hover:scale-110',
                          isActive ? 'text-sky-400' : 'text-slate-400 group-hover:text-slate-200'
                        )}
                      />
                      {isOpen && (
                        <div className="flex items-center justify-between flex-1 min-w-0">
                          <span className="truncate">{item.label}</span>
                          {item.badge && (
                            <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-white/5 text-slate-400 border border-white/5 shrink-0">
                              {item.badge}
                            </span>
                          )}
                        </div>
                      )}
                    </Link>
                  );
                })}
              </div>
            </div>
          ))}
        </div>

        {/* Sidebar Footer telemetry */}
        {isOpen && (
          <div className="p-3 border-t border-white/10 bg-white/[0.02] space-y-2 text-[11px] font-mono text-slate-400">
            <div className="flex items-center justify-between px-1">
              <span>Catalog State:</span>
              <span className="text-emerald-400 font-semibold">23 Local Objects</span>
            </div>
            <div className="flex items-center justify-between px-1">
              <span>Integrator:</span>
              <span className="text-sky-400 font-semibold">IAS15 (Rebound)</span>
            </div>
          </div>
        )}

        {/* Collapse toggle button */}
        <div className="hidden lg:flex p-2 border-t border-white/10 justify-end">
          <button
            onClick={onToggle}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/5 transition-colors w-full flex items-center justify-center"
            title={isOpen ? 'Collapse Sidebar' : 'Expand Sidebar'}
          >
            {isOpen ? <ChevronLeft className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
          </button>
        </div>
      </aside>
    </>
  );
};
