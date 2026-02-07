import { Link } from 'react-router-dom'
export default function NavBar(){
  return <nav className="glass p-4 flex gap-4 sticky top-2 z-20"><Link to="/">Home</Link><Link to="/chat">Chat</Link><Link to="/history">History</Link><Link to="/status">Status</Link><Link to="/admin">Admin</Link><Link to="/analytics">Analytics</Link></nav>
}
