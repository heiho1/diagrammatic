import { createApp } from 'vue'
import { Quasar, Dark } from 'quasar'
import '@quasar/extras/material-icons/material-icons.css'
import '@quasar/extras/roboto-font/roboto-font.css'
import 'quasar/dist/quasar.css'

import App from './App.vue'

const app = createApp(App)

app.use(Quasar, {
  config: {
    brand: {
      primary: '#1976d2',
      secondary: '#26a69a',
      accent: '#9c27b0'
    },
    dark: false,
    notify: {
      position: 'top-right',
      timeout: 2500
    }
  }
})

app.mount('#app')
