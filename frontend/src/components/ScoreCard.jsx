export default function ScoreCard({ results }) {
  const scores = [
    { label: "Overall Score",        value: results.overall_score,        max: 100, color: "#4f46e5" },
    { label: "CV Score",             value: results.cv_score,             max: 100, color: "#0891b2" },
    { label: "Cover Letter Score",   value: results.cover_letter_score,   max: 100, color: "#059669" },
  ];

  return (
    <div style={styles.card}>
      <h2 style={styles.heading}>Quality Scores</h2>

      <div style={styles.grid}>
        {scores.map(s => (
          <div key={s.label} style={styles.scoreBox}>
            <div style={{ ...styles.circle, borderColor: s.color }}>
              <span style={{ ...styles.scoreNum, color: s.color }}>
                {s.value}
              </span>
              <span style={styles.scoreMax}>/{s.max}</span>
            </div>
            <p style={styles.scoreLabel}>{s.label}</p>
          </div>
        ))}

        <div style={styles.scoreBox}>
          <div style={{ ...styles.circle, borderColor: "#f59e0b" }}>
            <span style={{ ...styles.scoreNum, color: "#f59e0b" }}>
              {results.iterations}
            </span>
            <span style={styles.scoreMax}>/3</span>
          </div>
          <p style={styles.scoreLabel}>Critic Iterations</p>
        </div>
      </div>

      {/* Job Info */}
      <div style={styles.jobInfo}>
        <span>🏢 <strong>{results.job_analysis?.company}</strong></span>
        <span style={{ margin: "0 12px", color: "#ccc" }}>|</span>
        <span>💼 <strong>{results.job_analysis?.job_title}</strong></span>
      </div>
    </div>
  );
}

const styles = {
  card: {
    background: "#fff",
    border: "1px solid #e5e7eb",
    borderRadius: 12,
    padding: 28,
    marginBottom: 24,
    boxShadow: "0 2px 12px rgba(0,0,0,0.06)",
  },
  heading: {
    fontSize: 18,
    fontWeight: 700,
    marginTop: 0,
    marginBottom: 20,
    color: "#1a1a2e",
  },
  grid: {
    display: "flex",
    gap: 20,
    flexWrap: "wrap",
    justifyContent: "center",
    marginBottom: 20,
  },
  scoreBox: {
    textAlign: "center",
    minWidth: 100,
  },
  circle: {
    width: 80,
    height: 80,
    borderRadius: "50%",
    border: "4px solid",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    margin: "0 auto",
    flexDirection: "row",
  },
  scoreNum: {
    fontSize: 24,
    fontWeight: 700,
  },
  scoreMax: {
    fontSize: 12,
    color: "#999",
    marginTop: 4,
  },
  scoreLabel: {
    fontSize: 13,
    color: "#002fff",
    marginTop: 8,    
    fontWeight: 700,
  },
  jobInfo: {
    textAlign: "center",
    fontSize: 14,
    color: "#444",
    paddingTop: 16,
    borderTop: "1px solid #f0f0f0",
  },
};