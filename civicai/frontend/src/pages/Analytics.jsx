import { useEffect, useState } from 'react'
import { api } from '../lib/api'

function AnalyticsPage() {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    api
      .get('/analytics')
      .then((res) => {
        setData(res.data)
        setError('')
      })
      .catch((err) => {
        setData(null)
        setError(err?.response?.data?.detail || 'Unable to load analytics')
      })
  }, [])

  return (
    <div className="panel p-5 space-y-3">
      <h2 className="text-2xl font-semibold">Analytics Control Center</h2>
      {!data && !error && <p className="text-slate-300">Connect backend to load analytics.</p>}
      {error && <p className="text-rose-300">{error}</p>}
      {data && (
        <div className="grid grid-cols-3 gap-3">
          <div className="mini-card">Total Complaints: {data.total_complaints}</div>
          <div className="mini-card">Total Tickets: {data.total_tickets}</div>
          <div className="mini-card">Open SLA: {data.sla_open}</div>
        </div>
      )}
    </div>
  )
}

export default AnalyticsPage
