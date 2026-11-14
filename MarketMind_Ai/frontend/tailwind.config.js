/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        obsidian: "#071B17",
        "deep-emerald": "#0E3B32",
        "forest-surface": "#123B30",
        "emerald-accent": "#42E6A4",
        "champagne-gold": "#D9B978",
        "warm-ivory": "#F4F0E6",
        "muted-emerald": "#A8B9B0",
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'pulse-emerald': 'pulseEmerald 3s ease-in-out infinite',
        'spin-slow': 'spin 20s linear infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        pulseEmerald: {
          '0%, 100%': { opacity: '0.7', filter: 'drop-shadow(0 0 15px rgba(66, 230, 164, 0.4))' },
          '50%': { opacity: '1', filter: 'drop-shadow(0 0 25px rgba(66, 230, 164, 0.8))' },
        },
      }
    },
  },
  plugins: [],
}
