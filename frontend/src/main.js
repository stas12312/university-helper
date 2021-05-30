import {createApp} from 'vue'
import router from './router'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/lib/theme-chalk/index.css';
import locale from 'element-plus/lib/locale/lang/ru'
import 'dayjs/locale/ru'
import store from './store'

createApp(App).use(router).use(ElementPlus, {locale}).use(store).mount('#app')