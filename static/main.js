import Vue from 'vue';
import VueTelInput from 'vue-tel-input';
import App from './App.vue';
import Api from './src/services/Api'
import router from './src/router/index';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

Vue.use(VueTelInput);

Vue.prototype.$http = Api;

new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
