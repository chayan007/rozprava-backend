import { createRouter, createWebHistory } from 'vue-router'
import SignUp from '../components/SignUp.vue'
import Register from '../views/Register.vue'
import SplashScreen from '../views/SplashScreen.vue'
import Login from '../views/Login.vue'

const routes = [
  {
    path: '/signup',
    name: 'SignUp',
    component: SignUp
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/splashscreen',
    name: 'SplashScreen',
    component: SplashScreen
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router