<template>

  <p></p>
  <el-row type="flex" justify="center" class="block">
    <el-col :xs="24" :sm="14">
      <h3 style="text-align: center">
        <p>Добро пожаловать!</p>
        <p>Для использования данного сервиса авторизуйтесь или
          зарегистрируйтесь.</p>
      </h3>
      <p>
        За регистрацию вы получите 100 приветственных бонусов.
      </p>
    </el-col>


    <el-col :xs="24" :sm="14">
      <el-row type="flex" justify="center">
        <el-button type="primary" @click="$router.push('login')">Авторизация</el-button>
        <el-button type="success" @click="$router.push('register')">Регистрация</el-button>
      </el-row>
    </el-col>
  </el-row>
  <el-row type="flex" justify="center" class="block">
    <el-col :xs="24" :sm="14" style="text-align: center">
      <h4>Что умеет данный сервис:</h4>
    </el-col>
    <el-col :xs="24" :sm="14" style="text-align: center">
      <p>
        Данный сервис позволяет получать правильные ответы на тесты из системы Dispace*.
      </p>
      <p> Получение ответов происходит автоматически и занимает не больше 30 минут, для получение ответов нужен только
        идентификатор теста в системе Dispace.</p>
      <p>Вы платите только за количество полученных ответов, никакой предоплаты за кота в мешке:)</p>
      <el-alert
          title="*Сервис не гарантирует получение 100% ответов, в среднем удается получить около 95% вопросов и шанс,
          что вам попадётся вопрос, на который система не нашла ответ, крайне мал."
          type="info"
          :closable="false"
          center
          show-icon>
      </el-alert>
    </el-col>

  </el-row>

  <el-row type="flex" justify="center" class="block">
    <el-col :xs="24" :sm="14" style="text-align: center">
      <h4>Как расcчитывается стоимость теста:</h4>
    </el-col>
    <el-col :xs="24" :sm="14" style="text-align: center">
      <p>Сервис предоставляет динамическую тарификацию.</p>
      <p>Стоимость теста формируется исходя из количества полученных ответов*,
        в таблице представлена стоимость одного вопроса в зависимости от количества вопросов в тесте:</p>
    </el-col>
    <el-col :xs="24" :sm="14">
      <el-table
          :data="tableDate"
          style="width: 100%"
          border
      >
        <el-table-column
            align="center"
            prop="questionsCount"
            label="Кол-во вопросов">
        </el-table-column>
        <el-table-column
            align="center"
            prop="questionCost"
            label="Цена за ответ">
        </el-table-column>
      </el-table>
    </el-col>

    <el-col :xs="24" :sm="14">
      <p>Рассчитать стоимость теста:</p>
      <el-row type="flex" justify="center">
        <el-col :xs="24" :xl="6">
          <el-input v-model="questionsCount" placeholder="Количество вопросов" type="number" clearable
                    min="1"></el-input>
        </el-col>
        <el-col :xs="24" :xl="6">
          <span style="line-height: 40px">Стоимость теста составляет: {{ testCost }}</span>
        </el-col>
      </el-row>
    </el-col>


    <el-col :xs="24" :sm="14" style="text-align: center">
      <p></p>
      <el-alert
          title="*Учитывается количество вопросов в банке вопросов, а не количество вопросов в тесте для студента."
          type="info"
          :closable="false"
          center
          style="font-size: 20px"
          show-icon>
      </el-alert>
    </el-col>
  </el-row>

  <el-row type="flex" justify="center" class="block">
    <el-col :span="24" style="text-align: center">
      <h4>Контакты для связи:</h4>
    </el-col>
    <el-col :span="24" style="text-align: center">
      <el-link icon="el-icon-message" :underline="false" href="mailto:support@university-helper.ru" type="primary"
               style="font-size: 16px">support@university-helper.ru
      </el-link>
    </el-col>

  </el-row>

</template>

<script>

import {computed, ref} from 'vue';

export default {
  name: "Home",
  setup() {
    const tableDate = [
      {
        questionsCount: '1-25',
        questionCost: 7,
        avgCost: 140
      },
      {
        questionsCount: '26-50',
        questionCost: 6,
        avgCost: 240
      },
      {
        questionsCount: '51-75',
        questionCost: 5,
        avgCost: 300,
      },
      {
        questionsCount: '76-100',
        questionCost: 4,
        avgCost: 360,
      },
      {
        questionsCount: '101-150',
        questionCost: 3,
        avgCost: 375,
      },
      {
        questionsCount: '151-200',
        questionCost: 2,
        avgCost: 350
      },
      {
        questionsCount: '201-*',
        questionCost: 1,
        avgCost: 300,
      }
    ]

    const questionsCount = ref(0);
    const testCost = computed(() => {
      if (questionsCount.value === "") {
        return ''
      }
      let qC = parseInt(questionsCount.value)
      let cost = 7
      if (qC >= 201) {
        cost = 1
      } else if (qC >= 151) {
        cost = 2
      } else if (qC >= 101) {
        cost = 3
      } else if (qC >= 76) {
        cost = 4
      } else if (qC >= 51) {
        cost = 5
      } else if (qC >= 26) {
        cost = 6
      }
      return qC * cost
    })

    return {
      tableDate,
      questionsCount,
      testCost,
    }
  }
};
</script>

<style scoped>
h4 {
  margin: 4px;
}

.cell {
  word-break: break-word !important;
}
</style>