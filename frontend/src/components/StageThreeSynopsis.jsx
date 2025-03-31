import React, { useState } from 'react';

export default function StageThreeSynopsis({ data, onBack, recordFeedback }) {
  const [rating, setRating] = useState(null);
  const [suggestion, setSuggestion] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = () => {
    recordFeedback({
      rating,
      suggestion,
      timestamp: new Date().toISOString(),
      trial: data.summary,
    });
    setSubmitted(true);
  };

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Copilot Trial Synopsis</h2>

      <div className="bg-gray-100 p-4 rounded shadow text-sm whitespace-pre-wrap">
        {data?.summary?.synopsis || 'Copilot summary not yet available.'}
      </div>

      <div>
        <h3 className="font-medium mb-1">Rate this summary</h3>
        <div className="flex gap-2">
          {[1, 2, 3, 4, 5].map((star) => (
            <button
              key={star}
              className={`w-8 h-8 rounded-full border text-sm ${rating === star ? 'bg-blue-500 text-white' : 'bg-white'}`}
              onClick={() => setRating(star)}
            >
              {star}
            </button>
          ))}
        </div>
      </div>

      <div>
        <label className="block font-medium mt-4 mb-1">Your suggestions</label>
        <textarea
          className="w-full border p-2"
          rows={3}
          value={suggestion}
          onChange={(e) => setSuggestion(e.target.value)}
          placeholder="What could make this more useful or insightful?"
        />
      </div>

      {!submitted ? (
        <div className="flex justify-between mt-6">
          <button className="px-4 py-2 bg-gray-300 rounded" onClick={onBack}>Back</button>
          <button className="px-4 py-2 bg-green-600 text-white rounded" onClick={handleSubmit}>
            Submit Feedback
          </button>
        </div>
      ) : (
        <div className="text-green-700 font-medium">Thank you for your feedback!</div>
      )}
    </div>
  );
}