import {createStore} from "vuex";
import auth from './auth';
import test from './test'
export default createStore({
    modules: {
        auth,
        test
    },
    strict: true,
})


