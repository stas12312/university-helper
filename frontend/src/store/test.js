import test from '../services/TestService'

const state = () => ({
    all: [],
    current: {},
    questions: [],
    isLoading: false,
})

const actions = {
    async getAllTests({commit, state}, token) {
        let r = await test.getAllTests(token);
        commit('pushAllTests', r.data);
        commit('load')
    },

    async getTest({commit, state}, payload) {
        let r = await test.getTest(payload.token, payload.test_id);
        commit('pushTest', r.data)
    },

    async getQuestions({commit, state}, payload) {
        let r = await test.getQuestions(payload.token, payload.test_id);
        commit('pushQuestions', r.data);
    },

    async clearData({commit, state}) {
        commit('pushTest', {});
        commit('pushQuestions', []);
    }
}

const getters = {
    questionsCount(state) {
        return state.questions.length;
    }
}

const mutations = {
    pushAllTests(state, tests) {
        state.all = tests
        console.log(tests)
    },

    pushTest(state, test) {
        state.current = test;
    },

    pushQuestions(state, questions) {
        state.questions = questions
    },

    load(state){
        console.log(state.isLoading)
        state.isLoading = true
        console.log(state.isLoading)
    }
}


export default {
    namespaces: true,
    state,
    actions,
    getters,
    mutations,
}
