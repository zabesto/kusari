import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)
const store = new Vuex.Store({
  state: {
    account: '',
    contract: '',
    type: ''
  },
  mutations: {
    setContract (state, address) {
      state.contract = address
    },
    setAccount (state, address) {
      state.account = address
    },
    setType (state, type) {
      state.type = type
    }
  }
})

export default store
