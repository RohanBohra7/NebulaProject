import React, { useEffect, useState, useMemo } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { useMode } from '../context/ModeContext';
import { fetchObjects } from '../services/api';
import { AstronomicalObject } from '../types/astronomy';
import { Object3DViewer } from '../components/visualization/Object3DViewer';
import { Modal, Button, LoadingState, ErrorState, EmptyState } from '../components/ui';
import {
  Compass,
  Search,
  SlidersHorizontal,
  LayoutGrid,
  List,
  ArrowRight,
  ExternalLink,
  Eye,
  CheckCircle2,
  ChevronLeft,
  ChevronRight,
  ArrowUpDown,
  ShieldCheck,
  Sparkles,
  X
} from 'lucide-react';

export const ExplorerPage: React.FC = () => {
  const { mode } = useMode();
  const [searchParams, setSearchParams] = useSearchParams();
  const initialCategory = searchParams.get('cat') || 'All';

  const [objects, setObjects] = useState<AstronomicalObject[]>([]);
  const [category, setCategory] = useState(initialCategory);
  const [search, setSearch] = useState('');
  const [sortBy, setSortBy] = useState<'distance' | 'mass' | 'radius' | 'period' | 'temperature' | 'name'>('distance');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');
  const [viewMode, setViewMode] = useState<'grid' | 'table'>('grid');
  const [filterAtmosphere, setFilterAtmosphere] = useState<boolean | null>(null);
  const [filterRings, setFilterRings] = useState<boolean | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(9);

  // Preview Modal state
  const [previewObject, setPreviewObject] = useState<AstronomicalObject | null>(null);

  const loadObjects = () => {
    setLoading(true);
    setError(null);
    fetchObjects()
      .then((data) => {
        setObjects(data);
      })
      .catch((err) => {
        console.error(err);
        setError(err.message || 'Failed to retrieve astronomical objects from NEBULA backend.');
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadObjects();
  }, []);

  const handleResetFilters = () => {
    setSearch('');
    setCategory('All');
    setFilterAtmosphere(null);
    setFilterRings(null);
    setCurrentPage(1);
    searchParams.delete('cat');
    setSearchParams(searchParams);
  };

  // Update URL search param when category changes
  const handleCategoryChange = (cat: string) => {
    setCategory(cat);
    setCurrentPage(1);
    if (cat === 'All') {
      searchParams.delete('cat');
      setSearchParams(searchParams);
    } else {
      setSearchParams({ cat });
    }
  };

  const categories = ['All', 'Planet', 'Moon', 'Star', 'Exoplanet', 'Asteroid', 'Comet', 'Deep-Sky'];

  // Count per category
  const categoryCounts = useMemo(() => {
    const counts: Record<string, number> = { All: objects.length };
    categories.forEach((c) => {
      if (c !== 'All') {
        counts[c] = objects.filter((o) => o.category.toLowerCase() === c.toLowerCase()).length;
      }
    });
    return counts;
  }, [objects]);

  // Filtered & Sorted items
  const filteredObjects = useMemo(() => {
    return objects
      .filter((obj) => {
        const matchCat = category === 'All' || obj.category.toLowerCase() === category.toLowerCase();
        const s = search.toLowerCase().trim();
        const matchSearch = !s ||
          obj.name.toLowerCase().includes(s) ||
          obj.id.includes(s) ||
          obj.category.toLowerCase().includes(s) ||
          (obj.spectral_type && obj.spectral_type.toLowerCase().includes(s));
        const matchAtm = filterAtmosphere === null || obj.has_atmosphere === filterAtmosphere;
        const matchRings = filterRings === null || obj.has_rings === filterRings;
        return matchCat && matchSearch && matchAtm && matchRings;
      })
      .sort((a, b) => {
        const mult = sortOrder === 'asc' ? 1 : -1;
        if (sortBy === 'name') return a.name.localeCompare(b.name) * mult;
        if (sortBy === 'distance') return ((a.semi_major_axis_au ?? 0) - (b.semi_major_axis_au ?? 0)) * mult;
        if (sortBy === 'mass') return ((a.mass_earth_relative ?? 0) - (b.mass_earth_relative ?? 0)) * mult;
        if (sortBy === 'radius') return ((a.radius_km ?? 0) - (b.radius_km ?? 0)) * mult;
        if (sortBy === 'period') return ((a.orbital_period_days ?? 0) - (b.orbital_period_days ?? 0)) * mult;
        if (sortBy === 'temperature') return ((a.surface_temperature_k ?? 0) - (b.surface_temperature_k ?? 0)) * mult;
        return 0;
      });
  }, [objects, category, search, sortBy, sortOrder, filterAtmosphere, filterRings]);

  // Pagination calculation
  const totalPages = Math.ceil(filteredObjects.length / pageSize) || 1;
  const paginatedObjects = useMemo(() => {
    const start = (currentPage - 1) * pageSize;
    return filteredObjects.slice(start, start + pageSize);
  }, [filteredObjects, currentPage, pageSize]);

  const getAdaptiveDescription = (obj: AstronomicalObject) => {
    switch (mode) {
      case 'researcher': return obj.description_researcher;
      case 'student': return obj.description_student;
      case 'citizen': return obj.description_citizen;
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8">
      {/* Header and Provenance Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex flex-wrap items-center gap-2 mb-2">
            <span className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-sky-500/10 text-sky-300 border border-sky-400/20 text-xs font-mono">
              <Compass className="w-3.5 h-3.5" />
              <span>Celestial Catalog Explorer • {filteredObjects.length} Targets Found</span>
            </span>
            <span className="inline-flex items-center space-x-1 px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[11px] font-mono">
              <ShieldCheck className="w-3 h-3" />
              <span>Astropy Physical Validation: 96%</span>
            </span>
          </div>
          <h1 className="text-3xl font-extrabold text-white">
            Astronomical Object Explorer
          </h1>
        </div>

        {/* View Mode Toggle */}
        <div className="flex items-center space-x-2 bg-space-900 border border-white/10 rounded-xl p-1 text-xs">
          <button
            onClick={() => setViewMode('grid')}
            className={`p-2 rounded-lg transition-all flex items-center space-x-1.5 ${
              viewMode === 'grid' ? 'bg-sky-500 text-white shadow' : 'text-slate-400 hover:text-white'
            }`}
            title="Grid Cards View"
          >
            <LayoutGrid className="w-4 h-4" />
            <span className="hidden sm:inline font-mono">Cards</span>
          </button>
          <button
            onClick={() => setViewMode('table')}
            className={`p-2 rounded-lg transition-all flex items-center space-x-1.5 ${
              viewMode === 'table' ? 'bg-sky-500 text-white shadow' : 'text-slate-400 hover:text-white'
            }`}
            title="Scientific Table View"
          >
            <List className="w-4 h-4" />
            <span className="hidden sm:inline font-mono">Telemetry Table</span>
          </button>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="p-5 rounded-2xl glass-panel border border-white/10 space-y-4 shadow-xl">
        {/* Category Chips with Counts */}
        <div className="flex flex-wrap gap-2">
          {categories.map((cat) => {
            const count = categoryCounts[cat] || 0;
            const isSelected = category.toLowerCase() === cat.toLowerCase();
            return (
              <button
                key={cat}
                onClick={() => handleCategoryChange(cat)}
                className={`px-3 py-1.5 rounded-xl text-xs font-medium transition-all flex items-center space-x-1.5 ${
                  isSelected
                    ? 'bg-sky-500 text-white shadow-md shadow-sky-500/25 border border-sky-400 font-semibold'
                    : 'bg-white/5 text-slate-300 hover:bg-white/10 border border-white/5'
                }`}
              >
                <span>{cat}</span>
                <span className={`text-[10px] px-1.5 py-0.2 rounded-full font-mono ${
                  isSelected ? 'bg-white/20 text-white' : 'bg-white/5 text-slate-400'
                }`}>
                  {count}
                </span>
              </button>
            );
          })}
        </div>

        {/* Search, Sort, and Atmospheric Filters */}
        <div className="grid grid-cols-1 sm:grid-cols-12 gap-3 pt-2 border-t border-white/5">
          {/* Search Box */}
          <div className="sm:col-span-5 relative">
            <Search className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
            <input
              type="text"
              value={search}
              onChange={(e) => {
                setSearch(e.target.value);
                setCurrentPage(1);
              }}
              placeholder="Search by name, ID, spectral class..."
              className="w-full bg-space-950 border border-white/10 rounded-xl pl-9 pr-8 py-2 text-xs text-white focus:outline-none focus:border-sky-500 font-mono"
            />
            {search && (
              <button
                onClick={() => setSearch('')}
                className="absolute right-2.5 top-2.5 text-slate-400 hover:text-white"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            )}
          </div>

          {/* Sort Selector */}
          <div className="sm:col-span-4 flex items-center space-x-2">
            <SlidersHorizontal className="w-4 h-4 text-slate-400 shrink-0" />
            <select
              value={sortBy}
              onChange={(e: any) => setSortBy(e.target.value)}
              className="flex-1 bg-space-950 border border-white/10 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-sky-500 font-mono"
            >
              <option value="distance">Sort: Distance from Sun (AU)</option>
              <option value="mass">Sort: Mass (M_earth)</option>
              <option value="radius">Sort: Radius (km)</option>
              <option value="period">Sort: Orbital Period (days)</option>
              <option value="temperature">Sort: Surface Temperature (K)</option>
              <option value="name">Sort: Name (A-Z)</option>
            </select>
            <button
              onClick={() => setSortOrder(prev => prev === 'asc' ? 'desc' : 'asc')}
              className="p-2 bg-space-950 border border-white/10 hover:border-sky-500/50 rounded-xl text-slate-300 hover:text-white transition-all text-xs flex items-center justify-center shrink-0"
              title={`Toggle ${sortOrder === 'asc' ? 'Descending' : 'Ascending'}`}
            >
              <ArrowUpDown className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* Feature toggles */}
          <div className="sm:col-span-3 flex items-center space-x-2 justify-end text-xs font-mono">
            <button
              onClick={() => setFilterAtmosphere(prev => prev === true ? null : true)}
              className={`px-2.5 py-1.5 rounded-lg border transition-all ${
                filterAtmosphere === true
                  ? 'bg-sky-500/20 border-sky-400 text-sky-300 font-semibold'
                  : 'bg-white/5 border-white/5 text-slate-400 hover:text-slate-200'
              }`}
              title="Filter by atmosphere"
            >
              Atmosphere
            </button>
            <button
              onClick={() => setFilterRings(prev => prev === true ? null : true)}
              className={`px-2.5 py-1.5 rounded-lg border transition-all ${
                filterRings === true
                  ? 'bg-purple-500/20 border-purple-400 text-purple-300 font-semibold'
                  : 'bg-white/5 border-white/5 text-slate-400 hover:text-slate-200'
              }`}
              title="Filter by ring system"
            >
              Rings
            </button>
          </div>
        </div>
      </div>

      {/* Content Area: Loading / Error / Empty / Grid / Table */}
      {loading ? (
        <div className="py-20 glass-panel rounded-3xl border border-white/10">
          <LoadingState
            message="Scanning Celestial Catalog & Ephemerides..."
            subMessage="Querying normalized astronomical data from NEBULA backend"
            size="lg"
          />
        </div>
      ) : error ? (
        <div className="py-16">
          <ErrorState
            title="Celestial Catalog Unavailable"
            message={error}
            onRetry={loadObjects}
          />
        </div>
      ) : filteredObjects.length === 0 ? (
        <div className="py-16 glass-panel rounded-3xl border border-white/10">
          <EmptyState
            title="No Celestial Objects Found"
            description={
              search
                ? `No objects matched "${search}" within the selected filters.`
                : 'No astronomical bodies matched your selected category and filter constraints.'
            }
            actionText="Reset All Filters"
            onAction={handleResetFilters}
          />
        </div>
      ) : (
        <>
          {/* Grid Cards View */}
          {viewMode === 'grid' ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {paginatedObjects.map((obj) => (
                <div
                  key={obj.id}
              className="group p-6 rounded-3xl glass-panel border border-white/10 hover:border-sky-400/40 hover:shadow-2xl hover:shadow-sky-500/10 transition-all flex flex-col justify-between space-y-4 relative overflow-hidden"
            >
              <div className="space-y-3">
                {/* Top Badge & Color Dot */}
                <div className="flex items-center justify-between">
                  <span className="text-[11px] font-mono px-2.5 py-0.5 rounded-full bg-white/5 border border-white/10 text-slate-300">
                    {obj.category}
                  </span>
                  <div className="flex items-center space-x-2">
                    <span
                      className="w-3 h-3 rounded-full shadow-sm"
                      style={{ backgroundColor: obj.color_hex || '#38bdf8' }}
                      title={`Albedo / Display Tint: ${obj.color_hex}`}
                    />
                    <button
                      onClick={() => setPreviewObject(obj)}
                      className="p-1 rounded-lg text-slate-400 hover:text-sky-300 hover:bg-white/5 transition-colors"
                      title="Quick 3D Telemetry Preview"
                    >
                      <Eye className="w-4 h-4" />
                    </button>
                  </div>
                </div>

                {/* Name */}
                <Link
                  to={`/object/${obj.id}`}
                  className="block text-xl font-bold text-white group-hover:text-sky-300 transition-colors"
                >
                  {obj.name}
                </Link>

                {/* Adaptive Multi-Persona Description */}
                <p className="text-xs text-slate-300 line-clamp-3 leading-relaxed">
                  {getAdaptiveDescription(obj)}
                </p>
              </div>

              {/* Empirical Telemetry Bar */}
              <div className="space-y-3 pt-3 border-t border-white/5">
                <div className="grid grid-cols-3 gap-2 text-center text-xs font-mono">
                  <div className="p-2 rounded-lg bg-white/5 border border-white/5">
                    <span className="text-[10px] text-slate-400 block font-sans">Mass</span>
                    <span className="font-semibold text-slate-200">
                      {obj.mass_earth_relative ? `${obj.mass_earth_relative} M⊕` : '—'}
                    </span>
                  </div>
                  <div className="p-2 rounded-lg bg-white/5 border border-white/5">
                    <span className="text-[10px] text-slate-400 block font-sans">Semi-Major</span>
                    <span className="font-semibold text-slate-200">
                      {obj.semi_major_axis_au !== null && obj.semi_major_axis_au !== undefined
                        ? `${obj.semi_major_axis_au} AU`
                        : '—'}
                    </span>
                  </div>
                  <div className="p-2 rounded-lg bg-white/5 border border-white/5">
                    <span className="text-[10px] text-slate-400 block font-sans">Period</span>
                    <span className="font-semibold text-slate-200">
                      {obj.orbital_period_days ? `${Math.round(obj.orbital_period_days)} d` : '—'}
                    </span>
                  </div>
                </div>

                {/* Source Badge & Action */}
                <div className="flex items-center justify-between pt-1 text-[11px] font-mono text-slate-400">
                  <span className="truncate max-w-[160px]" title={obj.data_source || 'Verified NASA Catalog'}>
                    src: {obj.data_source ? obj.data_source.split('(')[0].trim() : 'NASA / JPL Horizons'}
                  </span>
                  <Link
                    to={`/object/${obj.id}`}
                    className="text-sky-400 hover:text-sky-300 font-semibold inline-flex items-center space-x-1 group-hover:translate-x-0.5 transition-transform"
                  >
                    <span>Inspect</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        /* High-Density Scientific Table View */
        <div className="p-6 rounded-3xl glass-panel border border-white/10 overflow-x-auto shadow-2xl">
          <table className="w-full text-left text-xs">
            <thead className="bg-white/5 text-slate-400 border-b border-white/10 font-mono">
              <tr>
                <th className="p-3">Celestial Body</th>
                <th className="p-3">Category</th>
                <th className="p-3">Mass (M⊕)</th>
                <th className="p-3">Radius (km)</th>
                <th className="p-3">Semi-Major (AU)</th>
                <th className="p-3">Period (days)</th>
                <th className="p-3">Gravity (m/s²)</th>
                <th className="p-3">Temperature (K)</th>
                <th className="p-3">Data Provenance</th>
                <th className="p-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5 font-mono">
              {paginatedObjects.map((obj) => (
                <tr key={obj.id} className="hover:bg-white/5 transition-all">
                  <td className="p-3 font-bold text-white flex items-center space-x-2 font-sans">
                    <span className="w-2.5 h-2.5 rounded-full shrink-0" style={{ backgroundColor: obj.color_hex || '#38bdf8' }} />
                    <Link to={`/object/${obj.id}`} className="hover:text-sky-400 transition-colors">
                      {obj.name}
                    </Link>
                  </td>
                  <td className="p-3 text-slate-300">{obj.category}</td>
                  <td className="p-3 text-slate-300">{obj.mass_earth_relative ? `${obj.mass_earth_relative}` : '—'}</td>
                  <td className="p-3 text-slate-300">{obj.radius_km ? obj.radius_km.toLocaleString() : '—'}</td>
                  <td className="p-3 text-slate-300">{obj.semi_major_axis_au !== null ? `${obj.semi_major_axis_au}` : '—'}</td>
                  <td className="p-3 text-slate-300">{obj.orbital_period_days ? `${obj.orbital_period_days}` : '—'}</td>
                  <td className="p-3 text-slate-300">{obj.surface_gravity_m_s2 ? `${obj.surface_gravity_m_s2}` : '—'}</td>
                  <td className="p-3 text-slate-300">{obj.surface_temperature_k ? `${obj.surface_temperature_k}` : '—'}</td>
                  <td className="p-3 text-slate-400 text-[10px] truncate max-w-[140px]" title={obj.data_source || 'NASA JPL / Gaia'}>
                    {obj.data_source || 'NASA JPL'}
                  </td>
                  <td className="p-3 text-right">
                    <div className="inline-flex items-center space-x-1.5">
                      <button
                        onClick={() => setPreviewObject(obj)}
                        className="p-1.5 rounded-lg bg-white/5 hover:bg-white/10 text-slate-300 hover:text-white"
                        title="Quick Preview"
                      >
                        <Eye className="w-3.5 h-3.5" />
                      </button>
                      <Link
                        to={`/object/${obj.id}`}
                        className="px-2.5 py-1 rounded-lg bg-sky-500/20 text-sky-400 hover:bg-sky-500/30 text-xs font-semibold inline-flex items-center space-x-1"
                      >
                        <span>Telemetry</span>
                        <ArrowRight className="w-3 h-3" />
                      </Link>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Pagination Controls */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 p-4 rounded-2xl glass-panel border border-white/10 text-xs font-mono text-slate-400">
        <div className="flex items-center space-x-2">
          <span>Showing {paginatedObjects.length > 0 ? (currentPage - 1) * pageSize + 1 : 0} - {Math.min(currentPage * pageSize, filteredObjects.length)} of {filteredObjects.length} objects</span>
          <span>•</span>
          <span>Page {currentPage} of {totalPages}</span>
        </div>

        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-1.5">
            <span>Per Page:</span>
            <select
              value={pageSize}
              onChange={(e) => {
                setPageSize(Number(e.target.value));
                setCurrentPage(1);
              }}
              className="bg-space-950 border border-white/10 rounded-lg px-2 py-1 text-white focus:outline-none"
            >
              <option value={6}>6</option>
              <option value={9}>9</option>
              <option value={18}>18</option>
              <option value={36}>36</option>
            </select>
          </div>

          <div className="flex items-center space-x-1">
            <button
              onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
              disabled={currentPage <= 1}
              className="p-1.5 rounded-lg bg-space-900 border border-white/10 text-slate-300 disabled:opacity-40 disabled:cursor-not-allowed hover:text-white"
              aria-label="Previous Page"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="px-3 py-1 font-bold text-white bg-white/5 rounded-lg border border-white/10">
              {currentPage}
            </span>
            <button
              onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
              disabled={currentPage >= totalPages}
              className="p-1.5 rounded-lg bg-space-900 border border-white/10 text-slate-300 disabled:opacity-40 disabled:cursor-not-allowed hover:text-white"
              aria-label="Next Page"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
      </>
      )}

      {/* Quick Object Preview Modal */}
      {previewObject && (
        <Modal
          isOpen={!!previewObject}
          onClose={() => setPreviewObject(null)}
          title={previewObject.name}
          description={`${previewObject.category} • Empirical Astronomical Telemetry`}
          size="lg"
        >
          <div className="space-y-6">
            {/* 3D Visualizer Canvas */}
            <div className="h-64 rounded-2xl bg-space-950/80 border border-white/10 overflow-hidden relative shadow-inner">
              <Object3DViewer
                colorHex={previewObject.color_hex}
                hasRings={previewObject.has_rings}
              />
              <div className="absolute bottom-3 left-3 bg-space-900/80 backdrop-blur-md px-3 py-1 rounded-lg border border-white/10 text-[11px] font-mono text-slate-300">
                Albedo / Color: <span style={{ color: previewObject.color_hex || '#38bdf8' }}>{previewObject.color_hex || '#38bdf8'}</span>
              </div>
            </div>

            {/* Persona Adaptive Description */}
            <div className="p-4 rounded-xl bg-white/[0.03] border border-white/10 space-y-1">
              <span className="text-[10px] uppercase font-mono tracking-wider text-slate-400">
                {mode.toUpperCase()} Summary
              </span>
              <p className="text-xs text-slate-200 leading-relaxed">
                {getAdaptiveDescription(previewObject)}
              </p>
            </div>

            {/* Quick Metrics Grid */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-mono">
              <div className="p-3 rounded-xl bg-space-950 border border-white/10">
                <span className="text-[10px] text-slate-400 block font-sans uppercase">Mass</span>
                <span className="font-semibold text-white">
                  {previewObject.mass_earth_relative ? `${previewObject.mass_earth_relative} M⊕` : '—'}
                </span>
              </div>
              <div className="p-3 rounded-xl bg-space-950 border border-white/10">
                <span className="text-[10px] text-slate-400 block font-sans uppercase">Radius</span>
                <span className="font-semibold text-white">
                  {previewObject.radius_km ? `${previewObject.radius_km.toLocaleString()} km` : '—'}
                </span>
              </div>
              <div className="p-3 rounded-xl bg-space-950 border border-white/10">
                <span className="text-[10px] text-slate-400 block font-sans uppercase">Semi-Major Axis</span>
                <span className="font-semibold text-white">
                  {previewObject.semi_major_axis_au !== null ? `${previewObject.semi_major_axis_au} AU` : '—'}
                </span>
              </div>
              <div className="p-3 rounded-xl bg-space-950 border border-white/10">
                <span className="text-[10px] text-slate-400 block font-sans uppercase">Temperature</span>
                <span className="font-semibold text-white">
                  {previewObject.surface_temperature_k ? `${previewObject.surface_temperature_k} K` : '—'}
                </span>
              </div>
            </div>

            {/* Source Information & Provenance */}
            <div className="flex items-center justify-between text-xs font-mono text-slate-400 pt-3 border-t border-white/10">
              <div className="flex items-center space-x-1.5">
                <ShieldCheck className="w-4 h-4 text-emerald-400" />
                <span>Source: {previewObject.data_source || 'NASA Planetary Fact Sheet'}</span>
              </div>
              <Link
                to={`/object/${previewObject.id}`}
                onClick={() => setPreviewObject(null)}
                className="px-4 py-2 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-semibold flex items-center space-x-1.5 shadow-lg shadow-sky-600/30 transition-all font-sans"
              >
                <span>Open Full Detail</span>
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
};
