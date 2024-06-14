import { createRouter, createWebHistory } from 'vue-router';
//import ComingSoon from '/src/Views/ComingSoon_View.vue';
import Signin from "@/Views/Signin.vue";
import Home from '/src/Views/Home.vue'
import Swipe from '/src/Views/Swipe.vue'
import Profiel from '/src/Views/Profiel.vue'
import Chat from '/src/Views/Chat.vue'

const routes = [
    { path: '/', component: Home },
    {path: '/signin', component: Signin},
    {path: '/swipe/:showalert', component: Swipe},
    {path: '/profiel', component: Profiel},
    {path: '/chat/:bot_id', component: Chat}
];


const router = createRouter({
    history: createWebHistory(),
    routes
});


export default router;
