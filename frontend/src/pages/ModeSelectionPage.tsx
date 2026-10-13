import React from 'react';
import { useMode } from '../context/ModeContext';
import { UserMode } from '../types/astronomy';
import { useNavigate } from 'react-router-dom';
import { Sparkles, GraduationCap, Cpu, Check, ArrowRight } from 'lucide-react';

export const ModeSelectionPage: React.FC = () => {
  const { mode, setMode } = useMode();
  const navigate = useNavigate();

  const selectAndNavigate = (newMode: UserMode) => {
    setMode(newMode);
    switch (newMode) {
      case 'researcher': navigate('/researcher'); break;
      case 'student': navigate('/student'); break;
      case 'citizen': navigate('/citizen'); break;
    }
  };

  const modesConfig = [
    {
      id: 'citizen' as UserMode,
      name: 'Citizen Mode',
      tagline: 'Cosmic Wonder & Visual Storytelling',
      icon: Sparkles,
      color: 'purple',
      iconClass: 'bg-purple-500/10 border-purple-500/30 text-purple-400',
      badge: 'General Public (Grade 5-7)',
      description: 'Ideal for stargazers, astronomy fans, and anyone captivated by the sheer beauty and scale of space.',
      features: [
        'Plain-language cosmic explanations',
        'Relatable real-world analogies (e.g. flight times, Earth weight)',
        'Cinematic 3D orbit visuals & night sky highlights',
        'Conversational AI planetarium guide'
      ],
      readability: 'Grade Level: 5.0 - 7.0 • Jargon: < 3%',
      activeBorder: 'border-purple-500 shadow-purple-500/20'
    },
    {
      id: 'student' as UserMode,
      name: 'Student Mode',
      tagline: 'Guided Scaffolding & Concept Mastery',
      icon: GraduationCap,
      color: 'amber',
      iconClass: 'bg-amber-500/10 border-amber-500/30 text-amber-400',
      badge: 'High School & Undergrad (Grade 8-11)',
      description: 'Designed for STEM learners and educators seeking clear bridges between observations and physical laws.',
      features: [
        'Interactive Kepler & Newton concept sandboxes',
        'Guided tours across inner planets & TRAPPIST-1 system',
        'Interactive quizzes with comprehension checks',
        'Socratic AI tutor explaining the "why" behind phenomena'
      ],
      readability: 'Grade Level: 8.5 - 11.0 • Jargon: ~5 - 8%',
      activeBorder: 'border-amber-500 shadow-amber-500/20'
    },
    {
      id: 'researcher' as UserMode,
      name: 'Researcher Mode',
      tagline: 'Mathematical Precision & Scientific Telemetry',
      icon: Cpu,
      color: 'sky',
      iconClass: 'bg-sky-500/10 border-sky-500/30 text-sky-400',
      badge: 'Astrophysicists & Scholars (Grade 12-18)',
      description: 'Built for computational astrophysicists and researchers requiring empirical parameters and orbital analysis.',
      features: [
        'Full Keplerian orbital elements (a, e, i, Ω, ω, ν)',
        'Hohmann transfer Δv calculator & transfer time curves',
        'REBOUND IAS15 N-body integration with Hamiltonian error dE/E',
        'Peer-reviewed formulas, LaTeX expressions, and data provenance'
      ],
      readability: 'Grade Level: 12.0 - 18.0 • Jargon: ~12 - 22%',
      activeBorder: 'border-sky-500 shadow-sky-500/20'
    }
  ];

  return (
    <div className="max-w-6xl mx-auto px-4 py-10 space-y-12">
      <div className="text-center space-y-3">
        <h1 className="text-3xl sm:text-4xl font-extrabold text-white">
          Choose Your Perspective
        </h1>
        <p className="text-slate-400 max-w-2xl mx-auto text-sm">
          NEBULA's adaptive architecture transforms presentation, terminology, and AI responses while maintaining the exact same underlying empirical data.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {modesConfig.map((item) => {
          const Icon = item.icon;
          const isCurrent = mode === item.id;

          return (
            <div
              key={item.id}
              className={`p-6 rounded-3xl glass-panel border transition-all flex flex-col justify-between space-y-6 ${
                isCurrent ? `${item.activeBorder} shadow-xl scale-[1.02]` : 'border-white/10 hover:border-white/20'
              }`}
            >
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className={`w-12 h-12 rounded-2xl flex items-center justify-center border ${item.iconClass}`}>
                    <Icon className="w-6 h-6" />
                  </div>
                  {isCurrent && (
                    <span className="px-2.5 py-1 rounded-full bg-emerald-500/20 border border-emerald-500/30 text-emerald-300 text-[11px] font-semibold flex items-center space-x-1">
                      <Check className="w-3 h-3" />
                      <span>Active</span>
                    </span>
                  )}
                </div>

                <div>
                  <h3 className="text-xl font-bold text-white">{item.name}</h3>
                  <p className="text-xs text-slate-400 mt-0.5">{item.tagline}</p>
                </div>

                <div className="text-[11px] font-mono px-2.5 py-1 rounded-lg bg-white/5 border border-white/5 text-slate-300">
                  {item.badge}
                </div>

                <p className="text-xs text-slate-300 leading-relaxed">
                  {item.description}
                </p>

                <div className="space-y-2 pt-2 border-t border-white/5">
                  <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Features:</span>
                  <ul className="text-xs text-slate-300 space-y-1.5">
                    {item.features.map((feat, i) => (
                      <li key={i} className="flex items-start space-x-2">
                        <Check className="w-3.5 h-3.5 text-slate-400 mt-0.5 flex-shrink-0" />
                        <span>{feat}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              <div className="space-y-3 pt-4 border-t border-white/5">
                <div className="text-[10px] text-slate-400 font-mono">
                  {item.readability}
                </div>

                <button
                  onClick={() => selectAndNavigate(item.id)}
                  className={`w-full py-2.5 rounded-xl text-xs font-bold flex items-center justify-center space-x-2 transition-all ${
                    isCurrent
                      ? 'bg-white text-space-950 hover:bg-slate-200 shadow-md'
                      : 'bg-white/10 hover:bg-white/20 text-white border border-white/10'
                  }`}
                >
                  <span>{isCurrent ? 'Continue to Dashboard' : `Switch to ${item.name}`}</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
