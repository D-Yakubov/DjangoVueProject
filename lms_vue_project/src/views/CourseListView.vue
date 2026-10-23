<template>
  <div class="courses">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="title">Kurslar</h1>
      </div>
    </div>

    <section class="section">
      <div class="container">
        <div class="columns">
          <div class="column is-2">
            <aside class="menu">
              <p class="menu-label">Kategoriya</p>

              <ul class="menu-list">
                <li>
                  <a
                    :class="{ 'is-active': !activeCategory }"
                    @click="setActiveCategory(null)"
                  >
                    Barcha kurslar
                  </a>
                </li>
                <li
                  v-for="category in categories"
                  :key="category.id"
                  @click="setActiveCategory(category)"
                >
                  <a :class="{ 'is-active': activeCategory && activeCategory.id === category.id }">
                    {{ category.title }}
                  </a>
                </li>
              </ul>
            </aside>
          </div>

          <div class="column is-10">
            <div class="columns is-multiline">
              <div
                class="column is-4"
                v-for="course in courses"
                :key="course.id"
              >
                <CourseItem :course="course" />
              </div>

              <div v-if="!courses.length" class="column is-12">
                <p class="has-text-grey">Ushbu kategoriyada hozircha kurslar mavjud emas.</p>
              </div>
            </div>
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
  name: 'CourseListView',
  components: {
    CourseItem
  },
  data() {
    return {
      courses: [],
      categories: [],
      activeCategory: null
    }
  },
  async mounted() {
    document.title = 'Kurslar | TheMWE.tech'

    try {
      const response = await axios.get('courses/get_categories/')
      this.categories = response.data
    } catch (error) {
      console.error('Failed to fetch categories:', error)
    }

    await this.getCourses()
  },
  methods: {
    setActiveCategory(category) {
      this.activeCategory = category
      this.getCourses()
    },
    async getCourses() {
      let url = 'courses/'

      if (this.activeCategory) {
        url += `?category_id=${this.activeCategory.id}`
      }

      try {
        const response = await axios.get(url)
        this.courses = response.data
      } catch (error) {
        console.error('Failed to fetch courses:', error)
      }
    }
  }
}
</script>
