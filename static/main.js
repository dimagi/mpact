import Vue from 'vue';
import App from './App.vue';
import Toast from './src/components/Toast.vue';
import Api from './src/services/Api'
import router from './src/router/index';
import 'bootstrap/dist/css/bootstrap.min.css';
import store from './store'
import dateHelpers from './src/utils/helpers/dateHelpers';

Vue.prototype.$http = Api;

Vue.component('Toast', Toast);


new Vue({
  el: '#app',
  data: {
    connected: false
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
      const activeChannel = this.$store.state.active_channel
      // IF the new message isn't from the current room, just update the unread count and ignore the message
      if (activeChannel.toString() !== newMessage.room_id.toString()) {
        const currentUnreadMessages = this.$store.state.unread_messages
        currentUnreadMessages[newMessage.room_id] = currentUnreadMessages[newMessage.room_id] + 1
        this.$store.dispatch('update_unread_messages', currentUnreadMessages)
      }
      // Otherwise, let's add it to our messages array in the store so it displays on screen
      else {
        newMessage._id = newMessage.id,
        newMessage.content = newMessage.message
        newMessage.timestamp = dateHelpers.convertTime(newMessage.date)
        newMessage.date = dateHelpers.convertDate(newMessage.date)
        newMessage.username = newMessage.sender_name
        newMessage.roomId = newMessage.room_id
        currentMessages.push(newMessage)
        this.$store.dispatch('update_messages', {roomId: activeChannel, msgs: currentMessages})
      }
    }

    socket.onclose = event => {
      // We consume this in chat.vue to display an alert. It's not ideal but it works
      this.connected = false
    }

  },
  store,
  router,
  render: h => h(App)
})