<template>
  <div class="about">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="title">Biz haqimizda</h1>
      </div>
    </div>
    <section class="section">
      <div class="container">
        TheMWE - bu "The Modern World Education" so'zlarining qisqartmasi bo'lib
        "Zamonaviy dunyo ta'limi" degan ma'noni anglatadi. Biz bu platformada
        hamma uchun ochiq bo'lgan Zamonaviy dunyo ta'limini siz bilan bo'lishamiz.
        Saytimizdan video, matn, video va matn ko'rinishidagi kurslar va
        maqolalarni topishingiz mumkin. Shuningdek, o'zlashtirgan bilimlaringizni
        sinab ko'rish uchun quiz testlar, boshqa o'rganuvchilar bilan fikr
        almashish uchun izohlar bo'limlari mavjud. O'quv platformamiz
        hozirda test rejimida ishlamoqda, agar saytda biror xatolik yuzaga kelsa
        biz bilan bog'lanishingizni iltimos qilamiz. Bog'lanish uchun
        support@TheMWE.tech elektron pochta manziliga yoki telegramdan
        @TheMWEtech ga yozishingiz mumkin.
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'AboutView',
  mounted() {
    document.title = 'Biz haqimizda | TheMWE.tech'
  }
}
</script>
