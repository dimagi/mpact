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
  async getIndividualMessages({
    roomId,
    offset,
    limit = 50,
  }) {
    try {
      const response = await Api.get(`messages/${roomId}`, {
        params: {
          offset,
          limit,
        },
      });
      return response;
    } catch (err) {
      console.error(err);
      throw err;
    }
  },
  async fetchGroupMessages({
    roomId,
    offset,
    limit,
  }) {
    try {
      const response = await Api.get(`messages/${roomId}`, {
        params: {
          offset,
          limit,
        },
      });
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
    roomId,
    messageId,
    firstName,
    message,
    groupId,
    isGroup,
  }) {
    try {
      const response = await Api.post('flaggedmessages', {
        room_id: roomId,
        message_id: messageId,
        first_name: firstName,
        message,
        group_id: groupId,
        is_group: isGroup,
      });
      return response;
    } catch (err) {
      console.error(err);
      throw err;
    }
  },
  async fetchFlaggedMessages({
    offset = 0,
    limit = 50,
  }) {
    try {
      const response = await Api.get('flaggedmessages', {
        params: {
          offset,
          limit,
        },
      });
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
