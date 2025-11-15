import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { quasar, transformAssetUrls } from '@quasar/vite-plugin'
import { fileURLToPath } from 'node:url'

export default defineConfig({
  plugins: [
    vue({
      template: { transformAssetUrls }
    }),
    quasar({
      sassVariables: fileURLToPath(new URL('./src/quasar-variables.sass', import.meta.url))
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 5173,
    host: 'localhost',
    open: true,
    // Hot Module Replacement (HMR) configuration
    hmr: {
      host: 'localhost',
      port: 5173,
      protocol: 'ws'
    }
  }
})
