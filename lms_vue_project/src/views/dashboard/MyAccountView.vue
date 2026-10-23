<template>
  <div class="about">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="title">Mening hisobim</h1>
      </div>
    </div>

    <section class="section">
      <div class="container">
        <div class="columns is-multiline">
          <div class="column is-12">
            <h2 class="subtitle is-size-3">O'rganayotgan kurslaringiz:</h2>
          </div>

          <div
            class="column is-4"
            v-for="course in courses"
            :key="course.id"
          >
            <CourseItem :course="course" />
          </div>

          <div v-if="!courses.length" class="column is-12">
            <p class="has-text-grey">Siz hali hech qanday kursni boshlamagansiz.</p>
          </div>
        </div>

        <hr>

        <button @click="logout" class="button is-danger">Hisobdan chiqish</button>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios'
import CourseItem from '@/components/CourseItem.vue'

export default {
  name: 'MyAccountView',
  components: {
    CourseItem
  },
  data() {
    return {
      courses: []
    }
  },
  async mounted() {
    document.title = 'Mening hisobim | TheMWE.tech'

    try {
      const response = await axios.get('activities/get_active_courses/')
      this.courses = response.data
    } catch (error) {
      console.error('Failed to fetch active courses:', error)
    }
  },
  methods: {
    async logout() {
      try {
        await axios.post('token/logout/')
      } catch (error) {
        console.error('Logout error:', error)
      } finally {
        this.$store.commit('removeToken')
        this.$router.push('/')
      }
    }
  }
}
</script>
