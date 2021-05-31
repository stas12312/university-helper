<template>
  <transition name="el-fade-in-linear">
    <el-row class="block" v-show="show" style="margin-top: 10px" type="flex" justify="center">
      <el-col :span="24">
        <p><i class="el-icon-message"></i> Почта {{ user.email }}</p>
        <p><i class="el-icon-coin"></i> Ваш баланс: {{ user.balance }} </p>

        <el-input v-model="amount" placeholder="Сумма пополнения" style="max-width: 400px" type="number"
                  clearable></el-input>
        <p></p>
        <el-button type="success" @click="createPay" :disabled="amount===''" :loading="isLoading.createPay"
                   icon="el-icon-plus">Пополнить
          баланс
        </el-button>
      </el-col>
      <el-col :xs="24" :sm="13" style="margin-top: 10px;">
        <el-alert
            title="Платеж может обрабатываться несколько часов, но обычно это происходит мгновенно."
            show-icon
            type="info"
            center
            :closable="false"
        >
        </el-alert>
      </el-col>
      <el-col :xs="24" :sm="13" style="margin-top: 10px;">
        <el-alert
            title="Если возникли проблемы с оплатой или получением теста,
            обращайтесь в службу поддержки support@university-helper.ru"
            show-icon
            type="info"
            center
            :closable="false"
        >
        </el-alert>
      </el-col>
    </el-row>
  </transition>
  <transition name="el-fade-in-linear">
    <el-row class="block" v-show="show" type="flex" justify="center">
      <el-col :span="24">
        <el-input v-model="data.test_id" placeholder="Введите ID теста" style="max-width: 400px"
                  type="number"></el-input>
        <p></p>
        <el-button type="primary" @click="new_test" :loading="isLoading.createTest"
                   :disabled="data.test_id.length === 0" icon="el-icon-s-order">
          Заказать новый тест
        </el-button>
      </el-col>
      <el-col :xs="24" :sm="12" style="margin-top: 10px;">
        <el-alert
            title="Для тестового заказа укажите 1 в поле ID"
            type="info"
            :closable="false"
            center
            show-icon>
        </el-alert>
      </el-col>
    </el-row>
  </transition>
  <transition name="el-fade-in-linear">
    <div v-show="show">
      <h4>Ваши тесты</h4>
      <div class="block" v-show="testLoading">

        <el-row v-for="test in tests" class="card">
          <el-col :span="24">
            <el-card class="box-card" shadow="hover">

              <el-row>
                <el-col :xs="24" :sm="4">Добавлен {{ dayjs(test.created_at).utc(true).format('DD.MM.YY в HH:mm') }}
                </el-col>
                <el-col :xs="24" :sm="2">Тест #{{ test.external_id }} {{
                  }}
                </el-col>
                <el-col :xs="24" :sm="12">{{ test.title }}</el-col>

                <template v-if="test.cost > 0">

                  <el-col :xs="24" :sm="6">Стоимость {{ test.cost }}
                    <el-tag type="success" v-if="test.is_paid">Оплачено</el-tag>
                    <el-tag type="danger" v-if="!test.is_paid">Не оплачено</el-tag>
                  </el-col>
                  <el-col :span="24">
                    <p></p>
                    <el-button v-if="!test.is_paid" type="success"
                               @click="buy_test(test.uuid)" icon="el-icon-money" :disabled="user.balance < test.cost">
                      Оплатить
                    </el-button>
                    <el-button :ref-id="test.uuid" type="primary" v-if="test.is_paid" @click="openTest(test.uuid)"
                               icon="el-icon-view">Открыть
                    </el-button>
                  </el-col>
                </template>

              </el-row>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </div>
  </transition>

</template>

<script>

import {computed, onMounted, reactive, ref} from 'vue';
import {useStore} from 'vuex';
import {useRouter} from 'vue-router';
import test_api from '../services/TestService';
import pay_api from '../services/PayService';
import {ElNotification} from 'element-plus';
import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc';

dayjs.extend(utc);

export default {
  name: "Profile",

  setup() {
    const store = useStore();
    const router = useRouter();

    const tests = computed(() => store.state.test.all);
    const user = computed(() => store.state.auth.user);
    const testLoading = computed(() => store.state.test.isLoading);
    const data = reactive({
      test_id: '',
    })
    const isLoading = reactive({
      'createTest': false,
      'createPay': false,

    })

    let show = ref(false);

    onMounted(() => {
      show.value = true;
    })

    let amount = ref('');


    store.dispatch('getTokenFromLocal');
    store.dispatch('getAllTests', store.state.auth.token);

    const new_test = async () => {
      isLoading.createTest = true;
      try {
        await test_api.createTest(store.state.auth.token, data.test_id);
        data.test_id = '';
        store.dispatch('getAllTests', store.state.auth.token);

      } catch (e) {
        ElNotification.error({
          title: 'Ошибка',
          message: e.response.data.detail,
        })
      } finally {
        isLoading.createTest = false;
      }

    }

    const createPay = async () => {
      isLoading.createPay = true;
      let clear_amount = parseInt(amount.value);

      let r = await pay_api.createPay(store.state.auth.token, clear_amount)
      let data = r.data;
      amount.value = '';
      isLoading.createPay = false;
      window.open(data.payUrl, "_blank");
    }

    const buy_test = async (test_id) => {
      await test_api.payTest(store.state.auth.token, test_id)
      store.dispatch('getAllTests', store.state.auth.token);
      store.dispatch('getMe');
    }

    const openTest = async (test_uuid) => {
      router.push(`/tests/${test_uuid}`);
    }


    return {
      tests,
      user,
      data,
      new_test,
      buy_test,
      router,
      isLoading,
      testLoading,
      openTest,
      dayjs,
      show,
      amount,
      createPay,
    }

  },
}
</script>

<style scoped>
.card {
  margin: 10px;
}
</style>