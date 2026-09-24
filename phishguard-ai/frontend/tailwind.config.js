/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cyber: {
          50:  '#eef7ff',
          100: '#d9edff',
          200: '#bce0ff',
          300: '#8ecdff',
          400: '#59b0ff',
          500: '#3490ff',
          600: '#1a6ff5',
          700: '#1459e1',
          800: '#1749b6',
          900: '#19408f',
          950: '#142857',
        },
        dark: {
          50:  '#f4f6f7',
          100: '#e3e7ea',
          200: '#c9d1d7',
          300: '#a4b0ba',
          400: '#778795',
          500: '#5c6c7a',
          600: '#4f5b68',
          700: '#444e57',
          800: '#3d444b',
          900: '#1a1f25',
          950: '#0d1117',
        },
        threat: {
          safe:       '#10b981',
          safeBg:     '#064e36',
          suspicious: '#f59e0b',
          suspBg:     '#78350f',
          phishing:   '#ef4444',
          phishBg:    '#7f1d1d',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'scan': 'scan 2s ease-in-out infinite',
      },
      keyframes: {
        scan: {
          '0%, 100%': { opacity: 0.4 },
          '50%': { opacity: 1 },
        },
      },
    },
  },
  plugins: [],
}
