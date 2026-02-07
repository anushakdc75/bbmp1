import { Link, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import NavBar from './NavBar'

const sideLinks = [
  ['/', '⌘', 'Home'],
  ['/chat', '💬', 'Chat'],
  ['/status', '📍', 'Status'],
  ['/analytics', '📊', 'Analytics'],
  ['/admin', '🛠', 'Admin'],
]

export default function DesktopShell({ children }) {
  const location = useLocation()

  return (
    <div className="min-h-screen desktop-bg text-slate-100 p-6">
      <div className="max-w-[1700px] mx-auto grid grid-cols-[92px_1fr] gap-5">
        <aside className="glass-premium p-3 flex flex-col items-center gap-3">
          {sideLinks.map(([to, icon, label]) => {
            const active = location.pathname === to
            return (
              <Link
                key={to}
                to={to}
                title={label}
                className={`w-14 h-14 rounded-2xl flex items-center justify-center text-xl transition-all ${
                  active ? 'bg-white/20 shadow-glow scale-105' : 'bg-white/5 hover:bg-white/15'
                }`}
              >
                {icon}
              </Link>
            )
          })}
        </aside>
        <div className="space-y-5">
          <NavBar />
          <motion.section
            key={location.pathname}
            initial={{ opacity: 0, scale: 0.98, y: 8 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            transition={{ duration: 0.25 }}
            className="glass-premium p-5 min-h-[78vh]"
          >
            {children}
          </motion.section>
        </div>
      </div>
    </div>
  )
}
