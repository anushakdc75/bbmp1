import { BrowserRouter, Routes, Route } from 'react-router-dom'
import DesktopShell from './components/DesktopShell'
import Landing from './pages/Landing'
import Chat from './pages/Chat'
import History from './pages/History'
import Status from './pages/Status'
import Admin from './pages/Admin'
import Analytics from './pages/Analytics'

export default function App() {
  return (
    <BrowserRouter>
      <DesktopShell>
        <Routes>
          <Route path='/' element={<Landing />} />
          <Route path='/chat' element={<Chat />} />
          <Route path='/history' element={<History />} />
          <Route path='/status' element={<Status />} />
          <Route path='/admin' element={<Admin />} />
          <Route path='/analytics' element={<Analytics />} />
        </Routes>
      </DesktopShell>
    </BrowserRouter>
  )
}
