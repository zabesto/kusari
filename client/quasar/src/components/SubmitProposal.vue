<template>
  <div>
    <q-stepper ref='stepper'>
      <q-step title='Contract'>
        <h6>Contract Address</h6>
        <p class='light-paragraph'>Enter the contract address, and submit your bid!</p>
        <q-field>
          <q-input v-model='address' stack-label='Contract Address' v-on:keyup.enter='searchContract' :error='valid' />
          <br />
        </q-field>
        <q-btn :disabled='valid' @click='searchContract'>Search</q-btn>
      </q-step>
      <q-step title='Bid Submittal'>
        <h4>Contract</h4>
        <h6>RFP: {{contract.name}}</h6>
        <p class="light-paragraph">Manager: {{contract.manager}}</p>
        <q-uploader ref='upload' hide-upload-button url='na'></q-uploader>
        <br />
        <q-btn @click='$refs.stepper.previous()'>Back</q-btn>
        <q-btn @click='submit'>Upload</q-btn>
      </q-step>
      <q-step title="Completed">
        <h4>Bid Proposal</h4>
        <p class="light-paragraph">You may view your proposal at the following location: {{ipfsAddress}}</p>
      </q-step>
    </q-stepper>
  </div>
</template>

<script>
import {QBtn, QIcon, QField, QInput, QStepper, QStep, QUploader, Toast} from 'quasar'

export default {
  components: {
    QBtn,
    QIcon,
    QField,
    QInput,
    QStepper,
    QStep,
    QUploader,
    Toast
  },
  data () {
    return {
      address: '',
      ipfsAddress: '',
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
        whitelist: [],
        file: ''
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
    submit () {
      console.log(this.$refs.upload.files[0])
      this.$file(this.$refs.upload.files[0]).then((file) => {
        this.file = file
        console.log(JSON.stringify(this.contract))
        this.$http.post('/api/drfp/proposal/' + this.address, this.file)
          .then(res => {
            Toast.create['positive']({
              html: 'Success! Your proposal has been submitted.'
            })
            console.log(res)
          })
          .catch(err => {
            console.log(err)
          })
      })
    },
    searchContract () {
      this.$http.get('/api/drfp/contract/' + this.address)
        .then(res => {
          this.contract = res.data
          this.$refs.stepper.next()
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
