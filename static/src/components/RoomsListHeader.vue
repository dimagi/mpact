<template>
  <div class="row p-4 bg-dark text-white mx-0">
    
    <div class="col rooms-list-header-icon cal_down" @click="downloadSchedules()" title="Download schedules"></div>
    <label class='col rooms-list-header-icon cal_up file-upload-label' title='Upload schedules' for="schedule-file">
      <input type="file" id="schedule-file" ref="schedule-file" multiple v-on:change="uploadSchedules()"/>
    </label>
    <label class='col rooms-list-header-icon participants file-upload-label' title='Upload Study Participants' for="participant-file">
      <input type="file" id="participant-file" ref="participant-file" multiple v-on:change="uploadParticipants()"/>
    </label>
    <div class='col rooms-list-header-icon download' @click='exportMessages()' title='Export'></div>
    <div class='col rooms-list-header-icon logout' @click='logout()' title='Log out'></div>
  </div>
</template>
<script>
import Api from '../services/Api';
import { clearStorage } from '../utils/helpers';

export default {
  name: 'rooms-list-header',
  methods: {
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
        if (err.response.status == 400) {
          this.$toasts.error(err.response.data.message)
        } else {
          throw err;
        }
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
    async uploadParticipants() {
      const participantFile = document.getElementById("participant-file").files[0];
      const formData = new FormData();
      formData.append("file", participantFile);
      const response = await Api.post('/study_participants.xlsx', formData, {
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
  .rooms-list-header-icon {
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

  .logout {
    background-image: url('../assets/logout.svg');
  }

  .participants {
    background-image: url('../assets/user_add.svg');
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
