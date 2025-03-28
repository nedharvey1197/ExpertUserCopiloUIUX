// ✅ IntakeFlow.jsx (Restored original fields + NCT ID + backend wiring for ClinicalTrials.gov)
import React, { useState, useEffect } from "react";
import BenchmarkRunner from "/Users/nedharvey/Development/clinical-trials/ExpertUserCopiloUIUX/frontend/src/components/ui/benchmark_runner.js";

export default function IntakeFlow() {
  const [company, setCompany] = useState("");
  const [website, setWebsite] = useState("");
  const [therapeuticArea, setTherapeuticArea] = useState("");
  const [trialPhase, setTrialPhase] = useState("");
  const [nctId, setNctId] = useState("");

  const [sessionId, setSessionId] = useState(null);
  const [who, setWho] = useState("");
  const [what, setWhat] = useState("");
  const [where, setWhere] = useState("");
  const [when, setWhen] = useState("");
  const [why, setWhy] = useState("");

  const [uploadedFile, setUploadedFile] = useState(null);
  const [fileStatus, setFileStatus] = useState("idle");
  const [copilotSummary, setCopilotSummary] = useState("");

  const startSession = async () => {
    const res = await fetch("http://localhost:8000/copilot/session", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: "test-user",
        therapeutic_area: therapeuticArea,
        trial_phase: trialPhase,
        trial_condition: who,
        trial_intent: why,
        file_summary: "",
        ai_insights: {},
      }),
    });
    const data = await res.json();
    setSessionId(data.session_id);
    if (nctId) fetchTrialInfo(nctId);
  };

  const fetchTrialInfo = async (nct) => {
    try {
      const res = await fetch(`http://localhost:8000/copilot/nct/${nct}`);
      const data = await res.json();
      if (data && data.summary_snippet) setCopilotSummary(data.summary_snippet);
      if (data.phase) setTrialPhase(data.phase);
      if (data.who) setWho(data.who);
      if (data.what) setWhat(data.what);
      if (data.where) setWhere(data.where);
      if (data.when) setWhen(data.when);
      if (data.why) setWhy(data.why);
    } catch (err) {
      console.error("Failed to fetch trial info", err);
    }
  };

  useEffect(() => {
    const uploadFile = async () => {
      if (!uploadedFile || !sessionId) return;
      setFileStatus("processing");

      const formData = new FormData();
      formData.append("session_id", sessionId);
      formData.append("file", uploadedFile);

      try {
        const res = await fetch("http://localhost:8000/copilot/upload", {
          method: "POST",
          body: formData,
        });
        const data = await res.json();
        setFileStatus("done");
        fetchCopilotSummary(data.session_id || sessionId);
      } catch (err) {
        console.error("Upload failed", err);
        setFileStatus("error");
      }
    };
    uploadFile();
  }, [uploadedFile]);

  const fetchCopilotSummary = async (id) => {
    try {
      const res = await fetch(`http://localhost:8000/copilot/summary/${id}`);
      const data = await res.json();
      setCopilotSummary(JSON.stringify(data, null, 2));
    } catch (err) {
      console.error("Failed to fetch summary", err);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Step 1 */}
      <section className="bg-white rounded p-6 shadow">
        <h2 className="text-xl font-semibold mb-4">📋 Step 1: Trial Setup</h2>
        <div className="grid grid-cols-2 gap-4">
          <input value={company} onChange={e => setCompany(e.target.value)} placeholder="Company Name" className="input w-full" />
          <input value={website} onChange={e => setWebsite(e.target.value)} placeholder="Company Website" className="input w-full" />
          <input value={therapeuticArea} onChange={e => setTherapeuticArea(e.target.value)} placeholder="Therapeutic Area" className="input w-full" />
          <input value={trialPhase} onChange={e => setTrialPhase(e.target.value)} placeholder="Trial Phase" className="input w-full" />
          <input value={nctId} onChange={e => setNctId(e.target.value)} placeholder="NCT ID (e.g. NCT05791864)" className="input w-full col-span-2" />
        </div>
        <button onClick={startSession} className="btn mt-4">Start Copilot</button>
      </section>

      {/* Step 2 */}
      <section className="bg-white rounded p-6 shadow">
        <h2 className="text-xl font-semibold mb-4">🔎 Step 2: Define the 5Ws</h2>
        <div className="space-y-3">
          <textarea value={who} onChange={e => setWho(e.target.value)} placeholder="Who (Population)" className="textarea w-full resize-y min-h-[80px]" />
          <textarea value={what} onChange={e => setWhat(e.target.value)} placeholder="What (Intervention)" className="textarea w-full resize-y min-h-[80px]" />
          <textarea value={where} onChange={e => setWhere(e.target.value)} placeholder="Where (Geography)" className="textarea w-full resize-y min-h-[80px]" />
          <textarea value={when} onChange={e => setWhen(e.target.value)} placeholder="When (Timeline)" className="textarea w-full resize-y min-h-[80px]" />
          <textarea value={why} onChange={e => setWhy(e.target.value)} placeholder="Why (Purpose)" className="textarea w-full resize-y min-h-[80px]" />

          <input type="file" onChange={e => setUploadedFile(e.target.files[0])} className="mt-2" />
          {fileStatus === "done" && <p className="text-green-600 text-sm">✅ Copilot parsed your file. Summary updated.</p>}
          {fileStatus === "processing" && <p className="text-blue-500 text-sm">🔄 Uploading and parsing...</p>}
        </div>
        <BenchmarkRunner />
      </section>

      {/* Step 3 */}
      <section className="bg-white rounded p-6 shadow">
        <h2 className="text-xl font-semibold mb-4">🧠 Copilot Summary</h2>
        <pre className="text-sm whitespace-pre-wrap text-gray-800 bg-gray-50 p-4 rounded max-h-[400px] overflow-auto">
          {copilotSummary || "Copilot is waiting for your input..."}
        </pre>
      </section>
    </div>
  );
}