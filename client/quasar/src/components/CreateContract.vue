<template>
  <div class="">
    <h2>New Contract</h2>
    <q-field>
      <q-input v-model="contract.name" stack-label="Contract Name" />
    </q-field>
    <q-field>
      <q-chips-input v-model="contract.whitelist" float-label="Bidder Whitelist" :error="invalidBidders"/>
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
    <q-input type="file" />
    <q-uploader :url="url"></q-uploader>
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
  data () {
    return {
      url: "http://localhost:8080",
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
