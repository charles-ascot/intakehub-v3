import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import { useState, useEffect } from 'react'
import Dashboard from './pages/Dashboard'
import Providers from './pages/Providers'
import Credentials from './pages/Credentials'
import Testing from './pages/Testing'
import Monitoring from './pages/Monitoring'
import Storage from './pages/Storage'
import './App.css'

export default function App() {
  const [apiStatus, setApiStatus] = useState('checking')
  const [storageBackend, setStorageBackend] = useState(null)

  useEffect(() => {
    // Check backend connectivity
    fetch('http://localhost:8000/api/config')
      .then(res => res.json())
      .then(data => {
        setApiStatus('connected')
        setStorageBackend(data.storage_backend)
      })
      .catch(err => {
        console.error('Backend error:', err)
        setApiStatus('disconnected')
      })
  }, [])

  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <div className="nav-container">
            <Link to="/" className="nav-logo">
              <span className="logo-icon">🎯</span>
              IntakeHub A
              <span className="version">v3.0.0</span>
            </Link>
            
            <ul className="nav-menu">
              <li className="nav-item">
                <Link to="/" className="nav-link">Dashboard</Link>
              </li>
              <li className="nav-item">
                <Link to="/providers" className="nav-link">Providers</Link>
              </li>
              <li className="nav-item">
                <Link to="/credentials" className="nav-link">Credentials</Link>
              </li>
              <li className="nav-item">
                <Link to="/testing" className="nav-link">Testing</Link>
              </li>
              <li className="nav-item">
                <Link to="/monitoring" className="nav-link">Monitoring</Link>
              </li>
              <li className="nav-item">
                <Link to="/storage" className="nav-link">Storage</Link>
              </li>
            </ul>

            <div className="nav-status">
              <span className={`status-badge ${apiStatus}`}>
                {apiStatus === 'connected' ? '✓ Connected' : '✗ Offline'}
              </span>
              {storageBackend && (
                <span className="storage-badge">{storageBackend.toUpperCase()}</span>
              )}
            </div>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/providers" element={<Providers />} />
            <Route path="/credentials" element={<Credentials />} />
            <Route path="/testing" element={<Testing />} />
            <Route path="/monitoring" element={<Monitoring />} />
            <Route path="/storage" element={<Storage />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}
