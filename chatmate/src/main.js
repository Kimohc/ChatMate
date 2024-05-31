import { createApp } from 'vue';
import router from './router';
import store from './store';
//import ComingSoon_View from "@/Views/ComingSoon_View.vue";
//import Home from "@/Views/Home.vue";
import App from '/src/App.vue'


const app = createApp(App);

app.use(router);
app.use(store);

app.mount('#app');