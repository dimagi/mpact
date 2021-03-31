import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

const router = new Router({
  mode: 'history',
  routes: [{
    path: '',
    redirect: '/login',
  },
  {
    path: '/login',
    name: 'Auth',
    component: () => import('../views/Authentication.vue'),
  },
  {
    path: '/chat',
    name: 'chat',
    component: () => import('../views/Chat.vue'),
    meta: {
      auth: true,
    },
  },
  {
    path: '/flagged-messages',
    name: 'flagged_messages',
    component: () => import('../views/FlaggedMessages.vue'),
    meta: {
      auth: true,
    },
  },
  ],
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('Token');
  if (to.name === 'Auth') {
    if (token){
      router.push('/chat');
    }
    next();
  } else if (to.meta.auth && token) {
    next();
  } else {
    next();
  }
});

export default router;
