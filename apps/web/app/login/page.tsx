"use client";
import { useState } from "react";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function LoginPage() {
  const [email,setEmail]=useState(""); const [password,setPassword]=useState(""); const [name,setName]=useState(""); const [register,setRegister]=useState(false); const [message,setMessage]=useState("");
  async function submit(e:React.FormEvent){e.preventDefault(); setMessage(""); const path=register?"register":"login"; const body=register?{email,password,full_name:name}:{email,password}; const r=await fetch(`${API}/api/v1/auth/${path}`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)}); const d=await r.json(); if(!r.ok){setMessage(d.detail||"Request failed");return} localStorage.setItem("resume_token",d.access_token); setMessage("Logged in. Return to the home page to analyze your resume.");}
  return <main className="shell"><div className="card" style={{maxWidth:520,margin:"10vh auto"}}><div className="eyebrow">Resume AI Analyst</div><h1>{register?"Create your account":"Welcome back"}</h1><form onSubmit={submit}>{register&&<input placeholder="Full name" value={name} onChange={e=>setName(e.target.value)} required style={{display:"block",width:"100%",padding:14,margin:"12px 0"}}/>}<input type="email" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} required style={{display:"block",width:"100%",padding:14,margin:"12px 0"}}/><input type="password" placeholder="Password (8+ characters)" value={password} onChange={e=>setPassword(e.target.value)} required minLength={8} style={{display:"block",width:"100%",padding:14,margin:"12px 0"}}/><button className="button" type="submit">{register?"Create account":"Sign in"}</button></form><p className="muted" onClick={()=>setRegister(!register)} style={{cursor:"pointer"}}>{register?"Already have an account? Sign in":"New here? Create an account"}</p>{message&&<p>{message}</p>}</div></main>;
}
