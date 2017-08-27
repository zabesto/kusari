<template>
  <div>
    <q-stepper ref='stepper'>
      <q-step title='Find Contract'>
        <p class='light-paragraph'>Find the contract using address</p>
        <q-field>
          <q-input v-model='contractAddress' stack-label='Enter Contract Address' v-on:keyup.enter='$refs.stepper.next()' :error='contractvalid' />
          <br />
        </q-field>
        <q-field>
          <q-input v-model='bidderAddress' stack-label='Enter Your Address' v-on:keyup.enter='$refs.stepper.next()' :error='biddervalid' />
          <br />
        </q-field>
        <q-field>
          <q-input v-model='bidderKey' stack-label='Enter Your Key' v-on:keyup.enter='$refs.stepper.next()' />
          <br />
        </q-field>
        <q-btn @click='searchContract'>Reveal</q-btn>
      </q-step>
    </q-stepper>
    <sweet-modal ref="successmodal" icon="success">
	  Successfully revealed!
</sweet-modal>
<sweet-modal ref="errormodal" icon="error" title="Oh noes…">
	This is an error…
</sweet-modal>
  </div>
</template>

<script>
import { SweetModal, SweetModalTab } from 'sweet-modal-vue'
import { QCard, QStepper, QStep, QCardTitle, QBtn, QCardActions, QIcon, QInput, QField, QChipsInput, QDatetime, QUploader } from 'quasar'
export default {
  components: {
    QBtn,
    SweetModal,
    SweetModalTab,
    QCard,
    QStepper,
    QStep,
    QCardTitle,
    QCardActions,
    QIcon,
    QInput,
    QField,
    QChipsInput,
    QDatetime,
    QUploader
  },
  data () {
    return {
      url: 'http://localhost:8080',
      addressError: [],
      message: '',
      contractAddress: this.$store.state.contract,
      bidderAddress: this.$store.state.account,
      bidderKey: ''
    }
  },
  methods: {
    searchContract () {
      this.$http.post('/api/drfp/reveal', {contractAddr: this.contractAddress, bidderAddr: this.bidderAddress, privateKey: this.bidderKey})
        .then(response => {
          console.log(response)
          if (response.data === 'success') {
            this.$refs.successmodal.open()
          }
          else {
            this.$refs.errormodal.open()
          }
        })
        .catch(e => {
        })
    },
    goBack () {
      window.history.go(-1)
    }
  },
  computed: {
    contractvalid () {
      if (!this.contractAddress || this.$isAddress(this.contractAddress)) return false
      return true
    },
    biddervalid () {
      if (!this.bidderAddress || this.$isAddress(this.bidderAddress)) return false
      return true
    },
    keyvalid () {
      if (!this.bidderKey || this.$isAddress(this.bidderKey)) return false
      return true
    }
  }
}
</script>
<style lang="stylus">
</style>
