<template>
  <div class="courses">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="title">{{ course.title }}</h1>

        <router-link
          v-if="course.created_by && course.created_by.id"
          :to="{ name: 'Author', params: { id: course.created_by.id } }"
          class="subtitle"
        >
          Muallif: {{ authorFullName }}
        </router-link>
      </div>
    </div>

    <section class="section">
      <div class="container">
        <div class="columns content">
          <div class="column is-3">
            <h2>Darslar</h2>

            <aside class="menu">
              <ul class="menu-list">
                <li
                  v-for="lesson in lessons"
                  :key="lesson.id"
                >
                  <a
                    :class="{ 'is-active': activeLesson && activeLesson.id === lesson.id }"
                    @click="setActiveLesson(lesson)"
                  >
                    {{ lesson.title }}
                  </a>
                </li>
              </ul>
            </aside>
          </div>

          <div class="column is-9">
            <template v-if="$store.state.user.isAuthenticated">
              <template v-if="activeLesson">
                <h2>{{ activeLesson.title }}</h2>

                <span
                  class="tag is-warning is-clickable"
                  v-if="activity.status === 'started'"
                  @click="markAsDone"
                >
                  Boshlandi (yakunlangan qilib belgilash)
                </span>
                <span class="tag is-success" v-else-if="activity.status === 'done'">
                  Yakunlandi
                </span>

                <hr>

                <p>{{ activeLesson.long_description }}</p>

                <hr>

                <template v-if="activeLesson.lesson_type === 'quiz'">
                  <LessonQuiz
                    v-if="quiz && quiz.id"
                    :quiz="quiz"
                  />
                </template>

                <template v-if="activeLesson.lesson_type === 'video'">
                  <LessonVideo
                    :youtube_id="activeLesson.youtube_id"
                  />
                </template>

                <template v-if="activeLesson.lesson_type === 'article'">
                  <CourseComment
                    v-for="comment in comments"
                    :key="comment.id"
                    :comment="comment"
                  />

                  <AddComment
                    :course="course"
                    :activeLesson="activeLesson"
                    @submitComment="submitComment"
                  />
                </template>
              </template>

              <template v-else>
                <p>{{ course.long_description || course.short_description }}</p>
              </template>
            </template>

            <template v-else>
              <h2>Ma'lumotlar cheklangan!</h2>
              <p>Darslarni ko'rish va davom etish uchun tizimga kirishingiz yoki ro'yxatdan o'tishingiz kerak.</p>
              <div class="buttons mt-4">
                <router-link to="/log-in" class="button is-info">Kirish</router-link>
                <router-link to="/sign-up" class="button is-primary">Ro'yxatdan o'tish</router-link>
              </div>
            </template>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios'

import CourseComment from '@/components/CourseComment.vue'
import AddComment from '@/components/AddComment.vue'
import LessonQuiz from '@/components/LessonQuiz.vue'
import LessonVideo from '@/components/LessonVideo.vue'

export default {
  name: 'CourseDetailView',
  components: {
    CourseComment,
    AddComment,
    LessonQuiz,
    LessonVideo
  },
  data() {
    return {
      course: {
        created_by: {
          id: 0,
          username: '',
          first_name: '',
          last_name: ''
        }
      },
      lessons: [],
      comments: [],
      activeLesson: null,
      errors: [],
      quiz: {},
      activity: {}
    }
  },
  computed: {
    authorFullName() {
      const creator = this.course?.created_by
      if (!creator) return ''
      const fullName = `${creator.first_name || ''} ${creator.last_name || ''}`.trim()
      return fullName || creator.username || `Muallif #${creator.id}`
    }
  },
  async mounted() {
    const slug = this.$route.params.slug

    try {
      const response = await axios.get(`courses/${slug}/`)
      this.course = response.data.course
      this.lessons = response.data.lessons
      if (this.course?.title) {
        document.title = `${this.course.title} | TheMWE.tech`
      }
    } catch (error) {
      console.error('Failed to load course:', error)
    }
  },
  methods: {
    submitComment(comment) {
      this.comments.push(comment)
    },
    setActiveLesson(lesson) {
      if (!this.$store.state.user.isAuthenticated) {
        return
      }

      this.activeLesson = lesson
      this.quiz = {}
      this.comments = []
      this.activity = {}

      if (lesson.lesson_type === 'quiz') {
        this.getQuiz()
      } else if (lesson.lesson_type === 'article') {
        this.getComments()
      }

      this.trackStarted()
    },
    async trackStarted() {
      try {
        const response = await axios.post(
          `activities/track_started/${this.$route.params.slug}/${this.activeLesson.slug}/`
        )
        this.activity = response.data
      } catch (error) {
        console.error('Failed to track lesson start:', error)
      }
    },
    async markAsDone() {
      try {
        const response = await axios.post(
          `activities/mark_as_done/${this.$route.params.slug}/${this.activeLesson.slug}/`
        )
        this.activity = response.data
      } catch (error) {
        console.error('Failed to mark lesson as done:', error)
      }
    },
    async getQuiz() {
      try {
        const response = await axios.get(
          `courses/${this.course.slug}/${this.activeLesson.slug}/get-quiz/`
        )
        this.quiz = response.data
      } catch (error) {
        console.error('Failed to load quiz:', error)
      }
    },
    async getComments() {
      try {
        const response = await axios.get(
          `courses/${this.course.slug}/${this.activeLesson.slug}/get-comments/`
        )
        this.comments = response.data
      } catch (error) {
        console.error('Failed to load comments:', error)
      }
    }
  }
}
</script>
