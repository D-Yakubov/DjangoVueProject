<template>
  <div>
    <h3 class="subtitle is-5">{{ quiz.question }}</h3>

    <div class="control mb-2" v-if="quiz.op1">
      <label class="radio">
        <input type="radio" :value="quiz.op1" v-model="selectedAnswer"> {{ quiz.op1 }}
      </label>
    </div>

    <div class="control mb-2" v-if="quiz.op2">
      <label class="radio">
        <input type="radio" :value="quiz.op2" v-model="selectedAnswer"> {{ quiz.op2 }}
      </label>
    </div>

    <div class="control mb-2" v-if="quiz.op3">
      <label class="radio">
        <input type="radio" :value="quiz.op3" v-model="selectedAnswer"> {{ quiz.op3 }}
      </label>
    </div>

    <div class="control mt-4">
      <button class="button is-info" @click="submitQuiz">Jo'natish</button>
    </div>

    <div v-if="quizResult === 'unselected'" class="notification is-warning mt-4">
      Iltimos, avval javob variantini tanlang!
    </div>

    <div v-if="quizResult === 'correct'" class="notification is-success mt-4">
      To'g'ri!
    </div>

    <div v-if="quizResult === 'incorrect'" class="notification is-danger mt-4">
      Xato (Iltimos qayta urinib ko'ring!)
    </div>
  </div>
</template>

<script>
export default {
  name: 'LessonQuiz',
  props: {
    quiz: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      selectedAnswer: '',
      quizResult: null
    }
  },
  watch: {
    quiz() {
      this.selectedAnswer = ''
      this.quizResult = null
    }
  },
  methods: {
    submitQuiz() {
      this.quizResult = null

      if (!this.selectedAnswer) {
        this.quizResult = 'unselected'
        return
      }

      if (this.selectedAnswer === this.quiz.answer) {
        this.quizResult = 'correct'
      } else {
        this.quizResult = 'incorrect'
      }
    }
  }
}
</script>
