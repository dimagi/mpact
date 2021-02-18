<template>
  <div class='auth'>
    <div class='auth-container vw-100 vh-100 position-relative'>
      <header>
        <div class='login-header width-404 position-absolute mx-auto left-right_0 d-grid
        justify-content-between align-items-center'>
          <div class='login-header-logo d-flex align-items-center'>
            <i class='logo'></i>
            <h1 class='logo-text text-white d-flex align-items-center'>
              mpact-Telegram
            </h1>
          </div>
          <div :class="['login-header-btn', 'text-white', 'cursor__pointer', { 'text-danger': !nextButtonValidation }]"
            @click='nextButtonValidation && moveToNextPage()'>
            Next
            <i class='next-btn'></i>
          </div>
        </div>
      </header>
      <section class='position-relative'>
        <div class='position-absolute mx-auto left-right_0 w-100 d-grid
        justify-content-center login-top'>
          <Login v-if='showLoginPage' @moveToNextPage='nextButtonValidation && moveToNextPage()'>
            <vue-tel-input v-model='phoneNumber' v-bind='telephoneProps'
            @validate='validatePhoneNumber($event)' />
          </Login>
          <OTP @hideOtpComponent='showOTPPage = !showOTPPage; showLoginPage = !showLoginPage;' v-if='showOTPPage'
            @receiveOtpText='validateOTP($event)' :phone='phoneNumber' />
          <TwoFactorAuth v-if='show2FaPage' @receive2FaText='validate2FaText($event)' />
          <div class='login-footer width-404 text-center' v-show='!isInfoHide'>
            <div class='footer-1'>
              Welcome to the official mpact-Telegram web-client.
            </div>
            <div class='footer-2 cursor__pointer' @click='isInfoHide = !isInfoHide'
            v-show='!isInfoHide'>
              Learn more
            </div>
          </div>
          <Info v-if='isInfoHide' @closeInfoComponent='isInfoHide = false'
          :receiveClass='showOTPPage' />
        </div>
      </section>
      <Toast :text='toastInput' :hasError='toastError' />
    </div>
  </div>
</template>
<script>
const Login = () => import('../components/Login.vue');
const Info = () => import('../components/TelegramInfo.vue');
const OTP = () => import('../components/OTP.vue');
const Toast = () => import('../components/Toast.vue');
const TwoFactorAuth = () => import('../components/TwoFactorAuth.vue');

export default {
  components: {
    Login,
    Info,
    OTP,
    Toast,
    TwoFactorAuth,
  },
  mounted() {
    this.removeCookies();
  },
  data() {
    return {
      isInfoHide: false,
      showOTPPage: false,
      showLoginPage: true,
      show2FaPage: false,
      nextButtonValidation: false,
      phoneNumber: '',
      formattedPhoneNumber: '',
      otpNumber: '',
      phoneCodeHash: '',
      toastInput: '',
      toastError: false,
      telephoneProps: {
        required: true,
        mode: 'international',
      },
    };
  },
  methods: {
    removeCookies() {
      const res = document.cookie;
      const multiple = res.split(';');
      for (let i = 0; i < multiple.length; i += 1) {
        const key = multiple[i].split('=');
        document.cookie = `${key[0]} =; expires = Thu, 01 Jan 1970 00:00:00 UTC`;
      }
    },
    async moveToNextPage() {
      if (this.showLoginPage) {
        try {
          this.toastError = false;
          const data = await this.$http.post('/login', {
            phone: this.formattedPhoneNumber,
          });
          if (data && data.data && data.data.is_success) {
            this.phoneCodeHash = data.data.phone_code_hash;
            this.toastInput = 'OTP is sent to registered number';
            this.showLoginPage = false;
            this.show2FaPage = false;
            this.nextButtonValidation = false;
            this.showOTPPage = true;
            this.showNotification();
          }
        } catch (err) {
          this.toastError = true;
          this.nextButtonValidation = true;
          this.toastInput = 'Phone number is not registered';
          this.showNotification();
        }
      } else if (this.showOTPPage) {
        this.toastInput = 'Verifing the OTP';
        this.toastError = false;
        this.showNotification();
        try {
          const data = await this.$http.post('/login', {
            phone: this.formattedPhoneNumber,
            code: this.otpNumber,
            phone_code_hash: this.phoneCodeHash,
          });
          if (data && data.data && data.data.is_success) {
            const {
              is_2FA_enabled: is2FAEnabled = false,
            } = data.data;
            this.showOTPPage = false;
            this.showLoginPage = false;
            this.nextButtonValidation = false;
            this.show2FaPage = true;
            localStorage.setItem('userId', data.data.id || '');
            localStorage.setItem('username', data.data.first_name || '');
            localStorage.setItem('Token', data.data.token || '');
            if (!is2FAEnabled) {
              this.$router.push('/chat');
            }
          }
        } catch (err) {
          this.toastInput = 'Entered wrong OTP';
          this.toastError = true;
          this.showNotification();
        }
      } else {
        this.toastError = false;
        this.toastInput = 'Verifing the 2FA code';
        this.showNotification();
        try {
          const data = await this.$http.post('/login', {
            phone: this.formattedPhoneNumber,
            password: this.twoFactorAuthCode,
          });
          if (data && data.data && data.data.is_success) {
            localStorage.removeItem('username');
            localStorage.setItem('userId', data.data.id || '');
            localStorage.setItem('username', data.data.first_name || '');
            localStorage.setItem('Token', data.data.token || '');
            this.$router.push('/chat');
          }
        } catch (err) {
          this.toastInput = 'Entered wrong code';
          this.toastError = true;
          this.showNotification();
        }
      }
    },
    validatePhoneNumber(obj) {
      this.nextButtonValidation = obj.valid;
      this.formattedPhoneNumber = obj.number.e164;
    },
    validateOTP(obj) {
      this.nextButtonValidation = obj.target.value.toString().length >= 5;
      this.otpNumber = obj.target.value.toString();
      if (obj.keyCode === 13 && this.nextButtonValidation) {
        this.moveToNextPage();
      }
    },
    validate2FaText(obj) {
      this.nextButtonValidation = obj.target.value.toString().length >= 5;
      this.twoFactorAuthCode = obj.target.value.toString();
      if (obj.keyCode === 13 && this.nextButtonValidation) {
        this.moveToNextPage();
      }
    },
    showNotification() {
      this.$('.toast').toast('show');
    },
  },
};
</script>
<style scoped>
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
