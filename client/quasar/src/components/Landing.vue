<template>
  <div class="">
    <h4>Kusari</h4>
<p class="light-paragpraph">A decentralized protocol that ensures trust and openness in the RFP process, preventing collusion for multi-billion dollar bids.</p>
  </div>
</template>

<script>
import { QBtn, QIcon } from 'quasar'

export default {
  components: {
    QBtn,
    QIcon
  },
  data () {
    return {
      canGoBack: window.history.length > 1
    }
  },
  methods: {
    goBack () {
      window.history.go(-1)
    }
  }
}
</script>

<style lang="stylus">
</style>
