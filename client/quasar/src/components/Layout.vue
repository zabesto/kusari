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
        Quasar App
        <div slot="subtitle">Running on Quasar v{{$q.version}}</div>
      </q-toolbar-title>
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
    <router-view />
  </q-layout>
</template>

<script>
import {
  openURL,
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
    }
  },
  computed: {
  },
  methods: {
    launch (url) {
      openURL(url)
    }
  },
  mounted () {
    this.$nextTick(() => {
      if (this.orienting) {
        window.addEventListener('deviceorientation', this.orient, false)
      }
      else if (this.rotating) {
        window.addEventListener('devicemove', this.rotate, false)
      }
      else {
        document.addEventListener('mousemove', this.move)
      }
    })
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
