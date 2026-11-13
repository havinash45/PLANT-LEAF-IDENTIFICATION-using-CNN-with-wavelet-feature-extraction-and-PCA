import { createContext, useState, useContext, useEffect } from 'react'
import api from '../services/api'

const AuthContext = createContext()

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('token')
    const userData = localStorage.getItem('user')
    
    if (token && userData) {
      try {
        setUser(JSON.parse(userData))
        api.defaults.headers.common['Authorization'] = `Bearer ${token}`
      } catch (e) {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
      }
    }
    setLoading(false)
  }, [])

  const login = async (email, password) => {
    try {
      const response = await api.post('/api/auth/login', { email, password })
      const { token, email: userEmail, name, role } = response.data
      
      localStorage.setItem('token', token)
      localStorage.setItem('user', JSON.stringify({ email: userEmail, name, role }))
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`
      
      setUser({ email: userEmail, name, role })
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data?.message || 'Login failed' }
    }
  }

  const register = async (name, email, password, role = 'USER') => {
    try {
      const response = await api.post('/api/auth/register', { name, email, password, role })
      const { token, email: userEmail, name: userName, role: userRole } = response.data
      
      localStorage.setItem('token', token)
      localStorage.setItem('user', JSON.stringify({ email: userEmail, name: userName, role: userRole }))
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`
      
      setUser({ email: userEmail, name: userName, role: userRole })
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data?.message || 'Registration failed' }
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    delete api.defaults.headers.common['Authorization']
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, login, register, logout, loading }}>
      {children}
    </AuthContext.Provider>
  )
}

