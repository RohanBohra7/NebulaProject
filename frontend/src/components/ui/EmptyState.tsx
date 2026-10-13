import React from 'react';
import { Telescope } from 'lucide-react';
import { Button } from './Button';
import { cn } from '../../utils/cn';

interface EmptyStateProps {
  title?: string;
  description?: string;
  actionText?: string;
  onAction?: () => void;
  icon?: React.ReactNode;
  className?: string;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title = 'No Celestial Data Found',
  description = 'No objects matched your orbital filters or celestial query parameters.',
  actionText,
  onAction,
  icon,
  className,
}) => {
  return (
    <div
      className={cn(
        'p-8 sm:p-12 rounded-xl bg-space-900/40 border border-white/5 text-center flex flex-col items-center justify-center space-y-4 max-w-md mx-auto',
        className
      )}
    >
      <div className="w-14 h-14 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center text-slate-400">
        {icon || <Telescope className="w-7 h-7" />}
      </div>
      <div>
        <h4 className="text-base font-medium text-white">{title}</h4>
        <p className="text-xs text-slate-400 font-mono mt-1 leading-relaxed">{description}</p>
      </div>
      {actionText && onAction && (
        <Button variant="outline" size="sm" onClick={onAction}>
          {actionText}
        </Button>
      )}
    </div>
  );
};
