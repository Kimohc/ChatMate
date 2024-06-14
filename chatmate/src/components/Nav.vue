<template>
  <nav>
    <div class="logo">
      <div v-if="swipe">
        <div v-if="logged_in" class="aside-logo">
          <router-link to="/swipe/${false}">   <img class="aside-logo" src="/Jakubsk's..png" alt=""></router-link>
        </div>
        <div v-else class="aside-logo">
          <router-link to="/">   <img class="aside-logo"  src="/Jakubsk's..png" alt=""></router-link>
        </div>
      </div>
      <div v-else>
        <div v-if="logged_in">
          <router-link to='/swipe/{false}'>   <img src="/Jakubsk's..png" alt=""></router-link>
        </div>
        <div v-else>
          <router-link to="/">   <img src="/Jakubsk's..png" alt=""></router-link>
        </div>
      </div>

    </div>
    <div v-if="logged_in">
      <div v-if="profiel">
        <svg v-on:click="logout" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M8.51428 20H4.51428C3.40971 20 2.51428 19.1046 2.51428 18V6C2.51428 4.89543 3.40971 4 4.51428 4H8.51428V6H4.51428V18H8.51428V20Z" fill="currentColor" /><path d="M13.8418 17.385L15.262 15.9768L11.3428 12.0242L20.4857 12.0242C21.038 12.0242 21.4857 11.5765 21.4857 11.0242C21.4857 10.4719 21.038 10.0242 20.4857 10.0242L11.3236 10.0242L15.304 6.0774L13.8958 4.6572L7.5049 10.9941L13.8418 17.385Z" fill="currentColor" /></svg>
      </div>
      <div v-else>
        <router-link to="/profiel"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M16 9C16 11.2091 14.2091 13 12 13C9.79086 13 8 11.2091 8 9C8 6.79086 9.79086 5 12 5C14.2091 5 16 6.79086 16 9ZM14 9C14 10.1046 13.1046 11 12 11C10.8954 11 10 10.1046 10 9C10 7.89543 10.8954 7 12 7C13.1046 7 14 7.89543 14 9Z" fill="currentColor" /><path fill-rule="evenodd" clip-rule="evenodd" d="M12 1C5.92487 1 1 5.92487 1 12C1 18.0751 5.92487 23 12 23C18.0751 23 23 18.0751 23 12C23 5.92487 18.0751 1 12 1ZM3 12C3 14.0902 3.71255 16.014 4.90798 17.5417C6.55245 15.3889 9.14627 14 12.0645 14C14.9448 14 17.5092 15.3531 19.1565 17.4583C20.313 15.9443 21 14.0524 21 12C21 7.02944 16.9706 3 12 3C7.02944 3 3 7.02944 3 12ZM12 21C9.84977 21 7.87565 20.2459 6.32767 18.9878C7.59352 17.1812 9.69106 16 12.0645 16C14.4084 16 16.4833 17.1521 17.7538 18.9209C16.1939 20.2191 14.1881 21 12 21Z" fill="currentColor" /></svg></router-link>
      </div>
    </div>
    <div v-else>
   <router-link to="/signin"> <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.4857 20H19.4857C20.5903 20 21.4857 19.1046 21.4857 18V6C21.4857 4.89543 20.5903 4 19.4857 4H15.4857V6H19.4857V18H15.4857V20Z" fill="currentColor" /><path d="M10.1582 17.385L8.73801 15.9768L12.6572 12.0242L3.51428 12.0242C2.96199 12.0242 2.51428 11.5765 2.51428 11.0242C2.51429 10.4719 2.962 10.0242 3.51429 10.0242L12.6765 10.0242L8.69599 6.0774L10.1042 4.6572L16.4951 10.9941L10.1582 17.385Z" fill="currentColor" /></svg></router-link>
    </div>
  </nav>
</template>
<script>
import '/src/app.css'
export default {
  name: 'Nav_bar',
  components: {
  },
  props: {
    profiel: Boolean,
    swipe: Boolean,
  },
  data() {
    return {
    logged_in: false,
    }
  },
  methods: {
    logout(){
      this.$store.commit('setLoggedIn', false);
      this.$store.commit('setAccess_Token', null);
      this.$store.commit('setUser', null);
      this.$router.push('/')
    }

  },
  created() {
  },
  mounted() {
    this.logged_in = this.$store.getters.getLoggedIn

  }
}


</script>
<style>
nav{
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;

}
nav img{
  width: 20%;
  border-radius: 50%;
}
nav svg{
  margin: 30px;
  scale: 1.3;
  transition: 0.1s;
}
nav svg:hover{
  transform: scale(1.1);
  color: #803D3B;
  cursor: pointer;
}
.logo {
  display: flex;
  flex-direction: row;
  margin: 20px;
}


</style>