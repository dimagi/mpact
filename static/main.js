import Vue from 'vue';
import VueTelInput from 'vue-tel-input';
import jQuery from 'jquery';
import App from './App.vue';
import Toast from './src/components/Toast.vue';
import Api from './src/services/Api'
import router from './src/router/index';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

Vue.use(VueTelInput);

Vue.prototype.$http = Api;
Vue.prototype.$ = jQuery;

window.$ = jQuery;

Vue.component('Toast', Toast);

new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
