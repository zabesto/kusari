<template>
  <div>
  <h3>New Contract</h3>
  <q-stepper ref="stepper" >
    <q-step title="Contract Name">
      <h6>Contract Info</h6>
      <p class="light-paragraph">Entering a name is an important way for bidders to identify your bid. Make the name unique, this name will be saved onto the blockchain for enternity!</p>
      <q-field>
        <q-input v-model="contract.name" stack-label="Contract Name" v-on:keyup.enter="$refs.stepper.next()" />
        <br />
      </q-field>
      <q-field>
        <q-input v-model="contract.manager" stack-label="Manager Name" v-on:keyup.enter="$refs.stepper.next()" />
      </q-field>
      <q-stepper-navigation>
        <q-btn @click="$refs.stepper.next()">Next</q-btn>
      </q-stepper-navigation>
    </q-step>
    <q-step title="Bidder Whitelist">
      <h6>Bidder Whitelist</h6>
      <p class="light-paragraph">Whitelist the addresses you allow to bid on the project. The whitelist will prevent spamming and secure your bid request. A typical address format looks like the following, "0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe". Invalid address will not be accepted!</p>
      <q-field>
        <q-chips-input v-model="contract.whitelist" float-label="Bidder Whitelist" :error="invalidBidders"/>
      </q-field>
      <br />
      <q-stepper-navigation>
        <q-btn flat @click="$refs.stepper.previous()">Back</q-btn>
        <q-btn @click="$refs.stepper.next()">Next</q-btn>
      </q-stepper-navigation>
    </q-step>
    <q-step title="Periods">
      <h6>Period Ending Dates</h6>
      <p class="light-paragraph">These dates define the start of each period. The advertising period provides time for all parties to review the contract specification, and you will be able to modify your contract. The bidding period will lock the contract specification and allows the bidders to submit bids. The reveal period requires the bidders to submit their private keys and reveal their bid proposals. If a bidder fails to reveal their proposal before the award peiod, they will be removed as a qualified bidder.</p>
      <q-field>
        <q-datetime v-model="contract.periods.bidding" float-label="Bidding Start Date"/>
      </q-field>
      <q-field>
        <q-datetime v-model="contract.periods.reveal" float-label="Reveal Start Date"/>
      </q-field>
      <q-field>
        <q-datetime v-model="contract.periods.award" float-label="Award Start Date"/>
      </q-field>
      <br />
      <q-stepper-navigation>
        <q-btn flat @click="$refs.stepper.previous()">Back</q-btn>
        <q-btn @click="$refs.stepper.next()">Next</q-btn>
      </q-stepper-navigation>
    </q-step>
    <q-step title="Specification">
      <h6>Bid Specification</h6>
      <q-uploader ref="upload" hide-upload-button :url="url" :additionalFields="[{data: this.contract}]"></q-uploader>
      <q-stepper-navigation>
        <q-btn flat @click="$refs.stepper.previous()">Back</q-btn>
        <q-btn @click='submit'>Submit</q-btn>
      </q-stepper-navigation>
    </q-step>
  </q-stepper>
  </div>
</template>

<script>
import {QBtn, QIcon, QInput, QField, QChipsInput, QDatetime, QUploader, QStepper, QStepperNavigation, QStep} from 'quasar'

export default {
  components: {
    QBtn,
    QIcon,
    QInput,
    QField,
    QChipsInput,
    QDatetime,
    QUploader,
    QStepper,
    QStep,
    QStepperNavigation
  },
  mounted () {
  },
  data () {
    return {
      url: 'http://localhost:5000/',
      addressError: [],
      contract: {
        manager: null,
        name: null,
        whitelist: [],
        periods: {
          bidding: null,
          reveal: null,
          award: null
        },
        file: null
      },
      canGoBack: window.history.length > 1
    }
  },
  methods: {
    goBack () {
      window.history.go(-1)
    },
    submit () {
      console.log(this.$refs.upload.files[0])
      this.$file(this.$refs.upload.files[0]).then((file) => {
        this.contract.file = file
        console.log(JSON.stringify(this.contract))
        this.$http.post('/api/drfp/create', this.contract)
          .then(res => {
            console.log(res)
          })
          .catch(err => {
            console.log(err)
          })
      })
    }
  },
  computed: {
    invalidBidders () {
      var error = false
      this.addressError = this.contract.whitelist.map((el) => {
        if (!this.$isAddress(el)) {
          error = true
          return false
        }
        else {
          return true
        }
      })
      return error
    }
  }
}
</script>

<style lang="stylus">
</style>
