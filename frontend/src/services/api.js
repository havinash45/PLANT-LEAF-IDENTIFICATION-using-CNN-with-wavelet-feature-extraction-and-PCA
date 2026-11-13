import axios from 'axios'

const api = axios.create({
  // Backend is configured to run on port 8081 (see FastAPI uvicorn config / .env)
  baseURL: 'http://localhost:8081',
  headers: {
    'Content-Type': 'application/json',
  },
})

export default api

