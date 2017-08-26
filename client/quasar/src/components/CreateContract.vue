<template>
  <div class="layout-padding row justify-center">
    <div style="width: 800px; max-width: 90vw;">
        <h3>New Contract</h3>
        <q-stepper ref="stepper" >
          <q-step>
            <h6>Contract Name</h6>
            <p class="light-paragraph">Entering a name is an important way for bidders to identify your bid. Make the name unique, this name will be saved onto the blockchain for enternity!</p>
            <q-field>
              <q-input v-model="contract.name" stack-label="Contract Name" v-on:keyup.enter="$refs.stepper.next()" />
              <br />
            </q-field>
            <q-stepper-navigation>
              <q-btn @click="$refs.stepper.next()">Next</q-btn>
            </q-stepper-navigation>
          </q-step>
          <q-step>
            <h6>Contract Name</h6>
            <p class="light-paragraph">Whitelist the addresses you allow to bid on the project. The whitelist will prevent spamming and secure your bid request. A typical address format looks like the following, "0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe". Invalid address will not be accepted! </p>
            <q-field>
              <q-chips-input v-model="contract.whitelist" float-label="Bidder Whitelist" :error="invalidBidders"/>
            </q-field>
            <br />
            <q-stepper-navigation>
              <q-btn flat @click="$refs.stepper.previous()">Back</q-btn>
              <q-btn @click="$refs.stepper.next()">Next</q-btn>
            </q-stepper-navigation>
          </q-step>
          <q-step>
            <h6>Period Ending Dates</h6>
            <p class="light-paragraph">These dates define the end of each period. The advertising period provides time for all parties to review the contract specification, and you will be able to modify your contract. The bidding period will lock the contract specification and allows the bidders to submit bids. The reveal period requires the bidders to submit their private keys and reveal their bid proposals. If a bidder fails to reveal their proposal, they will be removed as a qualified bidder.</p>
            <q-field>
              <q-datetime v-model="contract.endPeriods.advertising" float-label="Advertising End Date"/>
            </q-field>
            <q-field>
              <q-datetime v-model="contract.endPeriods.bidding" float-label="Bidding End Date"/>
            </q-field>
            <q-field>
              <q-datetime v-model="contract.endPeriods.reveal" float-label="Reveal End Date"/>
            </q-field>
            <br />
            <q-stepper-navigation>
              <q-btn flat @click="$refs.stepper.previous()">Back</q-btn>
              <q-btn @click="$refs.stepper.next()">Next</q-btn>
            </q-stepper-navigation>
          </q-step>
          <q-step>
            <q-input type="file" />
            <q-uploader hide-upload-button :url="url"></q-uploader>
            <q-stepper-navigation>
              <q-btn flat @click="$refs.stepper.previous()">Back</q-btn>
              <q-btn @click="$refs.stepper.next()">Next</q-btn>
            </q-stepper-navigation>
          </q-step>
        </q-stepper>
    </div>
  </div>
</template>

<script>
import ethAddress from 'ethereum-address'
import { QBtn, QIcon, QInput, QField, QChipsInput, QDatetime, QUploader, QStepper, QStep} from 'quasar'

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
    QStep
  },
  mounted () {
    alert('test')
  },
  data () {
    return {
      url: 'http://localhost:8080',
      addressError: [],
      contract: {
        name: null,
        whitelist: [],
        endPeriods: {
          advertising: null,
          bidding: null,
          reveal: null
        }
      },
      canGoBack: window.history.length > 1
    }
  },
  methods: {
    goBack () {
      window.history.go(-1)
    }
  },
  computed: {
    invalidBidders () {
      var error = false
      this.addressError = this.contract.whitelist.map((el) => {
        if (!ethAddress.isAddress(el)) {
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
