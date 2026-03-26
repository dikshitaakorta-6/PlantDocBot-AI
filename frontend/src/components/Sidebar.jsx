export default function Sidebar({ history }) {
  const severityColor = {
    High   : "#e05050",
    Medium : "#e8a040",
    None   : "#20b28c",
    Low    : "#20b28c"
  }

  return (
    <div className="sidebar">
      <div className="sidebar-title">Active Session</div>
      <div className="sidebar-item active">
        <div className="sidebar-dot" />
        Current Diagnosis
      </div>

      {history.length > 0 && (
        <>
          <div className="sidebar-title" style={{ marginTop: "1rem" }}>
            Recent Diagnoses
          </div>
          {history.slice(-5).reverse().map((item, i) => (
            <div key={i} className="sidebar-item">
              <div
                className="sidebar-dot"
                style={{
                  background: severityColor[item.severity] || "#20b28c"
                }}
              />
              <span style={{ fontSize: "12px" }}>{item.disease_name}</span>
            </div>
          ))}
        </>
      )}

      <div style={{ marginTop: "auto" }}>
        <div className="sidebar-tip">
          Tip: Upload a clear photo of the affected leaf for best accuracy.
        </div>
      </div>
    </div>
  )
}