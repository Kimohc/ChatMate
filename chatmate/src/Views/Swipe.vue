<template>
  <div id="app">
    <my-alert ref="myAlert"></my-alert>
    <div class="sidebar">
      <nav-bar></nav-bar>
      <ul>
        <li v-for="boti in bots" :key="boti.bot_id" @click="$router.push(`/chat/${boti.bot_id}`)">
          <img :src="boti.bot_foto" alt="Jakubski" >
            <h2>{{boti.bot_naam}}</h2>
        </li>
      </ul>
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
      }
      catch(e){
        console.log(e)
        let nieuweAccestoken = await axios.get(`http://127.0.0.1:8000/refresh?gebruikersnaam=${this.user.username}`)
        this.access_token = nieuweAccestoken.data.access_token
        await this.getRandomBot()
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
        console.log(e)
        let nieuweAccestoken = await axios.get(`http://127.0.0.1:8000/refresh?gebruikersnaam=${this.user.username}`)
        this.access_token = nieuweAccestoken.data.access_token
        await this.skip()
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