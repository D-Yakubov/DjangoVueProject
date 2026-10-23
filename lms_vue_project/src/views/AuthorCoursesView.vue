<template>
  <div class="courses">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="title">{{ authorFullName }}</h1>
      </div>
    </div>

    <section class="section">
      <div class="container">
        <div class="columns is-multiline">
          <div
            class="column is-4"
            v-for="course in courses"
            :key="course.id"
          >
            <CourseItem :course="course" />
          </div>

          <div v-if="!courses.length" class="column is-12">
            <p class="has-text-grey">Muallifda hozircha nashr etilgan kurslar yo'q.</p>
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
  name: 'AuthorCoursesView',
  components: {
    CourseItem
  },
  data() {
    return {
      courses: [],
      created_by: {}
    }
  },
  computed: {
    authorFullName() {
      const fullName = `${this.created_by.first_name || ''} ${this.created_by.last_name || ''}`.trim()
      return fullName || this.created_by.username || 'Muallif'
    }
  },
  async mounted() {
    await this.getCourses()
    document.title = `${this.authorFullName} | TheMWE.tech`
  },
  methods: {
    async getCourses() {
      try {
        const response = await axios.get(`courses/get_author_courses/${this.$route.params.id}/`)
        this.courses = response.data.courses
        this.created_by = response.data.created_by
      } catch (error) {
        console.error('Failed to load author courses:', error)
      }
    }
  }
}
</script>
