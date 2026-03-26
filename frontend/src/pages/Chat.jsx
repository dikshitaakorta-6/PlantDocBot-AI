import "./Chat.css"
import { useState, useRef, useEffect } from "react"
import axios from "axios"
import { useDropzone } from "react-dropzone"
import MessageBubble from "../components/MessageBubble"
import DiagnosisCard from "../components/DiagnosisCard"
import Sidebar from "../components/Sidebar"

const API = "http://localhost:8000"

const SUGGESTIONS = [
  "Yellow spots on leaves",
  "Brown patches spreading fast",
  "White mold on underside",
  "Leaves curling and dying",
  "Orange rust on corn leaves"
]

export default function Chat() {
  const [messages, setMessages]   = useState([
    {
      role: "bot",
      content: "Welcome. I can diagnose plant diseases from leaf images or symptom descriptions. How can I help your crop today?",
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
    }
  ])
  const [input, setInput]         = useState("")
  const [loading, setLoading]     = useState(false)
  const [history, setHistory]     = useState([])
  const [preview, setPreview]     = useState(null)
  const [imageFile, setImageFile] = useState(null)
  const bottomRef                 = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const addMessage = (role, content, extra = {}) => {
    setMessages(prev => [...prev, {
      role,
      content,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      ...extra
    }])
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: { "image/*": [".jpg", ".jpeg", ".png"] },
    maxFiles: 1,
    noClick: true,
    onDrop: (files) => {
      if (files[0]) {
        setImageFile(files[0])
        setPreview(URL.createObjectURL(files[0]))
      }
    }
  })

  const handleImageSelect = (e) => {
    const file = e.target.files[0]
    if (file) {
      setImageFile(file)
      setPreview(URL.createObjectURL(file))
    }
  }

  const handleSend = async () => {
    if (!input.trim() && !imageFile) return
    setLoading(true)

    if (imageFile) {
      addMessage("user", `[Image uploaded: ${imageFile.name}]`, { isImage: true, preview })
      const formData = new FormData()
      formData.append("file", imageFile)
      try {
        const res = await axios.post(`${API}/api/diagnose/image`, formData)
        const data = res.data
        if (data.status === "low_confidence") {
          addMessage("bot", data.message)
        } else {
          addMessage("bot", "Here is my diagnosis based on your image:", {
            diagnosis: data.treatment,
            confidence: data.confidence
          })
          setHistory(prev => [...prev, {
            disease_name: data.treatment.disease_name,
            severity: data.treatment.severity
          }])
        }
      } catch {
        addMessage("bot", "Sorry, I could not process the image. Please try again.")
      }
      setImageFile(null)
      setPreview(null)

    } else {
      addMessage("user", input)
      const userText = input
      setInput("")
      try {
        const res = await axios.post(`${API}/api/chat/`, { message: userText, history: [] })
        const data = res.data
        if (data.type === "diagnosis" && data.treatment) {
          addMessage("bot", data.reply, {
            diagnosis: data.treatment,
            confidence: data.confidence
          })
          setHistory(prev => [...prev, {
            disease_name: data.treatment.disease_name,
            severity: data.treatment.severity
          }])
        } else {
          addMessage("bot", data.reply)
        }
      } catch {
        addMessage("bot", "Sorry, something went wrong. Please try again.")
      }
    }

    setLoading(false)
  }

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="chat-page" {...getRootProps()}>
      <input {...getInputProps()} />

      <Sidebar history={history} />

      <div className="chat-area">
        <div className="chat-header">
          <h2>AI Plant Disease Diagnosis</h2>
          <p>Describe symptoms or upload a leaf image to begin</p>
        </div>

        <div className={`chat-messages ${isDragActive ? "drag-active" : ""}`}>
          {isDragActive && (
            <div className="drag-overlay">Drop leaf image here</div>
          )}

          {messages.map((msg, i) => (
            <div key={i}>
              {msg.isImage && msg.preview ? (
                <div className="msg user">
                  <div className="msg-avatar user-avatar">U</div>
                  <div className="msg-bubble-wrap">
                    <img src={msg.preview} alt="uploaded" className="img-preview" />
                  </div>
                </div>
              ) : (
                <MessageBubble message={msg} />
              )}
              {msg.diagnosis && (
                <div className="diagnosis-wrapper">
                  <DiagnosisCard
                    data={msg.diagnosis}
                    confidence={msg.confidence}
                  />
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div className="msg bot">
              <div className="msg-avatar bot-avatar">PD</div>
              <div className="msg-bubble bot-bubble loading-dots">
                <span /><span /><span />
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        <div className="chat-input-area">
          <div className="suggestions">
            {SUGGESTIONS.map((s, i) => (
              <button
                key={i}
                className="suggestion-chip"
                onClick={() => setInput(s)}
              >
                {s}
              </button>
            ))}
          </div>

          {preview && (
            <div className="image-preview-row">
              <img src={preview} alt="preview" className="input-preview" />
              <button
                className="remove-preview"
                onClick={() => { setPreview(null); setImageFile(null) }}
              >
                x
              </button>
            </div>
          )}

          <div className="input-row">
            <label className="upload-btn" title="Upload image">
              +
              <input
                type="file"
                accept="image/*"
                style={{ display: "none" }}
                onChange={handleImageSelect}
              />
            </label>
            <textarea
              className="chat-input"
              placeholder="Describe symptoms or ask about a plant disease..."
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              rows={1}
            />
            <button
              className="send-btn"
              onClick={handleSend}
              disabled={loading}
            >
              &#8593;
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}