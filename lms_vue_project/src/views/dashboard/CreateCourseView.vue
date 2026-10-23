<template>
  <div class="create-course">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="title">Kurs yaratish</h1>
      </div>
    </div>

    <section class="section">
      <div class="container">
        <div class="notification is-danger" v-if="errors.length">
          <p v-for="(error, index) in errors" :key="index">{{ error }}</p>
        </div>

        <div class="mb-6 px-6 py-4 has-background-white-ter box">
          <h2 class="subtitle">Asosiy ma'lumotlar</h2>

          <div class="field">
            <label class="label">Kurs nomi</label>
            <input type="text" class="input" v-model.trim="form.title">
          </div>

          <div class="field">
            <label class="label">Qisqa tavsif</label>
            <textarea class="textarea" v-model.trim="form.short_description"></textarea>
          </div>

          <div class="field">
            <label class="label">To'liq tavsif</label>
            <textarea class="textarea" v-model.trim="form.long_description"></textarea>
          </div>

          <div class="field" v-if="categories.length">
            <label class="label">Kategoriyalar</label>
            <div class="select is-multiple is-fullwidth">
              <select multiple size="5" v-model="form.categories">
                <option
                  v-for="category in categories"
                  :key="category.id"
                  :value="category.id"
                >
                  {{ category.title }}
                </option>
              </select>
            </div>
          </div>
        </div>

        <div class="mb-6 px-6 py-4 has-background-white-ter box">
          <h2 class="subtitle">Darslar</h2>

          <div
            v-for="(lesson, index) in form.lessons"
            :key="index"
            class="mb-4"
          >
            <div class="is-flex is-justify-content-space-between is-align-items-center mb-2">
              <h3 class="subtitle is-size-6 mb-0">Dars #{{ index + 1 }}</h3>
              <button class="button is-small is-danger is-light" @click="removeLesson(index)">
                O'chirish
              </button>
            </div>

            <div class="field">
              <label class="label">Dars nomi</label>
              <input
                type="text"
                class="input"
                v-model.trim="lesson.title"
                :name="`form.lessons[${index}][title]`"
              >
            </div>

            <div class="field">
              <label class="label">Qisqa tavsif</label>
              <textarea
                class="textarea"
                v-model.trim="lesson.short_description"
                :name="`form.lessons[${index}][short_description]`"
              ></textarea>
            </div>

            <div class="field">
              <label class="label">To'liq tavsif</label>
              <textarea
                class="textarea"
                v-model.trim="lesson.long_description"
                :name="`form.lessons[${index}][long_description]`"
              ></textarea>
            </div>

            <hr>
          </div>

          <button class="button is-primary" @click="addLesson">Dars qo'shish</button>
        </div>

        <div class="field buttons">
          <button
            class="button is-success"
            :disabled="isSubmitting"
            @click="submitForm('draft')"
          >
            Qoralama sifatida saqlash
          </button>
          <button
            class="button is-info"
            :disabled="isSubmitting"
            @click="submitForm('in_review')"
          >
            Tekshiruvga yuborish
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CreateCourseView',
  data() {
    return {
      form: {
        title: '',
        short_description: '',
        long_description: '',
        categories: [],
        status: '',
        lessons: []
      },
      categories: [],
      errors: [],
      isSubmitting: false
    }
  },
  mounted() {
    document.title = 'Kurs yaratish | TheMWE.tech'
    this.getCategories()
  },
  methods: {
    async getCategories() {
      try {
        const response = await axios.get('courses/get_categories/')
        this.categories = response.data
      } catch (error) {
        console.error('Failed to load categories:', error)
      }
    },
    async submitForm(status) {
      this.errors = []

      if (!this.form.title) {
        this.errors.push('Kurs nomi kiritilishi shart!')
        return
      }

      this.form.status = status
      this.isSubmitting = true

      try {
        await axios.post('courses/create/', this.form)
        this.$router.push('/dashboard/my-account')
      } catch (error) {
        this.errors.push("Kursni saqlashda xatolik yuz berdi.")
      } finally {
        this.isSubmitting = false
      }
    },
    addLesson() {
      this.form.lessons.push({
        title: '',
        short_description: '',
        long_description: ''
      })
    },
    removeLesson(index) {
      this.form.lessons.splice(index, 1)
    }
  }
}
</script>
