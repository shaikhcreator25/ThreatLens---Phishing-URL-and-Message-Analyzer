import { AlertTriangle, Info } from 'lucide-react'

export default function ReasonsSection({ reasons, classification }) {
  if (!reasons || reasons.length === 0) return null

  const isPhishing = classification === 'PHISHING'
  const isSuspicious = classification === 'SUSPICIOUS'

  const iconColor = isPhishing
    ? 'text-red-400'
    : isSuspicious
    ? 'text-amber-400'
    : 'text-emerald-400'

  const borderColor = isPhishing
    ? 'border-red-500/20'
    : isSuspicious
    ? 'border-amber-500/20'
    : 'border-emerald-500/20'

  const bgColor = isPhishing
    ? 'bg-red-500/5'
    : isSuspicious
    ? 'bg-amber-500/5'
    : 'bg-emerald-500/5'

  return (
    <div className="glass-card p-6">
      <h3 className="flex items-center gap-2 text-sm font-semibold text-gray-300 mb-4 uppercase tracking-wider">
        <Info className="w-4 h-4 text-cyber-400" />
        Why was this flagged?
      </h3>

      <div className="space-y-2.5">
        {reasons.map((reason, index) => (
          <div
            key={index}
            className={`flex items-start gap-3 ${bgColor} border ${borderColor} rounded-xl px-4 py-3 transition-all duration-200`}
          >
            <AlertTriangle className={`w-4 h-4 ${iconColor} flex-shrink-0 mt-0.5`} />
            <span className="text-sm text-gray-300 leading-relaxed">{reason}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
