import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import SignupView from '../views/SignupView.vue'
import LoginView from '../views/LoginView.vue'
import CourseListView from '../views/CourseListView.vue'
import CourseDetailView from '../views/CourseDetailView.vue'
import AuthorCoursesView from '../views/AuthorCoursesView.vue'
import MyAccountView from '../views/dashboard/MyAccountView.vue'
import CreateCourseView from '../views/dashboard/CreateCourseView.vue'

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
    component: SignupView
  },
  {
    path: '/log-in',
    name: 'LogIn',
    component: LoginView
  },
  {
    path: '/courses',
    name: 'Courses',
    component: CourseListView
  },
  {
    path: '/courses/:slug',
    name: 'Course',
    component: CourseDetailView
  },
  {
    path: '/authors/:id',
    name: 'Author',
    component: AuthorCoursesView
  },
  {
    path: '/dashboard/my-account',
    name: 'MyAccount',
    component: MyAccountView,
    meta: { requireLogin: true }
  },
  {
    path: '/dashboard/create-course',
    name: 'CreateCourse',
    component: CreateCourseView,
    meta: { requireLogin: true }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireLogin) && !store.state.user.isAuthenticated) {
    next({ name: 'LogIn' })
  } else {
    next()
  }
})

export default router
