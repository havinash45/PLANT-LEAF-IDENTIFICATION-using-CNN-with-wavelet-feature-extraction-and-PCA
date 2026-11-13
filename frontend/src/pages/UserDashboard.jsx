import { useState, useEffect } from 'react'
import Navbar from '../components/Navbar'
import api from '../services/api'

const UserDashboard = () => {
  const [selectedImage, setSelectedImage] = useState(null)
  const [selectedImages, setSelectedImages] = useState([])
  const [preview, setPreview] = useState(null)
  const [previews, setPreviews] = useState([])
  const [prediction, setPrediction] = useState(null)
  const [batchPredictions, setBatchPredictions] = useState([])
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(false)
  const [batchLoading, setBatchLoading] = useState(false)
  const [uploadMode, setUploadMode] = useState('single') // 'single' or 'batch'
  const [selectedHistoryItem, setSelectedHistoryItem] = useState(null)

  useEffect(() => {
    loadHistory()
  }, [])

  const loadHistory = async () => {
    try {
      const response = await api.get('/api/predict/history')
      setHistory(response.data)
    } catch (error) {
      console.error('Failed to load history:', error)
    }
  }

  const handleImageSelect = (e) => {
    const file = e.target.files[0]
    if (file) {
      setSelectedImage(file)
      setPreview(URL.createObjectURL(file))
      setPrediction(null)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    const file = e.dataTransfer.files[0]
    if (file && file.type.startsWith('image/')) {
      setSelectedImage(file)
      setPreview(URL.createObjectURL(file))
      setPrediction(null)
    }
  }

  const handleDragOver = (e) => {
    e.preventDefault()
  }

  const handleBatchImageSelect = (e) => {
    const files = Array.from(e.target.files)
    if (files.length > 0) {
      // Limit to 30 images
      if (files.length > 30) {
        alert(`You selected ${files.length} images. Only the first 30 will be processed.`)
      }
      const limitedFiles = files.slice(0, 30)
      setSelectedImages(limitedFiles)

      // Create previews
      const newPreviews = limitedFiles.map(file => ({
        file,
        preview: URL.createObjectURL(file)
      }))
      setPreviews(newPreviews)
      setBatchPredictions([])
    }
  }

  const handlePredict = async () => {
    if (!selectedImage) return

    setLoading(true)
    try {
      const formData = new FormData()
      formData.append('image', selectedImage)

      const response = await api.post('/api/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      setPrediction(response.data)
      loadHistory()
    } catch (error) {
      console.error('Prediction failed:', error)
      alert('Prediction failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleBatchPredict = async () => {
    if (selectedImages.length === 0) return

    setBatchLoading(true)
    try {
      const formData = new FormData()
      selectedImages.forEach((file) => {
        formData.append('images', file)
      })

      const response = await api.post('/api/predict/batch', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      setBatchPredictions(response.data)
      loadHistory()
    } catch (error) {
      console.error('Batch prediction failed:', error)
      alert('Batch prediction failed. Please try again.')
    } finally {
      setBatchLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-text mb-8">Plant & Leaf Identification</h1>

        {/* Mode Toggle */}
        <div className="mb-6 flex gap-4">
          <button
            onClick={() => {
              setUploadMode('single')
              setSelectedImage(null)
              setSelectedImages([])
              setPreview(null)
              setPreviews([])
              setPrediction(null)
              setBatchPredictions([])
            }}
            className={`px-6 py-2 rounded-lg transition ${uploadMode === 'single'
              ? 'bg-primary text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
          >
            Single Image
          </button>
          <button
            onClick={() => {
              setUploadMode('batch')
              setSelectedImage(null)
              setSelectedImages([])
              setPreview(null)
              setPreviews([])
              setPrediction(null)
              setBatchPredictions([])
            }}
            className={`px-6 py-2 rounded-lg transition ${uploadMode === 'batch'
              ? 'bg-primary text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
          >
            Batch Upload (20-30 images)
          </button>
        </div>

        {uploadMode === 'single' ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Upload Section */}
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h2 className="text-xl font-semibold text-text mb-4">Upload Plant/Leaf Image</h2>
              <p className="text-sm text-gray-600 mb-4">
                Upload a plant leaf image for identification (species or disease)
              </p>

              <div className="mb-4">
                <input
                  type="file"
                  accept="image/*"
                  capture="environment"
                  onChange={handleImageSelect}
                  id="single-image-upload"
                  className="hidden"
                />
                <label
                  htmlFor="single-image-upload"
                  onDrop={handleDrop}
                  onDragOver={handleDragOver}
                  className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-primary rounded-lg cursor-pointer bg-secondary/10 hover:bg-secondary/20 transition"
                >
                  <div className="flex flex-col items-center justify-center pt-5 pb-6">
                    <svg className="w-10 h-10 mb-3 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                    <p className="mb-2 text-sm text-text">
                      <span className="font-semibold">Click to upload</span> or drag and drop
                    </p>
                    <p className="text-xs text-gray-500">PNG, JPG, JPEG (MAX. 10MB)</p>
                    <p className="text-xs text-primary mt-1">📷 Camera supported on mobile</p>
                  </div>
                </label>
              </div>

              {preview && (
                <div className="mb-4">
                  <img
                    src={preview}
                    alt="Preview"
                    className="w-full h-64 object-cover rounded-lg"
                  />
                </div>
              )}

              <button
                onClick={handlePredict}
                disabled={!selectedImage || loading}
                className="w-full bg-primary text-white py-2 px-4 rounded-lg hover:bg-green-700 transition disabled:opacity-50"
              >
                {loading ? 'Identifying...' : 'Identify Plant'}
              </button>
            </div>

            {/* Result Section */}
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h2 className="text-xl font-semibold text-text mb-4">Identification Result</h2>

              {prediction ? (
                <div className="space-y-4">
                  {/* Warning for low confidence */}
                  {prediction.confidence < 0.3 && (
                    <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-4">
                      <div className="flex">
                        <div className="flex-shrink-0">
                          <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                          </svg>
                        </div>
                        <div className="ml-3">
                          <p className="text-sm text-red-700">
                            Low prediction reliability. Please re-upload a clear image.
                          </p>
                        </div>
                      </div>
                    </div>
                  )}

                  <div className="flex justify-between items-start">
                    <div>
                      <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">Leaf</p>
                      <h3 className="text-lg font-bold text-gray-800">{prediction.plantName}</h3>
                    </div>
                    {/* Status Badge */}
                    <span
                      className={`px-3 py-1 rounded-full text-sm font-semibold ${prediction.status === 'Healthy'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                        }`}
                    >
                      {prediction.status}
                    </span>
                  </div>

                  <div>
                    <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">Disease Name</p>
                    <h3 className="text-2xl font-bold text-primary">{prediction.diseaseName}</h3>
                  </div>

                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium">Confidence: {prediction.confidenceLevel}</span>
                      <span className="text-lg font-bold text-primary">
                        {(prediction.confidence * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full transition-all ${prediction.confidence >= 0.5 ? 'bg-primary' : 'bg-yellow-500'
                          }`}
                        style={{ width: `${prediction.confidence * 100}%` }}
                      ></div>
                    </div>
                  </div>

                  {/* Pesticides Section */}
                  {prediction.status !== 'Healthy' && (
                    <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                      <h4 className="font-semibold text-gray-800 mb-2 flex items-center">
                        <svg className="w-5 h-5 mr-2 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                        </svg>
                        Recommended Pesticides
                      </h4>
                      {prediction.pesticides && prediction.pesticides.length > 0 ? (
                        <ul className="list-disc list-inside text-gray-700 space-y-1 ml-1">
                          {prediction.pesticides.map((pesticide, index) => (
                            <li key={index}>{pesticide}</li>
                          ))}
                        </ul>
                      ) : (
                        <p className="text-sm text-gray-500 italic">No specific recommendations available.</p>
                      )}
                    </div>
                  )}

                  {prediction.status === 'Healthy' && (
                    <div className="bg-green-50 p-4 rounded-lg border border-green-200">
                      <p className="text-green-800 font-medium">No pesticides required.</p>
                    </div>
                  )}

                  {prediction.scientificName && (
                    <div>
                      <span className="text-sm font-medium">Scientific Name: </span>
                      <span className="text-sm text-gray-600 italic">{prediction.scientificName}</span>
                    </div>
                  )}

                  {prediction.description && (
                    <div className="mt-2">
                      <p className="text-sm text-gray-600">{prediction.description}</p>
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-gray-500 text-center py-8">Upload an image to get started</p>
              )}
            </div>
          </div>
        ) : (
          /* Batch Upload Mode */
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h2 className="text-xl font-semibold text-text mb-4">Batch Upload (20-30 Images)</h2>

              <div className="mb-4">
                <input
                  type="file"
                  accept="image/*"
                  multiple
                  onChange={handleBatchImageSelect}
                  className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-primary file:text-white hover:file:bg-green-700"
                />
                <p className="text-sm text-gray-500 mt-2">
                  Selected: {selectedImages.length} images (Max 30)
                </p>
              </div>

              {previews.length > 0 && (
                <div className="mb-4">
                  <p className="text-sm font-medium mb-2">Image Previews ({previews.length}):</p>
                  <div className="grid grid-cols-4 md:grid-cols-6 lg:grid-cols-8 gap-2 max-h-64 overflow-y-auto">
                    {previews.map((item, index) => (
                      <img
                        key={index}
                        src={item.preview}
                        alt={`Preview ${index + 1}`}
                        className="w-full h-20 object-cover rounded border border-gray-200"
                      />
                    ))}
                  </div>
                </div>
              )}

              <button
                onClick={handleBatchPredict}
                disabled={selectedImages.length === 0 || batchLoading}
                className="w-full bg-primary text-white py-2 px-4 rounded-lg hover:bg-green-700 transition disabled:opacity-50"
              >
                {batchLoading ? `Processing ${selectedImages.length} images...` : `Identify ${selectedImages.length} Images`}
              </button>
            </div>

            {/* Batch Results */}
            {batchPredictions.length > 0 && (
              <div className="bg-white p-6 rounded-lg shadow-md">
                <h2 className="text-xl font-semibold text-text mb-4">
                  Batch Results ({batchPredictions.length} predictions)
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                  {batchPredictions.map((pred, index) => (
                    <div key={pred.predictionId || index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition">
                      <img
                        src={`http://localhost:8081${pred.imageUrl}`}
                        alt={pred.plantName}
                        className="w-full h-32 object-cover rounded mb-2"
                      />
                      <h3 className="font-bold text-primary text-lg">{pred.plantName}</h3>
                      {pred.scientificName && (
                        <p className="text-xs text-gray-500 italic mb-2">{pred.scientificName}</p>
                      )}
                      <div className="mb-2">
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-xs font-medium">Confidence</span>
                          <span className="text-sm font-bold text-primary">
                            {(pred.confidence * 100).toFixed(1)}%
                          </span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-1.5">
                          <div
                            className="bg-primary h-1.5 rounded-full transition-all"
                            style={{ width: `${pred.confidence * 100}%` }}
                          ></div>
                        </div>
                      </div>
                      {pred.leafType && (
                        <p className="text-xs text-gray-600">
                          <span className="font-medium">Type:</span> {pred.leafType}
                        </p>
                      )}
                      {pred.region && (
                        <p className="text-xs text-gray-600">
                          <span className="font-medium">Region:</span> {pred.region}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* History Section */}
        <div className="mt-8 bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold text-text mb-4">Prediction History</h2>

          {history.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {history.map((item) => (
                <div
                  key={item.id}
                  className="border border-gray-200 rounded-lg p-4 cursor-pointer hover:shadow-lg transition"
                  onClick={() => setSelectedHistoryItem(item)}
                >
                  <img
                    src={item.imageUrl.startsWith('http') ? item.imageUrl : `http://localhost:8081${item.imageUrl}`}
                    alt={item.plantName}
                    className="w-full h-32 object-cover rounded mb-2"
                  />
                  <h3 className="font-semibold">{item.plantName}</h3>
                  <p className="text-sm text-gray-600">
                    {(item.confidence * 100).toFixed(1)}% confidence
                  </p>
                  <p className="text-xs text-gray-500 mt-1">
                    {new Date(item.timestamp).toLocaleString()}
                  </p>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-center py-4">No prediction history yet</p>
          )}
        </div>
      </div>

      {/* History Item Modal */}
      {selectedHistoryItem && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50 backdrop-blur-sm">
          <div className="bg-white rounded-xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto relative animate-fadeIn">
            <button
              onClick={() => setSelectedHistoryItem(null)}
              className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition p-2 rounded-full hover:bg-gray-100"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>

            <div className="p-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-6 border-b pb-2">Prediction Details</h2>

              <div className="mb-6 bg-gray-50 rounded-lg overflow-hidden border border-gray-100">
                <img
                  src={selectedHistoryItem.imageUrl.startsWith('http') ? selectedHistoryItem.imageUrl : `http://localhost:8081${selectedHistoryItem.imageUrl}`}
                  alt={selectedHistoryItem.plantName}
                  className="w-full h-80 object-contain mx-auto"
                />
              </div>

              <div className="space-y-6">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-1">Identified Plant</p>
                    <h3 className="text-2xl font-bold text-gray-900">{selectedHistoryItem.plantName}</h3>
                  </div>
                  <span
                    className={`px-4 py-1.5 rounded-full text-sm font-bold shadow-sm ${selectedHistoryItem.status === 'Healthy'
                      ? 'bg-green-100 text-green-800 border border-green-200'
                      : 'bg-red-100 text-red-800 border border-red-200'
                      }`}
                  >
                    {selectedHistoryItem.status}
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="bg-blue-50 p-4 rounded-xl border border-blue-100">
                    <p className="text-xs font-bold text-blue-600 uppercase tracking-wider mb-1">Problem / Disease</p>
                    <p className="text-lg font-semibold text-gray-900">{selectedHistoryItem.diseaseName || 'None'}</p>
                  </div>

                  <div className="bg-purple-50 p-4 rounded-xl border border-purple-100">
                    <div className="flex justify-between items-center mb-1">
                      <p className="text-xs font-bold text-purple-600 uppercase tracking-wider">Confidence Score</p>
                      <span className="text-sm font-bold text-purple-700">
                        {(selectedHistoryItem.confidence * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div className="w-full bg-white rounded-full h-2.5 overflow-hidden border border-purple-100">
                      <div
                        className={`h-full rounded-full transition-all duration-1000 ${selectedHistoryItem.confidence >= 0.5 ? 'bg-purple-600' : 'bg-yellow-500'
                          }`}
                        style={{ width: `${selectedHistoryItem.confidence * 100}%` }}
                      ></div>
                    </div>
                    <p className="text-xs text-gray-500 mt-2 text-right">{selectedHistoryItem.confidenceLevel}</p>
                  </div>
                </div>

                {selectedHistoryItem.status !== 'Healthy' && (
                  <div className="bg-amber-50 p-5 rounded-xl border border-amber-200 shadow-sm">
                    <h4 className="font-bold text-amber-900 mb-3 flex items-center text-lg">
                      <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                      </svg>
                      Recommended Actions
                    </h4>
                    {selectedHistoryItem.pesticides && selectedHistoryItem.pesticides.length > 0 ? (
                      <ul className="space-y-2">
                        {selectedHistoryItem.pesticides.map((pesticide, index) => (
                          <li key={index} className="flex items-start text-amber-800 bg-white bg-opacity-60 p-2 rounded-lg">
                            <svg className="w-5 h-5 mr-2 text-amber-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                            </svg>
                            <span>{pesticide}</span>
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-sm text-amber-800 italic bg-white bg-opacity-50 p-3 rounded-lg">No specific pesticide recommendations available currently. Consult a local expert.</p>
                    )}
                  </div>
                )}

                {selectedHistoryItem.description && (
                  <div className="bg-gray-50 p-4 rounded-xl border border-gray-200 text-sm leading-relaxed text-gray-700">
                    <p className="font-semibold text-gray-900 mb-1">Description:</p>
                    {selectedHistoryItem.description}
                  </div>
                )}

                <div className="text-center pt-2 border-t mt-4">
                  <p className="text-xs text-gray-400">
                    Analysis ID: {selectedHistoryItem.id} • Verified: {selectedHistoryItem.verified ? 'Yes' : 'No'} • Date: {new Date(selectedHistoryItem.timestamp).toLocaleString()}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default UserDashboard

