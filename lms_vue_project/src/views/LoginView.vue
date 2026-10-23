<template>
  <div class="login">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="title">Kirish</h1>
      </div>
    </div>

    <section class="section">
      <div class="container">
        <div class="columns">
          <div class="column is-4 is-offset-4">
            <form @submit.prevent="submitForm">
              <div class="field">
                <label class="label">Email pochta manzili</label>
                <div class="control">
                  <input type="email" class="input" v-model.trim="username">
                </div>
              </div>

              <div class="field">
                <label class="label">Parolingiz</label>
                <div class="control">
                  <input type="password" class="input" v-model="password">
                </div>
              </div>

              <div class="notification is-danger" v-if="errors.length">
                <p
                  v-for="(error, index) in errors"
                  :key="index"
                >
                  {{ error }}
                </p>
              </div>

              <div class="field">
                <div class="control">
                  <button class="button is-dark" :class="{ 'is-loading': isLoading }" :disabled="isLoading">
                    Kirish
                  </button>
                </div>
              </div>
            </form>

            <hr>

            yoki <router-link to="/sign-up">ro'yxatdan</router-link> o'ting
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'LoginView',
  data() {
    return {
      username: '',
      password: '',
      errors: [],
      isLoading: false
    }
  },
  mounted() {
    document.title = 'Kirish | TheMWE.tech'
  },
  methods: {
    async submitForm() {
      this.$store.commit('removeToken')
      this.errors = []

      if (!this.username) {
        this.errors.push('Foydalanuvchi nomi kiritilmagan')
      }

      if (!this.password) {
        this.errors.push('Parol kiritilmagan')
      }

      if (!this.errors.length) {
        this.isLoading = true
        try {
          const response = await axios.post('token/login/', {
            username: this.username,
            password: this.password
          })
          const token = response.data.auth_token
          this.$store.commit('setToken', token)
          this.$router.push('/dashboard/my-account')
        } catch (error) {
          if (error.response && error.response.data) {
            for (const property in error.response.data) {
              this.errors.push(`${property}: ${error.response.data[property]}`)
            }
          } else {
            this.errors.push("Nimadir xato ketdi. Iltimos, qayta urinib ko'ring")
          }
        } finally {
          this.isLoading = false
        }
      }
    }
  }
}
</script>
