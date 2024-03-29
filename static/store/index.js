import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        messages: [],
        unread_messages: {},
        active_channel: null,
    },
    mutations: {
        SET_MESSAGE(state, messages) {
            this.state.messages = messages
        },
        SET_UNREAD_MESSAGE(state, unread_messages) {
            this.state.unread_messages = unread_messages
        },
        SET_ACTIVE_CHANNEL(state, active_channel) {
            this.state.active_channel = active_channel
        },
    },
    actions: {
        update_messages({commit}, payload) {
            let finalPayload = []
            const msgs = payload.msgs;
            msgs.forEach(msg => {
                // Only keep messages for the current room. As mentioned elsewhere, 
                // we could imagine caching messags, but we refetch every time we 
                // change a room at the moment.
                if (!msg.senderId) {
                    msg.senderId = msg.sender_id;
                }
                if(msg.roomId == this.state.active_channel) { 
                    finalPayload.push(msg);
                }
            });
            commit('SET_MESSAGE', finalPayload)
        },
        update_unread_messages({commit}, payload) {
            commit('SET_UNREAD_MESSAGE', payload)
        },
        update_active_channel({commit}, payload) {
            commit('SET_ACTIVE_CHANNEL', payload.activeChannel)
        },
        update_websocket({commit}, payload) {
            commit('SET_WEBSOCKET', payload)
        }
    },
    modules: {

    }
})