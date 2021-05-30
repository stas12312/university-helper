<template>
  <transition name="el-fade-in-linear">
    <div class="login" v-show="show">
      <el-card class="form" style="">
        <el-form @submit.prevent="submit">
          <h3>Регистрация</h3>
          <el-form-item label-width="0">
            <el-input placeholder="E-mail" v-model="data.email" :disabled="data.lock_fields"></el-input>
          </el-form-item>
          <el-form-item label-width="0">
            <el-input placeholder="Пароль" v-model="data.password" show-password
                      :disabled="data.lock_fields"></el-input>
          </el-form-item>
          <el-form-item label-width="0" v-if="data.verify_uuid !== ''">
            <el-input placeholder="Код подтверждения email" v-model="data.verify_code"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" class="login-button" @click="submit">Регистрация</el-button>
          </el-form-item>
          <el-form-item>
            <el-button type="warning" class="login-button" @click="reset">Сбросить</el-button>
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
<script lang="ts">
import {onMounted, reactive, ref} from "vue";
import auth from "../services/AuthService";
import {ElNotification} from 'element-plus';
import {useRouter} from 'vue-router'
import {useStore} from 'vuex'

export default {
  name: "Register",
  setup() {
    const data = reactive({
      'email': '',
      'password': '',
      'verify_uuid': '',
      'verify_code': '',
      'lock_fields': false,
    });
    const router = useRouter();
    const store = useStore();
    let show = ref(false);
    onMounted(() => {
      show.value = true;
    })


    const submit = async () => {
      try {
        if (data.verify_uuid === "") {
          if (data.password.length < 8) {
            ElNotification.error({
              title: 'Неверное заполнение полей',
              message: 'Пароль должен быть не менее 8 символов',
            })
            return
          }

          if (data.email.length < 2) {
            ElNotification.error({
              title: 'Неверное заполнение полей',
              message: 'Укажите действительную почту',
            })
            return
          }


          let verify = await auth.send_code(data.email);
          ElNotification.success({
            title: 'Письмо с подтверждением отправлено',
            message: `На ваш почтовый ящик ${data.email} было отправлено письмо с кодом подтверждения почты`,
          })
          data.lock_fields = true;
          data.verify_uuid = verify.data.uuid;
        } else {
          let jwt = await auth.register(data.email, data.password, data.verify_uuid, data.verify_code);
          ElNotification.success({
            title: 'Регистрация завершена',
            message: '',
          })

          await store.dispatch('login', {
            'email': data.email,
            'password': data.password,
          });
          router.push('/profile');
        }
      } catch
          (e) {
        ElNotification.error({
          title: 'Ошибка при регистрации',
          message: e.response.data,
        })
      }
    }

    const reset = () => {
      data.email = '';
      data.password = '';
      data.verify_uuid = '';
      data.verify_uuid = '';
      data.lock_fields = false;
    }

    return {
      data,
      submit,
      reset,
      show,
    }
  }
}
</script>

<style scoped>

</style>