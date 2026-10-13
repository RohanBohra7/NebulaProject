import React from 'react';
import { cn } from '../../utils/cn';

interface StatBadgeProps {
  label: string;
  value: string | number;
  unit?: string;
  icon?: React.ReactNode;
  variant?: 'sky' | 'purple' | 'amber' | 'emerald' | 'rose' | 'default';
  className?: string;
}

export const StatBadge: React.FC<StatBadgeProps> = ({
  label,
  value,
  unit,
  icon,
  variant = 'default',
  className,
}) => {
  const variantStyles = {
    default: 'bg-white/5 border-white/10 text-slate-300',
    sky: 'bg-sky-500/10 border-sky-500/30 text-sky-300',
    purple: 'bg-purple-500/10 border-purple-500/30 text-purple-300',
    amber: 'bg-amber-500/10 border-amber-500/30 text-amber-300',
    emerald: 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300',
    rose: 'bg-rose-500/10 border-rose-500/30 text-rose-300',
  };

  return (
    <div
      className={cn(
        'px-3 py-2 rounded-lg border flex items-center space-x-2.5 text-xs font-mono backdrop-blur-sm',
        variantStyles[variant],
        className
      )}
    >
      {icon && <span className="shrink-0">{icon}</span>}
      <div className="flex flex-col min-w-0">
        <span className="text-[10px] text-slate-400 uppercase tracking-wider font-sans">{label}</span>
        <span className="font-semibold text-white truncate">
          {value} {unit && <span className="text-[10px] text-slate-400 font-normal">{unit}</span>}
        </span>
      </div>
    </div>
  );
};
