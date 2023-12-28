import { createRouter, createWebHistory } from 'vue-router';
import MainPage from './components/MainPage.vue';
import Register from './components/Register.vue';
import Login from './components/Login.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: MainPage },
    { path: '/register', component: Register },
    { path: '/login', component: Login },
  ],
});

export default router;