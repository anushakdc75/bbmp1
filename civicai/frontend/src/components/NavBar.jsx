import { NavLink } from 'react-router-dom'

const links = [
  ['/', 'Dashboard'],
  ['/chat', 'AI Chat'],
  ['/history', 'History'],
  ['/status', 'Tracker'],
  ['/admin', 'Admin'],
  ['/analytics', 'Analytics'],
]

export default function NavBar() {
  return (
    <header className="glass-premium h-16 px-6 flex items-center justify-between">
      <div>
        <p className="text-xs uppercase tracking-[0.25em] text-slate-300/80">CivicAI</p>
        <h1 className="text-lg font-semibold">Smart Grievance Platform</h1>
      </div>
      <nav className="flex items-center gap-2">
        {links.map(([to, label]) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `px-4 py-2 rounded-xl text-sm transition-all ${
                isActive
                  ? 'bg-white/20 text-white shadow-glow'
                  : 'text-slate-300 hover:text-white hover:bg-white/10'
              }`
            }
          >
            {label}
          </NavLink>
        ))}
      </nav>
    </header>
  )
import { Link } from 'react-router-dom'
export default function NavBar(){
  return <nav className="glass p-4 flex gap-4 sticky top-2 z-20"><Link to="/">Home</Link><Link to="/chat">Chat</Link><Link to="/history">History</Link><Link to="/status">Status</Link><Link to="/admin">Admin</Link><Link to="/analytics">Analytics</Link></nav>
}
