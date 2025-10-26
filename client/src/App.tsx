function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-center text-gray-900 mb-8">
          DocuMind AI
        </h1>
        <p className="text-center text-gray-600">
          Your intelligent document knowledge assistant
        </p>
        <div className="mt-8 text-center">
          <p className="text-sm text-gray-500">
            API will be available at: <code className="bg-gray-100 px-2 py-1 rounded">{import.meta.env.VITE_API_URL || 'http://localhost:8000'}</code>
          </p>
        </div>
      </div>
    </div>
  )
}

export default App

