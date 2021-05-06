import Vue from 'vue';
import VueTelInput from 'vue-tel-input';
import jQuery from 'jquery';
import App from './App.vue';
import Toast from './src/components/Toast.vue';
import Api from './src/services/Api'
import router from './src/router/index';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import store from './store'
import _ from 'lodash'
import MessageService from './src/services/MessageService';
import dateHelpers from './src/utils/helpers/dateHelpers';

Vue.use(VueTelInput);

Vue.prototype.$http = Api;
Vue.prototype.$ = jQuery;

window.$ = jQuery;

Vue.component('Toast', Toast);


new Vue({
  el: '#app',
  data: {
    connections: 0
  },
  mounted() {
    const socket = new WebSocket(
      'ws://' + window.location.host +'/ws/connection', [], { "X-Auth-Token": {"Authorization": window.localStorage.Token}})
    this.$store.dispatch('update_websocket', socket)
    socket.onopen = event => {
        this.connected = true
        socket.send({})
    }

    socket.onmessage = async event => {
      const currentMessages = this.$store.state.messages
      const newMessage = JSON.parse(event.data).message
      const id = newMessage.id
      newMessage._id = newMessage.id,
      newMessage.content = newMessage.message
      newMessage.timestamp = dateHelpers.convertTime(newMessage.date)
      newMessage.date = dateHelpers.convertDate(newMessage.date)
      newMessage.username = newMessage.sender_name
      newMessage.roomId = newMessage.room_id
      currentMessages.push(newMessage)
      const activeChannel = this.$store.state.active_channel
      if (activeChannel !== newMessage.room_id) {
        const currentUnreadMessages = this.$store.state.unread_messages
        currentUnreadMessages[newMessage.room_id] = currentUnreadMessages[newMessage.room_id] + 1
        this.$store.dispatch('update_unread_messages', currentUnreadMessages)
      }
      else {
        const params = {
          roomId: newMessage.room_id,
          offset: 0,
          limit: 50
        }
        const data = await MessageService.getIndividualMessages(params);
      }
      this.$store.dispatch('update_messages', {roomId: activeChannel, msgs: currentMessages})
    }

    socket.onclose = event => {
      console.log('websocket connection closed')
      this.connected = false
    }

  },
  store,
  router,
  render: h => h(App)
})