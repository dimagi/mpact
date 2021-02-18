<template>
  <div class='otp-page width-404 bg-white border-0'>
    <div class='phone-number'>{{ phone }}</div>
    <div class='edit-number text-center cursor__pointer' @click="$emit('hideOtpComponent')">
      Edit phone number
    </div>
    <div class='otp-info text-center'>
      We've sent the code to the Telegram app on your mobile device.
    </div>
    <div class='otp-info text-center'>Please enter the code below.</div>
    <input type='text' placeholder='Enter your code'
      class='d-flex justify-content-center text-center input custom-input border-0 mx-auto'
      @keyup="$emit('receiveOtpText', $event)" />
  </div>
</template>
<script>
export default {
  name: 'OTP',
  props: ['phone'],
};
</script>

<style scoped>
  .otp-page {
    padding: 44px 65px;
    -webkit-box-shadow: 0 1px 1px rgba(97, 127, 152, 0.2),
      1px 0 0 rgba(97, 127, 152, 0.1), -1px 0 0 rgba(97, 127, 152, 0.1);
    -moz-box-shadow: 0 1px 1px rgba(97, 127, 152, 0.2),
      1px 0 0 rgba(97, 127, 152, 0.1), -1px 0 0 rgba(97, 127, 152, 0.1);
    box-shadow: 0 1px 1px rgba(97, 127, 152, 0.2), 1px 0 0 rgba(97, 127, 152, 0.1),
      -1px 0 0 rgba(97, 127, 152, 0.1);
    border-radius: 2px;
    max-width: none;
  }

  .otp-page .phone-number {
    color: #222;
    font-size: 15px;
    font-weight: 700;
    text-align: center;
    font: 13px/18px Tahoma, sans-serif, Arial, Helvetica;
  }

  .otp-page .otp-info {
    color: #999;
    margin: 15px 0;
    line-height: 160%;
    font: 13px/18px Tahoma, sans-serif, Arial, Helvetica;
  }

  .otp-page .custom-input {
    border-bottom: 1px solid #000 !important;
  }

  .edit-number {
    color: #3a6d99;
    text-decoration: none;
    margin: 5px 0 15px;
    font: 13px/18px Tahoma, sans-serif, Arial, Helvetica;
  }
</style>
