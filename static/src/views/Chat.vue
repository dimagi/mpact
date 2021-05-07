<template>
  <div class='vw-100 vh-100'>
    <Toast :text='toastMessage' :hasError='showToastError' />
    <chat-window 
      height='100vh' 
      :currentUserId='currentUserId' 
      :rooms='rooms'
      :room-id='roomId'
      :messages='messages' 
      :messages-loaded='messagesLoaded' 
      :rooms-loaded='roomsLoaded'
      :styles='styles'
      :message-actions='messageActions'
      @fetch-messages='messages.length>=50 ? loadOldMessages($event) : changeChat($event)' 
      :showNewMessagesDivider='showNewMessagesDivider'
      @send-message='sendMessage($event)' 
      @message-action-handler='messageActionHandler($event)'
      :text-messages='textMessages'
      :load-first-room='false' :show-files='false' :show-audio='false' :show-reaction-emojis='false' :show-add-room='false'>
      <template #dropdown-icon>
        <svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='currentColor' viewBox='0 0 16 16'>
          <path fill-rule='evenodd' d='M1.646 4.646a.5.5 0 0 1 .708 0L8
          10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6
            6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z' />
        </svg>
      </template>
      <template v-slot:rooms-header>
        <!-- TODO: Add back the buttons from SideNav here -->
        <!-- Probably best to make it a separate compontent -->
      </template>
      <template v-slot:room-list-item="{room}">
        <div :class="['vac-title-container','mpact-custom-room-list-item', room.type]">
          {{room.roomName}} <span class="badge alert-warning unread-count" v-if="room.unreadCount">{{room.unreadCount}}</span>
        </div>
      </template>
    </chat-window>
  </div>
</template>

<script>
/* eslint-disable import/no-named-as-default-member */
import Vue from 'vue';
import MessageService from '../services/MessageService';
import ToastMixin from '../mixins/ToastMixin';
import dateHelpers from '../utils/helpers/dateHelpers';
import 'vue-advanced-chat/dist/vue-advanced-chat.css';

const ChatWindow = () => import('vue-advanced-chat');
const SideNav = () => import('../components/SideNav.vue');

export default {
  name: 'chat',
  components: {
    ChatWindow,
    SideNav,
  },
  mixins: [ToastMixin],
  data() {
    return {
      username: '',
      toastMessage: '',
      showToastError: false,
      rooms: [],
      roomId: '',
      currentUserId: 1,
      groupAndIndividualChats: [],
      messagesLoaded: false,
      roomsLoaded: false,
      roomName: '',
      limit: 50,
      groupView: true,
      offset: 0,
      lastMessage: null,
      showNewMessagesDivider: false,
      textMessages: {
        ROOMS_EMPTY: 'Add your configured bot to a Telegram group and refresh to get started',
        ROOM_EMPTY: 'No group or individual chat selected',
      },
      messageActions: [
        {
          name: 'flagMessage',
          title: 'Flag Message',
        },
        {
          name: 'replyMessage',
          title: 'Reply',
        },
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
    unreadMessagesMap() {
      return this.$store.state.unread_messages;
    }
  },
  watch:{
    chatId(to, from) {
      if(this.roomId !== this.chatId){
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
    if(this.chatId)
      this.roomId = this.chatId;
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
        case 'editMessage':
          this.editMessage(options);
          break;
        case 'replyMessage':
          this.replyMessage(options);
          break;
        case 'deleteMessage':
          this.deleteMessage(options);
          break;
        default:
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
        const formattedRoomStructure = [];
        const userMap = {}
        const fakeUsers = [
          {_id:1,username:"fake1"},
          {_id:2,username:"fake2"},
          {_id:3,username:"fake3"},
        ]
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

        const batchSize = 50;
        const response = await MessageService.fetchMessages(this.roomId, this.offset, batchSize);
        if (!response || !response.data.is_success) {
          this.toastMessage = 'There was an issue fetching new messages!';
          this.showToastError = true;
          this.showToast();
          return;
        }

        // Weak support for rooms with custom bots
        const currentRoom = this.rooms.find((r) => r.roomId === this.roomId);
        this.currentUserId = currentRoom.botId;

        const formattedMessages = [];
        const messages = response.data.messages;
        if (messages.length < 50) {
          this.messagesLoaded = true;
        }
        messages.forEach((m) => {
          formattedMessages.push({
            _id: m.id || '',
            content: m.message || '',
            sender_id: m.sender_id || '',
            date: dateHelpers.convertDate(m.date),
            timestamp: dateHelpers.convertTime(m.date),
            username: m.sender_name, 
            isFlagged: m.is_flagged,
            roomId: this.roomId,
          });
        });
        this.messages = formattedMessages;
        this.offset += messages.length;
      } catch (err) {
        console.error(err);
      }
    },

    // TODO: Clean up beyond here.
    async flagMessage({ roomId, message }) {
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
            this.showToastError = false;
            this.toastMessage = `${trimmedMessage} is successfully flagged!`;
            this.showToast();
          }
        } else {
          this.showToastError = true;
          this.toastMessage = `${trimmedMessage} is already flagged!`;
          this.showToast();
        }
      } catch (err) {
        console.error(err);
      }
    },
    async editMessage({ roomId, message }) {
      try {
        const params = {
          roomId,
          id: message._id,
          content: message.content,
        };
        await MessageService.editMessage(params);
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
    async deleteMessage({ message }) {
      try {
        const params = {
          id: message._id,
        };
        await MessageService.deleteMessage(params);
      } catch (err) {
        console.error(err);
      }
    },
    async changeChat({room}) {
      const newChatId = room.roomId;
      const isGroup = (room.type === 'group-chat');

      if(this.chatId === newChatId) {
        // One could imagine caching messages in the future to speed things up.
        this.fetchMessages();
      } else { 
        // First time through we will update history. This will cause changeChat 
        // to be called a second time where we'll actually fetch the msgs
        this.$router.push({path:'/chat/', query: { chatId: newChatId, isGroup:isGroup || null}});
      }
    },
    async loadOldMessages({
      room,
      options = {},
    }) {
      try {
        const {
          roomId,
        } = room;
        const {
          reset = false,
        } = options;
        this.messagesLoaded = false;
        if (this.messages.length < 50) {
          this.messagesLoaded = true;
          return;
        }
        if (reset) {
          return;
        }
        const {
          limit,
          lastMessage,
          groupView,
        } = this;
        let newMessages = [];
        const params = {
          roomId,
          limit,
          lazy: true,
        };
        this.offset += 50;
        params.offset = this.offset;
        try{
          const data = await MessageService.fetchMessages(params);
          if (data.data.is_success) {
            newMessages = data.data.messages;
          }
          }catch(err){
          console.log(err.response);
          }
        if (!newMessages.length) {
          this.messagesLoaded = true;
          return;
        }
        const formattedMessages = [];
        const formattedRoomStructure = [];
        const users = [];
        newMessages.forEach((d) => {
        if (d.sender_id === this.botId) {
            this.currentUserId = d.sender_id;
          }
          users.push({
            _id: d.id,
            username: d.sender_name,
          });
          formattedMessages.push({
            _id: d.id,
            content: d.message || '',
            sender_id: d.sender_id,
            date: dateHelpers.convertDate(d.date),
            timestamp: dateHelpers.convertTime(d.date),
            isFlagged: d.is_flagged,
            username: d.sender_name,
            saved: false,
            groupId: this.groupId,
          });
        });
        if (groupView) {
          [this.lastMessage] = newMessages;
        }
        formattedRoomStructure.push({
          roomId,
          roomName: room.roomName,
          users,
        });
        if (formattedMessages.length < 50) {
          this.messagesLoaded = true;
        }
        this.messages = [...formattedMessages, ...this.messages];
        this.rooms = formattedRoomStructure;
      } catch (err) {
        console.error(err);
      }
    },
    async sendMessage({ roomId, content, file, replyMessage }) {
      try {
        const { groupView } = this;
        const response = await MessageService.addNewMessage({
          roomId,
          content,
          file,
          replyMessage,
          groupView,
        });
      } catch (err) {
        console.error(err);
      }
    },
    resetChatWidget() {
      this.messages = []
      this.rooms.length = 0;
      this.messages.length = 0;
      this.messagesLoaded = false;
      this.lastMessage = null;
      this.offset = 0;
    },
  },
};
</script>
<style scoped>
.bookmark {
  position: absolute;
  left: 22px;
  width: 12px;
  height: 12px;
}

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
</style>