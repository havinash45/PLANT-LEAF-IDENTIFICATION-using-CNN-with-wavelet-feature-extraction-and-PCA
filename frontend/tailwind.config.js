/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#2E7D32',
        secondary: '#A5D6A7',
        accent: '#FBC02D',
        background: '#F5F7F6',
        text: '#263238',
      },
    },
  },
  plugins: [],
}

