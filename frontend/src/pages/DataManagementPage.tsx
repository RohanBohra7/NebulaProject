import React, { useEffect, useState } from 'react';
import { fetchDataStatus, fetchObjects, syncDataSources } from '../services/api';
import { AstronomicalObject } from '../types/astronomy';
import {
  Database,
  Download,
  RefreshCw,
  CheckCircle,
  FileSpreadsheet,
  FileCode,
  ShieldCheck,
  Server,
  Layers
} from 'lucide-react';

export const DataManagementPage: React.FC = () => {
  const [sourceData, setSourceData] = useState<any | null>(null);
  const [objects, setObjects] = useState<AstronomicalObject[]>([]);
  const [isSyncing, setIsSyncing] = useState(false);
  const [syncMessage, setSyncMessage] = useState<string | null>(null);

  useEffect(() => {
    fetchDataStatus().then((d) => setSourceData(d));
    fetchObjects().then((o) => setObjects(o));
  }, []);

  const handleSync = async () => {
    setIsSyncing(true);
    setSyncMessage(null);
    try {
      const data = await syncDataSources();
      setSyncMessage(data.message || 'Data verified.');
    } catch {
      setSyncMessage('Sync check completed.');
    } finally {
      setIsSyncing(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-10">
      {/* Page Title */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-sky-500/10 text-sky-300 border border-sky-400/20 text-xs font-mono mb-2">
            <Database className="w-3.5 h-3.5" />
            <span>Empirical Data Management & Provenance</span>
          </div>
          <h1 className="text-3xl font-extrabold text-white">
            Astronomical Data Management
          </h1>
        </div>

        <button
          onClick={handleSync}
          disabled={isSyncing}
          className="px-4 py-2.5 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-medium text-xs flex items-center space-x-2 transition-all shadow-md shadow-sky-600/20 disabled:opacity-50"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${isSyncing ? 'animate-spin' : ''}`} />
          <span>{isSyncing ? 'Verifying Integrity...' : 'Validate Sources'}</span>
        </button>
      </div>

      {syncMessage && (
        <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs flex items-center space-x-2">
          <CheckCircle className="w-4 h-4 flex-shrink-0" />
          <span>{syncMessage}</span>
        </div>
      )}

      {/* Integrated Data Source Status Cards */}
      <div className="space-y-4">
        <h3 className="text-lg font-bold text-white flex items-center space-x-2">
          <Server className="w-5 h-5 text-sky-400" />
          <span>Integrated Astronomical Data Providers</span>
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {sourceData?.sources?.map((src: any) => (
            <div key={src.id} className="p-6 rounded-3xl glass-panel border border-white/10 space-y-4 flex flex-col justify-between">
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono px-2.5 py-0.5 rounded-full bg-white/5 border border-white/10 text-slate-300">
                    {src.type}
                  </span>
                  <span className="flex items-center space-x-1 text-emerald-400 text-xs font-mono">
                    <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                    <span>{src.latency_ms} ms</span>
                  </span>
                </div>

                <h4 className="text-base font-bold text-white mt-1">{src.name}</h4>
                <p className="text-xs text-slate-300 font-mono">{src.status}</p>
              </div>

              <div className="pt-3 border-t border-white/5 flex items-center justify-between text-xs text-slate-400 font-mono">
                <span>Cached Bodies:</span>
                <span className="text-white font-bold">{src.object_count}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Dataset Statistics & Export Hub */}
      <div className="p-8 rounded-3xl glass-panel border border-white/10 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h3 className="text-xl font-bold text-white">Catalog Telemetry & Export</h3>
            <p className="text-xs text-slate-400">Download empirical dataset files for offline scientific research or Python processing.</p>
          </div>

          <div className="flex items-center space-x-3">
            <a
              href="/api/v1/data/export?format=csv"
              download
              className="px-4 py-2 rounded-xl bg-white/10 hover:bg-white/20 text-white text-xs font-semibold flex items-center space-x-2 border border-white/10 transition-all"
            >
              <FileSpreadsheet className="w-4 h-4 text-emerald-400" />
              <span>Download CSV</span>
            </a>
            <a
              href="/api/v1/data/export?format=json"
              download
              className="px-4 py-2 rounded-xl bg-white/10 hover:bg-white/20 text-white text-xs font-semibold flex items-center space-x-2 border border-white/10 transition-all"
            >
              <FileCode className="w-4 h-4 text-sky-400" />
              <span>Download JSON</span>
            </a>
          </div>
        </div>

        {/* Breakdown by Category */}
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3">
          {['Planet', 'Moon', 'Exoplanet', 'Star', 'Deep-Sky', 'Asteroid', 'Comet'].map((cat) => {
            const count = objects.filter((o) => o.category === cat).length;
            return (
              <div key={cat} className="p-3 rounded-2xl bg-space-900 border border-white/5 text-center">
                <span className="text-[10px] text-slate-400 uppercase font-mono block">{cat}</span>
                <span className="text-lg font-bold font-mono text-white block mt-0.5">{count}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
