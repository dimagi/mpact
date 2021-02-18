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
    name: 'bookmarks',
    component: () => import('../views/Bookmarks.vue'),
    meta: {
      auth: true,
    },
  },
  ],
});

const token = localStorage.getItem('Token');
router.beforeEach((to, from, next) => {
  if (to.name === 'login') {
    next();
  } else if (to.meta.auth && token) {
    next();
  } else {
    next();
  }
});

export default router;
