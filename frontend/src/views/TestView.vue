<template>
  <h4>Ваши ответы</h4>
  <h5>Количество вопросов: {{ questions.length }}</h5>
  <div class="block">
    <el-row v-for="question in questions" class="card">
      <el-col :span="24">
        <el-card class="box-card" shadow="hover">
          <p><b>{{ question.rubric }}</b></p>
          <p><i>{{ question.body }}</i></p>
          <el-row>
            <el-col :span="24" v-for="answer in question.answers">
              <div class="answer">
                <span><i class="el-icon-success"></i> {{ answer }}</span>
              </div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import {computed, ref} from 'vue'
import {useStore} from 'vuex'
import {ElLoading} from 'element-plus'
import {useRoute, useRouter} from 'vue-router'


export default {
  name: "TestView",

  setup() {

    const store = useStore();
    const router = useRouter();
    const route = useRoute();

    const test = computed(() => store.state.test.current);
    const user = computed(() => store.state.auth.user);
    const questions = computed(() => store.state.test.questions);

    let loading = ElLoading.service({fullscreen: true});
    let test_id = ref('');

    store.dispatch('clearData');
    store.dispatch('getTokenFromLocal');
    store.dispatch('getTest', {
      'token': store.state.auth.token,
      'test_id': route.params.uuid,
    });

    store.dispatch('getQuestions', {
      'token': store.state.auth.token,
      'test_id': route.params.uuid,
    })
    loading.close();
    return {
      test,
      user,
      questions,
      test_id,
      router,
    }

  },
}
</script>

<style scoped>
.card {
  margin: 10px 0;
}

.answer {
  margin: 4px;
  padding: 10px;
  background-color: #f0f9eb;
  color: #67C23A;
}

p {
  margin: 1px;
}
</style>