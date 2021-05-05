<template>
  <div class='side-nav h-100'>
    <div class="container py-4 bg-dark text-white">
      <div class="row">
        <div class="col-md sidebar-nav-icon cal_down" @click="downloadSchedules()" title="Download schedules"></div>
        <label class='col-md sidebar-nav-icon cal_up file-upload-label' title='Upload schedules' for="schedule-file">
          <input type="file" id="schedule-file" ref="schedule-file" multiple v-on:change="uploadSchedules()"/>
        </label>
        <div class='col-md sidebar-nav-icon download' @click='exportMessages()' title='Export'></div>
        <div class='col-md sidebar-nav-icon flagged' @click='navigateToFlagged()' title='Flagged messages'></div>
        <div class='col-md sidebar-nav-icon logout' @click='logout()' title='Log out'></div>
      </div>
      <div class="row mt-2">
        <div class="col">
          <div class='text-truncate username text-left'>{{ username }}</div>
        </div>
      </div>
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
import Api from '../services/Api';

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
    async navigateToFlagged() {
      const route = this.$router.resolve({ path: '/flagged-messages' });
      window.open(route.href, '_self');
    },
    async downloadSchedules() {
      try {
        const response = await Api({
          method: 'get',
          url: '/schedules.xlsx',
          responseType: 'blob'
        });
        const blob = new Blob(
            [response.data],
            { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' }
        )
        // https://stackoverflow.com/a/9834261/8207
        const link = document.createElement('a')
        link.href = URL.createObjectURL(blob)
        link.download = 'schedules.xlsx'
        link.click()
        URL.revokeObjectURL(link.href)
      } catch (err) {
        console.error(err);
        throw err;
      }
    },
    async uploadSchedules() {
      const scheduleFile = document.getElementById("schedule-file").files[0];
      const formData = new FormData();
      formData.append("file", scheduleFile);
      const response = await Api.post('/schedule_messages', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log(response);
    },
    async exportMessages() {
      try {
        const response = await Api.get('/messages.csv');
        const blob = new Blob([response.data], { type: 'application/csv' })
        const link = document.createElement('a')
        link.href = URL.createObjectURL(blob)
        link.download = 'messages.csv'
        link.click()
        URL.revokeObjectURL(link.href)
      } catch (err) {
        console.error(err);
        throw err;
      }
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

  .sidebar-nav-icon {
    width: 25px;
    height: 25px;
    margin: 2px;
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
    cursor: pointer;
  }

  .cal_down {
    background-image: url('../assets/cal_down.svg');
  }

  .cal_up {
    background-image: url('../assets/cal_up.svg');
  }

  .download {
    background-image: url('../assets/download.svg');
  }

  .flagged {
    background-image: url('../assets/flag.svg');
  }

  .logout {
    background-image: url('../assets/logout.svg');
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

  /* https://stackoverflow.com/a/25825731/8207 */
  input[type="file"] {
    display: none;
  }

  /* override default margin styling on label */
  label.file-upload-label {
    margin-bottom: 0;
  }
</style>
