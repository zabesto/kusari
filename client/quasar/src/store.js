import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)
const store = new Vuex.Store({
  state: {
    address: '',
    type: ''
  },
  mutations: {
    setAddress (state, address) {
      state.address = address
    },
    setType (state, type) {
      state.type = type
    }
  }
})

export default store
