import { BrowserRouter, Routes, Route } from 'react-router-dom'
import NavBar from './components/NavBar'
import Landing from './pages/Landing'
import Chat from './pages/Chat'
import History from './pages/History'
import Status from './pages/Status'
import Admin from './pages/Admin'
import Analytics from './pages/Analytics'

export default function App(){
  return <BrowserRouter><main className="max-w-5xl mx-auto p-4 space-y-4"><NavBar/><Routes><Route path='/' element={<Landing/>}/><Route path='/chat' element={<Chat/>}/><Route path='/history' element={<History/>}/><Route path='/status' element={<Status/>}/><Route path='/admin' element={<Admin/>}/><Route path='/analytics' element={<Analytics/>}/></Routes></main></BrowserRouter>
}
