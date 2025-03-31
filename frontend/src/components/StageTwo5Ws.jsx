import React, { useState, useEffect } from 'react';

export default function StageTwo5Ws({ data, updateData, onBack, onComplete }) {
  const [form, setForm] = useState({ who: '', what: '', why: '', where: '', when: '' });

  useEffect(() => {
    if (data?.summary?.metadata) {
      setForm((prev) => ({ ...prev, ...data.summary.metadata }));
    }
  }, [data]);

  const handleChange = (field, value) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = () => {
    updateData({ metadata: form });
    onComplete();
  };

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Refine the 5Ws</h2>
      {['who', 'what', 'why', 'where', 'when'].map((field) => (
        <div key={field}>
          <label className="capitalize">{field}</label>
          <textarea
            className="w-full border p-2"
            rows={field === 'why' ? 4 : 2}
            value={form[field] || ''}
            onChange={(e) => handleChange(field, e.target.value)}
            placeholder={`Describe the ${field} of this trial...`}
          />
        </div>
      ))}

      <div className="flex justify-between mt-6">
        <button className="px-4 py-2 bg-gray-300 rounded" onClick={onBack}>Back</button>
        <button className="px-4 py-2 bg-blue-500 text-white rounded" onClick={handleSubmit}>
          Continue to Synopsis
        </button>
      </div>
    </div>
  );
}
