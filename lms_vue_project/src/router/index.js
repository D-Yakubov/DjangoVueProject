import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '@/views/AboutView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LoginInView from '@/views/LoginInView.vue'
import MyAccountView from '@/views/dashboard/MyAccountView.vue'
import CoursesView from '@/views/CoursesView.vue'
import CourseView from '@/views/CourseView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'About',
    component: AboutView
  },
  {
    path: '/sign-up',
    name: 'SignUp',
    component: SignUpView
  },
  {
    path: '/log-in',
    name: 'LogIn',
    component: LoginInView
  },
  {
    path: '/dashboard/my-account',
    name: 'MyAccount',
    component: MyAccountView
  },
  {
    path: '/courses',
    name: 'Courses',
    component: CoursesView
  },
  {
    path: '/courses/:slug',
    name: 'Course',
    component: CourseView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
