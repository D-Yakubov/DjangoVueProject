<template>
    <div>
        <h3>{{ question.question }}</h3>

        <div class="control">
            <label class="radio">
                <input type="radio" :value="question.op1" v-model="selectedAnswer" @change="emitAnswer"> {{ question.op1 }}
            </label>
        </div>

        <div class="control">
            <label class="radio">
                <input type="radio" :value="question.op2" v-model="selectedAnswer" @change="emitAnswer"> {{ question.op2 }}
            </label>
        </div>

        <div class="control">
            <label class="radio">
                <input type="radio" :value="question.op3" v-model="selectedAnswer" @change="emitAnswer"> {{ question.op3 }}
            </label>
        </div>
    </div>
</template>

<script>
export default {
    props: ['question'],
    data() {
        return {
            selectedAnswer: ''
        }
    },
    watch: {
        // Watch for question changes to reset selectedAnswer if the question prop itself changes
        // This is important if the same component instance is reused for different questions.
        question: {
            handler: function(newQuestion, oldQuestion) {
                if (newQuestion.id !== oldQuestion.id) {
                    this.selectedAnswer = '';
                }
            },
            deep: true // In case question is an object and its internal properties change
        }
    },
    methods: {
        emitAnswer() {
            if (this.selectedAnswer) {
                this.$emit('answer-selected', { questionId: this.question.id, selectedAnswer: this.selectedAnswer });
            }
        }
    }
}
</script>
