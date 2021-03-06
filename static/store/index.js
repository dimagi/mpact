import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        messages: [],
        unread_messages: {},
        active_channel: null,
        websocket: null
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
        SET_WEBSOCKET(state, websocket) {
            this.state.websocket = websocket
        }
    },
    actions: {
        update_messages({commit}, payload) {
            let finalPayload = []
            const msgs = payload.msgs;
            const roomId = payload.roomId;
            msgs.forEach(msg => {
                console.log(msg.room_id,roomId,msg.room_id == roomId);
                if (roomId === '' || msg.room_id === undefined || msg.room_id == roomId) {
                    finalPayload.push(msg);
                }
            });
            commit('SET_MESSAGE', finalPayload)
        },
        update_unread_messages({commit}, payload) {
            commit('SET_UNREAD_MESSAGE', payload)
        },
        update_active_channel({commit}, payload) {
            commit('SET_ACTIVE_CHANNEL', payload)
        },
        update_websocket({commit}, payload) {
            commit('SET_WEBSOCKET', payload)
        }
    },
    modules: {

    }
})