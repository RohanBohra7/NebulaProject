import React, { useEffect, useState, useRef } from 'react';
import {
  evaluateResearch,
  fetchResearchHistory,
  fetchResearchBenchmarks,
  fetchEvaluationTasks,
  startEvaluationTask,
  completeEvaluationTask,
  runAutomatedTask,
  runAllTasksAutomated,
  fetchScientificValidation,
  fetchTelemetrySummary
} from '../services/api';
import {
  ResearchEvaluationResult,
  EvaluationTask,
  ScientificValidationSuiteReport,
  TelemetrySummary
} from '../types/astronomy';
import {
  BarChart3,
  Sparkles,
  Zap,
  Cpu,
  GraduationCap,
  Layers,
  Activity,
  CheckCircle2,
  XCircle,
  Play,
  RotateCcw,
  Clock,
  Compass,
  Scale,
  ShieldCheck,
  ExternalLink,
  Atom,
  Eye,
  AlertTriangle,
  Radio
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
  Cell
} from 'recharts';

export const ResearchEvaluationPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'tasks' | 'validation' | 'telemetry' | 'personas'>('tasks');

  // Predefined Tasks State
  const [tasks, setTasks] = useState<EvaluationTask[]>([]);
  const [tasksLoading, setTasksLoading] = useState(false);
  const [runningAllTasks, setRunningAllTasks] = useState(false);
  const [activeTaskSession, setActiveTaskSession] = useState<{
    taskId: string;
    sessionId: string;
    startTime: number;
    elapsedSeconds: number;
  } | null>(null);

  // Scientific Validation State
  const [validationReport, setValidationReport] = useState<ScientificValidationSuiteReport | null>(null);
  const [validationLoading, setValidationLoading] = useState(false);

  // Telemetry Summary State
  const [telemetry, setTelemetry] = useState<TelemetrySummary | null>(null);
  const [telemetryLoading, setTelemetryLoading] = useState(false);

  // Persona Live Evaluation State
  const [evalQuery, setEvalQuery] = useState('How does TRAPPIST-1e compare to Earth in terms of mass, habitability, and orbital period?');
  const [evalResult, setEvalResult] = useState<ResearchEvaluationResult | null>(null);
  const [evalHistory, setEvalHistory] = useState<any[]>([]);
  const [benchmarks, setBenchmarks] = useState<any | null>(null);
  const [personaLoading, setPersonaLoading] = useState(false);
  const timerRef = useRef<any>(null);

  // Load initial data
  useEffect(() => {
    loadAllData();
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, []);

  // Timer interval for active stopwatch
  useEffect(() => {
    if (activeTaskSession) {
      timerRef.current = setInterval(() => {
        setActiveTaskSession((prev) => {
          if (!prev) return null;
          return {
            ...prev,
            elapsedSeconds: Math.floor((Date.now() - prev.startTime) / 1000)
          };
        });
      }, 1000);
    } else {
      if (timerRef.current) clearInterval(timerRef.current);
    }
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [activeTaskSession?.sessionId]);

  const loadAllData = async () => {
    setTasksLoading(true);
    setValidationLoading(true);
    setTelemetryLoading(true);

    try {
      const [tList, vReport, telSummary, bMarks, hist] = await Promise.all([
        fetchEvaluationTasks().catch(() => []),
        fetchScientificValidation().catch(() => null),
        fetchTelemetrySummary().catch(() => null),
        fetchResearchBenchmarks().catch(() => null),
        fetchResearchHistory().catch(() => [])
      ]);

      setTasks(tList);
      setValidationReport(vReport);
      setTelemetry(telSummary);
      setBenchmarks(bMarks);
      setEvalHistory(hist);
    } catch (err) {
      console.error('Error loading evaluation data', err);
    } finally {
      setTasksLoading(false);
      setValidationLoading(false);
      setTelemetryLoading(false);
    }

    // Run initial persona evaluation
    handleRunPersonaEvaluation(evalQuery);
  };

  const handleStartTask = async (taskId: string) => {
    try {
      const res = await startEvaluationTask(taskId);
      setActiveTaskSession({
        taskId,
        sessionId: res.session_id,
        startTime: Date.now(),
        elapsedSeconds: 0
      });
    } catch (e) {
      console.error(e);
    }
  };

  const handleCompleteTask = async (taskId: string, success: boolean) => {
    if (!activeTaskSession || activeTaskSession.taskId !== taskId) return;
    const durationMs = Date.now() - activeTaskSession.startTime;

    try {
      await completeEvaluationTask(taskId, {
        session_id: activeTaskSession.sessionId,
        success,
        duration_ms: durationMs,
        metadata: {
          task_id: taskId,
          user_verification: true
        }
      });
      setActiveTaskSession(null);
      // Refresh tasks & telemetry
      const [updatedTasks, updatedTel] = await Promise.all([
        fetchEvaluationTasks(),
        fetchTelemetrySummary()
      ]);
      setTasks(updatedTasks);
      setTelemetry(updatedTel);
    } catch (e) {
      console.error(e);
    }
  };

  const handleRunAutomatedSingle = async (taskId: string) => {
    try {
      await runAutomatedTask(taskId);
      const [updatedTasks, updatedTel] = await Promise.all([
        fetchEvaluationTasks(),
        fetchTelemetrySummary()
      ]);
      setTasks(updatedTasks);
      setTelemetry(updatedTel);
    } catch (e) {
      console.error(e);
    }
  };

  const handleRunAllAutomated = async () => {
    setRunningAllTasks(true);
    try {
      await runAllTasksAutomated();
      const [updatedTasks, updatedTel, updatedVal] = await Promise.all([
        fetchEvaluationTasks(),
        fetchTelemetrySummary(),
        fetchScientificValidation()
      ]);
      setTasks(updatedTasks);
      setTelemetry(updatedTel);
      setValidationReport(updatedVal);
    } catch (e) {
      console.error(e);
    } finally {
      setRunningAllTasks(false);
    }
  };

  const handleRunPersonaEvaluation = async (queryText: string) => {
    setPersonaLoading(true);
    try {
      const res = await evaluateResearch(queryText);
      setEvalResult(res);
      fetchResearchHistory().then(setEvalHistory);
    } catch (e) {
      console.error(e);
    } finally {
      setPersonaLoading(false);
    }
  };

  const sampleQueries = [
    "How does TRAPPIST-1e compare to Earth in terms of mass, habitability, and orbital period?",
    "Explain the gravitational properties and orbital mechanics of Jupiter.",
    "Describe the relativistic characteristics of Sagittarius A*.",
    "How do Hohmann transfer orbits allow spacecraft to travel from Earth to Mars?"
  ];

  // Chart data for Persona metrics
  const personaChartData = evalResult
    ? [
        {
          metric: 'FK Grade Level',
          Researcher: evalResult.researcher.flesch_kincaid_grade,
          Student: evalResult.student.flesch_kincaid_grade,
          Citizen: evalResult.citizen.flesch_kincaid_grade,
        },
        {
          metric: 'Tech Density (%)',
          Researcher: evalResult.researcher.technical_term_density_percent,
          Student: evalResult.student.technical_term_density_percent,
          Citizen: evalResult.citizen.technical_term_density_percent,
        },
        {
          metric: 'Words / Sentence',
          Researcher: evalResult.researcher.avg_words_per_sentence,
          Student: evalResult.student.avg_words_per_sentence,
          Citizen: evalResult.citizen.avg_words_per_sentence,
        },
        {
          metric: 'LaTeX Formulas',
          Researcher: evalResult.researcher.math_expressions_count,
          Student: evalResult.student.math_expressions_count,
          Citizen: evalResult.citizen.math_expressions_count,
        }
      ]
    : [];

  // Chart data for Telemetry Task Categories
  const categoryChartData = telemetry?.task_completion?.tasks_by_category
    ? Object.entries(telemetry.task_completion.tasks_by_category).map(([cat, d]) => ({
        category: cat,
        duration: d.avg_duration_ms,
        successRate: d.success_rate_pct
      }))
    : [];

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8">
      {/* Research Header Banner */}
      <div className="p-8 rounded-3xl glass-panel-glow border border-sky-500/20 space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-sky-500/10 text-sky-300 border border-sky-400/20 text-xs font-mono">
            <BarChart3 className="w-3.5 h-3.5" />
            <span>NEBULA Research Evaluation Engine • Phase 9 Verification</span>
          </div>

          <div className="inline-flex items-center space-x-2 text-xs font-mono text-emerald-400 bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/20">
            <ShieldCheck className="w-4 h-4" />
            <span>Empirical Grounding • Zero Fabricated Metrics</span>
          </div>
        </div>

        <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          System Evaluation & Scientific Validation Benchmarks
        </h1>
        <p className="text-sm text-slate-300 max-w-4xl leading-relaxed">
          Quantitative assessment framework measuring platform performance across canonical usability tasks,
          IAU/NASA empirical physical tolerances, system interaction telemetry, and multi-persona cognitive divergence.
        </p>

        {/* Tab Navigation Navigation Buttons */}
        <div className="flex flex-wrap gap-2 pt-4 border-t border-white/10">
          <button
            onClick={() => setActiveTab('tasks')}
            className={`px-4 py-2 rounded-xl text-xs font-semibold flex items-center space-x-2 transition-all ${
              activeTab === 'tasks'
                ? 'bg-sky-500 text-white shadow-lg shadow-sky-500/25'
                : 'bg-white/5 text-slate-400 hover:text-white hover:bg-white/10'
            }`}
          >
            <CheckCircle2 className="w-4 h-4" />
            <span>1. Canonical Tasks ({tasks.length})</span>
          </button>

          <button
            onClick={() => setActiveTab('validation')}
            className={`px-4 py-2 rounded-xl text-xs font-semibold flex items-center space-x-2 transition-all ${
              activeTab === 'validation'
                ? 'bg-sky-500 text-white shadow-lg shadow-sky-500/25'
                : 'bg-white/5 text-slate-400 hover:text-white hover:bg-white/10'
            }`}
          >
            <Atom className="w-4 h-4" />
            <span>2. Scientific Empirical Validation ({validationReport?.total_benchmarks || 9})</span>
          </button>

          <button
            onClick={() => setActiveTab('telemetry')}
            className={`px-4 py-2 rounded-xl text-xs font-semibold flex items-center space-x-2 transition-all ${
              activeTab === 'telemetry'
                ? 'bg-sky-500 text-white shadow-lg shadow-sky-500/25'
                : 'bg-white/5 text-slate-400 hover:text-white hover:bg-white/10'
            }`}
          >
            <Activity className="w-4 h-4" />
            <span>3. System Telemetry & Performance</span>
          </button>

          <button
            onClick={() => setActiveTab('personas')}
            className={`px-4 py-2 rounded-xl text-xs font-semibold flex items-center space-x-2 transition-all ${
              activeTab === 'personas'
                ? 'bg-sky-500 text-white shadow-lg shadow-sky-500/25'
                : 'bg-white/5 text-slate-400 hover:text-white hover:bg-white/10'
            }`}
          >
            <Layers className="w-4 h-4" />
            <span>4. Multi-Persona Cognitive Divergence</span>
          </button>
        </div>
      </div>

      {/* ========================================================================= */}
      {/* TAB 1: PREDEFINED EVALUATION TASKS                                        */}
      {/* ========================================================================= */}
      {activeTab === 'tasks' && (
        <div className="space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6 rounded-2xl glass-panel border border-white/10">
            <div>
              <h2 className="text-xl font-bold text-white flex items-center space-x-2">
                <CheckCircle2 className="w-5 h-5 text-sky-400" />
                <span>Predefined Canonical Usability Tasks</span>
              </h2>
              <p className="text-xs text-slate-400 mt-1">
                Execute structured benchmark tasks to evaluate discovery latency, comparison generation, 3D visualization, N-body accuracy, and AI reasoning.
              </p>
            </div>

            <button
              onClick={handleRunAllAutomated}
              disabled={runningAllTasks}
              className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-semibold text-xs flex items-center space-x-2 transition-all shadow-md disabled:opacity-50"
            >
              <RotateCcw className={`w-4 h-4 ${runningAllTasks ? 'animate-spin' : ''}`} />
              <span>{runningAllTasks ? 'Executing All Tasks...' : 'Run All 6 Automated Benchmarks'}</span>
            </button>
          </div>

          {/* Active Stopwatch Notification if a task is running */}
          {activeTaskSession && (
            <div className="p-4 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-between animate-pulse">
              <div className="flex items-center space-x-3">
                <Clock className="w-5 h-5 text-amber-400 animate-spin" />
                <div>
                  <span className="text-xs font-semibold text-white">Interactive Task Active: </span>
                  <span className="text-xs text-amber-300 font-mono">
                    {tasks.find((t) => t.id === activeTaskSession.taskId)?.name}
                  </span>
                  <div className="text-[11px] text-slate-400">
                    Perform the action in the UI, then mark completed below. Elapsed: {activeTaskSession.elapsedSeconds}s
                  </div>
                </div>
              </div>

              <div className="flex items-center space-x-2">
                <button
                  onClick={() => handleCompleteTask(activeTaskSession.taskId, true)}
                  className="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold"
                >
                  Mark Passed
                </button>
                <button
                  onClick={() => handleCompleteTask(activeTaskSession.taskId, false)}
                  className="px-3 py-1.5 rounded-lg bg-rose-600 hover:bg-rose-500 text-white text-xs font-bold"
                >
                  Mark Failed
                </button>
              </div>
            </div>
          )}

          {/* Task Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {tasks.map((task) => {
              const isSessionActive = activeTaskSession?.taskId === task.id;
              const hasRun = !!task.last_run;
              const passed = task.last_run?.success;

              return (
                <div
                  key={task.id}
                  className={`p-6 rounded-2xl glass-panel border transition-all flex flex-col justify-between space-y-4 ${
                    isSessionActive
                      ? 'border-amber-500/50 bg-amber-500/5'
                      : passed
                      ? 'border-emerald-500/30'
                      : hasRun
                      ? 'border-rose-500/30'
                      : 'border-white/10'
                  }`}
                >
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-[11px] font-mono px-2.5 py-0.5 rounded-full bg-white/5 text-slate-400 border border-white/5">
                        Task #{task.task_number} • {task.category}
                      </span>
                      {hasRun && (
                        <span
                          className={`text-[11px] font-mono px-2.5 py-0.5 rounded-full flex items-center space-x-1 ${
                            passed
                              ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                              : 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                          }`}
                        >
                          {passed ? <CheckCircle2 className="w-3 h-3" /> : <XCircle className="w-3 h-3" />}
                          <span>{passed ? 'Passed' : 'Failed'}</span>
                        </span>
                      )}
                    </div>

                    <h3 className="text-base font-bold text-white leading-tight">
                      {task.name}
                    </h3>

                    <p className="text-xs text-slate-300 leading-relaxed">
                      {task.instruction}
                    </p>

                    <div className="p-3 rounded-xl bg-space-900 border border-white/5 space-y-1.5 text-[11px] font-mono">
                      <div className="text-slate-400">
                        <strong className="text-slate-300">Criteria:</strong> {task.success_criteria}
                      </div>
                      <div className="text-slate-400">
                        <strong className="text-slate-300">Expected:</strong>{' '}
                        <span className="text-sky-400">{task.expected_value}</span>
                      </div>
                      {task.last_run && (
                        <div className="pt-1.5 border-t border-white/5 flex justify-between text-slate-400">
                          <span>Latency: {task.last_run.duration_ms.toFixed(1)} ms</span>
                          <span className="capitalize">{task.last_run.status}</span>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Task Actions */}
                  <div className="pt-3 border-t border-white/10 flex items-center justify-between gap-2">
                    {isSessionActive ? (
                      <div className="flex items-center space-x-2 w-full">
                        <button
                          onClick={() => handleCompleteTask(task.id, true)}
                          className="flex-1 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold"
                        >
                          Finish (Pass)
                        </button>
                        <button
                          onClick={() => handleCompleteTask(task.id, false)}
                          className="px-3 py-2 rounded-xl bg-rose-600 hover:bg-rose-500 text-white text-xs"
                        >
                          Fail
                        </button>
                      </div>
                    ) : (
                      <>
                        <button
                          onClick={() => handleStartTask(task.id)}
                          className="px-3 py-2 rounded-xl bg-white/5 hover:bg-white/10 text-white text-xs font-medium flex items-center space-x-1.5 border border-white/5 transition-all"
                        >
                          <Play className="w-3.5 h-3.5 text-sky-400" />
                          <span>Start Timer</span>
                        </button>

                        <button
                          onClick={() => handleRunAutomatedSingle(task.id)}
                          className="px-3 py-2 rounded-xl bg-sky-500/20 hover:bg-sky-500/30 text-sky-300 text-xs font-semibold flex items-center space-x-1.5 border border-sky-500/30 transition-all"
                        >
                          <Zap className="w-3.5 h-3.5" />
                          <span>Verify Auto</span>
                        </button>
                      </>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* TAB 2: SCIENTIFIC EMPIRICAL VALIDATION BENCHMARKS                          */}
      {/* ========================================================================= */}
      {activeTab === 'validation' && (
        <div className="space-y-6">
          <div className="p-6 rounded-2xl glass-panel border border-white/10 space-y-2">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h2 className="text-xl font-bold text-white flex items-center space-x-2">
                  <Atom className="w-5 h-5 text-indigo-400" />
                  <span>Scientific Validation Against Empirical Ground Truth</span>
                </h2>
                <p className="text-xs text-slate-400 mt-1">
                  Evaluated with explicit physical tolerances representing standard astronomical approximations.
                  Exact matches are not claimed, and arbitrary accuracy percentages are never fabricated.
                </p>
              </div>

              {validationReport && (
                <div className="flex items-center space-x-3 text-xs font-mono">
                  <div className="px-3 py-1.5 rounded-xl bg-emerald-500/10 text-emerald-300 border border-emerald-500/20">
                    Passed: <strong>{validationReport.passed_count}</strong> / {validationReport.total_benchmarks}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Validation Table */}
          <div className="rounded-2xl glass-panel border border-white/10 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-space-900 border-b border-white/10 text-slate-400 font-mono uppercase text-[11px]">
                  <tr>
                    <th className="p-4">Benchmark Property</th>
                    <th className="p-4">Mathematical Formulation</th>
                    <th className="p-4">Computed Value</th>
                    <th className="p-4">Empirical Reference</th>
                    <th className="p-4">Tolerance (±ε)</th>
                    <th className="p-4">Absolute Error</th>
                    <th className="p-4">Reference Source</th>
                    <th className="p-4 text-center">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5 font-mono">
                  {validationReport?.benchmarks.map((b) => (
                    <tr key={b.id} className="hover:bg-white/5 transition-colors">
                      <td className="p-4 font-sans font-semibold text-white">
                        <div>{b.property_name}</div>
                        <span className="text-[10px] text-slate-500 uppercase">{b.category}</span>
                      </td>
                      <td className="p-4 text-slate-300 font-mono text-[11px]">
                        <code>{b.formula}</code>
                      </td>
                      <td className="p-4 text-sky-400 font-bold">
                        {typeof b.computed_value === 'number'
                          ? b.computed_value < 1e-4
                            ? b.computed_value.toExponential(4)
                            : b.computed_value.toFixed(4)
                          : b.computed_value}{' '}
                        <span className="text-[10px] text-slate-400 font-normal">{b.units}</span>
                      </td>
                      <td className="p-4 text-slate-200">
                        {typeof b.reference_value === 'number'
                          ? b.reference_value < 1e-4
                            ? b.reference_value.toExponential(4)
                            : b.reference_value.toFixed(4)
                          : b.reference_value}{' '}
                        <span className="text-[10px] text-slate-400 font-normal">{b.units}</span>
                      </td>
                      <td className="p-4 text-amber-400">
                        ±{b.tolerance < 1e-3 ? b.tolerance.toExponential(2) : b.tolerance}{' '}
                        <span className="text-[10px] text-slate-400 font-normal">{b.units}</span>
                      </td>
                      <td className="p-4 text-slate-300">
                        {b.absolute_error < 1e-4 ? b.absolute_error.toExponential(4) : b.absolute_error.toFixed(5)}
                      </td>
                      <td className="p-4 font-sans text-slate-400 text-[11px] max-w-xs truncate">
                        {b.reference_source}
                      </td>
                      <td className="p-4 text-center">
                        <span
                          className={`inline-flex items-center space-x-1 px-2.5 py-1 rounded-full text-[11px] ${
                            b.passed
                              ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                              : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                          }`}
                        >
                          {b.passed ? <CheckCircle2 className="w-3.5 h-3.5" /> : <XCircle className="w-3.5 h-3.5" />}
                          <span>{b.passed ? 'PASSED' : 'OUT_OF_BOUNDS'}</span>
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {validationReport?.scientific_disclaimer && (
              <div className="p-4 bg-space-900 border-t border-white/10 text-[11px] text-slate-400 flex items-start space-x-2">
                <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                <span>{validationReport.scientific_disclaimer}</span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* TAB 3: SYSTEM TELEMETRY & PERFORMANCE METRICS                              */}
      {/* ========================================================================= */}
      {activeTab === 'telemetry' && (
        <div className="space-y-6">
          <div className="p-6 rounded-2xl glass-panel border border-white/10 space-y-2">
            <h2 className="text-xl font-bold text-white flex items-center space-x-2">
              <Activity className="w-5 h-5 text-emerald-400" />
              <span>Operational & Performance Telemetry</span>
            </h2>
            <p className="text-xs text-slate-400">
              Aggregated platform metrics monitoring task execution, discovery speed, 3D viewport events, simulation integration, and AI response latencies.
            </p>
          </div>

          {/* Metric KPI Cards */}
          {telemetry && (
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
              <div className="p-4 rounded-2xl glass-panel border border-white/10 space-y-1">
                <span className="text-[11px] text-slate-400 font-mono">Task Success Rate</span>
                <div className="text-2xl font-extrabold text-emerald-400">
                  {telemetry.task_completion.success_rate_percent}%
                </div>
                <span className="text-[10px] text-slate-500">{telemetry.task_completion.total_executed} runs total</span>
              </div>

              <div className="p-4 rounded-2xl glass-panel border border-white/10 space-y-1">
                <span className="text-[11px] text-slate-400 font-mono">Avg Task Latency</span>
                <div className="text-2xl font-extrabold text-sky-400">
                  {telemetry.task_completion.avg_completion_time_ms.toFixed(1)} <span className="text-xs font-normal text-slate-400">ms</span>
                </div>
                <span className="text-[10px] text-slate-500">Automated / user verified</span>
              </div>

              <div className="p-4 rounded-2xl glass-panel border border-white/10 space-y-1">
                <span className="text-[11px] text-slate-400 font-mono">Object Discovery</span>
                <div className="text-2xl font-extrabold text-indigo-400">
                  {telemetry.object_discovery.avg_discovery_time_ms.toFixed(1)} <span className="text-xs font-normal text-slate-400">ms</span>
                </div>
                <span className="text-[10px] text-slate-500">{telemetry.object_discovery.total_discovery_events} searches</span>
              </div>

              <div className="p-4 rounded-2xl glass-panel border border-white/10 space-y-1">
                <span className="text-[11px] text-slate-400 font-mono">Sim Max Energy Error</span>
                <div className="text-2xl font-extrabold text-purple-400">
                  {telemetry.simulation.avg_max_energy_drift < 1e-4
                    ? telemetry.simulation.avg_max_energy_drift.toExponential(1)
                    : telemetry.simulation.avg_max_energy_drift.toFixed(5)}
                </div>
                <span className="text-[10px] text-slate-500">{telemetry.simulation.total_simulations_executed} runs</span>
              </div>

              <div className="p-4 rounded-2xl glass-panel border border-white/10 space-y-1">
                <span className="text-[11px] text-slate-400 font-mono">AI Grounding Rate</span>
                <div className="text-2xl font-extrabold text-amber-400">
                  {telemetry.ai_interactions.grounding_fidelity_percent}%
                </div>
                <span className="text-[10px] text-slate-500">Latency: {telemetry.ai_interactions.avg_latency_ms.toFixed(1)}ms</span>
              </div>

              <div className="p-4 rounded-2xl glass-panel border border-white/10 space-y-1">
                <span className="text-[11px] text-slate-400 font-mono">System Error Rate</span>
                <div className="text-2xl font-extrabold text-emerald-400">
                  {telemetry.system_performance.error_rate_percent}%
                </div>
                <span className="text-[10px] text-slate-500">{telemetry.system_performance.total_errors} errors recorded</span>
              </div>
            </div>
          )}

          {/* Telemetry Charts Section */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Task Category Duration Chart */}
            <div className="p-6 rounded-2xl glass-panel border border-white/10 space-y-4">
              <h3 className="text-sm font-bold text-white flex items-center space-x-2">
                <BarChart3 className="w-4 h-4 text-sky-400" />
                <span>Task Execution Latency by Domain (ms)</span>
              </h3>
              <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={categoryChartData}>
                    <XAxis dataKey="category" stroke="#64748b" fontSize={10} />
                    <YAxis stroke="#64748b" fontSize={10} />
                    <Tooltip
                      contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '11px' }}
                    />
                    <Bar dataKey="duration" fill="#38bdf8" radius={[6, 6, 0, 0]} name="Avg Duration (ms)" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Interaction Distribution Breakdown */}
            <div className="p-6 rounded-2xl glass-panel border border-white/10 space-y-4">
              <h3 className="text-sm font-bold text-white flex items-center space-x-2">
                <Radio className="w-4 h-4 text-purple-400" />
                <span>System Interaction Event Breakdown</span>
              </h3>
              <div className="space-y-3 pt-2">
                {telemetry && Object.entries(telemetry.event_distribution).map(([evType, count]) => {
                  const pct = Math.round((count / telemetry.total_telemetry_events) * 100);
                  return (
                    <div key={evType} className="space-y-1">
                      <div className="flex justify-between text-xs font-mono">
                        <span className="text-slate-300 capitalize">{evType.replace(/_/g, ' ')}</span>
                        <span className="text-slate-400">{count} events ({pct}%)</span>
                      </div>
                      <div className="h-2 w-full rounded-full bg-space-900 overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-sky-500 to-indigo-500 rounded-full"
                          style={{ width: `${pct}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* TAB 4: MULTI-PERSONA COGNITIVE DIVERGENCE EXPERIMENT                       */}
      {/* ========================================================================= */}
      {activeTab === 'personas' && (
        <div className="space-y-6">
          <div className="p-6 rounded-2xl glass-panel border border-white/10 space-y-6">
            <div>
              <h2 className="text-xl font-bold text-white flex items-center space-x-2">
                <Zap className="w-5 h-5 text-amber-400" />
                <span>Parallel Multi-Persona Evaluation Experiment</span>
              </h2>
              <p className="text-xs text-slate-400 mt-1">
                Evaluates identical queries across Researcher, Student, and Citizen personas simultaneously under identical grounding conditions.
              </p>
            </div>

            {/* Query presets */}
            <div className="flex flex-wrap gap-2 text-xs">
              <span className="text-slate-400 self-center font-mono text-[11px]">Presets:</span>
              {sampleQueries.map((q, i) => (
                <button
                  key={i}
                  onClick={() => { setEvalQuery(q); handleRunPersonaEvaluation(q); }}
                  className="px-3 py-1 rounded-xl bg-white/5 hover:bg-white/10 text-slate-300 border border-white/5 transition-all text-left"
                >
                  {q.slice(0, 45)}...
                </button>
              ))}
            </div>

            {/* Query input */}
            <div className="flex gap-2">
              <input
                type="text"
                value={evalQuery}
                onChange={(e) => setEvalQuery(e.target.value)}
                className="flex-1 bg-space-900 border border-white/10 rounded-xl px-4 py-2.5 text-xs text-white focus:outline-none focus:border-sky-500"
              />
              <button
                onClick={() => handleRunPersonaEvaluation(evalQuery)}
                disabled={personaLoading || !evalQuery.trim()}
                className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-semibold text-xs flex items-center space-x-2 transition-all shadow-md disabled:opacity-50"
              >
                <Activity className="w-4 h-4" />
                <span>{personaLoading ? 'Evaluating...' : 'Run Parallel Evaluation'}</span>
              </button>
            </div>

            {/* Comparative Divergence Chart */}
            {evalResult && personaChartData.length > 0 && (
              <div className="pt-6 border-t border-white/10 space-y-4">
                <h4 className="text-sm font-bold text-white flex items-center space-x-2">
                  <Scale className="w-4 h-4 text-purple-400" />
                  <span>Quantitative Complexity Divergence Chart</span>
                </h4>

                <div className="h-72 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={personaChartData}>
                      <XAxis dataKey="metric" stroke="#64748b" fontSize={11} />
                      <YAxis stroke="#64748b" fontSize={11} />
                      <Tooltip
                        contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '11px' }}
                      />
                      <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
                      <Bar dataKey="Researcher" fill="#38bdf8" radius={[6, 6, 0, 0]} />
                      <Bar dataKey="Student" fill="#fbbf24" radius={[6, 6, 0, 0]} />
                      <Bar dataKey="Citizen" fill="#c084fc" radius={[6, 6, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            )}

            {/* 3-Column Persona Cards */}
            {evalResult && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-4">
                {/* Researcher */}
                <div className="p-5 rounded-2xl glass-panel border border-sky-500/30 space-y-4 flex flex-col justify-between">
                  <div className="space-y-3">
                    <div className="flex items-center space-x-2 text-sky-400">
                      <Cpu className="w-4 h-4" />
                      <h4 className="text-base font-bold text-white">Researcher Output</h4>
                    </div>

                    <div className="grid grid-cols-2 gap-2 text-[11px] font-mono">
                      <div className="p-2 rounded-lg bg-space-900 border border-white/5">
                        <span className="text-slate-400 block font-sans">FK Grade Level</span>
                        <strong className="text-sky-400 text-sm">{evalResult.researcher.flesch_kincaid_grade}</strong>
                      </div>
                      <div className="p-2 rounded-lg bg-space-900 border border-white/5">
                        <span className="text-slate-400 block font-sans">Reading Ease</span>
                        <strong className="text-white text-sm">{evalResult.researcher.flesch_reading_ease}</strong>
                      </div>
                      <div className="p-2 rounded-lg bg-space-900 border border-white/5">
                        <span className="text-slate-400 block font-sans">Tech Density</span>
                        <strong className="text-emerald-400 text-sm">{evalResult.researcher.technical_term_density_percent}%</strong>
                      </div>
                      <div className="p-2 rounded-lg bg-space-900 border border-white/5">
                        <span className="text-slate-400 block font-sans">Formulas</span>
                        <strong className="text-purple-400 text-sm">{evalResult.researcher.math_expressions_count}</strong>
                      </div>
                    </div>

                    <div className="max-h-60 overflow-y-auto p-3 rounded-xl bg-space-900/90 border border-white/5 text-[11px] text-slate-200 whitespace-pre-wrap leading-relaxed">
                      {evalResult.researcher.response_sample}
                    </div>
                  </div>
                </div>

                {/* Student */}
                <div className="p-5 rounded-2xl glass-panel border border-amber-500/30 space-y-4 flex flex-col justify-between">
                  <div className="space-y-3">
                    <div className="flex items-center space-x-2 text-amber-400">
                      <GraduationCap className="w-4 h-4" />
                      <h4 className="text-base font-bold text-white">Student Output</h4>
                    </div>

                    <div className="grid grid-cols-2 gap-2 text-[11px] font-mono">
                      <div className="p-2 rounded-lg bg-space-900 border border-white/5">
                        <span className="text-slate-400 block font-sans">FK Grade Level</span>
                        <strong className="text-amber-400 text-sm">{evalResult.student.flesch_kincaid_grade}</strong>
                      </div>
                      <div className="p-2 rounded-lg bg-space-900 border border-white/5">
                        <span className="text-slate-400 block font-sans">Reading Ease</span>
                        <strong className="text-white text-sm">{evalResult.student.flesch_reading_ease}</strong>
                      </div>
                      <div className="p-2 rounded-lg bg-space-900 border border-white/5">
                        <span className="text-slate-400 block font-sans">Tech Density</span>
                        <strong className="text-emerald-400 text-sm">{evalResult.student.technical_term_density_percent}%</strong>
                      </div>
                      <div className="p-2 rounded-lg bg-space-900 border border-white/5">
                        <span className="text-slate-400 block font-sans">Formulas</span>
                        <strong className="text-purple-400 text-sm">{evalResult.student.math_expressions_count}</strong>
                      </div>
                    </div>

                    <div className="max-h-60 overflow-y-auto p-3 rounded-xl bg-space-900/90 border border-white/5 text-[11px] text-slate-200 whitespace-pre-wrap leading-relaxed">
                      {evalResult.student.response_sample}
                    </div>
                  </div>
                </div>

                {/* Citizen */}
                <div className="p-5 rounded-2xl glass-panel border border-purple-500/30 space-y-4 flex flex-col justify-between">
                  <div className="space-y-3">
                    <div className="flex items-center space-x-2 text-purple-400">
                      <Sparkles className="w-4 h-4" />
                      <h4 className="text-base font-bold text-white">Citizen Output</h4>
                    </div>

                    <div className="grid grid-cols-2 gap-2 text-[11px] font-mono">
                      <div className="p-2 rounded-lg bg-space-900 border border-white/5">
                        <span className="text-slate-400 block font-sans">FK Grade Level</span>
                        <strong className="text-purple-400 text-sm">{evalResult.citizen.flesch_kincaid_grade}</strong>
                      </div>
                      <div className="p-2 rounded-lg bg-space-900 border border-white/5">
                        <span className="text-slate-400 block font-sans">Reading Ease</span>
                        <strong className="text-white text-sm">{evalResult.citizen.flesch_reading_ease}</strong>
                      </div>
                      <div className="p-2 rounded-lg bg-space-900 border border-white/5">
                        <span className="text-slate-400 block font-sans">Tech Density</span>
                        <strong className="text-emerald-400 text-sm">{evalResult.citizen.technical_term_density_percent}%</strong>
                      </div>
                      <div className="p-2 rounded-lg bg-space-900 border border-white/5">
                        <span className="text-slate-400 block font-sans">Formulas</span>
                        <strong className="text-purple-400 text-sm">{evalResult.citizen.math_expressions_count}</strong>
                      </div>
                    </div>

                    <div className="max-h-60 overflow-y-auto p-3 rounded-xl bg-space-900/90 border border-white/5 text-[11px] text-slate-200 whitespace-pre-wrap leading-relaxed">
                      {evalResult.citizen.response_sample}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
