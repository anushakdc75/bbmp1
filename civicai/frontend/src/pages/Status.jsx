import { useState } from 'react'
import { api } from '../lib/api'

export default function Status() {
  const [ticket, setTicket] = useState('')
  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const lookup = async () => {
    const id = ticket.trim()
    if (!id || loading) return
    setError('')
    setLoading(true)
    try {
      const res = await api.get(`/status/${id}`)
      setData(res.data)
    } catch (err) {
      setData(null)
      const detail = err?.response?.data?.detail || err.message
      setError(`Lookup failed: ${detail}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="grid grid-cols-[0.9fr_1.1fr] gap-5 h-full">
      <section className="panel p-5 space-y-4">
        <h2 className="text-2xl font-semibold">Status Tracking</h2>
        <p className="text-slate-300">Enter tracking ID (e.g., CIV-XXXXXXXXXX) to see authority, timeline logs, and escalation stage.</p>
        <div className="flex gap-3">
          <input value={ticket} onChange={(e) => setTicket(e.target.value.toUpperCase())} className="input-premium" placeholder="CIV-XXXXXXXXXX" />
          <button onClick={lookup} disabled={loading} className="btn-premium disabled:opacity-60">{loading ? 'Checking...' : 'Track'}</button>
        </div>
        {error && <p className="text-rose-300 text-sm">{error}</p>}
      </section>

      <section className="panel p-5">
        <h3 className="text-lg font-semibold mb-3">Ticket Timeline</h3>
        {!data && <p className="text-slate-300">No ticket loaded yet.</p>}
        {data && (
          <div className="space-y-3">
            <div className="mini-card"><b>{data.tracking_id}</b> · <span>{data.status}</span> · <span>{data.authority}</span></div>
            <div className="space-y-2">
              {(data.logs || []).map((log, idx) => (
                <div key={idx} className="mini-card">{idx + 1}. {log}</div>
              ))}
            </div>
          </div>
        )}
      </section>
    </div>
  )
}
export default function Status(){ return <div className="glass p-4">Status tracker page</div> }
