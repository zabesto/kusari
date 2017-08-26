<template>
  <div class="">
    <h2>View Contract</h2>
    <q-field>
      <q-input v-model="contract.firstname" stack-label="Contract Name" />
    </q-field>
    <q-field>
      <q-chips-input v-model="contract.whitelist" float-label="Bidder Whitelist"/>
    </q-field>
    <h4>Period Ending Dates</h4>
    <q-field>
      <q-datetime v-model="contract.endPeriods.advertising" float-label="Advertising End Date"/>
    </q-field>
    <q-field>
      <q-datetime v-model="contract.endPeriods.bidding" float-label="Bidding End Date"/>
    </q-field>
    <q-field>
      <q-datetime v-model="contract.endPeriods.reveal" float-label="Reveal End Date"/>
    </q-field>
  </div>
</template>

<script>
import ethAddress from 'ethereum-address'
import { QBtn, QIcon, QInput, QField, QChipsInput, QDatetime, QUploader } from 'quasar'
export default {
  components: {
    QBtn,
    QIcon,
    QInput,
    QField,
    QChipsInput,
    QDatetime,
    QUploader
  },
  mounted () {
    this.$http.get('/api').then(response => {
      this.contract.firstname = response.data.firstName
      console.log(response.data.firstName)
    }, response => {
      console.log(response)
    })
  },
  data () {
    return {
      url: 'http://localhost:8080',
      addressError: [],
      contract: {
        firstname: null,
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
