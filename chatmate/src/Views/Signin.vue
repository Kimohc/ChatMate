<template>
  <div id="app">
    <nav-bar></nav-bar>
    <my-alert ref="myAlert" ></my-alert>
    <main>
      <div class="container" v-if="registered">
        <div class="folder">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M16 7C16 9.20914 14.2091 11 12 11C9.79086 11 8 9.20914 8 7C8 4.79086 9.79086 3 12 3C14.2091 3 16 4.79086 16 7ZM14 7C14 8.10457 13.1046 9 12 9C10.8954 9 10 8.10457 10 7C10 5.89543 10.8954 5 12 5C13.1046 5 14 5.89543 14 7Z" fill="currentColor" /><path d="M16 15C16 14.4477 15.5523 14 15 14H9C8.44772 14 8 14.4477 8 15V21H6V15C6 13.3431 7.34315 12 9 12H15C16.6569 12 18 13.3431 18 15V21H16V15Z" fill="currentColor" /></svg>
          <input type="text" placeholder="Username" required v-model="username">
        </div>
        <div class="folder">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M18 10.5C19.6569 10.5 21 11.8431 21 13.5V19.5C21 21.1569 19.6569 22.5 18 22.5H6C4.34315 22.5 3 21.1569 3 19.5V13.5C3 11.8431 4.34315 10.5 6 10.5V7.5C6 4.18629 8.68629 1.5 12 1.5C15.3137 1.5 18 4.18629 18 7.5V10.5ZM12 3.5C14.2091 3.5 16 5.29086 16 7.5V10.5H8V7.5C8 5.29086 9.79086 3.5 12 3.5ZM18 12.5H6C5.44772 12.5 5 12.9477 5 13.5V19.5C5 20.0523 5.44772 20.5 6 20.5H18C18.5523 20.5 19 20.0523 19 19.5V13.5C19 12.9477 18.5523 12.5 18 12.5Z" fill="currentColor" /></svg>
      <input @keyup.enter="login" type="password" placeholder="Password" required v-model="password">
        </div>
          <button @click="login">Sign in</button>
        <button @click="registered = false">Not yet registered?</button>
    </div>
      <div class="container" v-else>
        <div class="folder">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M3.00977 5.83789C3.00977 5.28561 3.45748 4.83789 4.00977 4.83789H20C20.5523 4.83789 21 5.28561 21 5.83789V17.1621C21 18.2667 20.1046 19.1621 19 19.1621H5C3.89543 19.1621 3 18.2667 3 17.1621V6.16211C3 6.11449 3.00333 6.06765 3.00977 6.0218V5.83789ZM5 8.06165V17.1621H19V8.06199L14.1215 12.9405C12.9499 14.1121 11.0504 14.1121 9.87885 12.9405L5 8.06165ZM6.57232 6.80554H17.428L12.7073 11.5263C12.3168 11.9168 11.6836 11.9168 11.2931 11.5263L6.57232 6.80554Z" fill="currentColor" /></svg>
          <input type="email" placeholder="E-mail" required v-model="emailRegister">

        </div>
        <div class="folder">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M16 7C16 9.20914 14.2091 11 12 11C9.79086 11 8 9.20914 8 7C8 4.79086 9.79086 3 12 3C14.2091 3 16 4.79086 16 7ZM14 7C14 8.10457 13.1046 9 12 9C10.8954 9 10 8.10457 10 7C10 5.89543 10.8954 5 12 5C13.1046 5 14 5.89543 14 7Z" fill="currentColor" /><path d="M16 15C16 14.4477 15.5523 14 15 14H9C8.44772 14 8 14.4477 8 15V21H6V15C6 13.3431 7.34315 12 9 12H15C16.6569 12 18 13.3431 18 15V21H16V15Z" fill="currentColor" /></svg>
          <input type="text" placeholder="Username" required v-model="usernameRegister">
        </div>
        <div class="folder">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M18 10.5C19.6569 10.5 21 11.8431 21 13.5V19.5C21 21.1569 19.6569 22.5 18 22.5H6C4.34315 22.5 3 21.1569 3 19.5V13.5C3 11.8431 4.34315 10.5 6 10.5V7.5C6 4.18629 8.68629 1.5 12 1.5C15.3137 1.5 18 4.18629 18 7.5V10.5ZM12 3.5C14.2091 3.5 16 5.29086 16 7.5V10.5H8V7.5C8 5.29086 9.79086 3.5 12 3.5ZM18 12.5H6C5.44772 12.5 5 12.9477 5 13.5V19.5C5 20.0523 5.44772 20.5 6 20.5H18C18.5523 20.5 19 20.0523 19 19.5V13.5C19 12.9477 18.5523 12.5 18 12.5Z" fill="currentColor" /></svg>
          <input @keyup.enter="register" type="password" placeholder="Password" required v-model="passwordRegister">
        </div>
        <button v-on:click="register">Sign up</button>
        <button @click="registered = true">Already registered?</button>
      </div>


    </main>

  </div>
</template>
<script>
import '/src/app.css'
import Navbar from '/src/components/Nav.vue'
import axios from "axios";
import MyAlert from '/src/components/Alert.vue'

export default {
  name: 'Signin_view',
  components: {
    'nav-bar': Navbar,
    'my-alert': MyAlert,
  },
  data() {
    return {
      emailRegister: '',
      usernameRegister: '',
      passwordRegister: '',
      username: '',
      password: '',
      registered: false,


    }
  },
  methods: {
    showAlert(message, isGood) {
      const alert = this.$refs.myAlert;
      alert.localMessage = message;
      alert.localIsGood = isGood;
      alert.showToast();
    },
    async redirectToHome() {
      await this.$router.push(`/swipe/${true}`);
    },
  async register(){
    try{
      if (!this.usernameRegister  || !this.passwordRegister || !this.emailRegister || this.usernameRegister.length > 100 || this.passwordRegister.length > 100 || this.emailRegister.length > 100 ){
        this.showAlert("Vul alle velden in", false)
        return
      }
      const response = await axios.post('http://127.0.0.1:8000/gebruiker/', {
        "e_mail": this.emailRegister,
        "gebruikersnaam": this.usernameRegister,
        "wachtwoord": this.passwordRegister
      })
      console.log(response.data)
      this.emailRegister = ''
      this.passwordRegister = ''
      this.usernameRegister = ''
      this.showAlert('gebruiker aangemaakt', true)
      this.registered = true

    }
    catch (error) {
      if (error.response === undefined) {
        this.showAlert('Account met deze gebruikersnaam of e-mail bestaat al.', false);
        console.log(error);
      } else {
        this.showAlert('Er is iets misgegaan probeer het nog eens.', false)
        console.log(error)
        }
      }
  },
    async login(){
    try{
      if (this.username === '' || this.password === '' || this.username.length > 100 || this.password.length > 100 ){
        this.showAlert('vul alle velden in', false)
      }
      const response = await axios.post('http://127.0.0.1:8000/gebruiker/login', {
        'gebruikersnaam': this.username,
        'wachtwoord': this.password
      })

      this.username = ''
      this.password = ''
      this.$store.commit('setLoggedIn', true);
      this.$store.commit('setAccess_Token', response.data.access_token);
      this.$store.commit('setUser', response.data);
      console.log(this.$store.commit('setUser', response.data))
      await this.redirectToHome()
    }
    catch (error){
      if ( error.response.status === 401) {
        this.showAlert('Verkeerd gebruikersnaam of wachtwoord.')
      }
      else{
        this.showAlert("Er is iets mis gegaan probeer het nog eens", false)
        console.log(error)
      }
    }
    },

  },
  created() {
  },
  mounted() {

  }
}


</script>
<style>

</style>