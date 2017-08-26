<template>
  <div>
    <q-stepper ref='stepper'>
      <q-step title='Contract'>
        <h6>Contract Address</h6>
        <p class='light-paragraph'>Enter the contract address, and submit your bid!</p>
        <q-field>
          <q-input v-model='address' stack-label='Contract Address' v-on:keyup.enter='$refs.stepper.next()' :error='valid' />
          <br />
        </q-field>
        <q-btn :disabled='valid' @click='searchContract'>Search</q-btn>
      </q-step>
      <q-step title='Bid Submittal'>
        <h6>{{contract.name}}</h6>
        <p>{{contract.manager}}</p>
        <q-uploader ref='upload' hide-upload-button url='na'></q-uploader>
      </q-step>
    </q-stepper>
  </div>
</template>

<script>
import {QBtn, QIcon, QField, QInput, QStepper, QStep, QUploader} from 'quasar'

export default {
  components: {
    QBtn,
    QIcon,
    QField,
    QInput,
    QStepper,
    QStep,
    QUploader
  },
  data () {
    return {
      address: '',
      contract: {
        managerAdress: null,
        manager: null,
        name: null,
        periods: {
          award: null,
          bidding: null,
          reveal: null
        },
        specLink: null,
        whitelist: []
      },
      canGoBack: window.history.length > 1
    }
  },
  computed: {
    valid () {
      if (!this.address || this.$isAddress(this.address)) return false
      return true
    }
  },
  methods: {
    searchContract () {
      this.$http.get('/api/contract/' + this.address)
        .then(res => {
          console.log(res)
        })
        .catch(e => {
          return {
            'manager': 'rishabh',
            'managerAddress': 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNA3DQEBAQUAA4GNqGKukO1De7zhZj6+H0q',
            'name': 'Contruct12',
            'periods': {
              'award': 1503772718327,
              'bidding': 1503772718327,
              'reveal': 1503772718327
            },
            'specLink': 'https://www.google.com/',
            'whitelist': [
              'MIGfMA0GCSqGSIb',
              '3DQEBAQUAA4GN',
              '3DQEBAQUAA4GN',
              'ukO1De7zhZj6+'
            ]
          }
        })
    },
    goBack () {
      window.history.go(-1)
    }
  }
}
</script>

<style lang='stylus'>
</style>
