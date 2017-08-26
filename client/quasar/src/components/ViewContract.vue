<template>
  <div class="">
    <h5>View Contract</h5>
    <span>Contract Name: {{ contract.name }}</span><br><br>
    <span>Manager Address: {{ contract.managerAddress }}</span><br><br>
    <span>Manager Name: {{ contract.manager }}</span><br><br>
    <span>Spec Link: <a :href="contract.specLink">{{ contract.specLink }}</a></span><br><br>
    <span>Whitelist: {{ contract.whitelist }}</span><br><br>
    <span>Award Date: {{ contract.periods.award }}</span><br><br>
    <span>Bidding Date: {{ contract.periods.bidding }}</span><br><br>
    <span>Reveal Date: {{ contract.periods.reveal }}</span>
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
    this.$http.get('http://localhost:5000/').then(response => {
      this.contract.name = response.data.name
      this.contract.manager = response.data.manager
      this.contract.managerAddress = response.data.managerAddress
      this.contract.specLink = response.data.specLink
      this.contract.whitelist = response.data.whitelist
      this.contract.periods.award = response.data.periods.award
      this.contract.periods.bidding = response.data.periods.bidding
      this.contract.periods.reveal = response.data.periods.reveal
    }, response => {
      console.log(response)
    })
  },
  data () {
    return {
      url: 'http://localhost:8080',
      addressError: [],
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
