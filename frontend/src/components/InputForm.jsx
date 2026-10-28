import { useState } from "react";

export default function InputForm({ onSubmit, loading }) {
  const [cvText,   setCvText]   = useState("");
  const [jobUrl,   setJobUrl]   = useState("");
  const [jobText,  setJobText]  = useState("");
  const [jobMode,  setJobMode]  = useState("url"); // url | text

  const handleSubmit = () => {
    if (!cvText.trim()) {
      alert("Please paste your CV.");
      return;
    }
    if (jobMode === "url" && !jobUrl.trim()) {
      alert("Please enter a job URL.");
      return;
    }
    if (jobMode === "text" && !jobText.trim()) {
      alert("Please paste the job description.");
      return;
    }
    onSubmit({
      cvText,
      jobUrl:  jobMode === "url"  ? jobUrl  : "",
      jobText: jobMode === "text" ? jobText : "",
    });
  };

  return (
    <div style={styles.card}>

      {/* Job Input Toggle */}
      <div style={styles.section}>
        <label style={styles.label}>Job Posting</label>
        <div style={styles.toggle}>
          <button
            onClick={() => setJobMode("url")}
            style={jobMode === "url" ? styles.toggleActive : styles.toggleBtn}
          >
            🔗 Paste URL
          </button>
          <button
            onClick={() => setJobMode("text")}
            style={jobMode === "text" ? styles.toggleActive : styles.toggleBtn}
          >
            📋 Paste Text
          </button>
        </div>

        {jobMode === "url" ? (
          <input
            type="text"
            placeholder="https://apply.workable.com/..."
            value={jobUrl}
            onChange={e => setJobUrl(e.target.value)}
            style={styles.input}
          />
        ) : (
          <textarea
            placeholder="Paste the full job description here..."
            value={jobText}
            onChange={e => setJobText(e.target.value)}
            rows={7}
            style={styles.textarea}
          />
        )}
      </div>

      {/* CV Input */}
      <div style={styles.section}>
        <label style={styles.label}>CV or Resume</label>
        <textarea
          placeholder="Paste your full CV text here..."
          value={cvText}
          onChange={e => setCvText(e.target.value)}
          rows={12}
          style={styles.textarea}
        />
      </div>

      {/* Submit Button */}
      <button
        onClick={handleSubmit}
        disabled={loading}
        style={styles.submitBtn}
      >
        {loading ? "Processing..." : "Generate My Application"}
      </button>
    </div>
  );
}

const styles = {
  card: {
    background: "#b1aeae",
    border: "1px solid #034fe7",
    borderRadius: 30,
    padding: 28,
    boxShadow: "0 2px 12px rgba(0,0,0,0.06)",
  },
  section: {
    marginBottom: 24,
  },
  label: {
    display: "block",
    fontWeight: 900,
    fontSize: 18,
    marginBottom: 8,
    color: "#1010ec",
  },
  toggle: {
    display: "flex",
    gap: 8,
    marginBottom: 10,
  },
  toggleBtn: {
    padding: "8px 18px",
    border: "1px solid #d1d5db",
    borderRadius: 20,
    background: "#fefeff",
    cursor: "pointer",
    fontSize: 14,
    color: "#000000",
  },
  toggleActive: {
    padding: "8px 18px",
    border: "1px solid #4f46e5",
    borderRadius: 8,
    background: "#ede9fe",
    cursor: "pointer",
    fontSize: 14,
    color: "#4f46e5",
    fontWeight: 600,
  },
  input: {
    width: "100%",
    padding: "10px 14px",
    border: "1px solid #d1d5db",
    borderRadius: 18,
    fontSize: 14,
    background: "#fefeff",
    color: "#000000",
    outline: "none",
    boxSizing: "border-box",
  },
  textarea: {
    width: "100%",
    padding: "10px 14px",
    border: "1px solid #d1d5db",
    borderRadius: 14,
    fontSize: 14,
    outline: "none",
    resize: "vertical",
    color: "#000000",
    boxSizing: "border-box",
    background: "#fefeff",
    fontFamily: "inherit",
    lineHeight: 1.6,
  },
  submitBtn: {
    width: "100%",
    padding: "12px",
    background: "#4f46e5",
    color: "#fff",
    border: "none",
    borderRadius: 8,
    fontSize: 16,
    fontWeight: 700,
    cursor: "pointer",
    letterSpacing: 0.3,
  },
};