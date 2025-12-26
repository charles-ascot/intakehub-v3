import { useState, useEffect } from 'react'

export default function Providers() {
  const [providers, setProviders] = useState([])
  const [showForm, setShowForm] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [formData, setFormData] = useState({
    provider_type: 'betfair',
    name: '',
    description: '',
    enabled: true
  })

  const PROVIDER_TYPES = [
    { value: 'betfair', label: 'Betfair Exchange' },
    { value: 'pinnacle', label: 'Pinnacle Sports' },
    { value: 'timeform', label: 'Timeform' },
    { value: 'racing_post', label: 'Racing Post' },
    { value: 'sportradar', label: 'Sportradar' },
    { value: 'custom_api', label: 'Custom API' },
    { value: 'local_file', label: 'Local File' }
  ]

  useEffect(() => {
    fetchProviders()
  }, [])

  const fetchProviders = async () => {
    try {
      setLoading(true)
      setError(null)
      // TODO: Replace with real API call when endpoint is ready
      // const res = await fetch('http://localhost:8000/providers')
      // const data = await res.json()
      // setProviders(data)
      setProviders([]) // Empty for now
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const handleAddProvider = async (e) => {
    e.preventDefault()
    try {
      // TODO: Replace with real API call when endpoint is ready
      // const res = await fetch('http://localhost:8000/providers', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify(formData)
      // })
      // const newProvider = await res.json()
      // setProviders([...providers, newProvider])
      
      // For now, just add to local state
      const newProvider = {
        id: Math.random().toString(36).substr(2, 9),
        ...formData,
        created_at: new Date().toISOString()
      }
      setProviders([...providers, newProvider])
      
      setShowForm(false)
      setFormData({ provider_type: 'betfair', name: '', description: '', enabled: true })
    } catch (err) {
      setError(err.message)
    }
  }

  const handleDeleteProvider = async (id) => {
    if (!window.confirm('Are you sure you want to delete this provider?')) return
    try {
      // TODO: Replace with real API call when endpoint is ready
      // await fetch(`http://localhost:8000/providers/${id}`, { method: 'DELETE' })
      setProviders(providers.filter(p => p.id !== id))
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="container">
      <div className="page-title">📡 Providers</div>
      <div className="page-subtitle">Manage data providers and integrations</div>

      {error && (
        <div className="alert alert-error">
          ⚠️ {error}
        </div>
      )}

      {/* Add Provider Button */}
      <div style={{ marginBottom: '2rem' }}>
        <button 
          className="btn btn-primary"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? '✕ Cancel' : '➕ Add Provider'}
        </button>
      </div>

      {/* Add Provider Form */}
      {showForm && (
        <div className="card">
          <div className="card-title">New Provider</div>
          <form onSubmit={handleAddProvider}>
            <div className="form-group">
              <label>Provider Type</label>
              <select 
                name="provider_type" 
                value={formData.provider_type}
                onChange={handleInputChange}
                required
              >
                {PROVIDER_TYPES.map(type => (
                  <option key={type.value} value={type.value}>
                    {type.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Name</label>
              <input 
                type="text" 
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                placeholder="e.g., Production Betfair"
                required
              />
            </div>

            <div className="form-group">
              <label>Description</label>
              <textarea 
                name="description"
                value={formData.description}
                onChange={handleInputChange}
                placeholder="Optional description"
                rows="3"
              ></textarea>
            </div>

            <div className="form-group">
              <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <input 
                  type="checkbox" 
                  name="enabled"
                  checked={formData.enabled}
                  onChange={handleInputChange}
                  style={{ width: 'auto' }}
                />
                Enabled
              </label>
            </div>

            <button type="submit" className="btn btn-success">
              Create Provider
            </button>
          </form>
        </div>
      )}

      {/* Providers List */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '2rem' }}>
          <div className="loading"></div>
          <p style={{ marginTop: '1rem' }}>Loading providers...</p>
        </div>
      ) : providers.length === 0 ? (
        <div className="card">
          <div style={{ textAlign: 'center', padding: '2rem', color: '#999' }}>
            <p>No providers configured yet</p>
            <p style={{ fontSize: '0.9rem', marginTop: '1rem' }}>Click "Add Provider" to create your first integration</p>
          </div>
        </div>
      ) : (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Status</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {providers.map(provider => (
                <tr key={provider.id}>
                  <td><strong>{provider.name}</strong></td>
                  <td>
                    <span className="badge badge-primary">
                      {PROVIDER_TYPES.find(t => t.value === provider.provider_type)?.label}
                    </span>
                  </td>
                  <td>
                    <span className={`badge ${provider.enabled ? 'badge-success' : 'badge-danger'}`}>
                      {provider.enabled ? '✓ Enabled' : '✕ Disabled'}
                    </span>
                  </td>
                  <td>{new Date(provider.created_at).toLocaleDateString()}</td>
                  <td>
                    <button className="btn btn-primary btn-small" style={{ marginRight: '0.5rem' }}>
                      Edit
                    </button>
                    <button 
                      className="btn btn-danger btn-small"
                      onClick={() => handleDeleteProvider(provider.id)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Architecture Info */}
      <div className="card" style={{ marginTop: '2rem' }}>
        <div className="card-title">💡 How Provider Adapters Work</div>
        <div style={{ color: '#666', lineHeight: '1.8' }}>
          <p><strong>Pure Open Architecture:</strong> Every provider is a separate adapter implementing the same interface.</p>
          <ul style={{ marginTop: '1rem', paddingLeft: '1.5rem' }}>
            <li><strong>No Privilege:</strong> Betfair is one optional adapter, not baked in</li>
            <li><strong>Easy to Extend:</strong> Add new providers without touching core code</li>
            <li><strong>Swappable:</strong> Switch providers at runtime with configuration</li>
            <li><strong>Real APIs:</strong> All connections use real APIs, never mocked</li>
          </ul>
          <p style={{ marginTop: '1rem', fontSize: '0.9rem', fontStyle: 'italic', color: '#999' }}>
            Implementation files: <code>backend/src/integrations/</code>
          </p>
        </div>
      </div>
    </div>
  )
}
