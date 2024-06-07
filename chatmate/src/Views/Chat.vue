<template>
  <div id="app">
    <div class="top">
    <svg @click="$router.push('/swipe')" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M11.9481 14.8285L10.5339 16.2427L6.29126 12L10.5339 7.7574L11.9481 9.17161L10.1197 11H17.6568V13H10.1197L11.9481 14.8285Z" fill="currentColor" /><path fill-rule="evenodd" clip-rule="evenodd" d="M23 19C23 21.2091 21.2091 23 19 23H5C2.79086 23 1 21.2091 1 19V5C1 2.79086 2.79086 1 5 1H19C21.2091 1 23 2.79086 23 5V19ZM19 21H5C3.89543 21 3 20.1046 3 19V5C3 3.89543 3.89543 3 5 3H19C20.1046 3 21 3.89543 21 5V19C21 20.1046 20.1046 21 19 21Z" fill="currentColor" /></svg>
      <img :src="bot.bot_foto" alt="">
    </div>
    <div class="chat">
      <div v-for="(message) in messages" :key="message.bericht_id" :class="[message.verstuurder === 'you' ? 'bubble-you' : 'bubble-me']">
        <div class="message-container">
          <div class="message">
            <div class="dropdown-content">
              <p>{{ message.bericht }}</p>
              <div v-if="message.verstuurder === 'me'">
              <svg @click="editMessage(message.bericht_id)" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 6C4 5.44772 4.44772 5 5 5H19C19.5523 5 20 5.44772 20 6C20 6.55228 19.5523 7 19 7H5C4.44772 7 4 6.55228 4 6Z" fill="currentColor" /><path d="M4 18C4 17.4477 4.44772 17 5 17H19C19.5523 17 20 17.4477 20 18C20 18.5523 19.5523 19 19 19H5C4.44772 19 4 18.5523 4 18Z" fill="currentColor" /><path d="M5 11C4.44772 11 4 11.4477 4 12C4 12.5523 4.44772 13 5 13H13C13.5523 13 14 12.5523 14 12C14 11.4477 13.5523 11 13 11H5Z" fill="currentColor" /></svg>
              <svg @click="deleteMessage(message.bericht_id)" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.2253 4.81108C5.83477 4.42056 5.20161 4.42056 4.81108 4.81108C4.42056 5.20161 4.42056 5.83477 4.81108 6.2253L10.5858 12L4.81114 17.7747C4.42062 18.1652 4.42062 18.7984 4.81114 19.1889C5.20167 19.5794 5.83483 19.5794 6.22535 19.1889L12 13.4142L17.7747 19.1889C18.1652 19.5794 18.7984 19.5794 19.1889 19.1889C19.5794 18.7984 19.5794 18.1652 19.1889 17.7747L13.4142 12L19.189 6.2253C19.5795 5.83477 19.5795 5.20161 19.189 4.81108C18.7985 4.42056 18.1653 4.42056 17.7748 4.81108L12 10.5858L6.2253 4.81108Z" fill="currentColor" /></svg>
              </div>
              </div>
          </div>

        </div>
      </div>
    <div class="Down">
    <input type="text" v-model="message">
    <button @click="sendMessage">Send</button>
      <button>Block user</button>
    </div>
  </div>
  </div>
</template>

<script>
import axios from "axios";
//import Kebab from '/src/components/Kebab.vue'
export default {
  name: 'Chat_view',
  components: {
    //'kebab-menu': Kebab
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
      kebab_messages: [
          'Edit',
          'Delete'
      ],

    }
  },
  methods: {
    async getGesprek() {
      try {
        let response = await axios.get(`http://127.0.0.1:8000/gesprek/${this.user.user_id}/${this.bot_id}`);
        console.log(response);
        this.gesprek_id = response.data.gesprek_id;
        console.log(this.gesprek_id);
      } catch(e) {
        console.log(e);
      }
    },
    async getMessages() {
      try {
        let response = await axios.get(`http://127.0.0.1:8000/berichten/${this.gesprek_id}`);
        console.log(response);
        let messages = response.data;

        for (let message of messages) {
          let verstuurder = '';
          if (this.user.user_id === message.verstuurder_id) {
            verstuurder = 'me';
          } else {
            verstuurder = 'you';
          }
          this.messages.push({
            'bericht_id': message.bericht_id,
            'bericht': message.bericht,
            'verstuurder': verstuurder
          });
        }
        console.log(this.messages);

      } catch(e) {
        console.log(e);
      }
    },
    async sendMessage(){
      try{
        let response = await axios.post(`http://127.0.0.1:8000/berichten/`, {
          "gesprek_id": this.gesprek_id,
          "verstuurder_id": this.user.user_id,
          "bericht": this.message,
        })
        this.message = ''
        this.messages = []
        let ai_message = response.data.AI_bericht
        let ai_response = await axios.post(`http://127.0.0.1:8000/berichten/`, {
          "gesprek_id": this.gesprek_id,
          "verstuurder_id": this.bot.bot_id,
          "bericht": ai_message.content,
        })
        await this.getMessages()
        console.log(response)
        console.log(ai_response)
      }
      catch (e){
        console.log(e)
      }
    },
    async getBot(bot_id){
      try{
        let response = await axios.get(`http://127.0.0.1:8000/bot/${bot_id}`)
        this.bot = response.data
        console.log(response)
      }
      catch (e) {
        console.log(e)
      }
    },
    async deleteMessage(index){
      try{
        let response = await axios.delete(`http://127.0.0.1:8000/bericht/${index}`)
        this.messages = []
        await this.getMessages()
        console.log(response)
      }
      catch (e) {
        console.log(e)
      }
    },
    async editMessage(index){
      try{
        console.log(`message geedit ${index}`)
      }
      catch (e) {
        console.log(e)
      }
    }
  },
  created() {
  },
  async mounted() {
    this.logged_in = this.$store.getters.getLoggedIn;
    this.user = this.$store.getters.getUser;
    this.access_token = this.$store.getters.getAccess_Token;
    console.log(this.bot_id);
    await this.getGesprek();
    await this.getMessages();
    await this.getBot(this.bot_id)

  }
}
</script>

<style>
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
  scale: 2;
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
