import { useState } from 'react'
import { motion } from 'framer-motion'
import { api } from '../lib/api'

export default function Chat() {
  const [message, setMessage] = useState('')
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const send = async () => {
    const payload = message.trim()
    if (!payload || loading) return

    setError('')
    setLoading(true)
    try {
      const { data } = await api.post('/chat', { user_id: 'u1', message: payload, location: 'ward 12' })
      setItems((v) => [...v, { q: payload, a: data.reply, meta: data }])
      setMessage('')
    } catch (err) {
      const detail = err?.response?.data?.detail || err.message || 'Unable to reach backend API.'
      setError(`Send failed: ${detail}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="h-full grid grid-cols-[1.3fr_0.7fr] gap-5">
      <section className="panel p-5 flex flex-col">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-semibold">AI Chat Workspace</h2>
          <span className="text-xs text-slate-300">⌘+Enter to send</span>
        </div>
        <div className="flex-1 overflow-auto space-y-4 pr-2">
          {items.length === 0 && <p className="text-slate-300">Start with a grievance query (water, road, garbage, drainage...).</p>}
          {items.map((it, i) => (
            <motion.div key={i} initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="space-y-2">
              <div className="bubble-user">{it.q}</div>
              <div className="bubble-bot whitespace-pre-line">{it.a}</div>
            </motion.div>
          ))}
        </div>
        {error && <p className="text-rose-300 text-sm mt-3">{error}</p>}
        <div className="mt-4 flex gap-3">
          <input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) send()
            }}
            className="input-premium"
            placeholder="Describe complaint + location context"
          />
          <button onClick={send} disabled={loading} className="btn-premium disabled:opacity-60">
            {loading ? 'Sending...' : 'Send'}
          </button>
        </div>
      </section>

      <aside className="panel p-5 space-y-3">
        <h3 className="text-lg font-semibold">Live Guidance</h3>
        <p className="text-sm text-slate-300">Level-1: AI suggests department + solution. Low confidence auto-escalates to Level-2 ticket.</p>
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div className="mini-card"><p className="text-slate-300">Mode</p><p>Hybrid TF-IDF + Heuristic</p></div>
          <div className="mini-card"><p className="text-slate-300">Priority</p><p>Desktop Premium</p></div>
          <div className="mini-card"><p className="text-slate-300">Theme</p><p>Aurora Glass</p></div>
          <div className="mini-card"><p className="text-slate-300">Latency</p><p>&lt; 600ms target</p></div>
        </div>
      </aside>
    </div>
  )
}
