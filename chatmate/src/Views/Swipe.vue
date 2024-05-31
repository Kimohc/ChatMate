<template>
  <div id="app">
    <nav-bar></nav-bar>
    <main>

    </main>

  </div>
</template>
<script>
import '/src/app.css'
import Navbar from '/src/components/Nav.vue'

export default {
  name: 'Swipe_view',
  components: {
    'nav-bar': Navbar,
  },
  data() {
    return {
      user: {},
      access_token: '',
      logged_in: false
    }
  },
  methods: {

  },
  created() {

  },
  mounted() {
    this.logged_in = this.$store.getters.getLoggedIn
    this.user = this.$store.getters.getUser
    this.access_token = this.$store.getters.getAccess_Token
    console.log(this.user)

  }
}


</script>
<style>

</style>