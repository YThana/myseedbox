import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// vite-plugin-vue-devtools is currently disabled: its @vue/babel-plugin-jsx
// dependency imports `isHTMLTag`/`isSVGTag` from 'vue', which neither the
// stable (3.5.39) nor beta (3.6.0-beta.17) published builds export.
// Re-enable once upstream publishes a fix.
// import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
})
