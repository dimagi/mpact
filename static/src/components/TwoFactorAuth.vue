<template>
  <div class='f2a-body width-404 bg-white border-0'>
    <form @submit.prevent=''>
      <h3 class='f2a-title'>Password</h3>
      <p class='country-selection text-center'>
        You have enabled two-step verification, so your account is protected
        with an additional password.
      </p>
      <input type='password' placeholder='Enter your code'
        class='d-flex justify-content-center text-center input custom-input border-0 mx-auto'
        @keyup="$emit('receive2FaText', $event)" />
    </form>
  </div>
</template>
<script>
export default {
  name: 'two-factor-auth',
};
</script>

<style scoped>
  .f2a-title {
    color: #222;
    margin: 0 0 20px;
    font-size: 15px;
    font-weight: 700;
    font: 13px/18px Tahoma, sans-serif, Arial, Helvetica;
  }

  .f2a-body .country-selection {
    color: #999;
    margin: 15px 0 30px;
    font-size: 13px;
    line-height: 160%;
  }

  .f2a-body {
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

  .f2a-body .custom-input {
    border-bottom: 1px solid #000 !important;
  }
</style>
