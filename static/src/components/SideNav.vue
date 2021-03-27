<template>
  <div class='side-nav h-100'>
    <div class='h3 title w-100 text-center bg-dark text-white px-3 m-0 d-flex align-items-center
    d-flex justify-content-around'>
      <div class='text-truncate username text-left capitalize'>{{ username }}</div>
      <div class='download h-100' @click='exportMessages()' title='Export'></div>
      <div class='bookmarks h-100' @click='navigateToBookmarks()' title='Flagged messages'></div>
      <div class='logout h-100' @click='logout()' title='Log out'></div>
    </div>
    <div class='chat-contacts'>
      <div class='side-nav-row mt-2' v-for='(mainObj, i) in contacts' :key='i'>
        <div
          :class="['w-100 bg-telegram__primary text-white d-flex justify-content-between', { 'active-channel': activeChannel === i }]">
          <div class='btn channel-name text-left box-shadow__none px-0 border-0 rounded-0'
          @click="setActiveChannel(i, mainObj.chat.id); $emit('getGroupMessages', {
              roomName: mainObj.chat.title,
              roomId: mainObj.chat.id
            })" :data-id='mainObj.chat.id'>
            <span class='px-4 text-white'>{{ mainObj.chat.title }} </span>
            <span class='badge alert-info' v-if='unread_messages[mainObj.chat.id]'>{{ unread_messages[mainObj.chat.id]}}</span>
          </div>
          <button class='btn expand-icon box-shadow__none border-0 rounded-0 text-white' type='button'
            :data-id='mainObj.chat.id' :data-target="'#demo-' + i" data-toggle='collapse'>
            <i class='fa'></i>
          </button>
        </div>
        <div class='collapse border-0 bg-white cursor__pointer' :id="'demo-' + i">
          <div v-for='(subObj, j) in mainObj.bot.bot_individuals' :key='j' :data-id='subObj.individual.id'
            :class="['text-telegram__primary', 'pt-2', 'pb-1', 'pl-5', { 'active-chat': activeChat === (i + j) }]"
            @click="setActiveChannel(i, subObj.individual.id); setActiveChat(i + j);
            $emit('getIndividualMessages', {
              roomName: subObj.individual.first_name,
              roomId: subObj.individual.id,
              groupId: mainObj.chat.id
            })">
            {{ subObj.individual.first_name }}
            <span class='badge alert-info' v-if='unread_messages[subObj.individual.id]'>{{ unread_messages[subObj.individual.id]}}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { clearStorage } from '../utils/helpers';
 
export default {
  name: 'side-nav',
  props: ['username', 'contacts'],
  data() {
    return {
      activeChannel: null,
      activeChat: null,
    };
  },
  computed: {
    unread_messages: {
      get() {
        return this.$store.state.unread_messages

      },
    },

  },
  methods: {
    setActiveChannel(i, chatId) {
      this.activeChannel = i;
      this.activeChat = null;
      this.$store.dispatch('update_active_channel', chatId)
    },
    setActiveChat(i) {
      this.activeChat = i;
    },
    async navigateToBookmarks() {
      const route = this.$router.resolve({ path: '/flagged-messages' });
      window.open(route.href, '_self');
    },
    async exportMessages() {
      // navigate to /api/messages.csv
    },
    async logout() {
      try {
        await this.$http.post('logout', {
          refresh_token: `${localStorage.getItem('refreshToken')}`,
        });
        clearStorage();
        this.$router.push('/login');
      } catch (err) {
        console.error(err);
      }
    },
  },
};
</script>

<style scoped>
  .capitalize{
    text-transform: capitalize;
  }
  .side-nav {
    background: var(--bg-light-gray);
    box-shadow: 1px 0px 8px #000;
  }

  .title {
    height: 64px;
  }

  .chat-contacts {
    height: calc(100vh - 64px);
    overflow-y: auto;
  }

  .chat-contacts::-webkit-scrollbar {
    width: 12px;
  }

  .chat-contacts::-webkit-scrollbar-track {
    -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
    box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
    border-radius: 10px;
  }

  .chat-contacts::-webkit-scrollbar-thumb {
    border-radius: 10px;
    box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.5);
    -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.5);
  }

  [aria-expanded='false'] .fa:before,
  .fa:before {
    content: '+';
  }

  [aria-expanded='true'] .fa:before {
    content: '-';
  }

  .username {
    width: 85%;
  }

  .download {
    width: 15%;
    background-size: 20px;
    background-position: center;
    background-repeat: no-repeat;
    background-image: url('../assets/download.svg');
    cursor: pointer;
  }

  .bookmarks {
    width: 15%;
    background-size: 20px;
    background-position: center;
    background-repeat: no-repeat;
    background-image: url('../assets/bookmark.svg');
    cursor: pointer;
  }

  .logout {
    width: 15%;
    background-size: 20px;
    background-position: center;
    background-repeat: no-repeat;
    background-image: url('../assets/logout.svg');
    cursor: pointer;
  }

  .channel-name {
    flex-basis: 75%;
  }

  .expand-icon {
    flex-basis: 25%;
  }

  .active-channel {
    background: #5682a385 !important;
  }

  .active-chat {
    background: #e5effa !important;
  }
</style>
