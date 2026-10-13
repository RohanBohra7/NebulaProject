import React, { useState, useEffect } from 'react';
import { useLocation, Link } from 'react-router-dom';
import { TopNav } from './TopNav';
import { Sidebar } from './Sidebar';
import { Footer } from '../components/layout/Footer';
import { useMode } from '../context/ModeContext';
import { ChevronRight, Sparkles, GraduationCap, Cpu } from 'lucide-react';

interface AppShellProps {
  children: React.ReactNode;
}

export const AppShell: React.FC<AppShellProps> = ({ children }) => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(() => {
    const saved = localStorage.getItem('nebula_sidebar_open');
    return saved !== null ? saved === 'true' : true;
  });

  const { mode } = useMode();
  const location = useLocation();

  useEffect(() => {
    localStorage.setItem('nebula_sidebar_open', String(isSidebarOpen));
  }, [isSidebarOpen]);

  // Route title mapper for breadcrumbs
  const getBreadcrumbTitle = (pathname: string) => {
    if (pathname === '/') return 'Overview';
    if (pathname === '/mode') return 'Mode Selection Hub';
    if (pathname === '/citizen') return 'Citizen Dashboard';
    if (pathname === '/student') return 'Student Dashboard';
    if (pathname === '/researcher') return 'Researcher Dashboard';
    if (pathname === '/explorer') return 'Celestial Explorer';
    if (pathname.startsWith('/object/')) return 'Object Telemetry';
    if (pathname === '/compare') return 'Comparative Analysis';
    if (pathname === '/visualization') return '3D Keplerian Visualizer';
    if (pathname === '/simulation') return 'N-Body Laboratory';
    if (pathname === '/ai') return 'Grounded AI Assistant';
    if (pathname === '/data') return 'Data Management & Provenance';
    if (pathname === '/research') return 'Research Evaluation & Metrics';
    if (pathname === '/settings') return 'Platform Settings';
    return pathname.replace('/', '');
  };

  const isLandingOrMode = location.pathname === '/' || location.pathname === '/mode';

  return (
    <div className="min-h-screen flex flex-col bg-space-950 text-slate-100 selection:bg-sky-500/30 selection:text-sky-200">
      {/* Top Navigation */}
      <TopNav
        onToggleSidebar={() => setIsSidebarOpen((prev) => !prev)}
        isSidebarOpen={isSidebarOpen}
      />

      {/* Main Layout Area */}
      <div className="flex-1 flex w-full relative">
        {/* Sidebar */}
        <Sidebar
          isOpen={isSidebarOpen}
          onToggle={() => setIsSidebarOpen((prev) => !prev)}
        />

        {/* Content Body */}
        <div className="flex-1 flex flex-col min-w-0 overflow-x-hidden">
          {/* Persona & Breadcrumb Sub-bar (for internal pages) */}
          {!isLandingOrMode && (
            <div className="bg-space-900/40 border-b border-white/5 px-4 sm:px-8 py-2 flex items-center justify-between text-xs font-mono text-slate-400">
              <div className="flex items-center space-x-2">
                <Link to="/" className="hover:text-slate-200 transition-colors">
                  NEBULA
                </Link>
                <ChevronRight className="w-3.5 h-3.5 text-slate-600" />
                <span className="text-white font-medium">{getBreadcrumbTitle(location.pathname)}</span>
              </div>

              <div className="hidden sm:flex items-center space-x-2 text-[11px]">
                <span>Active Persona:</span>
                <span
                  className={`px-2 py-0.5 rounded capitalize font-semibold border ${
                    mode === 'researcher'
                      ? 'bg-sky-500/10 border-sky-500/30 text-sky-400'
                      : mode === 'student'
                      ? 'bg-amber-500/10 border-amber-500/30 text-amber-400'
                      : 'bg-purple-500/10 border-purple-500/30 text-purple-400'
                  }`}
                >
                  {mode}
                </span>
              </div>
            </div>
          )}

          {/* Children View */}
          <main className="flex-1">
            {children}
          </main>

          {/* Footer */}
          <Footer />
        </div>
      </div>
    </div>
  );
};
