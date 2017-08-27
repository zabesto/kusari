<template>
  <div>
    <q-stepper ref='stepper'>
      <q-step title='Find Contract'>
        <p class='light-paragraph'>Find the contract using address</p>
        <q-field>
          <q-input v-model='contractAddress' stack-label='Enter Contract Address' v-on:keyup.enter='$refs.stepper.next()' :error='valid' />
          <br />
        </q-field>
        <q-field>
          <q-input v-model='managerAddress' stack-label='Enter Manager Address' v-on:keyup.enter='$refs.stepper.next()' :error='valid' />
          <br />
        </q-field>
        <q-btn @click='searchContract'>Search</q-btn>
      </q-step>
      <q-step title='Contract Details'>
         <h5>Contract Details</h5>
    <span>Contract Name: {{ contract.name }}</span><br><br>
    <span>Manager Address: {{ contract.managerAddress }}</span><br><br>
    <span>Manager Name: {{ contract.manager }}</span><br><br>
    <span>Spec Link: <a :href="contract.specLink" target="_blank">{{ contract.specLink }}</a></span><br><br>
  <q-btn>
    <a :href="contract.specLink" target="_blank" download>Download</a>
</q-btn><br><br>
    <span>Award Date: {{ contract.periods.award }}</span><br><br>
    <span>Bidding Date: {{ contract.periods.bidding }}</span><br><br>
    <span>Reveal Date: {{ contract.periods.reveal }}</span><br><br>
  <!-- An basic example -->
   <q-card>
      <q-card-title align = "center">
        Whitelist
      </q-card-title>
      <q-card-actions >
        <q-btn flat v-for="item in contract.whitelist" :key="item">{{ item }}</q-btn>
      </q-card-actions>
    </q-card>
      </q-step>
    </q-stepper>
  </div>
</template>

<script>
import { QCard, QStepper, QStep, QCardTitle, QBtn, QCardActions, QIcon, QInput, QField, QChipsInput, QDatetime, QUploader } from 'quasar'
export default {
  components: {
    QBtn,
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
      contractAddress: '',
      managerAddress: '',
      contract: {
        name: null,
        manager: null,
        managerAddress: null,
        specLink: null,
        whitelist: [],
        periods: {
          award: null,
          bidding: null,
          reveal: null
        }
      },
      canGoBack: window.history.length > 1
    }
  },
  methods: {
    searchContract () {
      this.$http.post('http://localhost:5000/search/', {ownerAddr: this.contractAddress, contractAddr: this.managerAddress})
        .then(response => {
          this.contract.name = response.data.name
          this.contract.manager = response.data.manager
          this.contract.managerAddress = response.data.managerAddress
          this.contract.specLink = response.data.specLink
          this.contract.whitelist = response.data.whitelist
          this.contract.periods.award = new Date(response.data.periods.award).toString()
          this.contract.periods.bidding = new Date(response.data.periods.bidding).toString()
          this.contract.periods.reveal = new Date(response.data.periods.reveal).toString()
          this.$refs.stepper.next()
        })
        .catch(e => {
        })
    },
    goBack () {
      window.history.go(-1)
    }
  },
  computed: {
    valid () {
      if (!this.address || this.$isAddress(this.address)) return false
      return true
    }
  }
}
</script>
<style lang="stylus">
</style>
