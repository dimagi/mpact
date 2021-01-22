<template>
  <div class='side-nav h-100'>
    <div
      class='h3 title w-100 text-center bg-dark text-white px-3 m-0 d-flex align-items-center d-flex justify-content-around'>
      <div class='text-truncate username text-left'>{{ userName }}</div>
      <div class='logout h-100' @click='logout()' title='logout'></div>
    </div>
    <div class='chat-contacts'>
      <div class='side-nav-row mt-2' v-for='(mainObj, index) in contactsList' :key='index'>
        <button type='button'
          class='btn border-0 w-100 bg-telegram-primary border-0 rounded-0 text-white d-flex justify-content-between'
          data-toggle='collapse' :data-target="'#demo-' + index"
          @click="$emit('getGroupMessages', { roomName: mainObj.chat.title, roomId: mainObj.chat.id })">
          <span>{{ mainObj.chat.title }}</span><i class='fa'></i>
        </button>
        <div class='collapse border-0 bg-white cursor__pointer' :id="'demo-' + index">
          <div v-for='(subObj, index) in mainObj.bot.bot_individuals' :key='index'
            class='text-telegram-primary pt-2 pb-1 pl-5'
            @click="$emit('getIndividualMessages', { roomName: subObj.individual.first_name, roomId :subObj.individual.id } )">
            {{ subObj.individual.first_name }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  export default {
    name: 'side-nav',
    props: ['userName', 'contactsList'],
    data() {
      return {
        data: {},
      };
    },
    methods: {
      async logout() {
        try {
          await this.$http.get('/logout');
          localStorage.removeItem('username');
          localStorage.removeItem('Token');
          this.$router.push('/login');
        } catch (err) {
          console.error(err);
        }
      },
    },
  };
</script>

<style scoped>
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

  .logout {
    width: 15%;
    background-size: 20px 20px;
    background-position: center;
    background-repeat: no-repeat;
    background-image: url('../assets/logout.svg');
    cursor: pointer;
  }
</style>