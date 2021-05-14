<template>
  <div class="flagged-messages-list">
    <b-table-lite small responsive striped hover :items="flaggedMessages" :fields="columns">
      <template #cell(delete)="data">
        <div @click="unflagMessage(data.item._id)" class='cursor__pointer'>❌</div>
      </template>
      <template #cell(roomName)="data">
        <router-link exact-path :to="{path: '/chat/',
          query: { chatId: data.item.roomId, messageId: data.item.messageId || null}}">
            <span>
              {{data.item.roomName}}
            </span>
          </router-link>
      </template>
      <template #cell(content)="data">
        <router-link exact-path :to="{path: '/chat/',
          query: { chatId: data.item.roomId, messageId: data.item.messageId || null}}">
            <span>
              {{data.item.content}}
            </span>
          </router-link>
      </template>
    </b-table-lite>
  </div>
</template>
<script>
import MessageService from '../services/MessageService';

export default {
  name: 'flagged-messages-list',
  props: {
    flaggedMessages: {type: Array, required: true}
  },
  data() {
    return {
      columns: [
        { label: "", key:"delete"},
        { label: "Date", key:"date"},
        { label: "Sender", key:"firstName"},
        { label: "Chat", key:"roomName"},
        { label: "Message", key:"content"},
      ],
    }
  },
  methods: {
    async unflagMessage(id){
      try {
        const response = await MessageService.unFlagMessage({id: id});
        if(response.status == 200){
          const index = this.flaggedMessages.map(m => {return m._id}).indexOf(id);
          this.flaggedMessages.splice(index,1);
          this.$toasts.success('Successfully unflagged message');
        }        
      } catch (err) {
        this.$toasts.error('Something went wrong while trying to unflag the message');
        console.error(err);
      }
    }
  }
};

</script>

<style scoped>
.flagged-messages-list {
  font-style: normal;
  text-align: left;
}
</style>
