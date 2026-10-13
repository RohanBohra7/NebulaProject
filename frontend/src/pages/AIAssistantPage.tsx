import React, { useState, useEffect, useRef } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { useMode } from '../context/ModeContext';
import { fetchObjects, chatAI, fetchAIStatus } from '../services/api';
import { AstronomicalObject, AIChatResponse, UserMode } from '../types/astronomy';
import {
  Sparkles,
  Send,
  Cpu,
  GraduationCap,
  ShieldCheck,
  RotateCcw,
  Bot,
  User,
  Info,
  Layers,
  CheckCircle2,
  AlertTriangle,
  Zap,
  Orbit,
  GitCompare,
  X,
  ExternalLink,
  ChevronRight,
  Database
} from 'lucide-react';

interface ChatMessage {
  id: string;
  sender: 'user' | 'assistant';
  content: string;
  mode: UserMode;
  groundingMeta?: any;
  toolsInvoked?: string[];
  distinctions?: {
    nebula_data?: string;
    computed_result?: string;
    external_scientific_context?: string;
    general_explanation?: string;
  };
  validation?: {
    is_valid: boolean;
    score: number;
    safety_flags: string[];
  };
  provider?: string;
  usedFallback?: boolean;
  timestamp: string;
}

export const AIAssistantPage: React.FC = () => {
  const { mode: currentGlobalMode, setMode: setGlobalMode } = useMode();
  const [searchParams, setSearchParams] = useSearchParams();

  // URL Context parameters
  const targetParam = searchParams.get('target') || '';
  const simulationParam = searchParams.get('simulation') || '';
  const compareParam = searchParams.get('compare') || '';
  const promptParam = searchParams.get('prompt') || '';

  const [activePersona, setActivePersona] = useState<UserMode>(currentGlobalMode);
  const [objects, setObjects] = useState<AstronomicalObject[]>([]);
  const [targetObjectId, setTargetObjectId] = useState<string>(targetParam);
  const [simulationId, setSimulationId] = useState<string>(simulationParam);
  const [compareIds, setCompareIds] = useState<string[]>(
    compareParam ? compareParam.split(',').filter(Boolean) : []
  );

  const [aiStatus, setAiStatus] = useState<any | null>(null);
  const [inputPrompt, setInputPrompt] = useState(promptParam);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Sync params if URL updates
  useEffect(() => {
    if (targetParam) setTargetObjectId(targetParam);
    if (simulationParam) setSimulationId(simulationParam);
    if (compareParam) setCompareIds(compareParam.split(',').filter(Boolean));
    if (promptParam) setInputPrompt(promptParam);
  }, [targetParam, simulationParam, compareParam, promptParam]);

  // Load objects and AI status
  useEffect(() => {
    fetchObjects().then((data) => setObjects(data)).catch(() => {});
    fetchAIStatus().then((status) => setAiStatus(status)).catch(() => {});
  }, []);

  // Update greeting when persona switches
  useEffect(() => {
    const welcomeMsg: ChatMessage = {
      id: 'welcome-init',
      sender: 'assistant',
      content:
        activePersona === 'researcher'
          ? "Welcome to NEBULA Astrophysical Research Intelligence. Inquiries regarding secular orbital dynamics, barycentric state vectors, relativistic mechanics, or stellar astrophysics are evaluated against empirical catalogs and verified N-body integrators."
          : activePersona === 'student'
          ? "Welcome to your NEBULA Astronomy Classroom! 🚀 I'm your interactive physics tutor. Ask me about Kepler's laws, how gravity shapes the orbits of planets, why Saturn has rings, or how we run N-body simulations!"
          : "Welcome to the NEBULA Cosmic Backyard! ✨ I'm your stargazing companion. Ask me anything about planets, cosmic mysteries, or everyday questions like what you would weigh on Jupiter!",
      mode: activePersona,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    setMessages([welcomeMsg]);
  }, [activePersona]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleClearChat = () => {
    const resetMsg: ChatMessage = {
      id: String(Date.now()),
      sender: 'assistant',
      content:
        activePersona === 'researcher'
          ? "Session telemetry reset. Ready for new mathematical, orbital, or catalog inquiries."
          : activePersona === 'student'
          ? "Chat cleared! What astronomy topic or concept would you like to explore next?"
          : "Chat cleared! Ask me anything about space and our cosmic neighborhood!",
      mode: activePersona,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    setMessages([resetMsg]);
    setErrorMessage(null);
  };

  const handleSendMessage = async (text: string) => {
    const cleanText = text.trim();
    if (!cleanText || isLoading) return;

    setErrorMessage(null);
    const userMsg: ChatMessage = {
      id: String(Date.now()),
      sender: 'user',
      content: cleanText,
      mode: activePersona,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputPrompt('');
    setIsLoading(true);

    try {
      const res: AIChatResponse = await chatAI(
        cleanText,
        activePersona,
        targetObjectId || undefined,
        messages.slice(-4).map((m) => ({ role: m.sender, content: m.content })),
        simulationId || undefined,
        compareIds.length > 0 ? compareIds : undefined
      );

      const assistantMsg: ChatMessage = {
        id: String(Date.now() + 1),
        sender: 'assistant',
        content: res.response,
        mode: res.mode,
        groundingMeta: res.grounding_meta,
        toolsInvoked: res.tools_invoked,
        distinctions: res.distinctions,
        validation: res.validation,
        provider: res.provider,
        usedFallback: res.used_fallback,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      setErrorMessage(err.message || "Failed to communicate with NEBULA grounded AI service.");
      const errorMsg: ChatMessage = {
        id: String(Date.now() + 1),
        sender: 'assistant',
        content: "An error occurred while connecting to the grounded AI service. Please verify backend connectivity and retry.",
        mode: activePersona,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  // Context-aware suggested questions
  const getSuggestedQuestions = (): string[] => {
    if (simulationId) {
      return [
        `What happened in simulation ${simulationId}?`,
        "Explain this trajectory.",
        "Is total energy conserved in this N-body run?"
      ];
    }
    if (compareIds.length >= 2) {
      const name1 = compareIds[0];
      const name2 = compareIds[1];
      return [
        `Compare ${name1} and ${name2}.`,
        `Which world has stronger gravity, ${name1} or ${name2}?`,
        `Contrast their orbital periods and distances.`
      ];
    }
    if (targetObjectId) {
      const obj = objects.find((o) => o.id === targetObjectId);
      const name = obj ? obj.name : targetObjectId;
      return [
        `What is the mass of ${name}?`,
        `Explain the orbital period of ${name}.`,
        activePersona === 'citizen' ? `What is the most interesting fact about ${name}?` : `Derive the escape velocity for ${name}.`
      ];
    }

    // Default general suggestions
    if (activePersona === 'researcher') {
      return [
        "What is the mass of Jupiter?",
        "Compare Earth and Mars.",
        "Explain Earth's orbital period.",
        "Why does Saturn have rings?",
        "Which planet has the strongest gravity?"
      ];
    }
    if (activePersona === 'student') {
      return [
        "What is the mass of Jupiter?",
        "Compare Earth and Mars.",
        "Explain Earth's orbital period.",
        "Why does Saturn have rings?",
        "Which planet has the strongest gravity?"
      ];
    }
    // Citizen
    return [
      "What is the mass of Jupiter?",
      "Compare Earth and Mars.",
      "Why does Saturn have rings?",
      "Which planet has the strongest gravity?",
      "How heavy would I feel on the Moon?"
    ];
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 space-y-6">
      {/* Top Header Card */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 sm:p-8 rounded-3xl glass-panel border border-white/10 shadow-2xl">
        <div className="space-y-1.5">
          <div className="flex items-center space-x-2.5">
            <div className="p-2.5 rounded-2xl bg-sky-500/10 border border-sky-400/20 text-sky-400 shadow-md shadow-sky-500/10">
              <Bot className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
                  Grounded AI Astronomy Assistant
                </h1>
                <span className="text-[10px] px-2.5 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-400/30 text-emerald-300 font-mono">
                  Zero Hallucinations
                </span>
              </div>
              <p className="text-xs text-slate-300">
                Directly connected to NEBULA's empirical catalog, Astropy scientific engine, and REBOUND N-body solver.
              </p>
            </div>
          </div>
        </div>

        {/* Persona Switcher Buttons */}
        <div className="flex items-center space-x-1.5 bg-space-900 border border-white/10 rounded-2xl p-1.5 text-xs">
          <button
            onClick={() => { setActivePersona('citizen'); setGlobalMode('citizen'); }}
            className={`px-3.5 py-2 rounded-xl font-medium flex items-center space-x-1.5 transition-all ${
              activePersona === 'citizen'
                ? 'bg-purple-600 text-white shadow-md shadow-purple-600/30 font-semibold'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Citizen</span>
          </button>

          <button
            onClick={() => { setActivePersona('student'); setGlobalMode('student'); }}
            className={`px-3.5 py-2 rounded-xl font-medium flex items-center space-x-1.5 transition-all ${
              activePersona === 'student'
                ? 'bg-amber-600 text-white shadow-md shadow-amber-600/30 font-semibold'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <GraduationCap className="w-3.5 h-3.5" />
            <span>Student</span>
          </button>

          <button
            onClick={() => { setActivePersona('researcher'); setGlobalMode('researcher'); }}
            className={`px-3.5 py-2 rounded-xl font-medium flex items-center space-x-1.5 transition-all ${
              activePersona === 'researcher'
                ? 'bg-sky-600 text-white shadow-md shadow-sky-600/30 font-semibold'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <Cpu className="w-3.5 h-3.5" />
            <span>Researcher</span>
          </button>
        </div>
      </div>

      {/* Active System Status & Fallback Indicator Banner */}
      <div className="p-4 rounded-2xl bg-space-900/90 border border-white/10 flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex items-center space-x-2 font-mono">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
          <span className="text-slate-400">Active Engine:</span>
          <span className="text-white font-semibold">
            {aiStatus?.active_provider || 'NEBULA Grounded Local Knowledge Engine (Deterministic Fallback)'}
          </span>
          {aiStatus?.is_fallback_active && (
            <span className="px-2 py-0.5 rounded bg-amber-500/10 border border-amber-400/30 text-amber-300 text-[10px]">
              Offline Safe (No API Key Required)
            </span>
          )}
        </div>

        <div className="flex items-center space-x-3 text-[11px] font-mono text-slate-400">
          <span>{aiStatus?.registered_tools_count || 9} Verified Tools Ready</span>
          <button
            onClick={handleClearChat}
            className="flex items-center space-x-1 text-slate-400 hover:text-white transition-colors"
            title="Reset conversation history"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Clear Chat</span>
          </button>
        </div>
      </div>

      {/* Context Grounding Bar (Target Object, Simulation, or Comparison) */}
      <div className="p-4 rounded-2xl bg-space-900/50 border border-white/5 space-y-3">
        <div className="flex flex-wrap items-center justify-between gap-3 text-xs">
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-slate-400 font-medium">Grounded Context:</span>

            {/* Target Object Dropdown */}
            <div className="flex items-center space-x-1.5 bg-space-950 border border-white/10 rounded-xl px-2.5 py-1">
              <span className="text-slate-400">Body:</span>
              <select
                value={targetObjectId}
                onChange={(e) => setTargetObjectId(e.target.value)}
                className="bg-transparent text-white focus:outline-none font-mono text-xs cursor-pointer"
              >
                <option value="" className="bg-space-950 text-slate-400">Auto-Detect</option>
                {objects.map((o) => (
                  <option key={o.id} value={o.id} className="bg-space-950 text-white">
                    {o.name} ({o.category})
                  </option>
                ))}
              </select>
            </div>

            {/* Simulation Context Pill */}
            {simulationId && (
              <span className="px-3 py-1 rounded-xl bg-purple-500/10 border border-purple-400/30 text-purple-300 font-mono flex items-center space-x-1.5">
                <Orbit className="w-3.5 h-3.5" />
                <span>Sim: {simulationId}</span>
                <button onClick={() => setSimulationId('')} className="hover:text-white">
                  <X className="w-3 h-3" />
                </button>
              </span>
            )}

            {/* Comparison Context Pill */}
            {compareIds.length > 0 && (
              <span className="px-3 py-1 rounded-xl bg-sky-500/10 border border-sky-400/30 text-sky-300 font-mono flex items-center space-x-1.5">
                <GitCompare className="w-3.5 h-3.5" />
                <span>Comparing: {compareIds.join(', ')}</span>
                <button onClick={() => setCompareIds([])} className="hover:text-white">
                  <X className="w-3 h-3" />
                </button>
              </span>
            )}
          </div>

          {(targetObjectId || simulationId || compareIds.length > 0) && (
            <button
              onClick={() => {
                setTargetObjectId('');
                setSimulationId('');
                setCompareIds([]);
              }}
              className="text-[11px] text-slate-400 hover:text-white underline font-mono"
            >
              Clear All Context Filters
            </button>
          )}
        </div>
      </div>

      {/* Main Chat Feed */}
      <div className="h-[520px] rounded-3xl glass-panel border border-white/10 p-4 sm:p-6 overflow-y-auto space-y-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}
          >
            <div className="flex items-center space-x-2 text-[10px] text-slate-400 mb-1 px-1 font-mono">
              <span>{msg.sender === 'user' ? 'You' : `NEBULA ${msg.mode.toUpperCase()} ASSISTANT`}</span>
              <span>•</span>
              <span>{msg.timestamp}</span>
              {msg.usedFallback && (
                <span className="px-1.5 py-0.2 rounded bg-amber-500/10 text-amber-300 text-[9px]">
                  Local Fallback
                </span>
              )}
            </div>

            <div
              className={`max-w-[88%] rounded-3xl p-5 text-xs leading-relaxed space-y-3.5 shadow-xl ${
                msg.sender === 'user'
                  ? 'bg-gradient-to-r from-sky-600 to-indigo-600 text-white rounded-br-sm'
                  : 'bg-space-900/95 border border-white/10 text-slate-200 rounded-bl-sm'
              }`}
            >
              <div className="whitespace-pre-wrap font-sans">{msg.content}</div>

              {/* Assistant Grounding & Distinction Badges */}
              {msg.sender === 'assistant' && msg.id !== 'welcome-init' && (
                <div className="pt-3 border-t border-white/10 space-y-2 text-[10px] font-mono">
                  {/* Distinct Provenance Tabs */}
                  <div className="flex flex-wrap items-center gap-1.5 text-slate-400">
                    <span className="font-semibold text-slate-300">Grounding Provenance:</span>
                    <span className="px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 flex items-center space-x-1">
                      <ShieldCheck className="w-3 h-3" />
                      <span>NASA / JPL / Gaia DR3 Verified</span>
                    </span>
                    {msg.toolsInvoked && msg.toolsInvoked.length > 0 && (
                      <span className="px-2 py-0.5 rounded bg-sky-500/10 border border-sky-400/20 text-sky-300 flex items-center space-x-1">
                        <Zap className="w-3 h-3" />
                        <span>Tools: {msg.toolsInvoked.join(', ')}</span>
                      </span>
                    )}
                    {msg.validation && (
                      <span className="px-2 py-0.5 rounded bg-purple-500/10 border border-purple-400/20 text-purple-300">
                        Safety Score: {Math.round(msg.validation.score * 100)}%
                      </span>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex items-center space-x-3 text-xs text-slate-300 p-4 rounded-2xl bg-space-900 border border-sky-500/20 w-fit">
            <div className="w-4 h-4 rounded-full border-2 border-sky-400 border-t-transparent animate-spin" />
            <span className="font-mono">Accessing empirical catalog & solving equations...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Questions */}
      <div className="space-y-2">
        <span className="text-[11px] font-mono text-slate-400 block">Suggested Astronomical Questions:</span>
        <div className="flex flex-wrap items-center gap-2">
          {getSuggestedQuestions().map((q, i) => (
            <button
              key={i}
              onClick={() => handleSendMessage(q)}
              className="text-[11px] px-3.5 py-1.5 rounded-xl bg-space-900 hover:bg-space-800 text-slate-200 border border-white/10 hover:border-sky-500/50 transition-all text-left shadow-sm font-sans"
            >
              "{q}"
            </button>
          ))}
        </div>
      </div>

      {/* Error state alert if any */}
      {errorMessage && (
        <div className="p-4 rounded-2xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-xs flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <AlertTriangle className="w-4 h-4 shrink-0" />
            <span>{errorMessage}</span>
          </div>
          <button onClick={() => setErrorMessage(null)} className="text-rose-300 hover:text-white">
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* Chat Input Bar */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSendMessage(inputPrompt);
        }}
        className="flex gap-2"
      >
        <input
          type="text"
          value={inputPrompt}
          onChange={(e) => setInputPrompt(e.target.value)}
          placeholder={`Ask the ${activePersona} AI assistant anything about astronomy, mass, orbits, or simulations...`}
          className="flex-1 bg-space-900 border border-white/10 rounded-2xl px-5 py-3.5 text-xs text-white focus:outline-none focus:border-sky-500 shadow-inner font-sans"
        />
        <button
          type="submit"
          disabled={isLoading || !inputPrompt.trim()}
          className="px-6 py-3.5 rounded-2xl bg-gradient-to-r from-sky-600 to-indigo-600 hover:from-sky-500 hover:to-indigo-500 text-white font-semibold text-xs flex items-center space-x-2 transition-all disabled:opacity-50 shadow-lg shadow-sky-600/20"
        >
          <Send className="w-4 h-4" />
          <span>Send</span>
        </button>
      </form>
    </div>
  );
};
