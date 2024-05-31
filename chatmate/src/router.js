import { createRouter, createWebHistory } from 'vue-router';
//import ComingSoon from '/src/Views/ComingSoon_View.vue';
import Signin from "@/Views/Signin.vue";
import Home from '/src/Views/Home.vue'
import Swipe from '/src/Views/Swipe.vue'

const routes = [
    { path: '/', component: Home },
    {path: '/signin', component: Signin},
    {path: '/swipe', component: Swipe}
];


const router = createRouter({
    history: createWebHistory(),
    routes
});


export default router;
