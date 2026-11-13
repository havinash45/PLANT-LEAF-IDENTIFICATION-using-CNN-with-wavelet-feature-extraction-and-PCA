import { useState, useEffect, useCallback } from 'react'
import { Link } from 'react-router-dom'
import Navbar from '../components/Navbar'
import api from '../services/api'

const PAGE_SIZES = [5, 10, 20, 50]
const ROLES = ['USER', 'ADMIN', 'RESEARCHER']

const formatDate = (dateStr) => {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleString()
}

const AdminUsersPage = () => {
  const [users, setUsers] = useState([])
  const [totalElements, setTotalElements] = useState(0)
  const [totalPages, setTotalPages] = useState(0)
  const [currentPage, setCurrentPage] = useState(0)
  const [size, setSize] = useState(10)
  const [roleFilter, setRoleFilter] = useState('')
  const [loading, setLoading] = useState(true)
  const [updatingId, setUpdatingId] = useState(null)
  const [message, setMessage] = useState({ type: '', text: '' })

  const loadUsers = useCallback(async () => {
    setLoading(true)
    try {
      const params = { page: currentPage, size }
      if (roleFilter) params.role = roleFilter
      const res = await api.get('/api/admin/users/page', { params })
      setUsers(res.data.content || [])
      setTotalElements(res.data.totalElements ?? 0)
      setTotalPages(res.data.totalPages ?? 0)
    } catch (err) {
      console.error('Failed to load users:', err)
      setMessage({ type: 'error', text: 'Failed to load users' })
    } finally {
      setLoading(false)
    }
  }, [currentPage, size, roleFilter])

  useEffect(() => {
    loadUsers()
  }, [loadUsers])

  useEffect(() => {
    setCurrentPage(0)
  }, [roleFilter, size])

  const handleRoleChange = async (userId, newRole) => {
    setUpdatingId(userId)
    setMessage({ type: '', text: '' })
    try {
      await api.patch(`/api/admin/users/${userId}/role`, { role: newRole })
      await loadUsers()
      setMessage({ type: 'success', text: 'Role updated successfully' })
      setTimeout(() => setMessage({ type: '', text: '' }), 3000)
    } catch (err) {
      console.error('Failed to update role:', err)
      setMessage({ type: 'error', text: err.response?.data?.message || 'Failed to update role' })
    } finally {
      setUpdatingId(null)
    }
  }

  const hasPrev = currentPage > 0
  const hasNext = currentPage < totalPages - 1
  const startItem = totalElements === 0 ? 0 : currentPage * size + 1
  const endItem = Math.min((currentPage + 1) * size, totalElements)

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
          <div className="flex items-center gap-3">
            <Link
              to="/admin"
              className="text-gray-600 hover:text-primary transition-colors"
              aria-label="Back to dashboard"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
            </Link>
            <h1 className="text-3xl font-bold text-text">Manage Users</h1>
          </div>
        </div>

        {message.text && (
          <div
            className={`mb-4 px-4 py-2 rounded-lg ${
              message.type === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
            }`}
          >
            {message.text}
          </div>
        )}

        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="p-4 border-b border-gray-200 flex flex-wrap items-center gap-4">
            <label className="flex items-center gap-2 text-sm text-gray-600">
              Role:
              <select
                value={roleFilter}
                onChange={(e) => setRoleFilter(e.target.value)}
                className="border rounded px-2 py-1.5 text-sm"
              >
                <option value="">All</option>
                {ROLES.map((r) => (
                  <option key={r} value={r}>{r}</option>
                ))}
              </select>
            </label>
            <label className="flex items-center gap-2 text-sm text-gray-600">
              Per page:
              <select
                value={size}
                onChange={(e) => setSize(Number(e.target.value))}
                className="border rounded px-2 py-1.5 text-sm"
              >
                {PAGE_SIZES.map((n) => (
                  <option key={n} value={n}>{n}</option>
                ))}
              </select>
            </label>
            <button
              type="button"
              onClick={() => loadUsers()}
              className="text-sm text-primary hover:underline"
            >
              Refresh
            </button>
            <span className="text-sm text-gray-500 ml-auto">
              {totalElements} user{totalElements !== 1 ? 's' : ''} total
            </span>
          </div>

          <div className="overflow-x-auto">
            {loading ? (
              <div className="p-8 text-center text-gray-500">Loading users...</div>
            ) : (
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-gray-50 text-left text-gray-600">
                    <th className="py-3 px-4 font-medium">Email</th>
                    <th className="py-3 px-4 font-medium">Name</th>
                    <th className="py-3 px-4 font-medium">Role</th>
                    <th className="py-3 px-4 font-medium">Joined</th>
                    <th className="py-3 px-4 font-medium">Last login</th>
                    <th className="py-3 px-4 font-medium">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {users.length === 0 ? (
                    <tr>
                      <td colSpan={6} className="py-8 text-center text-gray-500">
                        No users found
                      </td>
                    </tr>
                  ) : (
                    users.map((u) => (
                      <tr key={u.id} className="border-t border-gray-100 hover:bg-gray-50/50">
                        <td className="py-3 px-4">{u.email}</td>
                        <td className="py-3 px-4">{u.name || '—'}</td>
                        <td className="py-3 px-4">
                          <span
                            className={`inline-flex px-2 py-0.5 rounded text-xs font-medium ${
                              u.role === 'ADMIN'
                                ? 'bg-purple-100 text-purple-800'
                                : u.role === 'RESEARCHER'
                                ? 'bg-blue-100 text-blue-800'
                                : 'bg-gray-100 text-gray-800'
                            }`}
                          >
                            {u.role}
                          </span>
                        </td>
                        <td className="py-3 px-4">{formatDate(u.createdAt)}</td>
                        <td className="py-3 px-4">{formatDate(u.lastLogin)}</td>
                        <td className="py-3 px-4">
                          <select
                            value={u.role}
                            onChange={(e) => handleRoleChange(u.id, e.target.value)}
                            disabled={updatingId === u.id}
                            className="border rounded px-2 py-1 text-xs disabled:opacity-50"
                          >
                            {ROLES.map((r) => (
                              <option key={r} value={r}>{r}</option>
                            ))}
                          </select>
                          {updatingId === u.id && (
                            <span className="ml-2 text-xs text-gray-500">Updating...</span>
                          )}
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            )}
          </div>

          {totalPages > 1 && (
            <div className="p-4 border-t border-gray-200 flex flex-wrap items-center justify-between gap-4">
              <span className="text-sm text-gray-600">
                Showing {startItem}–{endItem} of {totalElements}
              </span>
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setCurrentPage((p) => Math.max(0, p - 1))}
                  disabled={!hasPrev}
                  className="px-3 py-1.5 text-sm border rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
                >
                  Previous
                </button>
                <span className="text-sm text-gray-600">
                  Page {currentPage + 1} of {totalPages}
                </span>
                <button
                  type="button"
                  onClick={() => setCurrentPage((p) => Math.min(totalPages - 1, p + 1))}
                  disabled={!hasNext}
                  className="px-3 py-1.5 text-sm border rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
                >
                  Next
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default AdminUsersPage
