import store from '../../store'
import Api from './Api';

export default {
  async addNewMessage({
    roomId,
    content,
    groupView,
  }) {
    try {
      const response = await Api.post('/messages', {
        room_id: roomId,
        message: content,
        from_group: groupView,
      });
      return response;
    } catch (err) {
      console.error(err);
      throw err;
    }
  },
  async fetchMessages( roomId, offset, limit = 50 ) {
    try {
      const response = await Api.get(`messages/${roomId}`, {
        params: {
          offset,
          limit,
        },
      });
      const currentUnreadMessages = store.state.unread_messages;
      currentUnreadMessages[roomId] = 0
      store.dispatch('update_unread_messages', currentUnreadMessages)
      return response;
    } catch (err) {
      console.error(err);
      throw err;
    }
  },
  async editMessage({
    id,
    content,
  }) {
    try {
      const response = await Api.put('/message', {
        id,
        content,
      });
      return response;
    } catch (err) {
      console.error(err);
      throw err;
    }
  },
  async deleteMessage({
    id,
  }) {
    try {
      const response = await Api.delete('/message', {
        id,
      });
      return response;
    } catch (err) {
      console.error(err);
      throw err;
    }
  },
  async flagMessage({
    message,
    groupId,
  }) {
    try {
      const response = await Api.post('flaggedmessages', {
        message,
        group_id: groupId,
      });
      return response;
    } catch (err) {
      console.error(err);
      throw err;
    }
  },
  async fetchFlaggedMessages({
  }) {
    try {
      const response = await Api.get('flaggedmessages');
      return response;
    } catch (err) {
      console.error(err);
      throw err;
    }
  },
  async unFlagMessage({
    id,
  }) {
    try {
      const response = await Api.delete(`flaggedmessages/${id}`);
      return response;
    } catch (err) {
      console.error(err);
      throw err;
    }
  },
};
