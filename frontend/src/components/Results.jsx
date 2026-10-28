import { useState } from "react";

export default function Results({ results }) {
  const [activeTab, setActiveTab] = useState("cv");

  const tabs = [
    { id: "cv",       label: "Tailored CV" },
    { id: "cover",    label: "Cover Letter" },
    { id: "feedback", label: "Feedback" },
    { id: "keywords", label: "Keywords" },
  ];

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    alert("Copied to clipboard!");
  };

  return (
    <div style={styles.card}>
      {/* Tabs */}
      <div style={styles.tabs}>
        {tabs.map(t => (
          <button
            key={t.id}
            onClick={() => setActiveTab(t.id)}
            style={activeTab === t.id ? styles.tabActive : styles.tab}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* CV Tab */}
      {activeTab === "cv" && (
        <div>
          <div style={styles.tabHeader}>
            <h3 style={styles.tabTitle}>Your Tailored CV</h3>
            <button
              onClick={() => copyToClipboard(results.tailored_cv)}
              style={styles.copyBtn}
            >
              📋 Copy
            </button>
          </div>
          <pre style={styles.textBox}>{results.tailored_cv}</pre>
        </div>
      )}

      {/* Cover Letter Tab */}
      {activeTab === "cover" && (
        <div>
          <div style={styles.tabHeader}>
            <h3 style={styles.tabTitle}>Your Cover Letter</h3>
            <button
              onClick={() => copyToClipboard(results.cover_letter)}
              style={styles.copyBtn}
            >
              📋 Copy
            </button>
          </div>
          <pre style={styles.textBox}>{results.cover_letter}</pre>
        </div>
      )}

      {/* Feedback Tab */}
      {activeTab === "feedback" && (
        <div>
          <h3 style={styles.tabTitle}>Critic Feedback</h3>

          <div style={styles.feedbackSection}>
            <h4 style={styles.feedbackHeading}>CV Strengths</h4>
            <ul>
              {results.feedback?.cv_feedback?.strengths?.map((s, i) => (
                <li key={i} style={styles.feedbackItem}>{s}</li>
              ))}
            </ul>
          </div>

          <div style={styles.feedbackSection}>
            <h4 style={styles.feedbackHeading}>CV Improvements</h4>
            <ul>
              {results.feedback?.cv_feedback?.improvements?.map((s, i) => (
                <li key={i} style={styles.feedbackItem}>{s}</li>
              ))}
            </ul>
          </div>

          <div style={styles.feedbackSection}>
            <h4 style={styles.feedbackHeading}>Cover Letter Strengths</h4>
            <ul>
              {results.feedback?.cover_letter_feedback?.strengths?.map((s, i) => (
                <li key={i} style={styles.feedbackItem}>{s}</li>
              ))}
            </ul>
          </div>

          <div style={styles.feedbackSection}>
            <h4 style={styles.feedbackHeading}>Cover Letter Improvements</h4>
            <ul>
              {results.feedback?.cover_letter_feedback?.improvements?.map((s, i) => (
                <li key={i} style={styles.feedbackItem}>{s}</li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* Keywords Tab */}
      {activeTab === "keywords" && (
        <div>
          <h3 style={styles.tabTitle}>ATS Keywords Extracted</h3>
          <div style={styles.keywordsGrid}>
            {results.job_analysis?.keywords?.map((kw, i) => (
              <span key={i} style={styles.keyword}>{kw}</span>
            ))}
          </div>

          {results.feedback?.missing_keywords?.length > 0 && (
            <>
              <h4 style={{ ...styles.feedbackHeading, marginTop: 24 }}>
                Missing Keywords
              </h4>
              <div style={styles.keywordsGrid}>
                {results.feedback.missing_keywords.map((kw, i) => (
                  <span key={i} style={{ ...styles.keyword, background: "#fff0f0", color: "#cc0000", borderColor: "#ffcccc" }}>
                    {kw}
                  </span>
                ))}
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}

const styles = {
  card: {
    background: "#fff",
    border: "1px solid #e5e7eb",
    borderRadius: 12,
    padding: 28,
    boxShadow: "0 2px 12px rgba(0,0,0,0.06)",
  },
  tabs: {
    display: "flex",
    gap: 40,    
    marginBottom: 24,
    flexWrap: "wrap",
  },
  tab: {
    padding: "8px 16px",
    border: "1px solid #d1d5db",
    borderRadius: 8,
    background: "#f9fafb",
    cursor: "pointer",
    fontSize: 14,
    color: "#df7a27",
  },
  tabActive: {
    padding: "8px 16px",
    border: "1px solid #4f46e5",
    borderRadius: 8,
    background: "#ede9fe",
    cursor: "pointer",
    fontSize: 14,
    color: "#4f46e5",
    fontWeight: 700,
  },
  tabHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 12,
  },
  tabTitle: {
    fontSize: 16,
    fontWeight: 700,
    margin: 0,
    color: "#1a1a2e",
  },
  copyBtn: {
    padding: "6px 14px",
    background: "#141313",
    border: "1px solid #d1d5db",
    borderRadius: 6,
    cursor: "pointer",
    fontSize: 13,
  },
  textBox: {
    background: "#f9fafb",
    border: "1px solid #e5e7eb",
    borderRadius: 8,
    padding: 16,
    fontSize: 13,
    lineHeight: 1.8,
    whiteSpace: "pre-wrap",
    wordBreak: "break-word",
    maxHeight: 500,
    overflowY: "auto",
    fontFamily: "inherit",
  },
  feedbackSection: {
    marginBottom: 20,
  },
  feedbackHeading: {
    fontSize: 14,
    fontWeight: 700,
    color: "#333",
    marginBottom: 8,
  },
  feedbackItem: {
    fontSize: 14,
    color: "#444",
    lineHeight: 1.8,
  },
  keywordsGrid: {
    display: "flex",
    flexWrap: "wrap",
    gap: 8,
    marginTop: 12,
  },
  keyword: {
    padding: "4px 12px",
    background: "#ede9fe",
    color: "#4f46e5",
    border: "1px solid #c4b5fd",
    borderRadius: 20,
    fontSize: 13,
    fontWeight: 500,
  },
};