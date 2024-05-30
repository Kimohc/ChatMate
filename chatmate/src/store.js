import { createStore } from 'vuex';

// Create the Vuex store
const store = createStore({
    state: {
        loggedIn: false,
        user: {},
        access_token: '',
    },
    mutations: {
        setLoggedIn(state, payload) {
            state.loggedIn = payload;
        },
        setUser(state, payload) {
            state.user = payload;
        },
        setAccess_Token(state, payload) {
            state.access_token = payload;
        }
    },
    actions: {
        setLoggedIn({ commit }, payload) {
            commit('setLoggedIn', payload);
        },
        setUser({ commit }, payload) {
            commit('setUser', payload);
        },
        setAccess_Token({ commit }, payload) {
            commit('setAccess_Token', payload);
        }
    },
    getters: {
        getLoggedIn(state) {
            return state.loggedIn;
        },
        getUser(state) {
            return state.user;
        },
        getAccess_Token(state) {
            return state.access_token;
        }
    }
});

export default store