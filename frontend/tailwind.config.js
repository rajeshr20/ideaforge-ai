/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        navy: { DEFAULT: "#1B2A4A", light: "#2D4070" },
        brand: {
          teal:   "#0F6E56",
          amber:  "#BA7517",
          coral:  "#993C1D",
          purple: "#534AB7",
        }
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
    }
  },
  plugins: [],
}
