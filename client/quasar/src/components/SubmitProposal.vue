<template>
  <div>
    <q-stepper ref='stepper'>
      <q-step title='Contract'>
        <h6>Contract Address</h6>
        <p class='light-paragraph'>Enter the contract address, and submit your bid!</p>
        <q-field>
          <q-input v-model='contractAddress' stack-label='Contract Address' v-on:keyup.enter='searchContract' :error='valid' />
          <br />
        </q-field>
        <q-field>
          <q-input v-model='managerAddress' stack-label='User Address' v-on:keyup.enter='searchContract' :error='valid' />
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
        <p>{{privateKey}}</p>
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
      contractAddress: this.$store.state.contract,
      managerAddress: this.$store.state.account,
      ipfsAddress: '',
      contract: {
        managerAdress: null,
        manager: null,
        name: null,
        periods: {
          award: '08-26-2017',
          bidding: '08-27-2017',
          reveal: '08-28-2017'
        },
        specLink: null,
        whitelist: [],
        file: ''
      },
      privateKey: '',
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
        var load = {
          file: this.file,
          contractAddr: this.contractAddress,
          bidderAddr: this.managerAddress
        }
        console.log(load)
        this.$http.post('/api/drfp/proposal', load)
          .then(res => {
            this.privateKey = res.data[1]
            Toast.create['positive']({
              html: 'Success! Your proposal has been submitted.'
            })
            this.$refs.stepper.next()
            console.log(res)
          })
          .catch(err => {
            console.log(err)
          })
      })
    },
    searchContract () {
      this.$http.post('/api/drfp/search', {
        ownerAddr: this.managerAddress,
        contractAddr: this.contractAddress
      })
        .then(res => {
          console.log(res)
          this.contract = res.data
          this.$refs.stepper.next()
        })
        .catch(e => {
          console.log(e)
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
