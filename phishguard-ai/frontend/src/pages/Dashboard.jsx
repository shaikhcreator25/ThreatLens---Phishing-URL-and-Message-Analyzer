import { useState } from 'react'
import { AlertCircle, X } from 'lucide-react'
import Header from '../components/Header'
import InputSection from '../components/InputSection'
import ResultDashboard from '../components/ResultDashboard'
import ReasonsSection from '../components/ReasonsSection'
import Recommendation from '../components/Recommendation'
import { analyzeThreats } from '../services/api'

export default function Dashboard() {
  const [result, setResult] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleAnalyze = async (payload) => {
    setIsLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await analyzeThreats(payload)
      setResult(data)
    } catch (err) {
      setError(err.message || 'An unexpected error occurred. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen">
      {/* Ambient background */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-cyber-600/5 rounded-full blur-[120px]" />
        <div className="absolute bottom-0 left-0 w-[400px] h-[400px] bg-cyber-800/5 rounded-full blur-[100px]" />
      </div>

      <div className="relative z-10 max-w-2xl mx-auto px-4 pb-16">
        <Header />

        {/* Input */}
        <section className="mb-8">
          <InputSection onAnalyze={handleAnalyze} isLoading={isLoading} />
        </section>

        {/* Error */}
        {error && (
          <div className="mb-6 flex items-start gap-3 bg-red-500/10 border border-red-500/30 rounded-xl px-5 py-4">
            <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              <p className="text-sm text-red-300">{error}</p>
            </div>
            <button onClick={() => setError(null)} className="text-red-400 hover:text-red-300">
              <X className="w-4 h-4" />
            </button>
          </div>
        )}

        {/* Results */}
        {result && (
          <div className="space-y-5 animate-in fade-in">
            <ResultDashboard result={result} />
            <ReasonsSection reasons={result.reasons} classification={result.classification} />
            <Recommendation classification={result.classification} />
          </div>
        )}

        {/* Footer */}
        <footer className="mt-12 text-center text-xs text-dark-600">
          <p>ThreatLens &mdash; Hackathon MVP &bull; Defensive cybersecurity tool</p>
          <p className="mt-1">Analysis is heuristic-based. Always verify independently.</p>
        </footer>
      </div>
    </div>
  )
}
