"use client";
import { useState } from "react";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");

  async function analyze() {
    if (!file) return;
    setLoading(true); setError("");
    try {
      const token = localStorage.getItem("resume_token");
      if (!token) throw new Error("Please register/login through the API first.");
      const form = new FormData(); form.append("file", file);
      const res = await fetch(`${API}/api/v1/resumes/upload`, { method: "POST", headers: { Authorization: `Bearer ${token}` }, body: form });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Upload failed");
      setResult(data.analysis);
    } catch (e) { setError(e instanceof Error ? e.message : "Something went wrong"); }
    finally { setLoading(false); }
  }

  return <main className="shell">
    <section className="hero">
      <div>
        <div className="eyebrow">AI Resume Analyst</div>
        <h1 className="title">Turn your resume into a better job strategy.</h1>
        <p className="subtitle">Upload a PDF or DOCX resume to extract skills, estimate ATS readiness, identify gaps and prepare for intelligent job matching.</p>
        <div className="card" style={{marginTop:24}}>
          <input type="file" accept=".pdf,.docx" onChange={e => setFile(e.target.files?.[0] || null)} />
          <button className="button" style={{marginTop:16}} onClick={analyze} disabled={!file || loading}>{loading ? "Analyzing…" : "Analyze Resume"}</button>
          {error && <p style={{color:"#c0392b"}}>{error}</p>}
        </div>
      </div>
      <div className="card">
        {result ? <>
          <div className="muted">Estimated ATS readiness</div>
          <div className="score">{result.ats_score}</div>
          <div className="grid">
            <div className="metric"><b>{result.skills?.length || 0}</b><span className="muted">Skills detected</span></div>
            <div className="metric"><b>{result.keyword_score}</b><span className="muted">Keyword score</span></div>
            <div className="metric"><b>{result.section_score}</b><span className="muted">Section score</span></div>
          </div>
          <h3>Recommendations</h3><ul>{result.recommendations?.map((x:string) => <li key={x}>{x}</li>)}</ul>
        </> : <><div className="eyebrow">What you get</div><h2>Actionable analysis, not just a score.</h2><p className="muted">The first implementation combines deterministic resume parsing and explainable scoring. The AI provider layer can be enabled as the next production phase.</p></>}
      </div>
    </section>
  </main>;
}
