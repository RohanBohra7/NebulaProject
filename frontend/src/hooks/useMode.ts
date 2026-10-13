import { useMode as useModeContext } from '../context/ModeContext';

export const useMode = () => {
  return useModeContext();
};
