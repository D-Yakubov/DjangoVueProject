import { createApp } from 'vue'
import axios from 'axios'
import App from './App.vue'
import router from './router'
import store from './store'

axios.defaults.baseURL = process.env.VUE_APP_API_URL || 'http://127.0.0.1:8000/api/v1/'

store.commit('initializeStore')

createApp(App).use(store).use(router).mount('#app')
