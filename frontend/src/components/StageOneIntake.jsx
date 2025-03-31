import React, { useEffect, useState } from 'react';

const StageOneIntake = ({ updateData, onComplete }) => {
  const [company, setCompany] = useState('Tern Therapeutics');
  const [website, setWebsite] = useState('https://www.terntx.com/');
  const [nctId, setNctId] = useState('NCT05791864');
  const [file, setFile] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [copilotMessage, setCopilotMessage] = useState('');
  const [loading, setLoading] = useState(false);

  // Create session on mount

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setCopilotMessage('Creating session and uploading...');
  
    try {
      // ✅ 1. Create session with form data
      const sessionRes = await fetch('http://localhost:8000/copilot/session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          company_name: company,
          company_website: website,
          nct_id: nctId
        })
      });
  
      if (!sessionRes.ok) throw new Error("Session creation failed");
      const sessionData = await sessionRes.json();
      const sessionId = sessionData.session_id;
  
      // ✅ 2. Upload file and trigger enrichment
      const formData = new FormData();
      formData.append('session_id', sessionId);
      formData.append('company_name', company);
      formData.append('company_website', website);
      formData.append('nct_id', nctId);
      if (file) formData.append('file', file);
  
      const uploadRes = await fetch('http://localhost:8000/copilot/upload_file', {
        method: 'POST',
        body: formData,
      });
  
      if (!uploadRes.ok) throw new Error("Upload failed");
      const uploadResult = await uploadRes.json();
      console.log("Upload result:", uploadResult);
  
      updateData(uploadResult);
  
      // ✅ 3. Fetch summary
      const summaryRes = await fetch(`/copilot/summary/${sessionId}`);
      const summary = await summaryRes.json();
      updateData({ summary });
  
      setCopilotMessage('Copilot enrichment complete.');
      setLoading(false);
      onComplete();
    } catch (err) {
      console.error('Error during upload flow:', err);
      setCopilotMessage('An error occurred during Copilot enrichment.');
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      <h2 className="text-2xl font-semibold mb-2">Clinical Copilot Trial Intake</h2>
      <p className="text-sm text-gray-600 mb-4">Stage 1 of 3</p>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium">Company Name</label>
          <input
            type="text"
            className="w-full border p-2 rounded"
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium">Company Website</label>
          <input
            type="url"
            className="w-full border p-2 rounded"
            value={website}
            onChange={(e) => setWebsite(e.target.value)}
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium">NCT ID (optional)</label>
          <input
            type="text"
            className="w-full border p-2 rounded"
            value={nctId}
            onChange={(e) => setNctId(e.target.value)}
          />
        </div>

        <div>
          <label className="block text-sm font-medium">Upload Trial Document</label>
          <input
            type="file"
            className="w-full"
            onChange={(e) => setFile(e.target.files[0])}
            accept=".pdf,.docx,.txt,.csv,.tsv,.xlsx"
          />
        </div>

        {copilotMessage && (
          <p className="text-sm text-blue-600">{copilotMessage}</p>
        )}

        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          disabled={loading}
        >
          {loading ? 'Processing...' : 'Submit & Continue'}
        </button>
      </form>
    </div>
  );
};

export default StageOneIntake;