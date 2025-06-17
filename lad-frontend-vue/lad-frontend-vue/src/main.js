import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router' // On importe notre routeur

const app = createApp(App)

app.use(createPinia()) // On active Pinia (gestion d'état)
app.use(router)      // On active le Router

app.mount('#app')