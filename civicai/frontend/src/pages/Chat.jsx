import { useState } from 'react'
import { motion } from 'framer-motion'
import { api } from '../lib/api'

export default function Chat(){
  const [message,setMessage]=useState('')
  const [items,setItems]=useState([])
  const send=async()=>{
    if(!message) return
    const {data}=await api.post('/chat',{user_id:'u1',message,location:'ward 12'})
    setItems(v=>[...v,{q:message,a:data.reply,meta:data}]);setMessage('')
  }
  return <div className="glass p-4"><h2 className="text-xl mb-3">Chat</h2><div className="space-y-3">{items.map((it,i)=><motion.div key={i} initial={{opacity:0,x:20}} animate={{opacity:1,x:0}}><div className="text-cyan-300">You: {it.q}</div><div className="text-slate-100 whitespace-pre-line">Bot: {it.a}</div></motion.div>)}</div><div className="flex gap-2 mt-4"><input value={message} onChange={e=>setMessage(e.target.value)} className="flex-1 rounded bg-slate-900 p-2" placeholder="Describe complaint..."/><button onClick={send} className="bg-indigo-500 px-4 rounded">Send</button></div></div>
}
