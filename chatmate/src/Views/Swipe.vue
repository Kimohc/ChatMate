<template>
  <div id="app">
    <my-alert ref="myAlert"></my-alert>
    <span class="hamburger" id="hamburger" @click="openSideBar"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M8.01562 6.98193C7.46334 6.98193 7.01562 7.43285 7.01562 7.98513C7.01562 8.53742 7.46334 8.98833 8.01563 8.98833H15.9659C16.5182 8.98833 16.9659 8.53742 16.9659 7.98513C16.9659 7.43285 16.5182 6.98193 15.9659 6.98193H8.01562Z" fill="currentColor" /><path d="M7.01562 12C7.01562 11.4477 7.46334 10.9968 8.01562 10.9968H15.9659C16.5182 10.9968 16.9659 11.4477 16.9659 12C16.9659 12.5523 16.5182 13.0032 15.9659 13.0032H8.01563C7.46334 13.0032 7.01562 12.5523 7.01562 12Z" fill="currentColor" /><path d="M8.0249 15.0122C7.47262 15.0122 7.0249 15.4631 7.0249 16.0154C7.0249 16.5677 7.47262 17.0186 8.0249 17.0186H15.9752C16.5275 17.0186 16.9752 16.5677 16.9752 16.0154C16.9752 15.4631 16.5275 15.0122 15.9752 15.0122H8.0249Z" fill="currentColor" /><path fill-rule="evenodd" clip-rule="evenodd" d="M3 6C3 4.34315 4.34315 3 6 3H18C19.6569 3 21 4.34315 21 6V18C21 19.6569 19.6569 21 18 21H6C4.34315 21 3 19.6569 3 18V6ZM6 5H18C18.5523 5 19 5.44772 19 6V18C19 18.5523 18.5523 19 18 19H6C5.44772 19 5 18.5523 5 18V6C5 5.44772 5.44772 5 6 5Z" fill="currentColor" /></svg></span>
    <div class="sidebar" id="sidebar">
      <nav-bar></nav-bar>
      <ul>
        <li v-for="boti in bots" :key="boti.bot_id" @click="$router.push(`/chat/${boti.bot_id}`)">
          <img :src="boti.bot_foto" alt="Jakubski" >
            <h2>{{boti.bot_naam}}</h2>
        </li>
      </ul>
      <button class="hamburger-close" @click="closeSideBar">Close</button>
    </div>


      <h1>Swipe!</h1>
      <div class="card">
      <h2>{{bot.bot_naam}}</h2>
        <img :src="bot.bot_foto" alt="">
        <h4>Leeftijd: {{bot.bot_oud}}</h4>
        <h4>Geslacht: {{bot.bot_geslacht}}</h4>
        <h3>{{bot.bot_beschrijving}}</h3>
        <h4>Land: {{bot.bot_land}}</h4>
        <div class="buttons">
          <button @click="chat">Chat!</button>
          <button @click="skip" id="secondary">Skip</button>
        </div>
      </div>


  </div>
</template>
<script>
import '/src/app.css'
import axios from "axios";
import Navbar from '/src/components/Nav.vue'
import MyAlert from '/src/components/Alert.vue'

export default {
  name: 'Swipe_view',
  components: {
    'nav-bar': Navbar,
    'my-alert': MyAlert,
  },
  props:{

  },
  data() {
    return {
      user: {},
      access_token: '',
      logged_in: false,
      bot: {},
      gesprekken: [],
      bots: [],
      showalert: this.$route.params.showalert,

  }
  },
  methods: {
    openSideBar(){
      document.querySelector("#sidebar").style.display = 'block'
    },
    closeSideBar(){
      document.querySelector("#sidebar").style.display = 'none'
    },
    showAlert(message, isGood) {
      const alert = this.$refs.myAlert;
      alert.localMessage = message;
      alert.localIsGood = isGood;
      alert.showToast();
    },
    async getRandomBot(){
      try{
        let response = await axios.get('http://127.0.0.1:8000/randombot', {
          headers: {
            'Authorization': `Bearer ${this.access_token}`
          }
        })
        this.bot = response.data
        console.log(response)
        if (response.data === false){
          alert('Geen bots meer beschikbaar')
        }
      }
      catch(e){
        if(e.response === undefined){
          this.showAlert('Er is iets misgegaan probeer het nog eens', false)
        }
        else if(e.response.status === 401)
        {
          console.log(e)
          let nieuweAccestoken = await axios.get(`http://127.0.0.1:8000/refresh?gebruikersnaam=${this.user.username}`)
          this.access_token = nieuweAccestoken.data.access_token
          await this.getRandomBot()
        }
        else{
          console.log(e)
        }

      }
    },
    async skip(){
      try{
        let response = await axios.post(`http://127.0.0.1:8000/bots/gezien`, {
          "gebruiker_id": this.user.user_id,
          "bot_id": this.bot.bot_id
        }, {
          headers: {
            'Authorization': `Bearer ${this.access_token}`
          }
        })
        console.log(response)
       await this.getRandomBot()

      }
      catch(e){
        if(e.response === undefined){
          console.log(e)
          this.showalert('Er is iets misgegaan probeer het nog eens', false)
        }
        else if(e.response.status === 401){
          console.log(e)
          let nieuweAccestoken = await axios.get(`http://127.0.0.1:8000/refresh?gebruikersnaam=${this.user.username}`)
          this.access_token = nieuweAccestoken.data.access_token
          await this.skip()
        }

      }
    },
    async chat(){
      try{
        let response = await axios.post(`http://127.0.0.1:8000/gesprek`, {
          "gebruiker_id": this.user.user_id,
          "bot_id": this.bot.bot_id
        }, {
          headers: {
            'Authorization': `Bearer ${this.access_token}`
          }
        })
        let add_to_seen = await axios.post(`http://127.0.0.1:8000/bots/gezien`, {
          "gebruiker_id": this.user.user_id,
          "bot_id": this.bot.bot_id
        }, {
          headers: {
            'Authorization': `Bearer ${this.access_token}`
          }
        })
        console.log(add_to_seen)
        this.gesprekken = []
        await this.getGesprekken()
        this.bots = []
        await this.getBot()
        await this.getRandomBot()
        console.log(response)
      }
      catch(e){
        console.log(e)
        let nieuweAccestoken = await axios.get(`http://127.0.0.1:8000/refresh?gebruikersnaam=${this.user.username}`)
        this.access_token = nieuweAccestoken.data.access_token
        await this.chat()
      }
    },
    async getGesprekken(){
      try{
      let response = await axios.get(`http://127.0.0.1:8000/gesprekken/${this.user.user_id}`, {
        headers: {
          'Authorization': `Bearer ${this.access_token}`
        }
      })
      this.gesprekken = response.data
        console.log(response)
      }
      catch(e){
        console.log(e)
        let nieuweAccestoken = await axios.get(`http://127.0.0.1:8000/refresh?gebruikersnaam=${this.user.username}`)
        this.access_token = nieuweAccestoken.data.access_token
        await this.getGesprekken()
      }
    },
    async getBot(){
      try{
        for(let gesprek in this.gesprekken){
          let response = await axios.get(`http://127.0.0.1:8000/bot/${this.gesprekken[gesprek].bot_id}`, {
            headers: {
              'Authorization': `Bearer ${this.access_token}`
            }
          })
          console.log(response.data.bot_naam)
          let bot = {
            'bot_id': response.data.bot_id,
            'bot_naam': response.data.bot_naam,
            'bot_oud': response.data.bot_oud,
            'bot_land': response.data.bot_land,
            'bot_beschrijving': response.data.bot_beschrijving,
            'bot_foto': response.data.bot_foto,
            'bot_geslacht': response.data.bot_geslacht,
          }
          this.bots.push(bot)
        }
      }
      catch(e){
    console.log(e)
        let nieuweAccestoken = await axios.get(`http://127.0.0.1:8000/refresh?gebruikersnaam=${this.user.username}`)
        this.access_token = nieuweAccestoken.data.access_token
        await this.getBot()
      }
    },

  },
  async created() {
    try {
      this.logged_in = this.$store.getters.getLoggedIn;
      this.user = this.$store.getters.getUser;
      this.access_token = this.$store.getters.getAccess_Token;

      // Redirect to sign-in if not logged in
      if (!this.logged_in) {
        this.$router.push('/signin');
        return;
      }

      console.log(this.user);

      await this.getRandomBot();
      await this.getGesprekken();
      await this.getBot();

      console.log(this.bots);

      if (this.showalert === 'true') {
        this.showAlert("Ingelogd", true);
      }
    } catch (e) {
      console.error(e);
      // Check if already on sign-in page to avoid infinite loop
      if (this.$route.path !== '/signin') {
        this.$router.push('/signin');
      }
    }
  },


  async mounted() {

  }
}


</script>
<style>

</style>