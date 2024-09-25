export default defineNuxtConfig({
  compatibilityDate: '2024-09-01',
  devtools: { enabled: false },
  modules: [
    '@pinia/nuxt',
  ],
  app: {
    head: {
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1',
      title: "24articles",
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/Screenshot_1.png' },
      ],
    }
  }
})