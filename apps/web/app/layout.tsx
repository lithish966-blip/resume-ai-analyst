import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = { title: "Resume AI Analyst", description: "AI-powered resume analysis and job matching" };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en"><body>{children}</body></html>;
}
