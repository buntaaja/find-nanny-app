import { createApp, markRaw } from 'vue';
import { createPinia } from 'pinia'
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router';
import MainPage from './components/MainPage.vue';
import Register from './components/Register.vue';
import Login from './components/Login.vue';


const routes = [
  { path: '/', component: MainPage },
  { path: '/register', component: Register },
  { path: '/login', component: Login },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

const pinia = createPinia() 

pinia.use(({ store }) => { store.router = markRaw(router) })


createApp(App).use(router).use(pinia).mount('#app');