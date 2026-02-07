import { motion } from 'framer-motion'
export default function Landing(){
  return <motion.div initial={{opacity:0,y:20}} animate={{opacity:1,y:0}} className="glass p-8 text-center"><h1 className="text-4xl font-bold">CivicAI</h1><p className="mt-3">Smart grievance platform with Level-1 auto resolution and Level-2 escalation.</p></motion.div>
}
