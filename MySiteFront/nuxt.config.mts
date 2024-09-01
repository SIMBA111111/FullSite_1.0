// https://nuxt.com/docs/api/configuration/nuxt-config
import ckeditor5 from '@ckeditor/vite-plugin-ckeditor5'

export default defineNuxtConfig({
  compatibilityDate: '2024-09-01',
  devtools: { enabled: true },
  vite: {
    plugins: [ckeditor5({ theme: require.resolve( '@ckeditor/ckeditor5-theme-lark' ) })]
  }
})