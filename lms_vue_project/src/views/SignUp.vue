<template>
  <div class="signup">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="title">Ro'yxatdan o'tish</h1>
      </div>
    </div>

    <section class="section">
        <div class="container">
            <div class="columns">
                <div class="column is-4 is-offset-4">
                    <form v-on:submit.prevent="submitForm">
                        <div class="field">
                            <label>Elektron pochta manzili</label>
                            <div class="control">
                                <input type="email" class="input" v-model="username">
                            </div>
                        </div>

                        <div class="field">
                            <label>Parol o'rnating</label>
                            <div class="control">
                                <input type="password" class="input" v-model="password">
                            </div>
                        </div>

                        <div class="field">
                            <label>Parolni takrorlang</label>
                            <div class="control">
                                <input type="password" class="input" v-model="password2">
                            </div>
                        </div>

                        <div class="notification is-danger" v-if="errors.length">
                            <p
                                v-for="error in errors"
                                v-bind:key="error"
                            >
                                {{ error }}
                            </p>
                        </div>

                        <div class="field">
                            <div class="control">
                                <button class="button is-dark">Ro'yxatdan o'tish</button>
                            </div>
                        </div>
                    </form>

                    <hr>

                    yoki kirish uchun <router-link to="/log-in">bu yerga</router-link> bosing!
                </div>
            </div>
        </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            username: '',
            password: '',
            password2: '',
            errors: []
        }
    },
    mounted() {
        document.title = "Ro'yxatdan o'tish | TheMWE.tech"
    },
    methods: {
        submitForm() {
            console.log('submitForm')

            this.errors = []

            if (this.username === '') {
                this.errors.push('Foydalanuvchi nomi kiritilmagan!')
            }

            if (this.password === '') {
                this.errors.push('Parol kiritilmagan!')
            }

            if (this.password !== this.password2) {
                this.errors.push('Parolingiz mos kelmayapti')
            }

            if (!this.errors.length) {
                const formData = {
                    username: this.username,
                    password: this.password
                }

                axios
                    .post('users/', formData)
                    .then(response => {
                        this.$router.push('/log-in')
                    })
                    .catch(error => {
                        if (error.response) {
                            for (const property in error.response.data) {
                                this.errors.push(`${property}: ${error.response.data[property]}`)
                            }

                            console.log(JSON.stringify(error.response.data))
                        } else if (error.message) {
                            this.errors.push("Nimadir xato ketdi. Iltimos, qayta urinib ko'ring")
                            
                            console.log(JSON.stringify(error))
                        }
                    })
            }
        }
    }
}
</script>