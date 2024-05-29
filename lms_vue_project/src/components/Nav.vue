<template>
  <nav class="navbar is-info" role="navigation" aria-label="main naviation" style="min-height: 6rem;">
      <div class="navbar-brand">
          <router-link class="navbar-item is-size-4" to="/">TheMWE.tech</router-link>
      </div>

      <div id="navbar-item" class="navbar-menu">
          <div class="navbar-start">
              <router-link to="/" class="navbar-item">Bosh sahifa</router-link>
              <router-link to="/courses" class="navbar-item">Kurslar</router-link>
              <router-link to="/about" class="navbar-item">Biz haqimizda</router-link>
          </div>

          <div class="navbar-end">
              <div class="navbar-item">
                  <div class="buttons">
                      <template v-if="$store.state.user.isAuthenticated">
                          <!-- <router-link to="/dashboard/create-course" class="button is-primary">Create course</router-link> -->
                          <router-link to="/dashboard/my-account" class="button is-info">Dashboard</router-link>
                      </template>

                      <template v-else>
                          <router-link to="/sign-up" class="button is-primary"><strong>Ro'yxatdan o'tish</strong></router-link>
                          <router-link to="/log-in" class="button is-light">Kirish</router-link>
                      </template>
                  </div>
              </div>
          </div>
      </div>
  </nav>
</template>