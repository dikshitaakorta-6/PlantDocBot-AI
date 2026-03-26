export default function DiagnosisCard({ data, confidence }) {
  const severityClass = {
    High   : "badge-red",
    Medium : "badge-orange",
    Low    : "badge-green",
    None   : "badge-teal"
  }[data.severity] || "badge-teal"

  return (
    <div className="diag-card">
      <div className="diag-header">
        <div className="diag-name">{data.disease_name}</div>
        <div className={`severity-badge ${severityClass}`}>
          {data.severity} Severity
        </div>
      </div>

      <div className="diag-meta">
        <span className="diag-plant">Plant: {data.plant}</span>
      </div>

      <div className="confidence-bar-wrap">
        <div className="confidence-label">Confidence — {confidence}%</div>
        <div className="confidence-bar">
          <div
            className="confidence-fill"
            style={{ width: `${confidence}%` }}
          />
        </div>
      </div>

      <p className="diag-description">{data.description}</p>

      <div className="diag-remedies">
        <div className="remedy-box">
          <div className="remedy-label">Organic Remedy</div>
          {data.organic_remedy.slice(0, 2).map((r, i) => (
            <div key={i} className="remedy-text">• {r}</div>
          ))}
        </div>
        <div className="remedy-box">
          <div className="remedy-label">Chemical Remedy</div>
          {data.chemical_remedy.length > 0
            ? data.chemical_remedy.slice(0, 2).map((r, i) => (
                <div key={i} className="remedy-text">• {r}</div>
              ))
            : <div className="remedy-text">Not required</div>
          }
        </div>
      </div>

      <div className="diag-prevention">
        <div className="remedy-label">Prevention</div>
        {data.prevention.slice(0, 2).map((p, i) => (
          <div key={i} className="remedy-text">• {p}</div>
        ))}
      </div>
    </div>
  )
}