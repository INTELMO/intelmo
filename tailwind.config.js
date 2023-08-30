/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "intelmo/templates/**/*.html",
    "intelmo/static/src/**/*.js",
    'docs/**/*.{html,js,vue,ts,md}',
    'docs/.vitepress/**/*.{html,js,vue,ts,md}',
  ],
  theme: {
    extend: {},
  },
  plugins: [
      require('@tailwindcss/forms'),
      require('@tailwindcss/typography'),
  ],
}
