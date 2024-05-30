import { createRouter, createWebHistory } from 'vue-router';
import ComingSoon from '/src/Views/ComingSoon_View.vue';

const routes = [
    { path: '/', component: ComingSoon },
];


const router = createRouter({
    history: createWebHistory(),
    routes
});


export default router;
