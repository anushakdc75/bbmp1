import { motion } from 'framer-motion'

export default function Landing() {
  return (
    <div className="grid grid-cols-[1.2fr_0.8fr] gap-5 h-full">
      <motion.section initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="panel p-8">
        <p className="uppercase tracking-[0.2em] text-sm text-indigo-200">Desktop-First Premium Glass UI</p>
        <h2 className="text-5xl font-semibold mt-4 leading-tight">CivicAI Control Center for Predict, Escalate, and Resolve.</h2>
        <p className="mt-4 text-slate-300 max-w-3xl">A macOS-inspired civic-tech experience with floating glass windows, AI-assisted grievance triage, and level-based escalation tracking.</p>
      </motion.section>
      <section className="panel p-6 grid gap-3 content-start">
        <div className="mini-card">⌨️ Keyboard shortcuts ready</div>
        <div className="mini-card">🧩 Multi-panel workspace layout</div>
        <div className="mini-card">✨ Aurora gradient + depth shadows</div>
        <div className="mini-card">🛰 Real-time status timeline</div>
      </section>
    </div>
  )
export default function Landing(){
  return <motion.div initial={{opacity:0,y:20}} animate={{opacity:1,y:0}} className="glass p-8 text-center"><h1 className="text-4xl font-bold">CivicAI</h1><p className="mt-3">Smart grievance platform with Level-1 auto resolution and Level-2 escalation.</p></motion.div>
}
