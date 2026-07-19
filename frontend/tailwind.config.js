/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        peach: {
          50: '#fff9f6',
          100: '#ffede5',
          200: '#ffd6c7',
          300: '#ffb399',
          400: '#ff8a65',
          500: '#f4511e',
          600: '#e64a19',
          700: '#d84315',
          900: '#4a1b0c',
        },
        brand: {
          50: '#fff5f0',
          100: '#ffe8df',
          500: '#ff7043',
          600: '#f4511e',
          700: '#d84315',
        }
      },
    },
  },
  plugins: [],
}
