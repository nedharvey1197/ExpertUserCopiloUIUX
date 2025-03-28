// ✅ React Component: BenchmarkRunner.jsx
// Button at bottom of IntakeFlow to run the benchmark and show results
import React, { useState } from "react";

export default function BenchmarkRunner() {
  const [area, setArea] = useState("Oncology");
  const [limit, setLimit] = useState(10);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);

  const runBenchmark = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/copilot/benchmark", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ area, limit })
      });
      const data = await res.json();
      setResults(data);
    } catch (err) {
      console.error("Benchmark failed", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mt-8">
      <h3 className="text-lg font-bold mb-2">🧪 Trial Extraction Benchmark</h3>
      <div className="flex items-center gap-2 mb-4">
        <input
          type="text"
          className="input"
          value={area}
          onChange={e => setArea(e.target.value)}
          placeholder="Therapeutic Area (e.g. Oncology)"
        />
        <input
          type="number"
          className="input"
          value={limit}
          onChange={e => setLimit(Number(e.target.value))}
          placeholder="# Trials"
        />
        <button onClick={runBenchmark} className="btn">
          {loading ? "Running..." : "Run Benchmark"}
        </button>
      </div>

      {results.length > 0 && (
        <div className="overflow-x-auto max-h-[400px] border rounded p-4">
          {results.map((r, i) => (
            <div key={i} className="mb-4 border-b pb-2">
              <h4 className="font-semibold text-blue-700">{r.NCT_ID}</h4>
              <pre className="text-sm bg-gray-50 p-2 rounded overflow-x-auto">
                Direct Parse: {JSON.stringify(r.direct, null, 2)}
              </pre>
              <pre className="text-sm bg-green-50 p-2 rounded overflow-x-auto">
                LlamaExtract: {JSON.stringify(r.llama, null, 2)}
              </pre>
              <pre className="text-sm bg-yellow-50 p-2 rounded overflow-x-auto">
                LangChain: {JSON.stringify(r.langchain, null, 2)}
              </pre>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
