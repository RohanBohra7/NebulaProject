import React from 'react';
import { cn } from '../../utils/cn';

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'glass' | 'interactive' | 'bordered';
  glow?: 'none' | 'sky' | 'purple' | 'amber' | 'emerald';
}

export const Card: React.FC<CardProps> = ({
  children,
  variant = 'glass',
  glow = 'none',
  className,
  ...props
}) => {
  const baseStyles = 'rounded-xl transition-all duration-300 relative overflow-hidden';
  
  const variantStyles = {
    default: 'bg-space-900 border border-white/10',
    glass: 'bg-space-900/70 backdrop-blur-md border border-white/10 shadow-xl shadow-black/40',
    interactive: 'bg-space-900/60 backdrop-blur-md border border-white/10 hover:border-sky-500/40 hover:bg-space-900/80 hover:shadow-lg hover:shadow-sky-500/10 cursor-pointer',
    bordered: 'bg-space-950/80 border-2 border-white/15',
  };

  const glowStyles = {
    none: '',
    sky: 'shadow-lg shadow-sky-500/10 border-sky-500/30',
    purple: 'shadow-lg shadow-purple-500/10 border-purple-500/30',
    amber: 'shadow-lg shadow-amber-500/10 border-amber-500/30',
    emerald: 'shadow-lg shadow-emerald-500/10 border-emerald-500/30',
  };

  return (
    <div className={cn(baseStyles, variantStyles[variant], glowStyles[glow], className)} {...props}>
      {children}
    </div>
  );
};

export const CardHeader: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children, className, ...props }) => (
  <div className={cn('p-5 border-b border-white/5 flex flex-col space-y-1.5', className)} {...props}>
    {children}
  </div>
);

export const CardTitle: React.FC<React.HTMLAttributes<HTMLHeadingElement>> = ({ children, className, ...props }) => (
  <h3 className={cn('text-lg font-semibold tracking-tight text-white flex items-center justify-between', className)} {...props}>
    {children}
  </h3>
);

export const CardDescription: React.FC<React.HTMLAttributes<HTMLParagraphElement>> = ({ children, className, ...props }) => (
  <p className={cn('text-xs text-slate-400 font-mono leading-relaxed', className)} {...props}>
    {children}
  </p>
);

export const CardContent: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children, className, ...props }) => (
  <div className={cn('p-5', className)} {...props}>
    {children}
  </div>
);

export const CardFooter: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children, className, ...props }) => (
  <div className={cn('p-4 px-5 border-t border-white/5 bg-white/[0.02] flex items-center justify-between', className)} {...props}>
    {children}
  </div>
);
