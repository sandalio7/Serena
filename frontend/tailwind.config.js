/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          500: '#0ea5e9', // Azul principal
          600: '#0284c7',
          700: '#0369a1',
        },
        secondary: {
          500: '#14b8a6', // Verde/Turquesa 
          600: '#0d9488',
          700: '#0f766e',
        },
        danger: {
          500: '#ef4444', // Rojo para gastos
          600: '#dc2626',
        },
        success: {
          500: '#10b981', // Verde para ingresos
          600: '#059669',
        },
        warning: {
          500: '#f59e0b', // Amarillo para alertas
          600: '#d97706',
        }
      }
    },
  },
  plugins: [],
}