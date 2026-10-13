import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';
import { Button } from './Button';
import { cn } from '../../utils/cn';

interface ErrorStateProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
  className?: string;
}

export const ErrorState: React.FC<ErrorStateProps> = ({
  title = 'Orbital Computation Exception',
  message = 'An unexpected error occurred while communicating with the NEBULA scientific backend.',
  onRetry,
  className,
}) => {
  return (
    <div
      className={cn(
        'p-6 sm:p-8 rounded-xl bg-rose-950/20 border border-rose-500/30 text-center flex flex-col items-center justify-center space-y-4 max-w-lg mx-auto',
        className
      )}
    >
      <div className="w-12 h-12 rounded-xl bg-rose-500/10 border border-rose-500/20 flex items-center justify-center text-rose-400">
        <AlertTriangle className="w-6 h-6" />
      </div>
      <div>
        <h3 className="text-base font-semibold text-rose-200">{title}</h3>
        <p className="text-xs text-rose-300/80 mt-1 font-mono leading-relaxed">{message}</p>
      </div>
      {onRetry && (
        <Button variant="secondary" size="sm" onClick={onRetry} leftIcon={<RefreshCw className="w-3.5 h-3.5" />}>
          Retry Computation
        </Button>
      )}
    </div>
  );
};
