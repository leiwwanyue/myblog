import { createApp } from 'vue'
import App from './App.vue'
import LoginWithSMS from './components/LoginWithSMS.vue';
import axios from 'axios';

// 设置 Axios 基础 URL
axios.defaults.baseURL = 'http://localhost:8080';

createApp(App)
.component('LoginWithSMS', LoginWithSMS)
.mount('#app');
