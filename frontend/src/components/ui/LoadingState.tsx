import React from 'react';
import { Orbit } from 'lucide-react';
import { cn } from '../../utils/cn';

interface LoadingStateProps {
  message?: string;
  subMessage?: string;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const LoadingState: React.FC<LoadingStateProps> = ({
  message = 'Computing ephemerides & astronomical telemetry...',
  subMessage = 'Querying high-precision Keplerian solver',
  size = 'md',
  className,
}) => {
  const iconSizes = {
    sm: 'w-6 h-6',
    md: 'w-10 h-10',
    lg: 'w-16 h-16',
  };

  return (
    <div className={cn('flex flex-col items-center justify-center p-8 text-center space-y-4', className)}>
      <div className="relative">
        <div className="absolute -inset-3 bg-gradient-to-r from-sky-500/20 via-indigo-500/20 to-purple-500/20 rounded-full blur-lg animate-pulse" />
        <div className="relative p-3 rounded-2xl bg-space-900 border border-sky-500/30 shadow-xl">
          <Orbit className={cn('text-sky-400 animate-spin-slow', iconSizes[size])} />
        </div>
      </div>
      <div className="space-y-1">
        <p className="text-sm font-semibold text-white tracking-wide">{message}</p>
        {subMessage && <p className="text-xs text-slate-400 font-mono">{subMessage}</p>}
      </div>
    </div>
  );
};
