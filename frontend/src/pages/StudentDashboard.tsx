import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { chatAI } from '../services/api';
import {
  GraduationCap,
  BookOpen,
  Award,
  Sparkles,
  Sliders,
  Send,
  CheckCircle2,
  XCircle,
  ArrowRight,
  Compass,
  Orbit,
  Atom,
  GitCompare,
  Lightbulb,
  ExternalLink,
  HelpCircle
} from 'lucide-react';

export const StudentDashboard: React.FC = () => {
  const navigate = useNavigate();

  // Kepler's Laws Interactive Sandbox state
  const [keplerA, setKeplerA] = useState(1.0); // AU
  const [keplerE, setKeplerE] = useState(0.2); // Eccentricity

  const perihelion = keplerA * (1 - keplerE);
  const aphelion = keplerA * (1 + keplerE);
  const periodYears = Math.pow(keplerA, 1.5);
  const speedAtPerihelion = Math.sqrt((1 + keplerE) / (1 - keplerE));
  const speedAtAphelion = Math.sqrt((1 - keplerE) / (1 + keplerE));

  // Selected Concept state for expanded detail
  const [selectedConceptIndex, setSelectedConceptIndex] = useState(0);

  // Core Astronomy Concepts Data
  const astronomyConcepts = [
    {
      id: 'orbital_period',
      title: 'Orbital Period',
      tag: "Kepler's 3rd Law",
      definition:
        'The exact time required for a celestial body to complete one full revolution around its parent gravitational attractor.',
      explanation:
        "Orbital period is governed directly by Kepler's Third Law (T² ∝ a³). Because gravitational attraction weakens with distance, worlds farther from the Sun not only travel a larger orbital path but also travel at slower orbital speeds!",
      formula: 'T = 2π √(a³ / G(M + m))  ≈ √(a³)  (when a is in AU and T is in Earth years)',
      example:
        'Mercury (a = 0.387 AU) completes an orbit in 88 days. Earth (a = 1.0 AU) takes 365.25 days. Distant Neptune (a = 30.05 AU) takes 165 Earth years to complete a single year!',
      linkText: 'Experiment with Kepler Sandbox',
      linkAction: 'sandbox'
    },
    {
      id: 'gravity',
      title: 'Universal Gravity',
      tag: "Newton's Universal Law",
      definition:
        'The fundamental attractive force through which all physical bodies with mass pull on one another across spacetime.',
      explanation:
        "Newton's Universal Law of Gravitation shows gravity is an inverse-square force: doubling the distance between two objects reduces their gravitational pull to one-quarter (1/4th) of its original strength. Surface gravity (g) depends directly on the planet's mass and radius.",
      formula: 'F = G (m₁ m₂ / r²),   g = G M / R²',
      example:
        'A 70 kg student weighs ~686 Newtons on Earth (g = 9.8 m/s²), but only ~114 N on the Moon (g = 1.62 m/s²), and a crushing ~1,735 N on massive Jupiter (g = 24.79 m/s²)!',
      linkText: 'Compare Gravities Side-by-Side',
      linkAction: '/compare?obj1=earth&obj2=moon'
    },
    {
      id: 'planetary_mass',
      title: 'Planetary Mass',
      tag: 'Orbital Kinematics',
      definition:
        'The total quantitative amount of matter within a celestial body, fundamental to its gravitational pull and internal density.',
      explanation:
        "Astronomers cannot place planets on a scale! We determine a planet's mass by watching moons or visiting spacecraft orbit around it, applying Kepler's 3rd Law combined with Newton's gravitational constant (G).",
      formula: 'M = (4π² a³) / (G P²)',
      example:
        'Earth has a mass of 5.97 × 10²⁴ kg (1.0 M⊕). Jupiter contains 317.8 Earth masses—more massive than all other planets in our entire Solar System combined!',
      linkText: 'Explore Planetary Masses in Catalog',
      linkAction: '/explorer'
    },
    {
      id: 'orbital_velocity',
      title: 'Orbital Velocity',
      tag: 'Vis-Viva Dynamics',
      definition:
        'The instantaneous speed at which a celestial object moves along its curved trajectory to maintain a stable, non-decaying orbit.',
      explanation:
        'In a circular orbit, gravitational pull provides exactly the necessary centripetal acceleration to keep the planet in free-fall around the star. Planets in close orbits must move much faster to avoid spiraling into the star.',
      formula: 'v_c = √(G M / r),   v(r) = √(G M (2/r - 1/a))  (Vis-Viva Equation)',
      example:
        'Mercury speeds along at 47.4 km/s (~170,000 km/h), Earth travels at 29.8 km/s, while distant Neptune leisurely orbits at just 5.4 km/s.',
      linkText: 'Watch Planets Orbit in 3D',
      linkAction: '/visualization'
    },
    {
      id: 'nbody_simulation',
      title: 'N-Body Simulation',
      tag: 'Three-Body Problem',
      definition:
        'Numerical integration of the gravitational equations of motion for three or more bodies interacting through mutual gravity.',
      explanation:
        'While a two-body system has an exact closed-form solution (pure Keplerian conic sections), systems of 3 or more bodies cannot be solved with a simple formula. Computers must calculate mutual forces and update positions step-by-step using algorithms like REBOUND IAS15 or Symplectic Leapfrog.',
      formula: 'a_i = ∑_{j ≠ i} (G m_j (r_j - r_i)) / ||r_j - r_i||³',
      example:
        "The Sun-Earth-Moon system where the Sun's gravity constantly perturbs the Moon, or TRAPPIST-1's resonant chain of 7 planets interacting gravitationally.",
      linkText: 'Launch N-Body Lab',
      linkAction: '/simulation'
    }
  ];

  // Interactive Quiz state
  const quizQuestions = [
    {
      question: "According to Kepler's Second Law, when does a planet move fastest along its orbit?",
      options: [
        'At Aphelion (farthest point from the Sun)',
        'At Perihelion (closest point to the Sun)',
        'Its speed is always perfectly constant',
        'At the midpoint between major axes'
      ],
      correctIndex: 1,
      explanation:
        "Kepler's Second Law states that a line segment joining a planet and the Sun sweeps out equal areas in equal time intervals. Therefore, the planet travels fastest when closest to the Sun (perihelion)!"
    },
    {
      question: 'Why is Venus hotter than Mercury on average, even though Mercury is much closer to the Sun?',
      options: [
        'Venus has a higher core nuclear fusion rate',
        'Mercury has a massive ocean reflecting heat',
        'Venus has an extreme runaway greenhouse effect caused by a dense CO2 atmosphere',
        'Mercury is always shaded by asteroids'
      ],
      correctIndex: 2,
      explanation:
        'Venus has an atmosphere composed of 96.5% carbon dioxide with surface pressure 92 times that of Earth. This dense blanket traps heat relentlessly, driving temperatures to 464°C (737 K)!'
    },
    {
      question:
        "If planet A is at 1 AU and planet B is at 4 AU from the Sun, how do their orbital periods compare (Kepler's 3rd Law: T² = a³)?",
      options: [
        'Planet B takes 4 times longer',
        'Planet B takes 8 times longer (T = 4^(1.5) = 8 years)',
        'Planet B takes 16 times longer',
        'Planet B takes 2 times longer'
      ],
      correctIndex: 1,
      explanation: "Kepler's 3rd Law states T² = a³. For a = 4 AU, T = √(4³) = √64 = 8 years!"
    }
  ];

  const [currentQIndex, setCurrentQIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState<number | null>(null);
  const [showExplanation, setShowExplanation] = useState(false);
  const [score, setScore] = useState(0);

  const handleAnswer = (index: number) => {
    setSelectedOption(index);
    setShowExplanation(true);
    if (index === quizQuestions[currentQIndex].correctIndex) {
      setScore((prev) => prev + 1);
    }
  };

  const nextQuestion = () => {
    setSelectedOption(null);
    setShowExplanation(false);
    setCurrentQIndex((prev) => (prev + 1) % quizQuestions.length);
  };

  // AI Tutor state
  const [tutorPrompt, setTutorPrompt] = useState('');
  const [tutorResponse, setTutorResponse] = useState<string | null>(null);
  const [tutorLoading, setTutorLoading] = useState(false);

  const askTutor = async (q: string) => {
    setTutorLoading(true);
    setTutorPrompt(q);
    try {
      const res = await chatAI(q, 'student');
      setTutorResponse(res.response);
    } catch {
      setTutorResponse('The physics tutor is momentarily unavailable. Please retry.');
    } finally {
      setTutorLoading(false);
    }
  };

  const handleConceptLink = (action: string) => {
    if (action === 'sandbox') {
      const el = document.getElementById('kepler-sandbox');
      if (el) el.scrollIntoView({ behavior: 'smooth' });
    } else {
      navigate(action);
    }
  };

  const activeConcept = astronomyConcepts[selectedConceptIndex];

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-12">
      {/* Student Welcome Header */}
      <div className="p-8 rounded-3xl glass-panel-glow border border-amber-500/20 space-y-4">
        <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-amber-500/10 text-amber-300 border border-amber-400/20 text-xs font-mono">
          <GraduationCap className="w-3.5 h-3.5" />
          <span>Student Experience • Conceptual Mastery & Physics Scaffolding</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-white">
          Astronomy & Orbital Physics Lab
        </h1>
        <p className="text-sm text-slate-300 max-w-3xl leading-relaxed">
          Welcome to your interactive learning lab! Explore core astronomical concepts, experiment with Kepler's laws in
          real time, run guided gravitational simulations, and ask questions to your Socratic physics tutor.
        </p>

        {/* Quick Jump Bar */}
        <div className="flex flex-wrap items-center gap-2 pt-2">
          <a
            href="#concepts"
            className="px-3 py-1.5 rounded-xl bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 border border-amber-400/20 text-xs font-medium flex items-center space-x-1.5 transition-all"
          >
            <BookOpen className="w-3.5 h-3.5" />
            <span>Learn Concepts</span>
          </a>
          <Link
            to="/visualization"
            className="px-3 py-1.5 rounded-xl bg-white/5 hover:bg-white/10 text-slate-200 border border-white/10 text-xs font-medium flex items-center space-x-1.5 transition-all"
          >
            <Orbit className="w-3.5 h-3.5 text-sky-400" />
            <span>Interactive 3D</span>
          </Link>
          <a
            href="#guided-simulations"
            className="px-3 py-1.5 rounded-xl bg-white/5 hover:bg-white/10 text-slate-200 border border-white/10 text-xs font-medium flex items-center space-x-1.5 transition-all"
          >
            <Atom className="w-3.5 h-3.5 text-purple-400" />
            <span>Guided Simulations</span>
          </a>
          <Link
            to="/compare"
            className="px-3 py-1.5 rounded-xl bg-white/5 hover:bg-white/10 text-slate-200 border border-white/10 text-xs font-medium flex items-center space-x-1.5 transition-all"
          >
            <GitCompare className="w-3.5 h-3.5 text-emerald-400" />
            <span>Compare Objects</span>
          </Link>
          <a
            href="#ai-tutor"
            className="px-3 py-1.5 rounded-xl bg-white/5 hover:bg-white/10 text-slate-200 border border-white/10 text-xs font-medium flex items-center space-x-1.5 transition-all"
          >
            <Sparkles className="w-3.5 h-3.5 text-amber-400" />
            <span>AI Tutor</span>
          </a>
        </div>
      </div>

      {/* CORE ASTRONOMY CONCEPTS SECTION */}
      <div id="concepts" className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-white/10 pb-4">
          <div>
            <h2 className="text-2xl font-bold text-white flex items-center space-x-2">
              <BookOpen className="w-6 h-6 text-amber-400" />
              <span>Core Astronomy Concepts</span>
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Foundational principles with definitions, intuitive physical explanations, mathematical formulas, and real-world examples.
            </p>
          </div>
          <span className="text-xs font-mono px-3 py-1 rounded-full bg-amber-500/10 text-amber-300 border border-amber-500/20">
            5 Essential Topics
          </span>
        </div>

        {/* Concept Selector Tabs */}
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-2">
          {astronomyConcepts.map((concept, idx) => (
            <button
              key={concept.id}
              onClick={() => setSelectedConceptIndex(idx)}
              className={`p-3 rounded-2xl border text-left transition-all ${
                selectedConceptIndex === idx
                  ? 'bg-amber-500/15 border-amber-400 shadow-md shadow-amber-500/10 text-white font-bold'
                  : 'glass-panel border-white/5 text-slate-400 hover:text-slate-200 hover:border-white/20'
              }`}
            >
              <span className="text-[10px] font-mono uppercase block text-amber-400/90 tracking-wider">
                0{idx + 1} • {concept.tag}
              </span>
              <span className="text-xs font-semibold block mt-1">{concept.title}</span>
            </button>
          ))}
        </div>

        {/* Selected Concept Deep-Dive Card */}
        <div className="p-6 sm:p-8 rounded-3xl glass-panel border border-amber-500/20 space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-white/10 pb-4">
            <div>
              <span className="text-xs font-mono uppercase tracking-widest text-amber-400 font-bold">
                Concept Deep-Dive
              </span>
              <h3 className="text-2xl font-extrabold text-white mt-1">{activeConcept.title}</h3>
            </div>
            <button
              onClick={() => handleConceptLink(activeConcept.linkAction)}
              className="px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-space-950 font-bold text-xs flex items-center space-x-1.5 transition-all shadow-md shadow-amber-500/20"
            >
              <span>{activeConcept.linkText}</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
            {/* Definition & Explanation */}
            <div className="lg:col-span-7 space-y-4">
              <div className="p-4 rounded-2xl bg-space-950/60 border border-white/5 space-y-2">
                <span className="text-xs font-semibold text-amber-400 flex items-center space-x-1.5">
                  <Lightbulb className="w-4 h-4" />
                  <span>Scientific Definition:</span>
                </span>
                <p className="text-sm text-slate-200 leading-relaxed font-sans">{activeConcept.definition}</p>
              </div>

              <div className="p-4 rounded-2xl bg-space-950/60 border border-white/5 space-y-2">
                <span className="text-xs font-semibold text-sky-400 flex items-center space-x-1.5">
                  <Compass className="w-4 h-4" />
                  <span>Physical Intuition & Why It Happens:</span>
                </span>
                <p className="text-xs text-slate-300 leading-relaxed">{activeConcept.explanation}</p>
              </div>
            </div>

            {/* Formula & Real-World Example */}
            <div className="lg:col-span-5 space-y-4">
              <div className="p-4 rounded-2xl bg-space-950/80 border border-amber-500/30 space-y-2">
                <span className="text-xs font-semibold text-amber-300 font-mono">Mathematical Formulation:</span>
                <div className="p-3 rounded-xl bg-space-900 border border-white/10 font-mono text-xs text-amber-200 overflow-x-auto">
                  {activeConcept.formula}
                </div>
              </div>

              <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 space-y-2">
                <span className="text-xs font-bold text-emerald-300 flex items-center space-x-1.5">
                  <CheckCircle2 className="w-4 h-4" />
                  <span>Real-World Solar System Example:</span>
                </span>
                <p className="text-xs text-emerald-100/90 leading-relaxed">{activeConcept.example}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* GUIDED SIMULATIONS SECTION */}
      <div id="guided-simulations" className="space-y-4">
        <div className="flex items-center justify-between border-b border-white/10 pb-4">
          <div>
            <h2 className="text-2xl font-bold text-white flex items-center space-x-2">
              <Atom className="w-6 h-6 text-purple-400" />
              <span>Guided Gravitational Simulations</span>
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Pre-configured numerical physics scenarios with educational questions to explore in the N-Body Lab.
            </p>
          </div>
          <Link to="/simulation" className="text-xs text-purple-400 hover:text-purple-300 font-mono flex items-center space-x-1">
            <span>Open Full Simulation Lab</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[
            {
              title: "Why Doesn't the Moon Fly Away?",
              scenario: 'earth_moon_sun',
              desc: 'Discover how the Moon stays trapped inside Earth’s Hill sphere despite the Sun pulling on it with twice as much gravitational force!',
              physicsQuestion: 'Hill Sphere & Tidal Stability'
            },
            {
              title: 'The Great Planetary Race',
              scenario: 'solar_system_inner',
              desc: 'Watch Mercury, Venus, Earth, and Mars orbit together. Notice how orbital speed strictly drops as distance increases.',
              physicsQuestion: "Kepler's 3rd Law in Action"
            },
            {
              title: 'The Resonant 7-World Chain',
              scenario: 'trappist_1_resonance',
              desc: 'See 7 Earth-sized worlds orbit an ultra-cool dwarf star in musical Laplace integer resonances (24:15:9:6:4:3:2).',
              physicsQuestion: 'Orbital Commensurability'
            },
            {
              title: 'The Figure-8 Choreography',
              scenario: 'figure_eight_choreography',
              desc: 'Observe three equal-mass stars chasing each other indefinitely along a single figure-8 curve with zero angular momentum.',
              physicsQuestion: 'Periodic 3-Body Solution'
            }
          ].map((sim, i) => (
            <div key={i} className="p-5 rounded-2xl glass-panel border border-white/10 hover:border-purple-400/40 transition-all flex flex-col justify-between space-y-3">
              <div>
                <span className="text-[10px] font-mono text-purple-400 uppercase tracking-widest">{sim.physicsQuestion}</span>
                <h4 className="text-sm font-bold text-white mt-1">{sim.title}</h4>
                <p className="text-xs text-slate-300 mt-2 leading-relaxed">{sim.desc}</p>
              </div>
              <Link
                to={`/simulation`}
                className="inline-flex items-center space-x-1.5 text-xs text-purple-400 hover:text-purple-300 font-semibold pt-2"
              >
                <span>Launch Simulation</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          ))}
        </div>
      </div>

      {/* KEPLER'S LAWS SANDBOX */}
      <div id="kepler-sandbox" className="p-6 sm:p-8 rounded-3xl glass-panel border border-amber-500/20 space-y-6">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2 text-amber-400">
              <Sliders className="w-5 h-5" />
              <h3 className="text-lg font-bold text-white">Interactive Kepler's Laws Sandbox</h3>
            </div>
            <p className="text-xs text-slate-300 mt-1">
              Adjust semi-major axis (a) and orbital eccentricity (e) to see how orbit shape dictates period and speedup!
            </p>
          </div>
          <span className="px-3 py-1 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-300 text-xs font-mono">
            Keplerian Mechanics Solver
          </span>
        </div>

        {/* Controls */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 p-4 rounded-2xl bg-space-900 border border-white/5">
          <div className="space-y-2">
            <div className="flex justify-between text-xs">
              <span className="text-slate-300">Semi-Major Axis (a):</span>
              <span className="font-mono text-amber-400 font-bold">{keplerA.toFixed(2)} AU</span>
            </div>
            <input
              type="range"
              min="0.2"
              max="5.0"
              step="0.05"
              value={keplerA}
              onChange={(e) => setKeplerA(parseFloat(e.target.value))}
              className="w-full accent-amber-500"
            />
            <span className="text-[10px] text-slate-400">1 AU = Earth's distance to Sun (149.6 million km)</span>
          </div>

          <div className="space-y-2">
            <div className="flex justify-between text-xs">
              <span className="text-slate-300">Eccentricity (e):</span>
              <span className="font-mono text-amber-400 font-bold">{keplerE.toFixed(2)}</span>
            </div>
            <input
              type="range"
              min="0.0"
              max="0.85"
              step="0.01"
              value={keplerE}
              onChange={(e) => setKeplerE(parseFloat(e.target.value))}
              className="w-full accent-amber-500"
            />
            <span className="text-[10px] text-slate-400">0.0 = Perfect Circle • 0.85 = Highly Stretched Ellipse (Comet-like)</span>
          </div>
        </div>

        {/* Live Mathematical Physics Output */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="p-4 rounded-xl glass-panel border border-white/10 text-center space-y-1">
            <span className="text-[11px] text-slate-400">Orbital Period (T)</span>
            <span className="text-xl font-bold font-mono text-amber-400 block">{periodYears.toFixed(2)} yrs</span>
            <span className="text-[10px] text-slate-400 block">{(periodYears * 365.25).toFixed(0)} Earth days</span>
          </div>

          <div className="p-4 rounded-xl glass-panel border border-white/10 text-center space-y-1">
            <span className="text-[11px] text-slate-400">Closest Approach (rp)</span>
            <span className="text-xl font-bold font-mono text-emerald-400 block">{perihelion.toFixed(2)} AU</span>
            <span className="text-[10px] text-slate-400 block">Perihelion = a(1 - e)</span>
          </div>

          <div className="p-4 rounded-xl glass-panel border border-white/10 text-center space-y-1">
            <span className="text-[11px] text-slate-400">Farthest Point (ra)</span>
            <span className="text-xl font-bold font-mono text-sky-400 block">{aphelion.toFixed(2)} AU</span>
            <span className="text-[10px] text-slate-400 block">Aphelion = a(1 + e)</span>
          </div>

          <div className="p-4 rounded-xl glass-panel border border-white/10 text-center space-y-1">
            <span className="text-[11px] text-slate-400">Speed Ratio (vp / va)</span>
            <span className="text-xl font-bold font-mono text-purple-400 block">
              {(speedAtPerihelion / speedAtAphelion).toFixed(2)}x
            </span>
            <span className="text-[10px] text-slate-400 block">Kepler's 2nd Law Speedup</span>
          </div>
        </div>
      </div>

      {/* COMPREHENSION CHECK QUIZ */}
      <div className="p-6 sm:p-8 rounded-3xl glass-panel border border-white/10 space-y-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Award className="w-5 h-5 text-amber-400" />
            <h3 className="text-lg font-bold text-white">Physics Comprehension Quiz</h3>
          </div>
          <span className="text-xs font-mono text-slate-300">
            Score: <strong className="text-amber-400 font-bold">{score}</strong> / {quizQuestions.length}
          </span>
        </div>

        <div className="p-5 rounded-2xl bg-space-900 border border-white/5 space-y-4">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>Question {currentQIndex + 1} of {quizQuestions.length}</span>
          </div>

          <h4 className="text-base font-semibold text-white">{quizQuestions[currentQIndex].question}</h4>

          <div className="space-y-2 pt-2">
            {quizQuestions[currentQIndex].options.map((opt, i) => {
              const isSelected = selectedOption === i;
              const isCorrect = i === quizQuestions[currentQIndex].correctIndex;

              let btnStyle = 'bg-white/5 hover:bg-white/10 text-slate-200 border-white/10';
              if (showExplanation) {
                if (isCorrect) btnStyle = 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40';
                else if (isSelected) btnStyle = 'bg-rose-500/20 text-rose-300 border-rose-500/40';
              }

              return (
                <button
                  key={i}
                  disabled={showExplanation}
                  onClick={() => handleAnswer(i)}
                  className={`w-full p-3 rounded-xl border text-left text-xs transition-all flex items-center justify-between ${btnStyle}`}
                >
                  <span>{opt}</span>
                  {showExplanation && isCorrect && <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />}
                  {showExplanation && isSelected && !isCorrect && <XCircle className="w-4 h-4 text-rose-400 flex-shrink-0" />}
                </button>
              );
            })}
          </div>

          {showExplanation && (
            <div className="mt-4 p-4 rounded-xl bg-amber-500/10 border border-amber-500/20 space-y-3">
              <p className="text-xs text-amber-200 leading-relaxed">
                💡 <strong>Physics Explanation:</strong> {quizQuestions[currentQIndex].explanation}
              </p>
              <button
                onClick={nextQuestion}
                className="px-4 py-2 rounded-lg bg-amber-500 hover:bg-amber-400 text-space-950 font-bold text-xs transition-all"
              >
                Next Question
              </button>
            </div>
          )}
        </div>
      </div>

      {/* SOCRATIC AI TUTOR */}
      <div id="ai-tutor" className="p-6 rounded-3xl glass-panel border border-amber-500/20 space-y-4">
        <div className="flex items-center space-x-2">
          <Sparkles className="w-5 h-5 text-amber-400" />
          <h3 className="text-lg font-bold text-white">Socratic AI Physics Tutor</h3>
        </div>
        <p className="text-xs text-slate-300">
          Ask questions about orbital mechanics, Kepler's laws, or planetary physics. The AI tutor provides step-by-step
          reasoning with comprehension prompts!
        </p>

        <div className="flex flex-wrap gap-2 text-xs">
          {[
            'Why do all planets orbit in nearly the same flat plane?',
            'How does a gravitational slingshot work without violating energy conservation?',
            'What is the difference between mass and weight on Jupiter?',
            'Explain tidal locking using Earth and the Moon.'
          ].map((q, i) => (
            <button
              key={i}
              onClick={() => askTutor(q)}
              className="px-3 py-1 rounded-lg bg-white/5 hover:bg-white/10 text-slate-300 border border-white/5 transition-all text-left"
            >
              {q}
            </button>
          ))}
        </div>

        <div className="flex gap-2 pt-2">
          <input
            type="text"
            value={tutorPrompt}
            onChange={(e) => setTutorPrompt(e.target.value)}
            placeholder="Ask your physics question here..."
            className="flex-1 bg-space-900 border border-white/10 rounded-xl px-4 py-2.5 text-xs text-white focus:outline-none focus:border-amber-500"
          />
          <button
            onClick={() => askTutor(tutorPrompt)}
            disabled={tutorLoading || !tutorPrompt.trim()}
            className="px-5 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-space-950 font-bold text-xs flex items-center space-x-1.5 transition-all disabled:opacity-50"
          >
            <Send className="w-3.5 h-3.5" />
            <span>{tutorLoading ? 'Solving...' : 'Ask Tutor'}</span>
          </button>
        </div>

        {tutorResponse && (
          <div className="mt-4 p-5 rounded-2xl bg-space-900/90 border border-amber-500/20 text-xs text-slate-200 leading-relaxed whitespace-pre-wrap">
            {tutorResponse}
          </div>
        )}
      </div>
    </div>
  );
};
