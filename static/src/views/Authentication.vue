<template>
  <div class='auth'>
    <div class='auth-container vw-100 vh-100 position-relative'>
      <header>
        <div
          class='login-header width-404 position-absolute mx-auto left-right_0 d-grid
        justify-content-between align-items-center'
        >
          <div class='login-header-logo d-flex align-items-center'>
            <i class='logo'></i>
            <h1 class='logo-text text-white d-flex align-items-center'>
              mpact-Telegram
            </h1>
          </div>
        </div>
      </header>
      <section class='position-relative'>
        <div
          class='position-absolute mx-auto left-right_0 w-100 d-grid
        justify-content-center login-top'
        >
          <div class='login-box'>
            <form @submit.prevent="loginUser">
              <label for='name' class='login-user-label'>Username:</label>
              <input id='name' class='login-user login-input' v-model="userName" type='text' required />
              <br />
              <label for='password' class='login-user-label'>Password:</label>
              <input id='password' class='login-password login-input' v-model="password" type='password' required />
              <div class='login-box-btn-div'>
                <button type='submit' class='login-btn'>Log in</button>
              </div>
            </form>
          </div>
        </div>
      </section>
      <Toast :text="toastInput" :hasError="toastError" />
    </div>
  </div>
</template>
<script>
const Toast = () => import('../components/Toast.vue');
import { clearStorage } from '../utils/helpers'
import jwt from 'jwt-decode';

export default {
  components: {
    Toast,
  },
  mounted() {
    this.removeCookies();
  },
  data() {
    return {
      toastInput: '',
      toastError: false,
      userName: '',
      password: '',
    };
  },
  methods: {
    loginUser(event) {
      event.preventDefault();
      try {
        if (this.userName && this.password) {
          this.$http
            .post('token/', {
              username: this.userName,
              password: this.password,
            })
            .then((res) => {
              const decoded = jwt(res.data.access);
              localStorage.setItem('username', decoded.username);
              localStorage.setItem('Token', res.data.access);
              localStorage.setItem('refreshToken', res.data.refresh);
              this.$router.push('/chat');
            })
            .catch((err) => {
              clearStorage();
              this.toastError = true;
              this.toastInput = 'Incorrect username or password';
              this.showNotification();
            });
        }
      } catch (err) {
        console.log(err);
      }
    },

    removeCookies() {
      const res = document.cookie;
      const multiple = res.split(';');
      for (let i = 0; i < multiple.length; i += 1) {
        const key = multiple[i].split('=');
        document.cookie = `${key[0]} =; expires = Thu, 01 Jan 1970 00:00:00 UTC`;
      }
    },
    showNotification() {
      this.$('.toast').toast('show');
    },
  },
};
</script>
<style scoped>
  .login-box {
    background: white;
    padding: 20px 40px;
    width: 450px;
  }
  .login-user-label {
    display: block;
  }
  .login-input {
    border: 1px solid #ccc;
    padding: 8px;
    width: 100%;
    margin-bottom: 15px;
    border-radius: 5px;
  }
  .login-btn {
    background: #79aec8;
    padding: 10px 15px;
    border: none;
    border-radius: 4px;
    color: #fff;
    cursor: pointer;
  }
  .login-box-btn-div {
    text-align: center;
    margin: 15px 0;
  }
  header {
    height: 226px;
    background-color: var(--telegram-primary);
  }

  section {
    background-color: var(--telegram-secondary);
    height: calc(100vh - 226px);
  }

  .login-header {
    grid-template-columns: auto 78px;
    height: 75px;
    top: 95px;
  }

  .login-header-logo {
    padding: 23px 15px 22px;
    width: 140px;
    flex-direction: row;
  }

  .login-header-btn {
    justify-self: center;
    font-size: 13px;
    font: 13px/18px Tahoma, sans-serif, Arial, Helvetica;
    font-weight: 700;
    line-height: 20px;
  }

  .logo {
    width: 30px;
    height: 30px;
    display: inline-block;
    vertical-align: top;
    margin-right: 18px;
    background-image: url('../assets/telegram.png');
    background-repeat: no-repeat;
    background-position: -5px -10px;
    font-size: 13px;
    font: 13px/18px Tahoma, sans-serif, Arial, Helvetica;
  }

  .logo-text {
    width: 62px;
    height: 29px;
    display: inline-block;
    vertical-align: middle;
    background-repeat: no-repeat;
    background-position: 0 0;
    margin-top: 1px;
    white-space: nowrap;
    font-size: 14px;
    font: 13px/18px Tahoma, sans-serif, Arial, Helvetica;
  }

  .next-btn {
    width: 7px;
    height: 12px;
    display: inline-block;
    vertical-align: middle;
    margin-left: 12px;
    margin-top: -1px;
    background-image: url('../assets/telegram.png');
    background-repeat: no-repeat;
    background-position: -18px -50px;
  }

  .login-footer {
    color: #84a2bc;
    font-size: 13px;
    line-height: 16px;
    margin-top: 25px;
    top: 432px;
  }

  .login-top {
    top: -56px;
  }

  .footer-2 {
    color: var(--telegram-primary);
  }

  .footer-2:hover {
    text-decoration: underline;
  }

  .about-shown {
    margin-top: 25px;
  }

  .toast {
    top: 0;
    left: 0;
    right: 0;
  }
</style>
