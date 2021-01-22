<template>
  <div class='vw-100 vh-100'>
    <div class='row m-0 p-0'>
      <div class='col-2 p-0 z-index-25'>
        <side-nav :userName='userName' :contactsList='contactsList'
          @getIndividualMessages='getIndividualMessages($event)' @getGroupMessages='getGroupMessages($event)' />
      </div>
      <div class='col-10 p-0'>
        <chat-window :currentUserId='currentUserId' :rooms='rooms' :messages='messages' :single-room='hideSideNav'
          @send-message='sendMessages($event)' height='100vh' class='chat-widget-1' :messages-loaded='messagesLoaded' />
      </div>
    </div>
  </div>
</template>

<script>
  const ChatWindow = () => import('vue-advanced-chat');
  const SideNav = () => import('../components/SideNav.vue');
  import MessageService from '../services/MessageService';
  import 'vue-advanced-chat/dist/vue-advanced-chat.css';

  export default {
    name: 'chat',
    components: {
      ChatWindow,
      SideNav,
    },
    mounted() {
      this.userName = localStorage.getItem('username') || '';
      this.getContacts();
    },
    data() {
      return {
        userName: '',
        rooms: [],
        messages: [],
        currentUserId: 1,
        contactsList: null,
        messagesLoaded: false,
        hideSideNav: true,
        roomName: '',
        skip: 0,
        limit: 50,
      };
    },
    methods: {
      checkNewMessages() {
        const scrollY = window.scrollY
        const visible = document.documentElement.clientHeight
        const pageHeight = document.documentElement.scrollHeight
        const bottomOfPage = visible + scrollY >= pageHeight
        return bottomOfPage || pageHeight < visible
      },
      async getContacts() {
        try {
          const data = await this.$http.get('/dialogs');
          this.contactsList = data.data.dialogs;
        } catch (err) {
          console.error(err);
        }
      },
      async loadOldMessages({
        room,
        options = {},
      }) {
        try {
          const {
            roomId
          } = room;
          const {
            reset = false,
          } = options;
          if (reset) {
            this.skip = 50;
            return;
          }
          const {
            skip,
            limit
          } = this;
          const data = await MessageService.getIndividualMessages({
            roomId,
            skip,
            limit,
          });
          this.currentUserId = roomId;
          this.skip = this.skip + this.limit;
          const newMessages = data.data.messages.map((d, i) => ({
            _id: Math.random() * 1000,
            content: d.message || '',
            sender_id: (roomId === d.sender ? d.sender : d.individual),
            date: this.convertDate(d.date),
            timestamp: this.convertTime(d.date),
          }));
          const rooms = [];
          rooms.push({
            roomId,
            roomName,
            users: [],
          });
          this.messages = [...newMessages, ...this.messages];
          this.rooms = rooms;
          this.messagesLoaded = true;
        } catch (err) {
          console.error(err);
        }
      },
      async getIndividualMessages({
        roomName,
        roomId
      }) {
        try {
          const {
            skip,
            limit
          } = this;
          const data = await MessageService.getIndividualMessages({
            roomId,
            skip,
            limit,
          })
          if (data.data.is_success) {
            this.skip = this.skip + this.limit;
            this.resetChatWidget();
            const requireMessageStructure = [];
            const requireRoomStructure = [];
            this.currentUserId = roomId;
            data.data.messages.map((d, i) => {
              if (d.individual != d.sender) {
                this.currentUserId = d.sender
              }
              requireMessageStructure.push({
                _id: Math.random() * 1000,
                content: d.message || '',
                sender_id: d.sender,
                date: this.convertDate(d.date),
                timestamp: this.convertTime(d.date),
              });
            });
            requireRoomStructure.push({
              roomId,
              roomName,
              users: [],
            });
            this.messages = requireMessageStructure;
            this.rooms = requireRoomStructure;
            this.messagesLoaded = true;
          }
        } catch (err) {
          console.error(err);
        }
      },
      async getGroupMessages({
        roomName,
        roomId
      }) {
        try {
          const data = await MessageService.fetchGroupMessages({
            roomId,
          })
          if (data && data.data.is_success) {
            this.resetChatWidget();
            this.currentUserId = '';
            const requireMessageStructure = [];
            const requireRoomStructure = [];
            const userList = [];
            data.data.messages.map((d, index) => {
              this.roomName = d.sender;
              userList.push({
                _id: d.id,
                username: d.sender,
              });
              requireMessageStructure.push({
                _id: d.id || '',
                content: d.message || '',
                sender_id: d.sender || '',
                date: this.convertDate(d.date),
                timestamp: this.convertTime(d.date),
                username: this.roomName,
              });
            });
            requireRoomStructure.push({
              roomId: roomId,
              roomName,
              users: userList
            });
            this.messages = requireMessageStructure;
            this.rooms = requireRoomStructure;
            this.messagesLoaded = true;
          }
        } catch (err) {
          console.error(err);
        }
      },
      async sendMessages({
        roomId,
        content,
        file,
        replyMessage
      }) {
        try {
          const data = await MessageService.addNewMessage({
            roomId,
            content,
          });
          if (data && data.status === 200) {
            this.messagesLoaded = false;
            const newMessages = [...this.messages, {
              _id: Math.random().toString(32).slice(2),
              individual: roomId,
              content,
              sender_id: this.currentUserId,
              date: this.convertDate(new Date()),
              timestamp: this.convertTime(new Date()),
              username: this.sender,
            }];
            this.messages = newMessages;
            this.messagesLoaded = true;
          }
        } catch (err) {
          console.error(err);
        }
      },
      resetChatWidget() {
        this.rooms.length = 0;
        this.messages.length = 0;
        this.messagesLoaded = false;
      },
      convertDate(date) {
        const dateString = new Date(date);
        let month = '' + (dateString.getMonth() + 1),
          day = '' + dateString.getDate(),
          year = dateString.getFullYear();
        if (month.length < 2) month = '0' + month;
        if (day.length < 2) day = '0' + day;
        return [day, month, year].join('-');
      },
      convertTime(time) {
        const timeString = new Date(time);
        return `${timeString.getHours()}:${timeString.getMinutes()}`;
      },
    },
  };
</script>

<style scoped>
</style>