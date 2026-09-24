import { ShieldCheck, ShieldAlert, ShieldX } from 'lucide-react'

const RECOMMENDATIONS = {
  SAFE: {
    icon: ShieldCheck,
    title: 'Low Risk',
    text: 'No major phishing indicators were detected. Continue to verify the source before sharing sensitive information.',
    color: 'text-emerald-400',
    bg: 'bg-emerald-500/5',
    border: 'border-emerald-500/20',
  },
  SUSPICIOUS: {
    icon: ShieldAlert,
    title: 'Exercise Caution',
    text: 'Proceed with caution. Verify the sender and destination independently before clicking or sharing information.',
    color: 'text-amber-400',
    bg: 'bg-amber-500/5',
    border: 'border-amber-500/20',
  },
  PHISHING: {
    icon: ShieldX,
    title: 'High Risk — Take Action',
    text: 'Do not click the link or provide passwords, OTPs, payment information, or other sensitive data.',
    color: 'text-red-400',
    bg: 'bg-red-500/5',
    border: 'border-red-500/20',
  },
}

export default function Recommendation({ classification }) {
  const rec = RECOMMENDATIONS[classification]
  if (!rec) return null

  const Icon = rec.icon

  return (
    <div className={`glass-card ${rec.bg} border ${rec.border} p-6`}>
      <div className="flex items-start gap-4">
        <div className={`p-2.5 rounded-xl ${rec.bg} border ${rec.border}`}>
          <Icon className={`w-6 h-6 ${rec.color}`} />
        </div>
        <div>
          <h3 className={`text-sm font-bold ${rec.color} uppercase tracking-wider mb-1.5`}>
            Recommendation: {rec.title}
          </h3>
          <p className="text-sm text-gray-400 leading-relaxed">
            {rec.text}
          </p>
        </div>
      </div>
    </div>
  )
}
