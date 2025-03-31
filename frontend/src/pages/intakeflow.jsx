import React, { useState } from 'react';
import StageOneIntake from '../components/StageOneIntake';
import StageTwo5Ws from '../components/StageTwo5Ws';
import StageThreeSynopsis from '../components/StageThreeSynopsis';

export default function IntakeFlow() {
  const [stage, setStage] = useState(1);
  const [copilotData, setCopilotData] = useState({});
  const [feedback, setFeedback] = useState([]);

  const handleNextStage = () => setStage((prev) => Math.min(prev + 1, 3));
  const handlePrevStage = () => setStage((prev) => Math.max(prev - 1, 1));

  const updateCopilotData = (newData) => {
    setCopilotData((prev) => ({ ...prev, ...newData }));
  };

  const recordFeedback = (entry) => {
    setFeedback((prev) => [...prev, entry]);
    // Later: send to backend or persist
  };

  return (
    <div className="max-w-4xl mx-auto p-4">
      <div className="mb-6">
        <h1 className="text-2xl font-bold">Clinical Copilot Trial Intake</h1>
        <p className="text-sm text-gray-600">Stage {stage} of 3</p>
      </div>

      {stage === 1 && (
        <StageOneIntake
          onComplete={handleNextStage}
          updateData={updateCopilotData}
        />
      )}

      {stage === 2 && (
        <StageTwo5Ws
          data={copilotData}
          onBack={handlePrevStage}
          onComplete={handleNextStage}
          updateData={updateCopilotData}
        />
      )}

      {stage === 3 && (
        <StageThreeSynopsis
          data={copilotData}
          onBack={handlePrevStage}
          recordFeedback={recordFeedback}
        />
      )}
    </div>
  );
}
