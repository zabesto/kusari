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
        <span>Spec Link: <a :href="'http://ipfs.io/ipfs/' + contract.specLink" target="_blank">{{ contract.specLink }}</a></span><br><br>
        <br />
        <span>Award Date: {{ contract.award }}</span><br><br>
        <span>Bidding Date: {{ contract.bidding }}</span><br><br>
        <span>Reveal Date: {{ contract.reveal }}</span><br><br>
        <!-- An basic example -->
        <q-card inline style="width: 100%">
          <q-card-title>
            All Bids
          </q-card-title>
          <q-list separator>
            <q-collapsible v-for="item in contract.bidders" :key="item" icon="perm_identity" :label="item[l.account] ">
                <q-list highlight inset-separator>
              <q-item> <q-item-main label="FileLink"/>
                <a :href="'http://ipfs.io/ipfs/' + item[l.file]" target="_blank">{{ item[l.file] }}</a>
               </q-item>
               <q-item>
                 <q-item-main label="PrivateKey" :sublabel= " item[l.privateKey]"/>
            </q-item>
                </q-list>
            </q-collapsible>
          </q-list>
        </q-card>
      </q-step>
    </q-stepper>
   
  </div>
</template>

<script>
import { QCard, QList, QItem, QItemSide, QItemMain, QCollapsible, QStepper, QStep, QCardTitle, QBtn, QCardActions, QIcon, QInput, QField, QChipsInput, QDatetime, QUploader } from 'quasar'

export default {
  components: {
    QBtn,
    QCard,
    QList,
    QItem,
    QItemSide,
    QItemMain,
    QCollapsible,
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
      l: {
        'valid': 0,
        'account': 1,
        'name': 2,
        'publicKey': 3,
        'file': 4,
        'privateKey': 5
      },
      url: 'http://localhost:8080',
      addressError: [],
      contractAddress: this.$store.state.contract,
      managerAddress: this.$store.state.account,
      contract: {
        name: null,
        manager: null,
        managerAddress: null,
        specLink: null,
        whitelist: [],
        award: null,
        bidding: null,
        reveal: null
      },
      canGoBack: window.history.length > 1
    }
  },
  methods: {
    searchContract () {
      this.$http.post('/api/drfp/search', {
        ownerAddr: this.managerAddress,
        contractAddr: this.contractAddress
      })
        .then(res => {
          console.log(res)
          this.contract = res.data
          this.contract.award = new Date(res.data.award).toString()
          this.contract.bidding = new Date(res.data.bidding).toString()
          this.contract.reveal = new Date(res.data.reveal).toString()
          this.$refs.stepper.next()
          this.contract.bidder = res.data.bidder
          console.log(this.contract.whitelist)
        })
        .catch(e => {
          console.log(e)
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
