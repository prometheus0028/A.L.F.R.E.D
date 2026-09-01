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
          primary: '#050706', 
          secondary: '#080A09', 
          tertiary: '#0B0D0C',
        },
        border: {
          DEFAULT: '#1c2420',
          subtle: '#111613',
        },
        text: {
          primary: '#f3f4f1', // warm off-white / ivory
          secondary: '#8a9490', // desaturated gray
          muted: '#5a6460', // darker desaturated gray
        },
        accent: {
          DEFAULT: '#65a30d', // muted terminal green
          hover: '#4d7c0f',
          amber: '#d97706', // warm beige / amber
        },
        status: {
          success: '#65a30d',
          warning: '#d97706',
          error: '#b91c1c', // muted red
          info: '#2563eb', // keeping a muted blue just in case
        }
      },
      fontFamily: {
        sans: ['Space Grotesk', 'system-ui', 'sans-serif'],
        mono: ['Space Mono', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', 'monospace'],
      },
      animation: {
        'spin-slow': 'spin 8s linear infinite',
      }
    },
  },
  plugins: [],
}
