<template>
  <div id="app">
    <nav-bar :profiel="true"></nav-bar>
    <my-alert ref="MyAlert"></my-alert>
    <confirmation-modal ref="ConfirmationModal" @result="userResult" :text="modalText"></confirmation-modal>
    <main>
      <div class="profile-container" >
        <div class="profile-pic">
        <img :src="image" alt="" id="profile-foto">
        </div>
        <div class="profile-info">
        <div class="folder">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M3.00977 5.83789C3.00977 5.28561 3.45748 4.83789 4.00977 4.83789H20C20.5523 4.83789 21 5.28561 21 5.83789V17.1621C21 18.2667 20.1046 19.1621 19 19.1621H5C3.89543 19.1621 3 18.2667 3 17.1621V6.16211C3 6.11449 3.00333 6.06765 3.00977 6.0218V5.83789ZM5 8.06165V17.1621H19V8.06199L14.1215 12.9405C12.9499 14.1121 11.0504 14.1121 9.87885 12.9405L5 8.06165ZM6.57232 6.80554H17.428L12.7073 11.5263C12.3168 11.9168 11.6836 11.9168 11.2931 11.5263L6.57232 6.80554Z" fill="currentColor" /></svg>
          <input type="email" placeholder="E-mail" required v-model="email">
        </div>
        <div class="folder">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M16 7C16 9.20914 14.2091 11 12 11C9.79086 11 8 9.20914 8 7C8 4.79086 9.79086 3 12 3C14.2091 3 16 4.79086 16 7ZM14 7C14 8.10457 13.1046 9 12 9C10.8954 9 10 8.10457 10 7C10 5.89543 10.8954 5 12 5C13.1046 5 14 5.89543 14 7Z" fill="currentColor" /><path d="M16 15C16 14.4477 15.5523 14 15 14H9C8.44772 14 8 14.4477 8 15V21H6V15C6 13.3431 7.34315 12 9 12H15C16.6569 12 18 13.3431 18 15V21H16V15Z" fill="currentColor" /></svg>
          <input type="text" placeholder="Username" required v-model="username">
        </div>
        <div class="folder">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M18 10.5C19.6569 10.5 21 11.8431 21 13.5V19.5C21 21.1569 19.6569 22.5 18 22.5H6C4.34315 22.5 3 21.1569 3 19.5V13.5C3 11.8431 4.34315 10.5 6 10.5V7.5C6 4.18629 8.68629 1.5 12 1.5C15.3137 1.5 18 4.18629 18 7.5V10.5ZM12 3.5C14.2091 3.5 16 5.29086 16 7.5V10.5H8V7.5C8 5.29086 9.79086 3.5 12 3.5ZM18 12.5H6C5.44772 12.5 5 12.9477 5 13.5V19.5C5 20.0523 5.44772 20.5 6 20.5H18C18.5523 20.5 19 20.0523 19 19.5V13.5C19 12.9477 18.5523 12.5 18 12.5Z" fill="currentColor" /></svg>
          <input type="password" placeholder="Password" required v-model="password">
        </div>
        <div class="folder">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M7 7C5.34315 7 4 8.34315 4 10C4 11.6569 5.34315 13 7 13C8.65685 13 10 11.6569 10 10C10 8.34315 8.65685 7 7 7ZM6 10C6 9.44772 6.44772 9 7 9C7.55228 9 8 9.44772 8 10C8 10.5523 7.55228 11 7 11C6.44772 11 6 10.5523 6 10Z" fill="currentColor" /><path fill-rule="evenodd" clip-rule="evenodd" d="M3 3C1.34315 3 0 4.34315 0 6V18C0 19.6569 1.34315 21 3 21H21C22.6569 21 24 19.6569 24 18V6C24 4.34315 22.6569 3 21 3H3ZM21 5H3C2.44772 5 2 5.44772 2 6V18C2 18.5523 2.44772 19 3 19H7.31374L14.1924 12.1214C15.364 10.9498 17.2635 10.9498 18.435 12.1214L22 15.6863V6C22 5.44772 21.5523 5 21 5ZM21 19H10.1422L15.6066 13.5356C15.9971 13.145 16.6303 13.145 17.0208 13.5356L21.907 18.4217C21.7479 18.7633 21.4016 19 21 19Z" fill="currentColor" /></svg>
          <input type="file" ref="fileInput" name="file">
        </div>
        <div class="folder">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M8 11C7.44772 11 7 11.4477 7 12C7 12.5523 7.44772 13 8 13H15.9595C16.5118 13 16.9595 12.5523 16.9595 12C16.9595 11.4477 16.5118 11 15.9595 11H8Z" fill="currentColor" /><path d="M8.04053 15.0665C7.48824 15.0665 7.04053 15.5142 7.04053 16.0665C7.04053 16.6188 7.48824 17.0665 8.04053 17.0665H16C16.5523 17.0665 17 16.6188 17 16.0665C17 15.5142 16.5523 15.0665 16 15.0665H8.04053Z" fill="currentColor" /><path fill-rule="evenodd" clip-rule="evenodd" d="M5 3C3.89543 3 3 3.89543 3 5V19C3 20.1046 3.89543 21 5 21H19C20.1046 21 21 20.1046 21 19V5C21 3.89543 20.1046 3 19 3H5ZM7 5H5L5 19H19V5H17V6C17 7.65685 15.6569 9 14 9H10C8.34315 9 7 7.65685 7 6V5ZM9 5V6C9 6.55228 9.44772 7 10 7H14C14.5523 7 15 6.55228 15 6V5H9Z" fill="currentColor" /></svg>          <input type="text" v-model="beschrijving">
        </div>
          <div class="profile-buttons">
        <button @click="pasaan">Pas aan</button>
        <button @click="confirmReserveringCancellation">Verwijder</button>
          </div>
      </div>
      </div>



    </main>

  </div>
</template>
<script>
import '/src/app.css'
import Navbar from '/src/components/Nav.vue'
import axios from "axios";
import MyAlert from '/src/components/Alert.vue'
import ConfirmationModal from '/src/components/ConfirmationModal.vue'

export default {
  name: 'Profiel_view',
  components: {
    'nav-bar': Navbar,
    'my-alert': MyAlert,
    'confirmation-modal': ConfirmationModal,

  },
  data() {
    return {
      email: '',
      username: '',
      password: '',
      file: '',
      beschrijving: '',
      logged_in: false,
      user: {},
      access_token: '',
      image: '',
      modalText: '',
    }
  },
  methods: {
    showAlert(message, isGood) {
      const alert = this.$refs.MyAlert;
      alert.localMessage = message;
      alert.localIsGood = isGood;
      alert.showToast();
    },
    showConfirmationModal(message){
      this.modalText = message
      this.$refs.ConfirmationModal.show()
    },
    confirmReserveringCancellation() {
      this.showConfirmationModal("Weet je zeker dat je deze account wilt annuleren?");
    },
    async userResult(result) {
      if (result === 1) {
        await this.verwijderUser(this.user.user_id);
      }
    },
    async pasaan() {
      try {
        if (this.email && this.username && this.password && this.beschrijving && this.email.length < 50 && this.username.length < 50 && this.password.length < 50 && this.beschrijving.length < 900) {
          let response = await axios.patch(`http://127.0.0.1:8000/gebruiker/${this.user.user_id}`, {
            "e_mail": this.email,
            "gebruikersnaam": this.username,
            "wachtwoord": this.password,
            "beschrijving": this.beschrijving,
          },
              {
            headers: {
              'Authorization': `Bearer ${this.access_token}`
            }
              })
          if (this.$refs.fileInput.files[0]) {
            await this.voegFoto();
          }
          await this.getFoto()
          console.log(response)
          this.showAlert('Gelukt', true)
          this.password = ''
          let userInfo = await this.getUserInfo()
          this.user.username = userInfo.data.gebruikersnaam
          this.user.beschrijving = userInfo.data.beschrijving
          this.user.password = userInfo.data.wachtwoord
          this.user.e_mail = userInfo.data.e_mail

          this.$store.commit('setUser', this.user);

        }
        else{
          this.showAlert('vul alle velden in', false)
        }
      } catch (error) {

        if (error.response === undefined) {
          this.showAlert('Account met deze gebruikersnaam of e-mail bestaat al.', false);
          console.log(error);
        }
        if(error.response === 401){
          console.log(error)
          let nieuweAccestoken = await axios.get(`http://127.0.0.1:8000/refresh?gebruikersnaam=${this.username}`)
          this.access_token = nieuweAccestoken.data.access_token
          await this.pasaan()
        }
        else{
          this.showAlert('Er is iets misgegaan probeer het nog eens', false)
        }

      }
    },
    async voegFoto() {
      try{
        const formData = new FormData();
        formData.append('file', this.$refs.fileInput.files[0]);
        let response = await axios.post(`http://127.0.0.1:8000/gebruiker/image/${this.user.user_id}`, formData, {
          headers: {
            'Authorization': `Bearer ${this.access_token}`
          }
        })
        console.log(response)
      }
catch(e){

      console.log(e.response.status)
}

    },
    async getFoto(){
      try{
        let response = await axios.get(`http://127.0.0.1:8000/gebruiker/${this.user.user_id}/image`,
            {
              responseType: 'arraybuffer',
              headers: {
                'Authorization': `Bearer ${this.access_token}`
              }});
        console.log(response);
        if (response.status === 200){
          const imageData = new Uint8Array(response.data);
          const blob = new Blob([imageData], { type: 'image/jpeg' });
          const imageUrl = URL.createObjectURL(blob);
          this.image = imageUrl
        }
      }
      catch (error){
        console.log(error)
        let nieuweAccestoken = await axios.get(`http://127.0.0.1:8000/refresh?gebruikersnaam=${this.username}`)
        this.access_token = nieuweAccestoken.data.access_token
        await this.getFoto()
      }
    },
    async verwijderUser(){
      try{
        let response = await axios.delete(`http://127.0.0.1:8000/gebruiker/${this.user.user_id}`, {
          headers: {
            'Authorization': `Bearer ${this.access_token}`
          }
        })
        console.log(response)
        this.showAlert('User verwijdert', true)
        this.$store.commit('setLoggedIn', false);
        this.$store.commit('setAccess_Token', null);
        this.$store.commit('setUser', null);
        this.$router.push('/')
      }
      catch(error){
        console.log(error)
        let nieuweAccestoken = await axios.get(`http://127.0.0.1:8000/refresh?gebruikersnaam=${this.username}`)
        this.access_token = nieuweAccestoken.data.access_token
        await this.verwijderUser()
      }
    },
    async getUserInfo(){
      try{
        let response = await axios.get(`http://127.0.0.1:8000/gebruiker/${this.user.user_id}`)
        console.log(response.data)
        return response
      }
      catch (e) {
        console.log(e)
      }
    }
  },
  created() {
  },
  mounted() {
    try{
      this.logged_in = this.$store.getters.getLoggedIn
      this.user = this.$store.getters.getUser
      this.access_token = this.$store.getters.getAccess_Token

      if (!this.logged_in) {
        this.$router.push('/signin');
        return;
      }

      this.getFoto()
      this.username = this.user.username
      this.email = this.user.e_mail
      this.beschrijving = this.user.beschrijving
      console.log(this.access_token)
    }
    catch (e) {
    console.log(e)
      if (this.$route.path !== '/signin') {
        this.$router.push('/signin');
      }
    }
    
  }
}


</script>
<style>

</style>