import auth from '../services/AuthService'

const state = () => ({
    token: '',
    user: '',
})


const actions = {
    async login({commit, state}, payload) {
        let r = await auth.login(payload.email, payload.password);
        console.log(r.data);
        let token = r.data.access_token;
        console.log(token);
        commit('pushToken', token);
        let r_user = await auth.getMe(token);
        let user = r_user.data;
        commit('pushUser', user);
    },

    async logout({commit, state}) {
        commit('pushToken', '');
        commit('pushUser', {});
    },

    async getTokenFromLocal({commit, state}) {
        let token = sessionStorage.getItem('token');
        if (token) {
            commit('pushToken', token);
        }
        let r_user = await auth.getMe(token);
        let user = r_user.data;
        commit('pushUser', user);
        console.log(state.user)

    },

    async getMe({commit, state}) {
        let r = await auth.getMe(state.token);
        commit('pushUser', r.data);
    }


}

const mutations = {
    pushToken(state, token) {
        state.token = token;
        sessionStorage.setItem('token', token);
    },

    pushUser(state, user) {
        state.user = user;
    }
}

export default {
    namespaces: true,
    state,
    actions,
    mutations,
}

