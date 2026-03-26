import { useState } from "react"
import { BrowserRouter as Router, Routes, Route, NavLink } from "react-router-dom"
import Chat from "./pages/Chat"
import DiseaseLibrary from "./pages/DiseaseLibrary"
import TreatmentGuide from "./pages/TreatmentGuide"
import History from "./pages/History"
import About from "./pages/About"
import LeafCanvas from "./components/LeafCanvas"
import "./App.css"

export default function App() {
  return (
    <Router>
      <div className="app-wrapper">
        <LeafCanvas />
        <nav className="navbar">
          <div className="logo">Plant<span>Doc</span>Bot</div>
          <div className="nav-links">
            <NavLink to="/"             className={({isActive}) => isActive ? "nav-btn active" : "nav-btn"} end>Diagnose</NavLink>
            <NavLink to="/library"      className={({isActive}) => isActive ? "nav-btn active" : "nav-btn"}>Disease Library</NavLink>
            <NavLink to="/treatments"   className={({isActive}) => isActive ? "nav-btn active" : "nav-btn"}>Treatment Guide</NavLink>
            <NavLink to="/history"      className={({isActive}) => isActive ? "nav-btn active" : "nav-btn"}>History</NavLink>
            <NavLink to="/about"        className={({isActive}) => isActive ? "nav-btn active" : "nav-btn"}>About</NavLink>
          </div>
        </nav>
        <main className="main-content">
          <Routes>
            <Route path="/"           element={<Chat />} />
            <Route path="/library"    element={<DiseaseLibrary />} />
            <Route path="/treatments" element={<TreatmentGuide />} />
            <Route path="/history"    element={<History />} />
            <Route path="/about"      element={<About />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}