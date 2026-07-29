/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        forest: {
          50: '#f2f9f5',
          100: '#e1f2e8',
          200: '#c5e5d3',
          300: '#99cfb4',
          400: '#64b28e',
          500: '#3d9470',
          600: '#2d7759',
          700: '#265f49',
          800: '#214c3b',
          900: '#1b4332',
          950: '#0d261c',
        },
        earth: {
          50: '#fbfaf5',
          100: '#f4f1de',
          200: '#e9edc9',
          300: '#faedcd',
          400: '#d4a373',
          500: '#bc6c25',
          600: '#9b531a',
        }
      },
      fontFamily: {
        sans: ['Outfit', 'Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
