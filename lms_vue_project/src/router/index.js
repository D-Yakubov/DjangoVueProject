import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import SignUpView from '../views/SignUpView.vue'
import LoginInView from '../views/LoginInView.vue'

import CoursesView from '../views/CoursesView.vue'
import CourseView from '../views/CourseView.vue'

import MyAccountView from '../views/dashboard/MyAccountView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
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
    path: '/courses',
    name: 'Courses',
    component: CoursesView
  },
  {
    path: '/courses/:slug',
    name: 'Course',
    component: CourseView
  },
  {
    path: '/dashboard/my-account',
    name: 'MyAccount',
    component: MyAccountView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
