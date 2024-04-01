module.exports = {
  purge: ['./src/**/*.{html,svelte}', './src/**/*.{js,ts}'],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {},
  },
  variants: {},
  plugins: [require('daisyui')],
};