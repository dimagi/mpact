<template>
  <div class='login-body width-404 bg-white border-0'>
    <form @submit.prevent="$emit('moveToNextPage')">
      <h3 class='login-title'>Sign in</h3>
      <p class='country-selection'>
        Please choose your country and enter your full phone number.
      </p>
      <slot />
    </form>
  </div>
</template>
<script>
  export default {
    name: 'Login',
  };
</script>

<style scoped>
  .login-body .login-title {
    color: #222;
    margin: 0 0 20px;
    font-size: 15px;
    font-weight: 700;
    font: 13px/18px Tahoma, sans-serif, Arial, Helvetica;
  }

  .country-selection {
    color: #999;
    margin: 15px 0 30px;
    font-size: 13px;
    line-height: 160%;
  }

  .login-body {
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
</style>