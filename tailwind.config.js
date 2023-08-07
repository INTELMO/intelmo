/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "intelmo/templates/**/*.html",
    "intelmo/static/src/**/*.js"
  ],
  theme: {
    extend: {},
  },
  plugins: [
      require('@tailwindcss/forms'),
      require('@tailwindcss/typography'),
  ],
}
