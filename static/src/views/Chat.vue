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
          :message-actions='messageActions' @fetch-messages='loadOldMessages($event)' :showNewMessagesDivider='showNewMessagesDivider'
          @send-message='sendMessage($event)' @message-action-handler='messageActionHandler($event)'>
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
      messages: [],
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
    };
  },
  async mounted() {
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
      } catch (err) {
        console.error(err);
      }
    },
    async flagMessage({ roomId, message }) {
      try {
        const params = {
          roomId,
          messageId: message._id,
          firstName: message.sender_id,
          message: message.content,
          groupId: message.groupId || this.groupId,
          isGroup: this.groupView,
        };
        if (!params.isGroup) {
          const senderDetails = this.contacts.find(
            (contact) => contact.chat.id === params.groupId,
          );
          if (senderDetails) {
            if (senderDetails.bot.id === message.sender_id) {
              params.firstName = senderDetails.bot.username;
            } else {
              const userDetails = senderDetails.bot.bot_individuals.find(
                (individual) => individual.individual.id === message.sender_id,
              );
              if (userDetails) {
                params.firstName = userDetails.individual.first_name;
              }
            }
          }
        }
        const trimmedMessage = message.content.trim().length > 25 ? `${message.content.trim().slice(0, 25)}...` : message.content.trim();
        if (!message.isFlagged) {
          const result = await MessageService.flagMessage(params);
          if (result && result.data.is_success) {
            const messageIndex = this.messages.findIndex(
              (m) => m._id === params.messageId,
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
        if (groupView && lastMessage) {
          params.offset = lastMessage.id;
        } else {
          this.offset += 50;
          params.offset = this.offset;
        }
        if (groupView) {
          const data = await MessageService.fetchGroupMessages(params);
          if (data.data.is_success) {
            newMessages = data.data.messages;
          }
        } else {
          const data = await MessageService.getIndividualMessages(params);
          if (data.data.is_success) {
            newMessages = data.data.messages;
          }
        }
        if (!newMessages.length) {
          this.messagesLoaded = true;
          return;
        }
        const formattedMessages = [];
        const formattedRoomStructure = [];
        const users = [];
        newMessages.forEach((d) => {
          if (!groupView) {
            if (d.individual !== d.sender) {
              this.currentUserId = d.sender;
            }
          }
          users.push({
            _id: d.id,
            username: d.sender,
          });
          formattedMessages.push({
            _id: d.id,
            content: d.message || '',
            sender_id: d.sender,
            date: dateHelpers.convertDate(d.date),
            timestamp: dateHelpers.convertTime(d.date),
            isFlagged: d.is_flagged,
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
          this.currentUserId = roomId;
          const newMessages = data.data.messages;
          if (newMessages.length < 50) {
            this.messagesLoaded = true;
          }
          newMessages.forEach((d) => {
            if (d.individual !== d.sender) {
              this.currentUserId = d.sender;
            }
            formattedMessages.push({
              _id: d.id,
              content: d.message || '',
              sender_id: d.sender,
              date: dateHelpers.convertDate(d.date),
              timestamp: dateHelpers.convertTime(d.date),
              isFlagged: d.is_flagged,
              saved: false,
              groupId,
            });
          });
          formattedRoomStructure.push({
            roomId,
            roomName,
            users: [],
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
        if (this.messages.length && lazy && lastMessage) {
          params.offset = lastMessage.id;
        }
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
            if (d.individual !== d.sender) {
              this.currentUserId = d.sender;
            }
            this.roomName = d.sender;
            userList.push({
              _id: d.id,
              username: d.sender,
            });
            formattedMessages.push({
              _id: d.id || '',
              content: d.message || '',
              sender_id: d.sender || '',
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
    async sendMessage({
      roomId,
      content,
      file,
      replyMessage,
    }) {
      try {
        const response = await MessageService.addNewMessage({
          roomId,
          content,
          file,
          replyMessage,
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
