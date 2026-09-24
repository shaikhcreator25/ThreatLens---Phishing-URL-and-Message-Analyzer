import { ShieldCheck, ShieldAlert, ShieldX, MessageSquare, Link2 } from 'lucide-react'

const CONFIG = {
  SAFE: {
    icon: ShieldCheck,
    label: 'SAFE',
    subtitle: 'NO STRONG THREATS DETECTED',
    color: 'text-emerald-400',
    bg: 'bg-emerald-500/10',
    border: 'border-emerald-500/30',
    glow: 'glow-safe',
    stroke: 'stroke-emerald-400',
    track: 'stroke-emerald-900/40',
  },
  SUSPICIOUS: {
    icon: ShieldAlert,
    label: 'SUSPICIOUS',
    subtitle: 'SUSPICIOUS ACTIVITY DETECTED',
    color: 'text-amber-400',
    bg: 'bg-amber-500/10',
    border: 'border-amber-500/30',
    glow: 'glow-suspicious',
    stroke: 'stroke-amber-400',
    track: 'stroke-amber-900/40',
  },
  PHISHING: {
    icon: ShieldX,
    label: 'PHISHING',
    subtitle: 'PHISHING INDICATORS DETECTED',
    color: 'text-red-400',
    bg: 'bg-red-500/10',
    border: 'border-red-500/30',
    glow: 'glow-phishing',
    stroke: 'stroke-red-400',
    track: 'stroke-red-900/40',
  },
}

function RiskMeter({ score, size = 120, strokeWidth = 8, config }) {
  const radius = (size - strokeWidth) / 2
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (score / 100) * circumference

  return (
    <div className="relative inline-flex items-center justify-center">
      <svg width={size} height={size} className="-rotate-90">
        {/* Track */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          strokeWidth={strokeWidth}
          className={config.track}
        />
        {/* Progress */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          className={`${config.stroke} risk-meter-circle`}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          style={{ '--target-offset': offset }}
        />
      </svg>
      <div className="absolute flex flex-col items-center">
        <span className={`text-3xl font-bold ${config.color}`}>{score}</span>
        <span className="text-[10px] text-dark-400 font-medium uppercase tracking-wider">/100</span>
      </div>
    </div>
  )
}

function SubScore({ icon: Icon, label, score, config }) {
  const pct = `${score}%`
  return (
    <div className="flex items-center gap-3">
      <Icon className={`w-4 h-4 ${config.color} flex-shrink-0`} />
      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between mb-1">
          <span className="text-xs font-medium text-gray-400">{label}</span>
          <span className={`text-xs font-bold ${config.color}`}>{score}/100</span>
        </div>
        <div className={`h-1.5 rounded-full ${config.track}`}>
          <div
            className={`h-1.5 rounded-full ${config.stroke.replace('stroke', 'bg')} transition-all duration-1000 ease-out`}
            style={{ width: pct }}
          />
        </div>
      </div>
    </div>
  )
}

export default function ResultDashboard({ result }) {
  if (!result) return null

  const config = CONFIG[result.classification] || CONFIG.SAFE
  const ClassIcon = config.icon

  return (
    <div className={`glass-card ${config.glow} overflow-hidden`}>
      {/* Classification Header */}
      <div className={`${config.bg} border-b ${config.border} px-6 py-5`}>
        <div className="flex items-center justify-center gap-3">
          <ClassIcon className={`w-7 h-7 ${config.color}`} strokeWidth={2.5} />
          <div className="text-center">
            <h2 className={`text-xl font-bold ${config.color} tracking-wide`}>
              {config.subtitle}
            </h2>
            <span className={`text-xs font-mono font-semibold ${config.color} opacity-70 uppercase tracking-widest`}>
              Classification: {config.label}
            </span>
          </div>
        </div>
      </div>

      {/* Scores */}
      <div className="p-6">
        <div className="flex flex-col md:flex-row items-center gap-8">
          {/* Main Risk Meter */}
          <div className="flex flex-col items-center gap-2">
            <span className="text-xs font-semibold text-dark-400 uppercase tracking-widest">
              Risk Score
            </span>
            <RiskMeter score={result.risk_score} config={config} />
          </div>

          {/* Sub Scores */}
          <div className="flex-1 w-full space-y-4">
            <SubScore
              icon={MessageSquare}
              label="Message Risk"
              score={result.message_score}
              config={config}
            />
            <SubScore
              icon={Link2}
              label="URL Risk"
              score={result.url_score}
              config={config}
            />
          </div>
        </div>
      </div>
      
      {/* Disclaimer */}
      <div className="px-6 py-3 border-t border-white/5 bg-black/20 text-center">
        <p className="text-[10px] text-gray-500 uppercase tracking-wide opacity-80">
          Results are based on available URL, message, and reputation signals. A low-risk result does not guarantee that a URL is safe.
        </p>
      </div>
    </div>
  )
}
