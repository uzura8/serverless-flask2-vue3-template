// For Amplify to work in the browser, it needs to be able to access the global window object.
//window.global = window

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import i18n from './i18n'
import filters from './filters'

import FontAwesomeIcon from './fontawesome'

import './assets/main.css'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(i18n)

app.component('FontAwesomeIcon', FontAwesomeIcon)

// Register filters
declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $filters: Record<string, (value: any, ...args: any[]) => any>
  }
}
app.config.globalProperties.$filters = filters

app.mount('#app')
