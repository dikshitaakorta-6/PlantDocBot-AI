import { useState } from "react"
import "./Pages.css"

const DISEASES = [
  {
    name: "Tomato Late Blight",
    plant: "Tomato",
    severity: "High",
    cause: "Phytophthora infestans",
    symptoms: ["Dark brown water-soaked spots", "White mold on underside", "Brown rotting stems"],
    season: "Cool & Wet"
  },
  {
    name: "Tomato Early Blight",
    plant: "Tomato",
    severity: "Medium",
    cause: "Alternaria solani",
    symptoms: ["Concentric ring spots", "Yellow halo around lesions", "Lower leaves affected first"],
    season: "Warm & Humid"
  },
  {
    name: "Apple Scab",
    plant: "Apple",
    severity: "Medium",
    cause: "Venturia inaequalis",
    symptoms: ["Olive green velvety spots", "Scabby fruit lesions", "Premature leaf drop"],
    season: "Spring & Wet"
  },
  {
    name: "Apple Black Rot",
    plant: "Apple",
    severity: "High",
    cause: "Botryosphaeria obtusa",
    symptoms: ["Purple bordered leaf spots", "Black rotting fruit", "Cankers on branches"],
    season: "Warm & Humid"
  },
  {
    name: "Corn Common Rust",
    plant: "Corn",
    severity: "Medium",
    cause: "Puccinia sorghi",
    symptoms: ["Brick red pustules on leaves", "Yellowing leaves", "Reduced yield"],
    season: "Cool & Humid"
  },
  {
    name: "Potato Late Blight",
    plant: "Potato",
    severity: "High",
    cause: "Phytophthora infestans",
    symptoms: ["Water-soaked dark spots", "White cottony growth", "Stem collapse"],
    season: "Cool & Wet"
  },
  {
    name: "Grape Black Rot",
    plant: "Grape",
    severity: "High",
    cause: "Guignardia bidwellii",
    symptoms: ["Tan spots with dark borders", "Mummified black berries", "Brown shoot lesions"],
    season: "Warm & Wet"
  },
  {
    name: "Healthy Plant",
    plant: "General",
    severity: "None",
    cause: "No pathogen",
    symptoms: ["Vibrant green leaves", "No spots or lesions", "Normal growth"],
    season: "Any"
  }
]

const PLANTS = ["All", "Tomato", "Apple", "Corn", "Potato", "Grape", "General"]
const SEVERITIES = ["All", "High", "Medium", "None"]

export default function DiseaseLibrary() {
  const [search,   setSearch]   = useState("")
  const [plant,    setPlant]    = useState("All")
  const [severity, setSeverity] = useState("All")
  const [selected, setSelected] = useState(null)

  const filtered = DISEASES.filter(d => {
    const matchSearch   = d.name.toLowerCase().includes(search.toLowerCase()) ||
                          d.plant.toLowerCase().includes(search.toLowerCase())
    const matchPlant    = plant    === "All" || d.plant    === plant
    const matchSeverity = severity === "All" || d.severity === severity
    return matchSearch && matchPlant && matchSeverity
  })

  const severityColor = { High: "badge-red", Medium: "badge-orange", None: "badge-teal" }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Disease Library</h1>
        <p>Browse all known plant diseases in the database</p>
      </div>

      <div className="filter-bar">
        <input
          className="search-input"
          placeholder="Search diseases..."
          value={search}
          onChange={e => setSearch(e.target.value)}
        />
        <div className="filter-group">
          {PLANTS.map(p => (
            <button
              key={p}
              className={`filter-btn ${plant === p ? "active" : ""}`}
              onClick={() => setPlant(p)}
            >{p}</button>
          ))}
        </div>
        <div className="filter-group">
          {SEVERITIES.map(s => (
            <button
              key={s}
              className={`filter-btn ${severity === s ? "active" : ""}`}
              onClick={() => setSeverity(s)}
            >{s}</button>
          ))}
        </div>
      </div>

      <div className="cards-grid">
        {filtered.map((d, i) => (
          <div
            key={i}
            className={`library-card ${selected === i ? "selected" : ""}`}
            onClick={() => setSelected(selected === i ? null : i)}
          >
            <div className="library-card-header">
              <div>
                <div className="library-card-name">{d.name}</div>
                <div className="library-card-plant">{d.plant}</div>
              </div>
              <div className={`severity-badge ${severityColor[d.severity]}`}>
                {d.severity}
              </div>
            </div>
            <div className="library-card-cause">Cause: {d.cause}</div>
            <div className="library-card-season">Season: {d.season}</div>
            {selected === i && (
              <div className="library-card-symptoms">
                <div className="remedy-label">Symptoms</div>
                {d.symptoms.map((s, j) => (
                  <div key={j} className="remedy-text">• {s}</div>
                ))}
              </div>
            )}
            <div className="expand-hint">
              {selected === i ? "Click to collapse" : "Click to expand"}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}