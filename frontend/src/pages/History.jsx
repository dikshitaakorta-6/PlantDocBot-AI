import { useState, useEffect } from "react"
import "./Pages.css"

export default function History() {
  const [history, setHistory] = useState([])

  useEffect(() => {
    const stored = localStorage.getItem("plantdocbot_history")
    if (stored) setHistory(JSON.parse(stored))
  }, [])

  const severityColor = { High: "badge-red", Medium: "badge-orange", None: "badge-teal" }

  const clearHistory = () => {
    localStorage.removeItem("plantdocbot_history")
    setHistory([])
  }

  return (
    <div className="page-container">
      <div className="page-header" style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
        <div>
          <h1>Diagnosis History</h1>
          <p>All your past plant diagnoses in one place</p>
        </div>
        {history.length > 0 && (
          <button className="clear-btn" onClick={clearHistory}>
            Clear History
          </button>
        )}
      </div>

      {history.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">+</div>
          <div className="empty-text">No diagnosis history yet</div>
          <div className="empty-sub">Start a diagnosis from the chat page</div>
        </div>
      ) : (
        <div className="history-list">
          {history.slice().reverse().map((item, i) => (
            <div key={i} className="history-item">
              <div className="history-item-left">
                <div className="history-disease">{item.disease_name}</div>
                <div className="history-plant">{item.plant}</div>
                <div className="history-time">{item.timestamp}</div>
              </div>
              <div className="history-item-right">
                <div className={`severity-badge ${severityColor[item.severity] || "badge-teal"}`}>
                  {item.severity}
                </div>
                <div className="history-confidence">
                  {item.confidence}% confidence
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}