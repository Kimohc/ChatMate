<template>
  <div id="app">
    <confirmation-modal ref="ConfirmationModal" @result="userResult" :text="modalText"></confirmation-modal>
    <my-alert ref="MyAlert"></my-alert>
    <div class="modal-overlay" v-on:click.self="closeModal">
      <div class="modal-window">

        <h2>Commentaar</h2>
        <p>{{ modalBericht }}</p>
        <input type="text" v-model="bericht">
        <button @click="editMessage(berichtId)">Pas aan</button>
        <button @click="closeModal">Close</button>
      </div>
    </div>

    <div class="top">
    <svg @click="$router.push(`/swipe/${false}`)" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M11.9481 14.8285L10.5339 16.2427L6.29126 12L10.5339 7.7574L11.9481 9.17161L10.1197 11H17.6568V13H10.1197L11.9481 14.8285Z" fill="currentColor" /><path fill-rule="evenodd" clip-rule="evenodd" d="M23 19C23 21.2091 21.2091 23 19 23H5C2.79086 23 1 21.2091 1 19V5C1 2.79086 2.79086 1 5 1H19C21.2091 1 23 2.79086 23 5V19ZM19 21H5C3.89543 21 3 20.1046 3 19V5C3 3.89543 3.89543 3 5 3H19C20.1046 3 21 3.89543 21 5V19C21 20.1046 20.1046 21 19 21Z" fill="currentColor" /></svg>
      <img :src="bot.bot_foto" alt="">
    </div>
    <div class="chat" id="chat" ref="chatContainer">
      <div v-for="(message) in messages" :key="message.bericht_id" :class="[message.verstuurder === 'you' ? 'bubble-you' : 'bubble-me']">
        <div class="message-container">
          <div class="message">
            <div class="dropdown-content">
              <p>{{ message.bericht }}</p>
              <div v-if="message.verstuurder === 'me'">
              <svg @click="toggleModal('Pas je bericht aan', message.bericht_id)" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 6C4 5.44772 4.44772 5 5 5H19C19.5523 5 20 5.44772 20 6C20 6.55228 19.5523 7 19 7H5C4.44772 7 4 6.55228 4 6Z" fill="currentColor" /><path d="M4 18C4 17.4477 4.44772 17 5 17H19C19.5523 17 20 17.4477 20 18C20 18.5523 19.5523 19 19 19H5C4.44772 19 4 18.5523 4 18Z" fill="currentColor" /><path d="M5 11C4.44772 11 4 11.4477 4 12C4 12.5523 4.44772 13 5 13H13C13.5523 13 14 12.5523 14 12C14 11.4477 13.5523 11 13 11H5Z" fill="currentColor" /></svg>
              <svg @click="deleteMessage(message.bericht_id)" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.2253 4.81108C5.83477 4.42056 5.20161 4.42056 4.81108 4.81108C4.42056 5.20161 4.42056 5.83477 4.81108 6.2253L10.5858 12L4.81114 17.7747C4.42062 18.1652 4.42062 18.7984 4.81114 19.1889C5.20167 19.5794 5.83483 19.5794 6.22535 19.1889L12 13.4142L17.7747 19.1889C18.1652 19.5794 18.7984 19.5794 19.1889 19.1889C19.5794 18.7984 19.5794 18.1652 19.1889 17.7747L13.4142 12L19.189 6.2253C19.5795 5.83477 19.5795 5.20161 19.189 4.81108C18.7985 4.42056 18.1653 4.42056 17.7748 4.81108L12 10.5858L6.2253 4.81108Z" fill="currentColor" /></svg>
              </div>
              </div>

          </div>

        </div>
      </div>
      <div v-show="showLoading">
        <h3>Typing</h3>
      </div>
    <div class="Down">
    <input @keyup.enter="sendMessage" type="text" v-model="message">
      <div v-if="showLoading">
        <button disabled> Loading</button>
      </div>
      <div v-else>
        <button @click="sendMessage">Send</button>
      </div>
      <button id="secondary" @click="confirmReserveringCancellation(gesprek_id)">Block user</button>
    </div>
  </div>
  </div>
</template>

<script>
import axios from "axios";
//import Kebab from '/src/components/Kebab.vue'
import ConfirmationModal from '/src/components/ConfirmationModal.vue'
import Alert from '/src/components/Alert.vue'
export default {
  name: 'Chat_view',
  components: {
  'confirmation-modal': ConfirmationModal,
    'my-alert': Alert,
  },
  data() {
    return {
      bot_id: this.$route.params.bot_id,
      user: {},
      logged_in: false,
      access_token: '',
      gesprek_id: 0,
      messages: [],
      message: '',
      bot: {},
      modalText: '',
      pendingGesprekId: 0,
      modalMessage: '',
      berichtId: 0,
      userid: '',
      username: '',
      bericht: '',
      modalBericht: '',
      showLoading: false,
    }
  },
  methods: {
    scrollToNewestMessage() {
      this.$nextTick(() => {
        const chatContainer = this.$refs.chatContainer;
        if (chatContainer) {
          chatContainer.scrollTop = chatContainer.scrollHeight;
        }
      });
    },
    toggleModal(message, bericht_id) {
      this.modalBericht = message
      this.berichtId = bericht_id
      document.body.classList.toggle("open-modal");
    },
    closeModal() {
      document.body.classList.remove("open-modal");
    },
    editMessage(bericht_id) {
      axios.patch(`http://127.0.0.1:8000/bericht/${bericht_id}`, {
        gesprek_id: this.gesprek_id,
        verstuurder_id: this.userid,
        bericht: this.bericht
      }, {
        headers: {
          Authorization: `Bearer ${this.access_token}`
        }
      })
          .then(response => {
            console.log(response);
            this.closeModal()
            this.messages = []
            this.getMessages(this.gesprek_id, this.user.user_id, this.messages, this.username);
          })
          .catch(async error => {
            console.error(error);
            if (error.response && error.response.status === 401) {
              try {
                const newAccessToken = await axios.get(`http://127.0.0.1:8000/refresh?gebruikersnaam=${this.username}`);
                this.access_token = newAccessToken.data.access_token;
                this.editMessage(bericht_id); // Retry the editMessage call with the new access token
              } catch (refreshError) {
                console.error(refreshError);
              }
            } else {
              this.showAlert('Er is iets mis gegaan', false)
            }
          });
    },
    showAlert(message, isGood) {
      const alert = this.$refs.MyAlert;
      alert.localMessage = message;
      alert.localIsGood = isGood;
      alert.showToast();
    },
    showConfirmationModal(message) {
      this.modalText = message
      this.$refs.ConfirmationModal.show()
    },
    confirmReserveringCancellation(gesprek_id) {
      this.showConfirmationModal("Weet je zeker dat je deze gesprek wilt beeindigen?");
      this.pendingGesprekId = gesprek_id
    },
    async userResult(result) {
      if (result === 1) {
        await this.deleteGesprek(this.pendingGesprekId);
      }
    },
    async getGesprek() {
      try {
        this.user_id = this.user.user_id
        let response = await axios.get(`http://127.0.0.1:8000/gesprek/${this.user.user_id}/${this.bot_id}`, {
          headers: {
            'Authorization': `Bearer ${this.access_token}`
          }
        });
        console.log(response);
        this.gesprek_id = response.data.gesprek_id;
        console.log(this.gesprek_id);
      } catch (e) {
        console.log(e);
        let nieuweAccestoken = await axios.get(`http://127.0.0.1:8000/refresh?gebruikersnaam=${this.user.username}`)
        this.access_token = nieuweAccestoken.data.access_token
        await this.getGesprek()
      }
    },
    async getMessages(gesprek_id, user_id, messages, username) {
      try {
        let response = await axios.get(`http://127.0.0.1:8000/berichten/${gesprek_id}`, {
          headers: {
            'Authorization': `Bearer ${this.access_token}`
          }
        });
        console.log(response);
        let messagesResponse = response.data;

        for (let message of messagesResponse) {
          let verstuurder = '';
          if (user_id === message.verstuurder_id) {
            verstuurder = 'me';
          } else {
            verstuurder = 'you';
          }

          messages.push({
            'bericht_id': message.bericht_id,
            'bericht': message.bericht,
            'verstuurder': verstuurder
          });

        }
        this.messages = messages
        console.log(messages)
        this.scrollToNewestMessage()
      } catch (e) {
        console.log(e)
        let nieuweAccestoken = await axios.get(`http://127.0.0.1:8000/refresh?gebruikersnaam=${username}`)
        this.access_token = nieuweAccestoken.data.access_token
        await this.getMessages(gesprek_id, user_id, messages, username)
      }
    },
    async sendMessage() {
      try {
          if(this.message === '' || this.message.length > 200){
            this.showAlert('Je mag geen lege bericht versturen', false)
            return
          }
        this.showLoading = true;
        let response = await axios.post(`http://127.0.0.1:8000/berichten/`, {
          "gesprek_id": this.gesprek_id,
          "verstuurder_id": this.user.user_id,
          "bericht": this.message,
        }, {
          headers: {
            'Authorization': `Bearer ${this.access_token}`
          }});

        this.messages = [];

        await this.getMessages(this.gesprek_id, this.user.user_id, this.messages, this.user.username);

        let requestToAi = await axios.post(`http://127.0.0.1:8000/request/ai`, {
          "bericht": this.message
        }, {
          headers: {
            'Authorization': `Bearer ${this.access_token}`
          }
        })
        this.message = ''
        console.log(requestToAi)
        let ai_message = requestToAi.data;
        let ai_response = await axios.post(`http://127.0.0.1:8000/berichten/`, {
          "gesprek_id": this.gesprek_id,
          "verstuurder_id": this.bot.bot_id,
          "bericht": ai_message.content,
        }, {
          headers: {
            'Authorization': `Bearer ${this.access_token}`
          }
        });
        this.messages = [];

        await this.getMessages(this.gesprek_id, this.user.user_id, this.messages, this.user.username);

        console.log(response);
        console.log(ai_response);
      } catch (e) {
        console.log(e);
        let nieuweAccestoken = await axios.get(`http://127.0.0.1:8000/refresh?gebruikersnaam=${this.user.username}`)
        this.access_token = nieuweAccestoken.data.access_token
        await this.sendMessage()
      } finally {
        // Hide loading spinner
        this.showLoading = false;
      }
    },
    async getBot(bot_id) {
      try {
        let response = await axios.get(`http://127.0.0.1:8000/bot/${bot_id}`)
        this.bot = response.data
        console.log(response)
      } catch (e) {
        console.log(e)
        let nieuweAccestoken = await axios.get(`http://127.0.0.1:8000/refresh?gebruikersnaam=${this.user.username}`)
        this.access_token = nieuweAccestoken.data.access_token
        await this.sendMessage()
      }
    },
    async deleteMessage(bericht_id) {
      try {
        let response = await axios.delete(`http://127.0.0.1:8000/bericht/${bericht_id}`, {
          headers: {
            'Authorization': `Bearer ${this.access_token}`
          }
        })
        this.messages = []
        await this.getMessages(this.gesprek_id, this.user.user_id, this.messages, this.user.username)
        console.log(response)
      } catch (e) {
        console.log(e)
        let nieuweAccestoken = await axios.get(`http://127.0.0.1:8000/refresh?gebruikersnaam=${this.user.username}`)
        this.access_token = nieuweAccestoken.data.access_token
        await this.deleteMessage(bericht_id)
      }
    },

    async deleteGesprek(gesprek_id) {
      try {
        let response = await axios.delete(`http://127.0.0.1:8000/gesprek/${gesprek_id}`, {
          headers: {
            'Authorization': `Bearer ${this.access_token}`
          }
        })
        console.log(response)
        this.$router.push(`/swipe/${false}`)
      } catch (e) {
        console.log(e)
        let nieuweAccestoken = await axios.get(`http://127.0.0.1:8000/refresh?gebruikersnaam=${this.user.username}`)
        this.access_token = nieuweAccestoken.data.access_token
        await this.deleteGesprek(gesprek_id)
      }
    },
  },
  created() {
  },
  async mounted() {
    try{ this.logged_in = this.$store.getters.getLoggedIn;
    this.user = this.$store.getters.getUser;
    this.access_token = this.$store.getters.getAccess_Token;

      if (!this.logged_in) {
        this.$router.push('/signin');
        return;
      }
    await this.getGesprek();
    await this.getMessages(this.gesprek_id, this.user.user_id, this.messages, this.user.username);
    await this.getBot(this.bot_id)
      this.scrollToNewestMessage()
      this.userid = this.user.user_id
    this.username = this.user.username
    }
    catch(e){
      console.log(e)

    }


  }
}
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

.open-modal .modal-container {
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
.chat {
  display: flex;
  flex-direction: column;
  padding: 10px;
  height: 68vh;
  overflow-y: scroll;
}
img{
  border-radius: 50%;
  width: 10%;
}
.top{
  display: flex;
  justify-content: space-between;
  margin: 10px;
}
.bubble-you {
  background-color: #DCF8C6;
  color: #000;
  border-radius: 15px;
  max-width: 70%;
  padding: 25px;
  margin: 5px;
  align-self: flex-start;
}

.bubble-me {
  background-color: #DCF0F5;
  color: #000;
  border-radius: 15px;
  max-width: 70%;
  padding: 10px;
  margin: 5px;
  align-self: flex-end;
}
.Down{
  width: 100%;
  display: flex;
  align-content: center;
  justify-content: center;
}
input{
  width: 100%;
  max-width: 600px;
  height: 45px;
  padding: 22px;
  font-size: 20px;
  border-radius: 12px;
  border: 1.5px solid lightgrey;
  outline: none;
  transition: all 0.3s cubic-bezier(0.19, 1, 0.22, 1);
  box-shadow: 0px 0px 20px -18px;
  margin: 10px;
}
input:hover {
  border: 2px solid lightgrey;
  box-shadow: 0px 0px 20px -17px;
}

input:active {
  transform: scale(0.95);
}

input:focus {
  border: 2px solid grey;
}
svg{
  margin: 20px;
  scale: 1.5;
}
.message-container {
  display: flex;
  flex-direction: row;
}
.message {
  border-radius: 5px;
  transition: background-color 0.3s;
}
.dropdown-content svg{
  scale: 1;
  transition: 0.1s;
}
.dropdown-content svg:hover{
  scale: 1.3;
  cursor: pointer;
}
.dropdown-content{
  display: flex;
  flex-direction: row;
  text-align: center;
  align-items: center;
  justify-content: center;
}

</style>
