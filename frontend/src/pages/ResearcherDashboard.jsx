import { useState, useEffect } from 'react'
import Navbar from '../components/Navbar'
import api from '../services/api'

const ResearcherDashboard = () => {
  const [unverifiedPredictions, setUnverifiedPredictions] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadUnverifiedPredictions()
  }, [])

  const loadUnverifiedPredictions = async () => {
    try {
      // This endpoint would need to be implemented in the backend
      const response = await api.get('/api/researcher/unverified')
      setUnverifiedPredictions(response.data)
    } catch (error) {
      console.error('Failed to load unverified predictions:', error)
      // For now, show empty state
      setUnverifiedPredictions([])
    } finally {
      setLoading(false)
    }
  }

  const handleVerify = async (predictionId, correctPlantName) => {
    try {
      await api.post(`/api/researcher/verify/${predictionId}`, {
        correctPlantName,
      })
      loadUnverifiedPredictions()
      alert('Prediction verified successfully!')
    } catch (error) {
      console.error('Verification failed:', error)
      alert('Verification failed. Please try again.')
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-text mb-8">Researcher Portal</h1>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold text-text mb-4">
            Unverified Predictions
          </h2>

          {loading ? (
            <p className="text-center py-8">Loading...</p>
          ) : unverifiedPredictions.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {unverifiedPredictions.map((prediction) => (

                <div key={prediction._id} className="border border-gray-200 rounded-lg p-4 bg-white shadow-sm hover:shadow-md transition">
                  {/* Image and Basic Info */}
                  <div className="flex gap-4 mb-4">
                    <img
                      src={prediction.imageUrl.startsWith('http') ? prediction.imageUrl : `http://localhost:8081${prediction.imageUrl}`}
                      alt={prediction.plantName}
                      className="w-24 h-24 object-cover rounded-lg"
                    />
                    <div>
                      <h3 className="font-bold text-gray-800">{prediction.diseaseName}</h3>
                      <p className="text-sm text-gray-600">Leaf: {prediction.plantName}</p>
                      <p className="text-sm text-gray-500 mb-1">
                        Uploaded by: <span className="font-medium text-gray-700">{prediction.userId || 'Unknown User'}</span>
                      </p>
                      <span className={`text-xs px-2 py-1 rounded-full ${prediction.status === 'Healthy' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                        }`}>
                        {prediction.status}
                      </span>
                    </div>
                  </div>

                  {/* Confidence Bar */}
                  <div className="mb-4">
                    <div className="flex justify-between text-xs mb-1">
                      <span className="text-gray-500">Confidence: {prediction.confidenceLevel}</span>
                      <span className="font-semibold text-primary">{(prediction.confidence * 100).toFixed(1)}%</span>
                    </div>
                    <div className="w-full bg-gray-100 rounded-full h-1.5">
                      <div
                        className={`h-1.5 rounded-full ${prediction.confidence > 0.5 ? 'bg-primary' : 'bg-yellow-500'}`}
                        style={{ width: `${prediction.confidence * 100}%` }}
                      ></div>
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="mt-4 flex flex-col gap-2">
                    <button
                      onClick={() => handleVerify(prediction._id, null)}
                      className="w-full bg-green-600 text-white py-2 px-4 rounded hover:bg-green-700 transition text-sm flex items-center justify-center gap-2"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                      </svg>
                      Mark as Verified
                    </button>

                    <details className="w-full">
                      <summary className="list-none w-full bg-red-50 text-red-600 border border-red-200 py-2 px-4 rounded hover:bg-red-100 transition text-sm flex items-center justify-center gap-2 cursor-pointer">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                        Mark as Incorrect
                      </summary>
                      <div className="mt-2 p-2 bg-gray-50 rounded border border-gray-200">
                        <input
                          type="text"
                          placeholder="Enter correct label (e.g. Tomato___Early_blight)"
                          className="w-full px-3 py-2 border border-gray-300 rounded mb-2 text-sm focus:outline-none focus:border-primary"
                          id={`correct-${prediction._id}`}
                        />
                        <button
                          onClick={() => {
                            const input = document.getElementById(`correct-${prediction._id}`)
                            if (input.value) {
                              handleVerify(prediction._id, input.value)
                            } else {
                              alert("Please enter the correct label")
                            }
                          }}
                          className="w-full bg-red-600 text-white py-1.5 px-3 rounded hover:bg-red-700 transition text-xs"
                        >
                          Submit Correction
                        </button>
                      </div>
                    </details>
                  </div>
                </div>

              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-center py-8">
              No unverified predictions at the moment
            </p>
          )}
        </div>
      </div>
    </div>
  )
}

export default ResearcherDashboard

