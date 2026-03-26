import "./Pages.css"

export default function About() {
  return (
    <div className="page-container">
      <div className="page-header">
        <h1>About PlantDocBot</h1>
        <p>AI-powered plant disease diagnosis for farmers and gardeners</p>
      </div>

      <div className="about-grid">
        <div className="about-card">
          <div className="about-card-title">What is PlantDocBot?</div>
          <div className="about-card-text">
            PlantDocBot is an AI-powered chatbot that diagnoses plant diseases
            through leaf image analysis and symptom text descriptions. Built with
            deep learning models trained on 50,000+ plant images.
          </div>
        </div>

        <div className="about-card">
          <div className="about-card-title">How it works</div>
          <div className="about-card-text">
            Upload a photo of your plant leaf or describe the symptoms in plain
            language. Our CNN model analyzes images with 90% accuracy while our
            BERT model processes text descriptions for diagnosis.
          </div>
        </div>

        <div className="about-card">
          <div className="about-card-title">Image Diagnosis</div>
          <div className="about-card-text">
            Powered by MobileNetV2 trained on PlantVillage and PlantDoc datasets.
            Achieves over 90% validation accuracy across 10+ disease classes.
            Simply upload a clear leaf photo for instant diagnosis.
          </div>
        </div>

        <div className="about-card">
          <div className="about-card-title">Text Diagnosis</div>
          <div className="about-card-text">
            Powered by BERT natural language model fine-tuned on agricultural
            symptom descriptions. Describe what you see and the model will
            identify the most likely disease.
          </div>
        </div>

        <div className="about-card">
          <div className="about-card-title">Datasets Used</div>
          <div className="about-card-text">
            PlantVillage Dataset — 54,000+ annotated leaf images across 38 disease
            classes. PlantDoc Dataset — real-world noisy plant images for robust
            testing. Custom symptom text corpus for NLP training.
          </div>
        </div>

        <div className="about-card">
          <div className="about-card-title">Tech Stack</div>
          <div className="about-card-text">
            Frontend: React + Vite. Backend: FastAPI + Python. Image Model:
            MobileNetV2 via TensorFlow. Text Model: BERT via HuggingFace.
            Treatment Database: Custom rule-based mapping system.
          </div>
        </div>
      </div>

      <div className="disclaimer">
        This tool is for educational and advisory purposes only.
        Always consult a certified agricultural expert for critical crop decisions.
      </div>
    </div>
  )
}
