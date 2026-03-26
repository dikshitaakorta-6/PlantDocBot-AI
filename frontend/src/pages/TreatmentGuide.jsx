import { useState } from "react"
import "./Pages.css"

const TREATMENTS = [
  {
    disease: "Tomato Late Blight",
    plant: "Tomato",
    severity: "High",
    organic: [
      "Remove and destroy infected plant parts immediately",
      "Apply copper-based fungicide spray",
      "Use neem oil spray every 7 days",
      "Improve air circulation around plants",
      "Avoid overhead watering"
    ],
    chemical: [
      "Apply Mancozeb 75% WP at 2.5g/liter",
      "Use Metalaxyl + Mancozeb (Ridomil Gold)",
      "Spray Cymoxanil 8% + Mancozeb 64% WP"
    ],
    prevention: [
      "Use certified disease-free seeds",
      "Plant resistant varieties like Mountain Magic",
      "Rotate crops every season",
      "Avoid planting near potatoes"
    ]
  },
  {
    disease: "Tomato Early Blight",
    plant: "Tomato",
    severity: "Medium",
    organic: [
      "Remove infected lower leaves",
      "Apply compost tea spray",
      "Use copper fungicide spray",
      "Mulch around base of plant"
    ],
    chemical: [
      "Apply Chlorothalonil 75% WP",
      "Use Azoxystrobin based fungicide",
      "Spray Mancozeb 75% WP at 2g/liter"
    ],
    prevention: [
      "Use resistant tomato varieties",
      "Water at soil level not on leaves",
      "Space plants for good air circulation"
    ]
  },
  {
    disease: "Apple Scab",
    plant: "Apple",
    severity: "Medium",
    organic: [
      "Remove fallen leaves to reduce spore source",
      "Apply sulfur-based fungicide spray",
      "Prune trees for better air circulation"
    ],
    chemical: [
      "Apply Captan 50% WP at 2.5g/liter",
      "Use Myclobutanil 10% WP",
      "Spray Trifloxystrobin + Tebuconazole"
    ],
    prevention: [
      "Plant scab resistant varieties like Liberty",
      "Rake and destroy fallen leaves every autumn",
      "Apply dormant oil spray before bud break"
    ]
  },
  {
    disease: "Corn Common Rust",
    plant: "Corn",
    severity: "Medium",
    organic: [
      "Plant early to avoid peak rust season",
      "Remove heavily infected leaves",
      "Apply neem oil spray"
    ],
    chemical: [
      "Apply Propiconazole 25% EC",
      "Use Azoxystrobin + Propiconazole",
      "Spray Mancozeb 75% WP"
    ],
    prevention: [
      "Plant rust resistant hybrid varieties",
      "Monitor crops regularly from silking stage",
      "Rotate crops with non-host plants"
    ]
  },
  {
    disease: "Potato Late Blight",
    plant: "Potato",
    severity: "High",
    organic: [
      "Destroy infected plant material immediately",
      "Apply copper-based Bordeaux mixture",
      "Avoid overhead irrigation"
    ],
    chemical: [
      "Apply Metalaxyl + Mancozeb (Ridomil)",
      "Use Cymoxanil 8% + Mancozeb 64%",
      "Spray Dimethomorph 50% WP"
    ],
    prevention: [
      "Use certified disease-free seed tubers",
      "Plant resistant varieties like Sarpo Mira",
      "Destroy volunteer potato plants"
    ]
  },
  {
    disease: "Grape Black Rot",
    plant: "Grape",
    severity: "High",
    organic: [
      "Remove all mummified berries from vine",
      "Apply copper sulfate spray early season",
      "Prune for open canopy and air flow"
    ],
    chemical: [
      "Apply Myclobutanil 10% WP",
      "Use Mancozeb 75% WP spray",
      "Spray Captan 50% WP"
    ],
    prevention: [
      "Remove mummies and infected debris in winter",
      "Train vines for good air circulation",
      "Apply first spray at bud break"
    ]
  }
]

export default function TreatmentGuide() {
  const [selected, setSelected] = useState(0)
  const t = TREATMENTS[selected]
  const severityColor = { High: "badge-red", Medium: "badge-orange", None: "badge-teal" }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Treatment Guide</h1>
        <p>Detailed organic, chemical and prevention guide for each disease</p>
      </div>

      <div className="treatment-layout">
        <div className="treatment-sidebar">
          {TREATMENTS.map((item, i) => (
            <div
              key={i}
              className={`treatment-nav-item ${selected === i ? "active" : ""}`}
              onClick={() => setSelected(i)}
            >
              <div className="treatment-nav-name">{item.disease}</div>
              <div className={`severity-badge ${severityColor[item.severity]}`}>
                {item.severity}
              </div>
            </div>
          ))}
        </div>

        <div className="treatment-content">
          <div className="treatment-header">
            <h2>{t.disease}</h2>
            <div className={`severity-badge ${severityColor[t.severity]}`}>
              {t.severity} Severity
            </div>
          </div>

          <div className="treatment-sections">
            <div className="treatment-section">
              <div className="treatment-section-title">Organic Remedies</div>
              {t.organic.map((item, i) => (
                <div key={i} className="treatment-item organic">
                  <div className="treatment-item-num">{i + 1}</div>
                  <div className="treatment-item-text">{item}</div>
                </div>
              ))}
            </div>

            <div className="treatment-section">
              <div className="treatment-section-title">Chemical Remedies</div>
              {t.chemical.map((item, i) => (
                <div key={i} className="treatment-item chemical">
                  <div className="treatment-item-num">{i + 1}</div>
                  <div className="treatment-item-text">{item}</div>
                </div>
              ))}
            </div>

            <div className="treatment-section">
              <div className="treatment-section-title">Prevention Tips</div>
              {t.prevention.map((item, i) => (
                <div key={i} className="treatment-item prevention">
                  <div className="treatment-item-num">{i + 1}</div>
                  <div className="treatment-item-text">{item}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}