import { Shield, Activity } from 'lucide-react'

export default function Header() {
  return (
    <header className="relative pt-10 pb-8 text-center">
      {/* Background glow */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[300px] bg-cyber-600/10 rounded-full blur-[100px]" />
      </div>

      <div className="relative z-10">
        {/* Logo */}
        <div className="flex items-center justify-center gap-3 mb-4">
          <div className="relative">
            <div className="absolute inset-0 bg-cyber-500 blur-lg opacity-30 rounded-full" />
            <div className="relative bg-gradient-to-br from-cyber-500 to-cyber-700 p-3 rounded-2xl">
              <Shield className="w-8 h-8 text-white" strokeWidth={2.5} />
            </div>
          </div>
          <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight">
            <span className="bg-gradient-to-r from-cyber-400 to-cyber-600 bg-clip-text text-transparent">
              THREATLENS
            </span>
          </h1>
        </div>

        {/* Tagline */}
        <div className="flex items-center justify-center gap-2 text-dark-400 text-sm mb-2">
          <Activity className="w-4 h-4" />
          <span className="font-medium uppercase tracking-widest text-xs">
            Phishing Link &amp; Message Analyzer
          </span>
        </div>

        <p className="text-dark-300 text-base max-w-lg mx-auto">
          Analyze suspicious messages and URLs before you click.
        </p>
      </div>
    </header>
  )
}
