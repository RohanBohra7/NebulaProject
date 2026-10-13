import React, { createContext, useContext, useState, useEffect } from 'react';
import { UserMode } from '../types/astronomy';

interface ModeContextType {
  mode: UserMode;
  setMode: (mode: UserMode) => void;
  units: 'astronomical' | 'si';
  setUnits: (units: 'astronomical' | 'si') => void;
  getModeThemeColor: () => string;
  getModeBadgeText: () => string;
}

const ModeContext = createContext<ModeContextType | undefined>(undefined);

export const ModeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [mode, setModeState] = useState<UserMode>(() => {
    const saved = localStorage.getItem('nebula_user_mode');
    return (saved as UserMode) || 'citizen';
  });

  const [units, setUnitsState] = useState<'astronomical' | 'si'>(() => {
    const saved = localStorage.getItem('nebula_units');
    return (saved as 'astronomical' | 'si') || 'astronomical';
  });

  const setMode = (newMode: UserMode) => {
    setModeState(newMode);
    localStorage.setItem('nebula_user_mode', newMode);
  };

  const setUnits = (newUnits: 'astronomical' | 'si') => {
    setUnitsState(newUnits);
    localStorage.setItem('nebula_units', newUnits);
  };

  const getModeThemeColor = () => {
    switch (mode) {
      case 'researcher':
        return '#38bdf8'; // Cyan / Sky
      case 'student':
        return '#fbbf24'; // Amber / Yellow
      case 'citizen':
        return '#c084fc'; // Purple / Magenta
      default:
        return '#38bdf8';
    }
  };

  const getModeBadgeText = () => {
    switch (mode) {
      case 'researcher':
        return 'Researcher (Astrophysical Rigor)';
      case 'student':
        return 'Student (Guided Learning)';
      case 'citizen':
        return 'Citizen (Cosmic Wonder)';
    }
  };

  return (
    <ModeContext.Provider
      value={{
        mode,
        setMode,
        units,
        setUnits,
        getModeThemeColor,
        getModeBadgeText
      }}
    >
      {children}
    </ModeContext.Provider>
  );
};

export const useMode = () => {
  const context = useContext(ModeContext);
  if (!context) {
    throw new Error('useMode must be used within a ModeProvider');
  }
  return context;
};
