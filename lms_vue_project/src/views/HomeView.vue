<template>
  <div class="home">
    <div class="hero is-info is-medium">
      <div class="hero-body has-text-centered">
        <h1 class="title">TheMWE.tech ga Xush kelibsiz!</h1>

        <h2 class="subtitle">
          <strong>The Modern World Education</strong> - zamonaviy dunyo kasblarini o'rganish uchun online platforma!
        </h2>
      </div>
    </div>

    <section class="section">
      <div class="container">
        <div class="columns is-multiline">
          <div class="column is-4">
            <div class="box has-text-centered">
              <span class="icon is-size-2 has-text-info"><i class="far fa-clock"></i></span>

              <h2 class="is-size-4 mt-4 mb-4">O'zingizning tezlikda o'rganing!</h2>

              <p>Platformamizdagi darslar 24/7 holatda siz uchun ochiq! Agar sizga darslar murakkablik qilsa qayta va qayta o'rganib ularni tushunib olishingiz mumkin.</p>
            </div>
          </div>

          <div class="column is-4">
            <div class="box has-text-centered">
              <span class="icon is-size-2 has-text-info"><i class="far fa-comments"></i></span>

              <h2 class="is-size-4 mt-4 mb-4">Boshqalar bilan birga o'rganing!</h2>

              <p>Har bir dars tugallangandan keyin izohlar orqali boshqalar bilan muloqot qilishingiz mumkin va savollaringiz bo'lsa yozib qoldirishingiz mumkin.</p>
            </div>
          </div>

          <div class="column is-4">
            <div class="box has-text-centered">
              <span class="icon is-size-2 has-text-info"><i class="fas fa-home"></i></span>

              <h2 class="is-size-4 mt-4 mb-4">Uyingizdan chiqmasdan ta'lim oling.</h2>

              <p>Uyingizdan chiqmasdan platformadagi darslarni o'rganib hozirgi zamon talablariga mos kadr bo'lishingiz mumkin.</p>
            </div>
          </div>

          <div class="column is-12 has-text-centered">
            <router-link
              :to="$store.state.user.isAuthenticated ? '/courses' : '/sign-up'"
              class="button is-info is-size-3 mt-6 mb-6"
            >
              O'rganishni boshlang!
            </router-link>
          </div>

          <hr>

          <div
            class="column is-3"
            v-for="course in courses"
            :key="course.id"
          >
            <CourseItem :course="course" />
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios'
import CourseItem from '@/components/CourseItem.vue'

export default {
  name: 'HomeView',
  components: {
    CourseItem
  },
  data() {
    return {
      courses: []
    }
  },
  async mounted() {
    document.title = 'Xush kelibsiz | TheMWE.tech'

    try {
      const response = await axios.get('courses/get_frontpage_courses/')
      this.courses = response.data
    } catch (error) {
      console.error('Failed to load frontpage courses:', error)
    }
  }
}
</script>
