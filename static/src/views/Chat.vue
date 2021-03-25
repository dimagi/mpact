<template>
  <div class='vw-100 vh-100'>
    <div class='row m-0 p-0'>
      <div class='col-2 p-0 z-index__25'>
        <side-nav :username='username' :contacts='contacts' @getIndividualMessages='getIndividualMessages($event)'
          @getGroupMessages='getGroupMessages($event)' />
      </div>
      <Toast :text='toastMessage' :hasError='showToastError' />
      <div class='col-10 p-0'>
        <chat-window height='100vh' class='chat-widget-1' :currentUserId='currentUserId' :rooms='rooms'
          :messages='messages' :single-room='hideSideNav' :messages-loaded='messagesLoaded' :styles='styles'
          :message-actions='messageActions' @fetch-messages='messages.length>=50 ? loadOldMessages($event) : null' :showNewMessagesDivider='showNewMessagesDivider'
          @send-message='sendMessage($event)' @message-action-handler='messageActionHandler($event)'
          :show-files='false' :show-audio='false'>
          <template #dropdown-icon>
            <svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='currentColor' viewBox='0 0 16 16'>
              <path fill-rule='evenodd' d='M1.646 4.646a.5.5 0 0 1 .708 0L8
              10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6
                6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z' />
            </svg>
          </template>
        </chat-window>
      </div>
    </div>
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
      currentUserId: 1,
      contacts: [],
      messagesLoaded: false,
      hideSideNav: true,
      roomName: '',
      limit: 50,
      groupView: true,
      groupId: null,
      offset: 0,
      lastMessage: null,
      showNewMessagesDivider: false,
      messageActions: [
        {
          name: 'flagMessage',
          title: 'Flag Message',
        },
        {
          name: 'editMessage',
          title: 'Edit Message',
          onlyMe: true,
        },
        {
          name: 'replyMessage',
          title: 'Reply',
        },
        {
          name: 'deleteMessage',
          title: 'Delete Message',
          onlyMe: true,
        },
      ],
      styles: {
        icons: {
          dropdownMessageBackground: 'transparent',
        },
      },
      botId: '',
    };
  },
  computed: {
    messages: {
      get() {
        return this.$store.state.messages

      },
      set(payload) {
        this.$store.dispatch('update_messages', payload)
      }
    },
  },
  async mounted() {
    this.resetChatWidget();
    await this.getContacts();
    this.username = localStorage.getItem('username') || '';
    this.selectedRoom = this.$route.query.roomId || '';
    this.groupBookmark = this.$route.query.isGroup === 'true' || false;
    this.groupId = this.$route.query.groupId || null;
    const selectedDiv = document.querySelector(`div[data-id='${this.selectedRoom}']`);
    const groupButton = document.querySelector(`button[data-id='${this.groupId}']`);
    if (this.groupBookmark && (this.groupId === this.selectedRoom)) {
      if (selectedDiv) {
        selectedDiv.click();
      }
    } else if (groupButton && selectedDiv) {
      groupButton.click();
      selectedDiv.click();
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
    async getContacts() {
      try {
        const data = await this.$http.get('/dialogs');
        this.contacts = data.data.dialogs;
        this.botId = this.contacts[0].bot.id
        const unreadMessagesObj = {}
        this.contacts.forEach((oneGroup) => {
          oneGroup.bot.bot_individuals.forEach((oneIndividual) => {
            unreadMessagesObj[oneIndividual.individual.id] = oneIndividual.individual.unread_count;
        });
        unreadMessagesObj[oneGroup.chat.id] = oneGroup.chat.unread_count;
        })
        this.$store.dispatch('update_unread_messages', unreadMessagesObj)
      } catch (err) {
        console.error(err);
      }
    },
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
          const data = await MessageService.getIndividualMessages(params);
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
    async getIndividualMessages({
      roomName,
      roomId,
      groupId,
    }) {
      try {
        this.groupId = groupId;
        this.messagesLoaded = false;
        this.offset = 0;
        const {
          limit,
          offset,
        } = this;
        const params = {
          roomId,
          limit,
          offset,
        };
        this.resetChatWidget();
        const data = await MessageService.getIndividualMessages(params);
        if (data.data.is_success) {
          this.groupView = false;
          const formattedMessages = [];
          const formattedRoomStructure = [];
          const users = [];
          this.currentUserId = roomId;
          const newMessages = data.data.messages;
          if (newMessages.length < 50) {
            this.messagesLoaded = true;
          }
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
              groupId,
            });
          });
          formattedRoomStructure.push({
            roomId,
            roomName,
            users,
          });
          this.messages = formattedMessages;
          this.rooms = formattedRoomStructure;
        }
      } catch (err) {
        console.error(err);
      }
    },
    async getGroupMessages({
      roomName,
      roomId,
      lazy = false,
    }) {
      this.groupId = roomId;
      try {
        const {
          limit,
          lastMessage,
        } = this;
        if (!this.groupView) {
          this.lastMessage = null;
        }
        this.groupView = true;
        const params = {
          roomId,
          limit,
        };
        this.offset = 0;
        params.offset = this.offset;
        this.resetChatWidget();
        const data = await MessageService.fetchGroupMessages(params);
        if (data && data.data.is_success) {
          this.currentUserId = '';
          const formattedMessages = [];
          const formattedRoomStructure = [];
          const userList = [];
          const newMessages = data.data.messages;
          if (newMessages.length < 50) {
            this.messagesLoaded = true;
          }
          newMessages.forEach((d) => {
            if (d.sender_id === this.botId) {
              this.currentUserId = d.sender_id;
            }
            this.roomName = d.sender_name;
            userList.push({
              _id: d.id,
              username: d.sender_name,
            });
            formattedMessages.push({
              _id: d.id || '',
              content: d.message || '',
              sender_id: d.sender_id || '',
              date: dateHelpers.convertDate(d.date),
              timestamp: dateHelpers.convertTime(d.date),
              username: this.roomName,
              isFlagged: d.is_flagged,
              saved: false,
              groupId: this.groupId,
            });
          });
          formattedRoomStructure.push({
            roomId,
            roomName,
            users: userList,
          });
          this.messages = formattedMessages;
          this.rooms = formattedRoomStructure;
          [this.lastMessage] = newMessages;
        }
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
        if (response && response.status === 200) {
          this.messagesLoaded = false;
          const { message } = response.data;
          const { date } = message;
          const newMessages = [...this.messages, {
            _id: message.id,
            individual: roomId,
            content,
            sender_id: this.currentUserId,
            date: dateHelpers.convertDate(date),
            timestamp: dateHelpers.convertTime(date),
            isFlagged: false,
            username: message.sender,
          }];
          this.messages = newMessages;
          this.messagesLoaded = true;
        }
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
</style>