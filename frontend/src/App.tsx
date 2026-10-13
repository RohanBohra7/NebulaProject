import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ModeProvider } from './context/ModeContext';
import { ToastProvider } from './context/ToastContext';
import { AppShell } from './layouts/AppShell';

// Pages
import { LandingPage } from './pages/LandingPage';
import { ModeSelectionPage } from './pages/ModeSelectionPage';
import { CitizenDashboard } from './pages/CitizenDashboard';
import { StudentDashboard } from './pages/StudentDashboard';
import { ResearcherDashboard } from './pages/ResearcherDashboard';
import { ExplorerPage } from './pages/ExplorerPage';
import { ObjectDetailPage } from './pages/ObjectDetailPage';
import { ComparisonPage } from './pages/ComparisonPage';
import { VisualizationPage } from './pages/VisualizationPage';
import { SimulationPage } from './pages/SimulationPage';
import { AIAssistantPage } from './pages/AIAssistantPage';
import { DataManagementPage } from './pages/DataManagementPage';
import { ResearchEvaluationPage } from './pages/ResearchEvaluationPage';
import { SettingsPage } from './pages/SettingsPage';

export const App: React.FC = () => {
  return (
    <ModeProvider>
      <ToastProvider>
        <Router>
          <AppShell>
            <Routes>
              <Route path="/" element={<LandingPage />} />
              <Route path="/mode" element={<ModeSelectionPage />} />
              <Route path="/citizen" element={<CitizenDashboard />} />
              <Route path="/student" element={<StudentDashboard />} />
              <Route path="/researcher" element={<ResearcherDashboard />} />
              <Route path="/explorer" element={<ExplorerPage />} />
              <Route path="/object/:id" element={<ObjectDetailPage />} />
              <Route path="/compare" element={<ComparisonPage />} />
              <Route path="/visualization" element={<VisualizationPage />} />
              <Route path="/simulation" element={<SimulationPage />} />
              <Route path="/ai" element={<AIAssistantPage />} />
              <Route path="/data" element={<DataManagementPage />} />
              <Route path="/research" element={<ResearchEvaluationPage />} />
              <Route path="/settings" element={<SettingsPage />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </AppShell>
        </Router>
      </ToastProvider>
    </ModeProvider>
  );
};

export default App;
