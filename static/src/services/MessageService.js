import Api from './Api';

export default {
  async addNewMessage({
    roomId,
    content,
  }) {
    try {
      const response = await Api.post('/message', {
        individual: roomId,
        message: content,
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
      const response = await Api.get(`message/individual/${roomId}`, {
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
      const response = await Api.get(`message/chat/${roomId}`, {
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
