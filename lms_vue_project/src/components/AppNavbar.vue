<template>
  <nav class="navbar is-info" role="navigation" aria-label="main navigation" style="min-height: 5rem;">
    <div class="navbar-brand">
      <router-link class="navbar-item is-size-4" to="/">TheMWE.tech</router-link>

      <a
        role="button"
        class="navbar-burger"
        :class="{ 'is-active': showMobileMenu }"
        aria-label="menu"
        :aria-expanded="showMobileMenu"
        @click="showMobileMenu = !showMobileMenu"
      >
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>

    <div id="navbar-item" class="navbar-menu" :class="{ 'is-active': showMobileMenu }">
      <div class="navbar-start">
        <router-link to="/" class="navbar-item" @click="showMobileMenu = false">Bosh sahifa</router-link>
        <router-link to="/courses" class="navbar-item" @click="showMobileMenu = false">Kurslar</router-link>
        <router-link to="/about" class="navbar-item" @click="showMobileMenu = false">Biz haqimizda</router-link>
      </div>

      <div class="navbar-end">
        <div class="navbar-item">
          <div class="buttons">
            <template v-if="$store.state.user.isAuthenticated">
              <router-link to="/dashboard/create-course" class="button is-primary" @click="showMobileMenu = false">
                Kurs yaratish
              </router-link>
              <router-link to="/dashboard/my-account" class="button is-light" @click="showMobileMenu = false">
                Kabinet
              </router-link>
            </template>

            <template v-else>
              <router-link to="/sign-up" class="button is-primary" @click="showMobileMenu = false">
                <strong>Ro'yxatdan o'tish</strong>
              </router-link>
              <router-link to="/log-in" class="button is-light" @click="showMobileMenu = false">
                Kirish
              </router-link>
            </template>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'AppNavbar',
  data() {
    return {
      showMobileMenu: false
    }
  }
}
</script>
