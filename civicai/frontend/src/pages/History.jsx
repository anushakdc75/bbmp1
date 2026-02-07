import { useState } from 'react'
import { api } from '../lib/api'

export default function History() {
  const [userId, setUserId] = useState('u1')
  const [rows, setRows] = useState([])
  const [error, setError] = useState('')

  const load = async () => {
    setError('')
    try {
      const { data } = await api.get(`/history/${userId}`)
      setRows(data)
    } catch (err) {
      setError(err?.response?.data?.detail || err.message)
    }
  }

  return (
    <div className="panel p-5 space-y-4">
      <h2 className="text-2xl font-semibold">Complaint History</h2>
      <div className="flex gap-3 max-w-xl">
        <input className="input-premium" value={userId} onChange={(e) => setUserId(e.target.value)} />
        <button className="btn-premium" onClick={load}>Load</button>
      </div>
      {error && <p className="text-rose-300">{error}</p>}
      <div className="grid grid-cols-2 gap-3">
        {rows.map((r, i) => (
          <div key={i} className="mini-card">
            <p className="text-slate-300">{r.category} · {r.location}</p>
            <p>{r.text}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
