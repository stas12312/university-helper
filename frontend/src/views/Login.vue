<template>
  <transition name="el-fade-in-linear">
    <div class="login" v-show="show">
      <el-card class="form" style="">
        <el-form>
          <h3>Авторизация</h3>
          <el-form-item label-width="0">
            <el-input placeholder="E-mail" v-model="data.email"></el-input>
          </el-form-item>
          <el-form-item label-width="0">
            <el-input placeholder="Пароль" v-model="data.password" show-password></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" class="login-button" @click="submit" :loading="isLoading.login"> Вход</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </transition>
</template>

<style>
.login {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  padding: 0 10px;
}

.form {
  width: 490px;
  margin: 0 auto;
  text-align: center;
}

.login-button {
  width: 100%;
}
</style>

<script>
import {onMounted, reactive, ref} from "vue"
import {useStore} from 'vuex'
import {useRouter} from 'vue-router'
import {ElNotification} from 'element-plus';

export default {

  name: "Login",
  setup() {

    const store = useStore();
    const router = useRouter();

    const data = reactive({
      'email': '',
      'password': '',
    })

    const isLoading = reactive({
      'login': false,
    })

    let show = ref(false);
    onMounted(() => {
      show.value = true;
    })

    const submit = async () => {
      try {
        isLoading.login = true;
        await store.dispatch('login', {
          'email': data.email,
          'password': data.password,
        });
        ElNotification.success({
          title: 'Успешная авторизация',
          message: 'Вы авторизовались',
        })
        router.push('/profile');
      } catch (e) {
        ElNotification.error({
          title: 'Ошибка авторизации',
          message: 'Не удалось авторизоваться',
        })
      } finally {
        isLoading.login = false;
      }


    }

    return {
      data,
      isLoading,
      submit,
      show
    }
  }
};
</script>

<style scoped>
</style>