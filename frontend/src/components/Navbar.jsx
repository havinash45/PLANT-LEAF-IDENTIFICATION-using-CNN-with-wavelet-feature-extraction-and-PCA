import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const Navbar = () => {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="bg-primary text-white shadow-lg">
      <div className="container mx-auto px-4 py-3">
        <div className="flex items-center justify-between">
          <Link to="/dashboard" className="text-xl font-bold">
            🌿 LeafAI Hub
          </Link>
          <div className="flex items-center gap-4">
            <span className="text-sm">Welcome, {user?.name}</span>
            {user?.role === 'ADMIN' && (
              <Link to="/admin" className="hover:underline">Admin</Link>
            )}
            {user?.role === 'RESEARCHER' && (
              <Link to="/researcher" className="hover:underline">Researcher</Link>
            )}
            <button
              onClick={handleLogout}
              className="bg-accent text-text px-4 py-2 rounded hover:bg-yellow-400 transition"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar

