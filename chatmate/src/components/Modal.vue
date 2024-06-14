<template>
  <div v-if="showCommentaar" class="modal-overlay" v-on:click.self="closeModal">
    <div class="modal-window">

      <h2>Commentaar</h2>
      <p>{{ message }}</p>
      <input type="text" v-model="bericht">
      <button @click="editMessage(berichtid)">Pas aan</button>
      <button @click="closeModal">Close</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Chat from '/src/Views/Chat.vue'
export default {
  name: 'MyModal',
  props: ['message', 'berichtid', 'gesprekid', 'verstuurderid', 'messages', 'username'],
  data() {
    return {
      showCommentaar: false,
      bericht: '',
      messagesToGet: this.messages
    };
  },
  methods: {
    toggleModal() {
      this.showCommentaar = !this.showCommentaar;
      document.body.classList.toggle("open-modal");
    },
    closeModal() {
      this.showCommentaar = false;
      document.body.classList.remove("open-modal");
    },
    async editMessage(bericht_id){
      try{
        let response = await axios.patch(`http://127.0.0.1:8000/bericht/${bericht_id}`, {
          "gesprek_id": this.gesprekid,
          "verstuurder_id": this.verstuurderid,
          "bericht": this.bericht
        }, {
          headers: {
            'Authorization': `Bearer ${this.access_token}`
          }
        })
        console.log(response)
        this.messagesToGet = []
        this.showCommentaar = false
        await Chat.methods.getMessages(this.gesprekid, this.verstuurderid, this.messagesToGet, this.username)
      }
      catch (e) {
        console.log(e)
        let nieuweAccestoken = await axios.get(`http://127.0.0.1:8000/refresh?gebruikersnaam=${this.username}`)
        this.access_token = nieuweAccestoken.data.access_token
        await this.editMessage(bericht_id)
      }
    },
  },
  mounted() {
    this.logged_in = this.$store.getters.getLoggedIn;
    this.user = this.$store.getters.getUser;
    this.access_token = this.$store.getters.getAccess_Token;
  }
};
</script>
<style>
.modal-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  opacity: 0;
  visibility: hidden;
  background: rgba(0, 0, 0, 0.25);
}

body.open-modal .modal-container {
  visibility: visible;
  opacity: 1;
}

.main-container,
.modal-window,
.modal-container {
  transition: 0.2s;
}

.modal-window {
  text-align: center;
  position: fixed;
  top: 50%;
  left: 50%;
  background: #ffffff;
  color: #000000;
  padding: 48px 40px;
  width: 800px;
  border-radius: 12px;
  translate: -50% -50%;
  scale: 1;
  opacity: 0;
  visibility: hidden;
}
.modal-window p {
  font-size: 15px;
}
body.open-modal > .main-container {
  scale: 0.75;
}

body.open-modal .modal-window {
  opacity: 1;
  visibility: visible;
  animation: modal-window-in 0.5s;
}


@keyframes modal-window-in {
  0% {
    translate: -50% 10%;
    scale: 0.5;
  }
  100% {
    opacity: 1;
    scale: 1;
    visibility: visible;
  }
}
</style>