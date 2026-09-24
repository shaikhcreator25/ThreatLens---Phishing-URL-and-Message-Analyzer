import { useState } from 'react'
import { Search, Trash2, Zap, MessageSquare, Link2 } from 'lucide-react'

const DEMOS = [
  {
    label: 'Phishing',
    message: 'URGENT! Your bank account will be suspended today. Verify your account immediately using the link below.',
    url: 'http://192.168.1.50/login/verify-account',
  },
  {
    label: 'Suspicious',
    message: 'Your account requires verification. Please review your information using the link provided.',
    url: 'http://secure-account-verification.example.com/login',
  },
  {
    label: 'Safe',
    message: 'Hey, are we still meeting at 5 PM today?',
    url: '',
  },
]

export default function InputSection({ onAnalyze, isLoading }) {
  const [message, setMessage] = useState('')
  const [url, setUrl] = useState('')

  const handleAnalyze = () => {
    if (!message.trim() && !url.trim()) return
    onAnalyze({ message: message.trim(), url: url.trim() })
  }

  const handleClear = () => {
    setMessage('')
    setUrl('')
  }

  const handleDemo = (demo) => {
    setMessage(demo.message)
    setUrl(demo.url)
  }

  const hasInput = message.trim() || url.trim()

  return (
    <div className="space-y-5">
      {/* Message Input Card */}
      <div className="glass-card p-6">
        <label className="flex items-center gap-2 text-sm font-semibold text-gray-300 mb-3 uppercase tracking-wider">
          <MessageSquare className="w-4 h-4 text-cyber-400" />
          Suspicious Message
        </label>
        <textarea
          id="message-input"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Paste the suspicious message here..."
          rows={4}
          maxLength={10000}
          className="w-full bg-dark-950/60 border border-dark-700 rounded-xl px-4 py-3 text-gray-200 placeholder-dark-500 resize-none transition-all duration-200 text-sm leading-relaxed"
        />
      </div>

      {/* URL Input Card */}
      <div className="glass-card p-6">
        <label className="flex items-center gap-2 text-sm font-semibold text-gray-300 mb-3 uppercase tracking-wider">
          <Link2 className="w-4 h-4 text-cyber-400" />
          Suspicious URL
        </label>
        <input
          id="url-input"
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://example.com/..."
          maxLength={2048}
          className="w-full bg-dark-950/60 border border-dark-700 rounded-xl px-4 py-3 text-gray-200 placeholder-dark-500 transition-all duration-200 text-sm font-mono"
        />
      </div>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-3">
        <button
          id="analyze-btn"
          onClick={handleAnalyze}
          disabled={isLoading || !hasInput}
          className="flex-1 flex items-center justify-center gap-2 bg-gradient-to-r from-cyber-600 to-cyber-700 hover:from-cyber-500 hover:to-cyber-600 disabled:from-dark-700 disabled:to-dark-700 disabled:text-dark-500 text-white font-semibold py-3.5 px-6 rounded-xl transition-all duration-200 shadow-lg shadow-cyber-900/30 disabled:shadow-none"
        >
          {isLoading ? (
            <>
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              Analyzing threat...
            </>
          ) : (
            <>
              <Search className="w-5 h-5" />
              Analyze Threat
            </>
          )}
        </button>

        <button
          id="clear-btn"
          onClick={handleClear}
          disabled={isLoading}
          className="flex items-center justify-center gap-2 bg-dark-800 hover:bg-dark-700 text-gray-400 hover:text-gray-200 font-medium py-3.5 px-6 rounded-xl transition-all duration-200 border border-dark-700"
        >
          <Trash2 className="w-4 h-4" />
          Clear
        </button>
      </div>

      {/* Demo Buttons */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3">
        <span className="text-xs font-medium text-dark-500 uppercase tracking-wider flex items-center gap-1.5">
          <Zap className="w-3.5 h-3.5" />
          Try Demo
        </span>
        <div className="flex flex-wrap gap-2">
          {DEMOS.map((demo) => (
            <button
              key={demo.label}
              onClick={() => handleDemo(demo)}
              disabled={isLoading}
              className={`text-xs font-medium px-3.5 py-1.5 rounded-lg border transition-all duration-200 ${
                demo.label === 'Phishing'
                  ? 'border-red-500/30 text-red-400 hover:bg-red-500/10'
                  : demo.label === 'Suspicious'
                  ? 'border-amber-500/30 text-amber-400 hover:bg-amber-500/10'
                  : 'border-emerald-500/30 text-emerald-400 hover:bg-emerald-500/10'
              } disabled:opacity-50`}
            >
              {demo.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
