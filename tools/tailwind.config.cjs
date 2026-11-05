/**
 * Tailwind CSS configuration (development only).
 * Matches the runtime config used in HTML CDN.
 * Used to compile static assets/tailwind.css for production.
 */
module.exports = {
  content: ['./*.html', './assets/js/*.js'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'secondary-container': '#fe9e74',
        'on-tertiary-fixed': '#111f05',
        'surface-container-low': '#f6f3ec',
        'tertiary': '#2e3e20',
        'outline': '#72796e',
        'on-tertiary-container': '#b6c9a0',
        'primary-fixed-dim': '#a1d494',
        'inverse-on-surface': '#f3f0e9',
        'background': '#fcf9f2',
        'surface-container-highest': '#e5e2db',
        'surface-tint': '#3b6934',
        'surface-dim': '#dcdad3',
        'secondary': '#944926',
        'surface-container-lowest': '#ffffff',
        'on-error': '#ffffff',
        'outline-variant': '#c2c9bb',
        'on-secondary-fixed': '#360f00',
        'on-primary-fixed': '#002201',
        'on-secondary-container': '#773311',
        'on-primary-fixed-variant': '#23501e',
        'surface': '#fcf9f2',
        'error': '#ba1a1a',
        'on-surface-variant': '#42493e',
        'inverse-primary': '#a1d494',
        'tertiary-container': '#455535',
        'on-primary-container': '#9dd090',
        'on-secondary': '#ffffff',
        'on-error-container': '#93000a',
        'surface-container': '#f1eee7',
        'tertiary-fixed': '#d6e9be',
        'error-container': '#ffdad6',
        'primary-fixed': '#bcf0ae',
        'on-primary': '#ffffff',
        'primary': '#154212',
        'on-tertiary-fixed-variant': '#3c4c2c',
        'on-background': '#1c1c18',
        'primary-container': '#2d5a27',
        'secondary-fixed-dim': '#ffb597',
        'secondary-fixed': '#ffdbcd',
        'tertiary-fixed-dim': '#bacda4',
        'on-surface': '#1c1c18',
        'on-tertiary': '#ffffff',
        'surface-bright': '#fcf9f2',
        'surface-variant': '#e5e2db',
        'surface-container-high': '#ebe8e1',
        'inverse-surface': '#31312c',
        'on-secondary-fixed-variant': '#763311'
      },
      borderRadius: {
        DEFAULT: '0.5rem',
        lg: '0.5rem',
        xl: '0.75rem',
        full: '9999px'
      },
      fontFamily: {
        headline: ['Noto Serif'],
        body: ['Manrope'],
        label: ['Manrope']
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/container-queries'),
  ],
}
