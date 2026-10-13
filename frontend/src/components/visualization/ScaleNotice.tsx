import React, { useState } from 'react';
import { ScaleMode } from '../../utils/orbitalMath';
import { Scale, Info, X } from 'lucide-react';

interface ScaleNoticeProps {
  scaleMode: ScaleMode;
  onToggleScaleMode: (mode: ScaleMode) => void;
}

export const ScaleNotice: React.FC<ScaleNoticeProps> = ({ scaleMode, onToggleScaleMode }) => {
  const [showExplanation, setShowExplanation] = useState(false);

  return (
    <>
      <div className="flex items-center space-x-2 bg-space-950/80 backdrop-blur-md px-3 py-1.5 rounded-xl border border-white/10 text-xs">
        <Scale className="w-3.5 h-3.5 text-amber-400" />
        <span className="text-slate-400">Scale:</span>
        <button
          onClick={() => onToggleScaleMode(scaleMode === 'enhanced' ? 'scientific' : 'enhanced')}
          className={`px-2.5 py-0.5 rounded-lg text-[11px] font-semibold border transition-all ${
            scaleMode === 'enhanced'
              ? 'bg-amber-500/20 border-amber-400/40 text-amber-300'
              : 'bg-cyan-500/20 border-cyan-400/40 text-cyan-300'
          }`}
          title="Toggle non-linear enhanced scale vs proportional scientific scale"
        >
          {scaleMode === 'enhanced' ? 'Visibility-Enhanced' : 'Scientific Proportional'}
        </button>

        <button
          onClick={() => setShowExplanation(true)}
          className="p-1 rounded text-slate-400 hover:text-white transition-colors"
          title="Why are astronomical scales adjusted?"
        >
          <Info className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* Modal / Dialog explaining astronomical scale rationale */}
      {showExplanation && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in">
          <div className="max-w-md w-full glass-panel rounded-2xl border border-white/15 p-6 space-y-4 shadow-2xl relative">
            <button
              onClick={() => setShowExplanation(false)}
              className="absolute top-4 right-4 text-slate-400 hover:text-white transition-colors"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex items-center space-x-2 text-amber-400">
              <Scale className="w-5 h-5" />
              <h3 className="text-base font-bold text-white">Astronomical Scale Rationale</h3>
            </div>

            <div className="space-y-3 text-xs text-slate-300 leading-relaxed font-sans">
              <p>
                In the physical Solar System, astronomical distances (100 million km) and planetary diameters (thousands of km) differ by more than <strong className="text-white">5 orders of magnitude</strong>.
              </p>
              <p>
                If drawn to 1:1 physical scale, the Earth would be a microscopic fraction of a pixel at orbital distance, while Neptune would be hundreds of screen widths away.
              </p>

              <div className="p-3 rounded-xl bg-space-900 border border-white/5 space-y-1.5 font-mono text-[11px]">
                <div className="flex justify-between">
                  <span className="text-amber-400 font-semibold">Visibility-Enhanced:</span>
                  <span className="text-slate-300">Logarithmic orbital spacing & boosted radii</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-cyan-400 font-semibold">Scientific Proportional:</span>
                  <span className="text-slate-300">Linear astronomical units ($a \propto r$)</span>
                </div>
              </div>

              <p className="text-[11px] text-slate-400 italic">
                * Note: Visual scale does not represent literal unadjusted 1:1 physical scale. Keplerian velocity, period, and eccentricity geometry remain rigorously accurate.
              </p>
            </div>

            <button
              onClick={() => setShowExplanation(false)}
              className="w-full py-2 rounded-xl bg-sky-500 hover:bg-sky-400 text-space-950 font-bold text-xs transition-all shadow-md"
            >
              Understood
            </button>
          </div>
        </div>
      )}
    </>
  );
};
