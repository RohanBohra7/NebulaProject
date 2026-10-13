import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { fetchObjects, chatAI } from '../services/api';
import { AstronomicalObject } from '../types/astronomy';
import { Object3DViewer } from '../components/visualization/Object3DViewer';
import {
  Sparkles,
  Compass,
  Orbit,
  Send,
  Lightbulb,
  Moon,
  Star,
  ArrowRight,
  Shuffle,
  Weight,
  Clock,
  Heart,
  Thermometer,
  Layers,
  HelpCircle,
  Eye,
  GitCompare
} from 'lucide-react';

export const CitizenDashboard: React.FC = () => {
  const navigate = useNavigate();
  const [objects, setObjects] = useState<AstronomicalObject[]>([]);
  const [featuredObject, setFeaturedObject] = useState<AstronomicalObject | null>(null);
  const [triviaIndex, setTriviaIndex] = useState(0);

  // "Discover Something Interesting" State
  const [curiosityItem, setCuriosityItem] = useState<{
    title: string;
    description: string;
    objectId: string;
    tag: string;
  } | null>(null);

  // Quick AI Assistant state
  const [aiPrompt, setAiPrompt] = useState('');
  const [aiResponse, setAiResponse] = useState<string | null>(null);
  const [aiLoading, setAiLoading] = useState(false);

  // Human scale comparison weight state (default 70 kg)
  const [userWeightKg, setUserWeightKg] = useState(70);

  const triviaFacts = [
    'One day on Venus is longer than one entire Venusian year! It rotates so slowly that a single day lasts 243 Earth days.',
    'A full NASA spacesuit costs roughly $12 million, with 70% of that cost being the life support backpack and helmet module.',
    'Neutron stars are so dense that a single sugar-cube-sized chunk of their material would weigh about 1 billion tons on Earth!',
    'The footprints left by Apollo astronauts on the Moon will stay there for at least 100 million years because the Moon has no wind or water erosion.',
    'Jupiter is so massive that it actually orbits a common center of gravity with the Sun that lies just outside the Sun’s physical surface!'
  ];

  const cosmicCuriosities = [
    {
      title: 'Diamond Rain on Neptune and Uranus',
      description:
        'Deep beneath the cloud tops of Neptune and Uranus, temperatures and pressures are so extreme that carbon atoms are crushed into literal solid diamonds that hail down toward the planets’ rocky cores!',
      objectId: 'neptune',
      tag: 'Extreme Weather'
    },
    {
      title: 'A Subsurface Saltwater Ocean on Europa',
      description:
        'Jupiter’s icy moon Europa hides a global ocean beneath a 20 km crust of ice containing more liquid water than all of Earth’s oceans combined. NASA considers it one of our best chances of finding alien microbial life.',
      objectId: 'europa',
      tag: 'Alien Oceans'
    },
    {
      title: 'The Great Red Spot: A Storm Larger than Earth',
      description:
        'Jupiter’s Great Red Spot is a colossal anticyclonic hurricane that has been raging for over 350 years. At its peak, three entire Earths could have fit inside it side-by-side!',
      objectId: 'jupiter',
      tag: 'Monster Storms'
    },
    {
      title: 'TRAPPIST-1e: An Earth-Sized Habitable World',
      description:
        'Located 40 light-years away, TRAPPIST-1e receives almost the exact same amount of stellar warmth that Earth receives from the Sun, making liquid oceans and temperate weather theoretically possible.',
      objectId: 'trappist-1e',
      tag: 'Habitable Worlds'
    },
    {
      title: 'Saturn’s Ring Material is Thin as a House Sheet',
      description:
        'Saturn’s magnificent rings span over 280,000 kilometers in width—almost the distance from Earth to the Moon—yet they are only about 10 to 30 meters thick on average!',
      objectId: 'saturn',
      tag: 'Planetary Rings'
    }
  ];

  useEffect(() => {
    fetchObjects().then((data) => {
      setObjects(data);
      const saturn = data.find((o) => o.id === 'saturn') || data[0];
      setFeaturedObject(saturn);
      setCuriosityItem(cosmicCuriosities[0]);
    });
  }, []);

  const handleRandomCuriosity = () => {
    const nextIdx = Math.floor(Math.random() * cosmicCuriosities.length);
    setCuriosityItem(cosmicCuriosities[nextIdx]);
  };

  const handleQuickAsk = async (promptText: string) => {
    setAiLoading(true);
    setAiPrompt(promptText);
    try {
      const res = await chatAI(promptText, 'citizen', featuredObject?.id);
      setAiResponse(res.response);
    } catch {
      setAiResponse('Unable to retrieve an answer right now. Please check your connection.');
    } finally {
      setAiLoading(false);
    }
  };

  const handleCustomSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!aiPrompt.trim()) return;
    handleQuickAsk(aiPrompt);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-12">
      {/* Citizen Welcome Banner */}
      <div className="p-8 rounded-3xl glass-panel-glow border border-purple-500/20 relative overflow-hidden flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="space-y-3 max-w-2xl">
          <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-purple-500/10 text-purple-300 border border-purple-400/20 text-xs font-mono">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Citizen Experience • Cosmic Wonder & Night Sky Exploration</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white">
            Welcome to the Cosmic Backyard
          </h1>
          <p className="text-sm text-slate-300 leading-relaxed">
            Discover the beauty of our planetary neighbors and distant stars through plain-language stories, striking 3D
            views, relatable everyday analogies, and fascinating cosmic trivia.
          </p>
          <div className="flex flex-wrap items-center gap-3 pt-2">
            <Link
              to="/visualization"
              className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-medium text-xs flex items-center space-x-1.5 shadow-md shadow-purple-600/20 transition-all"
            >
              <Orbit className="w-4 h-4" />
              <span>Launch 3D Planetarium</span>
            </Link>
            <Link
              to="/explorer"
              className="px-4 py-2 rounded-xl bg-white/10 hover:bg-white/20 text-slate-200 text-xs font-medium flex items-center space-x-1.5 transition-all"
            >
              <Compass className="w-4 h-4 text-sky-400" />
              <span>Discover All 23 Worlds</span>
            </Link>
            <Link
              to="/compare"
              className="px-4 py-2 rounded-xl bg-white/10 hover:bg-white/20 text-slate-200 text-xs font-medium flex items-center space-x-1.5 transition-all"
            >
              <GitCompare className="w-4 h-4 text-emerald-400" />
              <span>Side-by-Side Compare</span>
            </Link>
          </div>
        </div>

        {/* Trivia Callout Card */}
        <div className="w-full md:w-80 p-5 rounded-2xl bg-space-900 border border-purple-500/20 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-purple-300 flex items-center space-x-1">
              <Lightbulb className="w-3.5 h-3.5 text-amber-400" />
              <span>Did You Know?</span>
            </span>
            <button
              onClick={() => setTriviaIndex((prev) => (prev + 1) % triviaFacts.length)}
              className="text-[11px] text-slate-400 hover:text-white underline font-mono"
            >
              Next Fact
            </button>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed italic">"{triviaFacts[triviaIndex]}"</p>
        </div>
      </div>

      {/* DISCOVER SOMETHING INTERESTING ("Surprise Me" Curiosity Generator) */}
      <div className="p-6 sm:p-8 rounded-3xl glass-panel border border-purple-500/30 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-white/10 pb-4">
          <div className="flex items-center space-x-3">
            <div className="p-2.5 rounded-2xl bg-purple-500/20 text-purple-300 border border-purple-500/30">
              <Sparkles className="w-5 h-5 text-purple-400" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-white">Discover Something Interesting</h3>
              <p className="text-xs text-slate-400">Hand-curated cosmic phenomena explained in plain language.</p>
            </div>
          </div>
          <button
            onClick={handleRandomCuriosity}
            className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-semibold text-xs flex items-center space-x-2 transition-all shadow-md shadow-purple-600/20"
          >
            <Shuffle className="w-3.5 h-3.5" />
            <span>Surprise Me With Another Discovery!</span>
          </button>
        </div>

        {curiosityItem && (
          <div className="p-5 rounded-2xl bg-space-900 border border-white/5 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
            <div className="space-y-2 max-w-3xl">
              <div className="flex items-center space-x-2">
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/30 uppercase tracking-widest">
                  {curiosityItem.tag}
                </span>
                <span className="text-xs text-slate-400 font-mono">Curated Phenomenon</span>
              </div>
              <h4 className="text-xl font-bold text-white">{curiosityItem.title}</h4>
              <p className="text-sm text-slate-200 leading-relaxed font-sans">{curiosityItem.description}</p>
            </div>

            <Link
              to={`/object/${curiosityItem.objectId}`}
              className="px-4 py-2.5 rounded-xl bg-sky-500 hover:bg-sky-400 text-white font-semibold text-xs flex items-center space-x-1.5 transition-all flex-shrink-0"
            >
              <span>Explore This World</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        )}
      </div>

      {/* FEATURED WORLD SPOTLIGHT (With 3D Viewer) */}
      {featuredObject && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center p-6 sm:p-8 rounded-3xl glass-panel border border-white/10">
          <div className="lg:col-span-5 flex flex-col items-center">
            <Object3DViewer object={featuredObject} size={320} />
            <div className="flex items-center space-x-2 mt-2">
              {objects.slice(0, 5).map((o) => (
                <button
                  key={o.id}
                  onClick={() => setFeaturedObject(o)}
                  className={`w-6 h-6 rounded-full border-2 transition-all ${
                    featuredObject.id === o.id ? 'border-purple-400 scale-110 shadow-lg' : 'border-transparent opacity-60 hover:opacity-100'
                  }`}
                  style={{ backgroundColor: o.color_hex || '#38bdf8' }}
                  title={`Switch Spotlight to ${o.name}`}
                />
              ))}
            </div>
          </div>

          <div className="lg:col-span-7 space-y-5">
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-xs px-2.5 py-0.5 rounded-full bg-purple-500/20 border border-purple-400/30 text-purple-300 font-mono">
                  World Spotlight
                </span>
                <span className="text-xs text-slate-400 font-mono">{featuredObject.category}</span>
              </div>
              <h2 className="text-3xl font-extrabold text-white mt-1">{featuredObject.name}</h2>
            </div>

            <p className="text-sm text-slate-300 leading-relaxed font-sans">
              {featuredObject.description_citizen || featuredObject.description_student || ''}
            </p>

            {/* Plain-Language Everyday Comparisons */}
            <div className="grid grid-cols-3 gap-3">
              <div className="p-3.5 rounded-2xl bg-space-900 border border-white/5 space-y-1">
                <span className="text-[10px] text-slate-400 block font-medium flex items-center space-x-1">
                  <Weight className="w-3 h-3 text-sky-400" />
                  <span>How Heavy?</span>
                </span>
                <span className="text-sm font-bold text-white font-mono block">
                  {featuredObject.mass_earth_relative
                    ? `${featuredObject.mass_earth_relative}x Earth`
                    : 'Gigantic'}
                </span>
                <span className="text-[10px] text-slate-400 block">Relative Mass</span>
              </div>

              <div className="p-3.5 rounded-2xl bg-space-900 border border-white/5 space-y-1">
                <span className="text-[10px] text-slate-400 block font-medium flex items-center space-x-1">
                  <Thermometer className="w-3 h-3 text-rose-400" />
                  <span>Temperature</span>
                </span>
                <span className="text-sm font-bold text-white font-mono block">
                  {featuredObject.surface_temperature_k
                    ? `${Math.round(featuredObject.surface_temperature_k - 273.15)}°C`
                    : 'Variable'}
                </span>
                <span className="text-[10px] text-slate-400 block">Average Surface</span>
              </div>

              <div className="p-3.5 rounded-2xl bg-space-900 border border-white/5 space-y-1">
                <span className="text-[10px] text-slate-400 block font-medium flex items-center space-x-1">
                  <Clock className="w-3 h-3 text-amber-400" />
                  <span>One Year Lasts</span>
                </span>
                <span className="text-sm font-bold text-white font-mono block">
                  {featuredObject.orbital_period_days
                    ? `${Math.round(featuredObject.orbital_period_days)} days`
                    : 'N/A'}
                </span>
                <span className="text-[10px] text-slate-400 block">Earth Day Equivalent</span>
              </div>
            </div>

            <div className="flex flex-wrap items-center gap-3 pt-2">
              <Link
                to={`/object/${featuredObject.id}`}
                className="px-4 py-2 rounded-xl bg-sky-500 hover:bg-sky-400 text-white font-medium text-xs flex items-center space-x-1.5 transition-all shadow-md shadow-sky-500/20"
              >
                <span>View Complete Profile</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
              <button
                onClick={() => handleQuickAsk(`What is the most surprising fact about ${featuredObject.name}?`)}
                className="px-4 py-2 rounded-xl bg-white/10 hover:bg-white/20 text-slate-200 text-xs font-medium flex items-center space-x-1.5 transition-all"
              >
                <Sparkles className="w-3.5 h-3.5 text-purple-400" />
                <span>Ask AI About {featuredObject.name}</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* SOLAR SYSTEM EXPLORATION & DISCOVERY HIGHLIGHTS */}
      <div className="space-y-4">
        <div className="flex items-center justify-between border-b border-white/10 pb-4">
          <div>
            <h2 className="text-2xl font-bold text-white flex items-center space-x-2">
              <Compass className="w-6 h-6 text-sky-400" />
              <span>Solar System Guided Highlights</span>
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">Click any world to spotlight it in the interactive 3D viewer.</p>
          </div>
          <Link to="/explorer" className="text-xs text-sky-400 hover:text-sky-300 font-mono flex items-center space-x-1">
            <span>Explore Entire 23-Body Catalog</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {objects.slice(0, 6).map((obj) => (
            <div
              key={obj.id}
              onClick={() => setFeaturedObject(obj)}
              className={`p-5 rounded-2xl glass-panel border cursor-pointer transition-all space-y-3 ${
                featuredObject?.id === obj.id
                  ? 'border-purple-500/60 shadow-lg shadow-purple-500/10 ring-1 ring-purple-400/30'
                  : 'border-white/10 hover:border-white/25'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono text-purple-400">{obj.category}</span>
                <span className="w-3 h-3 rounded-full" style={{ backgroundColor: obj.color_hex || '#38bdf8' }} />
              </div>
              <h4 className="text-base font-bold text-white">{obj.name}</h4>
              <p className="text-xs text-slate-300 line-clamp-3 leading-relaxed">
                {obj.description_citizen || obj.description_student || ''}
              </p>
              <div className="pt-2 flex items-center justify-between text-xs font-mono text-slate-400 border-t border-white/5">
                <span>Gravity: {obj.surface_gravity_m_s2 ? `${obj.surface_gravity_m_s2} m/s²` : '—'}</span>
                <span className="text-sky-400 flex items-center space-x-1 hover:underline">
                  <span>Spotlight</span>
                  <Eye className="w-3 h-3" />
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* SIMPLE COMPARISON: "HOW MUCH WOULD YOU WEIGH HERE?" */}
      <div className="p-6 sm:p-8 rounded-3xl glass-panel border border-white/10 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-white/10 pb-4">
          <div>
            <div className="flex items-center space-x-2 text-emerald-400">
              <Weight className="w-5 h-5" />
              <h3 className="text-lg font-bold text-white">Everyday Human Comparison: What Would You Weigh?</h3>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Enter your weight on Earth to see how gravity alters your scale reading across other worlds!
            </p>
          </div>

          <div className="flex items-center space-x-3 bg-space-900 border border-white/10 px-3 py-1.5 rounded-2xl">
            <span className="text-xs text-slate-300 font-medium">Your Weight on Earth:</span>
            <input
              type="number"
              min={20}
              max={300}
              value={userWeightKg}
              onChange={(e) => setUserWeightKg(Math.max(1, parseInt(e.target.value, 10) || 70))}
              className="w-16 bg-space-950 border border-white/20 rounded-lg px-2 py-1 text-xs text-white font-mono text-center"
            />
            <span className="text-xs text-slate-400 font-mono">kg</span>
          </div>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-3 text-center">
          {[
            { name: 'Moon', gRel: 0.165, color: '#cbd5e1' },
            { name: 'Mars', gRel: 0.379, color: '#ef4444' },
            { name: 'Venus', gRel: 0.905, color: '#eab308' },
            { name: 'Earth', gRel: 1.0, color: '#38bdf8' },
            { name: 'Jupiter', gRel: 2.528, color: '#d97706' },
            { name: 'Sun', gRel: 27.9, color: '#f59e0b' }
          ].map((w) => {
            const planetWeight = Math.round(userWeightKg * w.gRel);
            return (
              <div key={w.name} className="p-4 rounded-2xl bg-space-900 border border-white/5 space-y-1">
                <span className="w-2.5 h-2.5 rounded-full inline-block" style={{ backgroundColor: w.color }} />
                <span className="text-xs font-semibold text-white block">{w.name}</span>
                <span className="text-lg font-extrabold text-emerald-400 font-mono block">{planetWeight} kg</span>
                <span className="text-[10px] text-slate-400 block font-mono">({w.gRel}x Earth gravity)</span>
              </div>
            );
          })}
        </div>
      </div>

      {/* QUICK AI ASTRONOMY ASSISTANT (Plain Language) */}
      <div className="p-6 sm:p-8 rounded-3xl glass-panel border border-purple-500/30 space-y-4">
        <div className="flex items-center space-x-2">
          <Sparkles className="w-5 h-5 text-purple-400" />
          <h3 className="text-lg font-bold text-white">Ask the Citizen Astronomy Assistant</h3>
        </div>
        <p className="text-xs text-slate-300">
          Got a curiosity about the cosmos? Ask in plain language, and get wonder-filled, easy-to-understand explanations!
        </p>

        {/* Prompt suggestions */}
        <div className="flex flex-wrap gap-2 text-xs">
          {[
            'Why is Mars called the Red Planet?',
            'What would it feel like to stand on Titan?',
            'How long would it take to travel to the nearest star?',
            'Why do planets have rings?'
          ].map((prompt, i) => (
            <button
              key={i}
              onClick={() => handleQuickAsk(prompt)}
              className="px-3 py-1 rounded-lg bg-white/5 hover:bg-white/10 text-slate-300 border border-white/5 transition-all text-left"
            >
              {prompt}
            </button>
          ))}
        </div>

        <form onSubmit={handleCustomSubmit} className="flex gap-2 pt-2">
          <input
            type="text"
            value={aiPrompt}
            onChange={(e) => setAiPrompt(e.target.value)}
            placeholder="Ask anything about planets, stars, or the cosmos in plain English..."
            className="flex-1 bg-space-900 border border-white/10 rounded-xl px-4 py-2.5 text-xs text-white focus:outline-none focus:border-purple-500"
          />
          <button
            type="submit"
            disabled={aiLoading}
            className="px-5 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-semibold text-xs flex items-center space-x-1.5 transition-all disabled:opacity-50"
          >
            <Send className="w-3.5 h-3.5" />
            <span>{aiLoading ? 'Thinking...' : 'Ask'}</span>
          </button>
        </form>

        {aiResponse && (
          <div className="mt-4 p-5 rounded-2xl bg-space-900/90 border border-purple-500/20 text-xs text-slate-200 leading-relaxed font-sans whitespace-pre-wrap">
            {aiResponse}
          </div>
        )}
      </div>
    </div>
  );
};
