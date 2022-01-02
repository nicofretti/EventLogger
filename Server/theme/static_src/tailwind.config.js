module.exports = {
    content: [
        '../templates/**/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',
    ],
    theme: {
        extend: {
            colors:{
                transparent: 'transparent',
                current: 'currentColor',
                'th-primary': '#3F90F0',
                'th-card': '#1C1C1C',
                'th-background': '#0A090B',
                'th-label': '#C4C4C4'
            }
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
