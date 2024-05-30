import { createApp } from 'vue';
import router from './router';
import store from './store';
import ComingSoon_View from "@/Views/ComingSoon_View.vue";


const app = createApp(ComingSoon_View);

app.use(router);
app.use(store);

app.mount('#app');