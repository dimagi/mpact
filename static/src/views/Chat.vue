<template>
  <div class='vw-100 vh-100'>
    <!-- The toasts library we use doesn't have the concept of permanent alerts. Not worth trying to do it there for something so simple -->
    <div class="alert alert-danger pinned-alert position-absolute" role="alert" v-show="!this.$root.connected">
      Not connected to server! If it does not resolve shortly, please <a href="javascript:window.location.reload()">refresh</a> the page.
    </div>
    <chat-window 
      height='100vh' 
      :currentUserId='currentUserId' 
      :rooms='rooms'
      :room-id='roomId'
      :messages='messages' 
      :messages-loaded='messagesLoaded' 
      :rooms-loaded='roomsLoaded'
      :styles='styles'
      :show-footer='showFooter'
      :message-actions='messageActions'
      @fetch-messages='changeChat($event)' 
      @send-message='sendMessage($event)' 
      @message-action-handler='messageActionHandler($event)'
      :text-messages='textMessages'
      :load-first-room='false' :show-files='false' :show-audio='false' :show-reaction-emojis='false' :show-add-room='false'>
      <template #dropdown-icon>
        <svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='currentColor' viewBox='0 0 16 16'>
          <path fill-rule='evenodd' d='M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z' />
        </svg>
      </template>
      <template v-slot:rooms-header>
        <rooms-list-header />
      </template>
      <template v-slot:room-list-item="{room}">
        <div :class="['vac-title-container','mpact-custom-room-list-item', room.type]">
          {{room.roomName}} <span class="badge alert-warning unread-count" v-if="room.unreadCount">{{room.unreadCount}}</span>
        </div>
      </template>
      <template v-slot:messages-empty>
        <template v-if="roomId===flaggedMsgsId"><flagged-messages-list :flaggedMessages="flaggedMessages"/></template>
        <template v-else>{{ textMessages.MESSAGES_EMPTY }}</template>
      </template>
    </chat-window>
  </div>
</template>

<script>
/* eslint-disable import/no-named-as-default-member */
import Vue from 'vue';
import MessageService from '../services/MessageService';
import dateHelpers from '../utils/helpers/dateHelpers';
import 'vue-advanced-chat/dist/vue-advanced-chat.css';
import RoomsListHeader from '../components/RoomsListHeader.vue';
import FlaggedMessagesList from '../components/FlaggedMessagesList.vue';

const ChatWindow = () => import('vue-advanced-chat');

export default {
  name: 'chat',
  components: {
    ChatWindow,
    RoomsListHeader,
    FlaggedMessagesList
  },
  data() {
    return {
      rooms: [],
      roomId: '',
      currentUserId: 1,
      groupAndIndividualChats: [],
      messagesLoaded: false,
      roomsLoaded: false,
      roomName: '',
      showFooter: true, // This is the text entry box for messages
      batchSize: 50,
      offset: 0,
      flaggedMsgsId: "flaggedMsgs",
      flaggedMessages: [],
      textMessages: {
        ROOMS_EMPTY: 'Add your configured bot to a Telegram group and refresh to get started',
        ROOM_EMPTY: 'No group or individual chat selected',
        MESSAGES_EMPTY: 'No messages',
      },
      messageActions: [{
          name: 'flagMessage',
          title: 'Flag Message',
        }, {
          name: 'replyMessage',
          title: 'Reply',
        }
      ],
      styles: {
        icons: {
          dropdownMessageBackground: 'transparent',
        },
      },
    };
  },
  computed: {
    messages: {
      get() {
        return this.$store.state.messages;
      },
      set(payload) {
        this.$store.dispatch('update_messages', {roomId: this.selectedRoom, msgs: payload});
      }
    },
    chatId() {
      return this.$route.query.chatId || null;
    },
    scrollToMsgId() {
      return this.$route.query.messageId;
    },
    unreadMessagesMap() {
      return this.$store.state.unread_messages;
    }
  },
  watch:{
    chatId(to, from) {
      if(this.roomId !== this.chatId) {
        // Updating the roomId will cause changeChat to be called
        this.roomId = this.chatId;
        this.offset = 0;
      }
    },
    roomId(to,from) {
      this.$store.dispatch('update_active_channel',{activeChannel: to});
    },
    unreadMessagesMap: {
      handler(to,from) {
        for(const [rId, unreadCount] of Object.entries(to)) {
          try {
            const updateRoom = this.rooms.find((r) => r.roomId === rId);
            updateRoom.unreadCount = unreadCount;
          } catch(err) {
            console.error(err);
          }
        }
      },
      deep: true // required since we're watching an object
    }
  },
  async mounted() {
    this.resetChatWidget();
    await this.getGroupAndIndividualChats();
    if(this.chatId) {
      this.roomId = this.chatId;
    }
  },
  destroyed(){
    this.resetChatWidget();
  },
  methods: {
    async messageActionHandler({ roomId, action, message }) {
      try {
        const options = { roomId, message };
        switch (action.name) {
        case 'flagMessage':
          this.flagMessage(options);
          break;
        case 'replyMessage':
          this.replyMessage(options);
          break;
        }
      } catch (err) {
        console.error(err);
      }
    },
    async getGroupAndIndividualChats() {
      try {
        const response = await this.$http.get('/dialogs');
        this.groupAndIndividualChats = response.data.dialogs;
        const unreadMessagesObj = {}
        this.groupAndIndividualChats.forEach((oneGroup) => {
          oneGroup.bot.bot_individuals.forEach((oneIndividual) => {
            unreadMessagesObj[oneIndividual.individual.id] = oneIndividual.individual.unread_count;
          });
          unreadMessagesObj[oneGroup.chat.id] = oneGroup.chat.unread_count;
        });
        this.$store.dispatch('update_unread_messages', unreadMessagesObj)

        // NOTE: We are abusing the user property for these rooms. By faking 
        // three users, we are forcing the library to always show sender / usernames 
        // with messages. We aren't passing a real list of users because we are
        // not currently using any of the functionality.
        const userMap = {}
        const fakeUsers = [
          {_id:1,username:"fake1"},
          {_id:2,username:"fake2"},
          {_id:3,username:"fake3"},
        ];
        // Fake first 'room' is the flagged messages list
        const formattedRoomStructure = [{
          roomId: this.flaggedMsgsId,
          roomName: "🏳️ Flagged Messages",
          unreadCount: 0,
          type: 'flagged-msgs',
          users: fakeUsers,
        }];
        this.groupAndIndividualChats.forEach((d) =>{
          formattedRoomStructure.push({
            roomId: d.chat['id'].toString(),
            roomName: d.chat['title'],
            unreadCount: d.chat['unread_count'],
            type: 'group-chat',
            botId: d.bot['id'],
            users: fakeUsers});
          d.bot.bot_individuals.forEach((i) =>{
            userMap[i.individual.id] ={
              roomId: i.individual.id.toString(),
              roomName: i.individual.first_name,
              type: 'individual-chat',
              botId: d.bot['id'],
              users: fakeUsers};
          });
        });
        // Even if a user is in multiple group chats, put 'em in the room list once.
        for(let key in userMap) {
          formattedRoomStructure.push(userMap[key]);
        }
        this.rooms = formattedRoomStructure;
        this.roomsLoaded = true;
      } catch (err) {
        console.error(err);
      }
    },
    async fetchMessages(){
      try {
        this.messagesLoaded = false;
        // Not ideal, but basically we're going to abuse the plugin again.
        // When we enter the flagged messages room, we are going to tell the plugin
        // that there are no messages so that it tries to display the "messages empty"
        // text, but we hijack it in the template to display a custom component
        // that uses the flaggedMessages list to create a table of flagged messages.
        const isFlaggedMessages = (this.roomId === this.flaggedMsgsId);
        this.showFooter = !isFlaggedMessages;

        const response = isFlaggedMessages ? 
                await MessageService.fetchFlaggedMessages({}) : 
                await MessageService.fetchMessages(this.roomId, this.offset, this.batchSize);
        
        if (!response || !response.data.is_success) {
          this.$toasts.error('There was an issue fetching new messages!');
          return;
        }

        // Weak support for rooms with custom bots
        const currentRoom = this.rooms.find((r) => r.roomId === this.roomId);
        this.currentUserId = currentRoom.botId;

        const messages = isFlaggedMessages ? response.data.flagged_messages : response.data.messages;
        if (messages.length < this.batchSize) {
          this.messagesLoaded = true;
        }
        const formattedMessages = isFlaggedMessages ? [] : this._processMessages(messages);
        this.flaggedMessages = isFlaggedMessages ? this._processFlaggedMessages(messages) : [];
        if (this.offset >= this.batchSize) {
          // We are loading old messages
          this.messages = [...formattedMessages, ...this.messages];
        } else {
          this.messages = formattedMessages;
          if(this.scrollToMsgId) {
            // We are trying to jump to a specific message. We need to wait until
            // nextTick so that the DOM is updated.
            // Then there's a bit of a hack that we set a timer and w/ a 200ms delay
            // to do the scrolling. This is because internally there is some scrolling
            // that happens in the plugin. We need to wait for it to finish before we 
            // jump to the particular message.
            this.$nextTick(()=> {
                setTimeout(
                  () => document.getElementById(this.scrollToMsgId).scrollIntoView({behavior:'smooth'}), 
                  200
                );
              });
          }
        }
        this.offset += messages.length;
      } catch (err) {
        console.error(err);
      }
    },
    _processFlaggedMessages(messages) {
      const formattedMessages = [];
      messages.forEach((d) => {
        const roomSource = this.rooms.find((r) => r.roomId === d.message.room_id.toString()) || {roomName:'<unknown chat>'};

        formattedMessages.push({
          _id: d.id,
          messageId: d.message.id,
          firstName: d.message.sender_name || '',
          content: d.message.message || '',
          date: dateHelpers.convertDateTime(d.date),
          roomId: d.message.room_id,
          roomName: roomSource.roomName,
        });
      });
      return formattedMessages;
    },
    _processMessages(messages) {
      const formattedMessages = [];
      messages.forEach((m) => {
        formattedMessages.push({
          _id: m.id || '',
          messageId: m.message.id || '',
          content: m.message || '',
          sender_id: m.sender_id || '',
          date: dateHelpers.convertDate(m.date),
          timestamp: dateHelpers.convertTime(m.date),
          username: m.sender_name, 
          isFlagged: m.is_flagged,
          roomId: this.roomId,
        });
      });
      return formattedMessages;
    },
    async flagMessage({ roomId, message }) {
      // TODO: clean up flag messages code
      try {
        const params = {
          message: message._id,
          groupId: message.groupId || this.groupId,
        };
        const trimmedMessage = message.content.trim().length > 25 ? `${message.content.trim().slice(0, 25)}...` : message.content.trim();
        if (!message.isFlagged) {
          const result = await MessageService.flagMessage(params);
          if (result && result.data.is_success) {
            const messageIndex = this.messages.findIndex(
              (m) => m._id === params.message,
            );
            Vue.set(this.messages, messageIndex, {
              ...message,
              isFlagged: true,
              saved: false,
            });
            this.$toasts.success(`${trimmedMessage} successfully flagged!`);
          }
        } else {
          this.$toasts.base(`${trimmedMessage} is already flagged!`);
        }
      } catch (err) {
        console.error(err);
      }
    },
    async replyMessage({ roomId, message }) {
      try {
        const params = {};
        console.info('replyMessage', roomId, message);
      } catch (err) {
        console.error(err);
      }
    },
    async changeChat({room}) {
      const newChatId = room.roomId;

      if(this.chatId === newChatId) {
        // One could imagine caching messages in the future to speed things up.
        this.fetchMessages();
      } else { 
        // First time through we will update history. This will cause changeChat 
        // to be called a second time where we'll actually fetch the msgs
        this.$router.push({path:'/chat/', query: { chatId: newChatId }});
      }
    },
    async sendMessage({ roomId, content, file, replyMessage }) {
      try {
        const response = await MessageService.addNewMessage({
          roomId,
          content,
          file,
          replyMessage,
        });
      } catch (err) {
        console.error(err);
      }
    },
    resetChatWidget() {
      this.rooms.length = 0;
      this.messages.length = 0;
      this.messagesLoaded = false;
      this.offset = 0;
    },
  },
};
</script>
<style scoped>
/* A little CSS hack to add some custom styles */
.vac-room-item > .mpact-custom-room-list-item {
  /* Repeat the parent CSS properties */
  position: relative;
  min-height: 71px;
  border-radius: 8px;
  padding: 0 16px;
  display: flex;
  flex: 1 1 100%;
  align-items: center;

  color: black;

  /* A little CSS hack to cover the list item */
  left: -16px;
  margin-right: -32px;
}

.vac-room-item > .flagged-msgs {
  background-color: #717579 ;
  color: #fff;
}
.vac-room-item > .flagged-msgs:hover,
.vac-room-selected > .flagged-msgs {
  background-color: #343a40; /* bg-dark */
}

.vac-room-item > .group-chat {
  background-color: #F6FDF7;
}

.vac-room-item > .individual-chat {
  background-color: #F6F9FD;
}

/* Tetradic https://www.canva.com/colors/color-wheel/  */
.vac-room-item > .group-chat:hover,
.vac-room-selected > .group-chat {
  background-color: #E5FAE6;
}
.vac-room-item > .individual-chat:hover,
.vac-room-selected > .individual-chat {
  background-color: #CCDDF4;
}

.unread-count {
  margin-left: auto;
}

.pinned-alert {
  left: 0;
  right: 0;
  z-index: 99999;
}
</style>