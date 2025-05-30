<template>
  <div class="courses">
      <div class="hero is-info">
          <div class="hero-body has-text-centered">
              <h1 class="title">Kurslar</h1>
          </div>
      </div>

      <template v-if="isAuthenticated">
          <section class="section">
              <div class="container">
                  <div class="columns">
                      <div class="column is-2">
                      <aside class="menu">
                          <p class="menu-label">Kategoriya</p>

                          <ul class="menu-list">
                              <li>
                                  <a 
                                      v-bind:class="{'is-active': !activeCategory}"
                                      @click="setActiveCategory(null)"
                                  >
                                      Barcha kurslar
                                  </a>
                              </li>
                              <li
                                  v-for="category in categories"
                                  v-bind:key="category.id"
                                  @click="setActiveCategory(category)"
                              >
                                  <a>{{ category.title }}</a>
                              </li>
                          </ul>
                      </aside>
                  </div>

                  <div class="column is-10">
                      <div class="columns is-multiline">
                          <div 
                              class="column is-4"
                              v-for="course in courses"
                              v-bind:key="course.id"
                          >
                              <CourseItem :course="course" />
                          </div>

                          <div class="column is-12">
                              <nav class="pagination">
                                  <a class="pagination-previous">Avvalgi</a>
                                  <a class="pagination-next">Keyingi</a>
                              </nav>
                          </div>
                      </div>
                  </div>
              </div>
          </div>
      </section>
      </template>
      <template v-else>
          <section class="section">
              <div class="container has-text-centered">
                  <p class="is-size-4">You need to be logged in to view courses.</p>
                  <p>Please <router-link to="/log-in">Log In</router-link> or <router-link to="/sign-up">Sign Up</router-link>.</p>
              </div>
          </section>
      </template>
  </div>
</template>

<script>
import axios from 'axios'

import CourseItem from '@/components/CourseItem.vue'

export default {
  data() {
      return {
          courses: [],
          categories: [],
          activeCategory: null
      }
  },
  components: {
      CourseItem
  },
  computed: {
    isAuthenticated() {
      return this.$store.state.user.isAuthenticated;
    }
  },
  async mounted() {
    document.title = 'Kurslar | theMWE.tech';

    if (!this.isAuthenticated) {
      this.courses = [];
      this.categories = [];
      return;
    }

    console.log('mounted');

    await axios
        .get('courses/get_categories/')
        .then(response => {
            console.log(response.data);
            this.categories = response.data;
        });

    this.getCourses();
  },
  methods: {
      setActiveCategory(category) {
          console.log(category);
          this.activeCategory = category;

          this.getCourses();
      },
      getCourses() {
          if (!this.isAuthenticated) return;

          let url = 'courses/';

          if (this.activeCategory) {
              url += '?category_id=' + this.activeCategory.id
          }

          axios
              .get(url)
              .then(response => {
                  console.log(response.data)

                  this.courses = response.data
              })
      }
  }
}
</script>