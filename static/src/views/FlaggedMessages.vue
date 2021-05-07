<template>
  <div class='vw-100 vh-100'>
    <div class='row m-0 p-0'>
      <div class='col-10 p-0'>
        <chat-window height='100vh' class='bookmarks-widget-1' v-bind='chatProps' :messages-loaded='chatProps.messagesLoaded'>
          <template #message='{message}'>
            <div :id='message._id' class='message-container'>
              <div class='message-card cursor__pointer'>
                <div class='username'>
                  <router-link exact-path :to="{path: '/chat',
                  query: { roomId: message.roomId, messageId: message.messageId, isGroup:
                  message.isGroup, groupId: message.groupId || null}}">
                    <span>
                      {{message.firstName}}
                    </span>
                  </router-link>
                </div>
                <div>
                  <router-link exact-path :to="{path: '/chat',
                  query: { roomId: message.roomId, messageId: message.messageId, isGroup:
                  message.isGroup, groupId: message.groupId || null, }}">
                    <span class='message-content cursor__pointer'>
                      {{message.content}}
                    </span>
                  </router-link>
                </div>
                <div class='text-timestamp'>
                  <span>{{message.timestamp}}</span>
                </div>
                <div class='svg-button message-options cursor__pointer' :data-id='message._id'
                  @click='currentMessage = message' title='Unflag Message'
                  data-toggle='modal' data-target='#deleteWarning'>
                  <svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' fill='currentColor'
                    viewBox='0 0 16 16'>
                    <path d='M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1
                    .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5
                    0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z' />
                  </svg>
                </div>
              </div>
            </div>
          </template>
        </chat-window>
        <warning-modal v-if='currentMessage' :message='currentMessage' @unFlagMessage='unFlagMessage($event)' />
      </div>
    </div>
  </div>
</template>
<script>
import Vue from 'vue';
import MessageService from '../services/MessageService';
import { convertDate, convertTime } from '../utils/helpers';
import 'vue-advanced-chat/dist/vue-advanced-chat.css';
import '../styles/message.css';

const ChatWindow = () => import('vue-advanced-chat');

Vue.component('warning-modal', {
  props: ['message'],
  template: `
    <div class='modal fade' id='deleteWarning' tabindex='-1' role='dialog' aria-labelledby='deleteWarning'
      aria-hidden='true'>
      <div class='modal-dialog' role='document'>
        <div class='modal-content'>
          <div class='modal-header'>
            <h5 class='modal-title' id='exampleModalLabel'>
            {{message.content.trim().length > 25 ? message.content.trim().slice(0, 75) + '...' : message.content.trim()}}
            </h5>
            <button type='button' class='close' data-dismiss='modal' aria-label='Close'>
              <span aria-hidden='true'>&times;</span>
            </button>
          </div>
          <div class='modal-body'>
            Are you sure you want to unflag this message?
          </div>
          <div class='modal-footer'>
            <button type='button' class='btn btn-secondary' data-dismiss='modal'>Close</button>
            <button type='button' class='btn btn-danger' data-dismiss='modal' @click='$emit("unFlagMessage", {id: message._id})'>Delete</button>
          </div>
        </div>
      </div>
    </div>
  `,
});

export default {
  name: 'flagged_messages',
  components: {
    ChatWindow,
  },
  data() {
    return {
      lastMessage: null,
      currentMessage: null,
      chatProps: {
        currentUserId: 1,
        rooms: [],
        messages: [],
        singleRoom: true,
        roomsLoaded: true,
        textMessages: {
          ROOMS_EMPTY: 'No flagged messages to show',
          ROOM_EMPTY: 'No flagged messages to show',
          MESSAGES_EMPTY: 'No flagged messages to show',
          CONVERSATION_STARTED: '',
        },
        showFooter: false,
        showEmojis: false,
        showReactionEmojis: false,
        messagesLoaded: false,
        styles: {},
        showNewMessagesDivider: false,
      },
    };
  },
  mounted() {
    try {
      this.fetchFlaggedMessages();
    } catch (err) {
      console.error(err);
    }
  },
  methods: {
    async fetchFlaggedMessages() {
      try {
        const result = await MessageService.fetchFlaggedMessages({});
        if (result && result.data.flagged_messages) {
          const formattedMessages = [];
          result.data.flagged_messages.forEach((d) => {
            formattedMessages.push({
              _id: d.id,
              messageId: d.message.id,
              firstName: d.message.sender_name || '',
              content: d.message.message || '',
              sender_id: d.message.sender_id || 1,
              date: convertDate(d.date),
              timestamp: convertTime(d.date),
              roomId: d.message.room_id,
              isGroup: d.message.from_group || false,
              groupId: d.group_id || null,
            });
          });
          this.chatProps.messages = formattedMessages;
          this.chatProps.messagesLoaded = true;
          this.chatProps.rooms = [{
            roomId: 1,
            roomName: 'Flagged Messages',
            users: [],
          }];
          // this.showToastError = false;
          // this.toastMessage = 'Fetched all flagged messages';
          // this.showToast();
        }
      } catch (err) {
        console.error(err);
      }
    },
    async unFlagMessage({ id }) {
      try {
        this.currentMessage = null;
        const params = {
          id,
        };
        const response = await MessageService.unFlagMessage(params);
        if (response && response.data.is_success) {
          const updatedMessages = this.chatProps.messages.filter((message) => message._id !== id);
          this.chatProps.messages = updatedMessages;
          // this.toastMessage = 'Message is unflagged';
          // this.showToast();
        }
      } catch (err) {
        console.error(err);
      }
    },
  },
};
</script>
