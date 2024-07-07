// main.js/ts
import { createApp } from 'vue'
import { createBootstrap } from 'bootstrap-vue-next'
import App from './App.vue'
import { createI18n } from 'vue-i18n'

import router from './router'
// Add the necessary CSS
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css'

const i18n = createI18n({
    locale: 'fr',
    fallbackLocale: 'fr',
    messages: {
      en: {
        message: {
          hello: 'Hello'
        }
      },
      fr: {
        message: {
          hello: 'Bonjour'
        }
      }
    }
  })
const app = createApp(App)
app.use(createBootstrap()) // Important
app.use(router)
app.use(i18n)
app.mount('#app')