"use client";

import { useMemo, useState } from "react";

const jobs = [
  ["Senior Python Developer", "Tech Solutions Inc.", "Remote", 92],
  ["Backend Developer", "InnovateX", "Bangalore, India", 85],
  ["Full Stack Developer", "DevWorks", "Hyderabad, India", 78],
  ["Software Engineer", "CodeCraft", "Pune, India", 75],
  ["Python Developer", "WebVerse", "Remote", 72],
];

const skills = [["Docker", 90], ["AWS", 85], ["FastAPI", 80], ["Kubernetes", 75], ["Redis", 70]];

export default function Dashboard() {
  const [active, setActive] = useState("Dashboard");
  const [uploaded, setUploaded] = useState(false);
  const [showAll, setShowAll] = useState(false);
  const visibleJobs = useMemo(() => showAll ? jobs : jobs.slice(0, 4), [showAll]);

  const nav = ["Dashboard", "Resumes", "Job Matches", "Skill Gap", "Job Recommendations", "Applications"];
  const account = ["Profile", "Preferences", "Billing"];

  return (
    <main className="shell">
      <aside className="sidebar">
        <div className="brand"><span className="brandMark">AI</span><span>Resume AI<br/><b>Analyst</b></span></div>
        <p className="navLabel">MAIN</p>
        {nav.map(item => <button key={item} className={`navItem ${active === item ? "active" : ""}`} onClick={() => setActive(item)}><span>{icon(item)}</span>{item}</button>)}
        <div className="divider" />
        <p className="navLabel">ACCOUNT</p>
        {account.map(item => <button key={item} className="navItem" onClick={() => setActive(item)}><span>{icon(item)}</span>{item}</button>)}
        <div className="divider" />
        <p className="navLabel">ADMIN</p>
        {["Admin Dashboard", "Users", "Jobs", "Analytics", "Settings"].map(item => <button key={item} className="navItem" onClick={() => setActive(item)}><span>{icon(item)}</span>{item}</button>)}
        <div className="upgrade"><div>👑</div><strong>Upgrade to Pro</strong><p>Unlock premium features</p><button>Upgrade Now</button></div>
      </aside>

      <section className="content">
        <header className="topbar"><div><div className="hamburger">☰</div><div><h1>{active}</h1><p>Overview of your resume analysis and career insights</p></div></div><div className="user"><span className="bell">♧</span><span className="avatar">JD</span><div><b>John Doe</b><small>👑 Premium Plan</small></div><span>⌄</span></div></header>

        <div className="body">
          <section className="hero">
            <div className="heroArt">📄<span>🔎</span></div>
            <div><h2>Welcome back, John! 👋</h2><p>Your resume score is <b>Good</b>. Let&apos;s improve it to Excellent!</p><div className="heroActions"><button className="primary" onClick={() => document.getElementById("resume-upload")?.click()}>↥ Upload New Resume</button><button className="ghost">› View Recommendations</button></div></div>
            <div className="scoreRing"><strong>72</strong><span>Overall Score</span><em>Good</em></div>
          </section>

          <div className="grid topCards">
            <Metric title="ATS Score" value="72" label="Good" tone="green" icon="🎯" />
            <Metric title="Content Score" value="78" label="Good" tone="blue" icon="▤" />
            <Metric title="Skills Score" value="68" label="Average" tone="purple" icon="⌘" />
            <Metric title="Format Score" value="82" label="Very Good" tone="orange" icon="▦" />
            <UploadCard uploaded={uploaded} setUploaded={setUploaded} />
          </div>

          <div className="grid mainGrid">
            <section className="card analysis"><div className="cardHead"><h3>Recent Resume Analysis</h3><button>View Full Analysis</button></div><div className="resumeRow"><span className="docIcon">▤</span><div><b>John_Doe_Resume.pdf</b><small>Uploaded just now · 245 KB</small></div><span className="status">Analyzed</span></div><div className="analysisBody"><div className="bigScore"><div className="miniRing"><strong>72</strong></div><b>ATS Score</b><small>Good</small></div><div><h4>Strengths</h4><p>✓ Good use of action verbs</p><p>✓ Relevant work experience</p><p>✓ Skills match with job market</p><p>✓ Education is well structured</p></div><div><h4>Areas to Improve</h4><p className="warn">⚠ Add more quantified achievements</p><p className="warn">⚠ Improve resume summary</p><p className="warn">⚠ Include more relevant keywords</p><p className="warn">⚠ Add certifications</p></div></div><div className="recommendations"><h4>Recommendations</h4>{["Add quantifiable achievements to improve impact","Include more industry-specific keywords","Improve your professional summary","Add relevant certifications to boost score"].map(x => <div key={x}>▣ {x}<span>→</span></div>)}</div></section>

            <section className="card"><div className="cardHead"><h3>Top Job Matches</h3><button onClick={() => setShowAll(!showAll)}>{showAll ? "Show Less" : "View All"}</button></div>{visibleJobs.map(([title, company, location, score]) => <div className="job" key={title}><span className="jobLogo">●</span><div><b>{title}</b><small>{company} · {location}</small></div><strong>{score}% Match</strong></div>)}<button className="fullBtn" onClick={() => setShowAll(!showAll)}>{showAll ? "Show Less" : "See All Matches"}</button></section>

            <section className="card skillCard"><div className="cardHead"><h3>Skill Gap Overview</h3><button>View Full Report</button></div><div className="donut"><strong>24</strong><span>Total Gaps</span></div><div className="legend"><span>🔴 High Priority <b>8</b></span><span>🟠 Medium Priority <b>10</b></span><span>🟢 Low Priority <b>6</b></span></div></section>

            <section className="card recommended"><div className="cardHead"><h3>Recommended Skills</h3><button>View All</button></div>{skills.map(([skill, pct]) => <div className="skill" key={skill}><div><b>{skill}</b><span>{pct}%</span></div><div className="bar"><i style={{ width: `${pct}%` }} /></div></div>)}<button className="fullBtn">Get Learning Path</button></section>
          </div>

          <section className="card career"><div className="cardHead"><h3>AI Career Insights</h3><button>View Career Report</button></div><div className="insights"><Insight icon="💼" title="In-Demand Role" value="Python Developer" sub="High demand in your location" trend="+24% growth"/><Insight icon="💰" title="Salary Insight" value="₹12 – 18 LPA" sub="Estimated salary range" trend="+15% vs last year"/><Insight icon="↗" title="Career Path" value="Backend Architect" sub="Suggested next role" trend="High match potential"/><Insight icon="📈" title="Market Trend" value="Very High" sub="Job market demand" trend="Increasing rapidly"/></div></section>
        </div>
      </section>
    </main>
  );
}

function Metric({ title, value, label, tone, icon }: {title:string;value:string;label:string;tone:string;icon:string}) { return <section className="card metric"><span className={`metricIcon ${tone}`}>{icon}</span><div><h3>{title}</h3><strong>{value}<small>/100</small></strong><em>{label}</em></div><div className="spark">⌁⌁⌁⌁</div></section> }
function UploadCard({ uploaded, setUploaded }: {uploaded:boolean;setUploaded:(v:boolean)=>void}) { return <section className="card upload"><h3>Resume Upload</h3><label htmlFor="resume-upload"><span>☁</span><b>{uploaded ? "Resume ready for analysis" : "Drag & drop your resume here"}</b><small>PDF, DOCX (Max 5MB)</small><button type="button">{uploaded ? "Analyze Resume" : "Upload Resume"}</button></label><input id="resume-upload" type="file" accept=".pdf,.docx" onChange={() => setUploaded(true)} /></section> }
function Insight({icon,title,value,sub,trend}:{icon:string;title:string;value:string;sub:string;trend:string}) { return <div className="insight"><span>{icon}</span><div><small>{title}</small><b>{value}</b><p>{sub}</p><em>{trend}</em></div></div> }
function icon(item:string) { const m:any={Dashboard:"⌂",Resumes:"▤","Job Matches":"◎","Skill Gap":"◌","Job Recommendations":"☆",Applications:"▣",Profile:"♙",Preferences:"⚙",Billing:"▤","Admin Dashboard":"▦",Users:"♙",Jobs:"▣",Analytics:"◔",Settings:"⚙"}; return m[item] || "•"; }
