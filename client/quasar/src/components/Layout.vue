<template>
  <q-layout
    ref="layout"
    view="lHh Lpr fff"
    :left-class="{'bg-grey-2': true}"
  >
    <q-toolbar slot="header" class="">
      <q-btn
        flat
        @click="$refs.layout.toggleLeft()"
      >
        <q-icon name="menu" />
      </q-btn>

      <q-toolbar-title>
        dRFP
        <div slot="subtitle">Decentralized Contract Proposals</div>
      </q-toolbar-title>
      <q-btn :disabled="account=='owner'" @click='owner' flat>
        Owner
      </q-btn>
      <q-btn :disable="account=='bidder'" @click='bidder' flat>
        Bidder
      </q-btn>
    </q-toolbar>

    <div slot="left">
      <!--
        Use <q-side-link> component
        instead of <q-item> for
        internal vue-router navigation
      -->
      <q-list no-border link inset-delimiter>
        <q-list-header>Contract</q-list-header>
        <q-item to="/viewcontract">
          <q-item-side icon="developer_board" />
          <q-item-main label="View Contract" />
        </q-item>
        <q-list-header>Contract Manager</q-list-header>
        <q-item to="/createcontract">
          <q-item-side icon="add_box" />
          <q-item-main label="Create Contract" />
        </q-item>
        <q-item to="/modifycontract">
          <q-item-side icon="mode_edit" />
          <q-item-main label="Modify Contract" />
        </q-item>
        <q-list-header>Contract Bidder</q-list-header>
        <q-item to="/submitproposal">
          <q-item-side icon="insert_drive_file" />
          <q-item-main label="Submit Proposal" />
        </q-item>
        <q-item to="/revealbid">
          <q-item-side icon="fingerprint" />
          <q-item-main label="Reveal Bid" />
        </q-item>
      </q-list>
    </div>

    <!--
      Replace following <div> with
      <router-view /> component
      if using subRoutes
    -->
    <div class="layout-padding row justify-center">
      <div style="width: 800px; max-width: 90vw;">
        <router-view></router-view>
      </div>
    </div>
  </q-layout>
</template>

<script>
import {
  QLayout,
  QToolbar,
  QToolbarTitle,
  QBtn,
  QIcon,
  QList,
  QListHeader,
  QItem,
  QItemSide,
  QItemMain
} from 'quasar'

export default {
  name: 'index',
  components: {
    QLayout,
    QToolbar,
    QToolbarTitle,
    QBtn,
    QIcon,
    QList,
    QListHeader,
    QItem,
    QItemSide,
    QItemMain
  },
  data () {
    return {
      account: 'owner',
      key: ''
    }
  },
  computed: {
  },
  methods: {
    owner () {
      this.$http.get('/api/drfp/account/owner')
        .then(res => {
          this.account = 'owner'
          this.key = res.data
          window.localStorage.setItem('account', res.data)
        })
    },
    bidder () {
      this.$http.get('/api/drfp/account/bidder/1')
        .then(res => {
          this.account = 'bidder'
          this.key = res.data
          window.localStorage.setItem('account', res.data)
        })
    }
  },
  mounted () {
  }
}
</script>

<style lang="stylus">
.logo-container
  width 255px
  height 242px
  perspective 800px
  position absolute
  top 50%
  left 50%
  transform translateX(-50%) translateY(-50%)
.logo
  position absolute
  transform-style preserve-3d
</style>
