module.exports = {
    content: [
        '../templates/**/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',
    ],
    theme: {
        colors:{
            transparent: 'transparent',
            current: 'currentColor',
            'th-primary': '#3F90F0',
            'th-card': '#1C1C1C',
            'th-background': '#0A090B',
            'th-text': '#ffffff',
            'th-label': '#7A7A7A'
        },
        extend: {},
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
