import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Landing from './pages/Landing';
import DashboardLayout from './components/DashboardLayout';
import Workspace from './pages/Workspace';
import Tasks from './pages/Tasks';
import Approvals from './pages/Approvals';
import Activity from './pages/Activity';
import Knowledge from './pages/Knowledge';
import Finance from './pages/Finance';
import Settings from './pages/Settings';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        
        <Route path="/dashboard" element={<DashboardLayout />}>
          <Route index element={<Workspace />} />
          <Route path="tasks" element={<Tasks />} />
          <Route path="approvals" element={<Approvals />} />
          <Route path="activity" element={<Activity />} />
          <Route path="knowledge" element={<Knowledge />} />
          <Route path="finance" element={<Finance />} />
          <Route path="settings" element={<Settings />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
