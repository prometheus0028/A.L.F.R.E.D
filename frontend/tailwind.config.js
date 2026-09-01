/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        surface: {
          primary: '#ffffff',
          secondary: '#f8fafc', // slate-50
          tertiary: '#f1f5f9', // slate-100
        },
        border: {
          DEFAULT: '#e2e8f0', // slate-200
        },
        text: {
          primary: '#0f172a', // slate-900
          secondary: '#475569', // slate-600
          muted: '#94a3b8', // slate-400
        },
        accent: {
          DEFAULT: '#0284c7', // sky-600
          hover: '#0369a1', // sky-700
        },
        status: {
          success: '#16a34a', // green-600
          warning: '#d97706', // amber-600
          error: '#dc2626', // red-600
          info: '#2563eb', // blue-600
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
