<template>
  <div class="courses">
      <div class="hero is-info">
          <div class="hero-body has-text-centered">
              <h1 class="title">{{ course.title }}</h1>

              <router-link
                  :to="{name: 'Author', params: {id: course.created_by.id }}"
                  class="subtitle"
              >
                  By {{ course.created_by.first_name + ' ' + course.created_by.last_name }}
              </router-link>
          </div>
      </div>

      <section class="section">
          <div class="container">
              <div class="columns content">
                  <div class="column is-2">
                      <h2>Darslar</h2>

                      <ul>
                          <li
                              v-for="lesson in lessons"
                              v-bind:key="lesson.id"
                          >
                              <a @click="setActiveLesson(lesson)">{{ lesson.title }}</a>
                          </li>
                      </ul>
                  </div>

                  <div class="column is-10">
                      <template v-if="isAuthenticated">
                          <template v-if="activeLesson">
                              <h2>{{ activeLesson.title }}</h2>

                              <span class="tag is-warning" v-if="activity.status == 'started'" @click="markAsDone">Boshlandi (yakunlangan qilib belgilash)</span>
                              <span class="tag is-success" v-else>Yakunlandi</span>

                              <hr>
                              
                              {{ activeLesson.long_description }}

                              <hr>

                              <template v-if="activeLesson.lesson_type === 'quiz'">
                                  <div v-if="!quizResults">
                                      <div v-for="question_item in quizQuestions" :key="question_item.id" class="mb-4">
                                          <Question :question="question_item" @answer-selected="handleAnswerSelected" />
                                      </div>
                                      <button v-if="quizQuestions.length > 0 && Object.keys(userAnswers).length === quizQuestions.length" @click="submitAllAnswers" class="button is-success mt-4">Submit All Answers</button>
                                      <p v-else-if="quizQuestions.length > 0" class="mt-4 is-size-7">Please answer all questions to submit.</p>
                                  </div>
                                  <div v-if="quizResults" class="mt-4">
                                      <h3 class="is-size-4">Quiz Results</h3>
                                      <p class="is-size-5">Your score: {{ quizResults.score }} out of {{ quizResults.total_questions }}</p>
                                      <div v-for="result in quizResults.results" :key="result.question_id" class="mt-3 p-3" :class="result.correct ? 'has-background-success-light' : 'has-background-danger-light'">
                                          <p><strong>Question ID: {{result.question_id}}</strong></p>
                                          <p>Your answer: {{ result.selected_answer }}</p>
                                          <p>Correct answer: {{ result.correct_answer }}</p>
                                          <p :class="result.correct ? 'has-text-success-dark' : 'has-text-danger-dark'">You were {{ result.correct ? 'Correct' : 'Incorrect' }}</p>
                                      </div>
                                      <button @click="resetQuiz" class="button is-info mt-4">Retake Quiz</button>
                                  </div>
                              </template>

                              <template v-if="activeLesson.lesson_type === 'video'">
                                  <Video
                                      v-bind:youtube_id="activeLesson.youtube_id"
                                  />
                              </template>

                              <template  v-if="activeLesson.lesson_type === 'article'">
                                  <CourseComment
                                      v-for="comment in comments"
                                      v-bind:key="comment.id"
                                      v-bind:comment="comment"
                                  />

                                  <AddComment
                                      v-bind:course="course"
                                      v-bind:activeLesson="activeLesson"
                                      v-on:submitComment="submitComment"
                                  />
                              </template>
                          </template>

                          <template v-else>
                              {{ course.long_description }}
                          </template>
                      </template>

                      <template v-else>
                          <h2>Malumotlar cheklangan!</h2>
                          
                          <p>Davom etish uchun akkaunt ochishingiz kerak.</p>
                      </template>
                  </div>
              </div>
          </div>
      </section>
  </div>
</template>

<script>
import axios from 'axios'

import CourseComment from '@/components/CourseComment'
import AddComment from '@/components/AddComment'
import Question from '@/components/Question.vue' // Changed from Quiz to Question
import Video from '@/components/Video'

export default {
  components: {
      CourseComment,
      AddComment,
      Question, // Changed from Quiz to Question
      Video
  },
  data() {
      return {
          course: {
              created_by: {
                  id: 0
              }
          },
          lessons: [],
          comments: [],
          activeLesson: null,
          errors: [],
          quizQuestions: [], // Renamed from quiz to quizQuestions
          userAnswers: {},   // Added
          quizResults: null, // Added
          activity: {}
      }
  },
  computed: {
    isAuthenticated() {
      return this.$store.state.user.isAuthenticated;
    }
  },
  async mounted() {
    if (!this.isAuthenticated) {
      this.course = { created_by: { id: 0 } };
      this.lessons = [];
      this.activeLesson = null;
      // Set a generic title or handle it appropriately
      document.title = 'Course | theMWE.tech';
      return;
    }

    console.log('mounted');

    const slug = this.$route.params.slug;

    await axios
        .get(`courses/${slug}/`)
        .then(response => {
            console.log(response.data);
            this.course = response.data.course;
            this.lessons = response.data.lessons;
            // Set document title here now that course.title is available
            document.title = this.course.title + ' | theMWE.tech';
        })
        .catch(error => {
            console.error("Error fetching course data:", error);
            // Handle error, maybe redirect or show error message
            document.title = 'Error | theMWE.tech';
        });
  },
  methods: {
      submitComment(comment) {
          this.comments.push(comment)
      },
      setActiveLesson(lesson) {
          this.activeLesson = lesson;
          this.quizQuestions = []; // Reset quiz questions
          this.userAnswers = {};   // Reset user answers
          this.quizResults = null; // Reset quiz results
          this.comments = [];      // Reset comments

          if (lesson.lesson_type === 'quiz') {
              this.getQuizQuestions();
          } else if (lesson.lesson_type === 'article') { // Assuming comments are for articles
              this.getComments();
          }
          // For video lessons, no specific data fetching here beyond the lesson content itself

          this.trackStarted();
      },
      trackStarted() {
          axios
              .post(`activities/track_started/${this.$route.params.slug}/${this.activeLesson.slug}/`)
              .then(response => {
                  console.log(response.data)

                  this.activity = response.data
              })
      },
      markAsDone() {
          axios
              .post(`activities/mark_as_done/${this.$route.params.slug}/${this.activeLesson.slug}/`)
              .then(response => {
                  console.log(response.data)

                  this.activity = response.data
              })
      },
      getQuizQuestions() { // Renamed from getQuiz
          if (!this.isAuthenticated || !this.activeLesson) return;
          axios
              .get(`courses/${this.course.slug}/${this.activeLesson.slug}/get-quiz-questions/`) // Updated endpoint
              .then(response => {
                  console.log("Quiz questions:", response.data);
                  this.quizQuestions = response.data;
              })
              .catch(error => {
                  console.error("Error fetching quiz questions:", error);
                  this.quizQuestions = []; // Ensure it's an array on error
              });
      },
      handleAnswerSelected(payload) {
          this.userAnswers = {
              ...this.userAnswers,
              [payload.questionId]: payload.selectedAnswer
          };
          console.log("User answers:", this.userAnswers);
      },
      submitAllAnswers() {
          if (!this.isAuthenticated || !this.activeLesson) return;

          const payload = this.quizQuestions.map(q => ({
              question_id: q.id,
              selected_answer: this.userAnswers[q.id] || '' // Ensure an answer is provided, even if empty
          }));

          axios
              .post(`courses/${this.course.slug}/${this.activeLesson.slug}/submit-quiz-answers/`, payload)
              .then(response => {
                  console.log("Quiz submission response:", response.data);
                  this.quizResults = response.data;
                  // Optionally, clear answers or questions if not retaking immediately
                  // this.userAnswers = {};
                  // this.quizQuestions = [];
              })
              .catch(error => {
                  console.error("Error submitting quiz answers:", error);
                  // Potentially show an error message to the user
              });
      },
      resetQuiz() {
          this.quizQuestions = []; // Will be refetched by getQuizQuestions if needed or could re-use existing
          this.userAnswers = {};
          this.quizResults = null;
          this.getQuizQuestions(); // Refetch questions for a fresh attempt
      },
      getComments() {
          axios
              .get(`courses/${this.course.slug}/${this.activeLesson.slug}/get-comments/`)
              .then(response => {
                  console.log(response.data)

                  this.comments = response.data
              })
      }
  }
}
</script>