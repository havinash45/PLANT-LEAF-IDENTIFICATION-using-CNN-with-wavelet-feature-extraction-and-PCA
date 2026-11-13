import { useState, useEffect, useCallback } from 'react'
import { Link } from 'react-router-dom'
import Navbar from '../components/Navbar'
import api from '../services/api'
import { Bar } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const LIMIT_OPTIONS = [5, 10, 25, 50]

const formatDate = (dateStr) => {
  if (!dateStr) return '—'
  const d = new Date(dateStr)
  return d.toLocaleString()
}

const AdminDashboard = () => {
  const [stats, setStats] = useState(null)
  const [recentUsers, setRecentUsers] = useState([])
  const [recentPredictions, setRecentPredictions] = useState([])
  const [loading, setLoading] = useState(true)
  const [usersLimit, setUsersLimit] = useState(10)
  const [predictionsLimit, setPredictionsLimit] = useState(10)
  const [verifyingId, setVerifyingId] = useState(null)

  const loadStats = useCallback(async () => {
    try {
      const res = await api.get('/api/admin/stats')
      setStats(res.data)
    } catch (err) {
      console.error('Failed to load stats:', err)
    } finally {
      setLoading(false)
    }
  }, [])

  const loadRecentUsers = useCallback(async () => {
    try {
      const res = await api.get('/api/admin/users', { params: { limit: usersLimit } })
      setRecentUsers(res.data)
    } catch (err) {
      console.error('Failed to load users:', err)
    }
  }, [usersLimit])

  const loadRecentPredictions = useCallback(async () => {
    try {
      const res = await api.get('/api/admin/predictions', { params: { limit: predictionsLimit } })
      setRecentPredictions(res.data)
    } catch (err) {
      console.error('Failed to load predictions:', err)
    }
  }, [predictionsLimit])

  useEffect(() => {
    loadStats()
  }, [loadStats])

  useEffect(() => {
    loadRecentUsers()
  }, [loadRecentUsers])

  useEffect(() => {
    loadRecentPredictions()
  }, [loadRecentPredictions])

  const handleVerify = async (predictionId) => {
    setVerifyingId(predictionId)
    try {
      await api.patch(`/api/admin/predictions/${predictionId}/verify`)
      await loadRecentPredictions()
      await loadStats()
    } catch (err) {
      console.error('Verify failed:', err)
    } finally {
      setVerifyingId(null)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <div className="container mx-auto px-4 py-8">
          <p>Loading...</p>
        </div>
      </div>
    )
  }

  const topPlants = stats?.topPlants || {}
  const chartData = {
    labels: Object.keys(topPlants).slice(0, 10),
    datasets: [
      {
        label: 'Number of Predictions',
        data: Object.values(topPlants).slice(0, 10),
        backgroundColor: '#2E7D32',
      },
    ],
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-text mb-8">Admin Dashboard</h1>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Link
            to="/admin/users"
            className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg hover:ring-2 hover:ring-primary/20 transition-all cursor-pointer block"
          >
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-sm font-medium text-gray-600 mb-2">Total Users</h3>
                <p className="text-3xl font-bold text-primary">{stats?.totalUsers ?? 0}</p>
              </div>
              <div className="p-2 bg-primary/10 rounded-full">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
              </div>
            </div>
            <p className="text-xs text-gray-500 mt-2">Click to manage users →</p>
          </Link>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-sm font-medium text-gray-600 mb-2">Total Predictions</h3>
                <p className="text-3xl font-bold text-primary">{stats?.totalPredictions ?? 0}</p>
              </div>
              <div className="p-2 bg-green-100 rounded-full">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
            </div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-sm font-medium text-gray-600 mb-2">Unverified Predictions</h3>
                <p className="text-3xl font-bold text-accent">{stats?.unverifiedPredictions ?? 0}</p>
              </div>
              <div className="p-2 bg-yellow-100 rounded-full">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Users - Dynamic */}
        <div className="bg-white p-6 rounded-lg shadow-md mb-8">
          <div className="flex flex-wrap items-center justify-between gap-4 mb-4">
            <h2 className="text-xl font-semibold text-text">Recent Users</h2>
            <div className="flex items-center gap-2">
              <label className="text-sm text-gray-600">Show:</label>
              <select
                value={usersLimit}
                onChange={(e) => setUsersLimit(Number(e.target.value))}
                className="border rounded px-2 py-1 text-sm"
              >
                {LIMIT_OPTIONS.map((n) => (
                  <option key={n} value={n}>{n}</option>
                ))}
              </select>
              <button
                type="button"
                onClick={loadRecentUsers}
                className="text-sm text-primary hover:underline"
              >
                Refresh
              </button>
            </div>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b text-left text-gray-600">
                  <th className="py-2 pr-4">Email</th>
                  <th className="py-2 pr-4">Name</th>
                  <th className="py-2 pr-4">Role</th>
                  <th className="py-2 pr-4">Joined</th>
                </tr>
              </thead>
              <tbody>
                {recentUsers.length === 0 ? (
                  <tr><td colSpan={4} className="py-4 text-gray-500 text-center">No users yet</td></tr>
                ) : (
                  recentUsers.map((u) => (
                    <tr key={u.id} className="border-b border-gray-100">
                      <td className="py-2 pr-4">{u.email}</td>
                      <td className="py-2 pr-4">{u.name}</td>
                      <td className="py-2 pr-4">{u.role}</td>
                      <td className="py-2 pr-4">{formatDate(u.createdAt)}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Recent Predictions - Dynamic */}
        <div className="bg-white p-6 rounded-lg shadow-md mb-8">
          <div className="flex flex-wrap items-center justify-between gap-4 mb-4">
            <h2 className="text-xl font-semibold text-text">Recent Predictions</h2>
            <div className="flex items-center gap-2">
              <label className="text-sm text-gray-600">Show:</label>
              <select
                value={predictionsLimit}
                onChange={(e) => setPredictionsLimit(Number(e.target.value))}
                className="border rounded px-2 py-1 text-sm"
              >
                {LIMIT_OPTIONS.map((n) => (
                  <option key={n} value={n}>{n}</option>
                ))}
              </select>
              <button
                type="button"
                onClick={loadRecentPredictions}
                className="text-sm text-primary hover:underline"
              >
                Refresh
              </button>
            </div>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b text-left text-gray-600">
                  <th className="py-2 pr-4">Plant</th>
                  <th className="py-2 pr-4">Confidence</th>
                  <th className="py-2 pr-4">Time</th>
                  <th className="py-2 pr-4">Status</th>
                  <th className="py-2 pr-4">Action</th>
                </tr>
              </thead>
              <tbody>
                {recentPredictions.length === 0 ? (
                  <tr><td colSpan={5} className="py-4 text-gray-500 text-center">No predictions yet</td></tr>
                ) : (
                  recentPredictions.map((p) => (
                    <tr key={p._id} className="border-b border-gray-100">
                      <td className="py-2 pr-4">{p.plantName || '—'}</td>
                      <td className="py-2 pr-4">{p.confidence != null ? `${(p.confidence * 100).toFixed(1)}%` : '—'}</td>
                      <td className="py-2 pr-4">{formatDate(p.timestamp)}</td>
                      <td className="py-2 pr-4">
                        {p.verified ? (
                          <span className="text-green-600">Verified</span>
                        ) : (
                          <span className="text-amber-600">Unverified</span>
                        )}
                      </td>
                      <td className="py-2 pr-4">
                        {!p.verified && (
                          <button
                            type="button"
                            disabled={verifyingId === p._id}
                            onClick={() => handleVerify(p._id)}
                            className="text-primary hover:underline disabled:opacity-50"
                          >
                            {verifyingId === p._id ? 'Verifying...' : 'Verify'}
                          </button>
                        )}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Top Plants Chart */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold text-text mb-4">Top 10 Identified Plants</h2>
          {Object.keys(topPlants).length > 0 ? (
            <Bar data={chartData} options={{
              responsive: true,
              plugins: {
                legend: { display: false },
              },
            }} />
          ) : (
            <p className="text-gray-500 text-center py-8">No data available</p>
          )}
        </div>
      </div>
    </div>
  )
}

export default AdminDashboard

