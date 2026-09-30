/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cream: {
          main: '#FAF6F0',
          card: '#FFFFFF',
          panel: '#F3E9DD',
        },
        wood: {
          primary: '#8B5E3C',
          secondary: '#5C3D2E',
          border: '#E4D6C3',
          text: '#3B2C22',
          muted: '#8C7B6E',
        }
      }
    },
  },
  plugins: [],
}