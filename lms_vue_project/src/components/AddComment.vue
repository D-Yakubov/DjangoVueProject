<template>
  <form @submit.prevent="submitComment">
    <div class="field">
      <label class="label">Ismingiz</label>
      <div class="control">
        <input type="text" class="input" v-model.trim="comment.name">
      </div>
    </div>

    <div class="field">
      <label class="label">Kontent</label>
      <div class="control">
        <textarea class="textarea" v-model.trim="comment.content"></textarea>
      </div>
    </div>

    <div
      class="notification is-danger"
      v-for="(error, index) in errors"
      :key="index"
    >
      {{ error }}
    </div>

    <div class="field">
      <div class="control">
        <button class="button is-link" :class="{ 'is-loading': isSubmitting }" :disabled="isSubmitting">
          Jo'natish
        </button>
      </div>
    </div>
  </form>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AddComment',
  props: ['course', 'activeLesson'],
  emits: ['submitComment'],
  data() {
    return {
      comment: {
        name: '',
        content: ''
      },
      errors: [],
      isSubmitting: false
    }
  },
  methods: {
    async submitComment() {
      this.errors = []

      if (!this.comment.name) {
        this.errors.push('Nom kiritilishi shart!')
      }

      if (!this.comment.content) {
        this.errors.push("Ma'lumot kiritilishi shart!")
      }

      if (!this.errors.length) {
        this.isSubmitting = true
        try {
          const response = await axios.post(
            `courses/${this.$route.params.slug}/${this.activeLesson.slug}/`,
            this.comment
          )
          this.comment.name = ''
          this.comment.content = ''
          this.$emit('submitComment', response.data)
        } catch (error) {
          this.errors.push("Izoh yuborishda xatolik yuz berdi.")
        } finally {
          this.isSubmitting = false
        }
      }
    }
  }
}
</script>
