import { useEffect, useState } from 'react'
import { api } from '../lib/api'

export default function Analytics() {
  const [data, setData] = useState(null)

  useEffect(() => {
    api.get('/analytics').then((res) => setData(res.data)).catch(() => setData(null))
  }, [])

  return (
    <div className="panel p-5 space-y-3">
      <h2 className="text-2xl font-semibold">Analytics Control Center</h2>
      {!data && <p className="text-slate-300">Connect backend to load analytics.</p>}
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
export default function Analytics(){ return <div className="glass p-4">Analytics charts placeholder</div> }
