import { useState } from "react";
import InputForm from "./components/InputForm";
import Results from "./components/Results";
import ScoreCard from "./components/ScoreCard";

export default function App() {
  const [loading, setLoading]   = useState(false);
  const [results, setResults]   = useState(null);
  const [error, setError]       = useState("");
  const [step, setStep]         = useState("form"); // form | loading | results

  const handleSubmit = async ({ cvText, jobUrl, jobText }) => {
    setLoading(true);
    setError("");
    setStep("loading");

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/apply`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          cv_text:  cvText,
          job_url:  jobUrl  || null,
          job_text: jobText || null,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Something went wrong.");
      }

      setResults(data.data);
      setStep("results");
    } catch (err) {
      setError(err.message);
      setStep("form");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResults(null);
    setError("");
    setStep("form");
  };

  return (
    <div style={styles.wrapper}>
      {/* Header */}
      <div style={styles.header}>
        <h1 style={styles.title}>AI Job Application Assistant</h1>
        <p style={styles.subtitle}>
          Our AI agents tailors your
          resume and write a cover letter in seconds.
        </p>
      </div>

      {/* Error Banner */}
      {error && (
        <div style={styles.errorBanner}>
          ⚠️ {error}
        </div>
      )}

      {/* Loading Screen */}
      {step === "loading" && (
        <div style={styles.loadingBox}>
          <div style={styles.spinner} />
          <h2 style={{ marginTop: 20 }}>Agents are working...</h2>
          <div style={styles.steps}>
            <p> (1) Analyzing job description</p>
            <p> (2) Tailoring your CV</p>
            <p> (3) Writing cover letter</p>
            <p> (4) Critic reviewing & refining</p>
          </div>
          <p style={{ color: "#1134d1", marginTop: 16 }}>
            This usually takes 15–30 seconds...
          </p>
        </div>
      )}

      {/* Input Form */}
      {step === "form" && (
        <InputForm onSubmit={handleSubmit} loading={loading} />
      )}

      {/* Results */}
      {step === "results" && results && (
        <>
          <ScoreCard results={results} />
          <Results results={results} />
          <div style={{ textAlign: "center", marginTop: 32 }}>
            <button onClick={handleReset} style={styles.resetBtn}>
              Back To Application
            </button>
          </div>
        </>
      )}
    </div>
  );
}

const styles = {
  wrapper: {
    maxWidth: 860,
    margin: "0 auto",
    padding: "32px 24px",
    fontFamily: "'Segoe UI', sans-serif",
    color: "#1a1a1a",
  },
  header: {
    textAlign: "center",
    marginBottom: 36,
  },
  title: {
    fontSize: 32,
    fontWeight: 700,
    margin: 0,
    color: "#11bbe6",
  },
  subtitle: {
    fontSize: 16,
    color: "#ffffff",
    marginTop: 8,
    maxWidth: 600,
    margin: "10px auto 0",
  },
  errorBanner: {
    background: "#fff0f0",
    border: "1px solid #ffcccc",
    borderRadius: 8,
    padding: "12px 16px",
    color: "#cc0000",
    marginBottom: 20,
    textAlign: "center",
  },
  loadingBox: {
    textAlign: "center",
    padding: "60px 20px",
    background: "#f9f9ff",
    borderRadius: 12,
    border: "1px solid #e0e0ff",
  },
  spinner: {
    width: 48,
    height: 48,
    border: "5px solid #e0e0ff",
    borderTop: "5px solid #4f46e5",
    borderRadius: "50%",
    animation: "spin 1s linear infinite",
    margin: "0 auto",
  },
  steps: {
    marginTop: 24,
    lineHeight: 2.2,
    fontSize: 15,
    color: "#444",
  },
  resetBtn: {
    padding: "12px 28px",
    background: "#4f46e5",
    color: "#fff",
    border: "none",
    borderRadius: 8,
    fontSize: 15,
    cursor: "pointer",
    fontWeight: 600,
  },
};