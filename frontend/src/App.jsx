import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import IntakeFlow from "/src/pages/intakeFlow";
// ...any other components you added

export default function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100 p-4">
        <header className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold">🧪 Clinical Copilot</h1>
          <nav className="space-x-4">
            <Link to="/intake" className="text-blue-600 hover:underline">Intake Flow</Link>
            <span className="text-gray-400">Dashboard (coming soon)</span>
          </nav>
        </header>

        <Routes>
          <Route path="/intake" element={<IntakeFlow />} />
          {/* Re-add any other routes/components you had here */}
        </Routes>
      </div>
    </Router>
  );
}