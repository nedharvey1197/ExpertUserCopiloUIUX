import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import IntakeFlow from '/src/pages/intakeFlow';
import Dashboard from '/src/pages/Dashboard';
// ...any other components you added

export default function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100 p-4">
        <header className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold">🧪 Clinical Copilot</h1>
          <nav className="space-x-4">
            <Link to="/intake" className="text-blue-600 hover:underline">
              Intake Flow
            </Link>
            <Link to="/dashboard" className="text-blue-600 hover:underline">
              Dashboard
            </Link>
          </nav>
        </header>

        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/intake" element={<IntakeFlow />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </div>
    </Router>
  );
}
